import notifier

from action_manager.actions.webhooks.discord_webhook import DiscordWebHookAction
from action_manager.actions.webhooks.hipchat_webhook import HipChatWebHookAction
from action_manager.actions.webhooks.mattermost_webhook import MattermostWebHookAction
from action_manager.actions.webhooks.pagerduty_webhook import PagerDutyWebHookAction
from action_manager.actions.webhooks.slack_webhook import SlackWebHookAction
from action_manager.actions.webhooks.webhook import WebHookAction

notifier.subscribe_action(DiscordWebHookAction)
notifier.subscribe_action(HipChatWebHookAction)
notifier.subscribe_action(MattermostWebHookAction)
notifier.subscribe_action(PagerDutyWebHookAction)
notifier.subscribe_action(SlackWebHookAction)
notifier.subscribe_action(WebHookAction)
