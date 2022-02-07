# [ Welcome to Python PDF WATERMARK REMOVER ]
# [ website : https://ViKi-R.github.io ]
# [ Author : ViKi-R ]

from PyPDF4 import PdfFileReader, PdfFileWriter
from PyPDF4.pdf import ContentStream
from PyPDF4.generic import TextStringObject, NameObject
from PyPDF4.utils import b_
import os 
import time
import shutil


def remove_watermark(wmText, inputFile, outputFile):
    # This Function Reads PDF file and Removes the WATERMARK TEXT
    
    with open(inputFile, "rb") as f:
        source = PdfFileReader(f, "rb")
        output = PdfFileWriter()
        
        #print(output)

        for page in range(source.getNumPages()):
            page = source.getPage(page)
            content_object = page["/Contents"].getObject()
            content = ContentStream(content_object, source)

            for operands, operator in content.operations:
                if operator == b_("Tj"):
                    text = operands[0]

                    for i in wmText:
                        if isinstance(text, str) and text.startswith(i):
                            operands[0] = TextStringObject('')
                    
            page.__setitem__(NameObject('/Contents'), content)
            output.addPage(page)

        #print(output)
        
        with open(outputFile, "wb") as outputStream:
            output.write(outputStream)


def watermark_text(inputFile, waterMarkTextStarting):
    # This Function reads the PDF file and searches for input string and deletes the WaterMark

    wmText = []
    pdfFileObj = open(inputFile, 'rb') 
    pdfReader = PdfFileReader(pdfFileObj) 
    pageObj = pdfReader.getPage(0) 
    watermark = pageObj.extractText() 
    pdfFileObj.close()
    x = watermark.find(waterMarkTextStarting)
    lengthWmText = len(waterMarkTextStarting) 
    wmText.append(watermark[x:x+lengthWmText])
    wmText.append(watermark[x+lengthWmText:])
    return wmText 


def draw(): 
    # This Function Prints the below message

    print(f'-'*57)
    print("|\t\tPYTHON PDF WATERMARK REMOVER\t\t|")
    print(f'-'*57)       
    print("""[ Welcome to PYTHON PDF WATERMARK REMOVER ]\n[ website : https://ViKi-R.github.io ]\n[ Author : ViKi-R ]""")
    print(f'-'*57)       


def creatingFolder(dirName):
    # This Function is used to create Folder, Original-pdf and Watermark-Removed-pdf

    os.makedirs(os.path.dirname(dirName), exist_ok=True)
    time.sleep(2)
    return dirName


def CheckingFiles(dirName):
    # This Function is used to check if any pdf present in Orginal-pdf Folder
    # if present excutes next step
    # else prompts user to add pdf files to folder

    input(f"Please place the PDF files in the '{dirName}' Folder Created! and Press Enter...")
    print(f"-"*50)

    while True:
        inputFilesNames = os.listdir(dirName)
        if len(inputFilesNames) == 0:
            input(f"No PDF files Found in '{dirName}' Folder! Please add and Press Enter...")
        else:
            break

    print(f"Total Number of PDF Files Found: {len(inputFilesNames)}")    
    return inputFilesNames    


def processingFilesInFolder(inputFileDir, outputFileDir, inputFilesNames, waterMarkTextStarting):
    # This Function used to process all files added in folder 

    x = u'\u2713'
    print(f'-'*50)
    for idx, i in enumerate(inputFilesNames):
        inputFile = f'{inputFileDir}{i}'
        outputFile = f'{outputFileDir}{i}'
        wm_text = watermark_text(inputFile, waterMarkTextStarting)
        remove_watermark(wm_text, inputFile, outputFile)
        print(f'[ {x} ]  {idx+1} File Done...')


def deletingFiles(inputDirName, outputDirName):
    # This Function removes the files once the process is completed
    # if the watermark-removed-pdf folder is empty it deletes the folder
    # else prompts the user to empty the folder 

    input(f"Please Cut PDF files found in '{outputDirName}' and Paste in other folder and Press Enter...")
    print(f'-'*50)
    while True:
        outputDir_files = os.listdir(outputDirName)
        if(len(outputDir_files) == 0):
            print(f'-'*50)
            print(f"Deleting Folders {inputDirName} and {outputDirName}")
            shutil.rmtree(inputDirName)
            time.sleep(2)
            shutil.rmtree(outputDirName)
            time.sleep(2)
            print("Done...")
            break
        else:
            input(f"'{outputDirName}' is not empty. Please empty folder and Press Enter...")


def verbosity(inputFilesNames, outputDirName):
    # This Function verboses information

    print(f'-'*50)
    print(f"Watermark for {len(inputFilesNames)} Files has been Removed.")
    print(f'-'*50)
    print(f"Watermark Removed PDF Files can be found in '{outputDirName}' ...")
    print(f'-'*50)


def main():
    # Driver Function

    draw()
    waterMarkTextStarting = input("Enter First Line of Watermark text: ")
    print(f'-'*50)
    inputDirName = creatingFolder('Original-pdf/')
    inputFilesNames = CheckingFiles(inputDirName)
    outputDirName = creatingFolder('Watermark-Removed-pdf/')
    processingFilesInFolder(inputDirName, outputDirName, inputFilesNames, waterMarkTextStarting)
    verbosity(inputFilesNames, outputDirName)
    time.sleep(3)
    deletingFiles(inputDirName, outputDirName)
    print(f'-'*50)
    input("Press Enter to exit...")
    os.system("exit") 


if __name__ == "__main__":
    main()    
