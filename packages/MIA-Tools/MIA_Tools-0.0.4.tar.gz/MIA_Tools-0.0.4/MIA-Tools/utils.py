import os
import ants

def read_image(img_path, v=False):
    '''
    TODO: functions for load nifti image using antspy
    :param img_path: medical image path
    :param v: return detailed image info or just ants image object
    :return: data
    '''
    img = ants.image_read(img_path)
    if v:
        return img.origin, img.spacing, img.direction, img.numpy()
    else:
        return img
