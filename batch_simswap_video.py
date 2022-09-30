
# File creation & System tools
from opcode import hasconst
import sys
import os
from os import path, rename
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

# Video editing
from moviepy.editor import *
import proglog
import shutil

def main():
    global batchSimSwap, terminalColors
    batchSimSwap = BatchSimSwap()
    terminalColors = TerminalColors()

    os.system('cls')
    sortArguments()

    # Display Title
    inputFolderString = terminalColors.getString(os.path.join('.', batchSimSwap.getbatchSimSwapDirectoryOnly(), batchSimSwap.paths['input'], batchSimSwap.dynamicPaths['input']),'red').replace('\\','/')
    batchSimSwap.title("BatchSimSwap: Swap video folder with single image" + (' '+terminalColors.getString('(Debug Mode)', 'debug') if batchSimSwap.debugMode == True else ''))
    print(" ".join(['\tSwapping face', terminalColors.getString(batchSimSwap.faces[1].face,'face'), 'with videos from ',inputFolderString]))

    # Get list of video files from folder
    batchSimSwap.title("Scanning Video Files..")
    input_files = getInputFiles()
    for index, videofile in enumerate(input_files):
        print("\t" + str(index+1) + ") " + terminalColors.getString(os.path.basename(videofile),'file'))
    absoluteDirectory = batchSimSwap.getDynamicPath('input')

    absoluteDirectory = batchSimSwap.createOutputFilePath([
        batchSimSwap.faces.get(1).face,
        datetime.now().strftime('%j')
    ])

    if hasattr(batchSimSwap, 'startTimeStamp') and hasattr(batchSimSwap, 'endTimeStamp'):
        # Cut the videos
        batchSimSwap.title(' '.join(['Trimming all video in input_'+batchSimSwap.inputFolderNumber,'from', batchSimSwap.startTimeStamp, 'to', batchSimSwap.endTimeStamp]))
        minutes, seconds = batchSimSwap.startTimeStamp.split(':')
        startSeconds = (int(minutes) * 60) + int(seconds)
        minutes, seconds = batchSimSwap.endTimeStamp.split(':')
        endSeconds = (int(minutes) * 60) + int(seconds)
        for index, videofile in enumerate(input_files):
            print("\t" + str(index+1) + ") " + terminalColors.getString(os.path.basename(videofile),'file'))
            clip = VideoFileClip(str(videofile))
            clip = clip.subclip(startSeconds, endSeconds)
            tmpFileName = os.path.join(batchSimSwap.getDynamicPath('input'), "trimming__" + os.path.basename(videofile))
            clip.write_videofile(tmpFileName,audio_codec='aac',logger=proglog.TqdmProgressBarLogger(print_messages=False))
            clip.close()
            os.remove(str(videofile))
            os.rename(tmpFileName, str(videofile))


    # Swap Faces
    batchSimSwap.title("Swapping faces though " + str(len(input_files)) + " files..")
    for index, videofile in enumerate(input_files):
        print("\t" + str(index+1) + ") Swapping " + terminalColors.getString(os.path.basename(videofile),'file') + " with " + terminalColors.getString(batchSimSwap.faces[1].face, 'face'))
        faceSwap(absoluteDirectory, videofile)

    # Open working directory
    os.startfile(absoluteDirectory)

    batchSimSwap.title('Finished.')

# Prepare all given arguments into batchSimSwap object
def sortArguments():
    
    if batchSimSwap.dynamicFolderCheck(sys.argv[1], 'input') == True and batchSimSwap.dynamicFolderCheck(sys.argv[1], 'temp') == True:
        batchSimSwap.inputFolderNumber = sys.argv[1]
    else:
        raise SystemExit('\tThere was a problem creating / accessing the input folder.')    

    # Find given faces and files
    if(isinstance(sys.argv[2], str)):
        faceFilename = batchSimSwap.findFaceFilename(sys.argv[2])
        if(faceFilename):
            batchSimSwap.faces[1] = Face(sys.argv[2], faceFilename)
        else:
            raise Exception(' '.join(['Unable to find file for face 1',"\""+str(sys.argv[2])+"\""," is not a valid face."]))
    else:
        raise Exception('Face 1 is not a valid face string.')
    
    if(isinstance(sys.argv[3], str)):
        batchSimSwap.startTimeStamp = sys.argv[3]
    if(isinstance(sys.argv[4], str)):
        batchSimSwap.endTimeStamp = sys.argv[4]
        

def blockPrint():
    # sys.stdout = open(os.devnull, 'w')
    sys.stderr = open(os.devnull, 'w')

# Enable print again
def enablePrint():
    # sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__


# Get the input files from the input_X folder
def getInputFiles():
    inputvideos = []
    for file in pathlib.Path(batchSimSwap.getDynamicPath('input')).iterdir():
        if file.is_file():
            if '.mp4' in str(file):
                inputvideos.append(file)
            if '.webm' in str(file):
                newfilename = str(file).replace(".webm",".mp4")
                os.rename(file, newfilename)
                inputvideos.append(newfilename)
    
    return inputvideos

# Compile and run a simswap command with given files
def faceSwap(outputDirectory, videofile):

    success = True
    outputVideoFilename = os.path.basename(videofile)
    compiled_command = batchSimSwap.simswapCommands['video_swapsingle']
    compiled_command = compiled_command.replace('__input_selected_face__', os.path.join(batchSimSwap.getbatchSimSwapDirectoryOnly(),batchSimSwap.paths['input_faces'], batchSimSwap.faces[1].filename).replace("\\","/"))
    compiled_command = compiled_command.replace('__input_video_file__', '"' + str(videofile).replace('\\','/') + '"')
    compiled_command = compiled_command.replace('__output_file_name__', '"' + os.path.join(outputDirectory, outputVideoFilename) + '"')
    compiled_command = compiled_command.replace('__temp_folder_path__', '"' + batchSimSwap.getDynamicPath('temp') + '"')
  
    if(batchSimSwap.debugMode):
        print("\n\t SimSwap Compiled Command:")
        print("\n\t" + terminalColors.getString(compiled_command,'yellow', True)) 
        subprocess.run(compiled_command)
        # send2trash(os.path.join(outputDirectory, outputVideoFilename))
    else:
        subprocess.run(compiled_command)
        send2trash(str(videofile))
    
    return success

if __name__ == '__main__':
    main()
    




