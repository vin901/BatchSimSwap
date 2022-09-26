
# File creation & System tools
import sys
import os
from os import path
from os import startfile
import pathlib

# BatchProcessing commands and setup
from batch.BatchSimSwap import BatchSimSwap
from batch.Face import Face
from batch.TerminalColors import TerminalColors

# Use instaloader to grab instagram content
from instaloader import Post, instaloader

# Get current day of the year
from datetime import datetime

# To run the command
import subprocess

# Send file to Recycle Bin
from send2trash import send2trash



def main():
    global batchProcessing, terminalColors
    batchProcessing = BatchProcessing()
    terminalColors = TerminalColors()
    
    os.system('cls')
    sortArguments()

    # Display Title
    batchProcessing.title("Single Face Swap from URL" + (' '+terminalColors.getString('(Debug Mode)', 'yellow') if batchProcessing.debugMode == True else ''))

    print(" ".join(['\tSwapping face', terminalColors.getString("\"" + batchProcessing.faces[1].face + "\"", 'purple'), 'with images downloaded from given URL.']))

    # Download Images from URL
    batchProcessing.title("Downloading Images")
    input_files, absoluteDirectory = downloadPictures(batchProcessing.url)

    # Swap Faces
    batchProcessing.title("Swapping faces though " + str(len(input_files)) + " images..")
    runSuccess = True
    for index, imagefile in enumerate(input_files):
        sys.stdout.write("\t" + str(index+1) + ") " + terminalColors.getString(imagefile, 'blue') + " swapping with face "+terminalColors.getString("\"" + batchProcessing.faces[1].face + "\"", 'purple'))
        success = faceSwap(absoluteDirectory, imagefile, index)
        if not success: runSuccess = False
        
    if not runSuccess:
        batchProcessing.title('Errors Found..', 'red')
        print(terminalColors.red)
        print('\tThere was errors when running the faceswap, try turning on debugMode  True in batch_processing/batch_processing.py to find out what is going wrong.')
        print('\n\tIf it was only one or two files, then it may just be alignment issues.  If all files are showing an error and none of them worked, then there is a problem with your simswap installation, or a possible bug in BatchSimSwap.  You can raise an issue at https://github.com/chud37/BatchSimSwap/issues')
        print(terminalColors.endColor)

    # Create link.url
    createLinkFile(absoluteDirectory)

    # Open working directory
    os.startfile(absoluteDirectory)

    batchProcessing.title('Finished.')



# Prepare all given arguments into batchProcessing object
def sortArguments():
    # Find given faces and files
    for faceNumber in range(1, 2):
        try:
            if(isinstance(sys.argv[faceNumber], str)):
                faceFilename = batchProcessing.findFaceFilename(sys.argv[faceNumber])
                if(isinstance(faceFilename, str)):
                    if(batchProcessing.debugMode == True): print("\tFound face from sys.argv " + str(faceNumber) + " face name: " + sys.argv[faceNumber])
                    batchProcessing.faces[faceNumber] = Face(sys.argv[faceNumber], faceFilename)
                else:
                    print(str(sys.argv))
                    raise SystemExit(' '.join(['Unable to find file for face',str(faceNumber),"\""+str(sys.argv[faceNumber])+"\" is not a valid face."]))
            else:
                raise SystemExit(' '.join(['Face',str(faceNumber)," is not a valid face string."]))
        except Exception as e:
            raise SystemExit('Unknown error: ' + str(e))

    ## (string) Website URL
    try:
        if(isinstance(sys.argv[2], str)):
            batchProcessing.url = sys.argv[2]
        else:
            raise SystemExit('Argument 2: URL is not a valid string.')
    except IndexError as e:
        print(' '.join(['Unable to find URL from argument 2',str(e)]))

# Download images from URL
def downloadPictures(postShortCode):

    outputFilePath = batchProcessing.createOutputFilePath([
        batchProcessing.faces.get(1).face,
        datetime.now().strftime('%j'),
        postShortCode
    ])

    outputFilePathRelative = os.path.join(
        batchProcessing.getbatchSimSwapDirectoryOnly(),
        batchProcessing.paths['output'],
        batchProcessing.faces.get(1).face,
        datetime.now().strftime('%j'),
        '{target}'
    ).replace('\\','/')

    instaLoader = instaloader.Instaloader(
        dirname_pattern=outputFilePathRelative,
        quiet=True,
        save_metadata=False,
        download_comments=False,
    )
    
    instagramUser = batchProcessing.getEnvironmentVar('INSTAGRAM_USERNAME')
    instagramPassword = batchProcessing.getEnvironmentVar('INSTAGRAM_PASSWORD')
    if(instagramUser != 'your_instagram_username') and (instagramPassword != 'your_instagram_password'):
        instaLoader.login(instagramUser, instagramPassword)        
        post = Post.from_shortcode(instaLoader.context, postShortCode)
        postDownload = instaLoader.download_post(post, target=postShortCode)
    else:
        raise SystemExit('\tError: You do not have INSTAGRAM_USER and INSTAGRAM_PASSWORD set in your .env.local file.')
    
    inputimages = []
    for file in pathlib.Path(outputFilePath).iterdir():
        if file.is_file():
            print("\tDownloaded: " + os.path.basename(file))
            inputimages.append(os.path.basename(file))
    
    return inputimages, outputFilePath


# Compile and run a simswap command with given files
def faceSwap(directory, originalImage, imagePrefix):

    success = True
    input_image_file = '"' + directory + "\\" +  str(originalImage).replace('\\','/') + '"'
    output_path_name = '"' + directory + '"'
    output_file_name = '"' + str(imagePrefix) + "_" + os.path.basename(originalImage) + '"'
    compiled_command = batchProcessing.simswapCommands['image_single']
    
    compiled_command = compiled_command.replace('__input_selected_face__', os.path.join(batchProcessing.getbatchSimSwapDirectoryOnly(),batchProcessing.paths['input_faces'], batchProcessing.faces[1].filename).replace("\\","/"))
    compiled_command = compiled_command.replace('__input_image_file__', input_image_file)
    compiled_command = compiled_command.replace('__output_path_name__', output_path_name)
    compiled_command = compiled_command.replace('__output_file_name__', output_file_name)
  
    if(batchProcessing.debugMode):
        print("\n\tReplaced compiled command")
        print("\n" + terminalColors.getString(compiled_command, 'purple', True) + "\n") 
        subprocess.run(compiled_command)
        send2trash(os.path.join(directory, originalImage))
    else:
        result = subprocess.run(compiled_command, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        if batchProcessing.simswapCommandComplete in str(result.stdout):
            sys.stdout.write(' - ' + terminalColors.getString('Complete.', 'green', True))
        else: 
            sys.stdout.write(' - ' + terminalColors.getString('Error.', 'fail', True))
            success = False
        send2trash(os.path.join(directory, originalImage))
    
    return success

# Create a link file to the original website provided
def createLinkFile(directory):
    # Create link.url
    batchProcessing.title("Creating link.url file")
    with (open(os.path.join(directory,'link.url'), 'w')) as f:
        f.write('[InternetShortcut]\n')
        f.write('URL='+batchProcessing.url+'\n')

if __name__ == '__main__':
    main()
    




