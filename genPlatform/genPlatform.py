import xml.etree.ElementTree as ET
import sys
import random
import math
from ElementTree_pretty import prettify

totalArgs = len(sys.argv)
cmdArgs = sys.argv

if (totalArgs < 3):
        print "Usage : python genPlatform.py p s d\n   p : 2^p gives the total number of clients.\n    s : the number of servers\n    d : the degree of inner nodes\n"
        sys.exit()

p = int(cmdArgs[1])
s = int(cmdArgs[2])
d = int(cmdArgs[3])

AS_prefix = "AS_"
exitAS_prefix = "exitAS_"
server_prefix = "Server_"
client_prefix = "Client_"
router_prefix = "R_"
central_router_prefix = "CenterRouter_"
gateway_router_prefix = "Gateway_"
link_prefix = "Link_"
server_link_prefix = "Serverlink_"
bb_link_prefix = "Backbone_"

power = "1000000000"
c_link_bw = "10000000"
c_link_lat = "5E-4"
s_link_bw = "1000000000"
s_link_lat = "5E-3"
bb_link_bw = "10000000000"
bb_link_lat = "0.1"

# Printing preamble
print "<?xml version='1.0'?>\n";
print "<!DOCTYPE platform SYSTEM \"http://simgrid.gforge.inria.fr/simgrid.dtd\">\n";

platform = ET.Element('platform')
platform.set('version', "3")

as_num = AS_prefix + "0"
Root_AS = ET.SubElement(platform, 'AS')
Root_AS.set('id', as_num)
Root_AS.set('routing', "Full")

def createAS(n, P):
    if n == 0:
	as_num_str = P.get('id')
	items = as_num_str.split('_')
	as_num = items[-1]
	central_router = ET.SubElement(P, 'router')
	central_router.set('id', central_router_prefix + as_num)
	gateway_router = ET.SubElement(P, 'router')
	gateway_router.set('id', gateway_router_prefix + as_num)
	for i in range(d):
		host = ET.SubElement(P, 'host')
		host.set('id', client_prefix + as_num + str(i))
		host.set('power', power)
	for i in range(d):
		link = ET.SubElement(P, 'link')
		link.set('id', link_prefix + as_num + str(i))
		link.set('bandwidth', c_link_bw)
		link.set('latency', c_link_lat)
	link = ET.SubElement(P, 'link')
	link.set('id', bb_link_prefix + as_num)
	link.set('bandwidth', bb_link_bw)
	link.set('latency', bb_link_lat)
	for i in range(d):
		route = ET.SubElement(P, 'route')
		route.set('src', central_router_prefix + as_num)
		route.set('dst', client_prefix + as_num + str(i))
		link_ctn = ET.SubElement(route, 'link_ctn')
		link_ctn.set('id', link_prefix + as_num + str(i))
	gateway_route = ET.SubElement(P, 'route')
	gateway_route.set('src', central_router_prefix + as_num)
	gateway_route.set('dst', gateway_router_prefix + as_num)
	gateway_route_link_ctn = ET.SubElement(gateway_route, 'link_ctn')
	gateway_route_link_ctn.set('id', bb_link_prefix + as_num)
    else:
	as_num_str = P.get('id')
	items = as_num_str.split('_')
	upper_as_num = items[-1]
        for i in range(d):
		as_num = upper_as_num + str(i)
		curAS = ET.SubElement(P, 'AS')
		curAS.set('id', AS_prefix + as_num)
		curAS.set('routing', "Dijsktra")
		createAS(n-1, curAS)
	central_router = ET.SubElement(P, 'router')
	central_router.set('id', central_router_prefix + upper_as_num)
	gateway_router = ET.SubElement(P, 'router')
	gateway_router.set('id', gateway_router_prefix + upper_as_num)
	host = ET.SubElement(P, 'host')
	host.set('id', server_prefix + upper_as_num)
	host.set('power', power)
	link = ET.SubElement(P, 'link')
	link.set('id', bb_link_prefix + upper_as_num)
	link.set('bandwidth', bb_link_bw)
	link.set('latency', bb_link_lat)
	link = ET.SubElement(P, 'link')
	link.set('id', server_link_prefix + upper_as_num)
	link.set('bandwidth', s_link_bw)
	link.set('latency', s_link_lat)
	for i in range(d):
		link = ET.SubElement(P, 'link')
		link.set('id', link_prefix + upper_as_num + str(i))
		link.set('bandwidth', bb_link_bw)
		link.set('latency', bb_link_lat)
	for i in range(d):
		route = ET.SubElement(P, 'ASroute')
		route.set('src', AS_prefix + upper_as_num)
		route.set('dst', AS_prefix + upper_as_num + str(i))
		route.set('gw_src', gateway_router_prefix + upper_as_num)
		route.set('gw_dst', gateway_router_prefix + upper_as_num + str(i))
		link_ctn = ET.SubElement(route, 'link_ctn')
		link_ctn.set('id', link_prefix + upper_as_num + str(i))
	gateway_route = ET.SubElement(P, 'route')
	gateway_route.set('src', central_router_prefix + upper_as_num)
	gateway_route.set('dst', gateway_router_prefix + upper_as_num)
	gateway_route_link_ctn = ET.SubElement(gateway_route, 'link_ctn')
	gateway_route_link_ctn.set('id', bb_link_prefix + upper_as_num)
	server_route = ET.SubElement(P, 'route')
	server_route.set('src', central_router_prefix + upper_as_num)
	server_route.set('dst', server_prefix + upper_as_num)
	server_route_link_ctn = ET.SubElement(server_route, 'link_ctn')
	server_route_link_ctn.set('id', server_link_prefix + upper_as_num)

createAS(p - 1, Root_AS)
print prettify(platform)
