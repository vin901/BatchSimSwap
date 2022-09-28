# File creation & System tools
import sys
import os
from os import path
from os import startfile

# batchSimSwap commands and setup
from batch.BatchSimSwap import BatchSimSwap
from batch.Face import Face
from batch.TerminalColors import TerminalColors

# BeautifulSoup & HTML scraping
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
    global batchSimSwap, terminalColors
    batchSimSwap = BatchSimSwap()
    terminalColors = TerminalColors()
    
    os.system('cls')
    sortArguments()

    # Display Title
    batchSimSwap.title("Single Face Swap from URL" + (' '+terminalColors.getString('(Debug Mode)', 'yellow') if batchSimSwap.debugMode == True else ''))

    print(" ".join(['\tSwapping face', terminalColors.getString("\"" + batchSimSwap.faces[1].face + "\"", 'purple'), 'with images downloaded from given URL.']))

    # Download Images from URL
    batchSimSwap.title("Downloading Images")
    input_files, absoluteDirectory = downloadPictures(batchSimSwap.url)


    batchSimSwap.title("Extracting Faces from images..")
    extractFacesFromIndexImage(absoluteDirectory, batchSimSwap.indexImageFile)
    
    # Create DST_O1 and DST_02 images to source_destination folder
    # (The faces supplied via the command to swap to)
    shutil.copy(batchSimSwap.findFaceFilename(batchSimSwap.faces.get(1).filename, True), os.path.join(absoluteDirectory,"source_destination", "DST_01.png"))
    shutil.copy(batchSimSwap.findFaceFilename(batchSimSwap.faces.get(2).filename, True), os.path.join(absoluteDirectory,"source_destination", "DST_02.png"))
    
    # Swap Faces
    batchSimSwap.title("Swapping faces though " + str(len(input_files)) + " images..")
    runSuccess = True
    for index, imagefile in enumerate(input_files):
        sys.stdout.write("\t" + str(index+1) + ") " + terminalColors.getString(imagefile, 'blue') + " swapping with face "+terminalColors.getString(batchSimSwap.faces[1].face, 'face') + " and " + terminalColors.getString(batchSimSwap.faces[2].face, 'face'))
        success = faceSwap(absoluteDirectory, imagefile, index)
        if not success: runSuccess = False
        
    if not runSuccess:
        batchSimSwap.title('Errors Found..', 'red')
        print(terminalColors.red)
        print('\tThere was errors when running the faceswap, try turning on debugMode  True in batch_processing/batch_processing.py to find out what is going wrong.')
        print('\n\tIf it was only one or two files, then it may just be alignment issues.  If all files are showing an error and none of them worked, then there is a problem with your simswap installation, or a possible bug in BatchSimSwap.  You can raise an issue at https://github.com/chud37/BatchSimSwap/issues')
        print(terminalColors.endColor)

    # Create link.url
    createLinkFile(absoluteDirectory)

    # Open working directory
    os.startfile(absoluteDirectory)

    batchSimSwap.title('Finished.')

# Prepare all given arguments into batchSimSwap object
def sortArguments():
    # Find given faces and files
    for faceNumber in range(1, 3):
        try:
            if(isinstance(sys.argv[faceNumber], str)):
                faceFilename = batchSimSwap.findFaceFilename(sys.argv[faceNumber])
                if(isinstance(faceFilename, str)):
                    if(batchSimSwap.debugMode == True): print("\tFound face from sys.argv " + str(faceNumber) + " face name: " + sys.argv[faceNumber])
                    batchSimSwap.faces[faceNumber] = Face(sys.argv[faceNumber], faceFilename)
                else:
                    print(str(sys.argv))
                    raise SystemExit(' '.join(['Unable to find file for face',str(faceNumber),"\""+str(sys.argv[faceNumber])+"\" is not a valid face."]))
            else:
                raise SystemExit(' '.join(['Face',str(faceNumber)," is not a valid face string."]))
        except Exception as e:
            raise SystemExit('Unknown error: ' + str(e))

    ## (int) Index Image
    try:
        batchSimSwap.indexImage = int(sys.argv[3]) - 1
    except IndexError:
        raise SystemExit('Argument 3: IndexImage has not been passed.')

    ## (string) Website URL
    try:
        if(isinstance(sys.argv[4], str)):
            batchSimSwap.url = sys.argv[4]
        else:
            raise SystemExit('Argument 4: URL is not a valid string.')
    except IndexError as e:
        print(' '.join(['Unable to find URL from argument 4',str(e)]))

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

    outputFilePath = batchSimSwap.createOutputFilePath([
        batchSimSwap.faces.get(1).face,
        datetime.now().strftime('%j'),
        ''.join([model,"_",h1])
    ])

    for link in current_page_tree.find_all("a"):
        if link.get("href").endswith(".jpg"):
            imageHyperlinks.append(link.get("href"))

    print("\tTitle : " + page_title + " (" + str(len(imageHyperlinks))+" images)")
    print("\tFolder: " + model + "_" + h1)
    print("\tUrl   : " + target_url + "\n")

    inputimages = []
    try:
        for index, target in enumerate(imageHyperlinks):
            re = requests.get(target)
            with open(outputFilePath + "/" + target.split('/')[-1], 'wb') as f:
                f.write(re.content)
                file = target.split('/')[-1]
            
            if (index == batchSimSwap.indexImage): 
                indicator = " <-- (IndexImage)"
                batchSimSwap.indexImageFile = file
            else: 
                indicator = ""
            
            print("\tDownloading "+str(index) + ") " + str(file) + indicator)
            inputimages.append(file)
                        
        return inputimages, outputFilePath
    except Exception as e:
            print(str(e))

