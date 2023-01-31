#!/usr/bin/env python3

#run this script by using the following format
#"python3 AuthenticationCheckOnAPICalls.py <api_file> <camera_IP> <camera_HTTP_port>"
#
#for the API file.....
#please enter API values with leading slashes included
#each API should be on its own line
#example....
#/api/GetMac
#/api/GetStats
#/api/GetTime

import requests
import sys
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.auth import HTTPBasicAuth
from requests.auth import HTTPDigestAuth

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class colors:
    On_Red = '\033[41m'
    On_Green = '\033[42m'
    Color_Off = '\033[0m'
    BWhite = '\033[1;37m'

if len(sys.argv) != 4:
    print(colors.BWhite + "Invalid Arguments")
    print("python3 AuthenticationCheckOnAPICalls.py <api_file> <camera_IP> <camera_HTTP_port>")
    print(colors.On_Red + "Failed" + colors.Color_Off)
    quit()


api_file     = sys.argv[1]
camera_ip    = sys.argv[2]
camera_port  = sys.argv[3]

failed = 0

url = "http://"+ camera_ip + ":" + camera_port
test_user = "admin"
test_pw   = "password"


file = open(api_file,"r")

def test_stat_code(code, tested_url, auth_type):
    if code != 400 and code != 401 and code != 403 and code != 404 and code != 405:
        global failed 
        failed = 1
        print(colors.On_Red + colors.BWhite + str(code) + colors.Color_Off + "  " + colors.BWhite + tested_url + "  " + auth_type)

try:
    test_req = requests.get(url)
except:
    print(colors.BWhite + "Couldn't find camera")
    print("python3 AuthenticationCheckOnAPICalls.py <api_file> <camera_IP> <camera_HTTP_port>")
    print(colors.On_Red + "FAILED" + colors.Color_Off)
    quit()



for api in file:
    api = api.strip()
    url_full = url + api
    
###########################  BASIC AUTH          #######################
    #GETS
    r = requests.get(url_full, auth=HTTPBasicAuth(test_user,test_pw))
    test_stat_code(r.status_code,url_full, "Basic Auth")
    
    #POSTS
    r = requests.post(url_full, auth=HTTPBasicAuth(test_user,test_pw))
    test_stat_code(r.status_code,url_full, "Basic Auth")
    
    #PUTS
    r = requests.put(url_full, auth=HTTPBasicAuth(test_user,test_pw))
    test_stat_code(r.status_code,url_full, "Basic Auth")

    #PATCHES
    r = requests.patch(url_full, auth=HTTPBasicAuth(test_user,test_pw))
    test_stat_code(r.status_code,url_full, "Basic Auth")

############################    DIGEST AUTH       #######################
    #GETS
    r = requests.get(url_full, auth=HTTPDigestAuth(test_user,test_pw))
    test_stat_code(r.status_code,url_full, "Digest Auth")

    #POSTS
    r = requests.post(url_full, auth=HTTPDigestAuth(test_user,test_pw))
    test_stat_code(r.status_code,url_full, "Digest Auth")

    #PUTS
    r = requests.put(url_full, auth=HTTPDigestAuth(test_user,test_pw))
    test_stat_code(r.status_code,url_full, "Digest Auth")

    #PATCHES
    r = requests.patch(url_full, auth=HTTPDigestAuth(test_user,test_pw))
    test_stat_code(r.status_code,url_full, "Digest Auth")

####################     NO AUTH     ####################################
    #GETS
    r = requests.get(url_full)
    test_stat_code(r.status_code,url_full, "No Auth")

    #POSTS
    r = requests.post(url_full)
    test_stat_code(r.status_code,url_full, "No Auth")

    #PUTS
    r = requests.put(url_full)
    test_stat_code(r.status_code,url_full, "No Auth")

    #PATCHES
    r = requests.patch(url_full)
    test_stat_code(r.status_code,url_full, "No Auth")


#####################   PASS/FAIL    ####################################
if failed == 1:
    print(colors.On_Red + colors.BWhite + "FAILED" + colors.Color_Off)
else:
    print(colors.On_Green + colors.BWhite + "PASS" + colors.Color_Off)

