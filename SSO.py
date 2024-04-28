from time import time, sleep
import webbrowser
from boto3.session import Session

class SSO:
    def __init__(self, session, startUrl, ssoRegion):
        self.session = session
        self.startUrl = startUrl
        self.ssoRegion = ssoRegion
    
    def getToken(self):
        ssoOidc = self.session.client('sso-oidc', region_name=self.ssoRegion)
        clientCreds = ssoOidc.register_client(
            clientName='sso-py',
            clientType='public',
        )
        deviceAuthorization = ssoOidc.start_device_authorization(
            clientId=clientCreds['clientId'],
            clientSecret=clientCreds['clientSecret'],
            startUrl=self.startUrl,
        )
        url = deviceAuthorization['verificationUriComplete']
        deviceCode = deviceAuthorization['deviceCode']
        expiresIn = deviceAuthorization['expiresIn']
        interval = deviceAuthorization['interval']
        webbrowser.open(url, autoraise=True)
        for n in range(1, expiresIn // interval + 1):
            sleep(interval)
            try:
                token = ssoOidc.create_token(
                    grantType='urn:ietf:params:oauth:grant-type:device_code',
                    deviceCode=deviceCode,
                    clientId=clientCreds['clientId'],
                    clientSecret=clientCreds['clientSecret'],
                )
                break
            except ssoOidc.exceptions.AuthorizationPendingException:
                pass

        return token['accessToken']

    def getMainRoles(self, accessToken):
        sso = self.session.client('sso', region_name=self.ssoRegion)
        accounts = sso.list_accounts(
            maxResults=123,
            accessToken=accessToken,
        )['accountList']

        mainRoles = []
        for account in accounts:
            accountId = account['accountId']
            accountName = account['accountName']
            mainRole = sso.list_account_roles(
                accessToken=accessToken,
                accountId=accountId,
            )['roleList'][0]['roleName']

            mainRoles.append({
                'accountId': accountId,
                'accountName': accountName,
                'mainRole': mainRole,
            })
        return mainRoles

    def getRoleCredentials(self, accessToken, accountId, roleName):
        sso = self.session.client('sso', region_name=self.ssoRegion)
        roleCreds = sso.get_role_credentials(
            roleName=roleName,
            accountId=accountId,
            accessToken=accessToken,
        )['roleCredentials']

        return {
            'accessKeyId': roleCreds['accessKeyId'],
            'secretAccessKey': roleCreds['secretAccessKey'],
            'sessionToken': roleCreds['sessionToken'],
        }
