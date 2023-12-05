from typing import List, Dict, Union, Optional

from flask import url_for
from pydantic import BaseModel, computed_field, Field


class UserSchema(BaseModel):
    id: int
    available_option_list: Optional[List[str]] = []
    current_options: Optional[List[Dict[str, Union[int, str]]]] = Field(
        alias="options", default=[]
    )

    class Config:
        orm_mode = True
        from_attributes = True

    @computed_field
    @property
    def options(
        self,
    ) -> Optional[List[Dict[str, Union[Optional[int], Optional[str]]]]]:
        result = []

        for option in self.current_options:
            for k in option.keys():
                if k in self.available_option_list:
                    result.append(option)

        return result

    def model_dump(self, **kwargs):
        data = super(UserSchema, self).model_dump(**kwargs)

        for attr in list(data):
            if attr in ["available_option_list", "current_options"]:
                del data[attr]
        return data


class UserLink(BaseModel):
    id: int

    @computed_field
    @property
    def link(self) -> str:
        return url_for("api.auth_user", user_id=self.id, _external=True)

    class Config:
        orm_mode = True
        from_attributes = True


class UsersSchema(BaseModel):
    users: List[UserLink]
