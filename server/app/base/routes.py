# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from flask import jsonify, render_template, redirect, request, url_for
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user
)

from app import db, login_manager
from app.base import blueprint
from app.base.forms import LoginForm, CreateAccountForm
from app.base.models import User

from app.base.util import verify_pass

from datetime import datetime, date, timedelta
import json
import os
import os.path
import base64
import copy

@blueprint.route('/')
def route_default():
    return redirect(url_for('base_blueprint.login'))

@blueprint.route('/page_<error>')
def route_errors(error):
    return render_template('errors/page_{}.html'.format(error))

## Login & Registration

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    # print("***********")
    # print([*request.form.keys()])
    # print(current_user)
    # print(login_form)
    # print("***********")
    if 'login' in request.form:
        
        # read form data
        username = request.form['username']
        password = request.form['password']

        # Locate user
        user = User.query.filter_by(username=username).first()
        
        # Check the password
        if user and verify_pass( password, user.password):

            login_user(user)
            return redirect(url_for('base_blueprint.route_default'))

        # Something (user or pass) is not ok
        return render_template( 'login/login.html', msg='Wrong user or password', form=login_form)

    if not current_user.is_authenticated:
        return render_template( 'login/login.html',
                                form=login_form)
    return redirect(url_for('home_blueprint.index'))

@blueprint.route('/create_user', methods=['GET', 'POST'])
def create_user():
    login_form = LoginForm(request.form)
    create_account_form = CreateAccountForm(request.form)
    if 'register' in request.form:

        username  = request.form['username']
        email     = request.form['email'   ]

        user = User.query.filter_by(username=username).first()
        if user:
            return render_template( 'login/register.html', msg='Username already registered', form=create_account_form)

        user = User.query.filter_by(email=email).first()
        if user:
            return render_template( 'login/register.html', msg='Email already registered', form=create_account_form)

        # else we can create the user
        user = User(**request.form)
        db.session.add(user)
        db.session.commit()

        return render_template( 'login/register.html', success='User created please <a href="/login">login</a>', form=create_account_form)

    else:
        return render_template( 'login/register.html', form=create_account_form)

@blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('base_blueprint.login'))

@blueprint.route('/shutdown')
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return 'Server shutting down...'

## Errors

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('errors/page_403.html'), 403

@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('errors/page_403.html'), 403

@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('errors/page_404.html'), 404

@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('errors/page_500.html'), 500

@blueprint.route('/testsss', methods=['GET'])
def testsss():
    a = datetime.now()
    b = {"time": a}
    return jsonify("<h2>"+str(a)[:len(str(a))-7]+"</h2>")

@blueprint.route('/index_1')
def index_1():
    return render_template('index_1.html')

@blueprint.route('/video_list', methods=['GET', 'POST'])
def video_list():
    # print("************")
    # print(request.json["type"])
    # print("************")
    # a = datetime.now()
    # b = {"time": a}
    if request.json["type"] == "current_list":
        filename = date.today().strftime("%Y%m%d")+".json"
        try:
            with open(filename) as file:
                json_data = json.load(file)
        except:
            json_data = {"videos": []}
        for video in json_data["videos"]:
            video["status"] = "Unplayed"
        print(json_data)
        with open("finished.txt") as file:
            finished_index = int(file.read())
        with open("current_time.txt") as file:
            current_time = int(file.read())
        with open("duration.txt", "w") as file:
            file.write(json_data["videos"][finished_index]["duration"])
        with open("name.txt", "w") as file:
            file.write(json_data["videos"][finished_index]["name"])
        for i in range(finished_index):
            json_data["videos"][i]["status"] = "Played"
        json_data["videos"][finished_index]["status"] = "Playing: " + str(int(current_time*1.0/int(json_data["videos"][finished_index]["duration"])*100)) + "%"
    else:
        filename = request.json["type"]+".json"
        try:
            with open(filename) as file:
                json_data = json.load(file)
        except:
            json_data = {"videos": []}
        print(json_data)
    for video in json_data["videos"]:
        video["duration"] = GetTime(video["duration"])
    return jsonify(json_data)

