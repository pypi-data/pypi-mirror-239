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
from pydantic import BaseModel
from bgrafana_api.models.email_config import EmailConfig
from bgrafana_api.models.ops_genie_config import OpsGenieConfig
from bgrafana_api.models.pagerduty_config import PagerdutyConfig
from bgrafana_api.models.postable_grafana_receiver import PostableGrafanaReceiver
from bgrafana_api.models.pushover_config import PushoverConfig
from bgrafana_api.models.slack_config import SlackConfig
from bgrafana_api.models.victor_ops_config import VictorOpsConfig
from bgrafana_api.models.webhook_config import WebhookConfig
from bgrafana_api.models.wechat_config import WechatConfig

class ExtendedReceiver(BaseModel):
    """
    ExtendedReceiver
    """
    email_configs: Optional[EmailConfig] = None
    grafana_managed_receiver: Optional[PostableGrafanaReceiver] = None
    opsgenie_configs: Optional[OpsGenieConfig] = None
    pagerduty_configs: Optional[PagerdutyConfig] = None
    pushover_configs: Optional[PushoverConfig] = None
    slack_configs: Optional[SlackConfig] = None
    victorops_configs: Optional[VictorOpsConfig] = None
    webhook_configs: Optional[WebhookConfig] = None
    wechat_configs: Optional[WechatConfig] = None
    __properties = ["email_configs", "grafana_managed_receiver", "opsgenie_configs", "pagerduty_configs", "pushover_configs", "slack_configs", "victorops_configs", "webhook_configs", "wechat_configs"]

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
    def from_json(cls, json_str: str) -> ExtendedReceiver:
        """Create an instance of ExtendedReceiver from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of email_configs
        if self.email_configs:
            _dict['email_configs'] = self.email_configs.to_dict()
        # override the default output from pydantic by calling `to_dict()` of grafana_managed_receiver
        if self.grafana_managed_receiver:
            _dict['grafana_managed_receiver'] = self.grafana_managed_receiver.to_dict()
        # override the default output from pydantic by calling `to_dict()` of opsgenie_configs
        if self.opsgenie_configs:
            _dict['opsgenie_configs'] = self.opsgenie_configs.to_dict()
        # override the default output from pydantic by calling `to_dict()` of pagerduty_configs
        if self.pagerduty_configs:
            _dict['pagerduty_configs'] = self.pagerduty_configs.to_dict()
        # override the default output from pydantic by calling `to_dict()` of pushover_configs
        if self.pushover_configs:
            _dict['pushover_configs'] = self.pushover_configs.to_dict()
        # override the default output from pydantic by calling `to_dict()` of slack_configs
        if self.slack_configs:
            _dict['slack_configs'] = self.slack_configs.to_dict()
        # override the default output from pydantic by calling `to_dict()` of victorops_configs
        if self.victorops_configs:
            _dict['victorops_configs'] = self.victorops_configs.to_dict()
        # override the default output from pydantic by calling `to_dict()` of webhook_configs
        if self.webhook_configs:
            _dict['webhook_configs'] = self.webhook_configs.to_dict()
        # override the default output from pydantic by calling `to_dict()` of wechat_configs
        if self.wechat_configs:
            _dict['wechat_configs'] = self.wechat_configs.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ExtendedReceiver:
        """Create an instance of ExtendedReceiver from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return ExtendedReceiver.parse_obj(obj)

        _obj = ExtendedReceiver.parse_obj({
            "email_configs": EmailConfig.from_dict(obj.get("email_configs")) if obj.get("email_configs") is not None else None,
            "grafana_managed_receiver": PostableGrafanaReceiver.from_dict(obj.get("grafana_managed_receiver")) if obj.get("grafana_managed_receiver") is not None else None,
            "opsgenie_configs": OpsGenieConfig.from_dict(obj.get("opsgenie_configs")) if obj.get("opsgenie_configs") is not None else None,
            "pagerduty_configs": PagerdutyConfig.from_dict(obj.get("pagerduty_configs")) if obj.get("pagerduty_configs") is not None else None,
            "pushover_configs": PushoverConfig.from_dict(obj.get("pushover_configs")) if obj.get("pushover_configs") is not None else None,
            "slack_configs": SlackConfig.from_dict(obj.get("slack_configs")) if obj.get("slack_configs") is not None else None,
            "victorops_configs": VictorOpsConfig.from_dict(obj.get("victorops_configs")) if obj.get("victorops_configs") is not None else None,
            "webhook_configs": WebhookConfig.from_dict(obj.get("webhook_configs")) if obj.get("webhook_configs") is not None else None,
            "wechat_configs": WechatConfig.from_dict(obj.get("wechat_configs")) if obj.get("wechat_configs") is not None else None
        })
        return _obj


