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
from pydantic import BaseModel, StrictBool, StrictStr
from bgrafana_api.models.http_client_config import HTTPClientConfig
from bgrafana_api.models.url import URL

class WebexConfig(BaseModel):
    """
    WebexConfig
    """
    api_url: Optional[URL] = None
    http_config: Optional[HTTPClientConfig] = None
    message: Optional[StrictStr] = None
    room_id: Optional[StrictStr] = None
    send_resolved: Optional[StrictBool] = None
    __properties = ["api_url", "http_config", "message", "room_id", "send_resolved"]

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
    def from_json(cls, json_str: str) -> WebexConfig:
        """Create an instance of WebexConfig from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of api_url
        if self.api_url:
            _dict['api_url'] = self.api_url.to_dict()
        # override the default output from pydantic by calling `to_dict()` of http_config
        if self.http_config:
            _dict['http_config'] = self.http_config.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> WebexConfig:
        """Create an instance of WebexConfig from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return WebexConfig.parse_obj(obj)

        _obj = WebexConfig.parse_obj({
            "api_url": URL.from_dict(obj.get("api_url")) if obj.get("api_url") is not None else None,
            "http_config": HTTPClientConfig.from_dict(obj.get("http_config")) if obj.get("http_config") is not None else None,
            "message": obj.get("message"),
            "room_id": obj.get("room_id"),
            "send_resolved": obj.get("send_resolved")
        })
        return _obj


