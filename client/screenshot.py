import requests
from base64 import b64encode
import pyscreenshot as ImageGrab
import json
import time
import os

def make_screenshot():
    im = ImageGrab.grab()
    im.save('screenshot.png')
    with open("screenshot.png", "rb") as file:
        data = file.read()
        data = b64encode(data)
    uploaded = False
    while not uploaded:
        try:
            r = requests.post('https://127.0.0.1:5000/upload_screenshot', json={'data': data.decode("utf-8")}, verify=False)
            uploaded = True
        except:
            time.sleep(1)

def do_expressvpn(commands):
    if commands["expressvpn_connect"]:
        command_list = ["echo anzhe990206 | sudo -S systemctl restart expressvpn", "expressvpn connect"]
    elif commands["expressvpn_disconnect"]:
        command_list = ["expressvpn disconnect", "echo 4869221B | sudo -S systemctl restart NetworkManager.service"]
    elif commands["expressvpn_status"]:
        command_list = ["expressvpn status"]
    else:
        return
    print("***********************\n************\n**************\n")
    # print(command_list)
    output = ""
    for command in command_list:
        print(command)
        output += os.popen(command).read()+"\n\n\n"
        time.sleep(3)
    # output, error = process.communicate()
    json_data = {"data": output}
    uploaded = False
    print(json_data)
    while not uploaded:
        try:
            r = requests.post('https://127.0.0.1:5000/expressvpn_connected', json=json_data, verify=False)
            uploaded = True
        except:
            time.sleep(1)

def wait_commands():
    while True:
        try:
            r = requests.get('https://127.0.0.1:5000/get_commands', verify=False)
            if json.loads(json.loads(r.content))["screenshot"]:
                print("***********************")
                make_screenshot()
            do_expressvpn(json.loads(json.loads(r.content)))
            time.sleep(1)
        except:
            time.sleep(1)
        

if __name__ == "__main__":
    wait_commands()
