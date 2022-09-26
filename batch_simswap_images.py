
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

def main():
    global batchSimSwap, terminalColors
    batchSimSwap = BatchSimSwap()
    terminalColors = TerminalColors()

    os.system('cls')
    sortArguments()

    # Display Title
    inputFolderString = terminalColors.getString(os.path.join('.', batchSimSwap.getbatchSimSwapDirectoryOnly(), batchSimSwap.paths['input'], batchSimSwap.dynamicPaths['input']),'red').replace('\\','/')
    batchSimSwap.title("BatchSimSwap: Swap multiple images with a single face" + (' '+terminalColors.getString('(Debug Mode)', 'debug') if batchSimSwap.debugMode == True else ''))
    print(" ".join(['\tSwapping face', terminalColors.getString(batchSimSwap.faces[1].face,'face'), 'with images from ',inputFolderString]))

    # Get list of video files from folder
    
    batchSimSwap.title("Scanning Image Files..")
    input_files = getInputFiles()
    for index, imagefile in enumerate(input_files):
        print("\t" + str(index+1) + ") " + terminalColors.getString(os.path.basename(imagefile),'file'))
    absoluteDirectory = batchSimSwap.getDynamicPath('input')

    dayOfTheYear = str(datetime.now().strftime('%j'))
    timestamp = str(int(datetime.now().timestamp()))

    absoluteDirectory = batchSimSwap.createOutputFilePath([
        batchSimSwap.faces.get(1).face,
        dayOfTheYear,
        timestamp
    ])

    # Swap Faces
    batchSimSwap.title("Swapping faces though " + str(len(input_files)) + " files..")
    for index, imagefile in enumerate(input_files):
        sys.stdout.write("\t" + str(index+1) + ") Swapping " + terminalColors.getString(os.path.basename(imagefile),'file') + " with " + terminalColors.getString(batchSimSwap.faces[1].face, 'face'))
        faceSwap(absoluteDirectory, imagefile, index)

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

# Get the input files from the input_X folder
def getInputFiles():
    inputimages = []
    for file in pathlib.Path(batchSimSwap.getDynamicPath('input')).iterdir():
        if file.is_file():
            if '.jpg' in str(file).lower():
                inputimages.append(file)
            if '.png' in str(file).lower():
                inputimages.append(file)
    
    return inputimages

# Compile and run a simswap command with given files
def faceSwap(directory, imagefile, imagePrefix):

    success = True
    input_image_file = '"' + str(imagefile).replace('\\','/') + '"'
    output_path_name = '"' + directory + '"'
    output_file_name = '"' + str(imagePrefix) + "_" + os.path.basename(imagefile) + '"'
    compiled_command = batchSimSwap.simswapCommands['image_single']
    
    compiled_command = compiled_command.replace('__input_selected_face__', os.path.join(batchSimSwap.getbatchSimSwapDirectoryOnly(),batchSimSwap.paths['input_faces'], batchSimSwap.faces[1].filename).replace("\\","/"))
    compiled_command = compiled_command.replace('__input_image_file__', input_image_file)
    compiled_command = compiled_command.replace('__output_path_name__', output_path_name)
    compiled_command = compiled_command.replace('__output_file_name__', output_file_name)
  
    if(batchSimSwap.debugMode):
        print("\n\tReplaced compiled command")
        print("\n" + compiled_command + "\n") 
        subprocess.run(compiled_command)
        send2trash(os.path.join(directory, imagefile))
    else:
        result = subprocess.run(compiled_command, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        if   batchSimSwap.simswapCommandComplete in str(result.stdout):
            sys.stdout.write(' - ' + terminalColors.getString('Complete.', 'green', True))
        else: 
            sys.stdout.write(' - ' + terminalColors.getString('Error.', 'red', True))
            success = False
        send2trash(os.path.join(directory, imagefile))
    
    return success

if __name__ == '__main__':
    main()
    




