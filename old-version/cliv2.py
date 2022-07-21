import json
import os
import subprocess
import sys
from subprocess import Popen, PIPE, STDOUT

########################## Declaro funciones ##########################################

def generateToken():  ##################################### GENERACION DEL ACCESS TOKEN

    import boto3
    
    session = boto3.Session(profile_name='sso')
    client = session.client('sso-oidc')
    registerClient = client.register_client(
        clientName='script',
        clientType='public',
    )

    json_data = json.dumps(registerClient,indent=2,default=str)
    json_load = json.loads(json_data)
    
    clientId = json_load['clientId']

    clientSecret = json_load['clientSecret']

    startDeviceAuthorization = client.start_device_authorization(
        clientId=clientId,
        clientSecret=clientSecret,
        startUrl='https://naranjax.awsapps.com/start'
    )

    json_data = json.dumps(startDeviceAuthorization,indent=2,default=str)
    json_load = json.loads(json_data)

    deviceCode = json_load['deviceCode']

    verificationUriComplete = json_load ['verificationUriComplete']

    echo=""" 
    
Generando Link de autorización...

Por favor ingrese el siguiente link en su navegador y haga click en el botón de \"Sign in to AWS CLI \":"""

    print(echo)
    print("")
    print("         ", verificationUriComplete)
    print("")
    print("No olvide estar logueado en su correo de Naranja X")

    respuesta = ""
    while (respuesta != "siguiente") and (respuesta != "cancelar") :
        print(" ")
        respuesta = input('Una vez realizado el login, escriba \"siguiente\" para continuar o \"cancelar\" para interrumpir la configuración : ')
        print(" ")

        if respuesta == "cancelar":
            exit()

    createToken = client.create_token(
        clientId=clientId,
        clientSecret=clientSecret,
        grantType='urn:ietf:params:oauth:grant-type:device_code',
        deviceCode=deviceCode,
    )

    json_data = json.dumps(createToken,indent=2,default=str)
    json_load = json.loads(json_data)

    accessToken =  json_load['accessToken']

    return accessToken    

def installCli(sysOs, which):   #####################################  INSTALACIÓN DEL CLI

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

def removeCli(sysOs, pathPy, which):   ##################################### ELIMINACION DEL CLI

    if (sysOs == "linux"):

        cmd= pathPy + " -m pip uninstall awscli -y"
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

def upgradeCli(sysOs, which):   ##################################### ACTUALIZACION DEL CLI

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

def preInstall():  ##################################### PRE INSTALACIÓN

## Busco el Path de python3

    cmd = 'python --version'
    checkPy=os.system(cmd)

    if checkPy == 0:                #### Chequea si existe python

        p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
        output = p.stdout.readline()
        versionPy = int(output.decode()[7:8])

        if versionPy == 3:

            pathPy="python"

        else:   

            cmd = 'python3 --version'
            p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
            output = p.stdout.readline()
            versionPy3 = int(output.decode()[7:8])

            if versionPy3 == 3:        #### Si $ python3 devuelve python 3.x defino el path python3
                pathPy="python3"

            else:
                print(" ")
                print(" Necesitas tener Python3 instalado para ejecutar este Script")
                print(" ")
                exit()

    else:               ##### Si no existe python, busca python3

        cmd = 'python3 --version'
        p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
        output = p.stdout.readline()
        versionPy3 = int(output.decode()[7:8])

        if versionPy3 == 3:        #### Si $ python3 devuelve python 3.x defino el path python3
            pathPy="python3"

        else:
            print(" ")
            print(" Necesitas tener Python3 instalado para ejecutar este Script")
            print(" ")
            exit()

