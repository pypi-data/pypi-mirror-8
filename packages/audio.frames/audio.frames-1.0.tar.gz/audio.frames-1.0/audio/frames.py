#!/usr/bin/env python
# coding: utf-8
"""
Audio Frames Toolkit
"""

# Python Standard Library
import doctest
import unittest

# Third-Party Libraries
import numpy as np

#
# Metadata
# ------------------------------------------------------------------------------
#
__main__ = (__name__ == "__main__")

from audio.about_frames import *

#
# TODO
# ------------------------------------------------------------------------------
#
#   - support n-dim. array with an axis parameters (defaults to last axis: -1)
#   - support "init values" whose length match the overlap ? There is a use
#     case in shrink, study it. By default, I'd say no support for this obscure
#     feature.
#   - change the API so that split returns only arrays.
#

#
# Application Programming Interface
# ------------------------------------------------------------------------------
#
def split(data, frame_length, zero_pad=False, overlap=0, window=None):
    """
    Split an array into frames.

    Arguments
    ---------

      - `data`: a sequence of numbers,

      - `frame_length`: the desired frame length,

      - `zero_pad`: if `True`, zeros are added to the last frame to make it
        match the prescribed frame length, otherwise it may be shorter than
        the others; defaults to `False`.

      - `overlap`: number of samples shared between successive frames,
        defaults to `0`.

      - `window`: an optional window applied to each frame after the split.
        The default (rectangular window) does not modify the frames.

    Result
    ------

      - `frames`: a sequence of numpy arrays.
    """
    data = np.array(data, copy=False)
    length = len(data)
    if overlap >= frame_length:
        error = "overlap >= frame_length"
        raise ValueError(error)
    frames = []
    i = 0
    j = i + frame_length
    while j < length:
        frames.append(data[i:j])
        i += frame_length - overlap
        j = i + frame_length
    last_frame = data[i:j]
    if zero_pad and len(last_frame) < frame_length:
        padding = np.zeros(frame_length - len(last_frame), dtype=data.dtype)
        last_frame = np.r_[last_frame, padding]
    frames.append(last_frame)
    if window:
        frames = [window(len(frame)) * frame for frame in frames]
    return frames

# TODO: do not require `frames` to support `len`, so that generator can
#       be used.

def merge(frames, overlap=0, window=None):
    """
    Merge a sequence of frames.

    Arguments
    ---------

      - `frames`: a sequence of frames,

      - `overlap`: number of overlapping samples between successive frames,
        defaults to `0`.

      - `window`: an optional window applied to each frame before the merge.
        The default (rectangular window) does not modify the frames.

    Result
    ------

      - `data`: a numpy array.
"""
    try:
        num_frames = len(frames)
    except TypeError:
        frames = [frame for frame in frames]
        num_frames = len(frames)
    length = sum([len(frame) for frame in frames]) - (num_frames - 1) * overlap
    dtype = np.find_common_type([np.array(frame).dtype for frame in frames], [])
    data = np.zeros(length, dtype=dtype)
    offset = 0
    for i, frame in enumerate(frames):
        if window:
            frame = window(len(frame)) * frame
        data[offset:offset+len(frame)] += frame
        offset += len(frame) - overlap
    return data

#
# Unit Tests
# ------------------------------------------------------------------------------
#

def test():
    """
Preamble:

    >>> import numpy as np

Test array:

    >>> data = [1, 2, 3, 4, 5]

Basic usage:

    >>> split(data, 1)
    [array([1]), array([2]), array([3]), array([4]), array([5])]
    >>> split(data, 2)
    [array([1, 2]), array([3, 4]), array([5])]
    >>> split(data, 3)
    [array([1, 2, 3]), array([4, 5])]
    >>> split(data, 4)
    [array([1, 2, 3, 4]), array([5])]
    >>> split(data, 5)
    [array([1, 2, 3, 4, 5])]
    >>> split(data, 6)
    [array([1, 2, 3, 4, 5])]

Zero padding:

    >>> split(data, 1, zero_pad=True)
    [array([1]), array([2]), array([3]), array([4]), array([5])]
    >>> split(data, 2, zero_pad=True)
    [array([1, 2]), array([3, 4]), array([5, 0])]
    >>> split(data, 3, zero_pad=True)
    [array([1, 2, 3]), array([4, 5, 0])]
    >>> split(data, 4, zero_pad=True)
    [array([1, 2, 3, 4]), array([5, 0, 0, 0])]
    >>> split(data, 5, zero_pad=True)
    [array([1, 2, 3, 4, 5])]
    >>> split(data, 6, zero_pad=True)
    [array([1, 2, 3, 4, 5, 0])]

Overlapping Frames:

    >>> split(data, 2, overlap=1)
    [array([1, 2]), array([2, 3]), array([3, 4]), array([4, 5])]
    >>> split(data, 3, overlap=1)
    [array([1, 2, 3]), array([3, 4, 5])]
    >>> split(data, 3, overlap=2)
    [array([1, 2, 3]), array([2, 3, 4]), array([3, 4, 5])]
    >>> split(data, 3, overlap=3) # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    ValueError: ...

Windows:
    >>> data = np.ones(24)
    >>> frames = split(data, 6, window=np.hanning)
    >>> all(all(frame == np.hanning(6)) for frame in frames)
    True

Merging Frames:

    >>> frames = [[1, 2, 3], [4, 5, 6], [7, 8, 9]] 
    >>> merge(frames)
    array([1, 2, 3, 4, 5, 6, 7, 8, 9])
    >>> merge(frames, overlap=1)
    array([ 1,  2,  7,  5, 13,  8,  9])
    >>> merge(frames, overlap=2)
    array([ 1,  6, 15, 14,  9])
    >>> merge(frames, window=np.bartlett)
    array([0, 2, 0, 0, 5, 0, 0, 8, 0])
    >>> merge(frame for frame in frames)
    array([1, 2, 3, 4, 5, 6, 7, 8, 9])
    """
    doctest.testmod()

test_suite = doctest.DocTestSuite() # support for `python setup.py test`

if __main__:
    test()

