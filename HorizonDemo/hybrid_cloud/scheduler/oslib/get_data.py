import base64,urllib,httplib,json,os

from urlparse import urlparse

def get_data(url1):
	
	#url1 = "192.168.222.10:5000"
	#url1 = "192.168.1.123:5000"
	params1 = '{"auth": {"tenantName": "admin","passwordCredentials":{"username": "admin", "password": "admin"}}}'
	headers1 = {"Content-Type": 'application/json'}
	conn1 = httplib.HTTPConnection(url1)
	conn1.request("POST","/v2.0/tokens",params1,headers1)
	response1 = conn1.getresponse()
	data1 = response1.read()
	dd1 = json.loads(data1)
	conn1.close()

	apitoken = dd1['access']['token']['id']
	apitenant= dd1['access']['token']['tenant']['id']
	apiurl = dd1['access']['serviceCatalog'][0]['endpoints'][0]['publicURL']
	apiurlt = urlparse(dd1['access']['serviceCatalog'][0]['endpoints'][0]['publicURL'])
	url2 = apiurlt[1]

	params2 = ''
	headers2 = { "X-Auth-Token":apitoken, "Content-type":"application/json" } 
	request = "/v2/"+apitenant+"/os-hypervisors/detail"
	conn2 =  httplib.HTTPConnection(url2)
	conn2.request("GET", request, params2, headers2)
	response2 = conn2.getresponse()
	data2 = response2.read()
	data2 = json.loads(data2)
	conn2.close()

	#print data2
	return data2

def get_total_ram_mb(data):
	total = 0
	for i in data['hypervisors']:
		total = total + i['free_ram_mb']
	return total

def get_total_cpu(data):
	total1 = 0
	total2 = 0
	for i in data['hypervisors']:
		total1 = total1 + i['vcpus']
		total2 = total2 + i['vcpus_used']
	return total1-total2

def get_total_disk_gb(data):
	total = 0
	for i in data['hypervisors']:
		total = total + i['free_disk_gb']
	return total

def get_host_info(data):
	host_list = []
	for i in data['hypervisors']:
		name = i['service']['host']
		cpu = i['vcpus']-i['vcpus_used']
		ram_mb = i['free_ram_mb']
		disk_gb = i['free_disk_gb']
		host_list.append({'name':name,'cpu':cpu,'ram_mb':ram_mb,'disk_gb':disk_gb})
	return host_list
	
if  __name__=='__main__' :
	data = get_data('192.168.1.123:5000')
	print get_total_ram_mb(data)
	print get_total_cpu(data)
	print get_total_disk_gb(data)
	print get_host_info(data)
