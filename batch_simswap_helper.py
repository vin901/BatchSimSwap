# BatchProcessing commands and setup
from batch.BatchSimSwap import BatchSimSwap
from batch.TerminalColors import TerminalColors
import sys
import os
from pick import pick
import pathlib
import cmd

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
        "\tOpen Input Folder",
        "\tOpen Input Faces Folder",
        "\tOpen Output Folder",
        "\t(Wizard) Batch Video",
        "\t(Wizard) Batch Video - Multi Specific",
        "\t(Wizard) Batch Images",
        "\t(Wizard) Batch URL",
        "\t(Wizard) Instagram Post",
    ]
    command = pick(options, title='Batch Processing Helper & Wizards', indicator='=>', multiselect=False)
    index = command[0][1]


    batchSimSwap.title('Batch Processing Helper & Wizards.')

    print("\tAvailable faces:")
    cli = cmd.Cmd()
    cli.columnize(faces, displaywidth=80)
    print()
    
    if(index == 0):
        print("\t>> Opening Input folder in Windows Explorer..")
        os.startfile(os.path.join(batchSimSwap.getbatchSimSwapDirectoryOnly(), batchSimSwap.paths['input']))

    elif(index == 1):
        print("\t>> Opening Input Faces folder in Windows Explorer..")
        os.startfile(os.path.join(batchSimSwap.getbatchSimSwapDirectoryOnly(), batchSimSwap.paths['input_faces']))

    elif(index == 2):
        print("\t>> Opening output folder in Windows Explorer..")
        os.startfile(os.path.join(batchSimSwap.getbatchSimSwapDirectoryOnly(), batchSimSwap.paths['output']))

    elif(index == 3):
        print("\t>> Batch Video Wizard")
        face = input("\tEnter the name of the face (filename, without extension): ")
        input_folder = input("\tThe single number for the input folder where files are kept: ")
        os.system(' '.join(['bsvideo', input_folder, face]))
                
    elif(index == 4):
        print("\t>> Batch Video - Multi Specific Wizard")
        face = input("\tEnter the name of the face (filename, without extension): ")
        input_folder = input("\tThe single number for the input folder where files are kept: ")
        timestamp = input("\tTimestamp for the index image (05:10) (mm:ss):")
        os.system(' '.join(['bsvideomulti', input_folder, face, timestamp]))
         
    elif(index == 5):
        print("\t>> Batch Images Wizard")
        face = input("\tEnter the name of the face (filename, without extension): ")
        input_folder = input("\tThe single number for the input folder where files are kept: ")
        os.system(' '.join(['bsimages', input_folder, face]))
        
    elif(index == 6):
        print("\t>> Batch URL Wizard")
        face = input("\tEnter the name of the face (filename, without extension): ")
        url = input("\tThe URL to scrape the images from: ")
        os.system(' '.join(['bsimages', face, "\""+url+"\""]))
        
    elif(index == 7):
        print("\t>> Batch URL (2 Faces)")
        face = input("\tEnter the name of the face (filename, without extension):")
        input_folder = input("\tThe single number for the input folder where files are kept:")

    elif(index == 8):
        print("\t>> Batch URL (3 Faces)")
        face = input("\tEnter the name of the face (filename, without extension):")
        input_folder = input("\tThe single number for the input folder where files are kept:")

    elif(index == 9):
        print("\t>> Instagram Post")


if __name__ == '__main__':
    main()
    