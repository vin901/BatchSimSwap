
# File creation & System tools
from email.mime import base
import sys
import os
from os import path
from os import startfile

# BatchProcessing commands and setup
from batch.BatchSimSwap import BatchSimSwap
from batch.Face import Face
from batch.TerminalColors import TerminalColors

# BeautifulSoup
from bs4 import BeautifulSoup
from lxml import etree
import requests

# Simswap face detection
from models.models import create_model
from insightface_func.face_detect_crop_multi import Face_detect_crop
import cv2
import shutil

# Get current day of the year
from datetime import datetime

# To run the command
import subprocess

# Send file to Recycle Bin
from send2trash import send2trash


def main():
    global batchProcessing
    batchProcessing = BatchProcessing()

    sortArguments()

    # Display Title
    os.system('cls')
    batchProcessing.title("Single Face Swap from URL" + (' '+terminalColors.getString('(Debug Mode)', 'yellow') if batchProcessing.debugMode == True else ''))
    print(" ".join(['\tSwapping face', '\"'+batchProcessing.faces[1].face+'\"', 'with images downloaded from given URL.']))

    # Download Images from URL
    batchProcessing.title("Downloading Images")
    input_images, workingDirectory = downloadPictures(batchProcessing.url)

    # Swap Faces
    batchProcessing.title("Swapping faces though " + str(len(input_images)) + " images..")
    for index, imagefile in enumerate(input_images):
        print("\t" + str(index+1) + ") " + imagefile + " swapping with " + batchProcessing.faces[1].face)
        faceSwap(workingDirectory, imagefile, index)

    # Create link.url
    createLinkFile(workingDirectory)

    # Open working directory
    os.startfile(workingDirectory)

    batchProcessing.title('Finished.')

# Prepare all given arguments into batchProcessing object
def sortArguments():

    # Find given faces and files
    for faceNumber in range(1, 4):
        try:
            if(isinstance(sys.argv[faceNumber], str)):
                faceFilename = batchProcessing.findFaceFilename(sys.argv[faceNumber])
                if(faceFilename):
                    batchProcessing.faces[faceNumber] = Face(sys.argv[faceNumber], faceFilename)
                else:
                    raise Exception(' '.join(['Unable to find file for face',str(faceNumber),"\""+str(sys.argv[faceNumber])+"\" is not a valid face."]))
            else:
                raise Exception(' '.join(['Face',str(faceNumber)," is not a valid face string."]))
        except Exception as e:
            print(str(e))

    ## (int) Index Image
    try:
        batchProcessing.indexImage = int(sys.argv[4]) - 1
    except IndexError:
        raise Exception('Argument 4: IndexImage has not been passed.')

    ## (string) Website URL
    try:
        if(isinstance(sys.argv[5], str)):
            batchProcessing.url = sys.argv[5]
        else:
            raise Exception('Argument 5: URL is not a valid string.')
    except IndexError as e:
        print(' '.join(['Unable to find URL from argument 5',str(e)]))

# Download images from URL
def downloadPictures(target_url):

    current_page_tree = BeautifulSoup(requests.get(target_url).content,'lxml')
    dom = etree.HTML(str(current_page_tree))

    imageHyperlinks = []
    page_title = current_page_tree.find("h1").text
    h1 = ''.join([i for i in target_url.split("/")[-2] if not i.isdigit()])[:-1]

    try:
        modellink = current_page_tree.select('.gallery-info__content:has(a)')
        model = modellink[0].text.split('\n')[1].replace(" ","_").lower()
    except:
        model = ''

    outputFilePath = batchProcessing.createOutputFilePath([
        batchProcessing.faces.get(1).face,
        datetime.now().strftime('%j'),
        ' '.join([model,"_",h1])
    ])

    for link in current_page_tree.find_all("a"):
        if link.get("href").endswith(".jpg"):
            imageHyperlinks.append(link.get("href"))

    print("\tTitle : " + page_title + " (" + str(len(imageHyperlinks))+" images)")
    print("\tFolder: " + model + "_" + h1)
    print("\tUrl   : " + target_url)

    inputimages = []
    try:
        for index, target in enumerate(imageHyperlinks):
            re = requests.get(target)
            with open(outputFilePath + "/" + target.split('/')[-1], 'wb') as f:
                f.write(re.content)
                file = target.split('/')[-1]

            if (index == batchProcessing.indexImage): 
                indicator = " <-- (IndexImage)"
            else: 
                indicator = ""
            print("\tDownloading "+str(index) + ") " + str(file) + indicator)
            
            print("\tDownloading "+str(index) + ") " + str(file))
            inputimages.append(file)
                        
        return inputimages, outputFilePath
    except Exception as e:
            print(str(e))

