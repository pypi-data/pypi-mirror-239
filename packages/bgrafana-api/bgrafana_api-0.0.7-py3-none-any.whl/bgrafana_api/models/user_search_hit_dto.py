# coding: utf-8

"""
    Grafana HTTP API.

    The Grafana backend exposes an HTTP API, the same API is used by the frontend to do everything from saving dashboards, creating users and updating data sources.

    The version of the OpenAPI document: 0.0.1
    Contact: hello@grafana.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, StrictBool, StrictInt, StrictStr, conlist

class UserSearchHitDTO(BaseModel):
    """
    UserSearchHitDTO
    """
    auth_labels: Optional[conlist(StrictStr)] = Field(None, alias="authLabels")
    avatar_url: Optional[StrictStr] = Field(None, alias="avatarUrl")
    email: Optional[StrictStr] = None
    id: Optional[StrictInt] = None
    is_admin: Optional[StrictBool] = Field(None, alias="isAdmin")
    is_disabled: Optional[StrictBool] = Field(None, alias="isDisabled")
    last_seen_at: Optional[datetime] = Field(None, alias="lastSeenAt")
    last_seen_at_age: Optional[StrictStr] = Field(None, alias="lastSeenAtAge")
    login: Optional[StrictStr] = None
    name: Optional[StrictStr] = None
    __properties = ["authLabels", "avatarUrl", "email", "id", "isAdmin", "isDisabled", "lastSeenAt", "lastSeenAtAge", "login", "name"]

    class Config:
        """Pydantic configuration"""
        allow_population_by_field_name = True
        validate_assignment = True

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.dict(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> UserSearchHitDTO:
        """Create an instance of UserSearchHitDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> UserSearchHitDTO:
        """Create an instance of UserSearchHitDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return UserSearchHitDTO.parse_obj(obj)

        _obj = UserSearchHitDTO.parse_obj({
            "auth_labels": obj.get("authLabels"),
            "avatar_url": obj.get("avatarUrl"),
            "email": obj.get("email"),
            "id": obj.get("id"),
            "is_admin": obj.get("isAdmin"),
            "is_disabled": obj.get("isDisabled"),
            "last_seen_at": obj.get("lastSeenAt"),
            "last_seen_at_age": obj.get("lastSeenAtAge"),
            "login": obj.get("login"),
            "name": obj.get("name")
        })
        return _obj


