from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="ConnectionsRemoveFromWorkspaceJsonBody")


@attr.s(auto_attribs=True)
class ConnectionsRemoveFromWorkspaceJsonBody:
    """  Request to remove a Connection from Workspace

        Attributes:
            workspace_id (int):  ID of the workspace to remove a connection from
            connection_id (str):  ID of the connection to remove from a workspace
     """

    workspace_id: int
    connection_id: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        workspace_id = self.workspace_id
        connection_id = self.connection_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "workspace_id": workspace_id,
            "connection_id": connection_id,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        workspace_id = d.pop("workspace_id")

        connection_id = d.pop("connection_id")

        connections_remove_from_workspace_json_body = cls(
            workspace_id=workspace_id,
            connection_id=connection_id,
        )

        connections_remove_from_workspace_json_body.additional_properties = d
        return connections_remove_from_workspace_json_body

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
