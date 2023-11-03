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
from pydantic import BaseModel, Field, StrictStr, conlist
from bgrafana_api.models.discord_config import DiscordConfig
from bgrafana_api.models.email_config import EmailConfig
from bgrafana_api.models.ops_genie_config import OpsGenieConfig
from bgrafana_api.models.pagerduty_config import PagerdutyConfig
from bgrafana_api.models.postable_grafana_receiver import PostableGrafanaReceiver
from bgrafana_api.models.pushover_config import PushoverConfig
from bgrafana_api.models.slack_config import SlackConfig
from bgrafana_api.models.sns_config import SNSConfig
from bgrafana_api.models.telegram_config import TelegramConfig
from bgrafana_api.models.victor_ops_config import VictorOpsConfig
from bgrafana_api.models.webex_config import WebexConfig
from bgrafana_api.models.webhook_config import WebhookConfig
from bgrafana_api.models.wechat_config import WechatConfig

class PostableApiReceiver(BaseModel):
    """
    PostableApiReceiver
    """
    discord_configs: Optional[conlist(DiscordConfig)] = None
    email_configs: Optional[conlist(EmailConfig)] = None
    grafana_managed_receiver_configs: Optional[conlist(PostableGrafanaReceiver)] = None
    name: Optional[StrictStr] = Field(None, description="A unique identifier for this receiver.")
    opsgenie_configs: Optional[conlist(OpsGenieConfig)] = None
    pagerduty_configs: Optional[conlist(PagerdutyConfig)] = None
    pushover_configs: Optional[conlist(PushoverConfig)] = None
    slack_configs: Optional[conlist(SlackConfig)] = None
    sns_configs: Optional[conlist(SNSConfig)] = None
    telegram_configs: Optional[conlist(TelegramConfig)] = None
    victorops_configs: Optional[conlist(VictorOpsConfig)] = None
    webex_configs: Optional[conlist(WebexConfig)] = None
    webhook_configs: Optional[conlist(WebhookConfig)] = None
    wechat_configs: Optional[conlist(WechatConfig)] = None
    __properties = ["discord_configs", "email_configs", "grafana_managed_receiver_configs", "name", "opsgenie_configs", "pagerduty_configs", "pushover_configs", "slack_configs", "sns_configs", "telegram_configs", "victorops_configs", "webex_configs", "webhook_configs", "wechat_configs"]

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
    def from_json(cls, json_str: str) -> PostableApiReceiver:
        """Create an instance of PostableApiReceiver from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each item in discord_configs (list)
        _items = []
        if self.discord_configs:
            for _item in self.discord_configs:
                if _item:
                    _items.append(_item.to_dict())
            _dict['discord_configs'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in email_configs (list)
        _items = []
        if self.email_configs:
            for _item in self.email_configs:
                if _item:
                    _items.append(_item.to_dict())
            _dict['email_configs'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in grafana_managed_receiver_configs (list)
        _items = []
        if self.grafana_managed_receiver_configs:
            for _item in self.grafana_managed_receiver_configs:
                if _item:
                    _items.append(_item.to_dict())
            _dict['grafana_managed_receiver_configs'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in opsgenie_configs (list)
        _items = []
        if self.opsgenie_configs:
            for _item in self.opsgenie_configs:
                if _item:
                    _items.append(_item.to_dict())
            _dict['opsgenie_configs'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in pagerduty_configs (list)
        _items = []
        if self.pagerduty_configs:
            for _item in self.pagerduty_configs:
                if _item:
                    _items.append(_item.to_dict())
            _dict['pagerduty_configs'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in pushover_configs (list)
        _items = []
        if self.pushover_configs:
            for _item in self.pushover_configs:
                if _item:
                    _items.append(_item.to_dict())
            _dict['pushover_configs'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in slack_configs (list)
        _items = []
        if self.slack_configs:
            for _item in self.slack_configs:
                if _item:
                    _items.append(_item.to_dict())
            _dict['slack_configs'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in sns_configs (list)
        _items = []
        if self.sns_configs:
            for _item in self.sns_configs:
                if _item:
                    _items.append(_item.to_dict())
            _dict['sns_configs'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in telegram_configs (list)
        _items = []
        if self.telegram_configs:
            for _item in self.telegram_configs:
                if _item:
                    _items.append(_item.to_dict())
            _dict['telegram_configs'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in victorops_configs (list)
        _items = []
        if self.victorops_configs:
            for _item in self.victorops_configs:
                if _item:
                    _items.append(_item.to_dict())
            _dict['victorops_configs'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in webex_configs (list)
        _items = []
        if self.webex_configs:
            for _item in self.webex_configs:
                if _item:
                    _items.append(_item.to_dict())
            _dict['webex_configs'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in webhook_configs (list)
        _items = []
        if self.webhook_configs:
            for _item in self.webhook_configs:
                if _item:
                    _items.append(_item.to_dict())
            _dict['webhook_configs'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in wechat_configs (list)
        _items = []
        if self.wechat_configs:
            for _item in self.wechat_configs:
                if _item:
                    _items.append(_item.to_dict())
            _dict['wechat_configs'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> PostableApiReceiver:
        """Create an instance of PostableApiReceiver from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return PostableApiReceiver.parse_obj(obj)

        _obj = PostableApiReceiver.parse_obj({
            "discord_configs": [DiscordConfig.from_dict(_item) for _item in obj.get("discord_configs")] if obj.get("discord_configs") is not None else None,
            "email_configs": [EmailConfig.from_dict(_item) for _item in obj.get("email_configs")] if obj.get("email_configs") is not None else None,
            "grafana_managed_receiver_configs": [PostableGrafanaReceiver.from_dict(_item) for _item in obj.get("grafana_managed_receiver_configs")] if obj.get("grafana_managed_receiver_configs") is not None else None,
            "name": obj.get("name"),
            "opsgenie_configs": [OpsGenieConfig.from_dict(_item) for _item in obj.get("opsgenie_configs")] if obj.get("opsgenie_configs") is not None else None,
            "pagerduty_configs": [PagerdutyConfig.from_dict(_item) for _item in obj.get("pagerduty_configs")] if obj.get("pagerduty_configs") is not None else None,
            "pushover_configs": [PushoverConfig.from_dict(_item) for _item in obj.get("pushover_configs")] if obj.get("pushover_configs") is not None else None,
            "slack_configs": [SlackConfig.from_dict(_item) for _item in obj.get("slack_configs")] if obj.get("slack_configs") is not None else None,
            "sns_configs": [SNSConfig.from_dict(_item) for _item in obj.get("sns_configs")] if obj.get("sns_configs") is not None else None,
            "telegram_configs": [TelegramConfig.from_dict(_item) for _item in obj.get("telegram_configs")] if obj.get("telegram_configs") is not None else None,
            "victorops_configs": [VictorOpsConfig.from_dict(_item) for _item in obj.get("victorops_configs")] if obj.get("victorops_configs") is not None else None,
            "webex_configs": [WebexConfig.from_dict(_item) for _item in obj.get("webex_configs")] if obj.get("webex_configs") is not None else None,
            "webhook_configs": [WebhookConfig.from_dict(_item) for _item in obj.get("webhook_configs")] if obj.get("webhook_configs") is not None else None,
            "wechat_configs": [WechatConfig.from_dict(_item) for _item in obj.get("wechat_configs")] if obj.get("wechat_configs") is not None else None
        })
        return _obj