## Detecto Sistema Operativo

    sysOs = sys.platform     

    if (sysOs == "linux" or sysOs == "darwin"):    #### Chequeo dependencias en mac y linux

        checkCurl = os.system('which curl')
        checkUnzip = os.system('which unzip')
        checkPip = os.system('which pip3')

        if (checkCurl != 0):
            print(" ")
            print(" Necesitas tener curl instalado para ejecutar este script")
            exit()

        elif (checkUnzip != 0):
            print(" ")
            print(" Necesitas tener unzip instalado para ejecutar este script")
            exit()

        elif (checkPip != 0):
            print(" ")
            print(" Necesitas tener python3-pip instalado para ejecutar este script")
            exit()

        cmd=pathPy + " -m pip list |grep boto3"
        checkBoto3 = os.system(cmd)

        if  checkBoto3 != 0:

            cmd=pathPy + " -m pip install boto3"
            os.system(cmd)
            import boto3

    else:               ### Valido el pip3 para Windows
        
        checkPip = os.system('pip3 --version')

        if (checkPip != 0):
            print(" ")
            print(" Necesitas tener python3-pip instalado para ejecutar este script")
            exit()

        cmd=pathPy + " -m pip list | findstr \"boto3\" "
        checkBoto3 = os.system(cmd)

        if  checkBoto3 != 0:

            cmd=pathPy + " -m pip install boto3"
            os.system(cmd)
            import boto3

    return sysOs, pathPy


def configUnixCli():               ####################### Configuro los perfiles del SSO en el CLI para MAC y Linux ###############

    import boto3

    home=subprocess.check_output("echo $HOME", shell=True).decode()
    home=home.replace('\n', '').replace('\r', '')                                

##### Comienzo a configurar el profile para autenticarme en el SSO

    respuesta=""
    while (respuesta != "siguiente") and (respuesta != "cancelar") :
        print(" ")
        respuesta = input('ADVERTENCIA, este script va a eliminar $HOME/.aws/credentials y $HOME/.aws/config ... escriba \"siguiente\" para continuar o \"cancelar\" para interrumpir la configuración : ')
        print(" ")

        if respuesta == "cancelar":
            exit()

    awsDir=home + "/.aws/"
    kubeDir=home + "/.kube/"                                                        

    if os.path.isdir(awsDir):
        ## No ejecuta ninguna acción
        pass
    else:
        cmd="mkdir " + awsDir                                                     
        os.system(cmd)

    cmd="touch " + awsDir + "credentials " + awsDir + "config"           
    os.system(cmd)

    cmd=awsDir + "credentials"
    os.remove(cmd)
    cmd=awsDir + "config"
    os.remove(cmd)

    respuesta=""
    while (respuesta != "sre") and (respuesta != "seguridad") and (respuesta != "otro") and (respuesta != "cancelar"):
        print(" ")
        respuesta = input('A qué equipo pertenece ? Responda: \"sre\" \"seguridad\" \"otro\" o \"cancelar\" para interrumpir la configuración : ')
        print(" ")

    if respuesta == "cancelar":
        exit() 

    elif respuesta == "sre":

        accountId="903852047062"
        roleName="CROSS-Admin-Policy"
        rolePrefix="eks"

    elif respuesta == "seguridad":

        accountId="609957287478"
        roleName="CROSS-Admin-Policy" 
        rolePrefix="eks"

    elif respuesta == "otro":

        accountId="609957287478"
        roleName="CROSS-Sbx-Policy" 
        rolePrefix="iac"

    ssoProfile= """
[sso]
sso_start_url = https://naranjax.awsapps.com/start
sso_region = us-east-1
sso_account_id = """ + accountId + """
sso_role_name = """ + roleName + """
region = us-east-1
output = json

"""
    cmd="echo \"" + ssoProfile + "\" > " + awsDir + "credentials" 
    os.system(cmd)

    return home, awsDir, kubeDir, rolePrefix


def configWinCli():               ####################### Configuro los perfiles del SSO en el CLI  PARA WINDOWS ###############

    import boto3

    home=subprocess.check_output("powershell echo $HOME", shell=True).decode()
    home=home.replace('\n', '').replace('\r', '')                                

