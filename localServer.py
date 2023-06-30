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

        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST'}
        )
        if "filename" in form:
            TimetableProcessor.clear()#clear object arrays
            print("filename is in form")
            fileitem = form["filename"]
            message = None

            if len(fileitem.filename) > 0:#test if file was uploaded
                print("filename length > 0")
                print(fileitem.filename)
                # strip leading path from file name to avoid 
                # directory traversal attacks
            try:
                print("creating the directory")
                fn = os.path.basename(fileitem.filename)
                if not os.path.isdir(".\\tmp"):
                    os.makedirs(".\\tmp")
                with open(SimpleHttpRequestHandlerWithPost.SAVE_FILE_PATH, "wb") as myFile:
                    print("writing the file to the directory")
                    myFile.write(fileitem.file.read())
            except BaseException as error:
                message = self.__getErrorJson("Could not write file: " + error.message)
            
            if message == None:
                print("no errors so far")
                try:
                    message = TimetableProcessor.createExamAndStudentObjects(SimpleHttpRequestHandlerWithPost.SAVE_FILE_PATH)
                    if message != None:
                        print("creating objects failed")
                        message = self.__getErrorJson(message)
                except BaseException as error:
                    print("file processing not possible")
                    message = self.__getErrorJson("Could not process file: " + error.message)
            
            if message == None:
                print("getting list of exams")
                if "startDate" in form:
                    startDate = form.getvalue("startDate")
                    print("startDate: " + str(startDate))
                    startDate = startDate.split("-")#makes a list [year,month,day]
                    startDatetime = datetime(int(startDate[0]),int(startDate[1]),int(startDate[2]))
                    if "mockExamSeriesLengthInDays" in form:
                        examSeriesLength = int(form.getvalue("mockExamSeriesLengthInDays"))
                        print("examSeriesLength: " + str(examSeriesLength))
                        message = self.__getTimetableJson(fn,startDatetime,examSeriesLength)
                        responseCode = 200# OK
                    else:
                        message = self.__getErrorJson("length of exam series was not supplied")
                else:
                    message = self.__getErrorJson("start date was not supplied")
            
            print("send json response: ",message)

            self._send_response_data(responseCode,msg=message)

PORT = 80

try:
    with socketserver.TCPServer(("",PORT),SimpleHttpRequestHandlerWithPost) as httpd:
        print("serving at port " + str(PORT))
        httpd.serve_forever()
except BaseException as e:
    print(e.message)