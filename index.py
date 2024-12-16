import re
import http.server
import socketserver
import requests
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

def getCsv(): 
    url = "https://storage.googleapis.com/mollusques-caen/data.csv"
    # En-têtes pour spécifier la plage de bytes
    headers = {"Range": "bytes=252240-252270"}

    # Faire la requête GET avec la plage de bytes
    response = requests.get(url, headers=headers)
    if response.status_code == 206 :
        return csv.reader(response.text)
        
def printLine(line, html_template):
    pattern = r"^(.*?),(.*)$"
    match = re.match(pattern, line[2])
    if match:
        timestamp = match.group(1)  # First group: timestamp
        value = float(match.group(2))

    html_template += "<li> Date : "  + timestamp + " Note : " + str(round(value/2))  + "</li>"
    return html_template


for row in getCsv():
    printLine(row, html_template)
    html_template += """
    </ul>
    </body> 
    </html> 
    """

# writing the code into the file 
f.write(html_template) 

# close the file 
f.close() 

PORT = 8080
Handler = http.server.SimpleHTTPRequestHandler

spamreader = []


with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
    
