from SSO import SSO
from boto3.session import Session

class SSOConfig:
    def __init__(self, startUrl, ssoRoleName, ssoRegion, defaultRegion, defaultOutput):
        self.startUrl = startUrl
        self.ssoRoleName = ssoRoleName
        self.ssoRegion = ssoRegion
        self.defaultRegion = defaultRegion
        self.defaultOutput = defaultOutput
        self.sso = SSO(Session(), self.startUrl, self.ssoRegion)
        self.token = self.sso.getToken()
    
    def getConfigProfiles(self, configFile):
        mainRoles = self.sso.getMainRoles(self.token)
        configContent = ""
        for mainRole in mainRoles:
            roleConfig = f"""
[profile {mainRole['accountName']}_{mainRole['mainRole']}]
sso_region = {self.ssoRegion}
sso_start_url = {self.startUrl}
sso_account_id = {mainRole['accountId']}
sso_role_name = {mainRole['mainRole']}
region = {self.defaultRegion}
output = {self.defaultOutput}
"""
            configContent = configContent + '\n' + roleConfig

        self.writeFile(configContent, configFile)

    def getCredentialsProfiles(self, credentialsFile):
        mainRoles = self.sso.getMainRoles(self.token)
        credentialsContent = ""
        for mainRole in mainRoles:
            mainRoleKeys = self.sso.getRoleCredentials(self.token, mainRole['accountId'], mainRole['mainRole'])
            roleCredentials = f"""
[{mainRole['accountName']}_{mainRole['mainRole']}]
aws_access_key_id = {mainRoleKeys['accessKeyId']}
aws_secret_access_key = {mainRoleKeys['secretAccessKey']}
aws_session_token = {mainRoleKeys['sessionToken']}
region = {self.defaultRegion}
output = {self.defaultOutput}
"""
            credentialsContent = credentialsContent + '\n' + roleCredentials

        self.writeFile(credentialsContent, credentialsFile)


    def writeFile(self, content, file):
        with open(file, "w") as f:
           f.write(content)


