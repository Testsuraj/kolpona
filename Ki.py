import requests
import json
from datetime import datetime
import os
import time

# Constants for colored output
YELLOW = "\033[93m"
RED = "\033[91m"
GREEN = "\033[92m"
WHITE = "\033[97m"
GREY = "\033[90m"
NEWLINE = "\n"

# Global variables
l = "-" * 50  # Separator line

# Configuration - REPLACE THESE WITH YOUR ACTUAL VALUES
CONFIG = {
  'User_Agent': 'Mozilla/5.0 (Linux; Android 13; sdk_gphone_x86_64 Build/TE1A.220922.033; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/103.0.5060.71 Mobile Safari/537.36',  # Replace with actual user agent
        'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY3ZmJlMjYzN2MwOTg3MDI4YjU3Mzk2MiIsInVzZXJuYW1lIjoic3k5MDUzOTg4IiwiZW1haWwiOiJzeTkwNTM5ODhAZ21haWwuY29tIiwiYWRtaW4iOmZhbHNlLCJpYXQiOjE3NDQ1NjE0ODMsImV4cCI6MTkwMjM0OTQ4M30.Yqi6sgCre97LH-l5d_Y0LsN-jvY2ER7Xz2AlFYR_sPc',     # Replace with actual auth token
        'Auth': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY3ZmJlMjYzN2MwOTg3MDI4YjU3Mzk2MiIsImlhdCI6MTc0NDU2MTM4MiwiZXhwIjoxODA3Njc2NTgyfQ.1WljN3BxfAiFLd7fErSk32LGbuHc_HDBlZQ1iER7MNs'             # Replace with actual auth token
}

def save_data(key):
    return CONFIG.get(key, "")

def header0():
    return {
        "accept": "*/*",
        "authorization": save_data('authorization'),
        "user-agent": save_data('User_Agent'),
        "content-type": "application/json",
        "origin": "https://spincoin.appmobile.top",
        "x-requested-with": "com.spincoin.appmobile.top",
        "referer": "https://spincoin.appmobile.top/dashboard"
    }

def headers():
    return {
        "host": "spincoin.appmobile.top",
        "accept": "application/json, text/plain, */*",
        "authorization": save_data('Auth'),
        "user-agent": "okhttp/4.9.2"
    }

def headers1():
    return {
        "host": "spincoin.appmobile.top",
        "accept": "application/json, text/plain, */*",
        "authorization": save_data('Auth'),
        "content-type": "application/json",
        "user-agent": "okhttp/4.9.2"
    }

def run(url, headers, data=None):
    try:
        if data:
            response = requests.post(url, headers=headers, data=data, timeout=10)
        else:
            response = requests.get(url, headers=headers, timeout=10)
        
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"{RED}Error in request to {url}: {str(e)}{WHITE}")
        return None

def run1(url, headers):
    return run(url, headers)

def fast(text):
    print(text, end="")

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner(title):
    print(f"{GREEN}{'=' * 50}")
    print(f"{title.center(50)}")
    print(f"{'=' * 50}{WHITE}")

def dashboard():
    global l
    data = {
        "operationName": "getUser",
        "variables": {},
        "query": """query getUser {
          getUser {
            id balance credits username email admin status createAt log xp level 
            next_level bonus_level address_fp bonus_loyalty total_earn ref
            statistics_earn { id clicks total __typename }
            __typename
          }
        }"""
    }
    req = json.dumps(data)
    response = run('https://spincoin.appmobile.top/graphql', header0(), req)
    
    if not response:
        print(f"{RED}Failed to fetch dashboard data{WHITE}")
        return False
    
    try:
        r = json.loads(response)
        user = r['data']['getUser']
        
        fast(f"{YELLOW}Welcome Back{RED} ➞ {GREEN}{user['username']}{NEWLINE}")
        fast(f"{YELLOW}Your Level{RED} ➞ {GREEN}{user['level']}{RED} | {YELLOW}level-Bonus{RED} ➞ {GREEN}{user['bonus_level']}{NEWLINE}")
        fast(f"{YELLOW}Your Balance{RED} ➞ {GREEN}{user['balance']}{NEWLINE}")
        fast(f"{YELLOW}Your Spin{RED} ➞ {GREEN}{user['credits']}{NEWLINE}")
        print(f"{GREEN}{l}")
        return True
    except Exception as e:
        print(f"{RED}Error parsing dashboard data: {str(e)}{WHITE}")
        return False

