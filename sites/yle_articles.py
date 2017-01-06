import requests

def parse(api_request):

    app_id = ""
    app_key = ""

    example_request = "https://articles.api.yle.fi/v2/articles.json?published_after=2016-12-20T12:00:00%2b0300&offset=0&limit=10"

    #r = requests.get( api_request )
    r = requests.get( example_request + "&app_id=" + app_id + "&app_key=" + app_key )
    print r.json()
