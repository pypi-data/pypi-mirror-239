from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
  from ..models.status_get_deployment_response_200_helm_item_info import \
      StatusGetDeploymentResponse200HelmItemInfo





T = TypeVar("T", bound="StatusGetDeploymentResponse200HelmItem")


@attr.s(auto_attribs=True)
class StatusGetDeploymentResponse200HelmItem:
    """  Helm runner deployment status.

        Attributes:
            info (StatusGetDeploymentResponse200HelmItemInfo):
     """

    info: 'StatusGetDeploymentResponse200HelmItemInfo'
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        info = self.info.to_dict()


        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "info": info,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.status_get_deployment_response_200_helm_item_info import \
            StatusGetDeploymentResponse200HelmItemInfo
        d = src_dict.copy()
        info = StatusGetDeploymentResponse200HelmItemInfo.from_dict(d.pop("info"))




        status_get_deployment_response_200_helm_item = cls(
            info=info,
        )

        status_get_deployment_response_200_helm_item.additional_properties = d
        return status_get_deployment_response_200_helm_item

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
