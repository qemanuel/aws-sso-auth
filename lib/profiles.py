import boto3
import os
import lib.generate_token as generate_token
import subprocess
import re
import lib.parse_json as json

def configProfiles(home, awsDir, kubeDir, sso_properties):
    
    ## Me autentico en el SSO para empezar a configurar los demas profiles

    print("Autenticando al AWS SSO...\n\n") 
    os.system('aws sso login --profile sso')
    print("Autenticación exitosa\n")

    generatedToken=generate_token.generateToken(sso_properties['startUrl'])

    print(" Preparando los perfiles ...\n\n")

    session = boto3.Session(profile_name='sso')

    client = session.client('sso')

    response = client.list_accounts(maxResults=123, 
                                    accessToken=generatedToken)

    for profile in response['accountList']:

        awsId=profile['accountId']
        awsName=profile['accountName'].lower()

        account_roles = client.list_account_roles(maxResults=123,
                                             accessToken=generatedToken,
                                             accountId=awsId)
    
        for roles in account_roles['roleList']:
            awsRole=roles['roleName']

            awsProfile = awsName + "/" + awsRole.lower()

            cmd= "echo [" + awsProfile + "] >> " + awsDir + "credentials"
            os.system(cmd)
            cmd=" echo sso_start_url =" + sso_properties['startUrl'] + " >> " + awsDir + "credentials"
            os.system(cmd)
            cmd="echo sso_region =" + sso_properties['ssoRegion'] + " >> " + awsDir + "credentials"
            os.system(cmd)
            cmd="echo sso_account_id = " + awsId + " >> " + awsDir + "credentials" 
            os.system(cmd)
            cmd="echo sso_role_name = " + awsRole + " >> " + awsDir + "credentials" 
            os.system(cmd)
            cmd="echo region =" + sso_properties['region'] + " >> " + awsDir + "credentials"
            os.system(cmd)
            cmd="echo output = json >> " + awsDir + "credentials"
            os.system(cmd)

            print("Obteniendo credenciales para " + awsProfile + "...\n\n") 
            os.system('aws sts get-caller-identity --profile ' + awsProfile)

            print("Cargando credenciales al perfil\n")
            credentials = json.parseCredentialsFile(awsDir)

            print("Credenciales: \n")
            print( credentials)

            cmd="echo aws_access_key_id=" + credentials[0] + " >> " + awsDir + "credentials"
            os.system(cmd)
            cmd="echo aws_secret_access_key=" + credentials[1] + " >> " + awsDir + "credentials"
            os.system(cmd)
            cmd="echo aws_session_token=" + credentials[2] + " >> " + awsDir + "credentials"
            os.system(cmd)

    print(" Perfiles listos ...\n\n")

