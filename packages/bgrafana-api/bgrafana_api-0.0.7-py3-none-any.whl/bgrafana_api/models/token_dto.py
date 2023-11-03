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

from datetime import datetime
from typing import Optional, Union
from pydantic import BaseModel, Field, StrictBool, StrictFloat, StrictInt, StrictStr

class TokenDTO(BaseModel):
    """
    TokenDTO
    """
    created: Optional[datetime] = None
    expiration: Optional[datetime] = None
    has_expired: Optional[StrictBool] = Field(None, alias="hasExpired")
    id: Optional[StrictInt] = None
    is_revoked: Optional[StrictBool] = Field(None, alias="isRevoked")
    last_used_at: Optional[datetime] = Field(None, alias="lastUsedAt")
    name: Optional[StrictStr] = None
    seconds_until_expiration: Optional[Union[StrictFloat, StrictInt]] = Field(None, alias="secondsUntilExpiration")
    __properties = ["created", "expiration", "hasExpired", "id", "isRevoked", "lastUsedAt", "name", "secondsUntilExpiration"]

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
    def from_json(cls, json_str: str) -> TokenDTO:
        """Create an instance of TokenDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> TokenDTO:
        """Create an instance of TokenDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return TokenDTO.parse_obj(obj)

        _obj = TokenDTO.parse_obj({
            "created": obj.get("created"),
            "expiration": obj.get("expiration"),
            "has_expired": obj.get("hasExpired"),
            "id": obj.get("id"),
            "is_revoked": obj.get("isRevoked"),
            "last_used_at": obj.get("lastUsedAt"),
            "name": obj.get("name"),
            "seconds_until_expiration": obj.get("secondsUntilExpiration")
        })
        return _obj