@blueprint.route('/video_lists', methods=['GET', 'POST'])
def video_lists():
    if request.json["type"] == "pending":
        filename = "playlists.json"
        try:
            with open(filename) as file:
                json_data = json.load(file)
            print(json_data)
            today = date.today().strftime("%Y%m%d")
            index = get_index(json_data["playlists"], "name", today)
            if index == []:
                index = len(json_data["playlists"])
            else:
                index = index[0]
            print(index)
            json_data["playlists"] = json_data["playlists"][index:]
            print("*********")
            print(json_data)
        except Exception as e:
            print(e)
            json_data = {"playlists": []}
        print(json_data)
    else:
        filename = "playlists.json"
        try:
            with open(filename) as file:
                json_data = json.load(file)
            print(json_data)
            today = date.today().strftime("%Y%m%d")
            index = get_index(json_data["playlists"], "name", today)
            if index == []:
                index = len(json_data["playlists"])
            else:
                index = index[0]
            print(index)
            json_data["playlists"] = json_data["playlists"][:index]
        except Exception as e:
            print(e)
            json_data = {"playlists": []}
        print(json_data)
    for playlist in json_data["playlists"]:
        playlist["duration"] = GetTime(playlist["duration"])
    return jsonify(json_data)

@blueprint.route('/upload_data', methods=['GET', 'POST'])
def upload_data():
    print("*******************")
    print(request.form)
    filename = request.form["filename"]
    data = request.form["content"]
    data_line = data.split("\n")
    videos = {"videos": []}
    for line in data_line:
        if line == "":
            del line
        else:
            details = line.split("/###/")
            videos["videos"].append({"name": details[0], "duration": ToTime(details[1]), "url": details[2]})
    duration = 0
    for video in videos["videos"]:
        duration += int(video["duration"])
    with open(filename+".json", "w") as file:
        json.dump(videos, file)
    with open("playlists.json") as file:
        playlists = json.load(file)
    playlists["playlists"].append({"name": filename, "duration": str(duration)})
    with open("playlists.json", "w") as file:
        json.dump(playlists, file)
    # if request.json["type"] == "pending":
    #     filename = "playlists.json"
    #     try:
    #         with open(filename) as file:
    #             json_data = json.load(file)
    #     except:
    #         json_data = {"playlists": []}
    #     print(json_data)
    #     return jsonify(json_data)
    return redirect("/upload")

@blueprint.route('/update_list', methods=['GET', 'POST'])
def update_list():
    filename = request.json["filename"]
    try:
        json_data = {"videos": request.json["data"]}
        for video in json_data["videos"]:
            video["duration"] = ToTime(video["duration"])
        with open(filename+".json", "w") as file:
            json.dump(json_data, file)
        duration = 0
        for video in json_data["videos"]:
            duration += int(video["duration"])
        with open("playlists.json") as file:
            playlists = json.load(file)
        index = get_index(playlists["playlists"], "name", filename)[0]
        playlists["playlists"][index]["duration"] = duration
        with open("playlists.json", "w") as file:
            json.dump(playlists, file)
    except Exception as e:
        print(e)
    return jsonify({"duration": GetTime(duration)})

@blueprint.route('/current_get', methods=['GET', 'POST'])
def current_get():
    with open("finished.txt") as file:
        finished_index = int(file.read())
    with open("current_time.txt") as file:
        current_time = int(file.read())
    with open("duration.txt") as file:
        duration = file.read()
        if duration == "":
            duration = 999
        else:
            duration = int(duration)
    with open("name.txt") as file:
        name = file.read()
    if request.json["type"] == "normal":
        return jsonify({"index": finished_index, "current_time": current_time, "duration": duration, "name": name})
    else:
        return jsonify({"index": finished_index, "current_time": GetTime(current_time), "duration": GetTime(duration), "name": name})

@blueprint.route('/finished', methods=['GET', 'POST'])
def finished():
    with open("finished.txt") as file:
        finished_index = int(file.read())
    with open("current_time.txt", "w") as file:
        file.write("0")
    today = date.today().strftime("%Y%m%d")
    with open(today+".json") as file:
        json_data = json.load(file)
    length = len(json_data["videos"])
    if finished_index+1 >= length:
        finished_index = -1
    with open("finished.txt", "w") as file:
        file.write(str(finished_index+1))
    return jsonify("")

@blueprint.route('/update_current', methods=['GET', 'POST'])
def update_current():
    with open("current_time.txt", "w") as file:
        file.write(str(request.json["current_time"]))
    return jsonify("")

