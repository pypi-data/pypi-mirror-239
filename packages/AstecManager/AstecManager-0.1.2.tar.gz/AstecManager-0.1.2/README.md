## This library has been created to automatize and help users to segment using ASTEC software.
It will include tools to:
* enhance the data (contour computation, etc ...)
* manage the data (download and upload to distant storage, automatic compression, reduce size)
* segment the data (examples , etc ...)
* plot properties of the embryo data


# Table of contents 

1. [Downloads](#download)
2. [Installation](#install)
3. [Update](#update)
4. [Raw images management](#rawimages)
5. [Raw images troubleshooting](#rawimages-troubleshooting)
6. [Integration of data manager](#data-manager-integration)
7. [Fusion](#fusion)
8. [Fusion parameters tuning](#fusion-parameters-test)
9. [Fusion final run](#fusion-final-run)
10. [Fusion verification](#fusion-verification)
11. [Fusion troubleshooting](#fusion-troubleshooting)
12. [Data downscaling (optional)](#data-downscaling-optional)
13. [Deep learning backgrounds (optional)](#backgrounds-optional)
14. [Dataset contours (optional)](#contours-optional)
15. [First time point segmentation (MARS)](#segmentation-of-first-time-point)
16. [MARS verification](#mars-verification)
17. [Install MorphoNet](#install-morphonet)
18. [Detect segmentation errors](#detect-segmentation-errors)
19. [Fix segmentation errors](#fixing-segmentation-errors)
20. [Segmentation propagation](#propagation-of-the-segmentation)
21. [First step : segmentation tests](#segmentation-parameters-test)
22. [Segmentation test verification](#segmentation-test-verification) 
23. [Verification with astecmanagaer](#comparison-with-astecmanager)
24. [Verification with MorphoNet](#comparison-with-morphonet)
25. [Segmentation run](#segmentation-production-run)
26. [Alignment of all images](#images-alignment)
27. [Properties computation](#properties-computation)

## Download

* This tool will later be published on the pip python package management system. Doing so , it will be an easy install with 3 lines. For now , you have to follow the following steps :


* Using GIT , you can start a terminal in a folder you will not delete and run : `git clone https://gite.lirmm.fr/bgallean/astecamanager.git`
* Or heads to [this link](https://gite.lirmm.fr/bgallean/astecmanager), click on the download button and than "zip". Finally unzip it inside a folder named : "astecmanager"

## Install

you need to install conda on your computer
you can find a guide to install conda [here](/https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) 

Now that conda is installed,  open a new terminal in "astecmanager" folder created during the download step, and run in a terminal , line by line the following :

`conda create -n AstecManager -c ome python=3.6 zeroc-ice36-python omero-py` \
`conda activate AstecManager` \
`python3.6 -m pip install AstecManager` \
`python3.6 -m pip install matplotlib`\
`python3.6 -m pip install h5py`\
`python3.6 -m pip install opencv-contrib-python`
`python3.6 -m pip install dataclasses`



All the libraries are now installed, you can install the manager tool with this command, ran in a terminal inside the astecmanager folder :

`conda activate AstecManager` \
`pip install -e .` 

## Update

Often, the tool will be updated to add features, and debug the existing ones. 

* If the tool has been installed using pip , you can simply start a terminal in the astecmanager folder and run :
`conda activate AstecManager` \
`pip install astecmanager --upgrade` \

* If the tool has been downloaded by git , open a new terminal in the "astecmanager" folder and run :

`conda activate AstecManager` \
`git pull` \
`pip install -e .` 


## A complete example to use the pipeline

This example serves as a step-by-step guide on how to successfully convert data from the microscope into a precise 3D representation that can be used for in-depth analysis without any mistakes. It's designed specifically for our team's models and may not be suitable for your own data.

### Microscope 


We collect data using a special microscope called SPIM. This microscope has two cameras that work together and two lasers that provide light for imaging. The entire system, including the cameras and lasers, can rotate 90 degrees and capture images again.

When we complete these two sets of acquisitions, we end up with a total of four images for one point in the embryo's development. Each of these images has high-quality information for the part of the embryo that's close to the camera. However, the parts farther away from the camera are of lower quality because they are more distant. This is why we obtain four images for a single time point: to capture as much information as possible.

After we capture these images, we store the data in the microscope computer.

``` 
<find the folder name>
└───<find the folder name>
   └───<date of the day>
       │───raw
       │───bdv.h5 <= useless
       │───bdv.xml <= useless
       └───main_raw.lux.h5 <= useless
```


We can't use the microscope computer for calculations; it's only for capturing images. So, you'll need to transfer the raw images to the computer that will process them.

To do this, both computers are connected using a high-speed 10-gigabit per second (Gb/s) Ethernet cable. You can access the storage location on the segmentation computer, which has an address that starts with "10.5.0.161". It will be mounted as a folder on the machine.
Inside that, you'll find the acquisition folder.

Copy this folder to your experimentation folder and rename it with the name you want to give to the embryo. Also, remember to rename the "raw" folder to "RAWDATA" for the next steps.

### Rawimages

For now , your hierarchy should look like this :

``` 
experiment folder 
└───embryo specie
     └──embryo name
         └────RAWDATA
               │───stack_0_channel_0_obj_left
               │    │ Cam_Left_00XXX.h5
               │    │ Cam_Left_00XXX.h5
               │    └ ...
               │───stack_0_channel_0_obj_right
               │    │ Cam_Right_00XXX.h5
               │    │ Cam_Right_00XXX.h5
               │    └ ...
               │───stack_1_channel_0_obj_left
               │    │ Cam_Left_00XXX.h5
               │    │ Cam_Left_00XXX.h5
               │    └ ...
               └───stack_1_channel_0_obj_right
                   │ Cam_Right_00XXX.h5
                   │ Cam_Right_00XXX.h5
                   └ ...
```
Here, you can see that the Raw Images are organized into various folders. This particular structure is used by our team. If your data organization is different, please remember this when setting up the parameters for the fusion step.

These four different folders represent various stages of image acquisition:

- "stack_0_channel_0_obj_left" contains images from the left camera before any rotation.
- "stack_0_channel_0_obj_right" contains images from the right camera before any rotation.
- "stack_1_channel_0_obj_left" contains images from the left camera after the rotation.
- "stack_1_channel_0_obj_right" contains images from the right camera after the rotation.

##### *RawImages Troubleshooting*

The fusion step won't function correctly if your Raw images have multiple file extensions. For instance, the microscope generates images with names like "Cam_Right_00XXX.lux.h5," but you want them to be named "Cam_Right_00XXX.h5."

To solve this problem, you can automatically rename all the images in your folder using your computer's operating system:

* Select all the images.
* Right-click and choose "Rename."
* Search for ".lux" and replace it with nothing (leave it empty).

![Rename Raw Images](doc_images/rename_raw.png)

This way, you'll have the images with the desired names for the fusion step to work smoothly.

### Data Manager Integration

To store the data for further work and archives , the team uses a data manager called OMERO.
In the following pipeline, you will be able to upload the different data produced to OMERO , automatically.

In order to upload, you first need to create a file on your computer, somewhere no one can access and that you should not share !

The file should contain the following lines : 

```
host=adress.to.omero.instance
port=omero.port (usually 4064)
group=your team group
secure=True
java_arg=java
login=your omero login
password=your omero password
```

Save this file with the name you want, I prefer to use : omero_config.txt , and than copy the complete path to the file somewhere you can access.

In the following steps, to upload a data you produce, you will need to copy this path to the parameter "omero_config_file". I will explain this step everytime it will be needed.

### Fusion


The most crucial part of this process is combining the images, and it needs to be done quickly. You should begin this step right after copying the large Raw Images, and try to finish it as soon as you can.

These Raw Images are very large, roughly 3 gigabytes each. This means that if you're working with one time point, it will use up about 12 gigabytes of computer memory. Think about it this way: if you're dealing with an embryo at 300 different time points and you have multiple channels of images, your Raw Images folder could take up as much as 2 to 3 terabytes of space on your computer's hard drive.

Additionally, the Raw Images often have a significant amount of background information, which takes up a lot of memory. This background includes unnecessary data.

The fusion step is designed to address the problems we've just talked about:

- It keeps the most valuable information from each camera angle to create an isotropic image. An isotropic image means that it has the same characteristics, like intensity, across all regions.

- It reduces the memory needed for a single time point from around 12 gigabytes to a more manageable 500 megabytes.

- It also trims the image around the embryo, cutting out the excessive background and keeping only the essential information.

For more details about this step , please follow [this link](https://astec.gitlabpages.inria.fr/astec/astec_fusion.html#fusion-method-overview)

I would advise to split fusion in 2 steps 
* A test step where you will find the best parameters for this specific dataset.
* A production step where you will apply the best parameters to the complete dataset.

Before starting anything , please copy the example files located in "astec/examples_files/" , into the folder containing your embryo folder (inside your experiment folder)

* fuse_test.py
* fuse_prod.py (if your embryo has 2 channels , please copy fuse_prod_2_channels.py)

* Your folder hierarchy should now look like this

``` 
experiment folder 
│───embryo specie
│    │──embryo name
│    │   └───RAWDATA
│    │       │───stack_0_channel_0_obj_left
│    │       │───stack_0_channel_0_obj_right
│    │       │───stack_1_channel_0_obj_left
│    │       └───stack_1_channel_0_obj_right
│    │── fuse_test.py
│    └── fuse_prod.py
```

#### Fusion parameters test

Please open the fuse_test.py file in a text editor
This file is divided into several sections, but you only need to modify two of them.

First, you'll want to link the name of the embryo and the specific time point you want to test the fusion for. To select a time point, pick one that's roughly in the middle of the embryo's development. For instance, if your embryo timeline goes from 0 to 79, you could choose time point 40 as an example.

```
embryo_name = "embryo_name"
begin=40
end=40
```
Please make sure that the embryo_name in the file (and for all the following files), is the exact same than the embryo folder name! It can contain uppercase letter.

The second section to modify is the following :

```
parameters["DIR_RAWDATA"]= "'RAWDATA'"  
parameters["DIR_LEFTCAM_STACKZERO"]= "'stack_0_channel_0_obj_left'"
parameters["DIR_RIGHTCAM_STACKZERO"]= "'stack_0_channel_0_obj_right'"
parameters["DIR_LEFTCAM_STACKONE"]= "'stack_1_channel_0_obj_left'"
parameters["DIR_RIGHTCAM_STACKONE"]= "'stack_1_channel_0_obj_right'"
parameters["acquisition_leftcam_image_prefix"]= "'Cam_Left_000'"
parameters["acquisition_rightcam_image_prefix"]= "'Cam_Right_000'"
```

The parameter "DIR_RAWDATA" is the name of the folder containing the Raw Images , if you followed the tutorial it should be "RAWDATA"
The parameter "DIR_LEFTCAM_STACKZERO" is the name of the folder containing images from the left camera before any rotation
The parameter "DIR_RIGHTCAM_STACKZERO" is the name of the folder containing images from the right camera before any rotation
The parameter "DIR_LEFTCAM_STACKONE" is the name of the folder containing images from the left camera after rotation
The parameter "DIR_RIGHTCAM_STACKONE" is the name of the folder containing images from the right camera after rotation

The parameter "acquisition_leftcam_image_prefix" and "acquisition_rightcam_image_prefix" is the name of the image without any extension

Once you've configured all the necessary settings, you're ready to begin the fusion process. If the test is split into four tries, it's because we need to assess the combination of two parameters:

The first parameter is called "fusion_strategy," and it has two values that affect how the computation's output is generated:

- If you set it to "direct-fusion," the images will be combined using the left camera's image before rotation as the reference.
- If you set it to "hierarchical-fusion," the images from both cameras before rotation will be combined, then the images after rotation will also be combined, and finally, these two resulting images will be combined to produce the final image.


|                              Schema of direct-fusion                              |                             Schema of hierarchical-fusion                             |
|:---------------------------------------------------------------------------------:|:-------------------------------------------------------------------------------------:|
| ![Image of direct-strategy summary schema](doc_images/fusion-direct-strategy.png) | ![Image of hierarchical-strategy schema](doc_images/fusion-hierarchical-strategy.png) |
*Schemas by G. Malandain,  INRIA - Morpheme team*

The second parameter is "acquisition_orientation," which can be set to either "right" or "left." This parameter corresponds to how the camera is rotated to capture the second set of images. Once you set it to a specific value, it should remain consistent for all subsequent acquisitions conducted by the experimenter.

|                   Left acquisition schema                    |                    Right acquisition schema                    |
|:------------------------------------------------------------:|:--------------------------------------------------------------:|
| ![Left acquisition microscope sequence](doc_images/left.png) | ![Right acquisition microscope sequence](doc_images/right.png) |
*Schemas by G. Malandain,  INRIA - Morpheme team*

Remember, you don't have to manually change the values of "fusion-strategy" and "acquisition_orientation" during the testing phase. These adjustments are made automatically as part of the fusion test computation.

Once you've configured the parameters for the name and time points, you're ready to initiate the fusion test.

Here are the steps to follow:

- Open a terminal within the folder where the "fuse_test.py" file is located.

-In this terminal, run the following commands one by one:

`conda activate AstecManager` \
`python3 fuse_test.py`

- Now, you can wait for the code execution to finish.

After completing the fusion test, your folders should appear as described below : 

``` 
experiment folder 
└───embryo specie
     │──embryo name
     │    │───RAWDATA
     │    │    └─── ...
     │    └───FUSE
     │        │─── FUSE_01_left_direct
     │        │  │─── embryo_name_fuse_t040.nii
     │        │  └─── ... 
     │        │─── FUSE_01_left_hiearchical
     │        │  │─── embryo_name_fuse_t040.nii
     │        │  └─── ... 
     │        │─── FUSE_01_right_direct
     │        │  │─── embryo_name_fuse_t040.nii
     │        │  └─── ... 
     │        └─── FUSE_01_right_hiearchical
     │           │─── embryo_name_fuse_t040.nii
     │           └─── ... 
     │─ fuse_test.py
     └─ fuse_prod.py
```


To discover the optimal parameter set, you should load each "embryo_name_fuse_t040.nii" image into Fiji by simply dragging and dropping it. When you drag an image into Fiji, remember to rename it according to the corresponding fusion folder. This way, you'll keep track of which image corresponds to which parameters.

Here's how to rename an image in Fiji:

- Click on the window displaying the image you want to rename.
- Go to the top menu labeled "Image"
- Select the "Rename" option from the dropdown menu.
- A popup will appear. Type in the new name and save the changes

![Rename menu](doc_images/rename_image.png)

After you've loaded and renamed the four images, it's important to synchronize them so that you can explore them together. To do this, you can use the synchronization tool with these steps:

- Go to the top menu and click on "Analyze"
- From the dropdown menu, select "Tools"
- Then, choose "Synchronize window"
- In the window that appears, click on "Synchronize all"

![Synchronize menu](doc_images/sync_windows.png)

Now, when you move through the different depths of one image using the slider beneath its window, you'll notice that all four images will simultaneously adjust to the same depth.

The images are probably really bright, because Fiji is not able to adapt to the image high contrast to thoroughly analyze the images, you may also need to automatically adjust it : 

- Click on the window displaying the image you want to adjust.
- Go to the top menu and click on "Image"
- From the dropdown menu, select "Tools"
- Then, choose "Brightness/Contrast"
- Finally click on "Auto , for each image

![Auto contrast and brightness](doc_images/brightness_and_contrast.png)

After updating the contrast of all images, you will be able to see which fusion is good, and which one isn't good. 

| Example of correct fusion | Example of fusion with wrong rotation |
|:-------------------------:|:-------------------------------------:|
| ![](doc_images/file.jpg)  |       ![](doc_images/file.jpg)        |

When you spotted the correct fusion, please note the parameters values , to be able to use them in the production step.


### Fusion final run

To get the production process working, you have to take the settings you chose in the test file and use them. To do this, just open the "fuse_prod" file you copied earlier, and then copy these lines from the test file:


```
parameters["DIR_RAWDATA"]= .... 
parameters["DIR_LEFTCAM_STACKZERO"]= ....
parameters["DIR_RIGHTCAM_STACKZERO"]= ....
parameters["DIR_LEFTCAM_STACKONE"]= ....
parameters["DIR_RIGHTCAM_STACKONE"]= ....
parameters["acquisition_leftcam_image_prefix"]= ....
parameters["acquisition_rightcam_image_prefix"]= ....
```

and copy the following lines from the test instance that worked , still in the fuse_test file :
``` 
parameters["fusion_strategy"]= ....
parameters["acquisition_orientation"]= ....
``` 
When done you can start the complete fusion
open a new terminal in the "root" folder (the folder containing your embryo folder) and run, line by line :

`conda activate AstecManager` \
`python3 fuse_prod.py`

While the fusion is processing, you can delete the following :
- folder FUSE/FUSE_01_left_direct
- folder FUSE/FUSE_01_left_hiearchical 
- folder FUSE/FUSE_01_right_direct 
- folder FUSE/FUSE_01_right_hiearchical 
- and the 2 python files "fuse_test.py", "fuse_post.py"

The final folder architecture after fusion will be this one :

``` 
experiment folder 
└───embryo specie
    │──embryo name
    │   │───analysis
    │   │    └─── fusion_movie.mp4
    │   │───INTRAREG
    │   │    └─── ...
    │   │───RAWDATA
    │   │    └─── ...
    │   └───FUSE
    │       └─── FUSE_01
    │          │─── embryo_name_fuse_t000.nii
    │          │─── embryo_name_fuse_t001.nii
    │          └─── ... 
    │─── fuse_test.py
    └─── fuse_prod.py
```




### Fusion verification

Once the fusion production process is done, a special step will happen on its own. This step helps you make sure that the fusion was done correctly throughout the embryo's development. This special step creates 2 new folder called "INTRAREG" and "analysis".

We will not use the intraregistration folder, and find inside the "analysis" folder, a video called "fusion_movie.mp4." You can watch this video to see how the fusion processed over time. If the fusion is indeed correct, then this first step is all done.
<<<<<<<!!!!!!!!!!!!!!!!!!! Break here for rework of document !!!!!!!!!!!!!!!!!!>>>>>>>>>>>>>>


##### *Fusion Troubleshooting*</ins>*

The troubleshooting of incorrect fusion results can be done thanks to multiple data that are extracted during the tests. 
Inside each fusion folder , you can find a folder called "XZSECTION_XXX" where "XXX" is the time point fused. 
Inside the folder , you will see 4 images : 

- embryoname_xyXXXX_stack0_lc_reg.mha
- embryoname_xyXXXX_stack0_lc_weight.mha
- embryoname_xyXXXX_stack0_rc_reg.mha
- embryoname_xyXXXX_stack0_rc_weight.mha
- embryoname_xyXXXX_stack1_lc_reg.mha
- embryoname_xyXXXX_stack1_lc_weight.mha
- embryoname_xyXXXX_stack1_rc_reg.mha
- embryoname_xyXXXX_stack1_rc_weight.mha

|       Left-cam stack 0 reg + weighting       |       Stack cameras matching        |       Stack 0 and 1 matching       |
|----------------------------------------------|-------------------------------------|------------------------------------|
| ![](doc_images/fuse_extraction_lcstack0.png) | ![](doc_images/leftandrightcam.png) | ![](doc_images/stacksmatching.png) |

On the left image  of the table you can see that the registration image (left), is matching the weighting used for the computation. It means that the weighting is correct.
On the middle image , you can see that the left camera and right camera of the same stack is matching.
On the right image, you can see that both stacks images are matching , so the fusion will be correct.

If none of the fusions test instances give good result , it means that you will have to tune other parameters. After every change, delete the FUSE folder, and starts again the fuse_test file
If the weighting in the extracted images seem incorrect, you should use this parameter :

* parameters["fusion_weighting"]= "'guignard'" , set it to "'uniform'" , "'ramp'" or "'corner'"

If your embryo seems to be cropped , or the image does not have an embryo inside , you should change this parameter :

* parameters["raw_crop"]= "True" set it to "False"

If one of the stack in the fused image seems to be flipped comparing to what she should look like , use this parameter

* parameters["acquisition_mirrors"]= "False" set it to "True"

If despite all of your test, the fusion seems impossible , please verify these 3 things : 

* Verify that the data parameters are bound correctly. They shouldn't change between experiments (folders should have the same names) , but a mistake in the folders can happen
* Make sure the raw images folders is named : RAWDATA
* Open the different images for the same time point in Fiji , and verify that they match (find part of the image that you can find on others stacks and cameras too)
  _(To import a Raw image in Fiji , click on File > Import > HDF5 , and find your image)_


For more details on a parameter, please [click here](https://astec.gitlabpages.inria.fr/astec/astec_parameters.html#astec-fuse-parameters)  

## Data downscaling _(optional)_

The following steps of the pipeline can be really long (the segmentation can take 2 weeks depending on your data). We found a way to accelerate the computation by downscaling the fusion images by 2.
We than send the downscaled fusions to the data management system for further computations 

We will use the following script : morphoomero/pipeline_tools/fused_downscale_omero.py
To use it , we first need to edit the file configuring OMERO. for this open morphoomero/pipeline_tools/omero_config.txt

* host=omero.mri.cnrs.fr (path to your omero instance)
* port=4064 (should be the default port for any instance)
* group=Faure Lab (your group in the omero instance)
* secure=True (should always be True)
* java_arg=java (should always be "java")

now we will be able to start the script : 
open a terminal in morphoomero/pipeline_tools/
##### Run in a terminal , line by line the following :
`conda activate AstecManager` \
`python3 fused_downscale_omero.py -f folder -n project -d dataset -t target -v voxelsize -l login -p password`

Here is the explanation for each parameter 
* -f path to the fusion folder
* -n project name on omero (created if it doesn't exist)
* -d dataset name on omero (created if it doesn't exist)
* -t path to the output downscaled fusion folder (created if it doesn't exist)
* -v Down sampled voxel size (write 0.6 for down sampling by 2)
* -l Your account login on OMERO
* -p Your account password on OMERO

There is no troubleshooting for this section , if you have a problem , you need to find a team member

## Backgrounds _(optional)_

To compute backgrounds, we will use a deep learning tool trained by the MorphoNet team. It will need a special power to run , and should be installed on a specific computer
In the team , we use a computer called loki. To get access to Loki using ssh , first ask the team.

To start background  , you first need to get the identifier of your dataset on omero.
For this goes to omero , find your project and the dataset (green folder) , and look at the properties on the right.
You will find a line called "Dataset id : ". Copy the number on the right 
##### Run in a terminal , line by line the following :


`ssh loki.crbm.cnrs.fr` \
`cd /data/MorphoDeep/morphodeep/morphodeep/Process/` \
`python3 Compute_Background_From_Omero.py -d id_dataset_omero -m FusedToBackground`

After the computation , you will find a new dataset inside the omero project , called Background_name_of_fusion_dataset

There is no troubleshooting for this section , if you have a problem , you need to find a team member

## Contours _(optional)_

This section need to have the background (above) finished to work. 
This code will automatically download the backgrounds from OMERO, and compute the contours images, that will be used by ASTEC later
##### Run in a terminal , line by line the following :
`conda activate AstecManager` \
`python3 download_backgrounds_contour.py -n project -d project -o output_folder -t target -v voxelsize -l login -p password`


This code use the same configuration as upload before, so no need to change it
Here is the explanation for each parameter

* -p project name on omero
* -d dataset name on omero
* -o path to the output folder. it should be : "/embryoname/BACKGROUND/name_of_omero_dataset/"
* -v Voxel size for the contour
* -l Your account login on OMERO
* -p Your account password on OMERO

After running , the code will create this folder "/embryoname/CONTOUR/CONTOUR_RELEASE_6/" for voxel size 0.6

There is no troubleshooting for this section , if you have a problem , you need to find a team member

## Segmentation of first time point
In order to compute the complete embryo segmentation, for all the time points, the system will need a first time point segmentation that we will consider "perfect".
Using this time point , we will propagate the different cells through times, and detect detections.

The segmentation of the first time point is automatically processed by the AstecManager tool. This step , that we will call MARS now, is done in one step. 
The first thing todo for now , is to copy the file  automatic file. 
If you don't plan to use the contour, or you didn't compute them 

* copy the file "mars_test.py" from example_files folder, into your root folder (the folder that contains the embryo folder)

If you plan to use the contour for the segmentation 

* copy the file "mars_test_with_contour.py" from example_files folder, into your root folder (the folder that contains the embryo folder)

In both case, open the file in a text editor and modify the following : 

``` 
embryo_name = "name"
begin=1
end=1
woring_resolution = 0.3
``` 

If your MARS is done using half resolution fused images , you will need to update those parameters

* working_resolution = 0.6
* parameters["EXP_FUSE"]= "'01_down06'"

To put the correct embryo name. The parameters begin and end should be bound to the first time point of your embryo (most of the time 0 or 1)
You can than run the file doing the following : 

`conda activate AstecManager` \
`python3 mars_test(_with_contour).py`

### MARS Verification

After MARS run , the hierarchy of your file should look like this 
```
root folder
│───embryo name
│   │───RAWDATA
│   │    └─── ...
│   │───FUSE
│   │   └─── ...
│   │───INTRAREG
│   │   └─── ...
│   └───SEG
│       └─── SEG_mars_add
│       │     │─── LOGS
│       │     └─── embryo_name_mars_t001.nii
│       └─── SEG_mars_max
│            │─── LOGS
│            └─── embryo_name_mars_t001.nii
└─── mars_test(_with_contour).py
```

To determine if the segmentation is correct or incorrect, we will need to import the segmentations in MorphoNet. 

## Install Morphonet

You first need to download MorphoNet Application : [Click here to download](https://morphonet.org/downloads)
##### (use a stable version of MorphoNet)
After downloading the version corresponding to your operating system please do the following : 

* On macOS : you must drag the application into the "Applications" folder, and then double-click on the application to start it
* On Windows : ?
* On Linux : ?

For all the systems, the first start of the application will be really slow : all the dependencies are getting installed
1s soon as the application is started, you can add the segmentation , your first need to click on Add Dataset 

![AddDataset](doc_images/add_dataset.png "Add Dataset Button")

And then click to this folder, to automatically fill all the values with the folder of the segmentation 

![PickDataset](doc_images/folder_add.png "Pick Dataset Button")

This button will open a file explorer , and you'll have to double-click on the MARS folder you want to import
```
root folder
│───embryo name
│   │───RAWDATA
│   │    └─── ...
│   │───FUSE
│   │   └─── ...
│   │───INTRAREG
│   │   └─── ...
│   └───SEG
│       └─── SEG_mars_add               <========
│       │     │─── LOGS
│       │     └─── embryo_name_mars_t001.nii
│       └─── SEG_mars_max
│            │─── LOGS
│            └─── embryo_name_mars_t001.nii
└─── mars_test(_with_contour).py
```

And then you need to change the name, to make sure to know which MARS is addition, and which one is maximum , and you HAVE TO modify the Background Label value to 1. 

![FinalParameters](doc_images/plot_params.png "Final dataset configuration")

When everything is done, you can click on "Create" , and after a loading, the segmentation will appear on MorphoNet

### Detect Segmentation errors 

3 different errors can exist in the image result of MARS or the Segmentation : 

|           Over-segmentation           |           Under-segmentation           |        Missing cells        |
|:-------------------------------------:|----------------------------------------|:---------------------------:|
| ![](doc_images/over_segmentation.png) | ![](doc_images/under_segmentation.png) | ![](doc_images/missing.png) |

To determine the MARS parameters , we will need to choose the parameters that gives the lowest number of under-segmentation/missing cells as possible. Those 2 types of errors are difficult to fix
It's okay to have some over-segmentation , to reduce the number of under-segmentation, as it is easy to fix

### Fixing Segmentation errors 

For the rest of the documentation , fixing errors will be called : curating the embryo.

To curate the MARS image, and propagate further the segmentation, we will use the import we did in MorphoNet. 
MorphoNet gives access to a complete set of curation tools , using image analysis algorithms. 

# TODO

Finally , create a folder called "MARS" inside the embryo folder, and export the curated MARS image inside it. Choose "nii" as the export image format.

## Propagation of the segmentation

Now that we exported the first time point curated image, we will be able to use it as the source for the propagation.
Once more , exactly like the fusion and the MARS , the segmentation will be divided in 2 steps.

- The first will be a test segmentation , divided in 4 set of parameters , running 2 by 2. It will be computed on a short range of time.
- The second will be the production segmentation , on the complete embryo time points, and followed by an automatic error curation. 

### Segmentation parameters test

Depending on if you want to use the contour or not during the segmentation, copy the corresponding file (seg_test.py / seg_test_with_contour.py) from the "examples_files' folder, into the root folder (the folder containing the embryo folder)

Your file hierarchy should look like something like this.

```
root folder
│───embryo name
│   │───RAWDATA
│   │    └─── ...
│   │───FUSE
│   │    └─── ...
│   │───INTRAREG
│   │    └─── ...
│   │───SEG
│   │    └─── ...
│   └───MARS
│        └─── embryo_name_mars_t001.nii
└─── seg_test(_with_contour).py
```

Now edit the seg_test(_with_contour).py with a text editor, and modify these lines: 

``` 
embryo_name = "name"
begin=1
end=1
working_resolution = 0.3
``` 

Bind the "embryo_name" to the good name, "begin" to the same time point used for your MARS image , and "end" to the end of the test segmentation propagation run.
This "end" value depends of the embryo time points range, but 50 could be enough to get an idea of the segmentation. For a full resolution embryo , 50 time points for 4 instances could be a long computation.

If your segmentation is done using half resolution fused images , you will need to update those parameters

* working_resolution = 0.6
* parameters["EXP_FUSE"]= "'01_down06'"

You can than start the test using : 

`conda activate AstecManager` \
`python3 seg_test(_with_contour).py`


You can now wait for a day or two of segmentation propagation, maybe more if the data is in full resolution.
The folder hierarchy will look like this after segmentation test : 

```
root folder
│───embryo name
│   │───RAWDATA
│   │    └─── ...
│   │───FUSE
│   │    └─── ...
│   │───INTRAREG
│   │    └─── ...
│   │───SEG
│   │   │─── SEG_test_maximum_gace               
│   │   │     │─── LOGS
│   │   │     │─── embryo_name_mars_t001.nii
│   │   │     └─── ...
│   │   │─── SEG_test_maximum_glace   
│   │   │     │─── LOGS
│   │   │     │─── embryo_name_mars_t001.nii
│   │   │     └─── ...
│   │   │─── SEG_test_addition_gace               
│   │   │     │─── LOGS
│   │   │     │─── embryo_name_mars_t001.nii
│   │   │     └─── ...
│   │   └─── SEG_test_addition_glace   
│   │         │─── LOGS
│   │         │─── embryo_name_mars_t001.nii
│   │         └─── ...
│   └───MARS
│        └─── ...
└─── seg_test(_with_contour).py
```

### Segmentation test Verification

To verify the different segmentations tests that just ran, we will use 2 systems : 

* A comparison system integrated to the astecmanager tool
* MorphoNet in the exact same way we did for the MARS step. 

#### Comparison with astecmanager

The segmentation test will generate , inside the "embryo_name/analysis/test_segmentation/" , 2 images files. 

The image named "early_cell_death.png" represents, for each segmentation folder, the proportion of cells dying before the last time points.

![EarlyDeathProportion](doc_images/early_cell_death.png "Example of early cell death proportion plot")

The vertical axis represents the time points in the embryo , and the horizontal axis represents the different cells at the first time point.
Each point represents a cell dying too early, coming from the branch of the corresponding cell on the horizontal axis. For example , the cell pointed by the right arrows , means that a cell coming from the branch of the cell 50,111 , dying at time point 110 .
The box pointed by the blue arrows means that a majority of cells die too early for the corresponding starting cell on horizontal axis.

For this plot , we are looking for the least proportion of cells dying too early , and that , if cells die too early, they die the closer as possible to the last time point.

In this example , the "maximum" segmentation have way less cells dying too early (30% vs 70% for "addition" segmentation). But keep in mind that 30% of cells dying too early is a lot, and sometimes cells dying too early correspond to over segmentations stopping. We need the following plot to confirm "maximum" are the best.

The image named "cell_count.png" is the most important plot from the comparison. 

![CellCountComparison](doc_images/cell_count.png "Example of cell count plot")

The vertical axis represents the number of cells in the embryo, and the right axis the time points. 
In this plot, we will be looking for the embryo that has the most cell, because it will probably the segmentation with the less missing cells or under segmented cells errors. 
Keep in mind that if the number of cell is really high , other parameters could be better (with less over-segmented cells).
On top of the number of cells, the shape of the curve should follow the cell division pattern. For our embryos , it should look like a stair
shape, matching the cell divisions, and the plateau when no cells divide.

In this example, even if "addition_gace" and "addition_glace" seem to have more cells than the "maximum" segmentations , the curve for both "addition" are more random (no stair shape, growing and reducing again and again).
Even if they have less cells and still are slightly random , the "maximum" are probably better, even if they don't seem perfect.
#### Comparison with MorphoNet
Add the different folders to 4 MorphoNet datasets, while taking care to name them with the segmentation folder name and the embryo name. For each dataset , before adding it , you will need to add the properties file to the dataset on MorphoNet.
The properties file (format .xml) , includes properties that we will use to determine the best segmentation.

To add it , please use the folder button corresponding to "XML Properties file path" 

![Properties](doc_images/folder_xml.png "How to pick the property")

It will open a file explorer , and you will be able to pick the corresponding property file :

```
root folder
│───embryo name
│   │───RAWDATA
│   │    └─── ...
│   │───FUSE
│   │    └─── ...
│   │───INTRAREG
│   │    └─── ...
│   │───SEG
│   │   │─── SEG_test_maximum_gace               
│   │   │     │─── embryo_name_seg_lineage.xml    <============
│   │   │     │─── embryo_name_mars_t001.nii
│   │   │     └─── ...
│   │   │─── SEG_test_maximum_glace   
│   │   │     │─── embryo_name_seg_lineage.xml    <============
│   │   │     │─── embryo_name_mars_t001.nii
│   │   │     └─── ...
│   │   │─── SEG_test_addition_gace               
│   │   │     │─── embryo_name_seg_lineage.xml    <============
│   │   │     │─── embryo_name_mars_t001.nii
│   │   │     └─── ...
│   │   └─── SEG_test_addition_glace   
│   │         │─── embryo_name_seg_lineage.xml    <============
│   │         │─── embryo_name_mars_t001.nii
│   │         └─── ...
│   └───MARS
│        └─── ...
└─── seg_test(_with_contour).py
```

After binding the values of name and background label, you can create the dataset.
Once more , we will look for the different errors , and especially the segmentation with the less missing cells / under segmented cells. 
If a property file is included , you'll see a new button on the top left of the MorphoNet window, after loading the dataset.


![LineageButton](doc_images/lineage_button.png "Lineage button on MorphoNet")

Clicking on the button will load a new window , representing the embryo lineage (cell life and divisions through times).

![LineageWindow](doc_images/lineage_window.png "Lineage windows and tree on MorphoNet")

You are now able to explore the lineage to determine the different errors on the embryo if you wish. But to get an idea about the embryo errors , you can at least look at the lineage shape.

|        "Correct" lineage         |        "Uncorrect" Lineage        |
|:--------------------------------:|:---------------------------------:|
| ![](doc_images/good_lineage.png) | ![](doc_images/wrong_lineage.png) |


You now have the tools to determine which segmentation is the best, and so what parameters to use for the production segmentation. Keep in mind that even if there is a lot of oversegmented cells, a portion of them will be fixed automatically later.
### Segmentation production run

Copy the "seg_prod.py" file from "examples_files" into the root folder, depending on if you use the contour or not, and than edit it to bind the name , the first and last time points of the embryo.

Edit the following lines to match the parameters of the segmentation that worked :

```
parameters["reconstruction_images_combination"] = "'addition'"
parameters["intensity_enhancement"] = "'glace'"
```

If your segmentation is done using half resolution fused images , you will need to update those parameters

* working_resolution = 0.6
* parameters["EXP_FUSE"]= "'01_down06'"

When everything is ready , you can start the production segmentation : 

`conda activate AstecManager` \
`python3 seg_prod(_with_contour).py`

Please remember that this tool automatically starts the automatic correction of the over segmented cells , after the segmentation. So even if a new folder is created inside the SEG folder, the data you want is located inside the POST folder

```
root folder
│───embryo name
│   │───RAWDATA
│   │    └─── ...
│   │───FUSE
│   │    └─── ...
│   │───INTRAREG
│   │    └─── ...
│   │───SEG
│   │    └─── SEG_01              
│   │         │─── embryo_name_seg_lineage.xml   
│   │         │─── embryo_name_mars_t001.nii
│   │         │─── embryo_name_seg_t001.nii
│   │         └─── ...
│   │───POST
│   │    └─── POST_01              <============ The corrected data
│   │         │─── embryo_name_post_lineage.xml    
│   │         │─── embryo_name_post_t001.nii
│   │         └─── ...
│   └───MARS
│        └─── ...
└─── seg_prod(_with_contour).py
```

The segmentation will generate , inside the "embryo_name/analysis/post_segmentation/" , 2 images files. 

The image named "early_cell_death.png" represents, for each segmentation folder, the proportion of cells dying before the last time points.

![EarlyDeathProportion](doc_images/early_cell_death.png "Example of early cell death proportion plot")

The vertical axis represents the time points in the embryo , and the horizontal axis represents the different cells at the first time point.
Each point represents a cell dying too early, coming from the branch of the corresponding cell on the horizontal axis. For example , the cell pointed by the right arrows , means that a cell coming from the branch of the cell 50,111 , dying at time point 110 .
The box pointed by the blue arrows means that a majority of cells die too early for the corresponding starting cell on horizontal axis.

For this plot , we are looking for the least proportion of cells dying too early , and that , if cells die too early, they die the closer as possible to the last time point.

In this example , the "maximum" segmentation have way less cells dying too early (30% vs 70% for "addition" segmentation). But keep in mind that 30% of cells dying too early is a lot, and sometimes cells dying too early correspond to over segmentations stopping. We need the following plot to confirm "maximum" are the best.

The image named "cell_count.png" is the most important plot from the comparison. 

![CellCountComparison](doc_images/cell_count.png "Example of cell count plot")

The vertical axis represents the number of cells in the embryo, and the right axis the time points. 
In this plot, we will be looking for the embryo that has the most cell, because it will probably the segmentation with the less missing cells or under segmented cells errors. 
Keep in mind that if the number of cell is really high , other parameters could be better (with less over-segmented cells).
On top of the number of cells, the shape of the curve should follow the cell division pattern. For our embryos , it should look like a stair
shape, matching the cell divisions, and the plateau when no cells divide.

In this example, even if "addition_gace" and "addition_glace" seem to have more cells than the "maximum" segmentations , the curve for both "addition" are more random (no stair shape, growing and reducing again and again).
Even if they have less cells and still are slightly random , the "maximum" are probably better, even if they don't seem perfect.

### Manual curation

### Automatic naming