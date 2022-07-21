# AWS CLI and K8S profiles Wizard

## Asistente para instalar y configurar awscli v2 con sus perfiles de SSO y sus kubeconfig

*  **Necesita tener Python3 y pip3 instalado**
*  **El asistente se basa en el siguiente [documento](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html) para instalar el awscli v2.**
*  **El asistente crea los files $HOME/.aws/credentials y $HOME/.aws/config con las configuraciones de tu usuario de SSO.**
*  **El asistente descubre qué perfiles tienen acceso a un cluster de EKS y descarga sus kubeconfig correspondientes.**

## Instrucciones de uso:
  
### 1. Clonar este repositorio en el tag de la versión deseada y posicionarse en el directorio awscli-wizard.
`git clone --depth 1 --branch v1.0.0 git@gitlab.naranja.dev:devops/tools/awscli-wizard.git`

`cd awscli-wizard`

### 2. Instalar las librerías necesarias para el asistente.
`pip3 install -r requirements.txt`

### 3. Ejecutar el asistente con Python3.
`unset AWS_ACCESS_KEY_ID`   (para asegurarse de que no interfieran otras credenciales)

`python3 wizard.py`

### 4. Seguir el asistente según las necesidades de tu deployment.
**Aclaraciones:**
*  Al comenzar, el asistente va a eliminar los files $HOME/.aws/config y $HOME/.aws/credentials existentes
*  El asistente hace 2 logins al SSO para federar con SAML. Uno abre el navegador automáticamente y el siguiente imprime el link en consola.
*  Los Kubeconfig se descargan en $HOME/.kube/${cluster_name}


### 5. Post ejecución y uso de perfiles:
*  Se pueden modificar el nombre de los perfiles (el que figura entre "[ ]"), que NO sean usuarios de eks, creados en el file $HOME/.aws/credentials por uno mas amigable. 
*  El asistente crea los perfiles, pero las credenciales caducan en menos de 24hs, para renovarlas se debe volver a hacer el login: `aws sso login --profile sso`
*  Se puede usar un perfil de AWS al exportar su nombre a la variable de entorno AWS_PROFILE: `export AWS_PROFILE=nombrePerfil` (linux y mac) o `$env:AWS_PROFILE = “nombrePerfil”` (Windows Powershell)
*  Para autenticarse en k8s se debe exportar la ubicación del kubeconfig a la variable de entorno KUBECONFIG: `export KUBECONFIG=$HOME/.kube/${cluster_name}` (linux y mac) o `$env:KUBECONFIG = “$HOME/.kube/${cluster_name}”` (Windows Powershell)