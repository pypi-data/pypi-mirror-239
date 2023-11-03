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


from typing import Optional
from pydantic import BaseModel, Field, StrictStr, validator

class AddOrgUserCommand(BaseModel):
    """
    AddOrgUserCommand
    """
    login_or_email: Optional[StrictStr] = Field(None, alias="loginOrEmail")
    role: Optional[StrictStr] = None
    __properties = ["loginOrEmail", "role"]

    @validator('role')
    def role_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('Viewer', 'Editor', 'Admin'):
            raise ValueError("must be one of enum values ('Viewer', 'Editor', 'Admin')")
        return value

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
    def from_json(cls, json_str: str) -> AddOrgUserCommand:
        """Create an instance of AddOrgUserCommand from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> AddOrgUserCommand:
        """Create an instance of AddOrgUserCommand from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return AddOrgUserCommand.parse_obj(obj)

        _obj = AddOrgUserCommand.parse_obj({
            "login_or_email": obj.get("loginOrEmail"),
            "role": obj.get("role")
        })
        return _obj


