#!/usr/bin/python

# Derived from: http://vanderwijk.info/blog/creating-empty-placeholder-github-issues-automatically/

import sys
sys.path.append("./PyGithub");
from github import Github

import getpass

# Authenticate to github.com and create PyGithub "Github" object
username = raw_input("Github username: ")
pw = getpass.getpass()
g = Github(username, pw)

# repository like "dirtystylus/my-repo-name"
repository = "ENTER REPO NAME HERE"
repo = g.get_repo(repository)


issue = repo.create_issue("Test issue", "This is a test issue.")
