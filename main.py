import flask
import requests
from flask import request, jsonify, render_template, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import csv
import json
import io
app = flask.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask_db.db'
db = SQLAlchemy(app)


class FileContents(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300))
    data = db.Column(db.LargeBinary)


@app.route('/', methods=['GET'])
def home():
    return render_template('uploadFile.html')


@app.route('/modelscore', methods=['GET'])
def score():
    url = "http://localhost:5000/api/v1/bicycletheft/getAttributes"
    r = requests.get(url)
    print(r.json())
    return render_template('scores.html', attributes=r.json())


@app.route('/download', methods=['GET'])
def renderDownload():
    return render_template('download.html')


@app.route('/download', methods=['POST'])
def download():
    return send_from_directory("D:/STUDY/SEM 5/COMP309/Group Project", "userOutputFile.csv", as_attachment=True)


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['inputFile']
    newFile = FileContents(name=file.filename, data=file.read())
    jsonFilePath = 'D:/STUDY/SEM 5/COMP309/Group Project/data.txt'
    # call api
    csvFile = io.StringIO(newFile.data.decode('utf-8'))
    # read csv file and add to data
    data = {}
    # with open(newFile.name) as csvFile1:
    csvReader = csv.DictReader(csvFile)
    for rows in csvReader:
        id = rows['Index_']
        data[id] = rows

    with open(jsonFilePath, 'w') as jsonFile:
        jsonFile.write(json.dumps(data))

    f = open(jsonFilePath,)
    data = json.load(f)
    url = "http://localhost:5000/api/v1/bicycletheft/predict"
    requests.post(url, json=data)
    return render_template("download.html")


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5001)
