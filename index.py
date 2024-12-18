import re
import http.server
import socketserver
import requests
from datetime import date
from flask import Flask

app = Flask(__name__)

f = open('index.html', 'w')


def headRequest():
    url = "https://storage.googleapis.com/mollusques-caen/data.csv"
    # En-têtes pour spécifier la plage de bytes
    response = requests.head(url)
    return int(response.headers.get('Content-Length'))

def getData(): 
    url = "https://storage.googleapis.com/mollusques-caen/data.csv"
    # En-têtes pour spécifier la plage de bytes
    range_requests = "bytes=" + str(headRequest() - 32 * 24) + "-" + str(headRequest())
    headers = {"Range": range_requests}
    # Faire la requête GET avec la plage de bytes
    response = requests.get(url, headers=headers)
    data = 0
    if response.status_code == 206 :
        rows = response.text.splitlines()
        data = averageDay(rows)
        
    return data

def generateCurrentMark( rows):
    return "<p> La test du 23/11/2001" + str(date.today) + "est de " + averageDay(rows)
            
def getRowData(row):
    pattern = r"^(.*?),(.*)$"
    match = re.match(pattern, row)
    timestamp = match.group(1)  # First group: timestamp
    value = float(match.group(2))
    
    return [timestamp, value]

def averageDay(rows):
    mark = 0
    for row in rows: 
        data = getRowData(row)
        mark += round(data[1]/2)
    return str(round(mark / 24))

@app.route("/api")
def dataApi():
    return "<p>Hello, World!</p>"

@app.route("/")
def homepage():  
    return "<p> La note du " + "est de " + getData() + "</p>"

# close the file 
f.close() 
