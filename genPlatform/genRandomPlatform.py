import xml.etree.ElementTree as ET
import sys
import random
import math
from ElementTree_pretty import prettify

totalArgs = len(sys.argv)
cmdArgs = sys.argv

if (totalArgs < 3):
        print "Usage : python genPlatform.py d min max\n   l : the number of levels in the tree;\n    s: the minimum branches in one level;\n    e: e is the maximum branches in one level;"
        sys.exit()
else:
	l = int(cmdArgs[1])
	s = int(cmdArgs[2])
	e = int(cmdArgs[3])

ids = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
        'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
        'U', 'V', 'W', 'X', 'Y', 'Z']

AS_prefix = "AS_"
exitAS_prefix = "exitAS_"
serverAS_prefix = "serverAS_"
server_prefix = "Server_"
client_prefix = "Client_"
router_prefix = "R_"
server_router_prefix = "SRouter_"
link_prefix = "Link_"
server_link_prefix = "ServerAcessLink_"
serverAS_link_prefix = "BBServer_"
bb_link_prefix = "BB_"

power = "1E9"
s_power = "1E10"
c_link_bw = "1E7"
s_link_bw = "2E8"
upper_s_link_bw = "1E9"
super_bb_link_bw = "1E9"
bb_link_bw = "1E9"
inner_bb_link_bw = "1E9"
bb_link_lat = "0.002"

# Printing preamble
print "<?xml version='1.0'?>\n";
print "<!DOCTYPE platform SYSTEM \"http://simgrid.gforge.inria.fr/simgrid.dtd\">\n";

platform = ET.Element('platform')
platform.set('version', "3")

as_num = AS_prefix + "0"
Root_AS = ET.SubElement(platform, 'AS')
Root_AS.set('id', as_num)
Root_AS.set('routing', "Full")

def createAS(l, s, e, P):
	if l == 0:
		as_num_str = P.get('id')
		items = as_num_str.split('_')
		as_num = items[-1]
		P.set('routing', "Floyd")

		# Generating the client hosts in this AS.
		d = random.randint(s, e)
		for i in range(d):
			host = ET.SubElement(P, 'host')
			host.set('id', client_prefix + as_num + ids[i])
			host.set('power', power)

		# Generating the links connecting to hosts
		for i in range(d):
			link = ET.SubElement(P, 'link')
			link.set('id', link_prefix + as_num + ids[i])
			link.set('bandwidth', c_link_bw)
			# link.set('latency', c_link_lat)

		# Creating a central router
		router = ET.SubElement(P, 'router')
		router.set('id', router_prefix + as_num)

		# Creating routes to connect clients to the central router
		for i in range(d):
			route = ET.SubElement(P, 'route')
			route.set('src', router_prefix + as_num)
			route.set('dst', client_prefix + as_num + ids[i])
			route.set('symmetrical', "YES")
			link_ctn = ET.SubElement(route, 'link_ctn')
			link_ctn.set('id', link_prefix + as_num + ids[i])
	
	else:
		as_num_str = P.get('id')
		items = as_num_str.split('_')
		upper_as_num = items[-1]
		d = random.randint(s, e)

		# Setting current AS as Full routing since it is not leaf AS.
		P.set('routing', "Floyd")

		# Creating Exit AS for this AS
		exitP = ET.SubElement(P, 'AS')
		exitP.set('routing', 'Full')
		exitP.set('id', exitAS_prefix + upper_as_num)
		router = ET.SubElement(exitP, 'router')
		router.set('id', router_prefix + upper_as_num)

		# Creating sub ASes in this AS
		for i in range(d):
			as_num = upper_as_num + ids[i]
			curAS = ET.SubElement(P, 'AS')
			curAS.set('id', AS_prefix + as_num)
			createAS(l-1, s, e, curAS)

		# Creating a Server AS in this AS.
		serverAS = ET.SubElement(P, 'AS')
		serverAS.set('id', serverAS_prefix + upper_as_num)
		serverAS.set('routing', "Full")

		# Creating server, server router, server link in serverAS.
		server = ET.SubElement(serverAS, 'host')
		server.set('id', server_prefix + upper_as_num)
		server.set('power', power)
		server_link = ET.SubElement(serverAS, 'link')
		server_link.set('id', server_link_prefix + upper_as_num)
		if l > 1:
			server_link.set('bandwidth', upper_s_link_bw)
		else:
			server_link.set('bandwidth', s_link_bw)
		# server_link.set('latency', s_link_lat)
		server_router = ET.SubElement(serverAS, 'router')
		server_router.set('id', server_router_prefix + upper_as_num)
		server_route = ET.SubElement(serverAS, 'route')
		server_route.set('src', server_router_prefix + upper_as_num)
		server_route.set('dst', server_prefix + upper_as_num)
		server_route.set('symmetrical', "YES")
		server_route_link_ctn = ET.SubElement(server_route, 'link_ctn')
		server_route_link_ctn.set('id', server_link_prefix + upper_as_num)

		# Creating links to connect serverAS to the router in exitAS
		bb_server_link = ET.SubElement(P, 'link')
		bb_server_link.set('id', serverAS_link_prefix + upper_as_num)
		bb_server_link.set('bandwidth', bb_link_bw)
		# bb_server_link.set('latency', inner_bb_link_lat)

		# Creating links to connect subASes to the router in exitAS
		for i in range(d):
			as_num = upper_as_num + ids[i]
			bb_AS_link = ET.SubElement(P, 'link')
			bb_AS_link.set('id', bb_link_prefix + as_num)
			bb_AS_link.set('bandwidth', bb_link_bw)
			if l > 1:
				bb_AS_link.set('latency', bb_link_lat)

			# else:
			#	bb_AS_link.set('latency', bb_link_lat)

		# Creating routes to connect to serverAS
		serverAS_route = ET.SubElement(P, 'ASroute')
		serverAS_route.set('src', serverAS_prefix + upper_as_num)
		serverAS_route.set('dst', exitAS_prefix + upper_as_num)
		serverAS_route.set('gw_src', server_router_prefix + upper_as_num)
		serverAS_route.set('gw_dst', router_prefix + upper_as_num)
		serverAS_route.set('symmetrical', "YES")
		serverAS_route_link_ctn = ET.SubElement(serverAS_route, 'link_ctn')
		serverAS_route_link_ctn.set('id', serverAS_link_prefix + upper_as_num)

		# Creating routes to connect to sub ASes
		for i in range(d):
			as_num = upper_as_num + ids[i]
			bb_AS_route = ET.SubElement(P, 'ASroute')
			bb_AS_route.set('src', AS_prefix + as_num)
			bb_AS_route.set('dst', exitAS_prefix + upper_as_num)
			bb_AS_route.set('gw_src', router_prefix + as_num)
			bb_AS_route.set('gw_dst', router_prefix + upper_as_num)
			bb_AS_route.set('symmetrical', "YES")
			bb_AS_route_link_ctn = ET.SubElement(bb_AS_route, 'link_ctn')
			bb_AS_route_link_ctn.set('id', bb_link_prefix + as_num)


createAS(l-1, s, e, Root_AS)
print prettify(platform)
