from ast import Pass
import pyatspi
import time
import json
import requests
import dotenv
from dotenv import load_dotenv
from pathlib import Path
from os.path import exists

APP_LIST = []
response_data = '[{"Google Chrome":"search"},{"Chromium":"search bar"},{"Firefox":"Search with Google or enter address"},{"Brave Browser":"search bar"}]'
try:
    env_path = ('/tmp/.env')
    file_exists = exists(env_path)
    if file_exists:
        load_dotenv(env_path)
        leap_status = dotenv.get_key(env_path, 'login')

        # print(leap_status)
        if str(leap_status) == "1":
            # print("pass")
            dotenv.set_key(env_path, "login", ('0'))
            API_Url = dotenv.get_key(env_path, 'path')
            # print(API_Url)
            try:
                # API Call
                url = str(API_Url)+"/api/v1/browser-access-list"
                #url = "https://whdemo.maxicus.com/api/v1/browser-access-list"
                response = requests.request("GET", url)
                if("200" in str(response)):
                    if dotenv.get_key(env_path, 'response') != None:
                        dotenv.unset_key(env_path, "response")
                        dotenv.set_key(env_path, "\nresponse", (response.text))
                    else:
                        dotenv.set_key(env_path, "\nresponse", (response.text))
                # print(response.text)
                # print(response)
                # if Api Fail
                # print(response)
                if("200" not in str(response)):
                    raise Exception
            except:
                if dotenv.get_key(env_path, 'response') != None:
                    dotenv.unset_key(env_path, "response")
                    dotenv.set_key(env_path, "\nresponse", (response_data))
                else:
                    dotenv.set_key(env_path, "\nresponse", (response_data))
                # print("pass")
        else:
            if dotenv.get_key(env_path, 'response') == None:
                # print("pass")
                dotenv.set_key(env_path, "\nresponse", (response_data))

    else:
        raise Exception
except:
    APP_LIST = [("Google Chrome", "search"),
                ("Chromium", "search bar"),
                ("Firefox", "Search with Google or enter address"),
                ("Brave Browser", "search bar")]
else:
    env_response = dotenv.get_key(env_path, 'response')
    data = json.loads(env_response)
    # print(data)
    for i in data:
        APP_LIST.extend(list(i.items()))
#print(APP_LIST)
##############################################################################
# Find the desired app on the desktop


def find_app(desktop, text):
    try:
        for app in desktop:
            try:
                # print(app)
                # print(app.get_name())
                if app.get_name() == text:
                    return app
            finally:
                pass
    finally:
        pass

    return None

# Find the address bar component under the provided root component


def find_address_bar(root, text):
    if root is not None:
        try:

            if root.get_name().find(text) != -1:
                # print("root",root)
                return root

        finally:
            pass

        for child in root:
            obj = find_address_bar(child, text)
            if obj is not None:
                return obj

    return None

# Returns the text of the address bar component
# Filters out undesired URLs and text


def parse_url(obj, ignored_text=[]):
    #print (obj)
    url = obj.get_text(0, -1).strip()

    if url is None:
        return ''

    for item in ignored_text:
        if url.startswith(item):
            return ''

    return url


IGNORED_TEXT = [
    "Address",
    "chrome:",
    "about:"
]

# while True:


def get_url(app_list):
    # print(app_list)
    # Iterate through all desktops
    for index in range(pyatspi.Registry.getDesktopCount()):
        desktop = pyatspi.Registry.getDesktop(index)
        # print(desktop)
        for app_name, address_name in app_list:
            #print("appname ",app_name)
            #print("address_name ",address_name)
            # Find an instance of the desired apps
            app = find_app(desktop, app_name)
            #print ("app list ", app)
            if app is not None:
                # print("Pass")
                for window in app:
                    try:
                        # print(window.getState().contains(pyatspi.STATE_ACTIVE))
                        # Check if window of app is currently in the foreground
                        if window.getState().contains(pyatspi.STATE_ACTIVE):
                            # Find the address bar component
                            # print("Pass")
                            address_bar = find_address_bar(
                                window, address_name)
                            #print ('address bar',address_bar)
                            #print ('windows', window)
                            if address_bar is not None:
                                try:
                                    # Get the URL from the component
                                    return app_name, parse_url(address_bar, IGNORED_TEXT)
                                except:
                                    return '', ''
                    finally:
                        pass
        return '', ''


# App entry point
if __name__ == "__main__":
    browser, url = "", ""
    try:
        browser, url = get_url(APP_LIST)
    except:
        browser = ""
        url = ""

    # Print in JSON format to stdout
    print('{{"browser":"{}", "url":"{}"}}'.format(browser, url))
    # time.sleep(1)
