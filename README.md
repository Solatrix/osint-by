# OSINT-BY

### The ideas

This repo was born when I started investigating social media on two occasions
- During the 2020 Belarus protests in Minsk following president A. Lukashenka's reelection
- During March 2022 at the beginning of the Russian invasion of Ukraine
This repo is essentially a collection of the datasets I extracted and the tools I created in order to scrap, analyze or visualize said datasets

### What you'll find

The repo is organized as follows

```Bash
├── #Azovstal 
│   ├── azvostal.gephi
│   ├── cache
│   │   ├── followers.json
│   │   ├── friendships.json
│   │   └── tweets.json
│   ├── edges.csv
│   └── nodes.csv
├── CSV
│   ├── batka_tweets.csv
│   ├── SvoihNeBrosajem.csv
│   ├── UkraineNews.csv
│   ├── WarInUkraine-07052022.csv
│   ├── warOnFakes-2.csv
│   ├── warOnFakes.csv
│   ├── ZA-07052022.csv
│   ├── батька-2.csv
│   └── ябатька.txt
├── notebooks
│   ├── jabatka-notebook.ipynb
│   ├── notebook.ipynb
│   └── warInUkraine.ipynb
├── python-scripts
│   ├── tgstat-chartdata-crawler.py
│   └── twitter-location-scrapper.py
├── README.md <---- you are here :)
└── www
    ├── app.js
    ├── json-parsing.html
    ├── style.css
    └── tgstat-views-pul-pervogo-sept-2021.json
```

#### Graphs and data visualization

The `#Azovstal` folder contains translated `nodes.csv` and `edges.csv` from Tweets I extracted in May, 2022 containing the `Azovstal` hashtag. The dataset provided does not include the whole content of the tweets, but rather a collection of users that mentioned this hashtag during the chosen time interval.

The `www` folder contains a webpage rendering a D3 chart to visualise the number of subscribers to the `ПульПервого` channel that belongs to A. Lukashenko. Dataset is extracted from Tgstat.ru as `tgstat-views-pul-pervogo-sept-2021.json`

#### CSV Datasets

The `CSV` folder contains datasets extracted mainly from Twitter.
- `batka_tweets.csv`, `батька-2.csv` and `ябатька.txt` is a collection of tweets that used the hashtag `#ябатька` in support or criticism  against Belarus president A. Lukashenko
- `SvoihNeBrosajem.csv` contains tweets mentioning the hashtag `#свохнебросаем`, literally "We don't abandon our own" referring the Russian propaganda motto to legitimate the invasion of Ukraine.
- `WarInUkraine-07052022.csv` contains tweets mentioning the hashtag `#WarInUkraine` for said period
- The `warOnFakes.csv` and `warOnFakes-2.csv`contain tweets that harbor hyperlinks to the propaganda platform selling itself as a debunking portal WarOnFakes
- `ZA-07052022.csv` contains tweets mentioning the hashtag `#za` or `#за` meaning "for" which is widely used by Russian propaganda to legitmate the war

#### Notebooks and scripts

The `notebooks` folder contains Jupyter notebooks that are remnants of the notebooks I used to collect tweets using Twitter API and  `tweepy`

The `python-scripts` contains the `tgstat-chartdata-crawler.py` file which in essence reverse-engineered the Tgstat.ru API to collect statistical data about any given channel.


#### How-to

Using the `tgstat-chartdata-crawler.py` you will need Python 3.8+ and a CLI interface.
I usually run the script as follows : 

```bash
python3 -m tgstat-crawler.py --channels=@telegram_channel_name --period=(months|weeks|days|years) --metric=(views|posts|views_per_posts|members|reposts) --start-date=YYYY-MM-DD --end-date=YYYY-MM-DD > output.json
```

In a nutshell :

`--channels=@telegram_channel_name` : name of the channels whose data you wish to find

`--period=(months|weeks|days|years)` : Statsitics step, you can have data monthly, weekly, daily and sometimes yearly.
 
`--metric=(views|posts|views_per_posts|members|reposts)` : indicator you'd like to crawl
 
`--start-date=YYYY-MM-DD, --end-date=YYYY-MM-DD` : time frame in which you want to collect data

### Issues

Implementing output formats would be very useful.
The `tgstat-chartdata-crawler.py` makes use of Tgstat REST API, and does not format data for you. Further data processing is needed (lookup  `www/app.js`) to properly make use of the crawled data

