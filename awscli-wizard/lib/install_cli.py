import os
import subprocess
import sys
from subprocess import Popen, PIPE, STDOUT


#####################################  INSTALACIÓN DEL CLI
def installCli(sysOs, which):   
    if (sysOs == "linux"):
        os.system('sudo rm -rf /usr/local/aws-cli')
        os.system('curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"') 
        os.system('unzip -q awscliv2.zip')
        cmd="sudo ./aws/install --bin-dir " + which
        os.system(cmd)
        os.system('sudo rm -rf ./aws/')
        os.system('sudo rm awscliv2.zip')

    elif (sysOs == "darwin"):
        os.system('sudo rm -rf /usr/local/aws-cli')
        os.system('curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"')
        os.system('sudo installer -pkg AWSCLIV2.pkg -target /')
        os.system('sudo rm AWSCLIV2.pkg')

    elif (sysOs == "win32"):
        os.system('bitsadmin /create downloadawscliv2')
        os.system('bitsadmin /transfer downloadawscliv2 https://awscli.amazonaws.com/AWSCLIV2.msi C:\\Users\\AWSCLIV2.msi')
        os.system('msiexec /i C:\\Users\\AWSCLIV2.MSI /q')
        os.system('setx path "%path%;C:\\Program Files\\Amazon\\AWSCLIV2"')
        os.remove('C:\\Users\\AWSCLIV2.MSI')

##################################### ELIMINACION DEL CLI
def removeCli(sysOs, which):   

    if (sysOs == "linux"):
        try:
            cmd="python3 -m pip uninstall awscli -y"
            os.system(cmd)
        except:
            cmd="python -m pip uninstall awscli -y"
            os.system(cmd)              
        cmd=("sudo rm " + which + "/aws" )
        os.system(cmd)
        cmd=("sudo rm " + which + "/aws_completer" )
        os.system(cmd)
        os.system('sudo rm -rf /usr/local/aws-cli')

    elif (sysOs == "darwin"):

        cmd= pathPy + " -m pip uninstall awscli -y"
        os.system(cmd)  
        cmd=("sudo rm " + which + "/aws" )
        os.system(cmd)
        cmd=("sudo rm " + which + "/aws_completer" )
        os.system(cmd)
        os.system('sudo rm -rf /usr/local/aws-cli')

    elif (sysOs == "win32"):

        os.system('wmic product where name="AWS Command Line Interface" call uninstall /nointeractive')
        os.system('wmic product where name="AWS Command Line Interface v2" call uninstall /nointeractive')

##################################### ACTUALIZACION DEL CLI
def upgradeCli(sysOs, which):   

    if (sysOs == "linux"):
        os.system('sudo rm -rf /usr/local/aws-cli')
        os.system('curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"') 
        os.system('unzip -q awscliv2.zip')
        cmd="sudo ./aws/install --bin-dir " + which + " --update"
        os.system(cmd)
        os.system('sudo rm -rf ./aws/')
        os.system('sudo rm awscliv2.zip')

    elif (sysOs == "darwin"):
        os.system('sudo rm -rf /usr/local/aws-cli')
        os.system('curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"')
        os.system('sudo installer -pkg AWSCLIV2.pkg -target /')
        os.system('sudo rm AWSCLIV2.pkg')

    elif (sysOs == "win32"):
        os.system('bitsadmin /create downloadawscliv2')
        os.system('bitsadmin /transfer downloadawscliv2 https://awscli.amazonaws.com/AWSCLIV2.msi C:\\Users\\AWSCLIV2.msi')
        os.system('msiexec /i C:\\Users\\AWSCLIV2.MSI /q')
        os.system('setx path "%path%;C:\\Program Files\\Amazon\\AWSCLIV2"')
        os.remove('C:\\Users\\AWSCLIV2.MSI')  

