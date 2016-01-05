## Kevin Coe         
## kcoe3@gatech.edu  
## This code loads a .csv file with list of available class times and uses a greedy
## algorithm to choose a class schedule starting with either the class with the most 
## possible meeting times (max) or fewest possible meeting times (min)
## Output: .txt file with created class schedule

## For testing, use courseTimes.csv as input file


from Tkinter import *
import tkFileDialog as filedialog
from csv import *

class HW6:

# __init__
    def __init__(self,master):
        self.courses = {}
        self.fileName=''
        
        frame = Frame(master)
        frame.pack()
        
        #Row 0
        self.CoursesFilesText = Label(frame, text = "Courses file:")
        self.CoursesFilesText.grid(row = 0, column=0, sticky = E)

        self.Directory = Entry(frame, width= 60)
        self.Directory.config(state = "readonly")
        self.Directory.grid(row=0, column=1, columnspan=2, sticky = W)

        self.DirectoryButton = Button(frame, text = "Select File", command = self.openFileClicked)
        self.DirectoryButton.grid(row=0, column=3,sticky=W)

        #Row 1 to Row 3
        self.SchedulingModeText = Label(frame, text = " Scheduling Mode:")
        self.SchedulingModeText.grid(row=1, column = 0, sticky = E)

        # creates second frame
        frame2 = Frame(frame, height = 42, width = 59)
        frame2.grid(row=1, column=1, columnspan = 2,sticky = W)
        frame2.config(borderwidth=1)
        frame2.config(relief=SUNKEN)
        #frame2.grid_configure(columnspan=2)
        
        # radio buttons
        self.IV = IntVar()
        self.Max = Radiobutton(frame2, text = "Max", variable = self.IV, value = 2)
        self.Max.grid(row = 0, column= 0, sticky = W)
 
        self.IVmin = IntVar()
        self.Min = Radiobutton(frame2, text = "Min", variable = self.IV, value = 1)
        self.Min.grid(row=1, column=0, sticky = W)

        self.resultText = Label(frame2, width = 59, text = "...")
        self.resultText.grid(row=2, column=0, columnspan = 2, sticky = W)

        #Row 4
        self.ComputeButton = Button(frame, text = "Compute and Save Results", width = 84, command = self.computeNSaveClicked)
        self.ComputeButton.grid(row=4, column = 0, sticky = W, columnspan = 4)
        
        
        
# openFileClicked
    def openFileClicked(self):
        #open it
        self.fileName = filedialog.askopenfilename()
            
        #updateDirectory
        self.Directory.config(state = NORMAL)
        self.Directory.delete(0,END)
        self.Directory.insert(0, self.fileName)
        self.Directory.config(state = "readonly")
##        return fileName


#doesOverlap
    def doesOverlap(self, tuple1, tuple2):
##        print(tuple1)
##        print(tuple2)
        if (tuple2[1] - tuple2[0]) >= (tuple1[1] - tuple1[0]):
            long = tuple2
            short = tuple1
        else:
            long = tuple1
            short = tuple2
        # checks if shorter class end time is between longer class beginning and end
        # or if shorter class start time is between longer class beginning and end
        if ((short[0] < long[1]) & (short[0] > long[0])) | ((short[1] > long[0]) & (short[1] < long[1])):
            return True
        else:
            return False

    def makeScheduleMin(self):
##        print(self.courses)
        # assume self.courses has all the courses in it
        keys = list(self.courses)
        # loops to create a list of lengths that go with each key
        lengths = []
        schedule = []
        for i in range(0, len(keys)):
            lengths.append(len(self.courses[keys[i]]))
            
        sortedlengths = sorted(lengths)
        for x in sortedlengths:        
            # index of class with most meeting times:
            maxInd = lengths.index(x)
            maxKey = keys[maxInd]
##            print('maxInd:', maxInd)
##            print('maxKey:', maxKey)
            i = 0
##            print('Length through loop:', x)
            while i < len(self.courses[maxKey]):
                overlap = False
                # inner loop checks if the time overlaps with an already
                # scheduled course
                for j in schedule:
                    if self.doesOverlap(self.courses[maxKey][i], j[1]):
##                        print('Overlap is true for:', maxKey)
                        overlap = True
                # if it doesn't overlap at all, create tuple and append
                if overlap == False:
                    # create tuple:
                    classToAdd = (maxKey, self.courses[maxKey][i])
                    schedule.append(classToAdd)
