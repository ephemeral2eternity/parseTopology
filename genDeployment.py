import xml.etree.ElementTree as ET
import sys
from ElementTree_pretty import prettify

totalArgs = len(sys.argv)
cmdArgs = sys.argv

if (totalArgs < 2):
        print "Usage : python genDeployment.py hosts.csv deployment.xml\n   hosts.csv : the host name file you want to read host names.\n    deployment.xml : the deployment file name you want to generate\n"
        sys.exit()

hostFileName = cmdArgs[1]
deploymentFileName = cmdArgs[2]

try:
	with open(hostFileName, 'rb') as hostsFile:
		hosts = hostsFile.read().split('\n')
		print hosts
except IOError:
	print "Could not read file ", hostFileName, ", please check the availability of the file!"
	sys.exit()

deploymentFile = open(deploymentFileName, 'w')

comment = ET.Comment('DOCTYPE deployment SYSTEM "https://github.com/ephemeral2eternity/simgrid_simulations.git"')
platform = ET.Element('platform')
platform.set('version', "3")
for host in hosts:
	curProc = ET.SubElement(platform, 'process')
	curProc.set('function', "agentMngt.cacheAgent")
	curProc.set('host', host)
	argu = ET.SubElement(curProc, 'argument')
	argu.set('value', "hosts.csv")

# print ET.tostring(comment)
print prettify(platform)
deploymentFile.write(prettify(platform))

