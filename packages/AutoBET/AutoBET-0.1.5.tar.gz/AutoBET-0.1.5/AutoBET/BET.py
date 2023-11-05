import os
import sys
import ants

dir_test = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]

atlas_img_path = os.path.join(dir_test, 'data', 'MNI152_T1.nii.gz')
atlas_seg_path = os.path.join(dir_test, 'data', 'MNI152_mask.nii.gz')
