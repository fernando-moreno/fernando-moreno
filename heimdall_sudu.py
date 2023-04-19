from __future__ import print_function
import ftplib
from importlib.metadata import files
from traceback import print_tb
from unicodedata import name
import os

#credentials

HOSTNAME ="ftp2-dhllink-qa.dhl.com"
USER = "ford_asn_mx_tst"
PASSWORD = "COaNOnlAXIg_n0tx"

#connect to server

ftp_server = ftplib.FTP(HOSTNAME, USER, PASSWORD)
ftp_server.encoding = "utf-8"


#change to Maersk directory
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
  exit()
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

print ("I have finished Fer, until the next one.")
