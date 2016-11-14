# To get this to run I had to map to where my python packages were being stored. Check where this is located on your machine:
# export PYTHONPATH=/Library/Python/2.7/site-packages (work machine)
# export PYTHONPATH=/usr/local/lib/python2.7/site-packages (home machine)
# https://github.com/google/google-api-python-client/issues/100#issuecomment-139660908

from __future__ import print_function
import httplib2
import os
import csv
import getpass
import sys
import time
import oauth2client
sys.path.append("./PyGithub");
from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
from github import Github


try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# Most of below code is pulled from https://developers.google.com/sheets/quickstart/python
# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json

SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Sheets API Python Quickstart'


def get_credentials():

    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """

    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():

    # authenticate the user
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    # prompt user for sheet key, username, password, and repo name
    spreadsheetId = raw_input("Google sheet key (found in the URL): ")
    rangeName = 'Sheet1'
    result = service.spreadsheets().values().get(
                                                 spreadsheetId=spreadsheetId, range=rangeName).execute()
    values = result.get('values', [])

    if not values:
    	print('No data found for this key.')
    else:
        # time to create issues!
        # Authenticate to github.com and create PyGithub "Github" object
        username = raw_input("Github username: ")
        pw = getpass.getpass()
        g = Github(username, pw)
        r = raw_input("Repository name: ")
        repository = username + "/" + r
        repo = g.get_repo(repository)
        user = g.get_user(username)
        milestone = repo.get_milestone(1)
        # print(values)
        for row in values:
            label = [row[1]]
            issue = repo.create_issue(row[0], row[0], user, milestone, label)
            # print(row[1])

    # print confirmation
    print(len(values), "issues created in", repository)

if __name__ == '__main__':
    main()
