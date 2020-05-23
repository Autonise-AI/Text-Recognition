# Pytorch Implementation of [Pixel-LINK](https://arxiv.org/pdf/1801.01315.pdf)

## A brief abstract of your project including the problem statement and solution approach

We are attempting to detect all kinds of text in the wild. The technique used for text detection is based on the paper PixelLink: Detecting Scene Text via Instance Segmentation (https://arxiv.org/abs/1801.01315) by Deng et al. The text instances present in the scene images lie very close to each other, and it is challenging to distinguish them using semantic segmentation. So, there is a need of instance segmentation. 

The approach consists of two key steps: 
a) Linking of pixels in the same text instance - Segmentation step, 
b) Text bounding box extraction using the linking done.

There are two kinds of predictions getting done here at each pixel level in the image: 
a) Text/non-text prediction, 
b) Link prediction.

This approach sets it apart from other kinds of methodologies used so far for text detection. Before PixelLink, the SOTA approaches on text detection does two kinds of prediction: a) Text/non-text prediction, b) Location Regression. Here both of these predictions are made at one go taking many fewer number of iterations and less training data.

## Demo([Youtube Link](https://www.youtube.com/watch?v=3d3J0kH3u6c))

## Results: If numerical, mention them in tabular format. ToDo

## ![Test Results:](Aesthetics/output.png "Result on some Documents")

## A list of code dependencies.

All Code dependencies are present in the file requirements.txt<br/>
Run "pip install -r requirements.txt" to install all dependencies

ToDo Remove some files and add description of all files below in the code structure
## Code Structure
```bash
.
├── Coding_Guidelines.md
├── configs
│   ├── config.yaml
│   ├── dataset.yaml
│   └── text_config.yaml
├── Dockerfile
├── Errors_got.txt
├── ideas.txt
├── LICENSE
├── main.py
├── Misc
├── README.md
├── requirements.txt
├── sonar-project.properties
├── src
│   ├── Dlmodel
│   │   ├── Dlmodel.py
│   │   ├── __pycache__ (Cache Folder generated by python)
│   │   ├── TestOneImageD.py
│   │   ├── TestOneImageRD.py
│   │   ├── TestOneImageR.py
│   │   ├── TestRD.py
│   │   ├── TrainTestD.py
│   │   └── TrainTestR.py
│   ├── helper
│   │   ├── logger.py
│   │   ├── profiler.py
│   │   ├── __pycache__ (Cache Folder generated by python)
│   │   ├── read_yaml.py
│   │   └── utils.py
│   ├── loader
│   │   ├── art.py
│   │   ├── dete_loader.py
│   │   ├── generic_dataloader.py
│   │   ├── mnist.py
│   │   ├── __pycache__
│   │   ├── reco_loader.py
│   │   ├── scale_two.py
│   │   └── square.py
│   ├── model
│   │   ├── crnn.py ( Convolutional Recurrent Neural Network ) (ToDo - Link the original paper and implementation)
│   │   ├── densenet.py ( DenseNet Model ) (ToDo - Link the original paper and implementation)
│   │   ├── generic_model.py (Super class for all the models, contains basic functions)
│   │   ├── model_loader.py (Model loader for CRNN) (ToDo - Merge with CRNN.py)
|   |   ├── unet.py (UNET Model) (ToDo - Link the original paper and implementation) 
|   |   ├── unet_parts.py (Helper File to unet.py)
|   |   ├── u_net_resnet_50_encoder.py (UNET_RESNET model) (ToDo - Link the original paper and implementation)
|   |   ├── u_net_resnet_50_parts.py (Helper File to u_net_resnet_50_parts.py)
│   │   ├── __pycache__ (Cache Folder generated by python)
│   │   ├── resnet_own.py (Under Development CRNN)
│   │   └── trial.py (Under Development CRNN)
│   ├── pipeline_manager.py (Controls the flow of the repository)
│   ├── prepare_metadata (Preprocessing steps to be performed before Training/Testing
│   │   ├── meta_artificial.py (Prepare Metadata for artificial Dataset)
│   │   ├── meta_coco.py (Prepare Metadata for COCO V2 Dataset)
│   │   ├── meta_ic13.py (Prepare Metadata for IC13 Dataset)
│   │   ├── meta_ic15.py (Prepare Metadata for IC15 Dataset)
│   │   ├── meta_own.py (Prepare Metadata for OWN Dataset)
│   │   ├── meta_synth.py (Prepare Metadata for SynthText Dataset)
│   │   ├── prepare_metadata.py
│   │   └── __pycache__ (Cache Folder generated by python)
│   └── __pycache__
└── text.sublime-workspace
```

