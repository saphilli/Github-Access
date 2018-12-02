from github import Github
import matplotlib.pyplot as plt
import numpy as np
import getpass
import json
from datetime import datetime
from datetime import timedelta


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



user = input("Enter a Github username to view their stats: ")

#get a repository
print("Below is a list of the user's repositorys")
for repo in g.get_user("YasirZardari").get_repos():
    print(repo.name )

repo_name = input("Please enter one of the repository names listed above: ")
repo = g.get_user("YasirZardari").get_repo("Speech-Therapy-App")

commits = repo.get_commits() #(reverse the list of commits to get first one)
lastCommitDate = str.split(str(commits[0].commit.author.date))[0] #isolate the date from time
commits = commits.reversed
firstCommitDate = str.split(str(commits[0].commit.author.date))[0]

#create an array of commit dates and their authors in chronological order
commitStats = []
for c in commits:
    date = str.split(str(c.commit.author.date)) #split date and time into array
    name = str(c.commit.author.name)
    dateAndAuthor = date[0]+" "+ name.replace(" ","")
    commitStats.append(dateAndAuthor)

def stringToDate(date):
    splitDate = str.split(date,"-")
    dateObject = datetime(int(splitDate[0]),int(splitDate[1]),int(splitDate[2]))
    dateObject =datetime.date(dateObject)
    return dateObject

currentCommitDate = stringToDate(firstCommitDate)
lastCommitDate = stringToDate(lastCommitDate)

#create dictionary of contributor names and initialize commit count to 0
contributors = {}
for username in repo.get_contributors():
    contributors[username.login] = 0

def writeToJS(data):
    with open("./data.js", 'a') as file:
        file.write(data)

writeToJS("var data = [ \n") #start off the javascript data file
#construct the js file
while(currentCommitDate<=lastCommitDate):
    writeToJS("{\n'day':"+str(currentCommitDate.day)
    +",\n'month':" +str(currentCommitDate.month)
    +",\n'year':"+str(currentCommitDate.year) +",\n'values': [\n")

    for i in commitStats:
        if(stringToDate(i[0:10])==currentCommitDate):
            contributors[i[11:50]]+=1
    count = 0
    for j in contributors:
        count+=1
        writeToJS("{'value':"+str(contributors[j])+ ",\n'name':'"+ str(j)+ "'}\n")
        if(count!=len(contributors)):
            writeToJS(",")
        else:
            writeToJS("]\n}")
    currentCommitDate += timedelta(days=1)
    if (currentCommitDate<=lastCommitDate):
        writeToJS(",")
    else:
        writeToJS("]")
