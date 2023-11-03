from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
  from ..models.users_query_response_200_users import \
      UsersQueryResponse200Users





T = TypeVar("T", bound="UsersQueryResponse200")


@attr.s(auto_attribs=True)
class UsersQueryResponse200:
    """  Users that match the query.

        Attributes:
            users (UsersQueryResponse200Users):  User details keyed by User ID.
     """

    users: 'UsersQueryResponse200Users'
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        users = self.users.to_dict()


        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "users": users,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.users_query_response_200_users import \
            UsersQueryResponse200Users
        d = src_dict.copy()
        users = UsersQueryResponse200Users.from_dict(d.pop("users"))




        users_query_response_200 = cls(
            users=users,
        )

        users_query_response_200.additional_properties = d
        return users_query_response_200

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
