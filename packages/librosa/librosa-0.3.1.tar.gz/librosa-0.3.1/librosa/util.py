#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Utility functions"""

import numpy as np
import os
import glob
import pkg_resources

from numpy.lib.stride_tricks import as_strided
from sklearn.base import BaseEstimator, TransformerMixin


EXAMPLE_AUDIO = 'example_data/Kevin_MacLeod_-_Vibe_Ace.mp3'


def example_audio_file():
    '''Get the path to an included audio example file.

    :usage:
        >>> # Load the waveform from the example track
        >>> y, sr = librosa.load(librosa.util.example_audio_file())

    :parameters:
        - None

    :returns:
        - filename : str
            Path to the audio example file included with librosa
    '''

    return pkg_resources.resource_filename(__name__, EXAMPLE_AUDIO)


def frame(y, frame_length=2048, hop_length=512):
    '''Slice a time series into overlapping frames.

    This implementation uses low-level stride manipulation to avoid
    redundant copies of the time series data.

    :usage:
        >>> # Load a file
        >>> y, sr = librosa.load('file.mp3')
        >>> # Extract 2048-sample frames from y with a hop of 64
        >>> y_frames = librosa.util.frame(y, frame_length=2048, hop_length=64)

    :parameters:
      - y : np.ndarray [shape=(n,)]
          Time series to frame. Must be contiguous in memory

      - frame_length : int > 0 [scalar]
          Length of the frame in samples

      - hop_length : int > 0 [scalar]
          Number of samples to hop between frames

    :returns:
      - y_frames : np.ndarray [shape=(frame_length, N_FRAMES)]
          An array of frames sampled from ``y``:
          ``y_frames[i, j] == y[j * hop_length + i]``

    :raises:
      - ValueError
          If ``y`` is not contiguous in memory, framing is invalid.
          See ``np.ascontiguous()`` for details.

          If ``hop_length < 1``, frames cannot advance.
    '''

    if hop_length < 1:
        raise ValueError('Invalid hop_length: {:d}'.format(hop_length))

    if not y.flags['C_CONTIGUOUS']:
        raise ValueError('Input buffer must be contiguous.')

    # Compute the number of frames that will fit. The end may get truncated.
    n_frames = 1 + int((len(y) - frame_length) / hop_length)

    # Vertical stride is one sample
    # Horizontal stride is ``hop_length`` samples
    y_frames = as_strided(y, shape=(frame_length, n_frames),
                          strides=(y.itemsize, hop_length * y.itemsize))
    return y_frames


def pad_center(data, size, axis=-1, **kwargs):
    '''Wrapper for np.pad to automatically center an array prior to padding.
    This is analogous to ``str.center()``

    :usage:
        >>> # Generate a window vector
        >>> window = scipy.signal.hann(256)
        >>> # Center and pad it out to length 1024
        >>> window = librosa.util.pad_center(window, 1024, mode='constant')
        >>> # Pad a matrix along its first dimension
        >>> A = np.ones((3, 5))
        >>> Apad = librosa.util.pad_center(A, 7, axis=0)
        >>> # Or its second dimension
        >>> Apad = librosa.util.pad_center(A, 7, axis=1)

    :parameters:
        - data : np.ndarray
            Vector to be padded and centered

        - size : int >= len(data) [scalar]
            Length to pad ``data``

        - axis : int
            Axis along which to pad and center the data

        - *kwargs*
            Additional keyword arguments passed to ``np.pad()``

    :returns:
        - data_padded : np.ndarray
            ``data`` centered and padded to length ``size`` along the
            specified axis

    :raises:
        - ValueError
            If ``size < data.shape[axis]``
    '''

    kwargs.setdefault('mode', 'constant')

    n = data.shape[axis]

    lpad = int((size - n) / 2)

    lengths = [(0, 0)] * data.ndim
    lengths[axis] = (lpad, size - n - lpad)

    if lpad < 0:
        raise ValueError('Target size {:d} < input size {:d}'.format(size, n))

    return np.pad(data, lengths, **kwargs)


def fix_length(y, n, **kwargs):
    '''Fix the length of a one-dimensional array ``y`` to exactly ``n``.

    If ``len(y) < n``, pad according to the provided kwargs.
    By default, ``y`` is padded with trailing zeros.

    :parameters:
      - y : np.ndarray [shape=(m,)]
          one-dimensional array

      - n : int >= 0 [scalar]
          desired length of the array

      - *kwargs*
          Additional keyword arguments.  See ``np.pad()``

    :returns:
      - y : np.ndarray [shape=(n,)]
          ``y`` either trimmed or padded to length ``n``
    '''

    kwargs.setdefault('mode', 'constant')

    if len(y) > n:
        return y[:n]

    if len(y) < n:
        return np.pad(y, (0, n - len(y)), **kwargs)

    return y


