from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="DbfsListResponseFile")


@attr.s(auto_attribs=True)
class DbfsListResponseFile:
    """ A dbfs file entry

        Attributes:
            file_size (int):
            is_dir (bool):
            modification_time (int):
            path (str):
     """

    file_size: int
    is_dir: bool
    modification_time: int
    path: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        file_size = self.file_size
        is_dir = self.is_dir
        modification_time = self.modification_time
        path = self.path

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "file_size": file_size,
            "is_dir": is_dir,
            "modification_time": modification_time,
            "path": path,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        file_size = d.pop("file_size")

        is_dir = d.pop("is_dir")

        modification_time = d.pop("modification_time")

        path = d.pop("path")

        dbfs_list_response_file = cls(
            file_size=file_size,
            is_dir=is_dir,
            modification_time=modification_time,
            path=path,
        )

        dbfs_list_response_file.additional_properties = d
        return dbfs_list_response_file

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
