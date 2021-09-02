import requests
import json
import urllib3
urllib3.disable_warnings()


class Authentication:

    @staticmethod
    def get_jsessionid(vmanage_host : str, vmanage_port : str,
                       username : str, password : str):
        api = "/j_security_check"
        base_url = "https://%s:%s"%(vmanage_host, vmanage_port)
        url = base_url + api
        payload = {'j_username' : username, 'j_password' : password}

        response = requests.post(url=url, data=payload, verify=False)
        try:
            cookies = response.headers["Set-Cookie"]
            jsessionid = cookies.split(";")
            return(jsessionid[0])
        except:
            print("No valid JSESSION ID returned\n")
            exit()

    @staticmethod
    def get_token(vmanage_host : str, vmanage_port : str ,
                  jsessionid : str):
        headers = {'Cookie': jsessionid}
        base_url = "https://%s:%s"%(vmanage_host, vmanage_port)
        api = "/dataservice/client/token"
        url = base_url + api      
        response = requests.get(url=url, headers=headers, verify=False)
        if response.status_code == 200:
            return(response.text)
        else:
            return None


    def get_header(vmanage_host : str, vmanage_port : str,
                       username : str, password : str):
        session_id  =  Authentication.get_jsessionid(vmanage_host, vmanage_port,
                       username , password)
        token_id     =  Authentication.get_token(vmanage_host, vmanage_port,
                       session_id)

        if token_id is not None:
            return {'Content-Type': "application/json", 'Accept': '*/*',
              'Cookie': session_id, 'X-XSRF-TOKEN': token_id}
        else:
            return {'Content-Type': "application/json",'Cookie': session_id}


      
        
        
