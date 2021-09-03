"""
import all the reqiured librariers
"""
import requests
import json
from itertools import zip_longest
import difflib
import sys
import os
import time
import logging
import re
from tabulate import tabulate
import yaml
import json
from smtplib import SMTP
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pretty_html_table import build_table
from datetime import datetime, timedelta
import urllib.parse




from auth_header import Authentication as auth
from operations import Operation 





def url(vmanage_host,vmanage_port,api):
    """ return the URL for the privide API ENDpoint """
    """ function to get the url provide api endpoint """
    
    return f"https://{vmanage_host}:{vmanage_port}{api}"



def post_events(header, data):
    """ return the sla events """
    """  function to get the SLA events from the vmanage """
   

    api_events = '/dataservice/event'
    url_events = url(vmanage_host,vmanage_port,api_events)
    events = Operation.post_method(url_events, header, data)

    return events['data']

def send_email(sender_email, mail_passwd, receiver_email, body):
    
    """ return if email is sent successful or not"""
    """ function to sent email """

    
    message = MIMEMultipart()
    message['Subject'] = "SLA EVENTS"

    body_content = body
    message.attach(MIMEText(body_content, "html"))
    msg_body = message.as_string()

    server = SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, mail_passwd)
    try:
        server.sendmail(sender_email, receiver_email, msg_body)
        return ('email sent')
    except:
        return ('error sending mail')

    server.quit()




if __name__=='__main__':

    while True:

        """ open the yaml file where the constant data is stored"""

        with open("vmanage_login.yaml") as f:
            config = yaml.safe_load(f.read())
        
        
        """ extracting info from Yaml file"""

        vmanage_host = config['vmanage_host']
        vmanage_port = config['vmanage_port']
        username = config['vmanage_username']
        password = config['vmanage_password']

        time_delta = config['time_delta']


        """ get current time and data and use time_delta to subract the time by delta minutes """
        date_time = datetime.utcnow()
        end_time = date_time.strftime("%Y-%m-%dT%H:%M:%S UTC")
        delta = date_time - timedelta( minutes = time_delta)
        start_time = delta.strftime("%Y-%m-%dT%H:%M:%S UTC")


        """ Creted dataset"""
        sla_event_dataset = {"event-time":[],"host-name":[],"local-system-ip":[], "remote-system-ip":[], "local-color":[], "remote-color":[], "src-ip":[], "dst-ip":[], "src-port":[], "dst-port":[], "sla-classes":[], "old-sla-classes":[]}


    
        """  Calling the header function from Auth to get 
                'Content-Type': "application/json", 
                'Accept': '*/*', 'Cookie': session_id, 
                'X-XSRF-TOKEN': token_id}  """
        
        header = auth.get_header(vmanage_host, vmanage_port,username, password)



        """ Creating the request payload 
            since nested dict is not execpt in requests we used a str """
        data= '{\"query\":{\"condition\":\"AND\",\"rules\":[{\"value\":[\"'+start_time+'\",\"'+end_time+'\"],\"field\":\"entry_time\",\"type\":\"date\",\"operator\":\"between\"}]}}'



        """ Caling the API ('/dataservice/event') call with POST request """
        event_data = post_events(header, data)

        sla_list_count= 0

        
        """ parsing the returned data """
        for sla_event_data in event_data:
            if sla_event_data['eventname'] == 'sla-change':
                sla_list_count += 1
                sla_event_details = re.split('\=|;',sla_event_data['details'])


                sla_event_dataset["event-time"].append(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(sla_event_data['entry_time']//1000)))
                sla_event_dataset["host-name"].append(sla_event_details[1])
                sla_event_dataset["local-system-ip"].append(sla_event_details[13])
                sla_event_dataset["remote-system-ip"].append(sla_event_details[17])
                sla_event_dataset["local-color"].append(sla_event_details[15])
                sla_event_dataset["remote-color"].append(sla_event_details[19])
                sla_event_dataset["src-ip"].append(sla_event_details[3])
                sla_event_dataset["dst-ip"].append(sla_event_details[5])
                sla_event_dataset["src-port"].append(sla_event_details[9])
                sla_event_dataset["dst-port"].append(sla_event_details[11])
                sla_event_dataset["sla-classes"].append(sla_event_details[21])
                sla_event_dataset["old-sla-classes"].append(sla_event_details[23])

        
        """ Converting Dataset to Dataframe using pandas"""
        sla_event_dataframe = pd.DataFrame(sla_event_dataset)


        """ Convert pandas dataframe to HTML table """
        """ https://pypi.org/project/pretty-html-table/ """
        body = build_table(sla_event_dataframe, 'red_dark')
        

        """ extracting info from Yaml file"""
        sender_email = config['sender_email']
        receiver_email = config['receiver_email']
        mail_password = config['mail_password']

        """ call send_email """
        if sla_list_count >= 1:
            print(send_email(sender_email, mail_password, receiver_email, body))

        time.sleep(180)
