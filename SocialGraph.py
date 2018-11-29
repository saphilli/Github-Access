from github import Github
import matplotlib.pyplot as plt
import numpy as np
import getpass
import json


while True:
    try:
        username = input("Please enter a Github username: ")
        password = getpass.getpass() #receive the password securely without echoeing back to terminal
        g = Github(username,password)
        authen_user = g.get_user(username)
    except Exception:
        print("Invalid credentials")
        continue;
    else:
        print('Logged in as '+username)
        break;

languages = set([])
repos = []
user = input("Enter a Github username to view their stats: ")
#create set of all the repositories languages
for repo in g.get_user(user).get_repos():
    print(repo.name , "\n -" ,repo.language)
    if repo.language != None:
        languages.add(repo.language)
    if repo.name != None:
        repos.append(repo.name)

    #print repo.get_dir_contents(repo.name)
def writeToJSON(path,fileName,data):
    filePathName= path+'/'+fileName+'.json'
    with open(filePathName,'w') as out:
        json.dump(data,out)

path='./'
fileName1 = 'languages'
fileName2 = 'repos'
writeToJSON(path,fileName1,list(languages))
writeToJSON(path,fileName2,repos)
