import json
import os
import subprocess
from subprocess import Popen, PIPE

def parseFile(home):
    home=home + "\\.aws\\cli\\cache"   

    for filename in os.listdir(home):
        f = os.path.join(home, filename)
        # checking if it is a file
        if os.path.isfile(f):
            credentials = getCredentials(f)
            return credentials


def getCredentials(fileName):
    print("\n\nParseando file: ", fileName)
    with open(fileName, "r") as f:
        data = json.load(f)
        credentials = data['Credentials']
        return ("aws_access_key_id="+credentials['AccessKeyId'], "aws_secret_access_key="+credentials['SecretAccessKey'], "aws_session_token="+credentials['SessionToken'])


