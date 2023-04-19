import requests
import json
import os
import time



login = requests.post('http://127.0.0.1:8000/api/login', data={'email': 'lfernando.moreno@gmail.com', 'password':'123456789'})

token  = login.json() 

print(token["access_token"])

# open JSON and make HTTP Request

directory = 'MAEU'

many_file = len(os.listdir(directory))
processed = 0

for filename in os.listdir(directory):
    path = os.path.join(directory, filename)
    with open(path) as payload:
        ford_call = json.loads(payload.read())

    #validate schema


    # print("TrasladoMercancias" in ford_call)

    if "TrasladoMercancias" in ford_call == "False":
        print ("The schema is not compliant, I will ignore it.")
    elif "GuiadeCarga" in ford_call['TrasladoMercancias']  == "False":
        print("I cannot process because it has no guía de carga")
    elif "FordSourceSystem" in ford_call['TrasladoMercancias']['FordSourceSystem'] == "CMMS":
        print("I cannot process because CMMS has no BL")
    else:
        #call api and send request

        headers = {"Authorization": "Bearer"+" "+token["access_token"], 'Accept': 'application/json'}
        ford_ccp = requests.post('http://127.0.0.1:8000/api/ford/create', headers=headers, json=ford_call)
        print(filename + " " +  ford_call['TrasladoMercancias']['FordSourceSystem'] + " " +  ford_call['TrasladoMercancias']['Contenedor']['GuiadeCarga'] + " API Response is " + str(ford_ccp.json()))
        processed += 1
        time.sleep(1)





print ("I have finished Fer and processed: " + str(processed) + " files " + "Out of " + str(many_file))



