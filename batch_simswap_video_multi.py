
# File creation & System tools
import sys
import os
from os import path
from os import startfile
import pathlib

# batchSimSwap commands and setup
from batch.BatchSimSwap import BatchSimSwap
from batch.Face import Face
from batch.TerminalColors import TerminalColors

# Get current day of the year
from datetime import datetime

# To run the command
import subprocess

# Send file to Recycle Bin
from send2trash import send2trash

# Simswap face detection
from models.models import create_model
from insightface_func.face_detect_crop_multi import Face_detect_crop
import cv2
import shutil

def main():
    global batchSimSwap, terminalColors
    batchSimSwap = BatchSimSwap()
    terminalColors = TerminalColors()

    os.system('cls')
    sortArguments()

    # Display Title
    inputFolderString = terminalColors.getString(os.path.join('.', batchSimSwap.getbatchSimSwapDirectoryOnly(), batchSimSwap.paths['input'], batchSimSwap.dynamicPaths['input']),'red').replace('\\','/')
    batchSimSwap.title("BatchSimSwap: Swap video filter with multiple faces " + (' '+terminalColors.getString('(Debug Mode)', 'debug') if batchSimSwap.debugMode == True else ''))
    print(" ".join(['\tSwapping face', terminalColors.getString(batchSimSwap.faces[1].face,'face'),'and',terminalColors.getString(batchSimSwap.faces[2].face,'face'), 'with videos from ',inputFolderString]))

    # Get list of video files from folder
    batchSimSwap.title("Scanning Video Files..")
    input_files = getInputFiles()
    for index, videofile in enumerate(input_files):
        print("\t" + str(index+1) + ") " + terminalColors.getString(os.path.basename(videofile),'file'))
    
    # Get output file path
    outputFilePath = batchSimSwap.createOutputFilePath([
        batchSimSwap.faces.get(1).face,
        datetime.now().strftime('%j')
    ])
    
    # Find indexImageFrame to extract faces from, create image in the multispecific directory
    indexImageFrame = extractIndexImage(input_files[0])
    
    # Extract faces from the index image, create SRC and DST files
    extractFacesFromIndexImage(os.path.join(batchSimSwap.getPath('multispecific'), 'src_dst'), indexImageFrame)

    # Create DST_O1 and DST_02 images to src_dst folder
    # (The faces supplied via the command to swap to)
    shutil.copy(batchSimSwap.findFaceFilename(batchSimSwap.faces.get(1).filename, True), os.path.join(batchSimSwap.getPath('multispecific'),"src_dst", "DST_01.png"))
    shutil.copy(batchSimSwap.findFaceFilename(batchSimSwap.faces.get(2).filename, True), os.path.join(batchSimSwap.getPath('multispecific'),"src_dst", "DST_02.png"))

    # Swap Faces
    batchSimSwap.title("Swapping faces though " + str(len(input_files)) + " files..")
    for index, videofile in enumerate(input_files):
        print("\t" + str(index+1) + ") Swapping " + terminalColors.getString(os.path.basename(videofile),'file') + " with " + terminalColors.getString(batchSimSwap.faces[1].face, 'face'))
        faceSwap(outputFilePath, videofile)

    # Open working directory
    # os.startfile(outputFilePath)

    batchSimSwap.title('Finished.')

# Prepare all given arguments into batchSimSwap object
def sortArguments():

    batchSimSwap.dynamicFolderCheck('_multispecific', 'temp')
    
    # Find given faces and files
    if(isinstance(sys.argv[1], str)):
        faceFilename = batchSimSwap.findFaceFilename(sys.argv[1])
        if(faceFilename):
            batchSimSwap.faces[1] = Face(sys.argv[1], faceFilename)
        else:
            raise Exception(' '.join(['Unable to find file for face 1',"\""+str(sys.argv[1])+"\""," is not a valid face."]))
    else:
        raise Exception('Face 1 is not a valid face string.')
    
    if(isinstance(sys.argv[2], str)):
        faceFilename = batchSimSwap.findFaceFilename(sys.argv[2])
        if(faceFilename):
            batchSimSwap.faces[2] = Face(sys.argv[2], faceFilename)
        else:
            raise Exception(' '.join(['Unable to find file for face 1',"\""+str(sys.argv[2])+"\""," is not a valid face."]))
    else:
        raise Exception('Face 2 is not a valid face string.')
    
    if(isinstance(sys.argv[3], str)):
        batchSimSwap.indexImageTimeStamp = sys.argv[3]
    else:
        batchSimSwap.indexImageTimeStamp = '01:00'

