import json, math
from math import remainder
from os import times
from statistics import mean
from time import time
from urllib import response
from numpy import average
import requests, test, config, heapq

app_id = config.app_id
secret = config.secret
auth = requests.auth.HTTPBasicAuth(app_id, secret)
reddit_username = config.reddit_username
reddit_password = config.reddit_password
data = {
'grant_type': 'password',
'username': reddit_username,
'password': reddit_password
}
headers = {'User-Agent': 'nickwood5/Sentiment-Analysis-0.1'}
res = requests.post('https://www.reddit.com/api/v1/access_token',
auth=auth, data=data, headers=headers)
#print(res)

token = res.json()['access_token']
#print(token)
headers['Authorization'] = 'bearer {}'.format(token)

def get_post_details(post_id, database):
    response_code = 400
    post_json_link = "https://oauth.reddit.com/comments/{}.json?context=0&depth=0".format(post_id)
    while response_code != 200:
        post_data = requests.get(post_json_link, headers=headers)
        response_code = post_data.status_code

    json_data = post_data.json()
    post_data = json_data[0]["data"]["children"][0]["data"]
    selftext = json_data[0]["data"]["children"][0]["data"]["selftext"]
    #print(selftext)

    if selftext != "[removed]" and selftext != "[deleted]" and selftext != "":
        database.append({"score": post_data["score"], "created": post_data["created"], "selftext": selftext})
    #exit()
    ##print(post_json_link)

def handle_post_list(pushshift_api_response, ids, database):
    json_response = pushshift_api_response.json()
    data = json_response["data"]
    #print(len(data))
    for post in data:
        #print(post)

        if "selftext" in post.keys():
            if post["selftext"] != "[deleted]" and post["selftext"] != "[removed]" and post["selftext"] != "":
                post_link = post["full_link"]
                post_json_link = post_link.rstrip(post_link[-1]) + ".json"

                post_id = post["id"]
                get_post_details(post_id, database)

                ids.append(post["full_link"])

def construct_api_url(subreddit, after, before):
    url = "https://api.pushshift.io/reddit/submission/search/?after={}&before={}&sort_type=created_utc&size=500&sort=asc&subreddit={}".format(after, before, subreddit)
    return url

async def send_websocket_data(websocket, type, data):
    await websocket.send(json.dumps({"type": type, "data": data}))

async def get_post_list(subreddit, after, before, websocket):
    
    #api = 'https://oauth.reddit.com'
    #res = requests.get('{}/comments/b8yd3r/.json'.format(api), headers=headers)
    ##print(res.json())
    #exit()

    start_time = time()
    #print(start_time)

    duration = 3000
    timespan = before - after
    #print("Timespan is {}".format(timespan))
    periods = (timespan // duration) - 1
    ids = []
    database = []

    if timespan >= 2:
        timestamps = []
        if periods > 1:

            diff = before - (periods * duration)

            #print(periods)
            for a in range (0, periods):
                #print(before-a*duration)
                #print(before-((a+1)*duration + 1))
                #print("")

                before_stamp = before-a*duration
                after_stamp = before-((a+1)*duration + 1)
                timestamps.append((after_stamp, before_stamp))

            remainder = before-((periods+1)*duration)
            #print(remainder)
            #print("")
            #print(diff)

            timestamps.append(((remainder, diff)))
        else:
            #print(after)
            #print(before)
            timestamps.append((after, before))

        #print(timestamps)
        estimated_times = []
        elapsed_time = 0
        all_epoch_times = []
        num_epochs = len(timestamps)
        for segment_index, segment in enumerate(timestamps):
            epoch_start_timestamp = time()

            epoch = segment_index + 1
            url = construct_api_url(subreddit, segment[0], segment[1])
            #print(url)
            response_code = 400
            while response_code != 200:
                a = requests.get(url)
                response_code = a.status_code

                if response_code != 200:
                    "Retrying.."

            #print(a.status_code)
            handle_post_list(a, ids, database)

            epoch_end_timestamp = time()
            total_epoch_time = epoch_end_timestamp - epoch_start_timestamp
            elapsed_time += total_epoch_time
            print("This took {}".format(total_epoch_time))
            all_epoch_times.append(total_epoch_time)
            estimated = max(all_epoch_times) * num_epochs
            print("Estimated time is {}".format(estimated))

            percentage = round((epoch / num_epochs) * 100, 2)
            print(percentage)

            half = int(round(len(all_epoch_times) / 2, 0))
            print(round(len(all_epoch_times) / 2, 0))
            print(heapq.nlargest(half, all_epoch_times))
            if half > 0:
                top_half = heapq.nlargest(half, all_epoch_times)
            else:
                top_half = all_epoch_times
            print(mean(top_half) * num_epochs)

            remaining_epochs = num_epochs - epoch
            print("{} remaining".format(remaining_epochs))
            print(remaining_epochs * mean(all_epoch_times))
            estimated_time_remaining = remaining_epochs * mean(all_epoch_times)
            estimated_times.append(estimated_time_remaining + elapsed_time)

            data = {"estimated_time_remaining": estimated_time_remaining, "percentage": percentage}
            await send_websocket_data(websocket, "progress", data)

    print(estimated_times)


    #print(ids)
    #print(database)
    #print(len(database))

    end_time = time()
    #print(start_time)
    #print(end_time)

    stats = []

    total_absolute_score = 0

    for post in database:
        negative, neutral, positive, compound, overall_sentiment = test.sentiment_vader(post["selftext"])
        #print("Post is {}, score is {}".format(post["selftext"], compound))
        total_absolute_score += abs(post["score"])
        stats.append(compound)

    percentages = []
    weighted_averages = []
    for stat_index, stat in enumerate(stats):
        weighted_average = stat * (abs(database[stat_index]["score"]) / total_absolute_score)
        weighted_averages.append(weighted_average)
        percentages.append(abs(database[stat_index]["score"]) / total_absolute_score)
    





    #print(mean(stats))
    #print(mean(weighted_averages))
    #print(sum(weighted_averages))
    #print(weighted_averages)
    #print(sum(percentages))
    #print(percentages)
    print(sum(weighted_averages))
    print("{} to {} took {}, analyzed {} posts".format(after, before, end_time - start_time, len(weighted_averages)))

    sentiment = sum(weighted_averages)
    await send_websocket_data(websocket, "sentiment_result", sentiment)

    await websocket.close()

    return weighted_average


#get_post_list("bitcoin", 1662521042, 1662607442)

"""
start = 1662521042
end = 1662607442

for day in range (0, 30):
    get_post_list("bitcoin", start - (day * 86400), end - (day * 86400))

"""