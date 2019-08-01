"""
Has functions 'open_cbor', 'decode_image_bytes' and 'decode_image_metadata'
"""
import os
from cbor2 import dumps, loads, CBORTag, decoder
import io
import numpy as np
import itertools
import sys

def open_cbor(filename):
    """Input: Filename for cbor file
        Output: Two values:1-D Array of Dimensions data, 1-D Array of image bytes"""
    # Open file as binary
    with open(filename, 'rb') as data:
        obj=loads(data.read())
    # Access values inside cbor tags
    dimensions = obj[1].value[0].value
    image_data = obj[1].value[1].value
    return dimensions, image_data


def image_values(element):
    return int.from_bytes(element, byteorder='big', signed=False)


def metadata_values(element):
    return int.from_bytes(element, byteorder='big', signed=True)


def decode_image_bytes(image_byte_array):
    """Input: 1-D list of 16 bit two's compliment bytes 
        Operations: Converts the bytes to unsigned and decodes them
        Output: a 1-D array of 16-bit image data"""
    # Convert input to numpy array
    # Convert two's complement bytes to unsigned
    image = np.array(image_byte_array, dtype='uint8')
    # Split the unsigned bytes into segments
    bytes_array=np.array_split(image,(len(image)/2))
    # Convert segements into integer values
    bytes_array = np.apply_along_axis(image_values, 1, bytes_array)
    return bytes_array


def decode_image_metadata(image_dimensions_bytes_array):
    """Input: 1-D list of sint64 two's complement bytes
        Operations: Converts bytes to unsigned and decodes them
        Output: Dictionary with possible values: 'width, height, channels, Z, time'"""
    # Convert input to numpy array
    # Covert two's complement bytes to unsigned
    dimensions = np.array(image_dimensions_bytes_array, dtype='uint8')
    # Split the unsigned bytes into segements
    bytes_array=np.array_split(dimensions,(len(dimensions)/8))
    # Convert the segments into integer values
    bytes_array = np.apply_along_axis(metadata_values, 1, bytes_array)
    # Put the converted integer values into a dictionary
    end = dict(itertools.zip_longest(['width', 'height', 'channels', 'Z', 'time'], bytes_array, fillvalue=None))
    return end