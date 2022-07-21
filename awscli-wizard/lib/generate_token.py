import boto3

def generateToken(startUrl):                            ## GENERACION DEL ACCESS TOKEN

    session = boto3.Session(profile_name='sso')
    client = session.client('sso-oidc')
    registerClient = client.register_client(clientName='script',
                                            clientType='public')
    
    clientId = registerClient['clientId']

    clientSecret = registerClient['clientSecret']

    startDeviceAuthorization = client.start_device_authorization(clientId=clientId,
                                                                 clientSecret=clientSecret,
                                                                 startUrl=startUrl)

    deviceCode = startDeviceAuthorization['deviceCode']

    verificationUriComplete = startDeviceAuthorization ['verificationUriComplete']

    print("Generando Link de autorización..." + '\n' + '\n')
    print("Por favor ingrese el siguiente link en su navegador y haga click en el botón de \"Sign in to AWS CLI \":" + '\n')
    print("\t", verificationUriComplete, '\n')

    respuesta = ""
    noDevice=True
    while (noDevice):
        
        respuesta = input('Una vez realizado el login, escriba \"siguiente\" para continuar o \"cancelar\" para interrumpir la configuración: \n')
        
        if respuesta != "cancelar":
            try:
                createToken = client.create_token(clientId=clientId,
                                      clientSecret=clientSecret,
                                      grantType='urn:ietf:params:oauth:grant-type:device_code',
                                      deviceCode=deviceCode)
                noDevice = False
            except:
                print("El proceso no podrá continuar si no ingresas al link generado y completas el login" + '\n' + '\n' + verificationUriComplete)
                respuesta=""
        else:
            exit()

    accessToken =  createToken['accessToken']

    return accessToken 