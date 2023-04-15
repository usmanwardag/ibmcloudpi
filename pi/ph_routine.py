import ast
import json
import wiotp.sdk.application
from motors import adjust_ph
from read_ph import get_ph


def phUpdateCallback(evt):
    payload = ast.literal_eval(json.dumps(evt.data))
    ph_low = payload["low_ph"]
    ph_high = payload["high_ph"]
    print(
        f'pH update received from webapp. pH low: {ph_low}, pH high: {ph_high}')

    with open("config.json") as f:
        config = json.load(f)

    config["DESIRED_PH_LOWER"] = ph_low
    config["DESIRED_PH_UPPER"] = ph_high

    with open("config.json", "w") as f:
        json.dump(config, f)

    if config["RUNNING"] == "T":
        print('Motor is already running. So, only adjusting the pH bounds.')
    else:
        print('Motor not currently running. Starting the motor.')
        adjust_ph()


try:
    options = wiotp.sdk.application.parseConfigFile("application.yaml")
    client = wiotp.sdk.application.ApplicationClient(config=options)
    client.connect()
    client.subscribeToDeviceEvents(eventId="ph")
    client.deviceEventCallback = phUpdateCallback

    while True:
        pass

except Exception as e:
    print("Exception: ", e)
