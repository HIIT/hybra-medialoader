import requests

url = "https://ua.api.yle.fi/graphql?app_id=8d7303fe&app_key=105875199ef3a1f7e0fbf7e2834b2dc&query={uutisetMostRecentNews:articleList(publisher:YLE_UUTISET,limit:100,offset:0,coverage:NATIONAL){meta{count,total,remaining},items{fullUrl,properties}}}"


i = 0

while True:
    url = "https://ua.api.yle.fi/graphql?app_id=8d7303fe&app_key=105875199ef3a1f7e0fbf7e2834b2dc&query={uutisetMostRecentNews:articleList(publisher:YLE_UUTISET,limit:100,offset:" + str( i * 100 ) + ",coverage:NATIONAL){meta{count,total,remaining},items{fullUrl,properties}}}"

    r = requests.get( url )

    r = r.json()
    d = r['data']
    items = d['uutisetMostRecentNews']['items']

    for item in items:
        print item['fullUrl']

    if d['meta']['remaining'] < 100:
        return

    i += 1
