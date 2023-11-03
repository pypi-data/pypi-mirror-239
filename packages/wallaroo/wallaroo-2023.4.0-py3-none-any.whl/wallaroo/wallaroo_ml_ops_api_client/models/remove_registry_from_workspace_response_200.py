from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="RemoveRegistryFromWorkspaceResponse200")


@attr.s(auto_attribs=True)
class RemoveRegistryFromWorkspaceResponse200:
    """ 
        Attributes:
            id (str): The unique identifier for the Model Registry
            workspace_id (int): The unique identifier for the workspace.
     """

    id: str
    workspace_id: int
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        workspace_id = self.workspace_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "workspace_id": workspace_id,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        workspace_id = d.pop("workspace_id")

        remove_registry_from_workspace_response_200 = cls(
            id=id,
            workspace_id=workspace_id,
        )

        remove_registry_from_workspace_response_200.additional_properties = d
        return remove_registry_from_workspace_response_200

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
