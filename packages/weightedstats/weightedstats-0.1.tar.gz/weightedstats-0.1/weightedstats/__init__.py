#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Weighted statistics.

A small Python module with functions to calculate weighted mean,
median, and weighted median.

"""
from __future__ import division

__title__      = "WeightedStats"
__version__    = "0.1"
__author__     = "Jack Peterson"
__email__      = "jack@tinybike.net"
__license__    = "MIT"

def weighted_mean(data, weights=None):
    """Calculate the weighted mean of a list."""
    import numpy as np
    weights = np.array(weights).flatten() / float(sum(weights))
    return np.dot(np.array(data), weights)

def median(data):
    """Calculate the median of a list."""
    data.sort()
    num_values = len(data)
    half = num_values // 2
    if num_values % 2:
        return data[half]
    return 0.5 * (data[half-1] + data[half])

def weighted_median(data, weights=None):
    """Calculate the weighted median of a list."""
    if weights is None:
        return median(data)
    midpoint = 0.5 * sum(weights)
    if any([j > midpoint for j in weights]):
        return data[weights.index(max(weights))]
    if any([j > 0 for j in weights]):
        sorted_data, sorted_weights = zip(*sorted(zip(data, weights)))
        cumulative_weight = 0
        below_midpoint_index = 0
        while cumulative_weight <= midpoint:
            below_midpoint_index += 1
            cumulative_weight += sorted_weights[below_midpoint_index-1]
        cumulative_weight -= sorted_weights[below_midpoint_index-1]
        if cumulative_weight == midpoint:
            bounds = sorted_data[below_midpoint_index-2:below_midpoint_index]
            return sum(bounds) / float(len(bounds))
        return sorted_data[below_midpoint_index-1]

def numpy_weighted_median(data, weights=None):
    """Calculate the weighted median of an array/list using numpy."""
    import numpy as np
    if weights is None:
        return np.median(np.array(data).flatten())
    data, weights = np.array(data).flatten(), np.array(weights).flatten()
    if any(weights > 0):
        sorted_data, sorted_weights = map(np.array, zip(*sorted(zip(data, weights))))
        midpoint = 0.5 * sum(sorted_weights)
        if any(weights > midpoint):
            return (data[weights == np.max(weights)])[0]
        cumulative_weight = np.cumsum(sorted_weights)
        below_midpoint_index = np.where(cumulative_weight <= midpoint)[0][-1]
        if cumulative_weight[below_midpoint_index] == midpoint:
            return np.mean(sorted_data[below_midpoint_index:below_midpoint_index+2])
        return sorted_data[below_midpoint_index+1]
