import re, discord
from src.utils import Utils

from html2text import HTML2Text

from src.constants import Constants

class CommandMessageBuilder:
    def __init__(self, bot_id, content, author, channel, server) -> None:
        self.bot_id = bot_id
        self.author = author
        self.content = content
        self.channel = channel
        self.server_id = server
        self.url_submited = ""
        self.channel_submited = ""
        self.feed_name_submited = ""

    def set_data_submited(self, **options):
        self.url_submited = options.pop('url', '')
        self.channel_submited = options.pop('channel', '')
        self.feed_name_submited = options.pop('feed_name', '')

    def build_delete_waiting_message(self):
        description = \
            f"<@{self.author.id}> you asked for deleting `{self.feed_name_submited}`\n" +\
            f"I'm trying to delete the feed, please wait"
        return discord.Embed(
            title=Constants.bot_name,
                url=Constants.source_code_url,
                description=description,
                color=discord.Color.orange()
            )

    def build_delete_success_message(self):
        description = f"The feed as been correctly deleted\n"
        return discord.Embed(
            title=Constants.bot_name,
                url=Constants.source_code_url,
                description=description,
                color=discord.Color.green()
            )\
            .set_footer(text="Rest in Peace little feed 🪦")

    def build_delete_error_message(self, **props):
        status = 1
        name_in_error = props.pop('url_in_error', False)
        if name_in_error: status = 0
        else: status = 1
        descriptions = [
            f"<@{self.author.id}> The submitted name `{self.feed_name_submited}` is invalid \n",
            f"<@{self.author.id}> There's no feed named: `{self.feed_name_submited}` registered\n"
        ]
        return discord.Embed(
            title=Constants.bot_name,
                url=Constants.source_code_url,
                description=descriptions[status],
                color=discord.Color.red()
            )\
            .set_footer(text=f"Try again with a registered feed 🚨")

    def build_add_waiting_message(self):
        description = \
            f"<@{self.author.id}> you asked for adding `{self.url_submited}` in the channel `{self.channel_submited}`\n" +\
            f"I'm trying to add the feed, please wait"
        return discord.Embed(
            title=Constants.bot_name,
                url=Constants.source_code_url,
                description=description,
                color=discord.Color.orange()
            )

    def build_add_success_message(self, feed_name):
        description = f"The feed as been correctly added with name `{feed_name}`\n" +\
            f"Next time there will be an article in the feed, it will be posted on the channel"
        return discord.Embed(
            title=Constants.bot_name,
                url=Constants.source_code_url,
                description=description,
                color=discord.Color.green()
            )\
            .set_footer(text="Now you just need to enjoy the news posted 📰")

    def build_add_error_message(self, **props):
        status = 2
        url_in_error = props.pop('url_in_error', False)
        channel_in_error = props.pop('channel_in_error', False)
        if url_in_error: status = 0
        elif channel_in_error: status = 1
        else: status = 2
        descriptions = [
            f"<@{self.author.id}> an error occured with the url `{self.url_submited}` for the channel `{self.channel_submited}`\n",
            f"<@{self.author.id}> an error occured on the submited channel `{self.channel_submited}`\n",
            f"<@{self.author.id}> an error occured with the url `{self.url_submited}` and the channel `{self.channel_submited}`\n",
        ]
        footers = [
            "url",
            "channel id",
            "url and channel id"
        ]
        return discord.Embed(
            title=Constants.bot_name,
                url=Constants.source_code_url,
                description=descriptions[status],
                color=discord.Color.red()
            )\
            .set_footer(text=f"Try again with a valid {footers[status]} 🚨")

    def build_help_message(self, is_in_error=False):
        desc_help = \
            f"Hey <@{self.author.id}> ! You don't know me yet ?\n" +\
            f"I've been created to help you getting in touch with any websites you want !\n" +\
            f"Every time there will be a new article/video, i'll post it over discord on the channel you wanted\n" +\
            f"To help you using my services i'll tell you how i work."
        desc_error = \
            f"Hey <@{self.author.id}>, i miss understood your command\n" +\
            f"I'll explain what i'm able to do\n"
        description = desc_error if is_in_error else desc_help

        capabilites = \
            f"- `Add` a new feed to the list on a specific channel\n" +\
            f"- `Delete` a feed from the list on the current server"

        examples = \
            f"> **<@{self.bot_id}> add <url_to_follow> channel <channel_id>**\n" +\
            f"> **<@{self.bot_id}> delete <url_to_delete>**"

        return discord.Embed(
            title=Constants.bot_name,
                url=Constants.source_code_url,
                description=description,
                color=discord.Color.orange()
            )\
            .add_field(name="__Capabilites:__", value=capabilites, inline=False)\
            .add_field(name="__Examples:__", value=examples, inline=False)\
            .set_footer(text="Made with 🧡")
    
    def build_feeds_list_message(self, server_name, server_config):
        description = \
            f"Here is the list of all the feeds registered on the server `{server_name}`\n"
        feed_list = CommandBuilderUtils.get_feed_list_message(server_config)
        return discord.Embed(
            title=Constants.bot_name,
                url=Constants.source_code_url,
                description=description,
                color=discord.Color.orange()
            )\
            .add_field(name="__Feeds:__", value=feed_list, inline=False)\

class CommandBuilderUtils:
    def get_feed_list_message(server_config):
        feeds_list = ""
        for i, feed in enumerate(server_config['feeds']):
            feed_url = feed['url']
            if Utils.is_youtube_url(feed_url):
                feed_url = Utils.get_youtube_channel_url(feed['url'])
            feeds_list += f"**- Name: `{feed['name']}` with url: {feed_url}**"
            if i <  len(server_config['feeds']) - 1:
                feeds_list += "\n"
        return feeds_list


class NewsMessageBuilder:
    
    def __init__(self, single_news) -> None:
        self.single_news = single_news
    
    def build_message(self):
        auth = self._render_author()
        message = ''
        title = f'***{self.single_news.title}***'
        author = f'*{auth}*' if auth != '' else ''
        # published = single_news.published if not Message.is_youtube_feed(single_news) else ''
        link = self.single_news.link
        summary = self._parse_html() if not self._is_youtube_feed() else ''
        for field in (title, author, link, summary):
            if field != '' :
                message += field + '\n'                
        return message

    def _parse_html(self): 
        htmlfixer = HTML2Text()
        htmlfixer.ignore_links = True
        htmlfixer.ignore_images = True
        htmlfixer.ignore_emphasis = False
        htmlfixer.body_width = 1000
        htmlfixer.unicode_snob = True
        htmlfixer.ul_item_mark = "-" 
        markdownfield = htmlfixer.handle(self.single_news.summary)
        return re.sub("<[^<]+?>", "", markdownfield)

    def _render_author(self):
        if 'authors' or 'author' in self.single_news:
            if 'authors' in self.single_news:
                if self.single_news['authors'][0] == {}:
                    return "Unknow authors"
                else:
                    str_authors = 'Author: '
                    if len(self.single_news['authors']) == 1:
                        str_authors += (self.single_news['authors'][0]).name
                    else:
                        for author in self.single_news['authors']:
                            str_authors += author.name + ', '
                    return str_authors
            elif 'author' in self.single_news:
                return "Unknow author" if self.single_news['author'] == {} else self.single_news['author'].name
        return ''
    
    def _is_youtube_feed(self):
        return 'yt_videoid' in self.single_news