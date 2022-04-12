import os
import requests
import json
import urllib
import base64
from requests_ntlm import HttpNtlmAuth
from requests_negotiate_sspi import HttpNegotiateAuth
import pandas as pd

###########################################################################
########################## Pandas Settings ################################
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth',None)
###########################################################################


class ssrs():
    '''
    def __init__(self,Org,Orgid,User,Job_ID):
        self.org                = Org
        self.orgid              = Orgid
        self.User               = User
        self.Job                = Job_ID
        self.verifcationErrors  = []
        '''

    def __init__(self,Org,user=None,pwd=None):
        self.org                = Org
        self.user               = user
        self.pwd                = pwd
        self.verifcationErrors  = []

    @property
    def authorize(self):
        if self.user==None:
            domain = os.environ['userdomain']
            user = os.environ['USERNAME']
            self.user = f'{domain}\\{user}'

        try:
            auth = HttpNtlmAuth(self.user, self.pwd)
            return auth
        except Exception as e:
            return e

    @property
    def catalog(self):

        try:
            self.url                = f"http://{self.org}/reports/api/v2.0/CatalogItems"
            self.header             =  {'Content-Type': 'application/json','Accept': 'application/json'}
            self.response           = requests.request("GET", self.url, headers=self.header, auth=self.authorize)
            self.content            = self.response.content
            self.json               = json.dumps(self.response.json()['value'], indent = 4)
            return  self.json
        except Exception as e:
            return 'Failed: '+str(e)

    @property
    def subscriptions(self):

        try:
            self.url                = f"http://{self.org}/reports/api/v2.0/Subscriptions"
            self.header             =  {'Content-Type': 'application/json','Accept': 'application/json'}
            self.response           = requests.request("GET", self.url, headers=self.header, auth=self.authorize)
            self.content            = self.response.content
            self.json               = json.dumps(self.response.json(), indent = 4)
            return  self.json
        except Exception as e:
            return 'Failed: '+str(e)

    @property
    def reports(self):

        try:
            self.url = f"http://{self.org}/reports/api/v2.0/Reports"
            self.header = {'Content-Type': 'application/json', 'Accept': 'application/json'}
            self.response = requests.request("GET", self.url, headers=self.header, auth=self.authorize)
            self.content = self.response.content
            self.json = json.dumps(self.response.json()['value'], indent=4)
            return self.json
        except Exception as e:
            return 'Failed: ' + str(e)

    @property
    def folders(self):

        try:
            self.url = f"http://{self.org}/reports/api/v2.0/Folders"
            self.header = {'Content-Type': 'application/json', 'Accept': 'application/json'}
            self.response = requests.request("GET", self.url, headers=self.header, auth=self.authorize)
            self.content = self.response.content
            self.json = json.dumps(self.response.json()['value'], indent=4)
            return self.json
        except Exception as e:
            return 'Failed: ' + str(e)

    def download_item(self,path):
        self.path = path
        try:
            self.url                = f"http://{self.org}/reports/api/v2.0/CatalogItems(Path='{self.path}')/Content/$value"
            self.header             =  {'Content-Type': 'application/json','Accept': 'application/json'}
            self.response           = requests.request("GET", self.url, headers=self.header, data=self.payload,auth=self.authorize)
            #sessionid = self.sessionid
            return self.sessionid
        except Exception as e:
            return ' Failed: '+str(e)

    def upload_item(self,path):
        self.path = open(path,'rb').read()
        try:
            self.url                =  f"http://{self.org}/reports/api/v2.0/CatalogItems"
            self.payload            =  json.dumps({"@odata.type" : "image","Content" :base64.b64encode(self.path), "ContentType":"","Name" : 'test',"Path" : '/test'})
            self.header             =  {'Content-Type': 'application/json','Accept': 'application/json'}
            self.response           =  requests.request("GET", self.url, headers=self.header, data=self.payload,auth=self.authorize)
            #sessionid = self.sessionid
            return self.sessionid
        except Exception as e:
            return ' Failed: '+str(e)

    def delete_item(self,path):
        self.path = path
        try:
            self.url                = f"http://{self.org}/reports/api/v2.0/CatalogItems(Path='{self.path}')"
            #self.payload            = '{}'
            self.header             =  {'Content-Type': 'application/json','Accept': 'application/json'}
            self.response           = requests.request("DELETE", self.url, headers=self.header, data=self.payload)
            #sessionid = self.sessionid
            return self.sessionid
        except Exception as e:
            return ' Failed: '+str(e)

    def report_catalog(self,id):
        self.id = id
        try:
            self.url                = f"http://{self.org}/reports/api/v2.0/Reports({self.id})"
            self.header             = {'Content-Type': 'application/json','Accept': 'application/json'}
            self.response           = requests.request("GET", self.url, headers=self.header, auth=self.authorize)
            self.content            = self.response.content
            self.json               = json.dumps(self.response.json(), indent = 4)
            return  self.json
        except Exception as e:
            return 'Failed: '+str(e)

    @property
    def resources(self):
        self.id = id
        try:
            self.url                = f"http://{self.org}/reports/api/v2.0/Resources"
            self.header             = {'Content-Type': 'application/json','Accept': 'application/json'}
            self.response           = requests.request("GET", self.url, headers=self.header, auth=self.authorize)
            self.content            = self.response.content
            self.json               = json.dumps(self.response.json(), indent = 4)
            return  self.json
        except Exception as e:
            return 'Failed: '+str(e)


    def download_report(self,id):
        self.id = id
        try:
            self.url                = f"http://{self.org}/reports/api/v2.0/Reports({self.id})/Content/$value"
            self.header             = {'Accept': 'application/octet-stream'}
            self.response           = requests.request("GET", self.url, headers=self.header, auth=self.authorize)
            self.content            =self.response.content
            return self.content
        except Exception as e:
            return 'Failed: '+str(e)

pwd  = base64.b64decode(pwd).decode("utf-8")
user = base64.b64decode(user).decode("utf-8")



var = ssrs(Org='', pwd = pwd).reports
df= pd.read_json(var)
df =df[['Id','Name','Path']]
df['Download'] = df.apply(lambda x: open(fr"C:\Users\SHansen\test\{x['Path']}\{x['Name']}.rdl", 'wb').write(ssrs(Org='', pwd = pwd).download_report(id =x['Id'])),axis =1 )
print(df)
