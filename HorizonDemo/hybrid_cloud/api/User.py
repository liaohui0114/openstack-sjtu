
####defalut setting
AUTHURL = {
    'cloud1':"http://192.168.1.123:5000/v2.0",
    'cloud2':"http://192.168.1.125:5000/v2.0"
}
USER = "admin"
PASSWD = "admin"
TENANT="demo"

##to get nova credentials
def get_nova_credentials(url):
    #print("http://"+url+"/v2.0");
    d = {}
    d['username'] = USER
    d['api_key'] = PASSWD
    d['auth_url'] = url
    d['project_id'] = TENANT
    return d

