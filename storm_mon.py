#!/usr/bin/env python
import sys
import urllib2
import json


def api_get(url, dict_name):
    resp = urllib2.urlopen(url)
    if dict_name:
        return json.loads(resp.read())[dict_name]
    else:
        return json.loads(resp.read())


def topos_lld(ip, dict_name):
    url = 'http://{0}:9988/api/v1/topology/summary'.format(ip)
    ring = api_get(url, dict_name)
    topos = []
    for topo in ring:
        topo_id = topo.get("id")
        topos.append(topo_id)
    data = [{"{#TOPO}": topo} for topo in topos]
    print(json.dumps({"data": data}, indent=4))


def get_topo_errors_count(ip, topo_id):
    url = 'http://{0}:9988/api/v1/topology/{1}'.format(ip, topo_id)
    topo_info = api_get(url, dict_name=False)
    failed = topo_info['topologyStats'][0]['failed']
    if failed:
        print(failed)
    else:
        print(0)


if __name__ == "__main__":
    ip = '127.0.0.1'
    if sys.argv[1] == "count_super":
        url = 'http://{0}:9988/api/v1/supervisor/summary'.format(ip)
        print len(api_get(url, 'supervisors'))
    elif sys.argv[1] == "count_topos":
        url = 'http://{0}:9988/api/v1/topology/summary'.format(ip)
        print len(api_get(url, 'topologies'))
    elif sys.argv[1] == "topos_lld":
        topos_lld(ip, 'topologies')
    elif sys.argv[1] == "topo_errors":
        topo_id = sys.argv[2]
        get_topo_errors_count(ip, topo_id)
    else:
        print(-1)
        exit(-1)
    exit(0)

    get_topo_errors_count('176.9.154.104','TrackingTopology-3-1485163256')
    exit(0)
# sys.argv:
# count_super
# count_topos
# topos_lld
# topo_errors

    ips = ['176.9.154.104', '5.9.84.69', '176.9.158.26', '5.9.25.22']
    dict_name = "topologies"
    for ip in ips:
        topos_lld(ip, dict_name)

    '''
    #    if sys.argv[1] == "supervisors_number":
        print len(api_get('http://176.9.158.26:9988/api/v1/supervisor/summary', 'supervisors'))
#    if sys.argv[1] == "topologies_number"
# stage cluster
        stage = api_get('http://5.9.25.22:9988/api/v1/topology/summary', 'topologies')
        print len(stage)
# prod big cluster
        prod_big = api_get('http://176.9.158.26:9988/api/v1/topology/summary', 'topologies')
        print len(prod_big)
# prod small cluster
        prod_small = api_get('http://5.9.84.69:9988/api/v1/topology/summary', 'topologies')
        print len(prod_small)
# prod new cluster
        prod_new = api_get('http://176.9.154.104:9988/api/v1/topology/summary', 'topologies')
        print len(prod_new)

# stage topologies ids
        print json.dumps(stage, indent=4)

        for topo in stage:
            print topo.get("id")
    '''
