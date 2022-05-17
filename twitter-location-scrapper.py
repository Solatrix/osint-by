import pandas as pandas
import snscrape.modules.twitter as sntwitter
import itertools

tag = 'ябатька'

tweet_list = sntwitter.TwitterSearchScrapper(tag).get_items()
sliced_tweets = itertools.islice(tweet_list, 100)

df = pd.DataFrame(sliced_tweets)['date', 'content', 'user_location']

df.head()