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
from pydantic import BaseModel, Field, StrictBool, StrictStr, validator

class EmbeddedContactPoint(BaseModel):
    """
    EmbeddedContactPoint is the contact point type that is used by grafanas embedded alertmanager implementation.  # noqa: E501
    """
    disable_resolve_message: Optional[StrictBool] = Field(None, alias="disableResolveMessage")
    name: Optional[StrictStr] = Field(None, description="Name is used as grouping key in the UI. Contact points with the same name will be grouped in the UI.")
    provenance: Optional[StrictStr] = None
    settings: Dict[str, Any] = Field(...)
    type: StrictStr = Field(...)
    uid: Optional[StrictStr] = Field(None, description="UID is the unique identifier of the contact point. The UID can be set by the user.")
    __properties = ["disableResolveMessage", "name", "provenance", "settings", "type", "uid"]

    @validator('type')
    def type_validate_enum(cls, value):
        """Validates the enum"""
        if value not in ('alertmanager', ' dingding', ' discord', ' email', ' googlechat', ' kafka', ' line', ' opsgenie', ' pagerduty', ' pushover', ' sensugo', ' slack', ' teams', ' telegram', ' threema', ' victorops', ' webhook', ' wecom'):
            raise ValueError("must be one of enum values ('alertmanager', ' dingding', ' discord', ' email', ' googlechat', ' kafka', ' line', ' opsgenie', ' pagerduty', ' pushover', ' sensugo', ' slack', ' teams', ' telegram', ' threema', ' victorops', ' webhook', ' wecom')")
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
    def from_json(cls, json_str: str) -> EmbeddedContactPoint:
        """Create an instance of EmbeddedContactPoint from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                            "provenance",
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> EmbeddedContactPoint:
        """Create an instance of EmbeddedContactPoint from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return EmbeddedContactPoint.parse_obj(obj)

        _obj = EmbeddedContactPoint.parse_obj({
            "disable_resolve_message": obj.get("disableResolveMessage"),
            "name": obj.get("name"),
            "provenance": obj.get("provenance"),
            "settings": obj.get("settings"),
            "type": obj.get("type"),
            "uid": obj.get("uid")
        })
        return _obj


