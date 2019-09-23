import requests

url = "https://api.betaseries.com/shows/list"

querystring = {"key":"7c2f686dfaad","v":"3.0","limit":"10"}

response = requests.request("GET", url, params=querystring)

print(response.json())