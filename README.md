## Adapted From
https://github.com/IBM-Cloud/get-started-python

## Pre-requisites
You'll need the following:
* [IBM Cloud account](https://console.ng.bluemix.net/registration/)
* [Cloud Foundry CLI](https://github.com/cloudfoundry/cli#downloads)
* [Git](https://git-scm.com/downloads)
* [Python](https://www.python.org/downloads/)

## Clone the repository

First, clone the repository on your pi, so that you can run an application client that can listen to instructions from the web to turn the light ON or OFF.
 ```
git clone https://github.com/usmanwardag/ibmcloudpi/
 ```

Next, run the same cloning command on your PC. There, we will develop the web app and deploy it onto the IBM cloud.

## Web App Setup

To ready the web app setup, we first need to head over to the IBM cloud to create the app. 
- Head over to [cloud.ibm.com](https://cloud.ibm.com/)
- Select "Create Resource" and search for "Internet of Things Platform"
- Keep and default settings and select "Create"
- Hit "Launch"
- Select "Add Device"
- Enter device type, e.g., "RaspberryPi" (make sure there are no spaces)
- Enter a device ID which will act as a unique identified, e.g., "1"
- Click "Next"
- Leave the "Device Information" tab empty and click "Next"
- Enter an authentication token, e.g., "example_token"
- Click "Next"
- Click "Finish"
- On the top left menu, click "apps"
- Click "Generate API Key"
- Hit "Next"
- Select "Backend Trusted Application"
- Click "Generate Key"
- Note down the API Key and Authentication Token **(step A)**

Finally:
- Got back to [cloud.ibm.com](https://cloud.ibm.com/)
- From the top left menu, select [Cloud Foundry](https://cloud.ibm.com/cloudfoundry/overview)
- Select a Python runtime application under "Application Runtimes"
- Enter a unique name such as "csc543" (make sure there are no spaces) **(step B)**
- Hit "Create"

The web app setup is now ready. 

## Run client app on Pi

First, switch to the Pi code and install wiotp-sdk.
 ```
cd pi
pip3 install wiotp-sdk
 ```
Edit the `application.yaml` file.

- Enter any unique appID.
- Copy API Key from step A above.
- Copy Auth Token from step A above.

Run:
 ```
python code.py
 ```
 
You are good to go if the code doesn't return any errors.
 
## Prepare web app code

First, switch to the webapp code.
 ```
cd webapp
 ```   

Edit the `application.yaml` file.

- Enter any unique appID.
- Copy API Key from step A above.
- Copy Auth Token from step A above.

Edit the `manifest.yml` file:

- Copy name from step B above.

## Deploy web app

Deploy with the following steps:

```
ibmcloud login
```
Enter your username and password when prompted.
```
ibmcloud target --cf
ibmcloud cf push
```

If the code runs successfully, you should get a link to the web app, which you can run on browser.

  
