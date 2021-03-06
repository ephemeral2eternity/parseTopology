import xml.etree.ElementTree as ET
import sys
import random
from ElementTree_pretty import prettify

totalArgs = len(sys.argv)
cmdArgs = sys.argv

if (totalArgs < 3):
        print "Usage : python genDeployment.py server.csv hosts.csv deployment.xml\n   hosts.csv : the host name file you want to read host names.\n    deployment.xml : the deployment file name you want to generate\n"
        sys.exit()

serverFileName = cmdArgs[1]
hostFileName = cmdArgs[2]
deploymentFileName = cmdArgs[3]

try:
	with open(serverFileName, 'rb') as serversFile:
		servers = serversFile.read().split("\n")
		print servers
except IOError:
	print "Could not read file ", serverFileName, ", please check the availability of the file!"
	sys.exit()

try:
	with open(hostFileName, 'rb') as hostsFile:
		hosts = hostsFile.read().split("\n")
		print hosts
except IOError:
	print "Could not read file ", clientFileName, ", please check the availability of the file!"
	sys.exit()

deploymentFile = open(deploymentFileName, 'w')

while '' in servers:
	servers.remove('')

while '' in hosts:
	hosts.remove('')

#  Generate the deployment.xml file for all hosts
# Printing preamble
deploymentFile.write("<?xml version='1.0'?>\n")
deploymentFile.write("<!DOCTYPE platform SYSTEM \"http://simgrid.gforge.inria.fr/simgrid.dtd\">\n")

platform = ET.Element('platform')
platform.set('version', "3")
for host in hosts:
	curProc = ET.SubElement(platform, 'process')
	if host in servers:
		curProc.set('function', "agentMngt.cacheAgent")
	else:
		curProc.set('function', "agentMngt.clientAgent")

	curProc.set('host', host)
	argu = ET.SubElement(curProc, 'argument')
	argu.set('value', serverFileName)

# print ET.tostring(comment)
# print prettify(platform)
deploymentFile.write(prettify(platform))

