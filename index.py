import re
import http.server
import socketserver
import requests
from datetime import date
import csv

f = open('index.html', 'w')


html_template = """<html>
  <head>
    <title>Title</title>
  </head>
  <body>
    <h2>Site de la mairie trop bien fait</h2>
    <ul>
"""

def headRequest():
    url = "https://storage.googleapis.com/mollusques-caen/data.csv"
    # En-têtes pour spécifier la plage de bytes
    response = requests.head(url)
    return int(response.headers.get('Content-Length'))

def getData(): 
    global html_template
    url = "https://storage.googleapis.com/mollusques-caen/data.csv"
    # En-têtes pour spécifier la plage de bytes
    range_requests = "bytes=" + str(headRequest() - 32 * 24) + "-" + str(headRequest())
    headers = {"Range": range_requests}
    # Faire la requête GET avec la plage de bytes
    response = requests.get(url, headers=headers)
    if response.status_code == 206 :
        rows = response.text.splitlines()
        generateCurrentMark(rows)
        html_template += """
        </ul>
        </body> 
        </html> """
        
    return html_template

def generateCurrentMark( rows):
    global html_template
    html_template += "<p> La note du " + str(date.today) + "est de " + averageDay(rows)
            
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
        

getData()
# writing the code into the file 
f.write(html_template) 

# close the file 
f.close() 

PORT = 8080
Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
    
