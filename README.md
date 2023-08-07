# BatchSimSwap: Simswap Over and Over again

## What it is
Simswap is a github repo that will take a single image of a face and overlay it onto a video or an image.  However the commands are clunky and not very intuitive, so I forked the repo to make it simple and easy to use.  There are lots of features here and more to come as I expand it.

## Installation
You can read the [Preparation Guide](https://github.com/neuralchen/SimSwap/blob/main/docs/guidance/preparation.md) here to get started, although I have written something a bit simpler as its not very clear what files go where.

1.  Install Anaconda
    * Anaconda manages your Python environment.  Go to the [Anaconda website](https://docs.anaconda.com/anaconda/install/) to download it and run through the installation. You'll be running all the BatchSimSwap commands from the Anaconda Prompt.

2. Start by running these commands
    * Run the following commands in an Anaconda Prompt window to set up an Anaconda Environment called ***batchsimswap***:
```
conda create -n batchsimswap python=3.6
conda activate batchsimswap
conda install pytorch==1.8.0 torchvision==0.9.0 torchaudio==0.8.0 cudatoolkit=10.2 -c pytorch

(optional): pip install --ignore-installed imageio
pip install insightface==0.2.1 onnxruntime 

(optional): pip install onnxruntime-gpu  
(If you want to reduce the inference time.  It will be diffcult to install onnxruntime-gpu, the specific version of onnxruntime-gpu will depend on your machine and cuda version.)

pip install send2trash beautifulsoup4 lxml pick python-dotenv instaloader
(BatchSimSwap needs these extra libraries)
```

3. Extra Files To Download (From the Preperation Guide)
    * These files have already been covered in the [Preparation Guide](https://github.com/neuralchen/SimSwap/blob/main/docs/guidance/preparation.md) (Which also has the links to download them) from SimSwap but it doesnt explain very clearly exactly where everything needs to be.

    * `arcface_checkpoint.tar`
        * This file (dont extract it) goes into a new folder called `./arcface_model/`
    * `checkpoints.zip`
        * This will need to be extracted and you'll also need to create a new folder called `./checkpoints/people/` where you'll extract the files (`iter.txt`, `latest_net_D1.pth` etc)
    * `antelope.zip`
        * Another folder you'll need to create: `./insightface_func/models/antelope` where you will extract the contents of `antelope.zip` (Should be two files: `glintr100.onnx` and `scrfd_10g_bnkps.onnx`)

4. Each time you run SimSwap you'll need to run:
    * `conda activate simswap` from the Anaconda Prompt and then `cd` (Change Directory) into the SimSwap directory where you cloned or extracted this repository.  Since Anaconda Prompt always starts in the Windows Users Directory (i.e C:\Users\james - if your user is called james) I always create a bat file that activates simswap, and changes directory to where I cloned this repository (for example I cloned into the Documents folder)
        * `conda activate simswap`
        * `cd C:\Users\james\Document\BatchSimSwap`
    * Then its easy to get started by running one of the commands listed below i.e. `bsvideo 1 james`
---

## Folder Structure
BatchProcessing has a designated folders where it stores all the faces that you'll use and also all outputs.  You can set these folders to somewhere different in the file `BatchSimSwap/BatchSimSwap.py`.  The special folders you need to take note of are:

**Folder**|**Location**|**Purpose**
:-----:|:-----:|:-----:
**input_faces**|`./BatchSimSwap/input_faces`|All simswap face files stored in here i.e. `input_faces/james.jpg`|
**input/input_1**|`./BatchSimSwap/input/input_1`|Place all video or images files to be processed in here.|
**output**|`./BatchSimSwap/output`|All output files will be written to this directory under a folder with the name of the face (i.e. `output/james/video1.mp4`)|

**Note:** If any of these folder's dont exist, they will be created automatically.

---

## Commands available
So far all the commands are written for Windows users, as I primarily run Simswap on Windows 11.  The commands at the moment are:

| Command    | Example                  | Description|
|------------|--------------------------|------------|
| **bsvideo** | `bsvideo 1 james`        | Looks for all the videos inside `./BatchSimSwap/input/input_1` and SimSwaps them with the face james from the `input_faces` folder |
| **bsimages** | `bsimages 1 james`        | Looks for all the images inside `./BatchSimSwap/input/input_1` and SimSwaps them with the face james from the `input_faces` folder |
| **bsurl**  | `bsurl james www.etc.com` | Downloads all the images from given URL and SimSwaps them with the face ***james*** from the `input_faces` folder.|
| **bsurl2**  | `bsurl2 james bob 3 www.etc.com` | Downloads all the images from given URL and SimSwaps them with the faces ***james*** and ***bob*** from the `input_faces` folder.  You must provide an ***IndexImage*** (preferably an image in the set where both people are looking towards the camera)|
| **bshelp** | `bshelp` | A helper file that will open folders and more.|

## Common Issues
I've run SimSwap every which way and back again and so I've come across a lot of common problems.  I've tried to list them below with some explanation of how to fix.

* 'Cannot find file': Files are not in the correct place
    * Check the above guide (***Extra Files***) and double check you have the files downloaded and in the correct place.  SimSwap is guaranteed to not work unless you have these files in the exact right folders.  If you are on OSX or Linux, try running the `download-weights.sh` file to automatically download and extract all the required files to the right place.  You'll need to install `wget` if you dont already have it.
* Getting SimSwap to work with your Graphics Card for faster results
    * SimSwap will absolutely work with your graphics card, but it requires a bit of time to get set up.  You'll most likely need to create an nVidia development account too.  You'll need to get the correct version of pytorch for your graphics card, and install Cuda Dev kit from the nVidia site. Someone posted a [handy video](https://www.youtube.com/watch?v=Tiq_vea5Eqg) (Its a long process, but it really helps) which I used here. (To get it running on a RTX 3080, I replaced `pip install onnxruntime-gpu` with `pip install onnxruntime-gpu==1.9.0`.)
