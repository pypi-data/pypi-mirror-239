from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="ListRegistryModelsRequest")


@attr.s(auto_attribs=True)
class ListRegistryModelsRequest:
    """ Payload for the List Registry Models call.

        Attributes:
            registry_id (str):
     """

    registry_id: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        registry_id = self.registry_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "registry_id": registry_id,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        registry_id = d.pop("registry_id")

        list_registry_models_request = cls(
            registry_id=registry_id,
        )

        list_registry_models_request.additional_properties = d
        return list_registry_models_request

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
