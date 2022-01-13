import re
import json
import pandas as pd
from tkinter import Tk
from tkinter.messagebox import showinfo
from tkinter.filedialog import askopenfile

def cleanText(text):
    cleaned_text = re.sub(r'[^0-9A-Z ]', ' ', text)
    return ' '.join(cleaned_text.split())

def fileSelector():
    root = Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    newLabelsFile = askopenfile(parent=root, filetypes=[('Excel files', '.csv')])
    return newLabelsFile.name if newLabelsFile else None

def updateDict(filepath):
    newLabelsDict = {cleanText(row[0]): row[1] for row in pd.read_csv(filepath).values}
    jsonPath = './static/appscripts/json/icd_codes.json'
 
    with open(jsonPath) as file:
        causeIcd, icdCause = json.load(file).values()
    print('Length of original causeIcd: {}'.format(len(causeIcd)))
    
    with open(jsonPath, 'w') as newfile:
        causeIcd = {**causeIcd, **newLabelsDict}
        updatedDict = {"cause_icd": causeIcd, "icd_cause": icdCause}
        json.dump(updatedDict, newfile)
    print('Length of updated causeIcd: {}'.format(len(causeIcd)))

    return jsonPath.split('/')[-1]

def successMessage(jsonFile):
    msg = '{} has been updated successfully!'.format(jsonFile)
    showinfo(title='Operation Complete', message=msg)
     
    
if __name__=='__main__':
    filepath = fileSelector()
    if filepath:
        jsonFile = updateDict(filepath)
        successMessage(jsonFile)





