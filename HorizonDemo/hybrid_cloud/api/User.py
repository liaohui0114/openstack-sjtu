
####defalut setting
AUTHURL = "http://192.168.1.164:5000/v2.0"
USER = "admin"
PASSWD = "1"
TENANT="demo"

##to get nova credentials
def get_nova_credentials(url=AUTHURL):
    d = {}
    d['username'] = USER
    d['api_key'] = PASSWD
    d['auth_url'] = AUTHURL
    d['project_id'] = TENANT
    d['auth_url'] = url
    return d

