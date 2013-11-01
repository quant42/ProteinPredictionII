#! /usr/bin/env python

# imports
import socket, urllib, time

# general settings and constants
NCBI_BLAST_HOST = "www.ncbi.nlm.nih.gov"
NCBI_BLAST_PATH_SEND = "/blast/Blast.cgi"
NCBI_BLAST_PATH_SEND_PARAMS = "CMD=PUT&PROGRAM=blastp&DATABASE=nr&QUERY=%s"
NCBI_BLAST_PATH_WAIT = "/blast/Blast.cgi?CMD=Get&FORMAT_OBJECT=SearchInfo&RID=%s"
NCBI_BLAST_PATH_RESULTS = "/blast/Blast.cgi?CMD=Get&FORMAT_TYPE=Text&RID=%s"

NCBI_BLAST_MINTIMEOUT_MS = 2000

GENERAL_HTTP_POST_REQUEST  = "POST %s HTTP/1.0\r\n"
GENERAL_HTTP_POST_REQUEST += "Host: %s\r\n"
GENERAL_HTTP_POST_REQUEST += "Content-Length: %s\r\n"
GENERAL_HTTP_POST_REQUEST += "Content-Type: application/x-www-form-urlencoded\r\n"
GENERAL_HTTP_POST_REQUEST += "Connection: close\r\n"
GENERAL_HTTP_POST_REQUEST += "\r\n"

GENERAL_HTTP_GET_REQUEST  = "GET %s HTTP/1.0\r\n"
GENERAL_HTTP_GET_REQUEST += "Host: %s\r\n"
GENERAL_HTTP_GET_REQUEST += "Accept: text/html, */*"
GENERAL_HTTP_GET_REQUEST += "Connection: close\r\n"
GENERAL_HTTP_GET_REQUEST += "\r\n"

# functions

# this function sends an ncbi blast request
# and returns a tuple(query Id from with which the results can be fetched later, approximate time to wait for the blasting results)
# if nothing was given by ncbi, they are None
def sendNcbiBlastRequest(blastRequest):
  global NCBI_BLAST_HOST, NCBI_BLAST_PATH_SEND, NCBI_BLAST_PATH_WAIT, NCBI_BLAST_PATH_RESULTS, NCBI_BLAST_MINTIMEOUT_MS, GENERAL_HTTP_POST_REQUEST, GENERAL_HTTP_GET_REQUEST
  # build query
  httpRequestQuery = NCBI_BLAST_PATH_SEND_PARAMS % blastRequest
  # build a socket, connect to ncbi and send the request
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect((NCBI_BLAST_HOST, 80))
  s.send(GENERAL_HTTP_POST_REQUEST % (NCBI_BLAST_PATH_SEND, NCBI_BLAST_HOST, len(httpRequestQuery)))
  s.send(httpRequestQuery)
  # ok, now get the html
  html, rid, rtoe = "", None, None
  while True:
    data = s.recv(1024)
    if len(data) == 0:
      break
    html += data
  # ok parse html
  html = html.split('\n')
  for htmlLine in html:
    if htmlLine.find("    RID = ") != -1:
      rid = htmlLine[htmlLine.find("=") + 1:].strip()
    elif htmlLine.find("    RTOE = ") != -1:
      rtoe = htmlLine[htmlLine.find("=") + 1:].strip()
  # in the end close the socket connection
  s.close()
  return (rid, rtoe)

# this function check, if the requested blast search is ready, and might be fetched
def checkIfNcbiBlastRequestIsReads(rid):
  global NCBI_BLAST_HOST, NCBI_BLAST_PATH_SEND, NCBI_BLAST_PATH_WAIT, NCBI_BLAST_PATH_RESULTS, NCBI_BLAST_MINTIMEOUT_MS, GENERAL_HTTP_POST_REQUEST, GENERAL_HTTP_GET_REQUEST
  # build a socket, connect to ncbi and send the request
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect((NCBI_BLAST_HOST, 80))
  s.send(GENERAL_HTTP_GET_REQUEST % (NCBI_BLAST_PATH_WAIT % rid, NCBI_BLAST_HOST))
  # ok, now get the html
  html, result = "", False
  while True:
    data = s.recv(1024)
    if len(data) == 0:
      break
    html += data
  # ok parse html
  html = html.split('\n')
  for htmlLine in html:
    if htmlLine.find("Status=WAITING") != -1:
      break                                    # not ready yet
    elif htmlLine.find("Status=READY") != -1:
      result = True                            # cool
      break
  # in the end close the socket connection
  s.close()
  return result

def getNcbiBlastResultString(rid):
  global NCBI_BLAST_HOST, NCBI_BLAST_PATH_SEND, NCBI_BLAST_PATH_WAIT, NCBI_BLAST_PATH_RESULTS, NCBI_BLAST_MINTIMEOUT_MS, GENERAL_HTTP_POST_REQUEST, GENERAL_HTTP_GET_REQUEST
  # build a socket, connect to ncbi and send the request
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect((NCBI_BLAST_HOST, 80))
  s.send(GENERAL_HTTP_GET_REQUEST % (NCBI_BLAST_PATH_RESULTS % rid, NCBI_BLAST_HOST))
  # ok, now get the html
  html = ""
  while True:
    data = s.recv(1024)
    if len(data) == 0:
      break
    html += data
  return html

print "sending request ..."
request = sendNcbiBlastRequest("NWLGVKRQPLWTLVLILWPVIIFIILAITRTKFPP")
print "rid: %s rtoe: %s" % request
ready = checkIfNcbiBlastRequestIsReads(request[0])
print "result readyness: %s" % ready
time.sleep(float(request[1]))
print "check result ready ..."
ready = False
while not checkIfNcbiBlastRequestIsReads(request[0]):
  time.sleep(5)
print "result readyness: %s" % ready
print "Fetch results ..."
f = open("~/blast.txt", 'w+')
f.write(getNcbiBlastResultString(request[0]))
f.close()

