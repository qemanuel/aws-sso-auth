import os
from dotenv import load_dotenv

load_dotenv()

##################################### OBTENGO PROPIEDADES DE ARCHIVO DE CONFIGURACION
def getSSOProperties():
    startUrl = os.getenv('SSO_START_URL')
    accountId = os.getenv('ACCOUNT_ID')
    roleName = os.getenv('ROLE_NAME')
    ssoRegion = os.getenv('SSO_REGION')
    region = os.getenv('REGION')

    

    for key in startUrl,accountId,roleName,ssoRegion,region:
        if(key == None):
            raise Exception("""
            Falta alguna variable de entorno en tu archivo .env 
            Variables necesarias: [SSO_START_URL, ACCOUNT_ID, ROLE_NAME, SSO_REGION, REGION]
            """)

    return {
        'startUrl':startUrl,
        'accountId':accountId,
        'roleName':roleName,
        'ssoRegion':ssoRegion,
        'region':region
    }