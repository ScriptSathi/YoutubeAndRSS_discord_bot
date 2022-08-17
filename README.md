# [Youtube and RSS discord bot](https://github.com/ScriptSathi/discord_rss)

## <a name="introduction">Introduction</a>

This bot is a multi server content tracker. It can follow youtube channels/static web pages with articles (when using the [full project](https://github.com/ScriptSathi/Deep_Search_Gatherer)) or RSS feeds and post it on the discord channels you want. To configure part of it you just need to use the available [commands](#bot-cmds)
<br/>
This is part of a full featured discord bot, the [Deep Search Gatherer bot](https://github.com/ScriptSathi/Deep_Search_Gatherer). It can be run on it's own or with the [Scrape2RSS project](https://github.com/ScriptSathi/scrape2RSS) for tracking any websites that don't have rss feed and you wish to follow.

## <a name="features">Features</a>

- Follow an RSS feed and post latests news
- Follow a Youtube channel and post latests videos

To interact with the bot, simply tag at the beggining of the message(`@Information Gatherer` for example)
- `help` Command to display all the commands available
- `add` Register a new feed to your server
- `delete` Delete a registered feed from your server
- `list` List all registered feeds

## <a name="bot-cmds">Bot Commands</a>

| Commands | Explanations 
|----|----|
| `add` | No Aliases <br/> __Parameters__: <br/>- just give the desired url after specifying the "add" command <br/> - `channel`: the channel ID where you want to post news on (you need to enable dev mode in your discord settings) <br/> - `name`: (optional) Chose a name for the registered feed|
| `delete` |  Aliases: `del` / `dl` <br/> Take the name of the feed to delete as parameter|
| `help` | Aliases: `-h` / `` (no params) <br/> Display the help menu |
| `list` | List all the registered feeds in your server |

### Examples

```bash
@Information Gatherer add https://www.youtube.com/c/LiveOverflow channel 1009496824605843607
```
```bash
@Information Gatherer add https://www.youtube.com/c/LiveOverflow channel 1009496824605843607 name my-feed
```
```bash
@Information Gatherer del my-feed
```
```bash
@Information Gatherer ls
```

## <a name="disclaimer">Disclaimer</a>

If you are unfamiliar with Docker, check out the [Introduction to Docker](https://training.docker.com/introduction-to-docker) webinar, or consult your favorite search engine.

## <a name="build">Build the image</a> 

Simply run the following command from this project source directory to build your new image
```
docker build -t rssbot .
```
## <a name="start">Start the container</a> 

The configuration file is compatible with either `json` and `yaml` (or `yml`) format.
To understand how this project must be run, we will take the example with a valid yaml configuration file
The file don't need to be called `config.yaml` but need to be placed in `/config` folder. The file must be in a valid **JSON format**
```
docker run -d -v $(pwd)/config.yaml:/config/config.yaml --name=rssbot rssbot
```
You should then see your bot online on discord 

**Note:** If you've previously run a container with the same name, this command will fail. In that instance, you can use:
```
docker rm rssbot
```

## <a name="min-config">Minimal configuration needed</a> 

```
token: <TOKEN>
```

## <a name="allow-parameters">Configuration parameters</a> 

| Parameters | Explanation | Default value |
|----|----| ----|
| `token` | Your bot token, it's **mandatory** variable. | "" |
| `refresh-time` | Time between refreshes of a feed, in second | 900 |
| `published_since_default` | Maximum age of news before it's discarded, in second. Used only when `published_since` of a feed is not set. <br/>If `published_since_default` or `published_since` are equal to `0`, only posts published after the initialization of this bot will be sent (usefull in case you use [Scrape2RSS feature](https://github.com/ScriptSathi/scrape2RSS)) | 0 |
| `gameplayed` | Change the game displayed in bot profile | "Eating some RSS feeds" |

## [Scrape2RSS feature](https://github.com/ScriptSathi/scrape2RSS)

If you want to follow a website that doesn't have an RSS feed, submit the URL of the page in the `url` parameter like a normal feed.
To be used, you need to set the [full bot project](https://github.com/ScriptSathi/Deep_Search_Gatherer)

## <a name="youtube-feature">Youtube Feature</a> 

To follow a youtube channel just put the youtube url in the `url` field.

Format tested: 
- `https://www.youtube.com/c/<Channel-Name>`
- `https://www.youtube.com/user/<Channel-Name>`