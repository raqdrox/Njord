import NjordMailHandler as mail_hldr
import NjordStreamLabHandler as strlb_hldr
import os
import pickle
from apiclient import errors
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.errors import Error
import time
import requests
#------------globals---------
itertracker=0
strlabToken=''
donationCount=0
#----------------------------
def donationCheck(srv): #check Gmail API for Mail Updates
    search_str='from:noreply@phonepe.com is:unread'
    msgids=mail_hldr.search_message(srv,'me',search_str)
    if len(msgids):
        maiList=[]
        for ids in msgids:
            mailhtml=mail_hldr.get_message(srv, 'me', ids)
            data=mail_hldr.extractor(str(mailhtml['snippet']))
            maiList.append(data)
        return maiList
    else:
        print('No Donations')
        return []    

def strLabPut(donation): #send donation data to Streamlabs
    global strlabToken,donationCount
    strlb_hldr.postDonations(donation,strlabToken)
    donationCount+=1

def isconnected():
    while True:
        try:
            requests.get('https://www.google.com/').status_code
            break
        except:
            print("NOT CONNECTED...RETRYING...")

def startProcessGmail(): #Returns Gmail Service Object
    creds = None
    service = None

    if os.path.exists('./tokens/token.pickle'):
        with open('./tokens/token.pickle', 'rb') as token:
            creds = pickle.load(token)
        
        service = build('gmail', 'v1', credentials=creds)
        
    return service

def updateLoop(gmailSrv):   #mainloop
    global itertracker,strlabToken,donationCount
    while True:
        isconnected()
        donList=donationCheck(gmailSrv)
        for donation in donList:
            strLabPut(donation)
            print(f'Donation {donationCount} :\n{donation}')
            time.sleep(2)
        time.sleep(10)
        itertracker+=1
        if itertracker==60:
            strlabToken=strlb_hldr.refreshTokens()
            pass

def main():
    global strlabToken
    gmailSrv=startProcessGmail()
    strlabToken=strlb_hldr.refreshTokens()
    mail_hldr.readAll(gmailSrv)
    updateLoop(gmailSrv)

if __name__ == '__main__':
    main()