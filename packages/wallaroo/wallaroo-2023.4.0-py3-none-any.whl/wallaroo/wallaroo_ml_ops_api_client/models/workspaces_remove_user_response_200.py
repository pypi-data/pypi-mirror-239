from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="WorkspacesRemoveUserResponse200")


@attr.s(auto_attribs=True)
class WorkspacesRemoveUserResponse200:
    """  Response from removing a User from a Workspace

        Attributes:
            affected_rows (int):  The number of rows affected by the removal operation. This should be either 0 or 1.
     """

    affected_rows: int
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        affected_rows = self.affected_rows

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "affected_rows": affected_rows,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        affected_rows = d.pop("affected_rows")

        workspaces_remove_user_response_200 = cls(
            affected_rows=affected_rows,
        )

        workspaces_remove_user_response_200.additional_properties = d
        return workspaces_remove_user_response_200

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
