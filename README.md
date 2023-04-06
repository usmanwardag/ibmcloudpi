
# 1. Starting Out

## 1a. Pre-requisites
You'll need the following:
* [IBM Cloud account](https://console.ng.bluemix.net/registration/)
* [Google Cloud account](https://cloud.google.com/)
* [Google Cloud CLI](https://cloud.google.com/sdk/docs/install)
* [Git](https://git-scm.com/downloads)
* [Python](https://www.python.org/downloads/)

## 1b. Clone the repository

First, clone the repository on your Raspberry pi, so that you can run the application client that can listen to instructions from the web app to turn the light ON or OFF.
 ```
git clone https://github.com/usmanwardag/ibmcloudpi/
 ```
 
Next, run the same cloning command on your PC. There, we will develop the web app and deploy it onto the Google cloud.

# 2. Setup

There are two parts of the setup. First, we will set up the IOT Foundation service on IBM Cloud, which will allow the Raspberry Pi and our web app to communicate with each other through the MQTT protocol. Second, we will deploy the web app on Google Cloud.

## 2a. IOT Foundation Service

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

## 2b. Hosting Web App on Google Cloud

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
cf login
```
Enter your username and password when prompted.
```
cf push
```

If the code runs successfully, you should get a link to the web app, which you can run on browser.

  
