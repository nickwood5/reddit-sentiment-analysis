from asyncio.proactor_events import constants
from numpy import average
import requests
import pandas as pd
import test
app_id = 'MJz9lfdLsGWw39ez9S53iA'
secret = '6IgaElNrxtMaOYWRE7dzb_lDb8HXNg'
auth = requests.auth.HTTPBasicAuth(app_id, secret)
reddit_username = 'nickwood5'
reddit_password = 'jevdax-neQhyv-0cuxba'
data = {
'grant_type': 'password',
'username': reddit_username,
'password': reddit_password
}
headers = {'User-Agent': 'Tutorial2/0.0.1'}
res = requests.post('https://www.reddit.com/api/v1/access_token',
auth=auth, data=data, headers=headers)
print(res)

token = res.json()['access_token']
print(token)
headers['Authorization'] = 'bearer {}'.format(token)
requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)

api = 'https://oauth.reddit.com'
res = requests.get('{}/r/cryptocurrency/new'.format(api), headers=headers, params={'limit': '100'})
res.json()
print(res.json())

df = pd.DataFrame({'name': [], 'title': [], 'selftext': [], 'score': []})
for post in res.json()['data']['children']:
    print(post["data"])
    exit()
    df = df.append({
    'name': post['data']['name'],
    'title': post['data']['title'],
    'selftext': post['data']['selftext'],
    'score': post['data']['score']}, ignore_index=True)
print(df)
print(df["selftext"])

stats = []

for post in df["selftext"]:
    print(post)

    print(test.sentiment_vader(post))

    negative, neutral, positive, compound, overall_sentiment = test.sentiment_vader(post)
    stats.append(compound)

print(sum(stats))
