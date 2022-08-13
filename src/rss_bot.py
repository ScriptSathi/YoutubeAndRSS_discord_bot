import discord, functools, os, json, asyncio
from threading import Thread
from time import sleep

from src.feed import Feed
from src.logger import Logger
from src.constants import Constants

logger = Logger.get_logger()

class RSSBot:

    def __init__(self, client, config, generator_exist) -> None:
        self.client = client
        self.config = config
        self.generator_exist = generator_exist
    async def run(self):
        await self._display_bot_game()
        while True:
            await self._start_feeds()

    async def _start_feeds(self):
        try:
            for feed_config in self.config['feeds']:
                if bool(feed_config['is_valid_url']):
                    latest_post_in_feed = self._read_latest_post_file(feed_config['name'])
                    channels = await self._get_current_channel(feed_config)
                    rss_manager = Feed(feed_config, channels, latest_post_in_feed, self.generator_exist)
                    thread = Thread(target=rss_manager.run, args=(self.client,))
                    thread.start()
                else:
                    logger.error(f"{feed_config['url']} is not a valid url, skipping")
            await self._sleep_before_refresh()
        except Exception as e:
            logger.exception(str(e))
            logger.error(f'A network issue has occured')
            await self._sleep_before_refresh()
            await self._start_feeds()

    async def _get_current_channel(self, feed_config):
        config_channels = str(feed_config['channels']).split(',')
        client_channels = []

        for chan in config_channels:
            channel_obj = await self.client.fetch_channel(chan)
            client_channels.append(channel_obj)
        return client_channels

    async def _display_bot_game(self):
        game_displayed = self.config['game_displayed']
        await self.client.change_presence(activity=discord.Game(name=game_displayed))

    def _read_latest_post_file(self, feed_name):
        data_dir_path = Constants.feeds_data_dir
        file_path = data_dir_path + '/' + feed_name
        file_data = ''

        if os.path.isfile(file_path):
            with open(file_path, 'r') as file_buff:
                file_data = file_buff.read()
        else:
            if not os.path.isdir(data_dir_path):
                os.mkdir(data_dir_path)
            with open(file_path, 'w') as file_buff:
                file_buff.write(file_data)
        return file_data

    async def _sleep_before_refresh(self) -> None:
        refresh_time = self.config['refresh_time']
        logger.info(f'Sleep for {refresh_time}s before the next refresh')
        await asyncio.sleep(refresh_time)