def axis_sort(S, axis=-1, index=False, value=None):
    '''Sort an array along its rows or columns.

    :usage:
        >>> # Visualize NMF output for a spectrogram S
        >>> # Sort the columns of W by peak frequency bin
        >>> W, H = librosa.decompose.decompose(S)
        >>> W_sort = librosa.util.axis_sort(W)

        >>> # Or sort by the lowest frequency bin
        >>> W_sort = librosa.util.axis_sort(W, value=np.argmin)

        >>> # Or sort the rows instead of the columns
        >>> W_sort_rows = librosa.util.axis_sort(W, axis=0)

        >>> # Get the sorting index also, and use it to permute the rows of H
        >>> W_sort, idx = librosa.util.axis_sort(W, index=True)
        >>> H_sort = H[index, :]
        >>> # np.dot(W_sort, H_sort) == np.dot(W, H)

    :parameters:
      - S : np.ndarray [shape=(d, n)]
          Array to be sorted

      - axis : int [scalar]
          The axis along which to sort.

          - ``axis=0`` to sort rows by peak column index
          - ``axis=1`` to sort columns by peak row index

      - index : boolean [scalar]
          If true, returns the index array as well as the permuted data.

      - value : function
          function to return the index corresponding to the sort order.
          Default: ``np.argmax``.

    :returns:
      - S_sort : np.ndarray [shape=(d, n)]
          ``S`` with the columns or rows permuted in sorting order

      - idx : np.ndarray (optional) [shape=(d,) or (n,)]
        If ``index == True``, the sorting index used to permute ``S``.
        Length of ``idx`` corresponds to the selected ``axis``.

    :raises:
      - ValueError
          If ``S`` does not have exactly 2 dimensions.
    '''

    if value is None:
        value = np.argmax

    if S.ndim != 2:
        raise ValueError('axis_sort is only defined for 2-dimensional arrays.')

    bin_idx = value(S, axis=np.mod(1-axis, S.ndim))
    idx = np.argsort(bin_idx)

    if axis == 0:
        if index:
            return S[idx, :], idx
        else:
            return S[idx, :]
    else:
        if index:
            return S[:, idx], idx
        else:
            return S[:, idx]


def normalize(S, norm=np.inf, axis=0):
    '''Normalize the columns or rows of a matrix

    :parameters:
      - S : np.ndarray [shape=(d, n)]
          The matrix to normalize

      - norm : {inf, -inf, 0, float > 0}
          - ``inf``  : maximum absolute value
          - ``-inf`` : mininum absolute value
          - ``0``    : number of non-zeros
          - float  : corresponding l_p norm.
            See ``scipy.linalg.norm`` for details.

      - axis : int [scalar]
          Axis along which to compute the norm.
          ``axis=0`` will normalize columns, ``axis=1`` will normalize rows.

    :returns:
      - S_norm : np.ndarray [shape=S.shape]
          Normalized matrix

    .. note::
        Columns/rows with length 0 will be left as zeros.
    '''

    # All norms only depend on magnitude, let's do that first
    mag = np.abs(S)

    if norm == np.inf:
        length = np.max(mag, axis=axis, keepdims=True)

    elif norm == -np.inf:
        length = np.min(mag, axis=axis, keepdims=True)

    elif norm == 0:
        length = np.sum(mag > 0, axis=axis, keepdims=True)

    elif np.issubdtype(type(norm), np.number) and norm > 0:
        length = np.sum(mag ** norm, axis=axis, keepdims=True)**(1./norm)
    else:
        raise ValueError('Unsupported norm value: ' + repr(norm))

    # Avoid div-by-zero
    length[length == 0] = 1.0

    return S / length


