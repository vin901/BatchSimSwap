
# File creation & System tools
import sys
import os
from os import path
from os import startfile

# BatchProcessing commands and setup
from batch.BatchSimSwap import BatchSimSwap
from batch.Face import Face
from batch.TerminalColors import TerminalColors


# BeautifulSoup & HTML scraping
from bs4 import BeautifulSoup
from lxml import etree
import requests

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

    # Swap Faces
    batchSimSwap.title("Swapping faces though " + str(len(input_files)) + " images..")
    runSuccess = True
    for index, imagefile in enumerate(input_files):
        sys.stdout.write("\t" + str(index+1) + ") " + terminalColors.getString(imagefile, 'blue') + " swapping with face "+terminalColors.getString("\"" + batchSimSwap.faces[1].face + "\"", 'purple'))
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



# Prepare all given arguments into batchProcessing object
def sortArguments():
    # Find given faces and files
    for faceNumber in range(1, 2):
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

    ## (string) Website URL
    try:
        if(isinstance(sys.argv[2], str)):
            batchSimSwap.url = sys.argv[2]
        else:
            raise SystemExit('Argument 2: URL is not a valid string.')
    except IndexError as e:
        print(' '.join(['Unable to find URL from argument 2',str(e)]))

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

            print("\tDownloading "+str(index) + ") " + str(file))
            inputimages.append(file)
                        
        return inputimages, outputFilePath
    except Exception as e:
            print(str(e))

# Compile and run a simswap command with given files
def faceSwap(directory, originalImage, imagePrefix):

    success = True
    input_image_file = '"' + directory + "\\" +  str(originalImage).replace('\\','/') + '"'
    output_path_name = '"' + directory + '"'
    output_file_name = '"' + str(imagePrefix) + "_" + os.path.basename(originalImage) + '"'
    compiled_command = batchSimSwap.simswapCommands['image_single']
    
    compiled_command = compiled_command.replace('__input_selected_face__', os.path.join(batchSimSwap.getbatchSimSwapDirectoryOnly(),batchSimSwap.paths['input_faces'], batchSimSwap.faces[1].filename).replace("\\","/"))
    compiled_command = compiled_command.replace('__input_image_file__', input_image_file)
    compiled_command = compiled_command.replace('__output_path_name__', output_path_name)
    compiled_command = compiled_command.replace('__output_file_name__', output_file_name)
  
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
    




