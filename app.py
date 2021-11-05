from flask import Flask, render_template, send_from_directory
import json
app = Flask(__name__)
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/test.json")
def music_json_current_tracks():
    f = open('test.json')
    data = json.load(f)
    return data