
import json
import numpy as np
import os
import matplotlib.pyplot as plt
import cv2
from PIL import Image
import pickle
from shutil import copyfile
import re


class MetaIC15():

	def __init__(self, config):

		self.config = config
		self.seed()
		self.split_type = self.config['metadata']['IC15']['split_type']

	def seed(self):

		np.random.seed(self.config['seed'])

	def clean_1(self):

		#Reads coordinates and texts, dumps in pickle, and returns the final list of all_train_images

		image_path = self.config['metadata']['IC15']['dir']+'/UnClean/ch4_training_images'
		label_path = self.config['metadata']['IC15']['dir']+'/UnClean/ch4_training_localization_transcription_gt'

		all_train_images = sorted(os.listdir(image_path))
		all_train_labels = ['gt_'+i.split('.')[0]+'.txt' for i in all_train_images]

		for no, (image, label) in enumerate(zip(all_train_images, all_train_labels)):

			all_annots = []
			all_text = []
			with open(label_path+'/'+label, 'r') as f:

				for j in f:

					coords = re.findall(r'\d+', j)[0:8]
					coords = np.array([[coords[2*k],coords[2*k+1]] for k in range(4)]).astype(np.int32)
					all_annots.append(coords.reshape(coords.shape[0], 1, 2))

					text = ','.join(j.split(',')[8:])[:-1]
					if text!='###':
						all_text.append(text)
					else:
						all_text.append('')

			with open(self.config['metadata']['IC15']['dir']+'/Labels/train1_'+image+'.pkl', 'wb') as f:

				pickle.dump([all_annots, all_text], f)

			copyfile(image_path+'/'+image, self.config['metadata']['IC15']['dir']+'/Images/train1_'+image)

		all_train_images = ['train1_'+j for j in all_train_images]

		image_path = self.config['metadata']['IC15']['dir']+'/UnClean/ch4_test_images'
		label_path = self.config['metadata']['IC15']['dir']+'/UnClean/Challenge4_Test_Task4_GT'

		all_test_images = sorted(os.listdir(image_path))
		all_test_labels = ['gt_'+i.split('.')[0]+'.txt' for i in all_test_images]

		for no, (image, label) in enumerate(zip(all_test_images, all_test_labels)):

			all_annots = []
			all_text = []
			with open(label_path+'/'+label, 'r') as f:

				for j in f:

					coords = re.findall(r'\d+', j)[0:8]
					coords = np.array([[coords[2*k],coords[2*k+1]] for k in range(4)]).astype(np.int32)
					all_annots.append(coords.reshape(coords.shape[0], 1, 2))

					text = ','.join(j.split(',')[8:])[:-1]
					if text!='###':
						all_text.append(text)
					else:
						all_text.append('')

			with open(self.config['metadata']['IC15']['dir']+'/Labels/test1_'+image+'.pkl', 'wb') as f:

				pickle.dump([all_annots, all_text], f)

			copyfile(image_path+'/'+image, self.config['metadata']['IC15']['dir']+'/Images/test1_'+image)

		all_test_images = ['test1_'+j for j in all_test_images]

		return all_train_images + all_test_images

	def split_ratio(self, all_list, train_ratio):

		#Forms the training and testing image paths, by splitting the dataset, deterministic due to self.seed()

		idx = np.arange(len(all_list))
		np.random.shuffle(idx)

		# /home/mayank/Desktop/GitRepos/Text/Segmentation/Dataset/labels_text/meta

		if os.path.exists(self.config['metadata']['IC15']['meta']+'/train_files_'+str(train_ratio)+'.txt'):
			os.remove(self.config['metadata']['IC15']['meta']+'/train_files_'+str(train_ratio)+'.txt')

		f = open(self.config['metadata']['IC15']['meta']+'/train_files_'+str(train_ratio)+'.txt', 'w')

		train = np.array(all_list)[idx[:int(train_ratio*len(all_list))]]
		val = np.array(all_list)[idx[int(train_ratio*len(all_list)):]]

		for i in train:
			f.write(i+'\n')

		if os.path.exists(self.config['metadata']['IC15']['meta']+'/test_files_'+str(train_ratio)+'.txt'):
			os.remove(self.config['metadata']['IC15']['meta']+'/test_files_'+str(train_ratio)+'.txt')

		f = open(self.config['metadata']['IC15']['meta']+'/test_files_'+str(train_ratio)+'.txt', 'w')

		for i in val:
			f.write(i+'\n')

		return train

	def split_fixed(self, all_list):

		# /home/mayank/Desktop/GitRepos/Text/Segmentation/Dataset/labels_text/meta

		if os.path.exists(self.config['metadata']['IC15']['meta']+'/train_files_orig.txt'):
			os.remove(self.config['metadata']['IC15']['meta']+'/train_files_orig.txt')

		f = open(self.config['metadata']['IC15']['meta']+'/train_files_orig.txt', 'w')
		
		train = np.array([x for x in all_list if x[:5] == 'train'])
		# print(train)
		
		for i in train:
			f.write(i+'\n')

		if os.path.exists(self.config['metadata']['IC15']['meta']+'/test_files_orig.txt'):
			os.remove(self.config['metadata']['IC15']['meta']+'/test_files_orig.txt')

		f = open(self.config['metadata']['IC15']['meta']+'/test_files_orig.txt', 'w')

		val = np.array([x for x in all_list if x[:4] == 'test'])

		for i in val:
			f.write(i+'\n')

		return train

	def calc_average(self, train):

		image_average = [np.zeros(3), 0]
		image_std = [np.zeros(3), 0]

		random_images = np.random.choice(train, min(1000, len(train)), replace=False)

		for i in random_images:

			image = plt.imread(self.config['metadata']['IC15']['image']+'/'+i)
			if len(image.shape) == 2:
				continue
			image_average[0] += np.sum(image, axis=(0, 1))
			image_average[1] += image.shape[0]*image.shape[1]

		image_average[0] = image_average[0]/image_average[1]

		for i in random_images:

			image = plt.imread(self.config['metadata']['IC15']['image']+'/'+i)
			if len(image.shape) == 2:
				continue
			image_std[0] += np.sum(np.square(image - image_average[0]), axis=(0, 1))
			image_std[1] += image.shape[0]*image.shape[1]

		image_std[0] = image_std[0]/image_std[1]

		with open(self.config['metadata']['IC15']['meta']+'/normalisation_'+str(train_ratio)+'.pkl', 'wb') as f:
			pickle.dump({'average': image_average, 'std': image_std}, f)

	def create_annot(self):

		all_list = self.clean_1()
		if self.split_type == 'original':
			train = self.split_fixed(all_list)
		else:
			train = self.split_ratio(all_list, float(self.split_type))

		if self.config['metadata']['IC15']['cal_avg']:
			self.calc_average(train)
