#    Copyright IDEA Lab, School of Biomedical Engineering, ShanghaiTech. Shanghai, China
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Repo for Brain Extraction
#    Contact: JiamengLiu.PRC@gmail.com
from itertools import product

import SimpleITK as sitk
import ants
import numpy as np
from skimage import measure


def _ants_img_info(img_path):
    '''
    TODO: functions to load medical image using antspy
    :param img_path: path to image (str)
    :return: image parameters of origin, spacing, direction, and image array (numpy)
    '''
    img = ants.image_read(img_path)
    return img.origin, img.spacing, img.direction, img.numpy()


def _sitk_img_info(img_path):
    '''
    TODO: Functions to load medical image using SimpleITK and get fundamental informations
    :param img_path: absolute image path end with: .nii.gz, .mhd, .hdr
    :return: origin, spacing, direction, image numpy array
    '''
    img = sitk.ReadImage(img_path)
    img = img.transpose(2,1,0)
    origin = img.GetOrigin()
    spacing = img.GetSpacing()
    direction = img.GetDirection()
    data = sitk.GetArrayFromImage(img)
    return origin, spacing, direction, data


def _array_to_sitk_img(img, origin, spacing, direction):
    '''
    Functions to convert numpy array to simpleITK image
    :param img: numpy array with direction (x, z, y)
    :param origin: simpleITK parameter
    :param spacing: voxel size of each elements
    :param direction: image direction
    :return: simpleITK image
    '''
    img = img.transpose(2,1,0)
    simg = sitk.GetImageFromArray(img)
    simg.SetOrigin(origin)
    simg.SetSpacing(spacing)
    simg.SetDirection(direction)
    return simg


def _seg_to_label(seg):
    '''
    TODO: Labeling each single annotation in one image (single label to multiple label)
    :param seg: single label annotation (numpy data)
    :return: multiple label annotation
    '''
    labels, num = measure.label(seg, return_num=True)
    labels = labels.astype(np.float32)
    return labels, num


def _select_top_k_region(img, k=2):
    '''
    TODO: Functions to select top k connection regions
    :param img: numpy array with multiple regions
    :param k: number of selected regions
    :return: selected top k region data
    '''
    # seg to labels
    labels, nums = _seg_to_label(img)
    rec = list()

    for idx in range(1, nums+1):
        subIdx = np.where(labels==idx)
        rec.append(len(subIdx[0]))
    rec_sort = rec.copy()
    rec_sort.sort()

    rec = np.array(rec)
    index = np.where(rec >= rec_sort[-k])[0]
    index = list(index)

    for idx in index:
        labels[labels==idx+1] = 1000000

    labels[labels != 1000000] = 0
    labels[labels == 1000000] = 1

    return labels


def _normalize_z_score(data, clip=True):
    '''
    TODO: funtions to normalize data to standard distribution using (data - data.mean()) / data.std()
    :param data: numpy array
    :param clip: whether using upper and lower clip
    :return: normalized data by using z-score
    '''
    if clip == True:
        bounds = np.percentile(data, q=[0.00, 99.999])
        data[data <= bounds[0]] = bounds[0]
        data[data >= bounds[1]] = bounds[1]

    return (data-data.mean())/data.std()


def _normalize_to_standard(data, clip=True):
    '''
    TODO: funtions to normalize data to standard distribution using (data - data.mean()) / data.std()
    :param data: numpy array
    :param clip: whether using upper and lower clip
    :return: normalized data by using z-score
    '''
    if clip == True:
        bounds = np.percentile(data, q=[0.00, 99.999])
        data[data <= bounds[0]] = bounds[0]
        data[data >= bounds[1]] = bounds[1]

    return (((data - data.min()) / (data.max() - data.min())) - 0.5) * 2


def calculate_patch_index(target_size, patch_size, overlap_ratio = 0.25):
    '''
    TODO: functions to
    :param target_size:
    :param patch_size:
    :param overlap_ratio:
    :return:
    '''
    shape = target_size

    gap = int(patch_size[0] * (1-overlap_ratio))
    index1 = [f for f in range(shape[0])]
    index_x = index1[::gap]
    index2 = [f for f in range(shape[1])]
    index_y = index2[::gap]
    index3 = [f for f in range(shape[2])]
    index_z = index3[::gap]

    index_x = [f for f in index_x if f < shape[0] - patch_size[0]]
    index_x.append(shape[0]-patch_size[0])
    index_y = [f for f in index_y if f < shape[1] - patch_size[1]]
    index_y.append(shape[1]-patch_size[1])
    index_z = [f for f in index_z if f < shape[2] - patch_size[2]]
    index_z.append(shape[2]-patch_size[2])

    start_pos = list()
    loop_val = [index_x, index_y, index_z]
    for i in product(*loop_val):
        start_pos.append(i)
    return start_pos


def _ants_registration(moving_img_path, moving_seg_path=None, fixed_img_path=None, type_of_transform='SyN'):
    moving_img = ants.image_read(moving_img_path)
    if moving_seg_path == None:
        moving_img = ants.image_read(moving_img_path)
        fixed_img = ants.image_read(fixed_img_path)
        res = ants.registration(fixed=fixed_img, moving=moving_img, type_of_transform=type_of_transform)
        return res['warpedmovout']
    else:
        moving_img = ants.image_read(moving_img_path)
        moving_seg = ants.image_read(moving_seg_path)
        fixed_img = ants.image_read(fixed_img_path)

        res = ants.registration(fixed=fixed_img, moving=moving_img, type_of_transform=type_of_transform)

        warped_img = res['warpedmovout']
        warped_seg = ants.apply_transforms(fixed=fixed_img, moving=moving_seg, transformlist=res['fwdtransforms'],
                                           interpolator='nearestNeighbor')

        return warped_img, warped_seg