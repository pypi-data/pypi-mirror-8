#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Spectrogram decomposition"""

import numpy as np
import scipy
import scipy.signal

import sklearn.decomposition

import librosa.core


def decompose(S, n_components=None, transformer=None, sort=False):
    """Decompose a feature matrix.

    Given a spectrogram ``S``, produce a decomposition into ``components``
    and ``activations`` such that ``S ~= components.dot(activations)``.

    By default, this is done with with non-negative matrix factorization (NMF),
    but any ``sklearn.decomposition``-type object will work.

    :usage:
        >>> # Decompose a magnitude spectrogram into 32 components with NMF
        >>> S = np.abs(librosa.stft(y))
        >>> comps, acts = librosa.decompose.decompose(S, n_components=32)

        >>> # Sort components by ascending peak frequency
        >>> comps, acts = librosa.decompose.decompose(S, n_components=32,
                                                      sort=True)

        >>> # Or with sparse dictionary learning
        >>> T = sklearn.decomposition.DictionaryLearning(n_components=32)
        >>> comps, acts = librosa.decompose.decompose(S, transformer=T)

    :parameters:
        - S : np.ndarray [shape=(n_features, n_samples), dtype=float]
            The input feature matrix (e.g., magnitude spectrogram)

        - n_components : int > 0 [scalar] or None
            number of desired components
            if None, then ``n_features`` components are used

        - transformer : None or object
            If None, use ``sklearn.decomposition.NMF``

            Otherwise, any object with a similar interface to NMF should work.
            ``transformer`` must follow the scikit-learn convention, where
            input data is ``(n_samples, n_features)``.

            ``transformer.fit_transform()`` will be run on ``S.T`` (not ``S``),
            the return value of which is stored (transposed) as ``activations``

            The components will be retrieved as ``transformer.components_.T``

            ``S ~= np.dot(activations, transformer.components_).T``

            or equivalently:
            ``S ~= np.dot(transformer.components_.T, activations.T)``

        - sort : bool
            If ``True``, components are sorted by ascending peak frequency.

          .. note:: If used with ``transformer``, sorting is applied to copies
            of the decomposition parameters, and not to ``transformer``'s
            internal parameters.


    :returns:
        - components: np.ndarray [shape=(n_features, n_components)]
            matrix of components (basis elements).

        - activations: np.ndarray [shape=(n_components, n_samples)]
            transformed matrix/activation matrix
    """

    if transformer is None:
        transformer = sklearn.decomposition.NMF(n_components=n_components)

    activations = transformer.fit_transform(S.T).T

    components = transformer.components_.T

    if sort:
        components, idx = librosa.util.axis_sort(components, index=True)
        activations = activations[idx]

    return components, activations


def hpss(S, kernel_size=31, power=2.0, mask=False):
    """Median-filtering harmonic percussive source separation (HPSS).

    Decomposes an input spectrogram ``S = H + P``
    where ``H`` contains the harmonic components,
    and ``P`` contains the percussive components.

    :usage:
        >>> # Separate into harmonic and percussive
        >>> D = librosa.stft(y)
        >>> H, P = librosa.decompose.hpss(D)
        >>> # Resynthesize the harmonic component as a waveform
        >>> y_harmonic = librosa.istft(H)

        >>> # Or with a narrower horizontal filter
        >>> H, P = librosa.decompose.hpss(D, kernel_size=(13, 31))

        >>> # Just get harmonic/percussive masks, not the spectra
        >>> mask_H, mask_P = librosa.decompose.hpss(D, mask=True)

    :parameters:
      - S : np.ndarray [shape=(d, n)]
          input spectrogram. May be real (magnitude) or complex.

      - kernel_size : int or tuple (kernel_harmonic, kernel_percussive)
          kernel size(s) for the median filters.
          If scalar, the same size is used for both harmonic and percussive.
          If array_like, the first value specifies the width of the
          harmonic filter, and the second value specifies the width of the
          percussive filter.

      - power : float >= 0 [scalar]
          Exponent for the Wiener filter when constructing mask matrices.
          Mask matrices are defined by
          ``mask_H = (r_H ** power) / (r_H ** power + r_P ** power)``
          where ``r_H`` and ``r_P`` are the median-filter responses for
          harmonic and percussive components.

      - mask : bool
          Return the masking matrices instead of components

    :returns:
      - harmonic : np.ndarray [shape=(d, n)]
          harmonic component (or mask)

      - percussive : np.ndarray [shape=(d, n)]
          percussive component (or mask)

    .. note::
      - Fitzgerald, Derry.
        "Harmonic/percussive separation using median filtering." (2010).

    """

    if np.iscomplexobj(S):
        S, phase = librosa.core.magphase(S)
    else:
        phase = 1

    if np.isscalar(kernel_size):
        win_harm = kernel_size
        win_perc = kernel_size
    else:
        win_harm = kernel_size[0]
        win_perc = kernel_size[1]

    # Compute median filters. Pre-allocation here preserves memory layout.
    harm = np.empty_like(S)
    harm[:] = scipy.signal.medfilt2d(S, kernel_size=(1, win_harm))

    perc = np.empty_like(S)
    perc[:] = scipy.signal.medfilt2d(S, kernel_size=(win_perc, 1))

    if mask or power == 0:
        mask_harm = (harm > perc).astype(float)
        mask_perc = 1 - mask_harm
        if mask:
            return mask_harm, mask_perc
    else:
        perc = perc ** power
        zero_perc = (perc == 0)
        perc[zero_perc] = 0.0

        harm = harm ** power
        zero_harm = (harm == 0)
        harm[zero_harm] = 0.0

        # Find points where both are zero, equalize
        harm[zero_harm & zero_perc] = 0.5
        perc[zero_harm & zero_perc] = 0.5

        # Compute harmonic mask
        mask_harm = harm / (harm + perc)
        mask_perc = perc / (harm + perc)

    return ((S * mask_harm) * phase, (S * mask_perc) * phase)
