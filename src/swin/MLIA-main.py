import argparse
import os
import sys

import numpy as np
import json
from PIL import Image

from swin.mlia_swin_transformer import SwinUNETR

def load_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--train',action='store_true',help='Run training on the network')
    parser.add_argument('--inference',action='store_true',help='Run inference on the network')
    parser.add_argument('--net-cfg',required=True,help='Network configuration')
    parser.add_argument('--input',required=True,help='Input directory of images')
    return parser.parse_args()


def load_model_config(config_file:str):
    with open(config_file,'r') as cfg:
        return json.load(cfg)


def dataloader(directory, batch_size=1):
    """
    Loads images in directory and formats them into a list of (b, c, h, w)
    Output arrays are guaranteed to be 4D.

    :param directory: input data directory
    :param batch_size: number of images per batch
    :returns: list of 4D numpy array
    """
    img_files = [f for f in os.listdir(directory) if f.endswith('.png')]
    num_imgs = len(img_files)
    assert num_imgs % batch_size == 0, f'number of images ({num_imgs}) is not divisible by batch size ({batch_size})'

    data = np.asarray(Image.open(os.path.join(directory, img_files[0])))
    h, w = data.shape

    data_list = []
    data_arr = np.empty([batch_size, 1, h, w])
    batch_idx = 0
    for img_idx, filename in enumerate(img_files):
        # new batch
        if img_idx % batch_size == 0 and img_idx > 0:
            data_list.append(data_arr)
            data_arr = np.empty([batch_size, 1, h, w])
            batch_idx = 0

        data = np.asarray(Image.open(os.path.join(directory, filename)))
        data_arr[batch_idx, 0] = data
        batch_idx += 1

    return data_list


def zero_pad_image(data):
    """Pads the width of the images out to 256x256
    
    :input data - list of (b, c, h, w )
    :output - list of (b, c, h, w)"""
    raise NotImplementedError


def train_network(config,input_dir):
    model = SwinUNETR(**config)
    #TODO: 1) implement training
    #TODO: 2) save trained weights and 


def main(config_filepath,train,inference,input_dir):
    config = load_model_config(config_filepath)
    if args.train:
        train_network(config,input_dir)
    elif args.inference:
        raise NotImplementedError
        #TODO: implement this for testing...
        #run_inference(config,input)


if __name__ =='__main__':
    args = load_args()
    main(args.net_cfg,args.train,args.inference,args.input)