####################### Configuro los perfiles del SSO en el CLI para MAC y Linux ###############
def configUnixCli(sso_properties):               

    home=subprocess.check_output("echo $HOME", shell=True).decode()
    home=home.replace('\n', '').replace('\r', '')                                

    ##### Comienzo a configurar el profile para autenticarme en el SSO

    respuesta=""

    
    respuesta = input('ADVERTENCIA, este script va a eliminar ' + home + '/.aws/credentials y ' + home + '/.aws/config ... escriba \"cancelar\" para interrumpir la configuración o cualquier tecla para continuar:\n')
    if respuesta.lower == "cancelar":
        exit()

    awsDir=home + "/.aws/"
    kubeDir=home + "/.kube/"                                                        

    if os.path.isdir(awsDir):
        cmd='sudo rm ' + awsDir + "credentials"
        os.system(cmd)
        cmd='sudo rm ' + awsDir + "config"
        os.system(cmd)   

    else:
        cmd="mkdir " + awsDir                                                     
        os.system(cmd)

    cmd="touch " + awsDir + "credentials " + awsDir + "config"           
    os.system(cmd)


    respuesta=""
    ssoProfile= """
    [sso]
    sso_start_url =""" +sso_properties['startUrl'] +"""
    sso_account_id =""" +sso_properties['accountId'] +"""
    sso_role_name =""" +sso_properties['roleName'] +"""
    sso_region =""" +sso_properties['ssoRegion'] +"""
    region =""" +sso_properties['region'] +"""
    output = json

    """
    cmd="echo \"" + ssoProfile + "\" > " + awsDir + "credentials" 
    os.system(cmd)

    awsConfig= """
    [default]
    region = """ +sso_properties['region'] +"""
    output = json

    """
    cmd="echo \"" + awsConfig + "\" > " + awsDir + "config" 
    os.system(cmd)

    return home, awsDir, kubeDir


####################### Configuro los perfiles del SSO en el CLI  PARA WINDOWS ###############
def configWinCli(sso_properties):               

    home=subprocess.check_output("powershell echo $HOME", shell=True).decode()
    home=home.replace('\n', '').replace('\r', '')                                

    ##### Comienzo a configurar el profile para autenticarme en el SSO

    respuesta=""
    respuesta = input('ADVERTENCIA, este script va a eliminar ' + home + '/.aws/credentials y ' + home + '/.aws/config ... escriba \"cancelar\" para interrumpir la configuración o cualquier tecla para continuar:\n')

    if respuesta.lower == "cancelar":
        exit()

    awsDir=home + "\\.aws\\"
    kubeDir=home + "\\.kube\\"                                                        

    if os.path.isdir(awsDir):
        pass

    else:
        cmd="MD " + awsDir                                                     
        os.system(cmd)

    cmd="echo   >" + awsDir + "credentials "
    os.system(cmd)

    cmd="echo   >" + awsDir + "config"
    os.system(cmd)

    cmd=awsDir + "credentials"
    os.remove(cmd)
    cmd=awsDir + "config"
    os.remove(cmd)

    cmd= "echo [sso] >> " + awsDir + "credentials"
    os.system(cmd)
    cmd=" echo sso_start_url = " + sso_properties['startUrl'] + " >> " + awsDir + "credentials"
    os.system(cmd)
    cmd="echo sso_account_id = " + sso_properties['accountId'] + " >> " + awsDir + "credentials" 
    os.system(cmd)
    cmd="echo sso_role_name = " + sso_properties['roleName'] + " >> " + awsDir + "credentials" 
    os.system(cmd)
    cmd="echo sso_region = " + sso_properties['ssoRegion'] + " >> " + awsDir + "credentials"
    os.system(cmd)
    cmd="echo region = " + sso_properties['region'] + " >> " + awsDir + "credentials"
    os.system(cmd)
    cmd="echo output = json >> " + awsDir + "credentials"
    os.system(cmd)
    cmd="echo; >> " + awsDir + "credentials"
    os.system(cmd)


    cmd= "echo [default] >> " + awsDir + "config"
    os.system(cmd)
    cmd="echo region = " + sso_properties['region'] + " >> " + awsDir + "config"
    os.system(cmd)
    cmd="echo output = json >> " + awsDir + "config"
    os.system(cmd)
    cmd="echo; >> " + awsDir + "config"
    os.system(cmd)

    return home, awsDir, kubeDir


