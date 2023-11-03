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
from pydantic import BaseModel, Field, conlist
from bgrafana_api.models.alert_instances_response import AlertInstancesResponse
from bgrafana_api.models.sample import Sample

class TestRuleResponse(BaseModel):
    """
    TestRuleResponse
    """
    alerts: Optional[conlist(Sample)] = Field(None, description="Vector is basically only an alias for model.Samples, but the contract is that in a Vector, all Samples have the same timestamp.")
    grafana_alert_instances: Optional[AlertInstancesResponse] = None
    __properties = ["alerts", "grafana_alert_instances"]

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
    def from_json(cls, json_str: str) -> TestRuleResponse:
        """Create an instance of TestRuleResponse from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each item in alerts (list)
        _items = []
        if self.alerts:
            for _item in self.alerts:
                if _item:
                    _items.append(_item.to_dict())
            _dict['alerts'] = _items
        # override the default output from pydantic by calling `to_dict()` of grafana_alert_instances
        if self.grafana_alert_instances:
            _dict['grafana_alert_instances'] = self.grafana_alert_instances.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> TestRuleResponse:
        """Create an instance of TestRuleResponse from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return TestRuleResponse.parse_obj(obj)

        _obj = TestRuleResponse.parse_obj({
            "alerts": [Sample.from_dict(_item) for _item in obj.get("alerts")] if obj.get("alerts") is not None else None,
            "grafana_alert_instances": AlertInstancesResponse.from_dict(obj.get("grafana_alert_instances")) if obj.get("grafana_alert_instances") is not None else None
        })
        return _obj


