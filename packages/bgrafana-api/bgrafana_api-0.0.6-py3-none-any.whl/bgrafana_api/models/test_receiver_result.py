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


from typing import List, Optional
from pydantic import BaseModel, StrictStr, conlist
from bgrafana_api.models.test_receiver_config_result import TestReceiverConfigResult

class TestReceiverResult(BaseModel):
    """
    TestReceiverResult
    """
    grafana_managed_receiver_configs: Optional[conlist(TestReceiverConfigResult)] = None
    name: Optional[StrictStr] = None
    __properties = ["grafana_managed_receiver_configs", "name"]

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
    def from_json(cls, json_str: str) -> TestReceiverResult:
        """Create an instance of TestReceiverResult from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each item in grafana_managed_receiver_configs (list)
        _items = []
        if self.grafana_managed_receiver_configs:
            for _item in self.grafana_managed_receiver_configs:
                if _item:
                    _items.append(_item.to_dict())
            _dict['grafana_managed_receiver_configs'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> TestReceiverResult:
        """Create an instance of TestReceiverResult from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return TestReceiverResult.parse_obj(obj)

        _obj = TestReceiverResult.parse_obj({
            "grafana_managed_receiver_configs": [TestReceiverConfigResult.from_dict(_item) for _item in obj.get("grafana_managed_receiver_configs")] if obj.get("grafana_managed_receiver_configs") is not None else None,
            "name": obj.get("name")
        })
        return _obj


