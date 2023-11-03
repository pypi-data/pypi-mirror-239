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
from pydantic import BaseModel, Field, StrictInt, StrictStr

class SearchResultItem(BaseModel):
    """
    SearchResultItem
    """
    action: Optional[StrictStr] = None
    basic_role: Optional[StrictStr] = Field(None, alias="basicRole")
    org_id: Optional[StrictInt] = Field(None, alias="orgId")
    role_name: Optional[StrictStr] = Field(None, alias="roleName")
    scope: Optional[StrictStr] = None
    team_id: Optional[StrictInt] = Field(None, alias="teamId")
    user_id: Optional[StrictInt] = Field(None, alias="userId")
    version: Optional[StrictInt] = None
    __properties = ["action", "basicRole", "orgId", "roleName", "scope", "teamId", "userId", "version"]

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
    def from_json(cls, json_str: str) -> SearchResultItem:
        """Create an instance of SearchResultItem from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> SearchResultItem:
        """Create an instance of SearchResultItem from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return SearchResultItem.parse_obj(obj)

        _obj = SearchResultItem.parse_obj({
            "action": obj.get("action"),
            "basic_role": obj.get("basicRole"),
            "org_id": obj.get("orgId"),
            "role_name": obj.get("roleName"),
            "scope": obj.get("scope"),
            "team_id": obj.get("teamId"),
            "user_id": obj.get("userId"),
            "version": obj.get("version")
        })
        return _obj