@blueprint.route('/receive_commands', methods=['GET', 'POST'])
def receive_commands():
    with open("commands.json") as file:
        commands = json.load(file)
    for command in commands.keys():
        if "do" in request.json:
            if request.json["do"]:
                if command in request.json:
                    commands[command] = True
                else:
                    commands[command] = False    
        else:
            if command in request.json:
                commands[command] = True
            else:
                commands[command] = False
    print("1111111111111111")
    print(commands)
    with open("commands.json", "w") as file:
        json.dump(commands, file)
    if "screenshot" in request.json:
        with open("screenshot.txt") as file:
            data = file.read()
            data = data.replace("False", "")
            status = bool(data)
        print(status)
        if status:
            print("***************************")
            with open("screenshot.txt", "w") as file:
                file.write("False")
            print("***************************")
            return jsonify({"status": True})
        else:
            return jsonify({"status": False}) 
    else:
        return jsonify({"status": False})

@blueprint.route('/get_commands', methods=['GET', 'POST'])
def get_commands():
    with open("commands.json") as file:
        commands = json.load(file)
        commands_temp = copy.deepcopy(commands)
    for command in commands_temp.keys():
        commands_temp[command] = False
    with open("commands.json", "w") as file:
         json.dump(commands_temp, file)
    # for command in commands.keys():
    #     if commands[command]:
    #         commands[command] = "true"
    #     else:
    #         commands[command] = "false"
    commands = json.dumps(commands)
    print(commands)
    return jsonify(commands)

@blueprint.route('/upload_screenshot', methods=['GET', 'POST'])
def upload_screenshot():
    data = request.json["data"]
    data = base64.b64decode(data)
    print("asdsadsadasdsadsadsadasdasdasd")
    with open("app/base/static/screenshot.png", "wb") as file:
        file.write(data)
    print("#######################")
    with open("screenshot.txt", "w") as file:
        file.write("True")
    return jsonify("")

@blueprint.route('/expressvpn_connected', methods=['GET', 'POST'])
def expressvpn_connected():
    data = request.json["data"]
    # data = base64.b64decode(data)
    # print("asdsadsadasdsadsadsadasdasdasd")
    # with open("app/base/static/screenshot.png", "wb") as file:
        # file.write(data)
    with open("expressvpn_output.txt", "w") as file:
        file.write(data)
    result = os.popen("cat expressvpn_output.txt | sh ansi2html.sh > expressvpn_output.html").read()
    # result = os.popen("cat expressvpn_output.txt").read()
    # print(result)
    with open("expressvpn_output.html") as file:
        data = file.read()
    # print(data)
    data = data[data.index("<pre>"): data.index("</pre>")+6]
    with open("expressvpn_output.txt", "w") as file:
        file.write(data)
    with open("expressvpn.txt", "w") as file:
        file.write("True")
    return jsonify("")

@blueprint.route('/expressvpn_wait', methods=['GET', 'POST'])
def expressvpn_wait():
    with open("expressvpn.txt") as file:
        status = bool(file.read().replace("False", ""))
    if status:
        with open("expressvpn_output.txt") as file:
            output = file.read()
        with open("expressvpn.txt", "w") as file:
            file.write("False")
        return jsonify({"status": True, "output": output})
    else:
        return jsonify({"status": False})

def get_index(list, key, value):
    return [list.index(cdict) for cdict in list if cdict[key] == value]

def GetTime(seconds):
    sec = timedelta(seconds=int(seconds))
    d = datetime(1,1,1) + sec
    result = ""
    if d.hour > 0:
        result += str(d.hour)+" hours"
    if d.minute > 0:
        result += str(d.minute)+" minutes"
    if d.second >= 0:
        result += str(d.second)+" seconds"
    result = result.replace("hours", "hours ")
    result = result.replace("minutes", "minutes ")
    return result

def ToTime(time):
    result = 0
    if "hou" in time:
        result += int(time[:time.index("hou")])*60*60
        time = time[time.index("hou")+5:]
    if "min" in time:
        result += int(time[:time.index("min")])*60
        time = time[time.index("min")+7:]
    if "sec" in time:
        result += int(time[:time.index("sec")])
        time = time[time.index("sec")+7:]
    try:
        result += int(time)
    except:
        pass
    return str(result)