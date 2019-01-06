from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from datetime import datetime, timedelta

import base64
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mimetypes
import os

from apiclient import errors
from django.http import HttpRequest, HttpResponse
import jwt
from functools import wraps
import json
import psycopg2
from psycopg2.extras import RealDictCursor
from functools import wraps
from django.http import HttpResponseRedirect

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
jwt_token = 'token' # fake token
new_token = 'zzz'
import requests
import json

#select * from AspnetUsers;

#con = psycopg2.connect(dbname='LeadPolice', user='postgres', host='50.63.167.106', password='Modinagar@7')
con=''
def open():
    global con
    #cur = con.cursor()
    con = psycopg2.connect(dbname='touristshop', user='postgres', host='localhost', password='Bismillah@123')
    cur = con.cursor(cursor_factory=RealDictCursor)
    return cur


def close(cur):
    global con
    con.commit()
    cur.close()
    con.close()
    return True

JWT_SECRET = 'secretfudtr'
JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_SECONDS = 20


def create_token(user_name,company_id,role_id):
    global jwt_token
    payload = {
        "user": user_name,
        "comapnyid": company_id,
        "roleid": role_id,
        "exp": datetime.utcnow() + timedelta(seconds=900)
        }
    jwt_token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)
    return jwt_token.decode('utf-8')


# def decorator(function):
#     @wraps(function)
#     def wrap(request):
#         print(request.META)
#         content = request.META['HTTP_AUTHORIZATION'].split()
#         token = content[1]
#         print(token)
#         data = jwt.decode(token, JWT_SECRET)
#         return function(request, *args, **kwargs)
#     return wrap

def Auth(request, *args, **kwargs):
    content =request.META['HTTP_AUTHORIZATION']
    #print(request.META)
    # h = json.dumps(content['HTTP_AUTHORIZATION'])
    # print(content)
    # print(type(content))
    sp=list(content.split(" "))
    token=(sp[1])
    #print(type(sp))
    data = jwt.decode(token,JWT_SECRET )
    #print (data)
    return True

def other_leads_company_id(company_id):
    queryset = "Select u.Id as  Id,(u.FirstName || ' ' || u.LastName) as username,li.BuilderInterest,li.cmpctlabel," \
               "l.companyid,l.CreateDateTimeOffset,l.createuserid,l.EditDateTimeOffset,l.EditUser_ID,l.Email,l.leadid," \
               "l.name,l.phonenumber,li.ProjName,li.QueryRemarks,li.RangeFrom,li.RangeTo,li.receivedon,l.Status, li.StatusDate," \
               "li.statusid,li.TypeOfProperty,li.assignedto,li.LeadItemId from Leads l join LeadItems li on " \
               "li.leadid = l.leadid join AspNetUsers u on u.Id::varchar = li.assignedto where l.companyid = {} " \
               "and li.statusid =1".format(company_id)
    cursor = open()
    cursor.execute(queryset)
    records = cursor.fetchall()
    r = json.dumps(records, indent=4, sort_keys=True, default=str)
    loaded_r = json.loads(r)
    result = get_other_leads(loaded_r)
    return result

