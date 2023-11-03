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


from typing import Dict, Optional
from pydantic import BaseModel, StrictBool, StrictStr
from bgrafana_api.models.http_client_config import HTTPClientConfig
from bgrafana_api.models.url import URL

class VictorOpsConfig(BaseModel):
    """
    VictorOpsConfig
    """
    api_key: Optional[StrictStr] = None
    api_key_file: Optional[StrictStr] = None
    api_url: Optional[URL] = None
    custom_fields: Optional[Dict[str, StrictStr]] = None
    entity_display_name: Optional[StrictStr] = None
    http_config: Optional[HTTPClientConfig] = None
    message_type: Optional[StrictStr] = None
    monitoring_tool: Optional[StrictStr] = None
    routing_key: Optional[StrictStr] = None
    send_resolved: Optional[StrictBool] = None
    state_message: Optional[StrictStr] = None
    __properties = ["api_key", "api_key_file", "api_url", "custom_fields", "entity_display_name", "http_config", "message_type", "monitoring_tool", "routing_key", "send_resolved", "state_message"]

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
    def from_json(cls, json_str: str) -> VictorOpsConfig:
        """Create an instance of VictorOpsConfig from a JSON string"""
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
    def from_dict(cls, obj: dict) -> VictorOpsConfig:
        """Create an instance of VictorOpsConfig from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return VictorOpsConfig.parse_obj(obj)

        _obj = VictorOpsConfig.parse_obj({
            "api_key": obj.get("api_key"),
            "api_key_file": obj.get("api_key_file"),
            "api_url": URL.from_dict(obj.get("api_url")) if obj.get("api_url") is not None else None,
            "custom_fields": obj.get("custom_fields"),
            "entity_display_name": obj.get("entity_display_name"),
            "http_config": HTTPClientConfig.from_dict(obj.get("http_config")) if obj.get("http_config") is not None else None,
            "message_type": obj.get("message_type"),
            "monitoring_tool": obj.get("monitoring_tool"),
            "routing_key": obj.get("routing_key"),
            "send_resolved": obj.get("send_resolved"),
            "state_message": obj.get("state_message")
        })
        return _obj