##### Comienzo a configurar el profile para autenticarme en el SSO

    respuesta=""
    while (respuesta != "siguiente") and (respuesta != "cancelar") :
        print(" ")
        respuesta = input('ADVERTENCIA, este script va a eliminar $HOME\\.aws\\credentials y $HOME\\.aws\\config ... escriba \"siguiente\" para continuar o \"cancelar\" para interrumpir la configuración : ')
        print(" ")

        if respuesta == "cancelar":
            exit()

    awsDir=home + "\\.aws\\"
    kubeDir=home + "\\.kube\\"                                                        

    if os.path.isdir(awsDir):
        ## No ejecuta ninguna acción
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

    respuesta=""
    while (respuesta != "sre") and (respuesta != "seguridad") and (respuesta != "otro") and (respuesta != "cancelar"):
        print(" ")
        respuesta = input('A qué equipo pertenece ? Responda: \"sre\" \"seguridad\" \"otro\ o \"cancelar\" para interrumpir la configuración : ')
        print(" ")

    if respuesta == "cancelar":
        exit() 

    elif respuesta == "sre":

        accountId="903852047062"
        roleName="CROSS-Admin-Policy"
        rolePrefix="eks"

    elif respuesta == "seguridad":

        accountId="609957287478"
        roleName="CROSS-Admin-Policy"
        rolePrefix="eks"

    elif respuesta == "otro":

        accountId="609957287478"
        roleName="CROSS-Sbx-Policy"
        rolePrefix="iac"

    cmd= "echo [sso] >> " + awsDir + "credentials"
    os.system(cmd)
    cmd=" echo sso_start_url = https://naranjax.awsapps.com/start >> " + awsDir + "credentials"
    os.system(cmd)
    cmd="echo sso_region = us-east-1 >> " + awsDir + "credentials"
    os.system(cmd)
    cmd="echo sso_account_id = " + accountId + " >> " + awsDir + "credentials" 
    os.system(cmd)
    cmd="echo sso_role_name = " + roleName + " >> " + awsDir + "credentials" 
    os.system(cmd)
    cmd="echo region = us-east-1 >> " + awsDir + "credentials"
    os.system(cmd)
    cmd="echo output = json >> " + awsDir + "credentials"
    os.system(cmd)
    cmd="echo; >> " + awsDir + "credentials"
    os.system(cmd)

    return home, awsDir, kubeDir, rolePrefix


def configProfiles(home, awsDir, kubeDir, rolePrefix):
    
    rolePrefix=rolePrefix
    import boto3                                                        ########## Me autentico en el SSO para empezar a configurar los demas profiles

    print(" ")
    print("Autenticando al AWS SSO de Naranja X...") 
    print(" ")
    os.system('aws sso login --profile sso')
    print(" ")
    print("Autenticación exitosa")
    print(" ")

    generatedToken=generateToken()

    print(" ")
    print(" ")
    print(" Preparando los perfiles ...")
    print(" ")
    print(" ")

    session = boto3.Session(profile_name='sso')

    client = session.client('sso')

    response = client.list_accounts(
    maxResults=123,
    accessToken=generatedToken
    )

    json_data = json.dumps(response,indent=2,default=str)
    json_load = json.loads(json_data)

    cantFor=json_load['accountList']
    count1=0
    for i in cantFor:

        awsId=json_load['accountList'][count1]['accountId']
        awsName=json_load['accountList'][count1]['accountName']
        awsName=awsName.lower().split('nx-')[1]

        response = client.list_account_roles(
            maxResults=123,
            accessToken=generatedToken,
            accountId=awsId
        )
    
        json_data2 = json.dumps(response,indent=2,default=str)
        json_load2 = json.loads(json_data2)
    
        accountRoles=json_load2['roleList']

        count2=0

        for j in accountRoles:
            awsRole=json_load2['roleList'][count2]['roleName']

            prefix=awsRole.split('-')[0]
            prefix=prefix.lower() 

            if prefix == rolePrefix:   ############# configuro perfil de EKS  #######################################

                cmd= "echo [DONT_MODIFY_" + prefix + "/" + awsName + "] >> " + awsDir + "credentials"
                os.system(cmd)
                cmd=" echo sso_start_url = https://naranjax.awsapps.com/start >> " + awsDir + "credentials"
                os.system(cmd)
                cmd="echo sso_region = us-east-1 >> " + awsDir + "credentials"
                os.system(cmd)
                cmd="echo sso_account_id = " + awsId + " >> " + awsDir + "credentials" 
                os.system(cmd)
                cmd="echo sso_role_name = " + awsRole + " >> " + awsDir + "credentials" 
                os.system(cmd)
                cmd="echo region = us-east-1 >> " + awsDir + "credentials"
                os.system(cmd)
                cmd="echo output = json >> " + awsDir + "credentials"
                os.system(cmd)
                
                eksProfile="DONT_MODIFY_" + prefix + "/" + awsName

                if awsId == "209462518093":             ###### Chequeo cluster de producción

                    cmd="aws eks list-clusters --output text --profile " + eksProfile + " --query clusters[-1]"
                    clusterName = subprocess.check_output(cmd, shell=True).decode()
                 
                    cmd="aws eks update-kubeconfig --region us-east-1 --name " + clusterName + " --kubeconfig " + kubeDir + "nx-prod-eks" + " --profile " + eksProfile     ## ATENTI
                    cmd=cmd.replace('\n', '').replace('\r', '')
                    os.system(cmd)

                else:

                    cmd="aws eks list-clusters --output text --profile " + eksProfile + " --query clusters"
                    clusterName = subprocess.check_output(cmd, shell=True).decode()

                    cmd="aws eks update-kubeconfig --region us-east-1 --name " + clusterName + " --kubeconfig " + kubeDir + clusterName + " --profile " + eksProfile      ## ATENTI
                    cmd=cmd.replace('\n', '').replace('\r', '')
                    os.system(cmd)

                count2+=1


            else:           ############# configuro perfil de AWS #######################################
                
                prefix=awsRole.split('-')[1]
                prefix=prefix.lower()
                
                cmd= "echo [" + prefix + "/" + awsName + "] >> " + awsDir + "credentials"
                os.system(cmd)
                cmd=" echo sso_start_url = https://naranjax.awsapps.com/start >> " + awsDir + "credentials"
                os.system(cmd)
                cmd="echo sso_region = us-east-1 >> " + awsDir + "credentials"
                os.system(cmd)
                cmd="echo sso_account_id = " + awsId + " >> " + awsDir + "credentials" 
                os.system(cmd)
                cmd="echo sso_role_name = " + awsRole + " >> " + awsDir + "credentials" 
                os.system(cmd)
                cmd="echo region = us-east-1 >> " + awsDir + "credentials"
                os.system(cmd)
                cmd="echo output = json >> " + awsDir + "credentials"
                os.system(cmd)

                count2+=1

    
        count1+=1
    
