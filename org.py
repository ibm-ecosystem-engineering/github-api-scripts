import pandas as pd
import numpy as np
import argparse
import requests
import time


base_url = "https://api.github.com"


def invite_users_to_org(token, file, org):
    url = f'{base_url}/orgs/{org}/invitations'
    df = pd.read_csv(file)
    for index, row in df.iterrows():
        print(f'{row["Sr. No"]} - {row["Email"]} ({index})')
        payload = '{"email": "' + row['Email'] + '", "team_ids": [1]}'
        headers = {
            'Accept': 'application/vnd.github.v3+json',
            'Content-Type': 'application/json',
            'Authorization': 'token ' + token
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        if response.status_code != 201:
            failed = True
            print(response.text)
            while failed:
                print('Failed: will retry after 30sec')
                time.sleep(30)
                response = requests.request("POST", url, headers=headers, data=payload)
                if response.status_code == 201:
                    failed = False
        success_file = open("successes.txt", "a+")
        success_file.write(f'{row["Sr. No"]} - {row["Email"]}\n')
        success_file.close()
        time.sleep(1)


def add_team_members(token,org, team, users, role):
    for user in users:
        username = user['login']
        print(username)
        url = f'{base_url}/orgs/{org}/teams/{team}/memberships/{username}'
        payload = '{"role": "' + role + '"}'
        headers = {
            'Accept': 'application/vnd.github.v3+json',
            'Content-Type': 'application/json',
            'Authorization': 'token ' + token
        }
        response = requests.request("PUT", url, headers=headers, data=payload)
        if response.status_code != 200:
            failed = True
            print(response.status_code, response.text)
            while failed:
                print('Failed: will retry after 30sec')
                time.sleep(30)
                response = requests.request("PUT", url, headers=headers, data=payload)
                if response.status_code == 200:
                    failed = False
        time.sleep(0.1)


if __name__=="__main__":
    parser = argparse.ArgumentParser(description='GitHub organizations helper script.')
    parser.add_argument('action', help='Action to perform: one of {invite|add_team_members}')
    parser.add_argument('-t', '--token', required=True, dest='token', help='authentication token')
    parser.add_argument('-o', '--org', required=True, dest='org', help='GitHub organization')
    parser.add_argument('--team', dest='team', help='GitHub organization team')
    parser.add_argument('-r', '--role', dest='role', default="member", help='Team role')
    parser.add_argument('-f', '--file', dest='file', help='CSV file listing users. Needs to include columns "Email" (user email) and "Sr. No" (user int identifier)')

    args = parser.parse_args()

    # Handle action
    if args.action == "invite":
        invite_users_to_org(args.token, args.file, args.org)
    if args.action == "add_team_members":
        users = []
        for ix in range(3): # Assuming max 300 users per org
            url = f'{base_url}/orgs/{args.org}/members?per_page=100&page={ix+1}'
            headers = {
                'Accept': 'application/vnd.github.v3+json',
                'Authorization': 'token ' + args.token
            }
            response = requests.request("GET", url, headers=headers)
            users = users + response.json()
        add_team_members(args.token, args.org, args.team, users, args.role)
    else:
        parser.print_usage()
