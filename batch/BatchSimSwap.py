import sys
import os
from os import path
import pathlib
from pathlib import Path
from dotenv import dotenv_values
from .TerminalColors import TerminalColors


class BatchSimSwap():

    url = ''
    indexImage = 1
    indexImageFile = ''
    debugMode = False
    inputFolderNumber = 1
    
    paths = {
        'input_faces':  'input_faces',
        'input':        'input',
        'output':       'output',
    }

    dynamicPaths = {
        'input':    'input_',
        'temp':     'temp_results_',
    }

    simswapCommands = {
        'image_single':                 "python test_wholeimage_swapmulti.py --crop_size 224 --use_mask  --name people --Arc_path arcface_model/arcface_checkpoint.tar --pic_a_path ./__input_selected_face__ --pic_b_path __input_image_file__ --output_path __output_path_name__ --output_filename __output_file_name__  --no_simswaplogo",
        'video_swapsingle':             "python test_video_swapsingle.py --isTrain false --use_mask --name people --Arc_path arcface_model/arcface_checkpoint.tar --pic_a_path ./__input_selected_face__ --video_path __input_video_file__ --output_path __output_file_name__ --temp_path __temp_folder_path__ --no_simswaplogo",
        'image_multispecific':          "python test_wholeimage_swap_multispecific.py --crop_size 224 --use_mask  --name people --Arc_path arcface_model/arcface_checkpoint.tar --pic_b_path __input_image_file__ --output_path __output_path_name__ --output_filename __output_file_name__ --multisepcific_dir __multi_specific_path__  --no_simswaplogo",
        'video_swap_multispecific':     "python test_video_swap_multispecific.py --isTrain false --use_mask --name people --Arc_path arcface_model/arcface_checkpoint.tar --video_path __input_video_file__ --output_path __output_file_name__ --temp_path ./temp_results --multisepcific_dir __multi_specific_path__ --no_simswaplogo",
    }
    
    simswapCommandComplete = '************ Done ! ************'

    faces = {}
    env = {}

    def __init__(self):
        self.terminalColors = TerminalColors()
        self.getEnvironmentData()
        self.parseEnvironmentData()
        self.folderChecks()
        
        

    def folderChecks(self):
        for key, directory in self.paths.items():
            absolutePath = os.path.join(self.getAbsoluteDirectory(), directory)
            if not self.pathExists(absolutePath):
                print('\tFolder doesnt exist: ' + absolutePath)
                self.createDirectory(absolutePath)

    def dynamicFolderCheck(self, dynamicFolderNumber, dynamicPathString):
        dynamicPath = False
        if dynamicPathString in self.dynamicPaths:
            dynamicPath = self.dynamicPaths.get(dynamicPathString)

        absolutePath = os.path.join(self.getAbsoluteDirectory(), self.getPath('input'), dynamicPath + str(dynamicFolderNumber))
        if self.pathExists(absolutePath):
            self.dynamicPaths.update({dynamicPathString: dynamicPath + str(dynamicFolderNumber)})
            return True
        else:
            print('\tFolder doesnt exist: ' + absolutePath)
            if self.createDirectory(absolutePath):
                self.dynamicPaths.update({dynamicPathString: dynamicPath + str(dynamicFolderNumber)})
                return True
            else:
                return False
    
    
    def getbatchSimSwapDirectoryOnly(self):
        return os.path.basename(os.path.dirname(__file__))

    def getAbsoluteDirectory(self):
        return os.path.dirname(os.path.realpath(__file__))

    def pathExists(self, directory):
        if not path.exists(os.path.abspath(directory)):
            return False
        return True

    def createDirectory(self, directory):
        if not path.exists(directory):
            try:
                os.mkdir(directory.replace('\\','/'))
                return True
            except:
                raise SystemExit("[ Unable to create directory: ",directory," program fail. ]")
                return False

    def createOutputFilePath(self, newFilePaths):
        createDirectory = []
        for directory in newFilePaths:
            createDirectory.append(directory)
            # *createDirectory splat operator
            absolutePath = os.path.join(self.getAbsoluteDirectory(), self.paths['output'], *createDirectory)
            if not self.pathExists(absolutePath):
                self.createDirectory(absolutePath)
        return os.path.join(self.getAbsoluteDirectory(), self.paths['output'], *createDirectory)

    def getPath(self, batchPath):
        if(batchPath in self.paths):
            return os.path.join(self.getAbsoluteDirectory(), self.paths[batchPath])
        return False
    
    def getDynamicPath(self, dynamicPathString):
        if dynamicPathString in self.dynamicPaths:
            return os.path.join(self.getAbsoluteDirectory(), self.getPath('input'), self.dynamicPaths[dynamicPathString])
        return False
    
    def findFaceFilename(self, face, absolute = False):
        inputFacesPath = self.getPath('input_faces')
        if(inputFacesPath != False):
            for file in pathlib.Path(inputFacesPath).iterdir():
                if file.is_file():
                    if face in str(file):
                        if(absolute == True):
                            return file
                        else:
                            return os.path.basename(file)
            return False
        else:
            raise Exception('Unable to locate input_faces path in batch_processing folder.')    

    def title(self, str, color = 'cyan'):
        print("\n\t"+self.terminalColors.getString(str, color))
        print("\t------------------------------")

    def getEnvironmentData(self) -> dict:
        environmentFileLocal = os.path.join(self.getAbsoluteDirectory(),'.env.local')
        environmentFileDist = os.path.join(self.getAbsoluteDirectory(),'.env.dist')
        if self.pathExists(environmentFileLocal):
            self.env = dotenv_values(environmentFileLocal)
        else:
            source = Path(environmentFileDist)
            destination = Path(environmentFileLocal)
            destination.write_bytes(source.read_bytes())
            self.env = dotenv_values(environmentFileLocal)


    def getEnvironmentVar(self, var) -> str:
        for key, value in self.env.items():
            if key == var:
                return value
        return ''

    def parseEnvironmentData(self):
        
        # path_input = self.getEnvironmentVar('PATH_INPUT')
        self.paths['input'] = self.getEnvironmentVar('PATH_INPUT') if self.getEnvironmentVar('PATH_INPUT') != '' else self.paths['input']
        self.paths['output'] = self.getEnvironmentVar('PATH_OUTPUT') if self.getEnvironmentVar('PATH_OUTPUT') != '' else self.paths['output']
        self.paths['input_faces'] = self.getEnvironmentVar('PATH_INPUT_FACES') if self.getEnvironmentVar('PATH_INPUT_FACES') != '' else self.paths['input_faces']
        self.dynamicPaths['input'] = self.getEnvironmentVar('DYNAMIC_PATH_INPUT') if self.getEnvironmentVar('DYNAMIC_PATH_INPUT') != '' else self.dynamicPaths['input']
        self.dynamicPaths['temp'] = self.getEnvironmentVar('DYNAMIC_PATH_TEMP') if self.getEnvironmentVar('DYNAMIC_PATH_TEMP') != '' else self.dynamicPaths['temp']
        self.debugMode = True if self.getEnvironmentVar('DEBUG_MODE') == 'True' else self.debugMode
