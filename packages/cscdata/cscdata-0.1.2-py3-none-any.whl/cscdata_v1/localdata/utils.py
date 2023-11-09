# -*- coding:utf-8 -*-

import json
import h5py
import os

def find_file(name, path = '.'):
    # name in path
    for file in os.listdir(path):
        if file.startswith(name):
            return os.path.abspath(os.path.join(path, file))
    # return abs name
    if os.path.isabs(name):
        return name

    raise FileNotFoundError(f"file name '{name}' not found in path '{path}'.")

def remove_file_path(path):
    """remove exists file"""
    if os.path.exists(path):
        os.remove(path)

def remove_file_in_directory(directory):
    if os.path.exists(directory):
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            if os.path.isfile(item_path):
                os.remove(item_path)

def create_simple_not_exists(path):
    """create not exists file"""
    if not os.path.exists(path):
        os.mkdir(path)

def create_multi_not_exists(path):
    """create mutil not exists file"""
    if not os.path.exists(path):
        os.makedirs(path)
    
def read_json(json_file):
    """Read a JSON file and return its content as a Python object."""
    with open(json_file, 'r') as file:
        return json.load(file)

def read_h5(pth, key):
    with h5py.File(pth, 'r') as h5r:
        data = h5r[key][()]
    return data

def list_keys(pth):
    with h5py.File(pth, 'r') as h5r:
        return list(h5r.keys())
    
def read_h5_flow(pth, key, chunk_size):
    with h5py.File(pth, 'r') as f:
        dset = f[key]
        n = dset.shape[0]

        for i in range(0, n, chunk_size):
            yield dset[i: i+chunk_size]

def is_path(name):
    return os.path.isabs(name) or "/" in name or "\\" in name
