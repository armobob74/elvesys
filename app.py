from flask import Flask, request, render_template, redirect
from pman import pman
from flask_cors import CORS
from ob1_control import ob1_state_control
from mux_control import mux_state_control
from dist_control import dist_state_control
import pdb
app = Flask(__name__)
CORS(app)
app.register_blueprint(pman, url_prefix='/pman')

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/mux", methods=["GET", "POST"])
def mux():
    if request.method == "POST":
        com_port_mux = request.form["com_port"]
        curr_state = [int(request.form[f"curr_state_{i}"]) for i in range(8)]
        desired_state = [int(request.form[f"desired_state_{i}"]) for i in range(8)]
        mux_state_control(com_port_mux, curr_state, desired_state)
    return render_template("mux.html")

@app.route("/ob1", methods=["GET", "POST"])
def ob1():
    if request.method == "POST":
        com_port_ob1 = request.form["com_port_ob1"]
        channel_to_initialize = int(request.form["channel_to_initialize"])
        pressure_to_set = float(request.form["pressure_to_set"])
        ob1_state_control(com_port_ob1, channel_to_initialize, pressure_to_set)
    return render_template("ob1.html")

@app.route("/dist", methods=["GET", "POST"])
def dist():
    if request.method == "POST":
        com_port_dist = request.form["com_port_dist"]
        initial_channel = int(request.form["initial_channel"])
        final_channel = int(request.form["final_channel"])
        dist_state_control(com_port_dist, initial_channel, final_channel)
    return render_template("dist.html")

if __name__ == "__main__":
    app.run(debug=True, port = 5059)