## Instructions to run the code

### Setting up the dataset

	1. In the configs/dataset.yaml file add your dataset in the following format under the field metadata

		1. <Name of the dataset>
			1. dir:<Path-to-Dataset-Folder> 
			2. image: <Path-to-Dataset-Folder>/Images
			3. label: <Path-to-Dataset-Folder>/Labels
			4. meta: <Path-to-Dataset-Folder>/Meta
			5. contour_length_thresh_min: <Contours with length less than this are excluded from training and testing>
			6. contour_area_thresh_min: <Contours with area less than this are excluded from training and testing>
			7. segmentation_thresh: <Confidence value over which pixel is classified as positive>
    		8. link_thresh: <Confidence value over which link is classified as positive>
    		9. cal_avg: <If True: Padding with Average of the image, else: Padding with Zeros>
    		10. split_type: <% of Training Images which is randomly picked from the dataset, remaining is used for validation>

	2. Put all your images in the *<Path-to-Dataset-Folder>/Images* folder

	3. Create Labels in the format - 
		1. Contours = List of all bounding box(dtype=np.float32, shape=[4, 1, 2](4, 2 for four co-ordinates with two dimensions))
		2. Text = List of all strings which have text corresponding to every Contour
		3. Labels corresponding to every image would have the name <image-name.extension-of-image.pkl>. It will be a pickle dump of the list [Contours, Text]

	4. Save all the labels for the images in the folder *<Path-to-Dataset-Folder>/Labels*

	5. Create the folder *<Path-to-Dataset-Folder>/Meta*

	6. In the configs/dataset.yaml file put your dataset name in the field *dataset_train* and *dataset_test*

	7. Run python main.py prepare_metadata

### Training your own model(Detection)
	
	1. The configs/config.yaml contains all the hyper-parameters for training the detection model.
	2. After your dataset and config file is in place run the command `python main.py train_d`

### Testing your own model(Detection)
	
	1. In the configs/config.yaml in the field "PreTrained_model" change the value of the field "check" to True
	2. Configure the path of the model in the field "PreTrained_Model"
	3. After your dataset and config file is in place run the command `python main.py test_d`

### Generate Visual Results on a single image

	1. In the configs/config.yaml in the field "PreTrained_model" change the value of the field "check" to True
	2. Configure the path of the model in the field "PreTrained_Model"
	3. Run the command `python main.py test_one_d -p <path-to-test-image> -o <path-to-folder-output>`

### Generate Visual Results on an entire folder

	1. In the configs/config.yaml in the field "PreTrained_model" change the value of the field "check" to True
	2. Configure the path of the model in the field "PreTrained_Model"
	3. Run the command `python main.py test_entire_folder_d -p <path-to-test-folder> -o <path-to-output-folder>`

## Pretrained Model
	
Request access to a pretrained model - Write a mail to mayank2220singh@gmail.com stating your affiliations and purpose for using the model.

## References.
* Deng, Dan, et al. "Pixellink: Detecting scene text via instance segmentation." Thirty-Second AAAI Conference on Artificial Intelligence. 2018.
* Karatzas, Dimosthenis, et al. "ICDAR 2015 competition on robust reading." 2015 13th International Conference on Document Analysis and Recognition (ICDAR). IEEE, 2015.
* VGG Synth Text in the wild: A. Gupta, A. Vedaldi, A. Zisserman "Synthetic Data for Text Localisation in Natural Images" IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2016
* Ren, Mengye, and Richard S. Zemel. "End-to-end instance segmentation with recurrent attention." Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition. 2017.
* Girshick, Ross. "Fast r-cnn." Proceedings of the IEEE international conference on computer vision. 2015.
