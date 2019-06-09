import requests
import json
import random
 
url = "http://codeforces.com/api/problemset.problems"
contents = requests.get(url).json()
prob_list = list(filter(lambda d : 'rating' in d, contents['result']['problems']))

print("Por favor digite quantos problemas você quer no mashup, \n dê enter, depois entre um número de dificuldades igual ao número de problemas.")
num_problems = int(input())
dif_list = map(int, input().split())

dificulties_dict = {}
for prob in prob_list:
    rat = int(prob['rating'])
    if rat in dificulties_dict :
        dificulties_dict[rat].append(str(prob['contestId']) + prob['index'])
    else : 
        dificulties_dict[rat] = [str(prob['contestId']) + prob['index']]

for key in dificulties_dict :
    print("Na dificuldade %d tem %d problemas!" % (key, len(dificulties_dict[key])))

taken = set()
for dif in dif_list :
    while(True):
        try : 
            ind = random.randint(0, len(dificulties_dict[dif]) - 1)
        except :
            print("alguma das dificuldades nao tem nenhum problema nela! encerrando!")
            exit(0)
        if dificulties_dict[dif][ind] not in taken :
            taken.add(dificulties_dict[dif][ind])
            break

for problem in taken :
    print(problem)