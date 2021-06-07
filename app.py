from flask import Flask, render_template, request, json,jsonify
import os
from flask.wrappers import Response
import yaml
import joblib
import numpy as np
from src.models.predict_model import predict, form_response, api_response

webapp_root = "webapp"
static_dir = os.path.join(webapp_root, "static")
template_dir = os.path.join(webapp_root, "templates")
from src.data.make_dataset import read_params

app = Flask(__name__, static_folder=static_dir, template_folder=template_dir)

@app.route("/", methods={"GET", "POST"})
def index():
    if request.method == "POST":
        try:
            if request.form:
                data_req = dict(request.form)                
                response = form_response(data_req)
                return render_template('index.html',response=response)
            elif request.json:
                response = api_response(request.json)
                return jsonify(response)
        except Exception as e:
            print(e)
            # error = {"error": "Something went wrong!! Try again later!"}
            # error = {"error": e}
            return render_template("404.html",error=e)
    else:
        return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