# Extract all faces from given index image.  Index image needs to have two faces clearly looking at camera.
def extractFacesFromIndexImage(directory, indexImageFile):

    # Using SimSwap method

    multiSwapDirectory = os.path.join(directory,'source_destination')

    batchSimSwap.createDirectory(multiSwapDirectory)

    # Get faces from image (Simswap)
    blockPrint()
    app = Face_detect_crop(name='antelope', root='./insightface_func/models')
    app.prepare(ctx_id= 0, det_thresh=0.6, det_size=(640,640),mode='None')
    cv2Image = cv2.imread(os.path.join(directory, indexImageFile))
    cv2Height, cv2Width, cv2Channels = cv2Image.shape
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
        if(index+1 == 1): whichFace = batchSimSwap.faces.get(1).face
        if(index+1 == 2): whichFace = batchSimSwap.faces.get(2).face
        cv2.putText(faceDetectionImage,"Face" + str(index+1) + " " + whichFace, bottomLeftCornerOfText, font, fontScale,fontColor, thickness, lineType)
        cv2.rectangle(faceDetectionImage, (x1padding, y1padding), (x2padding, y2padding), (0, 255, 0), 2)
        cv2.imwrite(os.path.join(multiSwapDirectory, "face-detection.jpg"), faceDetectionImage)

# Block the print for Face_detect_crop used in extractFacesFromIndexImage()
def blockPrint():
    sys.stdout = open(os.devnull, 'w')
    sys.stderr = open(os.devnull, 'w')

# Enable print again
def enablePrint():
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__

# Compile and run a simswap command with given files
def faceSwap(directory, originalImage, imagePrefix):

    success = True
    input_image_file = '"' + directory + "\\" +  str(originalImage).replace('\\','/') + '"'
    output_path_name = '"' + directory + '"'
    output_file_name = '"' + str(imagePrefix) + "_" + os.path.basename(originalImage) + '"'
    compiled_command = batchSimSwap.simswapCommands['image_multispecific']
    
    compiled_command = compiled_command.replace('__input_selected_face__', os.path.join(batchSimSwap.getbatchSimSwapDirectoryOnly(),batchSimSwap.paths['input_faces'], batchSimSwap.faces[1].filename).replace("\\","/"))
    compiled_command = compiled_command.replace('__input_image_file__', input_image_file)
    compiled_command = compiled_command.replace('__output_path_name__', output_path_name)
    compiled_command = compiled_command.replace('__output_file_name__', output_file_name)
    compiled_command = compiled_command.replace('__multi_specific_path__', os.path.join(output_path_name, 'source_destination'))
  
    if(batchSimSwap.debugMode):
        print("\n\tReplaced compiled command")
        print("\n" + compiled_command + "\n") 
        subprocess.run(compiled_command)
        send2trash(os.path.join(directory, originalImage))
    else:
        result = subprocess.run(compiled_command, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        if batchSimSwap.simswapCommandComplete in str(result.stdout):
            sys.stdout.write(' - ' + terminalColors.getString('Complete.', 'green', True))
        else: 
            sys.stdout.write(' - ' + terminalColors.getString('Error.', 'red', True))
            success = False
        send2trash(os.path.join(directory, originalImage))
    
    return success

# Create a link file to the original website provided
def createLinkFile(directory):
    # Create link.url
    batchSimSwap.title("Creating link.url file")
    with (open(os.path.join(directory,'link.url'), 'w')) as f:
        f.write('[InternetShortcut]\n')
        f.write('URL='+batchSimSwap.url+'\n')

if __name__ == '__main__':
    main()
    




