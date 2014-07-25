import xml.etree.ElementTree as ET
import sys

def findDivergent(str1, str2):
	items1 = str1.split(',')
	items2 = str2.split(',')
	preItem = ""
	for i in range(min(len(items1), len(items2))):
		if (items1[i] == items2[i]):
			preItem = items1[i]
			pass
		else:
			# print preItem
			break

	return preItem

totalArgs = len(sys.argv)
cmdArgs = str(sys.argv)
tree = ET.parse('platform.xml')
root = tree.getroot()
routeList = []
routerList = []
graphList = []

if (totalArgs < 2):
	print "Usage : python readPlatform.py -h[lr]\n   -h : print all host names into hosts.csv\n   -l : print all link IDs (including switchs) into links.csv\n   -r : print all routes into routes.xml and print all switch IDs into swithes.csv"
	sys.exit()

if ("-h" in cmdArgs):
	print "Print host names into file hosts.csv!"
	hostFile = open("hosts.csv", 'w')

if ("-l" in cmdArgs):
	print "Print link IDs into file links.csv!"
	linkFile = open("links.csv", 'w')

if ("-r" in cmdArgs):
	print "Print routes into file routes.csv and print all switch IDs into switches.csv!"
	routeFile = open("routes.csv", 'w')
	routerFile = open("routers.csv", 'w')

if ("-g" in cmdArgs):
	print "Print all links into graph file for gephi!"
	graphFile = open("graph.csv", 'w')

for child in root.findall('AS'):
	# Write host names to hosts.xml file.
	if ("-h" in cmdArgs):
		for host in child.iter('host'):
			print "Host: ", host.get('id')
			hostFile.write(host.get('id') + '\n')

	if ("-l" in cmdArgs):
		for link in child.iter('link'):
			# print "Link: ", link.get('id'), "; Bandwidth: ", link.get('bandwidth'), "; Latency: ", link.get('latency')
			# linkFile.write(link.get('id') + "," + link.get('bandwidth') + "," + link.get('latency') + '\n')
			print "Link: ", link.get('id'), "; Bandwidth: ", link.get('bandwidth')
			linkFile.write(link.get('id') + "," + link.get('bandwidth') + '\n')

	
	if ("-r" in cmdArgs):
		for route in child.iter('route'):
			curRt = ""
			link_ctn_list = route.findall('link_ctn')
			for i, linkCtn in enumerate(link_ctn_list):
				curRt = curRt + linkCtn.get('id')
				if i < len(link_ctn_list) - 1:
					curRt = curRt + ","
			print "[Route]", route.get('src'), "-->", route.get('dst'), ":", curRt
			
			routeList.append(curRt)
			routeFile.write(route.get('src') + "," + curRt + "," + route.get('dst') + "\n")
		
		for route in child.iter('ASroute'):
			curRt = ""
			link_ctn_list = route.findall('link_ctn')
			for i, linkCtn in enumerate(link_ctn_list):
				curRt = curRt + linkCtn.get('id')
				if i < len(link_ctn_list) - 1:
					curRt = curRt + ","
			print "[Route]", route.get('gw_src'), "-->", route.get('gw_dst'), ":", curRt
			
			routeList.append(curRt)
			routeFile.write(route.get('gw_src') + "," + curRt + "," + route.get('gw_dst') + "\n")

		for router in child.iter('router'):
			print "Router ID: ", router.get('id')
			routerFile.write(router.get('id') + "\n")
	
	if ("-g" in cmdArgs):
		for route in child.iter('route'):
			print "[Graph Link]", route.get('src'), "-->", route.get('dst')
			graphFile.write(route.get('src') + "," + route.get('dst') + "\n")

		for route in child.iter('ASroute'):
			print "[Graph Link]", route.get('gw_src'), "-->", route.get('gw_dst')
			graphFile.write(route.get('gw_src') + "," + route.get('gw_dst') + "\n")

if ("-h" in cmdArgs):
	hostFile.close()

if ("-l" in cmdArgs):
	linkFile.close()

if ("-r" in cmdArgs):
	routeFile.close()
	routerFile.close()

if ("-g" in cmdArgs):
	graphFile.close()

