class Exam():
    def __init__(self,name):
        self.name = name
        self.examLength = ""
        self.room = ""
        self._listOfStudents = []
        self.numClashesPerSlotDict = {}
        self.numStudents = len(self._listOfStudents)
    
    
    def updateNumStudents(self):
        self.numStudents = len(self._listOfStudents)
    

    def addStudent(self, student):
        if student.__class__.__name__ == "Student":
            self._listOfStudents.append(student)
            self.updateNumStudents()
            return
        raise TypeError("Exam.addStudent: student argument is not an instance of Student:",str(student))

    def getExamDetailsDict(self):
        return {"name":self.name,
        "examLength":self.examLength,
        "room":self.room,
        "numStudents":self.numStudents}
    
    def toJson(self):
        return self.getExamDetailsDict()

    def addExamLength(self,examLength):
        self.examLength = examLength
    
    def addRoom(self,room):
        self.room = room

    def getNumClashes(self,exam):
        if isinstance(exam,Exam):
            clashes = set(self._listOfStudents).intersection(set(exam._listOfStudents))
            return len(clashes), None
        else:
            return None, "parameter supplied is not an Exam object"
    
    def listOfStudentsIsEmpty(self):
        if self._listOfStudents == []:
            return True
        return False

    def __str__(self):
        return "this object is an instance of 'Exam'"
