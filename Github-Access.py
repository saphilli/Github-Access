from github import Github
import matplotlib.pyplot as plt
import numpy as np
import getpass

username = input("Please enter a Github username: ")
password = getpass.getpass() #receive the password securely without echoeing back to terminal
g = Github(username,password)
user = input("Enter a username to view their language stats: ")
languages = set([])
numberPerLanguage = {}
repos = []

#create set of all the repositories languages
for repo in g.get_user(user).get_repos():
    if repo.language != None:
        languages.add(repo.language)
    if repo.name != None:
        repos.append(repo)

#make array to store number of repositories per language
for lang in languages:
    count = 0
    for repo in repos:
        if repo.language == lang:
                count+=1
    numberPerLanguage[lang] = count

fig, ax = plt.subplots()
size = 0.3
slicesInner = []
slicesOuter = []
labelsOuter = []
labelsInner = []

for x in numberPerLanguage:
    slicesOuter.append(numberPerLanguage[x])
    c = 0
    tmpAr = []
    while c < numberPerLanguage[x]:
        tmpAr.append(1)
        c+=1
    slicesInner.append(tmpAr)
    labelsOuter.append(x+' ('+str(numberPerLanguage[x])+')')

slices = np.array(slicesInner)

for y in repos:
    labelsInner.append(y.name)
cmap = plt.get_cmap("tab20c")
outer_colours = cmap(np.arange(3)*4)
inner_colours = cmap(np.array([1, 2, 5, 6, 9, 10]))

ax.pie(slicesOuter,labels= labelsOuter,colors = outer_colours,
wedgeprops=dict(width=size, edgecolor='w'))
ax.pie(slices.sum(), radius=1-size,colors = inner_colours,shadow = True,wedgeprops=dict(width=size, edgecolor='w'))
ax.set(aspect="equal", title='Repositories per Language for '+user,)

plt.show()
