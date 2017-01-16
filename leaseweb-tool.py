#!/usr/bin/env python
import sys
import urllib2
import json
import os


def get_ip(server_id):
# Get default IP addess for the server
    url = 'https://api.leaseweb.com/v1/bareMetals/' + server_id + '/ips'
    req = urllib2.Request(url, headers=headers)
    response = urllib2.urlopen(req)
    raw_ips = json.loads(response.read())
    for i in  raw_ips.get('ips'):
        if i.get('ip').get("isPrimary") == True:
            return i.get('ip').get("ip")


def gen_ids():
# Get ServerID from all Bare Metal servers list
    req = urllib2.Request('https://api.leaseweb.com/v1/bareMetals', headers=headers)
    response = urllib2.urlopen(req)
    my_dict = {}
    raw_data = json.loads(response.read())
    for i in raw_data.get("bareMetals"):
	for k, v in i.items():
	    my_dict[v.get("serverName")] = v.get("bareMetalId")
    return my_dict


def get_password(server_id):
# Get root password for the server
    url = 'https://api.leaseweb.com/v1/bareMetals/' + server_id + '/rootPassword'
    req = urllib2.Request(url, headers=headers)
    response = urllib2.urlopen(req)
    parsed = json.loads(response.read())
    return parsed.get("rootPassword")


def gen_ids_json():
    new_data = json.dumps(gen_ids())
    with open('ids.json', 'w') as outfile:
        json.dump(new_data, outfile)


if __name__ == "__main__" :
    if sys.argv[1] == "eu":
        headers = { 'x-lsw-auth': "XXX", 'Accept': "application/json" }
    elif sys.argv[1] == "us":
        headers = { 'x-lsw-auth': "YYY", 'Accept': "application/json" }
    else:
        print "Please specify LW region"
        exit(1)

    bm_server = sys.argv[2].split(",")

    if sys.argv[2] == "generate":
        gen_ids_json()
        exit(0)

    if not os.path.exists('ids.json'):
        gen_ids_json()

    with open('ids.json') as ids:
        raw_data = json.load(ids)
        data = json.loads(raw_data)

    for i in bm_server:
        server_id = data.get(i)
        srv_ip = get_ip(server_id)
        srv_pass = get_password(server_id)
        command = 'echo "' + srv_ip + ' ' + i + '" >> /etc/hosts; \
            ssh-keyscan ' + srv_ip + ' >> ~/.ssh/known_hosts; \
            ssh-keyscan ' + i + ' >> ~/.ssh/known_hosts; \
            sshpass -p' + srv_pass + ' ssh-copy-id ' + srv_ip
        print command
#        os.system(command)
