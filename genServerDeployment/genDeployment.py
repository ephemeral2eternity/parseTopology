import xml.etree.ElementTree as ET
import sys
import random
from ElementTree_pretty import prettify

totalArgs = len(sys.argv)
cmdArgs = sys.argv

if (totalArgs < 3):
        print "Usage : python genDeployment.py server.csv deployment.xml\n   hosts.csv : the host name file you want to read host names.\n    deployment.xml : the deployment file name you want to generate\n"
        sys.exit()

serverFileName = cmdArgs[1]
deploymentFileName = cmdArgs[2]

try:
	with open(serverFileName, 'rb') as serversFile:
		servers = serversFile.read().split("\n")
		print servers
except IOError:
	print "Could not read file ", serverFileName, ", please check the availability of the file!"
	sys.exit()

deploymentFile = open(deploymentFileName, 'w')

while '' in servers:
	servers.remove('')

N = len(servers)
#  Generate the deployment.xml file for all hosts
# Printing preamble
deploymentFile.write("<?xml version='1.0'?>\n")
deploymentFile.write("<!DOCTYPE platform SYSTEM \"http://simgrid.gforge.inria.fr/simgrid.dtd\">\n")

platform = ET.Element('platform')
platform.set('version', "3")
for idx, srv in enumerate(servers):
	preIdx = (idx - 1) % N
	nextIdx = (idx + 1) % N
	curProc = ET.SubElement(platform, 'process')
	curProc.set('function', "agentDiscovery.cacheAgent")
	curProc.set('host', srv)
	
	# Set predecessor first
	preSrv = servers[preIdx]
	argu = ET.SubElement(curProc, 'argument')
	argu.set('value', preSrv)
	
	# Set successor
	nextSrv = servers[nextIdx]
	argu = ET.SubElement(curProc, 'argument')
	argu.set('value', nextSrv)
	
	# Set overlayID file
	nextSrv = servers[nextIdx]
	argu = ET.SubElement(curProc, 'argument')
	argu.set('value', "overlayID.csv")

# print ET.tostring(comment)
# print prettify(platform)
deploymentFile.write(prettify(platform))

