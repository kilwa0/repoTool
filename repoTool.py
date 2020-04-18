#!/usr/bin/env python3
from github import Github, GithubException
import sys
import urllib3
import os
import errno
import glob
import re


class GitConn:
    """Simple class to define Github connections."""

    def __init__(self, token, host):
        self.token = token
        self.host = host
        if host != "github.com":
            self.g = Github(base_url="https://%s/api/v3" % host,
                            login_or_token=token, verify=False)
        else:
            self.g = Github(token)


# Disable Warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Set Base Dir
basePath = os.path.abspath('.')

tOrigin = ""  # Token Origin
tDestination = ""  # Token Destination
hOrigin = ""  # Host Origin
hDestination = ""  # Host Destination
organitationDest = ""  # Organitation


def cloneUserOrgs():
    connOrigin = GitConn(tOrigin, hOrigin)
    orgOrigin = connOrigin.g.get_user().get_orgs()
    try:
        os.mkdir("%s/repo" % basePath)
    except OSError as e:
        if e.errno == errno.EEXIST:
            if os.name == 'nt':
                os.system('rd /Q /S %s\\repo' % basePath)
                os.system('md %s\\repo' % basePath)
            else:
                os.system('rm -rf %s/./repo/*' % basePath)
        else:
            raise
    for organization in orgOrigin:
        for repo in\
         connOrigin.g.get_organization(organization.login).get_repos():
            print(repo.clone_url)
            try:
                os.mkdir("%s/./repo/%s" % (basePath, organization.login))
            except OSError as e:
                if e.errno == errno.EEXIST:
                    pass
                else:
                    raise
                tokenUrl = re.sub("https://",
                                  ("https://%s:@" % tOrigin), repo.clone_url)
                os.system('cd %s/repo/%s && git clone --mirror %s' %
                          (basePath, organization.login, tokenUrl))


def makeUrls():
    orgDestination = GitConn(tDestination,
                             hDestination).g.get_organization(organitationDest)

    orgNames = os.listdir('%s/repo' % basePath)
    for dir in orgNames:
        resposName = os.listdir('%s/repo/%s' % (basePath, dir))
        for repo in resposName:
            newRepo = "%s.%s" % (dir, repo)
            repoFmt = "eac.aws.%s" % re.sub(
                "-", ".", (re.sub("/", ".", newRepo))
                )
            if orgDestination.login is None:
                print("Error: organitation method return None")
            else:
                print(repoFmt.lower())
                orgDestination.create_repo(repoFmt.lower())


def pushRepos():
    orgDestination = GitConn(tDestination,
                             hDestination).g.get_organization(organitationDest)

    orgNames = os.listdir('%s/repo' % basePath)
    for dir in orgNames:
        resposName = os.listdir('%s/repo/%s' % (basePath, dir))
        for repo in resposName:
            newRepo = "%s.%s" % (dir, repo)
            repoFmt = "eac.aws.%s" % re.sub(
                "-", ".", (re.sub("/", ".", newRepo))
                )
            if orgDestination.login is None:
                print("Error: organitation method return None")
            else:
                me = ("https://%s@%s/%s/%s" %
                      (tDestination, hDestination, organitationDest,
                       repoFmt.lower()))
    tlzOrgs = glob.glob(os.path.abspath("%s/./repo/*" % basePath))
    for repos in tlzOrgs:
        subDir = repos + "/*"
        indivRepo = glob.glob(subDir)
        for sep in indivRepo:
            os.system('cd %s && pwd' % sep)
            os.system('cd %s && git push --mirror %s' % (sep, me))


def listRepo():
    tlzOrgs = glob.glob(os.path.abspath("%s/./repo/*" % basePath))
    for repos in tlzOrgs:
        subDir = repos + "/*"
        indivRepo = glob.glob(subDir)
        for sep in indivRepo:
            print(sep)
    return sep


def deleteRepos():
    orgDestination = GitConn(tDestination,
                             hDestination).g.get_organization(organitationDest)
    for repoToDelete in orgDestination.get_repos():
        print(repoToDelete)
        repoToDelete.delete()


try:
    action = sys.argv[1]
    if action == "clone":
        cloneUserOrgs()
    elif action == "list":
        listRepo()
    elif action == "makeUrls":
        makeUrls()
    elif action == "pushRepos":
        pushRepos()
    elif action == "deleteRepos":
        try:
            deleteRepos()
            deleteRepos()
        except GithubException:
            print("Organitation: %s Clean" % organitationDest)
        # deleteRepos()
    else:
        print("What do we Mooo? (clone / list / makeUrls / pushRepos / \
deleteRepos)")
except IndexError:
    action = ""
    print("What do we Mooo? (clone / list / makeUrls / pushRepos / \
deleteRepos)")
