import xml.etree.ElementTree as ET
import sys
import random
import copy
from ElementTree_pretty import prettify

totalArgs = len(sys.argv)
cmdArgs = sys.argv

if (totalArgs < 3):
        print "Usage : python genDeployment.py servers.csv clients.csv deployment.xml\n   hosts.csv : the host name file you want to read host names.\n    deployment.xml : the deployment file name you want to generate\n"
        sys.exit()

serverFileName = cmdArgs[1]
clientFileName = cmdArgs[2]
deploymentFileName = cmdArgs[3]

try:
	with open(serverFileName, 'rb') as serversFile:
		servers = serversFile.read().split("\n")
		print servers
except IOError:
	print "Could not read file ", serverFileName, ", please check the availability of the file!"
	sys.exit()

try:
	with open(clientFileName, 'rb') as clientsFile:
		clients = clientsFile.read().split("\n")
		print clients
except IOError:
	print "Could not read file ", clientFileName, ", please check the availability of the file!"
	sys.exit()

deploymentFile = open(deploymentFileName, 'w')

while '' in servers:
	servers.remove('')

while '' in clients:
	clients.remove('')

#  Generate the deployment.xml file for all hosts
# Printing preamble
deploymentFile.write("<?xml version='1.0'?>\n")
deploymentFile.write("<!DOCTYPE platform SYSTEM \"http://simgrid.gforge.inria.fr/simgrid.dtd\">\n")

platform = ET.Element('platform')
platform.set('version', "3")
for server in servers:
	curProc = ET.SubElement(platform, 'process')
	curProc.set('function', "agentMngt.cacheAgent")
	curProc.set('host', server)

def common_prefix(a,b):
	i = 0
	match_digit = i
	for i, (x, y) in enumerate(zip(a,b)):
		if x!=y:
			# print "unmatched digit: ", i 
			break
		else: match_digit = i
	return a[:match_digit + 1]

def getCacheAgent(client, serverList):
	client_num = client.split("_")[-1]
	match_digit = 0
	if serverList:
		cacheAgent = serverList[0]
	else:
		print "ServerList is empty, exit the program!"
		sys.exit()
	for server in serverList:
		server_num = server.split("_")[-1]
		match_prefix = common_prefix(client_num, server_num)
		# print "matched prefix for ", client_num, " and ", server_num, " is ", match_prefix
		if len(match_prefix) > match_digit:
			match_digit = len(match_prefix)
			cacheAgent = server

	return cacheAgent
		
for client in clients:
	clientProc = ET.SubElement(platform, 'process')
	clientProc.set('function', "agentMngt.clientAgent")
	clientProc.set('host', client)
	candidateServers = []
	candidateServers = copy.deepcopy(servers)
	print "The length of servers is :", len(candidateServers)
	cacheAgent = getCacheAgent(client, candidateServers)
	candidateServers.remove(cacheAgent)

	argu = ET.SubElement(clientProc, 'argument')
	argu.set('value', cacheAgent)

	for candidate in candidateServers:
		argu = ET.SubElement(clientProc, 'argument')
		argu.set('value', candidate)
# print ET.tostring(comment)
print prettify(platform)
deploymentFile.write(prettify(platform))
