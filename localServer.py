import http.server
import socketserver
import os
import cgi
import json
from TimetableProcessorClass import TimetableProcessor
from datetime import datetime

class SimpleHttpRequestHandlerWithPost(http.server.SimpleHTTPRequestHandler):
    SAVE_FILE_PATH = ".\\tmp\\inputFile.csv"

    def _send_response_data(self,responseCode,msg=None):
        self.send_response(responseCode,message=msg)
        self.end_headers()
        self.wfile.write(bytes(msg,"utf-8"))#payload

    
    def __getErrorJson(self,errorDesc):
        return json.dumps({"error":errorDesc})
    

    def __getTimetableJson(self,filename,startDatetime,lengthOfExamSeriesInDays):
        TimetableProcessor.createExamSlots(startDatetime,lengthOfExamSeriesInDays)
        TimetableProcessor.timetableExams()
        timetable = TimetableProcessor.getJsonExamSlotsArray()
        return json.dumps({"success":"The file " + filename + " was uploaded successfully",
                            "timetable":timetable})
    

    def do_POST(self):
        print("POST called")
        responseCode = 452# default response code is fail
        message = ""
        messageBodyLength = int(self.headers["Content-Length"])
        messageBody = json.loads(self.rfile.read(messageBodyLength))
        #!split message body into exams+students, rooms+capacities, and exams+examlengths
        #!create objects based on data
        #!redesign algorithm to take into account room capacities and exam lengths when calculating clashes
        #!incorporate room and exam length into output

       
        
        print("send json response: ",message)

        self._send_response_data(responseCode,msg=message)

PORT = 80

try:
    with socketserver.TCPServer(("",PORT),SimpleHttpRequestHandlerWithPost) as httpd:
        print("serving at port " + str(PORT))
        httpd.serve_forever()
except BaseException as e:
    print(e.message)