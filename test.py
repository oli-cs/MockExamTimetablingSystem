from TimetableProcessorClass import TimetableProcessor
import unittest
from datetime import datetime

class testcreateExamAndStudentObjects(unittest.TestCase):

    def setUp(self):
        TimetableProcessor.exams.clear()
        TimetableProcessor.students.clear()
        TimetableProcessor.examSlots.clear()
        self.maxDiff = None

    def test_emptyFile(self):
        data = TimetableProcessor.createExamAndStudentObjects("testData\\test_emptyFile.csv")
        self.assertEqual(data,"File is Empty")#expecting error message
    
    def test_firstRowShouldBeginWithFullName(self):
        data = TimetableProcessor.createExamAndStudentObjects("testData\\test_firstRowShouldBeginWithFullName.csv")
        self.assertEqual(data,"header row must have first value of 'Full Name', not 'blah'")

    def test_firstRowShouldHaveMoreThanThreeColumns(self):
        data = TimetableProcessor.createExamAndStudentObjects("testData\\test_firstRowShouldHaveMoreThanThreeColumns.csv")
        self.assertEqual(data,"header row must have between 4 and 9999 fields")

    def test_firstRowShouldNotContainBlankStrings(self):
        data = TimetableProcessor.createExamAndStudentObjects("testData\\test_firstRowShouldNotContainBlankStrings.csv")
        self.assertEqual(data,"header row must not contain empty fields")
    
    def test_noStudents(self):
        data = TimetableProcessor.createExamAndStudentObjects("testData\\test_noStudents.csv")
        self.assertEqual(data,"No Students were found in the file")

    def test_StudentRowColumnCountShouldNotBeMoreThanFirstRow(self):
        data = TimetableProcessor.createExamAndStudentObjects("testData\\test_StudentRowColumnCountShouldNotBeMoreThanFirstRow.csv")
        self.assertEqual(data,"the following line should have 26 columns: ,Year 13,13E,,,,,,,,,,,,,TRUE,,,,,TRUE,,,,,,,,,,,,,,,")
    
    def test_StudentRowColumnCountShouldNotBeLessThanFirstRow(self):
        data = TimetableProcessor.createExamAndStudentObjects("testData\\test_StudentRowColumnCountShouldNotBeLessThanFirstRow.csv")
        self.assertEqual(data,"the following line should have 26 columns: ,Year 13,13E,,,,,,,,,,,,,TRUE,,,,,TRUE,,,,")
    
    def test_happyPathExpectedExamsAndStudentsExist(self):
        data = TimetableProcessor.createExamAndStudentObjects("testData\\test_happyPathExpectedExamsAndStudentsExist.csv")
        self.assertEqual(23,len(TimetableProcessor.exams))
        self.assertEqual(6,len(TimetableProcessor.students))

    def test_createExamSlots(self):
        TimetableProcessor.createExamSlots(datetime(2021,8,12),6)
        self.assertEqual(len(TimetableProcessor.examSlots),12)
        self.assertEqual(TimetableProcessor.examSlots[0].__class__.__name__,"ExamSlot")
        self.assertEqual(str(TimetableProcessor.examSlots[0].datetime),"2021-08-12 09:00:00")
        self.assertEqual(str(TimetableProcessor.examSlots[1].datetime),"2021-08-12 13:00:00")
        self.assertEqual(str(TimetableProcessor.examSlots[2].datetime),"2021-08-13 09:00:00")
        self.assertEqual(str(TimetableProcessor.examSlots[3].datetime),"2021-08-13 13:00:00")
        #*there is a jump here because of the weekend
        self.assertEqual(str(TimetableProcessor.examSlots[4].datetime),"2021-08-16 09:00:00")
        self.assertEqual(str(TimetableProcessor.examSlots[5].datetime),"2021-08-16 13:00:00")
        self.assertEqual(str(TimetableProcessor.examSlots[6].datetime),"2021-08-17 09:00:00")
        self.assertEqual(str(TimetableProcessor.examSlots[7].datetime),"2021-08-17 13:00:00")
        self.assertEqual(str(TimetableProcessor.examSlots[8].datetime),"2021-08-18 09:00:00")
        self.assertEqual(str(TimetableProcessor.examSlots[9].datetime),"2021-08-18 13:00:00")
        self.assertEqual(str(TimetableProcessor.examSlots[10].datetime),"2021-08-19 09:00:00")
        self.assertEqual(str(TimetableProcessor.examSlots[11].datetime),"2021-08-19 13:00:00")

    def test_timetableExams(self):
        data = TimetableProcessor.createExamAndStudentObjects("testData\\test_timetablingAlgorithmTimetablesStudents.csv")
        TimetableProcessor.createExamSlots(datetime(2021,9,27),2)
        examSlots = TimetableProcessor.timetableExams()
        
        self.assertEqual(examSlots,TimetableProcessor.examSlots)
        self.assertEqual(examSlots[0].listOfSubjectExams[0].getExamDetailsDict(),
        {"name":"Biology","examLength":"","room":"","numStudents":3})
        self.assertEqual(examSlots[0].listOfSubjectExams[1].getExamDetailsDict(),
        {"name":"Physics","examLength":"","room":"","numStudents":1})
        self.assertEqual(examSlots[0].listOfSubjectExams[2].getExamDetailsDict(),
        {"name":"RE","examLength":"","room":"","numStudents":1})
        self.assertEqual(examSlots[1].listOfSubjectExams[0].getExamDetailsDict(),
        {"name":"Chemistry","examLength":"","room":"","numStudents":3})
        self.assertEqual(examSlots[2].listOfSubjectExams[0].getExamDetailsDict(),
        {"name":"Computer_Science","examLength":"","room":"","numStudents":1})
        self.assertEqual(examSlots[2].listOfSubjectExams[1].getExamDetailsDict(),
        {"name":"History","examLength":"","room":"","numStudents":3})
        self.assertEqual(examSlots[2].listOfSubjectExams[2].getExamDetailsDict(),
        {"name":"Maths","examLength":"","room":"","numStudents":3})
        self.assertEqual(examSlots[3].listOfSubjectExams[0].getExamDetailsDict(),
        {"name":"Economics","examLength":"","room":"","numStudents":1})


if __name__ == "__main__":
    unittest.main()