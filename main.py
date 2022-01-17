import glob, os
import string
from stemming.porter2 import stem

class BagOfWordsDocument:
    def parse_doc(self,docFile):
        dictOfWords = [] #A List for collecting all the words from the document
        startFlag = False #Flag for starting iternation over <text> in the xml document
        word_count = 0 #Gives the count of the words in a document
        for lines in docFile:
            lines = lines.strip() #removing spaces at begining and at the end of each character
            if(startFlag == False):
                if lines.startswith("<text>"): # loop for iterating over just <text> tag
                    startFlag = True
            elif lines.startswith("</text>"):
                break
            else:
                lines = lines.replace("<p>", "").replace("</p>", "") # removing <p> </p> tags from the xml document
                lines = lines.translate(str.maketrans('', '', string.digits)).translate(str.maketrans(string.punctuation, ' ' * len(string.punctuation))) #Removes punctuation and numbers repalcing with whitespace
                for term in lines.split(): # loop to split the line into words and then count the number and frequency of each word.
                    word_count += 1
                    term = term.lower() #removing case sensitivity
                    dictOfWords.append(term) #appending each term after parsing to a list

        return (word_count, dictOfWords)

    def addTerm(self,document, stop_words):  #Method to remove the stopwords and stem it
        termfrequency = {} #A collection of allwords after stemming and removing stopwords
        for term in document:
            if len(term) > 2 and term not in stop_words: #checking for stopwords
                stemterm = stem(term)
                try:
                    termfrequency[stemterm] += 1#appending each term after stemming and removing stopwords to a list
                except KeyError: #Error handling
                    termfrequency[stemterm] = 1

        SortedDocuments = sorted(termfrequency.items(), key=lambda item:item[1], reverse= True)
        return (SortedDocuments) #returning a sorted dictionary with frequency in descending order

    def getDocID(self,docFile): #Function to get Document ID
        dfile = docFile
        startFlag = False
        for line in dfile:
            line = line.strip() #Stripping the entire document into lines
            if (startFlag == False):
                if line.startswith("<newsitem"): #checking for newsitem
                    for part in line.split():
                        if part.startswith("itemid="): #Checking for itemID
                            documentID = part.split("=")[1].split("\"")[1] #Spliting the line by '=' & '/'
                            break

        return (documentID)#Returning Document ID

    def DocInfo(self,termFrequencyDataStructure, documentID , parsedDocumentFile):  # Fucntion to print the output
        print('Document ' + str(documentID) + ' contains ' + str(len(parsedDocumentFile[1])) + ' words ' + str(len(termFrequencyDataStructure)) + ' terms(stems)')
        for term, freq in termFrequencyDataStructure:
            print(term + ':' + str(freq))
        print("\n")



if __name__ == '__main__': #Main method starts
    inputpath = r'E:\IFN647\Kevin Jacob Mylakkattu n10654704\Question -1\Kevin_Jacob_Mylakkattu_Q1C\RCV1v2\inputdata' #Path of the data set
    stopwords_f = open(r'E:\IFN647\Kevin Jacob Mylakkattu n10654704\Question -1\Kevin_Jacob_Mylakkattu_Q1C\RCV1v2\inputdata\common-english-words.txt') #Path of the stopwords
    stop_words = stopwords_f.read().split(',') #Reading and spliting the stopwords
    stopwords_f.close()
    os.chdir(inputpath)
    BowDoc = BagOfWordsDocument()
    for file in glob.glob('*.xml'):  #iterating through folder where the files are stored
        with open(file) as files:#Opening the file
            docFile = files.readlines()  #reading the xml file
        documentID = BowDoc.getDocID(docFile) #extract the document ID from the file and storing it in a variable
        parsedDocumentFile = BowDoc.parse_doc(docFile) # Calling the function and pass files as parameter
        document = parsedDocumentFile[1] #Declaring a variable to select {term:Frequency} from parsedDocumentFile
        termFrequencyDataStructure = BowDoc.addTerm(document, stop_words) #Calling the function and pass output from previous method as parameter
        BowDoc.DocInfo(termFrequencyDataStructure,documentID, parsedDocumentFile) #Calling the function to print the output
