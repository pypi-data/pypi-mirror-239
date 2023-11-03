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
from pydantic import BaseModel, Field, StrictBool, StrictInt, StrictStr

class UpdateFolderCommand(BaseModel):
    """
    UpdateFolderCommand captures the information required by the folder service to update a folder. Use Move to update a folder's parent folder.  # noqa: E501
    """
    description: Optional[StrictStr] = Field(None, description="NewDescription it's an optional parameter used for overriding the existing folder description")
    overwrite: Optional[StrictBool] = Field(None, description="Overwrite only used by the legacy folder implementation")
    title: Optional[StrictStr] = Field(None, description="NewTitle it's an optional parameter used for overriding the existing folder title")
    uid: Optional[StrictStr] = Field(None, description="NewUID it's an optional parameter used for overriding the existing folder UID")
    version: Optional[StrictInt] = Field(None, description="Version only used by the legacy folder implementation")
    __properties = ["description", "overwrite", "title", "uid", "version"]

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
    def from_json(cls, json_str: str) -> UpdateFolderCommand:
        """Create an instance of UpdateFolderCommand from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> UpdateFolderCommand:
        """Create an instance of UpdateFolderCommand from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return UpdateFolderCommand.parse_obj(obj)

        _obj = UpdateFolderCommand.parse_obj({
            "description": obj.get("description"),
            "overwrite": obj.get("overwrite"),
            "title": obj.get("title"),
            "uid": obj.get("uid"),
            "version": obj.get("version")
        })
        return _obj


