import logging

from datetime import datetime
from discord_webhook import DiscordEmbed, DiscordWebhook


class Discord:
    def __init__(
        self, webhook_url, role_ids, user_ids, platform, thumb_url, embed_color, time_zone=None
    ):
        self.logger = logging.getLogger(__name__)
        self.platform = platform
        self.webhook_url = webhook_url
        self.role_ids = role_ids
        self.user_ids = user_ids
        self.thumb_url = thumb_url
        self.embed_color = embed_color
        self.time_zone = time_zone

    def create_embed_message(self, updated_keys, timestamp, result):

        _mention = ""
        for _role_id in self.role_ids:
            _mention += "@&{} ".format(_role_id)
        for _user_id in self.user_ids:
            _mention += "@{} ".format(_user_id)

        _description = "{}\n".format(_mention)

        _embed = DiscordEmbed(
            title="🚨 Apex 레전드 업데이트",
            description=_description,
            color=self.embed_color,
        )

        _update_details = ""
        for key in updated_keys:
            if key not in result:
                continue
            _update_details += "`{}` 업데이트 시간: `{}`".format(
                result[key].build_id,
                self.unix_time_to_datetime(result[key].data).strftime("%Y/%m/%d %H:%M:%S"),
            )

        _embed.set_thumbnail(url=self.thumb_url)
        _embed.add_embed_field(name="🛠️ 업데이트 정보", value=_update_details, inline=False)
        _embed.add_embed_field(
            name="🕑 확인한 시간", value=timestamp.strftime("%Y/%m/%d %H:%M:%S")
        )
        _embed.set_footer(text="Notified by Apex Legends Update Notifier")
        _embed.set_timestamp()

        return _embed
    

    def unix_time_to_datetime(self, unix_time):
        return datetime.fromtimestamp(int(unix_time), tz=self.time_zone)

    
    def fire(self, updated_keys, timestamp, result):
        self.logger.info("Prepare webhook")
        _webhook = DiscordWebhook(url=self.webhook_url)

        self.logger.info("Construct embed message")
        _embed = self.create_embed_message(updated_keys, timestamp, result)

        self.logger.info("Post embed message")
        _webhook.add_embed(_embed)
        _webhook.execute()


    """
    def fire(self, updated_apps, timestamp):
        self.logger.info("Prepare webhook")
        _webhook = DiscordWebhook(url=self.webhook_url)

        self.logger.info("Construct embed message")
        _embed = self.create_embed_message(updated_apps, timestamp)

        self.logger.info("Post embed message")
        _webhook.add_embed(_embed)
        _webhook.execute()
    """
