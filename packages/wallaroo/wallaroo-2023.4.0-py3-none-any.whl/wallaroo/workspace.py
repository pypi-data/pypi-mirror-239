import json
from typing import TYPE_CHECKING, Any, Dict, List, Optional, cast

import requests

from wallaroo.wallaroo_ml_ops_api_client.models.workspaces_create_response_200 import (
    WorkspacesCreateResponse200,
)

from . import queries
from .connection import Connection, ConnectionList
from .model import Model, ModelList
from .object import *
from .pipeline import Pipeline
from .user import User
from .user_type import UserType
from .version import _user_agent
from .wallaroo_ml_ops_api_client.api.workspace import workspaces_create
from .wallaroo_ml_ops_api_client.models import workspaces_create_json_body

if TYPE_CHECKING:
    # Imports that happen below in methods to fix circular import dependency
    # issues need to also be specified here to satisfy mypy type checking.
    from .client import Client


class Workspace(Object):
    """Workspace provides a user and visibility context for access to models and pipelines."""

    def __init__(
        self, client: Optional["Client"], data: Dict[str, Any], standalone=False
    ) -> None:
        assert client is not None
        self.client = client
        #        data = {"name": workspace_name, "owner": owner_user_id}
        super().__init__(gql_client=client._gql_client, data=data)

    def __repr__(self) -> str:
        return str(self.to_json())

    def _fetch_attributes(self) -> Dict[str, Any]:
        """Fetches all member data from the GraphQL API."""
        data = self._gql_client.execute(
            gql.gql(queries.named("WorkspaceById")),
            variable_values={"id": self.id()},
        )["workspace_by_pk"]

        return data

    def _fill(self, data: Dict[str, Any]) -> None:
        """Fills an object given a response dictionary from the GraphQL API.

        Only the primary key member must be present; other members will be
        filled in via rehydration if their corresponding member function is
        called.
        """

        for required_attribute in ["id"]:
            if required_attribute not in data:
                raise RequiredAttributeMissing(
                    self.__class__.__name__, required_attribute
                )
        # Required
        self._id = data["id"]

        # Optional
        self._name = value_if_present(data, "name")
        self._archived = value_if_present(data, "archived")
        self._created_at = value_if_present(data, "created_at")
        self._created_by = value_if_present(data, "created_by")
        self._models = value_if_present(data, "models")
        self._pipelines = value_if_present(data, "pipelines")
        self._users = value_if_present(data, "users")

    def to_json(self):
        return {
            "name": self.name(),
            "id": self.id(),
            "archived": self.archived(),
            "created_by": self.created_by(),
            "created_at": self.created_at(),
            "models": self.models(),
            "pipelines": self.pipelines(),
        }

    @staticmethod
    def _get_user_default_workspace(client):
        res = client._gql_client.execute(
            gql.gql(queries.named("UserDefaultWorkspace")),
            variable_values={"user_id": client.auth.user_id()},
        )
        if res["user_default_workspace"] == []:
            return None
        else:
            return Workspace(client, res["user_default_workspace"][0]["workspace"])

    @staticmethod
    def _create_user_default_workspace(client) -> "Workspace":
        res = client._gql_client.execute(
            gql.gql(queries.named("CreateDefaultUserWorkspace")),
            variable_values={
                "user_id": client.auth.user_id(),
                "workspace_name": f"{client.auth.user_email()} - Default Workspace",
                "user_type": UserType.OWNER.name,
            },
        )
        return Workspace(client, res["insert_workspace_one"])

    @staticmethod
    def _create_workspace(client: "Client", name: str):
        body = workspaces_create_json_body.WorkspacesCreateJsonBody(name)
        res = workspaces_create.sync(client=client.mlops(), json_body=body)

        if not isinstance(res, WorkspacesCreateResponse200):
            raise Exception("Failed to create workspace.")

        if res is None:
            raise Exception("Failed to create workspace.")

        return Workspace(client, {"id": res.workspace_id})

    def id(self) -> int:
        return self._id

    @rehydrate("_name")
    def name(self) -> str:
        return cast(str, self._name)

    @rehydrate("_archived")
    def archived(self) -> bool:
        return cast(bool, self._archived)

    @rehydrate("_created_at")
    def created_at(self) -> str:
        return cast(str, self._created_at)

    @rehydrate("_created_by")
    def created_by(self) -> str:
        return cast(str, self._created_by)

    @rehydrate("_models")
    def models(self) -> ModelList:
        """
        Returns a List of Models objects that have been created in this workspace.
        """
        self._fill(self._fetch_attributes())
        return cast(
            ModelList,
            list(
                map(
                    lambda m: Model(self.client, data=m),
                    cast(List[Dict], self._models),
                )
            ),
        )

    @rehydrate("_pipelines")
    def pipelines(self) -> List[Pipeline]:
        self._fill(self._fetch_attributes())
        return cast(
            List[Pipeline],
            list(
                map(
                    lambda m: Pipeline(self.client, data=m),
                    cast(List[Dict], self._pipelines),
                )
            ),
        )

    @rehydrate("_users")
    def users(self) -> List[User]:
        return cast(
            List[User],
            list(
                map(
                    lambda u: self.client._get_user_by_id(u["user_id"]),
                    cast(List[Dict], self._users),
                )
            ),
        )

    def add_user(self, user_email: str) -> "Workspace":
        """Add a user to workspace as participant"""
        user = self.client.get_user_by_email(user_email)
        if user is None:
            raise EntityNotFoundError("User", {"email": user_email})
        if user.email() in [u.email() for u in self.users()]:
            raise Exception(
                f"User {user.email()}, already exists in workspace {self.name()}"
            )
        return self._add_user(user, UserType.COLLABORATOR)

    def add_owner(self, user_email: str) -> "Workspace":
        """Add a user to workspace as owner"""

        user = self.client.get_user_by_email(user_email)
        if user is None:
            raise EntityNotFoundError("User", {"email": user_email})

        return self._add_user(user, UserType.OWNER)

    def _add_user(self, user: User, user_type: UserType) -> "Workspace":
        headers = {
            "authorization": self.client.auth._bearer_token_str(),
            "user-agent": _user_agent,
        }
        invite = requests.post(
            f"{self.client.api_endpoint}/v1/api/workspaces/add_user",
            data=json.dumps(
                {
                    "email": user.email(),
                    "workspace_id": self._id,
                    "user_id": user.id(),
                    "url": "http://localhost:3000",
                    "user_type": user_type,
                }
            ),
            headers=headers,
        )
        if invite.status_code > 299:
            raise Exception(f"Failed to invite: {user.id()} to workspace: {self._id}")
        self._fill(data={"id": self._id})
        return self

    def remove_user(self, user_email: str):
        user = self.client.get_user_by_email(user_email)
        assert user is not None
        if user.id() == self.client.auth.user_id():
            default_workspace = self._get_user_default_workspace(self.client)
            if default_workspace.id() == self.id():
                raise Exception("User cannot be removed from their default workspace")

        if len(self.users()) <= 1:
            raise Exception("Last user of a workspace cannot be removed")

        res = self.client._gql_client.execute(
            gql.gql(queries.named("DeleteWorkspaceUser")),
            variable_values={"user_id": user.id(), "workspace_id": self.id()},
        )
        if user.id() == self.client.auth.user_id():
            self._fill({"id": default_workspace.id()})
        else:
            self._rehydrate()

    def list_connections(self) -> ConnectionList:
        """Return a list of Connections available in this Workspace.
        :return: List of Connections in this Workspace.
        """

        return Connection.list_connections(self.client, self.id())

    def add_connection(self, name: str):
        """Adds an existing Connection with the given name to this Workspace."""

        connection = Connection.get_connection(self.client, name=name)
        connection.add_connection_to_workspace(self.id())

    def remove_connection(self, name: str):
        """Removes a Connection with the given name from this Workspace."""

        connection = Connection.get_connection(self.client, name=name)
        connection.remove_connection_from_workspace(self.id())


class Workspaces(List[Workspace]):
    """Wraps a list of workspaces for display."""

    @staticmethod
    def _format_users(users: List[User]) -> List[str]:
        return [u.email() for u in users]

    def _repr_html_(self) -> str:
        rows = [
            f"""
        <tr >
            <td>{r.name()}</td>
            <td>{r.created_at()[:19].replace("T", " ")}</td>
            <td>{Workspaces._format_users(r.users())}</td>
            <td>{len(r.models())}</td>
            <td>{len(r.pipelines())}</td>
        </tr>
        """
            for r in self
        ]
        table = """
        <table>
            <tr>
                <th>Name</th>
                <th>Created At</th>
                <th>Users</th>
                <th>Models</th>
                <th>Pipelines</th>
            </tr>
            {0}
        </table>
        """.format(
            "\n".join(rows)
        )
        return table
