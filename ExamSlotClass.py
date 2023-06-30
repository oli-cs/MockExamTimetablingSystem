from copy import deepcopy

class ExamSlot():
    def __init__(self,datetime):
        self.datetime = datetime
        self.date, self.time = str(self.datetime).split()
        self.listOfSubjectExams = []
        self.clashes = []
    
    def addSubjectExam(self,exam):
        if exam.__class__.__name__ == "Exam":
            self.listOfSubjectExams.append(exam)
            return
        raise TypeError("ExamSlot.addSubjectExam: exam argument is not an instance of Exam:",str(exam))

    
    def toJson(self):
        self.populateClashes()
        return {"date":self.date,"time":self.time,"clashes":self.clashes,"exams":[exam.toJson() for exam in self.listOfSubjectExams]}
    
    def populateClashes(self):
        """Find out which exams clash and how many students in each exam are causing the clash"""
        myExamlist = deepcopy(self.listOfSubjectExams)
        for i in range(len(myExamlist)-1):
            for j in range(i+1,len(myExamlist)):
                numClashes = myExamlist[i].getNumClashes(myExamlist[j])[0]
                if 0 < numClashes:
                    self.clashes.append(myExamlist[i].name + "/" + myExamlist[j].name + " [" + str(numClashes) + " students]")#create display str