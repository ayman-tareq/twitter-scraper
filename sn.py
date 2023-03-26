
import snscrape.modules.twitter as sntwitter
import pandas as pd
import os, json, csv


output_file_name = 'all_tweets.csv'
header = ['tweet_url', 'date', 'tweet_id', 'user_name', 'is_user_verified', 'user_followers', 'user_following', 'user_tot_status', 'user_location', 'user_description', 'user_label', 'user_url', 'reply_count', 'retweet_count', 'like_count', 'quote_count', 'conversation_id', 'lang', 'source_label', 'coordinates', 'place', 'hashtags', 'cashtags', 'view_count', 'tweet_content']

def open_or_create_csv():
    global csv_f, writer
    output_file_path = os.path.join(os.getcwd(), output_file_name)
    output_file_exists = os.path.exists(output_file_path)
    if output_file_exists:
        mde = 'a'
    else:
        mde = 'w'

    csv_f = open(output_file_path, mde, encoding='utf-8', newline='')
    writer = csv.writer(csv_f)
    if mde == 'w':
        writer.writerow(header)

open_or_create_csv()


# keyword_format = '#RussiaUkraineWar (#economy OR #worldeconomy) until:2022-02-23 since:2022-01-01'
keyword_format = '(#economy OR #worldeconomy) until:2017-12-31 since:2017-01-01'

limit = 100000
n = 0


for i,tweet in enumerate(sntwitter.TwitterSearchScraper(query=keyword_format).get_items()):

    if n>limit:
        break
    n+=1
    
    json_obj = tweet.json()
    json_obj = json.loads(json_obj, cls=json.JSONDecoder)
    # print('\n\tJson object created...')
    
    # ----------------- Tweet Data -----------------
    tweet_url = json_obj.get('url')
    date = json_obj.get('date')
    tweet_id = json_obj.get('id')
    user_name = json_obj.get('user').get('username')
    is_user_verified = json_obj.get('user').get('verified')

    user_followers = json_obj.get('user').get('followersCount')
    user_following = json_obj.get('user').get('friendsCount')
    user_tot_status = json_obj.get('user').get('statusesCount')
    user_location = json_obj.get('user').get('location')
    user_description = json_obj.get('user').get('renderedDescription')

    user_label = json_obj.get('user').get('label')
    user_url = json_obj.get('user').get('url')
    reply_count = json_obj.get('replyCount')
    retweet_count = json_obj.get('retweetCount')
    like_count = json_obj.get('likeCount')

    quote_count = json_obj.get('quoteCount')
    conversation_id = json_obj.get('conversationId')
    lang = json_obj.get('lang')
    source_label = json_obj.get('sourceLabel')
    coordinates = json_obj.get('coordinates')

    place = json_obj.get('place')
    hashtags = json_obj.get('hashtags')
    cashtags = json_obj.get('cashtags')
    view_count = json_obj.get('viewCount')
    tweet_content = json_obj.get('content')
    
    l = [
        tweet_url, date, tweet_id, user_name, is_user_verified, 
        user_followers, user_following, user_tot_status, user_location, user_description, 
        user_label, user_url, reply_count, retweet_count, like_count, 
        quote_count, conversation_id, lang, source_label, coordinates, 
        place, hashtags, cashtags, view_count, tweet_content]
    
    writer.writerow(l)
    csv_f.close()
    open_or_create_csv()
    print(f'\t{i+1} - {date} - {tweet_url} - {user_location} - {place} - {lang}')
    

csv_f.close()

df = pd.read_csv(output_file_name, encoding='utf-8')
df.duplicated(['tweet_id']).sum()
df.drop_duplicates(subset=['tweet_id'], inplace=True)
df.to_csv(output_file_name, index=False, encoding='utf-8')
print('\n\tDone! total tweets:', len(df))