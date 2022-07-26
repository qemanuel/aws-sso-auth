import os
import configparser
import subprocess
import sys
import lib.parse_json as json
import lib.get_properties as properties


sso_properties = properties.getSSOProperties()
sysOs=sys.platform

if sysOs == "darwin" or sysOs == "linux":
    slash="/"   
else:
    slash= "\\"

def getAWSHome():
    sysOs=sys.platform
    cmd = "echo $HOME"
    if sysOs == "win32":
        cmd = "powershell " + cmd 
    home=subprocess.check_output(cmd, shell=True).decode()
    return home.replace('\n', '').replace('\r', '') + slash + ".aws" + slash

os.system('aws sso login --profile sso')

config = configparser.ConfigParser()
home = getAWSHome()
credentialsFile = home + 'credentials'
config.read(credentialsFile)
## Vacio la carpeta de credenciales
for f in os.listdir(home + slash + "cli" + slash + "cache" ):
    os.remove(os.path.join(home + slash + "cli" + slash + "cache" , f))

for profileName in config.sections():
    profile = config[profileName]
    if profileName != 'sso':
        os.system('aws sts get-caller-identity --profile ' + profileName)
        credentials = json.parseCredentialsFile(home)
        profile['aws_access_key_id']=credentials[0]
        profile['aws_secret_access_key']=credentials[1]
        profile['aws_session_token']=credentials[2]

with open(credentialsFile, "w") as f:
    config.write(f, False)



