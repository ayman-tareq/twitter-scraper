
import snscrape.modules.twitter as sntwitter
import pandas as pd
import os

# Creating list to append tweet data to
tweets_list2 = []
# keyword_format = '#economy lang:en until:2022-08-31 since:2017-08-01'
keyword_format = '#economy #RussiaUkraineWar'
# keyword_format = '#bitcoin lang:en until:2022-03-31 since:2021-06-01 near:UK'
limit = 100

keyword_format='#economy since:2022-02-24'

# Using TwitterSearchScraper to scrape data and append tweets to list

n = 0

for i,tweet in enumerate(sntwitter.TwitterSearchScraper(query=keyword_format).get_items()):
    if n>limit:
        break
    # print(tweet)
    # try:
    #     if tweet.place.country != 'United Kingdom':
    #         continue
    # except:
    #     continue
    l = [tweet.date, tweet.id, tweet.content, tweet.user.username, tweet.url]
    # try:
    #   tweet.place.country
    # except:
    #   print('\n\tcountry not found!')
    #   continue
    # l = [tweet.date, tweet.id, tweet.content, tweet.user.username, tweet.place.country, tweet.url]
    tweets_list2.append(l)
    print(n, '||', i, l)
    n += 1
    
# Creating a dataframe from the tweets list above
# tweets_df2 = pd.DataFrame(tweets_list2, columns=['Datetime', 'Tweet Id', 'Text', 'Username', 'Ref'])
tweets_df2 = pd.DataFrame(tweets_list2)
# tweets_df2 = pd.DataFrame(tweets_list2, columns=['Datetime', 'Tweet Id', 'Text', 'Username', 'Country', 'Ref'])

output_file_name = 'economy.csv'
if os.path.exists(output_file_name):
    mode = 'a'
    header = False
else:
    mode = 'w'
    header = True

tweets_df2.to_csv(output_file_name, index=False, mode='a', header=header, encoding='utf-8')
# tweets_df2.to_excel('sample tweet.xlsx', index=False)
# df = pd.read_csv(output_file_name)
tweets_df2.duplicated(4).sum()
tweets_df2.drop_duplicates(4, inplace=True)
tweets_df2.to_csv(output_file_name, index=False)

print('\n\tDone!')


# from datetime import date

# today = date.today()
# end_date = today

# search_term = '#Pedro'
# from_date = '2022-05-19'


# os.system(f"snscrape twitter-search #economy > result-tweets.csv")
# if os.stat("result-tweets.csv").st_size == 0:
#   counter = 0
# else:
#   df = pd.read_csv('result-tweets.csv', names=['link'])
#   counter = df.size

# print('Number Of Tweets : '+ str(counter))