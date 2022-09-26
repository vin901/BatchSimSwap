# BatchProcessing commands and setup
from batch import BatchProcessing
import sys
import os
from pick import pick


def main():
    batchProcessing = BatchProcessing()

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
    option, index = pick(options, title='Batch Processing Helper & Wizards', indicator='=>', multiselect=False)

    if(index == '1'):
        print("\t>> Opening Input folder in Windows Explorer..")
        os.startfile(os.path.join(batchProcessing.getbatchSimSwapDirectoryOnly(), batchProcessing.paths['input']))

    elif(index == '2'):
        print("\t>> Opening Input Faces folder in Windows Explorer..")
        os.startfile(os.path.join(batchProcessing.getbatchSimSwapDirectoryOnly(), batchProcessing.paths['input_faces']))

    elif(index == '3'):
        print("\t>> Opening output folder in Windows Explorer..")
        os.startfile(os.path.join(batchProcessing.getbatchSimSwapDirectoryOnly(), batchProcessing.paths['output']))

    elif(index == '4'):
        print("\t>> Batch Video Wizard")
        face = input("\tEnter the name of the face (filename, without extension):")
        input_folder = input("\tThe single number for the input folder where files are kept:")

    elif(index == '5'):
        print("\t>> Batch Video - Multi Specific Wizard")
        face = input("\tEnter the name of the face (filename, without extension):")
        input_folder = input("\tThe single number for the input folder where files are kept:")
        timestamp = input("\tTimestamp for the index image (05:10) (mm:ss):")

    elif(index == '6'):
        print("\t>> Batch Images Wizard")
        face = input("\tEnter the name of the face (filename, without extension):")
        input_folder = input("\tThe single number for the input folder where files are kept:")

    elif(index == '7'):
        print("\t>> Batch URL Wizard")
        face = input("\tEnter the name of the face (filename, without extension):")
        input_folder = input("\tThe single number for the input folder where files are kept:")

    elif(index == '8'):
        print("\t>> Batch URL (2 Faces)")
        face = input("\tEnter the name of the face (filename, without extension):")
        input_folder = input("\tThe single number for the input folder where files are kept:")

    elif(index == '9'):
        print("\t>> Batch URL (3 Faces)")
        face = input("\tEnter the name of the face (filename, without extension):")
        input_folder = input("\tThe single number for the input folder where files are kept:")

    elif(index == '10'):
        print("\t>> Instagram Post")


if __name__ == '__main__':
    main()