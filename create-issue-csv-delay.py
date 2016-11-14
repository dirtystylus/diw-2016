#!/usr/bin/python

# Derived from: http://vanderwijk.info/blog/creating-empty-placeholder-github-issues-automatically/

import sys
import csv
import time

sys.path.append("./PyGithub");
from github import Github

import getpass

# Authenticate to github.com and create PyGithub "Github" object
username = raw_input("Github username: ")
pw = getpass.getpass()
g = Github(username, pw)
user = g.get_user(username)

# repository like "dirtystylus/my-repo-name"
repository = "ENTER REPO NAME HERE"
repo = g.get_repo(repository)
milestone = repo.get_milestone(1)
labels = ["Launch Checklist"]
csv_file = "launch-checklist.csv"

with open(csv_file, 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
      issue = repo.create_issue("Launch Checklist: " + row[0], row[0], user, milestone, labels)
      print "Created issue Launch Checklist: " + row[0]
      time.sleep(2)
