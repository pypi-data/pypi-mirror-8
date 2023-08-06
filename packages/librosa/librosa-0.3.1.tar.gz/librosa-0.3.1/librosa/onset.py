#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Onset detection"""

import numpy as np
import scipy
import scipy.signal

import librosa.core
import librosa.feature


def onset_detect(y=None, sr=22050, onset_envelope=None, hop_length=64,
                 **kwargs):
    """Basic onset detector.  Locate note onset events by picking peaks in an
    onset strength envelope.

    See also: :func:`librosa.onset.onset_strength()`

    :usage:
        >>> # Get onset times from a signal
        >>> onset_frames = librosa.onset.onset_detect(y=y,
                                                      sr=sr, hop_length=64)
        >>> onset_times = librosa.frames_to_time(onset_frames,
                                                 sr, hop_length=64)

        >>> # Or use a pre-computed onset envelope
        >>> o_env = librosa.onset.onset_strength(y, sr=sr)
        >>> onset_frames = librosa.onset.onset_detect(onset_envelope=o_env,
                                                      sr=sr)
        >>> onset_times = librosa.frames_to_time(onset_frames,
                                                 sr, hop_length=64)

    :parameters:
      - y          : np.ndarray [shape=(n,)]
          audio time series

      - sr         : int > 0 [scalar]
          sampling rate of ``y``

      - onset_envelope     : np.ndarray [shape=(m,)]
          (optional) pre-computed onset stength envelope

      - hop_length : int > 0 [scalar]
          hop length (in samples)

      - *kwargs*
          Additional parameters for peak picking

          See :func:`librosa.core.peak_pick()` for details

    :returns:

      - onsets : np.ndarray [shape=(n_onsets,)]
          estimated frame numbers of onsets

    :raises:
      - ValueError
          if neither ``y`` nor ``onsets`` are provided

    .. note::
      If no onset strength could be detected, onset_detect returns
      an empty list.

      The peak_pick parameters were chosen by large-scale hyper-parameter
      optimization over this dataset:
      https://github.com/CPJKU/onset_db
    """

    # First, get the frame->beat strength profile if we don't already have one
    if onset_envelope is None:
        if y is None:
            raise ValueError('Either "y" or "onsets" must be provided')

        onset_envelope = onset_strength(y=y, sr=sr, hop_length=hop_length)

    # Do we have any onsets to grab?
    if not onset_envelope.any():
        return np.array([], dtype=np.int)

    # Normalize onset strength function to [0, 1] range
    # (a common normalization step to make the threshold more consistent)
    onset_envelope -= onset_envelope.min()
    onset_envelope /= onset_envelope.max()

    # These parameter settings found by large-scale search
    kwargs.setdefault('pre_max', 0.03*sr/hop_length)    # 30ms
    kwargs.setdefault('post_max', 0.00*sr/hop_length)   # 0ms
    kwargs.setdefault('pre_avg', 0.10*sr/hop_length)    # 100ms
    kwargs.setdefault('post_avg', 0.10*sr/hop_length)   # 100ms
    kwargs.setdefault('wait', 0.03*sr/hop_length)       # 30ms
    kwargs.setdefault('delta', 0.06)

    # Peak pick the onset envelope
    return librosa.core.peak_pick(onset_envelope, **kwargs)


def onset_strength(y=None, sr=22050, S=None, detrend=False, centering=True,
                   feature=None, aggregate=None, **kwargs):
    """Compute a spectral flux onset strength envelope.

    Onset strength at time t is determined by:

    ``mean_f max(0, S[f, t+1] - S[f, t])``

    By default, if a time series ``y`` is provided, S will be the
    log-power Mel spectrogram.

    :usage:
        >>> # Mean aggregation with Mel-scaled spectrogram
        >>> o_env = librosa.onset.onset_strength(y, sr)

        >>> # Median aggregation
        >>> o_env = librosa.onset.onset_strength(y, sr,
                                                 aggregate=np.median)

        >>> # Log-frequency spectrogram instead of Mel
        >>> o_env = librosa.onset.onset_strength(y, sr,
                                                 feature=librosa.feature.logfsgram)

        >>> # Or Mel spectrogram with customized options
        >>> o_env = librosa.onset.onset_strength(y, sr,
                                                 n_mels=128,
                                                 fmin=32,
                                                 fmax=8000)

    :parameters:
      - y        : np.ndarray [shape=(n,)]
          audio time-series

      - sr       : int > 0 [scalar]
          sampling rate of ``y``

      - S        : np.ndarray [shape=(d, m)]
          pre-computed (log-power) spectrogram

      - detrend : bool [scalar]
          Filter the onset strength to remove the DC component

      - centering : bool [scalar]
          Shift the onset function by ``n_fft / (2 * hop_length)`` frames

      - feature : function
          Function for computing time-series features, eg, scaled spectrograms.
          By default, uses :func:`librosa.feature.melspectrogram`

      - aggregate : function
          Aggregation function to use when combining onsets
          at different frequency bins.
          Default: ``np.mean``

      - *kwargs*
          Additional parameters to ``feature()``, if ``S`` is not provided.

    .. note:: if ``S`` is provided, then ``(y, sr)`` are optional.

    :returns:
      - onset_envelope   : np.ndarray [shape=(m,)]
          vector containing the onset strength envelope

    :raises:
      - ValueError
          if neither ``(y, sr)`` nor ``S`` are provided
    """

    if feature is None:
        feature = librosa.feature.melspectrogram

    if aggregate is None:
        aggregate = np.mean

    # First, compute mel spectrogram
    if S is None:
        if y is None:
            raise ValueError('One of "S" or "y" must be provided.')

        S = np.abs(feature(y=y, sr=sr, **kwargs))

        # Convert to dBs
        S = librosa.core.logamplitude(S)

    # Retrieve the n_fft and hop_length,
    # or default values for onsets if not provided
    n_fft = kwargs.get('n_fft', 2048)
    hop_length = kwargs.get('hop_length', 64)

    # Compute first difference, include padding for alignment purposes
    onset_env = np.diff(S, axis=1)
    onset_env = np.pad(onset_env, ([0, 0], [1, 0]), mode='constant')

    # Discard negatives (decreasing amplitude)
    onset_env = np.maximum(0.0, onset_env)

    # Average over mel bands
    onset_env = aggregate(onset_env, axis=0)

    # Counter-act framing effects. Shift the onsets by n_fft / hop_length
    if centering:
        onset_env = np.pad(onset_env,
                           (int(n_fft / (2 * hop_length)), 0),
                           mode='constant')

    # remove the DC component
    if detrend:
        onset_env = scipy.signal.lfilter([1.0, -1.0], [1.0, -0.99], onset_env)

    return onset_env
