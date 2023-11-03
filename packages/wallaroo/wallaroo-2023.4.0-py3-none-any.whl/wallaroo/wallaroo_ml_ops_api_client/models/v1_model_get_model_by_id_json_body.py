from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="V1ModelGetModelByIdJsonBody")


@attr.s(auto_attribs=True)
class V1ModelGetModelByIdJsonBody:
    """  The Request body for /models/get_by_id

        Attributes:
            id (int):  The Model ID
     """

    id: int
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        v1_model_get_model_by_id_json_body = cls(
            id=id,
        )

        v1_model_get_model_by_id_json_body.additional_properties = d
        return v1_model_get_model_by_id_json_body

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
