# BatchProcessing commands and setup
from batch.BatchSimSwap import BatchSimSwap
from batch.TerminalColors import TerminalColors
import sys
import os
from pick import pick
import pathlib
import cmd
import textwrap

def getFaces():
    faces = []
    for file in pathlib.Path(batchSimSwap.getPath('input_faces')).iterdir():
        if file.is_file():
            if '.jpg' in str(file).lower():
                faces.append(terminalColors.getString(os.path.basename(file)[:-4],'face'))
            if '.png' in str(file).lower():
                faces.append(terminalColors.getString(os.path.basename(file)[:-4],'face'))
    
    return faces

def main():
    global batchSimSwap, terminalColors
    batchSimSwap = BatchSimSwap()
    terminalColors = TerminalColors()
    
    faces = getFaces()

    os.system('cls')
    
    options = [
        "Open Input Folder",
        "Open Input Faces Folder",
        "Open Output Folder",
        "Open MultiSpecific Folder",
        "(Wizard) Batch Video",
        "(Wizard) Batch Video - Multi Specific",
        "(Wizard) Batch Images",
        "(Wizard) Batch URL",
        "(Wizard) Instagram Post",
        "Exit BatchSimSwap Helper"
    ]
    command = pick(options, title='Batch Processing Helper & Wizards', indicator='=>', multiselect=False)
    index = command[0][1]


    batchSimSwap.title('Batch Processing Helper & Wizards.')

    print("Available faces:")
    cli = cmd.Cmd()
    cli.columnize(faces, displaywidth=110)
    print()
    
    if(index == 0):
        print(">> Opening Input folder in Windows Explorer..")
        os.startfile(os.path.join(batchSimSwap.getbatchSimSwapDirectoryOnly(), batchSimSwap.paths['input']))

    elif(index == 1):
        print(">> Opening Input Faces folder in Windows Explorer..")
        os.startfile(os.path.join(batchSimSwap.getbatchSimSwapDirectoryOnly(), batchSimSwap.paths['input_faces']))

    elif(index == 2):
        print(">> Opening output folder in Windows Explorer..")
        os.startfile(os.path.join(batchSimSwap.getbatchSimSwapDirectoryOnly(), batchSimSwap.paths['output']))

    elif(index == 3):
        print(">> Opening multispecific folder in Windows Explorer..")
        os.startfile(os.path.join(batchSimSwap.getbatchSimSwapDirectoryOnly(), batchSimSwap.paths['multispecific']))
        
    elif(index == 4):
        print(">> Batch Video Wizard")
        face = input("Enter the name of the face (filename, without extension): ")
        input_folder = input("The single number for the input folder where files are kept: ")
        os.system(' '.join(['bsvideo', input_folder, face]))
                
    elif(index == 5):
        print(">> Batch Video - Multi Specific Wizard")
        batchSimSwap.indentParagraph('Unfortunately due to the finicky nature of multi specific video it is not practical to perform batch operations.  Each video needs a list of faces, a timestamp to create an indexImage from (to extact the faces) and a video file.  Because batch functionality is not possible with multispecific video files, I\'ve opted to make the process a lot simpler instead.  Warning: Only run one multispecific command at a time as they use one directory.','yellow')
        face = input("Enter the name of the face (filename, without extension): ")
        input_folder = input("The single number for the input folder where files are kept: ")
        timestamp = input("Timestamp for the index image (05:10) (mm:ss):")
        os.system(' '.join(['bsvideomulti', input_folder, face, timestamp]))
         
    elif(index == 6):
        print(">> Batch Images Wizard")
        face = input("Enter the name of the face (filename, without extension): ")
        input_folder = input("The single number for the input folder where files are kept: ")
        os.system(' '.join(['bsimages', input_folder, face]))
        
    elif(index == 7):
        print(">> Batch URL Wizard")
        face = input("Enter the name of the face (filename, without extension): ")
        url = input("The URL to scrape the images from: ")
        os.system(' '.join(['bsimages', face, "\""+url+"\""]))
        
    elif(index == 8):
        print(">> Batch URL (2 Faces)")
        face = input("Enter the name of the face (filename, without extension):")
        input_folder = input("The single number for the input folder where files are kept:")

    elif(index == 9):
        sys.exit()


if __name__ == '__main__':
    main()
    