def match_intervals(intervals_from, intervals_to):
    '''Match one set of time intervals to another.

    This can be useful for mapping beat timings to segments.

    :parameters:
      - intervals_from : ndarray [shape=(n, 2)]
          The time range for source intervals.
          The ``i`` th interval spans time ``intervals_from[i, 0]``
          to ``intervals_from[i, 1]``.
          ``intervals_from[0, 0]`` should be 0, ``intervals_from[-1, 1]``
          should be the track duration.

      - intervals_to : ndarray [shape=(m, 2)]
          Analogous to ``intervals_from``.

    :returns:
      - interval_mapping : ndarray [shape=(n,)]
          For each interval in ``intervals_from``, the
          corresponding interval in ``intervals_to``.
    '''

    # The overlap score of a beat with a segment is defined as
    #   max(0, min(beat_end, segment_end) - max(beat_start, segment_start))

    starts = np.maximum.outer(intervals_from[:, 0], intervals_to[:, 0])
    ends = np.minimum.outer(intervals_from[:, 1], intervals_to[:, 1])
    score = np.maximum(0, ends - starts)

    return np.argmax(score, axis=1)


def find_files(directory, ext=None, recurse=True, case_sensitive=False,
               limit=None, offset=0):
    '''Get a sorted list of (audio) files in a directory or directory sub-tree.

    :usage:
       >>> # Get all audio files in a directory sub-tree
       >>> files = librosa.util.find_files('~/Music')

       >>> # Look only within a specific directory, not the sub-tree
       >>> files = librosa.util.find_files('~/Music', recurse=False)

       >>> # Only look for mp3 files
       >>> files = librosa.util.find_files('~/Music', ext='mp3')

       >>> # Or just mp3 and ogg
       >>> files = librosa.util.find_files('~/Music', ext=['mp3', 'ogg'])

       >>> # Only get the first 10 files
       >>> files = librosa.util.find_files('~/Music', limit=10)

       >>> # Or last 10 files
       >>> files = librosa.util.find_files('~/Music', offset=-10)

    :parameters:
      - directory : str
          Path to look for files

      - ext : str or list of str
          A file extension or list of file extensions to include in the search.

          Default: ``['aac', 'au', 'flac', 'm4a', 'mp3', 'ogg', 'wav']``

      - recurse : boolean
          If ``True``, then all subfolders of ``directory`` will be searched.

          Otherwise, only ``directory`` will be searched.

      - case_sensitive : boolean
          If ``False``, files matching upper-case version of
          extensions will be included.

      - limit : int > 0 or None
          Return at most ``limit`` files. If ``None``, all files are returned.

      - offset : int
          Return files starting at ``offset`` within the list.

          Use negative values to offset from the end of the list.

    :returns:
      - files : list of str
          The list of audio files.
    '''

    def _get_files(dir_name, extensions):
        '''Helper function to get files in a single directory'''

        # Expand out the directory
        dir_name = os.path.abspath(os.path.expanduser(dir_name))

        myfiles = []
        for sub_ext in extensions:
            globstr = os.path.join(dir_name, '*' + os.path.extsep + sub_ext)
            myfiles.extend(glob.glob(globstr))

        return myfiles

    if ext is None:
        ext = ['aac', 'au', 'flac', 'm4a', 'mp3', 'ogg', 'wav']

    elif isinstance(ext, str):
        if not case_sensitive:
            ext = ext.lower()
        ext = [ext]

    # Generate upper-case versions
    if not case_sensitive:
        for i in range(len(ext)):
            ext.append(ext[i].upper())

    files = []

    if recurse:
        for walk in os.walk(directory):
            files.extend(_get_files(walk[0], ext))
    else:
        files = _get_files(directory, ext)

    files.sort()
    files = files[offset:]
    if limit is not None:
        files = files[:limit]

    return files


