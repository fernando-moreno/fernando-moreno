from __future__ import print_function
import ftplib
from importlib.metadata import files
from traceback import print_tb
from unicodedata import name
import time
import json
import os
import requests
import shutil

#credentials

HOSTNAME ="ftp2-dhllink-qa.dhl.com"
USER = "ford_asn_mx_tst"
PASSWORD = "COaNOnlAXIg_n0tx"

#connect to server

ftp_server = ftplib.FTP(HOSTNAME, USER, PASSWORD)
ftp_server.encoding = "utf-8"


#change to Maersk directory
ftp_server.cwd("maeu")


list_of_files = []

ftp_server.retrlines('MLSD', list_of_files.append)

files_download = []
for file in list_of_files[2:]:
  bridge = file.split(";")
  bridge = bridge[8].strip()
  files_download.append(bridge)
  
print (len(files_download))

files_len = len(files_download)

if files_len < 1:
  print ("There are no files to download, try again later Fer.")

else:
  for ccp in files_download:
    try:
      local_filename = os.path.join('MAEU\\', ccp)
      with open (local_filename, 'wb') as file:
        ftp_server.retrbinary(f"RETR {ccp}", file.write)
        print("Successfully downloaded file, I will delete it for you :) " + " " + ccp)
        ftp_server.delete(ccp)
    except:
      print("An exception occurred")


ftp_server.quit()

print ("I have finished with Maersk files, let me fetch Hamburg sud...")


# #credentials

HOSTNAME ="ftp2-dhllink-qa.dhl.com"
USER = "ford_asn_mx_tst"
PASSWORD = "COaNOnlAXIg_n0tx"

#connect to server

ftp_server = ftplib.FTP(HOSTNAME, USER, PASSWORD)
ftp_server.encoding = "utf-8"

## Set API Server

# server = 'http://127.0.0.1:8000'
server = 'https://serviciosmaa.azurewebsites.net/'

#change to HSUD directory
ftp_server.cwd("sudu")


list_of_files = []

ftp_server.retrlines('MLSD', list_of_files.append)

files_download = []
for file in list_of_files[2:]:
  bridge = file.split(";")
  bridge = bridge[8].strip()
  files_download.append(bridge)
  
print (len(files_download))

files_len = len(files_download)

if files_len < 1:
  print ("There are no files to download, try again later Fer.")

else:
  for ccp in files_download:
    try:
      local_filename = os.path.join('SUDU\\', ccp)
      with open (local_filename, 'wb') as file:
        ftp_server.retrbinary(f"RETR {ccp}", file.write)
        print("Successfully downloaded file, I will delete it for you :) " + " " + ccp)
        ftp_server.delete(ccp)
    except:
      print("An exception occurred")


ftp_server.quit()

print ("I have finished HSUD, let's call  the APIs.")




login = requests.post('https://serviciosmaa.azurewebsites.net/api/login', data={'email': 'lfernando.moreno@gmail.com', 'password':'123456789'})

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
        ford_ccp = requests.post('https://serviciosmaa.azurewebsites.net/api/ford/create', headers=headers, json=ford_call)
        print(filename + " " +  ford_call['TrasladoMercancias']['FordSourceSystem'] + " " +  ford_call['TrasladoMercancias']['Contenedor']['GuiadeCarga'] + " API Response is " + str(ford_ccp.json()))
        processed += 1
        time.sleep(1)

for filename in os.listdir(directory):
  path = os.path.join(directory, filename)
  destination = r'C:\Users\LFM007\OneDrive - Maersk Group\Projects\Carta Porte\Ford\CCP_Heimdall\MAEU_bkp\\'
  shutil.move(path, destination+filename)



print ("I have finished Fer with MAEU and processed: " + str(processed) + " files " + "Out of " + str(many_file))





login = requests.post('https://serviciosmaa.azurewebsites.net/api/login', data={'email': 'lfernando.moreno@gmail.com', 'password':'123456789'})

token  = login.json() 

print(token["access_token"])

# open JSON and make HTTP Request

directory = 'SUDU'

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
    else:
        #call api and send request

        headers = {"Authorization": "Bearer"+" "+token["access_token"], 'Accept': 'application/json'}
        ford_ccp = requests.post('https://serviciosmaa.azurewebsites.net/api/ford/create', headers=headers, json=ford_call)
        print(filename + " " +  ford_call['TrasladoMercancias']['FordSourceSystem'] + " " +  ford_call['TrasladoMercancias']['Contenedor']['GuiadeCarga'] + " API Response is " + str(ford_ccp.json()))
        processed += 1
        time.sleep(1)

for filename in os.listdir(directory):
  path = os.path.join(directory, filename)
  destination = r'C:\Users\LFM007\OneDrive - Maersk Group\Projects\Carta Porte\Ford\CCP_Heimdall\SUDU_ Bkp\\'
  shutil.move(path, destination+filename)



print ("I have finished Fer with HSUD  and processed: " + str(processed) + " files " + "Out of " + str(many_file))
