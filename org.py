import pandas as pd
import argparse
import requests
import time

def invite_users_to_org(token, file, org):
    url = f'https://api.github.com/orgs/{org}/invitations'
    df = pd.read_csv(file)
    for index, row in df.iterrows():
        print(f'{row["Sr. No"]} - {row["Email"]} ({index})')
        payload='{"email": "' + row['Email'] + '"}'
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


if __name__=="__main__":
    parser = argparse.ArgumentParser(description='GitHub organizations helper script.')
    parser.add_argument('action')
    parser.add_argument('-t', '--token', required=True, dest='token', help='authentication token')
    parser.add_argument('-f', '--file', required=True, dest='file', help='CSV file name')
    parser.add_argument('-o', '--org', required=True, dest='org', help='GitHub organization')

    args = parser.parse_args()

    # Handle action
    if args.action == "invite":
        invite_users_to_org(args.token, args.file, args.org)
    else:
        parser.print_usage()
