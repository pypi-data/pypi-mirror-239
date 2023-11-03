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


from typing import Any, Dict, Optional
from pydantic import BaseModel, Field, StrictBool, StrictStr

class AddDataSourceCommand(BaseModel):
    """
    Also acts as api DTO  # noqa: E501
    """
    access: Optional[StrictStr] = None
    basic_auth: Optional[StrictBool] = Field(None, alias="basicAuth")
    basic_auth_user: Optional[StrictStr] = Field(None, alias="basicAuthUser")
    database: Optional[StrictStr] = None
    is_default: Optional[StrictBool] = Field(None, alias="isDefault")
    json_data: Optional[Dict[str, Any]] = Field(None, alias="jsonData")
    name: Optional[StrictStr] = None
    secure_json_data: Optional[Dict[str, StrictStr]] = Field(None, alias="secureJsonData")
    type: Optional[StrictStr] = None
    uid: Optional[StrictStr] = None
    url: Optional[StrictStr] = None
    user: Optional[StrictStr] = None
    with_credentials: Optional[StrictBool] = Field(None, alias="withCredentials")
    __properties = ["access", "basicAuth", "basicAuthUser", "database", "isDefault", "jsonData", "name", "secureJsonData", "type", "uid", "url", "user", "withCredentials"]

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
    def from_json(cls, json_str: str) -> AddDataSourceCommand:
        """Create an instance of AddDataSourceCommand from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> AddDataSourceCommand:
        """Create an instance of AddDataSourceCommand from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return AddDataSourceCommand.parse_obj(obj)

        _obj = AddDataSourceCommand.parse_obj({
            "access": obj.get("access"),
            "basic_auth": obj.get("basicAuth"),
            "basic_auth_user": obj.get("basicAuthUser"),
            "database": obj.get("database"),
            "is_default": obj.get("isDefault"),
            "json_data": obj.get("jsonData"),
            "name": obj.get("name"),
            "secure_json_data": obj.get("secureJsonData"),
            "type": obj.get("type"),
            "uid": obj.get("uid"),
            "url": obj.get("url"),
            "user": obj.get("user"),
            "with_credentials": obj.get("withCredentials")
        })
        return _obj


