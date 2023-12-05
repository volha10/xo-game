from typing import List, Dict, Union, Optional

from flask import url_for
from pydantic import BaseModel, computed_field


class UserSchema(BaseModel):
    id: int
    available_option_list: Optional[List[str]] = []
    profile_options: Optional[Dict[str, Union[int, str]]] = {}

    class Config:
        orm_mode = True
        from_attributes = True

    @computed_field
    @property
    def options(
        self,
    ) -> Optional[Dict[str, Union[Optional[int], Optional[str]]]]:
        result = {}

        if not self.profile_options:
            return result

        for k, v in self.profile_options.items():
            if k in self.available_option_list:
                result[k] = v

        return result

    def model_dump(self, **kwargs):
        data = super(UserSchema, self).model_dump(**kwargs)

        for attr in list(data):
            if attr in ["available_option_list", "profile_options"]:
                del data[attr]
        return data


class UserLink(BaseModel):
    id: int

    @computed_field
    @property
    def link(self) -> str:
        return url_for("api.auth_user_id", user_id=self.id, _external=True)

    class Config:
        orm_mode = True
        from_attributes = True


class UsersSchema(BaseModel):
    users: List[UserLink]
