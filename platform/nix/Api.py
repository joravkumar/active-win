import sys
import requests
try:
    API_Url = sys.argv[1]
    url = API_Url+"/api/v1/browser-access-list"
    #url = "https://whdemo.maxicus.com/api/v1/browser-access-list"
    response = requests.request("GET", url)
    print(response.text)
    data = open('/tmp/leap_log.json', 'w')
    data.writelines(response.text)
    data.close()
except:
    APP_LIST = '[{"Google Chrome":"search"},{"Google Chrome": "Type a URL"},{"Google Chrome": "Address"},{"Chromium":"search bar"},{"Firefox":"Search with Google or enter address"},{"Brave Browser":"search bar"}]'
    print(APP_LIST)
    data = open('/tmp/leap_log.json', 'w')
    data.writelines(APP_LIST)
    data.close()
