import requests

def parse(api_request):

    app_id = "f3365695"
    app_key = "7010dcef0cf2393423e747473b6068c"

    example_request = "https://articles.api.yle.fi/v2/articles.json?published_after=2016-12-20T12:00:00%2b0300&offset=0&limit=10"

    #r = requests.get( api_request )
    r = requests.get( example_request + "&app_id=" + app_id + "&app_key=" + app_key )
    print r.json()
