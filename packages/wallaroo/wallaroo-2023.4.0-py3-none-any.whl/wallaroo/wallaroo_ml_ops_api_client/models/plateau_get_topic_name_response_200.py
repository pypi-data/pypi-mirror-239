from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="PlateauGetTopicNameResponse200")


@attr.s(auto_attribs=True)
class PlateauGetTopicNameResponse200:
    """  Successfully retrieved topic name.

        Attributes:
            topic_name (str):  Topic name.
     """

    topic_name: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        topic_name = self.topic_name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "topic_name": topic_name,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        topic_name = d.pop("topic_name")

        plateau_get_topic_name_response_200 = cls(
            topic_name=topic_name,
        )

        plateau_get_topic_name_response_200.additional_properties = d
        return plateau_get_topic_name_response_200

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