# Extract all faces from given index image.  Index image needs to have two faces clearly looking at camera.
def extractFacesFromIndexImage(directory, indexImageFile):

    # Using SimSwap method

    multiSwapDirectory = os.path.join(directory,'source_destination')

    createDirectory(multiSwapDirectory)

    # Get faces from image (Simswap)
    blockPrint()
    app = Face_detect_crop(name='antelope', root='./insightface_func/models')
    app.prepare(ctx_id= 0, det_thresh=0.6, det_size=(640,640),mode='None')
    cv2Image = cv2.imread(os.path.join(directory, indexImageFile))
    cv2Width, cv2Height, cv2Channels = cv2Image.shape
    faceDetectionImage = cv2Image.copy()
    foundFaces, kpss = app.det_model.detect(cv2Image,
                                             threshold=0.6,
                                             max_num=0,
                                             metric='default')

    enablePrint()

    # Padding around faces to create larger image
    padding = 50

    # Sort faces from left to right.
    foundFaces = foundFaces[foundFaces[:, 0].argsort()]
        
    # Set up the font to write to detectedFaces Image
    font                   = cv2.FONT_HERSHEY_PLAIN
    
    fontScale              = 1
    fontColor              = (0,255,0)
    thickness              = 1
    lineType               = 2

    # Extract detected faces
    for index, (x1, y1, x2, y2, confidence) in enumerate(foundFaces):
        x1padding, y1padding, x2padding, y2padding = round(x1)-padding, round(y1)-padding, round(x2)+padding, round(y2)+padding
        if(x1padding < 0): x1padding = 0
        if(y1padding < 0): y1padding = 0
        if(x2padding > cv2Width): x2padding = cv2Width
        if(y2padding > cv2Height): y2padding = cv2Height
        bottomLeftCornerOfText = (x1padding+5,y2padding-5)
        print("\tExtracting face with dimensions: " + str(x1padding) + ", " + str(y1padding) + " : " + str(x2padding)  + ", " + str(y2padding))
        regionOfImage = cv2Image[y1padding:y2padding, x1padding:x2padding]
        sourceFileName = os.path.join(multiSwapDirectory, "SRC_0"+str(index+1)+".png")
        cv2.imwrite(sourceFileName, regionOfImage) 
        if(index+1 == 1): whichFace = face1
        if(index+1 == 2): whichFace = face2
        cv2.putText(faceDetectionImage,"Face" + str(index+1) + " " + whichFace, bottomLeftCornerOfText, font, fontScale,fontColor, thickness, lineType)
        cv2.rectangle(faceDetectionImage, (x1padding, y1padding), (x2padding, y2padding), (0, 255, 0), 2)
        cv2.imwrite(os.path.join(multiSwapDirectory, "face-detection.jpg"), faceDetectionImage)

# Block the print for Face_detect_crop used in extractFacesFromIndexImage()
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Enable print again
def enablePrint():
    sys.stdout = sys.__stdout__

# Compile and run a simswap command with given files
def faceSwap(directory, originalImage, imagePrefix):

    input_image_file = '"' + directory + "\\" +  str(originalImage).replace('\\','/') + '"'
    output_path_name = '"' + directory + '"'
    output_file_name = '"' + str(imagePrefix) + "_" + os.path.basename(originalImage) + '"'
    compiled_command = batchProcessing.simswapCommands['image_single']
    
    compiled_command = compiled_command.replace('__input_selected_face__', batchProcessing.faces[1].filename)
    compiled_command = compiled_command.replace('__input_image_file__', input_image_file)
    compiled_command = compiled_command.replace('__output_path_name__', output_path_name)
    compiled_command = compiled_command.replace('__output_file_name__', output_file_name)
  
    # print("\n\tReplaced compiled command")
    # print("\n" + compiled_command + "\n") 
    # subprocess.run(compiled_command)
    # 
    subprocess.run(compiled_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    send2trash(os.path.join(directory, originalImage))

# Create a link file to the original website provided
def createLinkFile(directory):
    # Create link.url
    batchProcessing.title("Creating link.url file")
    with (open(os.path.join(directory,'link.url'), 'w')) as f:
        f.write('[InternetShortcut]\n')
        f.write('URL='+batchProcessing.url+'\n')

if __name__ == '__main__':
    main()
    




