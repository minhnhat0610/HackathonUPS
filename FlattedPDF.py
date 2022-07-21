from turtle import right
import pdfplumber 
import re
from CheckBoxClass import CheckBox
# ========= Global defined variables =============


# List of Text Field Name
fieldNameLists = ["Name","Date","Address","Telephone #","Other Phone #", "Social Security #","Referred by","Position(s) applied for","Date available","Position(s) applied for","Date available"]

# Empty field list use to hold field when read pdf
fieldList = {}
fieldTextCorr = {}
# PDF cordinate for first line that contains a CheckBox [left,top,right,bottom]
boundingBox = [88.6,237.9,524.8,250.6]
lineHeight = 24
checkBoxList = ["Employment Type","Employer Contact","Employment Eligibility","Work Permit","Overtime","Applied Before","Employed Before","Relative Employed","Crime History"]

boundingBox2 = [89.0,107.0,523.3,120.1]
numOfTextLine = 6
def Main(FilePath):
    try:
        with open(FilePath,"rb") as f:
            reader = pdfplumber.open(f)
            firstPage = reader.pages[0]
            FirstPageText = str(firstPage.extract_text().encode('utf-8')).split("\\n")

            #Find Text field from extracted text
            words = firstPage.extract_words()
            for line in FirstPageText:
                FindFormField(line)
            # Find text field corrdinate
            FindFieldNameCor(firstPage,boundingBox2)

            #Find checkbox in the first page
            InvalidCheckBoxCorr = FindCheckBox(boundingBox,firstPage)
            # print("====================================================================================")
            # displayInvalid(fieldList,validCheckBox)
            # print("====================================================================================")
            # displayValid(fieldList,validCheckBox)

            # invalidTextField = [field for field,value in fieldList.items() if value == ""]
            invalidTextField = exportResult(fieldTextCorr)

            return {"Invalid_Text_Field":invalidTextField,"Invalid_Check_Box":InvalidCheckBoxCorr}

    except Exception as e:
        print(f'Main Error Thrown: {e}')

def exportResult(fieldTextCorr):
    invalidTextField = {}
    for field,value in fieldList.items():
        if(value == ""):
            invalidTextField[field] = fieldTextCorr[field]
    return invalidTextField

def FindFormField(line):
    try:
        indexList = []
        tempList = []
        # Find Text field name index in single line
        for fieldName in fieldNameLists:
            if(fieldName in line):
                indexList.append(line.index(fieldName))
                tempList.append(fieldName)
            
                
        # Extract field value
        for i in range(len(indexList)):
            if(i<len(indexList)-1):
                fieldValue = line[indexList[i]+len(tempList[i]):indexList[i+1]]
            else:
                fieldValue = line[indexList[i]+len(tempList[i]):]
            fieldValue = re.sub('[\(\)]',"",fieldValue)
            fieldList[tempList[i]] = fieldValue.strip()
            fieldNameLists.remove(tempList[i])
        
                
    except Exception as e:
        print(f'FindFieldForm Error Thrown: {e}')           

def FindFieldNameCor(page,boundingBox2):
    corr = {}
    index = 0
    for index in range(numOfTextLine):
        cropLine = page.crop(boundingBox2)
        words = cropLine.extract_words()

        for word in words:
            for field in fieldList:
                fieldNameWords = field.split(" ")
                if(word['text'] == fieldNameWords[0]):
                    corr['left'] = word['x0']
                    corr['top'] = word['top']
                    corr['bottom'] = word['bottom']
                # if(word['text'] == fieldNameWords[-1]):
                    corr['right'] = word['x1']
                    fieldTextCorr.update({field:corr})
                    corr = {}
        boundingBox2[1] += 22
        boundingBox2[-1] += 22


def FindCheckBox(boundingBox, page):
    try:
        InvalidLine = []
        ValidCheckBox = []
        for index in range(len(checkBoxList)):
            cropLine = page.crop(boundingBox)

            if(cropLine.objects['curve']):
                x1 = cropLine.objects['curve'][0]['x1']
                words = cropLine.extract_words()
                target = ""
                for word in words:
                    distance = word['x0'] - x1
                    if(distance >= 0):
                        target = word['text']
                        break
                checkBox = CheckBox(checkBoxList[index],target,True)
                ValidCheckBox.append(checkBox)
            else:
                if(cropLine.objects['rect']):
                    rect = cropLine.objects['rect'][0]
                    corr = [rect['x0'],rect["top"],rect['x1'],rect['bottom']]
                    InvalidLine.append(corr)
                checkBox = CheckBox(checkBoxList[index])
                ValidCheckBox.append(checkBox)
            boundingBox[1] += lineHeight
            boundingBox[-1] += lineHeight
        return InvalidLine
    except Exception as e:
        print(f'FindCheckBox Error Thrown: {e}') 

def displayInvalid(fieldList, checkBoxList):
    invalidTextField = [field for field,value in fieldList.items() if value == ""]
    InvalidCheckBox = [checkBox.fieldName for checkBox in checkBoxList if checkBox.status == False]
    print(f"Invalid Text Field: {invalidTextField}")
    print(f"Invalid Check Box: {InvalidCheckBox}")

def displayValid(fieldList, checkBoxList):
    validTextField = {}
    validCheckBox = {}
    for field,value in fieldList.items():
        if(value != ""):
            validTextField[field] = value
    for checkBox in checkBoxList:
        if (checkBox.status == True):
            validCheckBox[checkBox.fieldName] = checkBox.value
    print(f"Valid Text Field: {validTextField}")
    print(f"Valid Check Box: {validCheckBox}")


        



    

    
        