##                    print(schedule)
                    # changes value of i to end while loop
                    i = len(self.courses[maxKey])
                i = i+1
            # remove the key and length that was just used
            keys.remove(maxKey)
            lengths.remove(lengths[maxInd])
        return schedule

    def makeScheduleMax(self):
##        print(self.courses)
        # assume self.courses has all the courses in it
        keys = list(self.courses)
        # loops to create a list of lengths that go with each key
        lengths = []
        schedule = []
        for i in range(0, len(keys)):
            lengths.append(len(self.courses[keys[i]]))
            
        sortedlengths = sorted(lengths)
        sortedlengths.reverse()
        for x in sortedlengths:        
            # index of class with most meeting times:
            maxInd = lengths.index(x)
            maxKey = keys[maxInd]
##            print('maxInd:', maxInd)
##            print('maxKey:', maxKey)
            i = 0
##            print('Length through loop:', x)
            while i < len(self.courses[maxKey]):
                overlap = False
                # inner loop checks if the time overlaps with an already
                # scheduled course
                for j in schedule:
                    if self.doesOverlap(self.courses[maxKey][i], j[1]):
##                        print('Overlap is true for:', maxKey)
                        overlap = True
                # if it doesn't overlap at all, create tuple and append
                if overlap == False:
                    # create tuple:
                    classToAdd = (maxKey, self.courses[maxKey][i])
                    schedule.append(classToAdd)
##                    print(schedule)
                    # changes value of i to end while loop
                    i = len(self.courses[maxKey])
                i = i+1
            # remove the key and length that was just used
            keys.remove(maxKey)
            lengths.remove(lengths[maxInd])
        return schedule
                
    def computeNSaveClicked(self):
        # check if there is a file name
        if len(self.fileName) > 0 and (self.IV.get() == 1 or self.IV.get() == 2):
            # if so, call readCSVData(filename)
            self.readCSVFile(self.fileName)
            
            # prompt for file to save to
            savefile = filedialog.asksaveasfilename()
            try:
##                print('open file')
                afile = open(savefile, 'w')
             # if max button is selected, call makeScheduleMax()
##                print('button getting')
                if self.IV.get() == 2:
##                print('about to do max')
                    sched = self.makeScheduleMax()
            # if min button is selected, call makeScheduleMin()
                elif self.IV.get()==1:
##                print('about to do min')
                    sched = self.makeScheduleMin()
##            print(sched)
            # write to the file....
                for i in range(0, len(sched)):
                    line = '%s:\t%s - %s\n' %(sched[i][0], sched[i][1][0], sched[i][1][1])
                    afile.writelines(line)
            # closes file
                afile.close()
                self.resultText.config(text = 'File succesfully written!')
            except:
                pass

            

        

        
        

    def insertIntoDataStruct(self, title, startTime, endTime):
        startTime = int(startTime)
        endTime = int(endTime)
        newTup = (startTime, endTime)    
        if title in self.courses:
            self.courses[title].append(newTup)
            #return courses
        else: 
            self.courses[title] = [newTup]
            #return courses
##        print(self.courses)
        
    def parseLine(self, line):
        i=0
##        print('lline:',line)
        # find key
        for i in range(len(line)):
            if line[i] == ',':
                title = line[:i]
                break
##        print('while loop2')    
        while i < len(line):
            if line[i] == ',':
                startTime = line[i+1:i+5]
                endTime = line[i+6:i+10]
##                print('about to insert...')
                self.insertIntoDataStruct(title, startTime, endTime)
            i = i+10

    def readCSVFile(self, file):
##        print(file)
        try:
            afile = open(file, 'r')
##            print('file opened')
            line = 'dummy'
            while line != '':
##                print('while loop entered')
                line = afile.readline()
    ##            for i in range(len(line)-3):
    ##                if line[i]==',' and line[i+1]==',':
    ##                    line = ' '
    ##            parseLine(line)
                if line == '':
                    break
                elif line[0] == ',':
                    pass
                else:
##                    print('about to parse line')
##                    print('line:',line)
                    self.parseLine(line)
##                    print('line parsed')
            afile.close()
        except:
            print('Invalid file name')


    
        
    
rootWin = Tk()
app = HW6(rootWin)
rootWin.mainloop()