# Get the input files from the input_X folder
def getInputFiles():
    inputvideos = []
    for file in pathlib.Path(batchSimSwap.getPath('multispecific')).iterdir():
        if file.is_file():
            if '.mp4' in str(file):
                inputvideos.append(file)
            if '.webm' in str(file):
                newfilename = str(file).replace(".webm",".mp4")
                os.rename(file, newfilename)
                inputvideos.append(newfilename)
    
    return inputvideos

def extractIndexImage(videofile):
    
        
    multiSwapDirectory = os.path.join(os.path.join(batchSimSwap.getPath('multispecific'), 'src_dst'))
    batchSimSwap.createDirectory(multiSwapDirectory)
    
    video = cv2.VideoCapture(str(videofile))
    fps = video.get(cv2.CAP_PROP_FPS)
    minutes, seconds = batchSimSwap.indexImageTimeStamp.split(':')
    targetFrame = int(minutes) * (60 * int(fps)) + (int(seconds) * int(fps))
    framecount = 0
    success = True
    video.set(cv2.CAP_PROP_POS_FRAMES, targetFrame)
    success,frame = video.read()
    cv2.imwrite(os.path.join(multiSwapDirectory, 'indexframe.jpg'), frame)

    return os.path.join(multiSwapDirectory, 'indexframe.jpg')

def extractFacesFromIndexImage(multiSwapDirectory, indexImageFile):

    # Using SimSwap method
    # Get faces from image (Simswap)
    blockPrint()
    app = Face_detect_crop(name='antelope', root='./insightface_func/models')
    app.prepare(ctx_id= 0, det_thresh=0.6, det_size=(640,640),mode='None')
    cv2Image = cv2.imread(os.path.join(multiSwapDirectory, indexImageFile))
    cv2Height, cv2Width, cv2Channels = cv2Image.shape
    faceDetectionImage = cv2Image.copy()
    foundFaces, kpss = app.det_model.detect(cv2Image,
                                             threshold=0.6,
                                             max_num=0,
                                             metric='default')
    enablePrint()

    # Padding around faces to create larger image
    padding = 100

    # Sort faces from left to right.
    foundFaces = foundFaces[foundFaces[:, 0].argsort()]
        
    # Set up the font to write to detectedFaces Image
    font                   = cv2.FONT_HERSHEY_PLAIN
    
    fontScale              = 3
    fontColor              = (255,255,0)
    thickness              = 3
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
        cv2.putText(faceDetectionImage,"Face" + str(index+1) + " " + whichFace + " (" + str(int(confidence*100)) + "%)", bottomLeftCornerOfText, font, fontScale,fontColor, thickness, lineType)
        cv2.rectangle(faceDetectionImage, (x1padding, y1padding), (x2padding, y2padding), (0, 255, 0), 2)
        cv2.rectangle(faceDetectionImage, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 2)
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
def faceSwap(outputDirectory, videofile):

    success = True
    outputVideoFilename = os.path.basename(videofile)
    compiled_command = batchSimSwap.simswapCommands['video_swap_multispecific']
    compiled_command = compiled_command.replace('__input_selected_face__', os.path.join(batchSimSwap.getbatchSimSwapDirectoryOnly(),batchSimSwap.paths['input_faces'], batchSimSwap.faces[1].filename).replace("\\","/"))
    compiled_command = compiled_command.replace('__input_video_file__', '"' + str(videofile).replace('\\','/') + '"')
    compiled_command = compiled_command.replace('__output_file_name__', '"' + os.path.join(outputDirectory, outputVideoFilename) + '"')
    compiled_command = compiled_command.replace('__temp_folder_path__', '"' + batchSimSwap.getDynamicPath('temp') + '"')
    compiled_command = compiled_command.replace('__multi_specific_path__', os.path.join(batchSimSwap.getPath('multispecific'),"src_dst"))
  
    if(batchSimSwap.debugMode):
        print("\n\t SimSwap Compiled Command:")
        print("\n\t" + terminalColors.getString(compiled_command,'yellow', True)) 
        print()
        subprocess.run(compiled_command)
        # send2trash(os.path.join(outputDirectory, outputVideoFilename))
    else:
        subprocess.run(compiled_command)
        # send2trash(str(videofile))
    
    return success

if __name__ == '__main__':
    main()
    