##############################################################################################################################
####################################################### INCIO DEL SCRIPT #####################################################
##############################################################################################################################


################################ Comienzo a instalar el AWS CLI V2 #########################


preInstall=preInstall()
sysOs=preInstall[0]
pathPy=preInstall[1]

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

        print(" ")
        print("Se ha detectado una versión de AWS ClI v1 instalada...")
        print(" ")
        print("Su versión actual es:")
        print(" ")
        print(versionAws)
        print(" ")
        print("Comienza la actualización de AWS CLI v2...")
        upgradeCli(sysOs, which)
        print(" ")
        versionAws = subprocess.check_output("aws --version", shell=True).decode()
        checkVersion= int(versionAws[8:9])

        if checkVersion < 2:

            removeCli(sysOs, pathPy, which)
            print(" ")
            installCli(sysOs, which)
            print(" ")
            print("La instalación se ha realizado con éxito, su versión actual es: ")
            print(" ")
            versionAws = subprocess.check_output("aws --version", shell=True).decode()
            print(versionAws)

        else:

            print("La instalación se ha realizado con éxito, su versión actual es: ")
            print(" ")
            versionAws = subprocess.check_output("aws --version", shell=True).decode()
            print(versionAws)


    else:

        print(" ")
        print("La Versión del AWS Cli instalada no requiere actualización...")
        print(" ")
        print("Su versión actual es:")
        print(" ")
        print(versionAws)

    
else:
    
    print(" ")
    print("Comienza la instalación de AWS CLI v2...")
    print(" ")
    installCli(sysOs, which)
    versionAws = subprocess.check_output("aws --version", shell=True).decode()
    print(" ")
    print("La instalación se ha realizado con éxito, su versión actual es: ")
    print(" ")
    print(versionAws)



################################ Comienzo a configurar los perfiles de AWS SSO  #########################

if sysOs == "darwin" or sysOs == "linux":

    config=configUnixCli()
    home=config[0]
    awsDir=config[1]
    kubeDir=config[2]
    rolePrefix=config[3]

    configProfiles(home, awsDir, kubeDir, rolePrefix)

else:

    config=configWinCli()
    home=config[0]
    awsDir=config[1]
    kubeDir=config[2]
    rolePrefix=config[3]

    configProfiles(home, awsDir, kubeDir, rolePrefix)
