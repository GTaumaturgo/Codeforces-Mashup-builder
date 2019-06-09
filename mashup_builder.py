import requests
import json
import random
import time
url_problems = "http://codeforces.com/api/problemset.problems"
url_submissions = "http://codeforces.com/api/user.status?handle={}&count={}"

def getACsByUser(handle, cnt):
    while True:
        ans = requests.get('http://codeforces.com/api/user.status?handle={}&count={}'.format(handle, cnt)).json()
        if ans['status'] == 'OK': break
        time.sleep(0.3)
    return [(str(submition['contestId']) + str(submition['problem']['index'])) for submition in ans['result'] if submition['verdict'] == 'OK']

print("Fetching problems...")
prob_list = list(filter(lambda d : 'rating' in d, requests.get(url_problems).json()['result']['problems']))

handle_list = []
dif_list = []
with open("handles") as file :
    for line in file :
        handle_list.append(line.strip())
with open("difficulties") as file :
    for line in file :
        dif_list.append(int(line.strip()))


ACed_problems = set()

print("Fetching handles...")
for handle in handle_list :
    print(handle)
    ACed_problems.update(set(getACsByUser(handle, 400)))



dificulties_dict = {}
for prob in prob_list:
    rat = int(prob['rating'])
    if rat in dificulties_dict :
        dificulties_dict[rat].append(str(prob['contestId']) + prob['index'])
    else : 
        dificulties_dict[rat] = [str(prob['contestId']) + prob['index']]

for key in dificulties_dict :
    print("Na dificuldade %d tem %d problemas!" % (key, len(dificulties_dict[key])))

print("Fetching problems not aced by any user...")
taken = set()
for dif in dif_list :
    while(True):
        if dif not in dificulties_dict :
            print("alguma das dificuldades nao tem nenhum problema nela! encerrando!")
            exit(0)
        ind = random.randint(0, len(dificulties_dict[dif]) - 1)

        if dificulties_dict[dif][ind] not in taken and dificulties_dict[dif][ind] not in ACed_problems:
            taken.add(dificulties_dict[dif][ind])
            break
print("Results!")
for problem in taken :
    print(problem)