import praw
import pandas as pd
import requests
import json
import datetime
from datetime import timedelta

start_date = '2019-10-31 00:00:00'
stop_date = '2018-10-31 00:00:00'
start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
stop_date = datetime.datetime.strptime(stop_date, "%Y-%m-%d %H:%M:%S")

subreddit_list = ['finance', 'economy', 'SecurityAnalysis', 'Economics', 'business']

json_list = []


def api_req(url):
    response = requests.get(url)
    response_text = response.text
    response_text = json.loads(response_text)
    items = response_text['data']
    json_list.append(items)


while stop_date < start_date:
    stop_date = stop_date + timedelta(days=1)
    print(stop_date)
    print(start_date)

    api_start_time = stop_date
    api_stop_time = stop_date + timedelta(days=1)
    print('WE ARE BETWEEN: ', api_stop_time, ' AND ', api_start_time)
    start_date_api = int(datetime.datetime.strptime(str(api_start_time), '%Y-%m-%d %H:%M:%S').strftime("%s"))
    stop_date_api = int(datetime.datetime.strptime(str(api_stop_time), '%Y-%m-%d %H:%M:%S').strftime("%s"))

    for sub in subreddit_list:
        param_url = {'subreddit': sub,
                     'start_time': start_date_api,
                     'stop_time': stop_date_api}

        url = 'https://api.pushshift.io/reddit/search/submission/?subreddit={0}&sort=desc' \
              '&sort_type=created_utc&after={1}&before={2}&size=1000'\
              .format(param_url['subreddit'], param_url['start_time'], param_url['stop_time'])
        api_req(url)



df_dict = []

for each in json_list:
    for item in each:
        print(item['url'], item['author'])
        df_dict.append(item)

dd = pd.DataFrame(df_dict)
dd.to_pickle('/home/user/reddit_year.pickle')
