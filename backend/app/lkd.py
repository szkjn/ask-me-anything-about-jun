import requests

url = "https://www.linkedin.com/in/jun-suzuki/recent-activity/all/"
response = requests.get(url)
content = response.text

print(content)
