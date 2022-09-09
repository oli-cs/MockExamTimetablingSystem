class Student():
    def __init__(self,name,year,tutor_group):
        self._name = name
        self.tutorGroup = tutor_group
        self.year = year
        self._listOfExams = []
    
    def addExam(self, exam):
        if exam.__class__.__name__ == "Exam":
            self._listOfExams.append(exam)
            return
        raise TypeError("Student.addExam: exam argument is not an instance of Exam:",str(exam))

    def __str__(self):
        return "this object is an instance of 'Student'"