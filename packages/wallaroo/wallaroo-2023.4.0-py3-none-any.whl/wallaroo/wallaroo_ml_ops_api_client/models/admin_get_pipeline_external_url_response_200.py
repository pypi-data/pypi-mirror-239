from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="AdminGetPipelineExternalUrlResponse200")


@attr.s(auto_attribs=True)
class AdminGetPipelineExternalUrlResponse200:
    """  Response to pipeline URL-related operations.

        Attributes:
            url (str):  Requested URL.
     """

    url: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        url = self.url

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "url": url,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        url = d.pop("url")

        admin_get_pipeline_external_url_response_200 = cls(
            url=url,
        )

        admin_get_pipeline_external_url_response_200.additional_properties = d
        return admin_get_pipeline_external_url_response_200

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
