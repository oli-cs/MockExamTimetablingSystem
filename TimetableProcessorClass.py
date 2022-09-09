from ExamClass import Exam
from StudentClass import Student
from ExamSlotClass import ExamSlot
from EnumerationClass import ColumnEnum,FirstFieldEnum
import os
import json
from datetime import datetime,timedelta

class TimetableProcessor:
    exams = []
    students = []
    examSlots = []

    @staticmethod
    def clear():#*delete all objects when a new file is uploaded
        TimetableProcessor.exams.clear()
        TimetableProcessor.students.clear()
        TimetableProcessor.examSlots.clear()

    @staticmethod
    def getNextWeekdayDatetime(currentDatetime):
        """This method assumes that the user is not going to start an exam week when there is a bank holiday in the exam week"""
        newDatetime = currentDatetime
        while True:
            newDatetime = newDatetime + timedelta(days=1)
            if newDatetime.weekday() < 5:
                return newDatetime

    @staticmethod
    def createExamSlots(startDateTime,numberOfDays):
        """This method assumes that the user is not going to start an exam week when there is a bank holiday in the exam week"""
        TimetableProcessor.examSlots.clear()
        morningDateTime = datetime(startDateTime.year,startDateTime.month,startDateTime.day,9)
        afternoonDateTime = datetime(startDateTime.year,startDateTime.month,startDateTime.day,13)

        for i in range(numberOfDays): 
            TimetableProcessor.examSlots.append(ExamSlot(morningDateTime))
            TimetableProcessor.examSlots.append(ExamSlot(afternoonDateTime))
            morningDateTime = TimetableProcessor.getNextWeekdayDatetime(morningDateTime)
            afternoonDateTime = TimetableProcessor.getNextWeekdayDatetime(afternoonDateTime)
    
    @staticmethod
    def getJsonExamsArray():
        return [json.dumps(exam.getExamDetailsDict()) for exam in TimetableProcessor.exams] 

    @staticmethod
    def getJsonExamSlotsArray():
        return [examSlot.toJson() for examSlot in TimetableProcessor.examSlots]     

    @staticmethod
    def validateRow(firstField,row,rowType="",maxLength=9999,minLength=4):
        rowLength = len(row)
        if row[0] != firstField:
            return rowType + " row must have first value of '" + firstField + "', not '" + row[0] + "'"
        if maxLength == minLength and rowLength != maxLength:
            return rowType + " row must have exactly " + str(minLength) + " fields"
        elif rowLength > maxLength or rowLength < minLength:
            return rowType + " row must have between " + str(minLength) +  " and " + str(maxLength) + " fields"
        

    @staticmethod
    def createExamAndStudentObjects(filePath=".\\tmp\\inputFile.csv"):#only tests override the default
        if os.path.getsize(filePath) == 0:
            return "File is Empty"
        errMsg = TimetableProcessor.createExamsAndStudentsFromFile(filePath)
        if errMsg != None:
            return errMsg

    @staticmethod
    def createExamsAndStudentsFromFile(filePath=".\\tmp\\inputFile.csv"):#only tests override the default
        with open(filePath) as inputFile:
            errMsg, columnCount = TimetableProcessor.buildExams(inputFile)
            if errMsg != None:
                return errMsg
            errMsg = TimetableProcessor.buildStudents(inputFile,columnCount)
            if errMsg != None:
                return errMsg

    @staticmethod
    def buildExams(inputFile):
        headerList = inputFile.readline().replace("\n","").split(",")
        errMsg = TimetableProcessor.validateRow(FirstFieldEnum.HEADER_ROW,headerList,rowType="header")
        if errMsg != None:
            return errMsg,0
        if "" in headerList:
            return "header row must not contain empty fields",0
        rowLength = len(headerList)

        for i in range(ColumnEnum.COLUMNS_BEFORE_EXAM_DATA,len(headerList)):
            TimetableProcessor.exams.append(Exam(headerList[i]))
            
        return None,rowLength
    
    @staticmethod
    def buildStudents(inputFile,numColumns):
        reading = True
        while reading:
            try:
                line = inputFile.readline()
                line = line.replace("\n","")
                if len(line) == 0:
                    break 
                lineList = line.split(",")
                if len(lineList) != numColumns:
                    return "the following line should have " + str(numColumns) + " columns: " + str(line)

                myStudent = Student(
                    lineList[ColumnEnum.NAME_COLUMN],
                    lineList[ColumnEnum.YEAR_GROUP_COLUMN],
                    lineList[ColumnEnum.TUTOR_GROUP_COLUMN])
                TimetableProcessor.students.append(myStudent)
                for i in range(ColumnEnum.COLUMNS_BEFORE_EXAM_DATA,len(lineList)-1):
                    if lineList[i].upper() != "":
                        myExam = TimetableProcessor.exams[i-ColumnEnum.COLUMNS_BEFORE_EXAM_DATA]
                        myExam.addStudent(myStudent)
                        myStudent.addExam(myExam)
            except EOFError:
                reading = False
        if len(TimetableProcessor.students) == 0:
            return "No Students were found in the file"

    @staticmethod
    def timetableExams():
        examArray = TimetableProcessor.exams
        examSlotArray = TimetableProcessor.examSlots
        examArray.sort(key=lambda x:x.numStudents,reverse=True)#*sorts the array by the numStudents attribute of each item descending
        for exam in examArray:
            if exam.listOfStudentsIsEmpty():
                continue#jumps to the next exam if noone is taking the current one
            slotNum = -1
            foundSlotWithExams = False
            exam.numClashesPerSlotDict = {}
            for slot in examSlotArray:
                slotNum += 1
                if len(slot.listOfSubjectExams) == 0:
                    slot.listOfSubjectExams.append(exam)
                    foundSlotWithExams = False
                    break
                elif len(slot.listOfSubjectExams) > 0:
                    foundSlotWithExams = True
                    exam.numClashesPerSlotDict[slotNum] = 0#*initialises the number of clashes
                    for slotExam in slot.listOfSubjectExams:
                        numClashes, err = slotExam.getNumClashes(exam)
                        if err != None:
                            return err
                        #*slotNum must be the key because no two slots can have the same slotNum,
                        #*but two slots can have the same number of clashes
                        exam.numClashesPerSlotDict[slotNum] += numClashes#must be += or will only check clashes with the last exam in the slot
            if foundSlotWithExams:
                #turn the dictionary into (key,value) tuples and then sort based on value.
                #Find the slot with the lowest number of clashes and put the exam in that one
                sortedTupleList = sorted(exam.numClashesPerSlotDict.items(),key=lambda x:x[1])
                print(sortedTupleList)
                lowestNumClashesKey = [clashKeyAndValue[0] for clashKeyAndValue in sortedTupleList][0]
                print("--" + str(lowestNumClashesKey))
                examSlotArray[lowestNumClashesKey].addSubjectExam(exam)
        return examSlotArray