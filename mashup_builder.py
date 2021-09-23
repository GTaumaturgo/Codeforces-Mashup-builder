import requests
import json
import random
import time
url_problems = "http://codeforces.com/api/problemset.problems"
url_submissions = "http://codeforces.com/api/user.status?handle={}&count={}"

def getACsByUser(handle, cnt):
    while True:
        ans = requests.get('http://codeforces.com/api/user.status?handle={}&count={}'.format(handle, cnt)).json()
        if ans['status'] == 'OK': 
            break
        time.sleep(0.3)
    try :
        return [(str(submition['contestId']) + str(submition['problem']['index'])) for submition in ans['result'] if submition['verdict'] == 'OK']
    except :
        return []
        
def notFoundSomething():
    print("alguma das dificuldades nao tem nenhum problema nela! encerrando!")
    exit(0)


print("Fetching problems...")
prob_list = list(filter(lambda d : 'rating' in d, requests.get(url_problems).json()['result']['problems']))

handle_list = []
dif_set = set()
dif_count = {}
tags = []

with open("tags") as file:
    for line in file:
        tags.append(line.strip())
with open("handles") as file :
    for line in file :
        handle_list.append(line.strip())
with open("difficulties") as file :
    for line in file :
        dif = int(line.strip())
        dif_set.add(dif)
        if dif in dif_count:
            dif_count[dif] += 1
        else:
            dif_count[dif] = 1

ACed_problems = set()

print("Fetching handles...")
for handle in handle_list :
    print(handle)
    ACed_problems.update(getACsByUser(handle, 1000))



dificulties_dict = {}
for prob in prob_list:

    if str(prob['contestId'])+prob['index'] in ACed_problems:
        continue

    tagNotFound = 0
    for tag in tags:
        if tag not in prob['tags']:
            tagNotFound = 1
            break
    
    if tagNotFound: continue

    rat = int(prob['rating'])
    if rat in dificulties_dict :
        dificulties_dict[rat].append(str(prob['contestId']) + prob['index'])
    else : 
        dificulties_dict[rat] = [str(prob['contestId']) + prob['index']]

for key in dificulties_dict :
    print("Na dificuldade %d tem %d problemas!" % (key, len(dificulties_dict[key])))

print("Fetching problems not Aced by any user...")
taken = set()
for dif in dif_set :

    if dif not in dificulties_dict:
        print(dif)
        notFoundSomething()

    if len(dificulties_dict[dif]) < dif_count[dif]:
        print(dif)
        notFoundSomething()
    
    elif len(dificulties_dict[dif]) == dif_count[dif]:
        #random is useless here
        for prob in dificulties_dict[dif]:
            taken.add((dif,(prob)))
    
    else:
        for i in range(dif_count[dif]):
            while(True):

                ind = random.randint(0, len(dificulties_dict[dif]) - 1)
                
                if (dif, dificulties_dict[dif][ind]) not in taken and dificulties_dict[dif][ind] not in ACed_problems:
                    taken.add((dif ,(dificulties_dict[dif][ind])))
                    break

print("Results!")
l = list(taken)
l = sorted(l)
for problem in l :
    print("(%d,%s)" % (problem[0],problem[1]))