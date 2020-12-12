import pickle
import os.path
from apiclient import errors
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.errors import Error
import re

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']


def search_message(service, user_id, search_string):

    try:
        # initiate the list for returning
        list_ids = []

        # get the id of all messages that are in the search string
        search_ids = service.users().messages().list(userId=user_id, q=search_string).execute()
        
        # if there were no results, print warning and return empty string
        try:
            ids = search_ids['messages']

        except KeyError:
            #print("WARNING: the search queried returned 0 results")
            #print("returning an empty string")
            return ""

        if len(ids)>1:
            for msg_id in ids:
                list_ids.append(msg_id['id'])
            return(list_ids)

        else:
            list_ids.append(ids[0]['id'])
            return list_ids
        
    except (errors.HttpError):
        print("An error occured:")

def get_message(service, user_id, msg_id):
    message = service.users().messages().get(userId=user_id, id=msg_id).execute()
    service.users().messages().modify(userId=user_id, id=msg_id, body={'removeLabelIds': ['UNREAD']}).execute()
    return message

def extractor(snip):
    re1=re.compile(r'(?<=Received\sfrom\s)(.+)(?=\sTxn.\sID)')
    re2=re.compile(r'(?<=Message\s:\s)(.+)')
    match=re.search(re1,snip).group(0).split(' ₹ ')
    data={'name':match[0],'amount':match[1]}
    match=re.search(re2,snip).group(0)
    data['message']=match
    return data

def readAll(srv):
    search_str='from:noreply@phonepe.com is:unread'
    msgids=search_message(srv,'me',search_str)
    if len(msgids):
        for ids in msgids:
            srv.users().messages().modify(userId='me', id=ids, body={'removeLabelIds': ['UNREAD']}).execute()


