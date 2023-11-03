from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="AssaysSetActiveJsonBody")


@attr.s(auto_attribs=True)
class AssaysSetActiveJsonBody:
    """  Request to activate or deactivate an assay.

        Attributes:
            id (int):  Assay identifier.
            active (bool):  Flag to set assay as active or inactive.
     """

    id: int
    active: bool
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        active = self.active

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "active": active,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        active = d.pop("active")

        assays_set_active_json_body = cls(
            id=id,
            active=active,
        )

        assays_set_active_json_body.additional_properties = d
        return assays_set_active_json_body

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