class FeatureExtractor(BaseEstimator, TransformerMixin):
    """Sci-kit learn wrapper class for feature extraction methods.

    This class acts as a bridge between feature extraction functions
    and scikit-learn pipelines.

    :usage:
        >>> import librosa
        >>> import sklearn.pipeline

        >>> # Build a mel-spectrogram extractor
        >>> MS = librosa.util.FeatureExtractor(librosa.feature.melspectrogram,
                                               sr=22050, n_fft=2048,
                                               n_mels=128, fmax=8000)

        >>> # And a log-amplitude extractor
        >>> LA = librosa.util.FeatureExtractor(librosa.logamplitude,
                                               ref_power=np.max)

        >>> # Chain them into a pipeline
        >>> Features = sklearn.pipeline.Pipeline([('MelSpectrogram', MS),
                                                  ('LogAmplitude', LA)])

        >>> # Load an audio file
        >>> y, sr = librosa.load('file.mp3', sr=22050)

        >>> # Apply the transformation to y
        >>> F = Features.transform([y])

    :parameters:
      - function : function
          The feature extraction function to wrap.

          Example: ``librosa.feature.melspectrogram``

      - target : str or None
          If ``None``, then ``function`` is called with the input
          data as the first positional argument.

          If ``str``, then ``function`` is called with the input
          data as a keyword argument with key ``target``.

      - iterate : bool
          If ``True``, then ``function`` is applied iteratively to each
          item of the input.

          If ``False``, then ``function`` is applied to the entire data
          stream simultaneously.  This is useful for things like aggregation
          and stacking.

      - *kwargs*
          Parameters to be passed through to ``function``
    """

    def __init__(self, function, target=None, iterate=True, **kwargs):
        self.function = function
        self.target = target
        self.iterate = iterate
        self.kwargs = {}

        self.set_params(**kwargs)

    # Clobber _get_param_names here for transparency
    def _get_param_names(self):
        """Returns the parameters of the feature extractor as a dictionary."""
        temp_params = {'function': self.function, 'target': self.target}

        temp_params.update(self.kwargs)

        return temp_params

    # Wrap set_params to catch updates
    def set_params(self, **kwargs):
        """Update the parameters of the feature extractor."""

        # We don't want non-functional arguments polluting kwargs
        params = kwargs.copy()
        for k in ['function', 'target']:
            params.pop(k, None)

        self.kwargs.update(params)
        BaseEstimator.set_params(self, **kwargs)

    # We keep these arguments for compatibility, but don't use them.
    def fit(self, *args, **kwargs):  # pylint: disable=unused-argument
        """This function does nothing, and is provided for interface compatibility.

        .. note:: Since most ``TransformerMixin`` classes implement some
            statistical modeling (e.g., PCA), the ``fit()`` method is
            required.

            For the ``FeatureExtraction`` class, all parameters are fixed
            ahead of time, and no statistical estimation takes place.
        """

        return self

    # Variable name 'X' is for consistency with sklearn
    def transform(self, X):  # pylint: disable=invalid-name
        """Applies the feature transformation to an array of input data.

        :parameters:
          - X : iterable
              Array or list of input data

        :returns:
          - X_transform : list
              In positional argument mode (target=None), then
              ``X_transform[i] = function(X[i], [feature parameters])``

              If the ``target`` parameter was given, then
              ``X_transform[i] = function(target=X[i], [feature parameters])``
        """

        if self.target is not None:
            # If we have a target, each element of X takes the keyword argument
            if self.iterate:
                return [self.function(**dict(list(self.kwargs.items())
                                             + list({self.target: i}.items())))
                        for i in X]
            else:
                return self.function(**dict(list(self.kwargs.items())
                                            + list({self.target: X}.items())))
        else:
            # Each element of X takes first position in function()
            if self.iterate:
                return [self.function(i, **self.kwargs) for i in X]
            else:
                return self.function(X, **self.kwargs)


def buf_to_int(x, n_bytes=2):
    """Convert a floating point buffer into integer values.
    This is primarily useful as an intermediate step in wav output.

    .. seealso:: :func:`librosa.util.buf_to_float`

    :parameters:
        - x : np.ndarray [dtype=float]
            Floating point data buffer

        - n_bytes : int [1, 2, 4]
            Number of bytes per output sample

    :returns:
        - x_int : np.ndarray [dtype=int]
            The original buffer cast to integer type.
    """

    # What is the scale of the input data?
    scale = float(1 << ((8 * n_bytes) - 1))

    # Construct a format string
    fmt = '<i{:d}'.format(n_bytes)

    # Rescale and cast the data
    return (x * scale).astype(fmt)


def buf_to_float(x, n_bytes=2, dtype=np.float32):
    """Convert an integer buffer to floating point values.
    This is primarily useful when loading integer-valued wav data
    into numpy arrays.

    .. seealso:: :func:`librosa.util.buf_to_float`

    :parameters:
        - x : np.ndarray [dtype=int]
            The integer-valued data buffer

        - n_bytes : int [1, 2, 4]
            The number of bytes per sample in ``x``

        - dtype : numeric type
            The target output type (default: 32-bit float)

    :return:
        - x_float : np.ndarray [dtype=float]
            The input data buffer cast to floating point
    """

    # Invert the scale of the data
    scale = 1./float(1 << ((8 * n_bytes) - 1))

    # Construct the format string
    fmt = '<i{:d}'.format(n_bytes)

    # Rescale and format the data buffer
    return scale * np.frombuffer(x, fmt).astype(dtype)
