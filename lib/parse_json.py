import json
import os
import subprocess
from subprocess import Popen, PIPE

def parseCredentialsFile(awsDir):
    awsDir=awsDir + "\\cli\\cache"   

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


