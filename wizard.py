import os
import subprocess
import sys
from subprocess import Popen, PIPE, STDOUT
import lib.install_cli as cli 
import lib.profiles as profiles 
import lib.get_properties as properties


sso_properties = properties.getSSOProperties()
sysOs=sys.platform          ##Detecto OS

checkAws = os.system('aws --version')

which=os.system('which aws')

if which == 0:
    which=subprocess.check_output("which aws", shell=True).decode()
    which=which.replace('\n', '').replace('\r', '')
    which=which.lower().split('/aws')[0]
else:
    which="/usr/local/bin"

if checkAws == 0:
    versionAws = subprocess.check_output("aws --version", shell=True).decode()
    checkVersion= int(versionAws[8:9])

    if checkVersion < 2:
        print("Se ha detectado una versión de AWS ClI v1 instalada ("+versionAws+"})\n");
        print("Comienza la actualización de AWS CLI v2...\n")
        upgradeCli(sysOs, which)
        versionAws = subprocess.check_output("aws --version", shell=True).decode()
        checkVersion= int(versionAws[8:9])

        if checkVersion < 2:
            cli.removeCli(sysOs, pathPy, which)
            cli.installCli(sysOs, which)
            versionAws = subprocess.check_output("aws --version", shell=True).decode()

else:
    print("Comienza la instalación de AWS CLI v2...\n")
    cli.installCli(sysOs, which)
    versionAws = subprocess.check_output("aws --version", shell=True).decode()

print("Version actual" + versionAws + "\n")

################################ Comienzo a configurar los perfiles de AWS SSO  #########################

if sysOs == "darwin" or sysOs == "linux":

    config=cli.configUnixCli(sso_properties)
    home=config[0]
    awsDir=config[1]
    kubeDir=config[2]

    profiles.configProfiles(home, awsDir, kubeDir, sso_properties)

else:
    config=cli.configWinCli(sso_properties)
    home=config[0]
    awsDir=config[1]
    kubeDir=config[2]

    profiles.configProfiles(home, awsDir, kubeDir, sso_properties)
