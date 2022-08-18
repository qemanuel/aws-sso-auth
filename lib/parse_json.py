import json
import os
import subprocess
import sys
from subprocess import Popen, PIPE
import lib.get_properties as properties

sso_properties = properties.getSSOProperties()
sysOs=sys.platform

if sysOs == "darwin" or sysOs == "linux":
    slash="/"   
else:
    slash= "\\"

def parseCredentialsFile(awsDir):
    awsDir=awsDir + slash + "cli" + slash + "cache"   

    for filename in os.listdir(awsDir):
        f = os.path.join(awsDir, filename)
        # checking if it is a file
        if os.path.isfile(f):
            credentials = getCredentials(f)
            os.remove(f)
            return credentials


def getCredentials(fileName):
    with open(fileName, "r") as f:
        data = json.load(f)
        credentials = data['Credentials']
        return (credentials['AccessKeyId'], credentials['SecretAccessKey'], credentials['SessionToken'])