def get_other_leads(leads):
    #print(leads)
    new_grouped_assignment_3 = dict()
    for row in leads:
        if row['leadid'] not in new_grouped_assignment_3:
            new_grouped_assignment_3[row['leadid']] = [{'leadid': row['leadid'],
                                                         'queryremarks': row['queryremarks'],
                                                         'typeofproperty': row['typeofproperty'],
                                                         #'status': row['status'],
                                                         'rangefrom': row['rangefrom'],
                                                         'rangeto': row['rangeto'],
                                                         'cmpctlabel': row['cmpctlabel'],
                                                         'receivedon': row['receivedon'],
                                                         'projname': row['projname'],
                                                         'assignedto': row['assignedto'],
                                                         'statusid': row['statusid'],
                                                         'statusdate': row['statusdate'],
                                                         'leaditemid': row['leaditemid'],
                                                         }]
        else:
            new_grouped_assignment_3[row['leadid']] += [{'leadid': row['leadid'],
                                                          'queryremarks': row['queryremarks'],
                                                          'typeofproperty': row['typeofproperty'],
                                                          #'status': row['statusid'],
                                                          'rangefrom': row['rangefrom'],
                                                          'rangeto': row['rangeto'],
                                                          'cmpctlabel': row['cmpctlabel'],
                                                          'receivedon': row['receivedon'],
                                                          'projname': row['projname'],
                                                          'assignedto': row['assignedto'],
                                                          'statusid': row['statusid'],
                                                          'statusdate': row['statusdate'],
                                                          'leaditemid': row['leaditemid']
                                                          }]
    l = []
    # print(new_grouped_assignment_3)
    for a in new_grouped_assignment_3:
        # print(a)
        l.append(a)
        # new_ld = dict()

    # print(new_grouped_assignment_3[l[0]])
    i = 0
    leadsss = list()
    while (i < len(l)):
        new_ld = dict()
        new_ld['leadid'] = l[i]
        new_ld['createuserid'] = row['createuserid']
        new_ld['createdatetimeoffset'] = row['createdatetimeoffset']
        new_ld['edituserid'] = row['edituserid']
        new_ld['editdatetimeoffset'] = row['editdatetimeoffset']
        new_ld['name'] = row['name']
        new_ld['email'] = row['email']
        new_ld['phonenumber'] = row['phonenumber']
        # new_ld['isassigned']=row['isassigned']
        new_ld['companyid'] = row['companyid']
        new_ld['cmpctlabel'] = row['cmpctlabel']
        new_ld['receivedon'] = row['receivedon']
        new_ld['statusid'] = row['statusid']
        new_ld['items'] = new_grouped_assignment_3[l[i]]
        leadsss.append(new_ld)
        i = i + 1
    return leadsss

def firebase_push_notification(token):
    headers = {"Content-type": "application/json",
               "Authorization": "key=AAAA3Mgl_0Y:APA91bFKigkhtGaXIKoGL60v8hTOT-a4u7OwZ_Y98jK8AlRcqQUcLjmtDHMCuY9i5am54h7XMQzgWSpQS5YusFJ5P5Nym2YqccghCf4EMeVtGcGemwKf_bOsXCqM86GK3r2hCSoDt3yAlp5v2UncAh6gQ1h3UF6YnA"}
    url = "https://fcm.googleapis.com/fcm/send"
    data = {
        "to": token,
        "notification": {
            "title": "success",
            "body": "hello ",
            "story_id": "story_12345"
        }
    }
    response = requests.post(url, data=json.dumps(data), headers=headers)
    response_body = response.json()
    #print(response_body)
    return response_body



class send_email:
    def __init__(self,service):
        self.service = service

    def SendMessage(self, user_id, message):

        try:
            message = (self.service.users().messages().send(userId=user_id, body=message).execute())
            print( 'Message Id: %s' % message['id'])
            return message
        except errors.HttpError as error:
            print('An error occurred: %s' % error)


    def CreateMessage(self,sender, to, subject, message_text):
        message = MIMEText(message_text)
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject
        return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

    def CreateMessageWithAttachment(self,sender, to, subject, message_text, file_dir,filename):

      message = MIMEMultipart()
      message['to'] = to
      message['from'] = sender
      message['subject'] = subject

      msg = MIMEText(message_text)
      message.attach(msg)

      path = os.path.join(file_dir, filename)
      content_type, encoding = mimetypes.guess_type(path)

      if content_type is None or encoding is not None:
        content_type = 'application/octet-stream'
      main_type, sub_type = content_type.split('/', 1)
      if main_type == 'text':
        fp = open(path, 'rb')
        msg = MIMEText(fp.read(), _subtype=sub_type)
        fp.close()
      elif main_type == 'image':
        fp = open(path, 'rb')
        msg = MIMEImage(fp.read(), _subtype=sub_type)
        fp.close()
      elif main_type == 'audio':
        fp = open(path, 'rb')
        msg = MIMEAudio(fp.read(), _subtype=sub_type)
        fp.close()
      else:
        fp = open(path, 'rb')
        msg = MIMEBase(main_type, sub_type)
        msg.set_payload(fp.read())
        fp.close()

      msg.add_header('Content-Disposition', 'attachment', filename=filename)
      message.attach(msg)

      return {'raw': base64.urlsafe_b64encode(message.as_bytes().decode())}
