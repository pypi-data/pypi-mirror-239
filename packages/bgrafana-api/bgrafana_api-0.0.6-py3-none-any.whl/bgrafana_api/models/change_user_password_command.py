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
from pydantic import BaseModel, Field, StrictStr

class ChangeUserPasswordCommand(BaseModel):
    """
    ChangeUserPasswordCommand
    """
    new_password: Optional[StrictStr] = Field(None, alias="newPassword")
    old_password: Optional[StrictStr] = Field(None, alias="oldPassword")
    __properties = ["newPassword", "oldPassword"]

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
    def from_json(cls, json_str: str) -> ChangeUserPasswordCommand:
        """Create an instance of ChangeUserPasswordCommand from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ChangeUserPasswordCommand:
        """Create an instance of ChangeUserPasswordCommand from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return ChangeUserPasswordCommand.parse_obj(obj)

        _obj = ChangeUserPasswordCommand.parse_obj({
            "new_password": obj.get("newPassword"),
            "old_password": obj.get("oldPassword")
        })
        return _obj


