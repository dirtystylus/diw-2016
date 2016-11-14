#!/usr/bin/python                                                                    

# Taken from: https://github.com/UCSB-CS-Using-GitHub-In-Courses/PyGitHubExamples/blob/master/basicExample.py

import sys
sys.path.append("./PyGithub");
from github import Github

import getpass

# Authenticate to github.com and create PyGithub "Github" object
username = raw_input("Github username: ")
pw = getpass.getpass()
g = Github(username, pw)

# Use the PyGithub Github object g to do whatever you want,
# for example, list all your own repos (user is whichever user authenticated)

for repo in g.get_user().get_repos():
    print (repo.name)