def spin():
    global l
    xyz = 0
    
    while True:
        data = {
            "operationName": "earnRollGame",
            "variables": {"token": "token_recaptcha"},
            "query": """mutation earnRollGame($token: String) {
              earnRollGame(token: $token) {
                user {
                  id balance credits username email admin status createAt log xp level
                  next_level bonus_level address_fp bonus_loyalty total_earn
                  statistics_earn { id clicks total __typename }
                  __typename
                }
                result
                spin { spinOne spinTwo __typename }
                notification
                __typename
              }
            }"""
        }
        
        req = json.dumps(data)
        response = run('https://spincoin.appmobile.top/graphql', header0(), req)
        
        if not response:
            print(f"{RED}Failed to spin, retrying in 10 seconds...{WHITE}")
            time.sleep(10)
            continue
            
        try:
            r = json.loads(response)
            result = r['data']['earnRollGame']
            user = result['user']
            
            now = datetime.now().strftime('%d/%b/%Y %H:%M:%S')
            xyz += 1
            
            fast(f"{WHITE}[{GREEN}✓{WHITE}]{GREEN} Reward {RED}➞ {GREY}{result['result']}{GREEN} COINS!{RED} ➞ {WHITE}[{GREEN}{xyz}{WHITE}]{NEWLINE}")
            fast(f"{WHITE}[{YELLOW}+{WHITE}] {GREEN}Your Balance {RED}➞ {GREY}{user['balance']}{GREEN} COINS!{NEWLINE}")
            fast(f"{WHITE}[{RED}-{WHITE}] {GREEN}Your Spins {RED}➞ {GREY}{user['credits']}{NEWLINE}")
            fast(f"{WHITE}[{GREEN}✓{WHITE}]{GREEN} Progress {RED}➞ {GREY}level {int(user['level'])+1}{RED} ➞ {WHITE}({GREEN}{user['xp']}{WHITE}/{GREEN}{user['next_level']}{WHITE}){NEWLINE}")
            fast(f"{WHITE}[{GREEN}✓{WHITE}]{GREEN} Date {RED}➞ {WHITE}[{GREEN}{now}{WHITE}]{NEWLINE}")
            print(f"{GREEN}{l}")
            
            if user['credits'] == 0:
                getspin1()
                # Check spins again
                if not dashboard():  # If dashboard fails, pause before retrying
                    time.sleep(10)
                    continue
                
                if user['credits'] == 0:
                    getspin()
                    
            time.sleep(1)  # Add small delay between spins
            
        except Exception as e:
            print(f"{RED}Error processing spin result: {str(e)}{WHITE}")
            time.sleep(5)
            continue

def getspin():
    response = run('https://spincoin.appmobile.top/api/v1/users/getCaptchar', headers())
    if not response:
        return False
        
    try:
        r = json.loads(response)
        key = r['data']['key']
        data = json.dumps({"array_img": [key, key]})
        run('https://spincoin.appmobile.top/api/v1/users/validRecaptcha', headers1(), data)
        run1('https://spincoin.appmobile.top/api/v1/users/getCredits', headers())
        run1('https://spincoin.appmobile.top/api/v1/users/setSpinClick', headers())
        run1('https://spincoin.appmobile.top/api/v1/users/getClick', headers())
        return True
    except Exception as e:
        print(f"{RED}Error in getspin: {str(e)}{WHITE}")
        return False

def getspin1():
    run1('https://spincoin.appmobile.top/api/v1/users/getCredits', headers())
    run1('https://spincoin.appmobile.top/api/v1/users/setSpinClick', headers())
    run1('https://spincoin.appmobile.top/api/v1/users/getClick', headers())

if __name__ == "__main__":
    clear()
    banner('spin-coin')
    
    if not dashboard():
        print(f"{RED}Initial dashboard failed, check your authentication tokens{WHITE}")
    else:
        spin()
