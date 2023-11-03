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
from pydantic import BaseModel, StrictStr
from bgrafana_api.models.alert_managers_result import AlertManagersResult

class GettableAlertmanagers(BaseModel):
    """
    GettableAlertmanagers
    """
    data: Optional[AlertManagersResult] = None
    status: Optional[StrictStr] = None
    __properties = ["data", "status"]

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
    def from_json(cls, json_str: str) -> GettableAlertmanagers:
        """Create an instance of GettableAlertmanagers from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of data
        if self.data:
            _dict['data'] = self.data.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> GettableAlertmanagers:
        """Create an instance of GettableAlertmanagers from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return GettableAlertmanagers.parse_obj(obj)

        _obj = GettableAlertmanagers.parse_obj({
            "data": AlertManagersResult.from_dict(obj.get("data")) if obj.get("data") is not None else None,
            "status": obj.get("status")
        })
        return _obj


