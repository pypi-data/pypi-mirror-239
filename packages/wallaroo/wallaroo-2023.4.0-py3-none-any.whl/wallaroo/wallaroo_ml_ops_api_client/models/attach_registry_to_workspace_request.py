from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="AttachRegistryToWorkspaceRequest")


@attr.s(auto_attribs=True)
class AttachRegistryToWorkspaceRequest:
    """ The required information for creating a Model Registry

        Attributes:
            registry_id (str):
            workspace_id (int):
     """

    registry_id: str
    workspace_id: int
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        registry_id = self.registry_id
        workspace_id = self.workspace_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "registry_id": registry_id,
            "workspace_id": workspace_id,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        registry_id = d.pop("registry_id")

        workspace_id = d.pop("workspace_id")

        attach_registry_to_workspace_request = cls(
            registry_id=registry_id,
            workspace_id=workspace_id,
        )

        attach_registry_to_workspace_request.additional_properties = d
        return attach_registry_to_workspace_request

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
