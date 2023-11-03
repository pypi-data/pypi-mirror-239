from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="StatusGetDeploymentResponse200HelmItemInfoLabels")


@attr.s(auto_attribs=True)
class StatusGetDeploymentResponse200HelmItemInfoLabels:
    """  Kubernetes labels for the pod

     """

    additional_properties: Dict[str, str] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        
        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        status_get_deployment_response_200_helm_item_info_labels = cls(
        )


        status_get_deployment_response_200_helm_item_info_labels.additional_properties = d
        return status_get_deployment_response_200_helm_item_info_labels

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> str:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: str) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
