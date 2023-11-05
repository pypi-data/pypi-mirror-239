import os
import ants


def _ants_img_info():
    img = ants.image_read('../data/MNI152_T1.nii.gz')
    return img.origin, img.spacing, img.direction, img.numpy()

