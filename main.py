import os
from dotenv import load_dotenv
from SSOConfig import SSOConfig

def main():
    load_dotenv()
    startUrl = os.getenv('SSO_START_URL')
    ssoRoleName = os.getenv('SSO_ROLE_NAME')
    ssoRegion = os.getenv('SSO_REGION')
    defaultRegion = os.getenv('DEFAULT_REGION')
    defaultOutput = os.getenv('DEFAULT_OUTPUT', 'json')
    fileFormat = os.getenv('FILE_FORMAT')
    filePath = os.getenv('FILE_PATH', 'config')

    for key in startUrl,ssoRoleName,ssoRegion,defaultRegion:
        if(key == None):
            raise Exception(f'There are missing environment variables. Please, verify your .env file')

    ssoConfig = SSOConfig(startUrl, ssoRoleName, ssoRegion, defaultRegion, defaultOutput)
    if fileFormat == "config" :
        ssoConfig.getConfigProfiles(filePath)
    elif fileFormat == "credentials":
        ssoConfig.getCredentialsProfiles(filePath)
    else:
        raise Exception(f'Environment Variable "FILE_FORMAT" must be either "config" or "credentials"')

if __name__ == "__main__":
    main()
