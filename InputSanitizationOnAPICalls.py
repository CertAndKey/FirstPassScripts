#!/usr/bin/env python3
#user command line inputs shoud be: API file, camera IP, camera HTTP port, camera root username, camera root password, fuzz file
#
#API file should list APIs with inputs labled as {INPUT}
#fuzz file should contain list of malicious strings, BLNS is a good one to use
#

import requests
import sys
import random
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.auth import HTTPBasicAuth
from requests.auth import HTTPDigestAuth

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class colors:
    On_Red = '\033[41m'
    On_Green = '\033[42m'
    Color_Off = '\033[0m'
    BWhite = '\033[1;37m'

if len(sys.argv) != 7:
    print(colors.BWhite + "Invalid Arguments")
    print("python3 AuthenticationCheckOnAPICalls.py <api_file> <camera_IP> <camera_HTTP_port> <camera_username> <camera_password> <fuzz_file>")
    print(colors.On_Red + "Failed" + colors.Color_Off)
    quit()



### Command Line Args ###
api_file     = sys.argv[1]
camera_ip    = sys.argv[2]
camera_port  = sys.argv[3]
user         = sys.argv[4]
password     = sys.argv[5]
fuzz_file    = sys.argv[6]

failed = 0

url = "http://"+ camera_ip + ":" + camera_port

### See if fuzz list and API list exists ###
try:
    text_file = open(fuzz_file, "r")
    file = open(api_file, "r")
    bad_strings = text_file.readlines()
    text_file.close()
except:
    print(colors.BWhite + "Couldn't find file:" + fuzz_file)
    print(colors.On_Red + "Failed" + colors.Color_Off)
    quit()

### Checks if camera is still responsive ###
def test_req(urls):
    try:
        global url
        test_req = requests.get(url)
    except:
        print(colors.BWhite + urls +": crashed the camera")
        print(colors.On_Red + "FAILED" + colors.Color_Off)
        quit()

### Gets a random fuzz string ####
def randomize():
    num = random.choice(bad_strings)
    return num


###Checks if camera is reachable###
try:
    test_req = requests.get(url)
except:
    print(colors.BWhite + "Couldn't find camera")
    print(colors.On_Red + "FAILED" + colors.Color_Off)
    quit()




### iterates through API file and fills in {INPUT} values with bad strings###
########### sends these API endpoints to camera and reads response ##########
for api in file:
    api = api.strip()
    url_full = url + api
    url_full_copy = url_full
    i = 0
    while (i < 50):
        while "{INPUT}" in url_full_copy:
            url_full_copy = url_full_copy.replace("{INPUT}", randomize(),1)
        try:
            #####   BASIC AUTH #####
            #GETS
            r = requests.get(url_full_copy, auth=HTTPBasicAuth(user, password),timeout=10)
            #POSTS
            r = requests.post(url_full_copy, auth=HTTPBasicAuth(user,password),timeout=10)
            #PUTS
            r = requests.put(url_full_copy, auth=HTTPBasicAuth(user,password),timeout=10)

            #####    DIGEST AUTH    #####
            #GETS
            r = requests.get(url_full_copy, auth=HTTPDigestAuth(user,password),timeout=10)
            #POSTS
            r = requests.post(url_full_copy, auth=HTTPDigestAuth(user,password),timeout=10)
            #PUTS
            r = requests.put(url_full_copy, auth=HTTPDigestAuth(user,password),timeout=10)

            #####   NO AUTH    #####
            #GETS
            r = requests.get(url_full_copy,timeout=10)
            #POSTS
            r = requests.post(url_full_copy,timeout=10)
            #PUTS
            r = requests.put(url_full_copy,timeout=10)
        except:
            print(colors.BWhite + "The following endpoint caused a crash!")
            print(url_full_copy.encode('utf-8'))
            print(colors.On_Red + "FAILED" + colors.Color_Off)
            quit()

        i += 1
        url_full_copy= url_full


#####################   PASS/FAIL    ####################################
if failed == 1:
    print(colors.On_Red + colors.BWhite + "FAILED" + colors.Color_Off)
else:
    print(colors.On_Green + colors.BWhite + "PASS" + colors.Color_Off)

