import pandas as pd
import numpy as np
from scipy.stats import linregress
from scipy.signal import argrelextrema
import math

class Pyangles:
    def __init__(self):
        self.functions = [self.ascending_triangle, self.descending_triangle, self.symmetrical_triangle, self.ascending_channel, self.descending_channel, self.ascending_wedge, self.descending_wedge]

    def search(self, df, key, window, order):
        data = []
        lows, highs = self.range_slopes(df, key, window, order)
        for f in self.functions:
            data.append({'key': f.__name__, 'value': f.__name__.replace('_' , ' ').capitalize() if f(key,lows, highs) else False})
        return data, lows, highs

    def ascending_triangle(self, key,lows, highs):
        return math.isclose(highs[f'{key}_highs_slope'].iloc[-1], 0) and lows[f'{key}_lows_slope'].iloc[-1] > 0

    def descending_triangle(self, key,lows, highs):
        return (math.isclose(lows[f'{key}_lows_slope'].iloc[-1], 0)) and (highs[f'{key}_highs_slope'].iloc[-1] < 0)

    def symmetrical_triangle(self, key,lows, highs):
        return lows[f'{key}_lows_slope'].iloc[-1] > 0 and highs[f'{key}_highs_slope'].iloc[-1] < 0

    def ascending_channel(self, key,lows, highs):
        return lows[f'{key}_lows_slope'].iloc[-1] > 0 and highs[f'{key}_highs_slope'].iloc[-1] > 0 and math.isclose(lows[f'{key}_lows_slope'].iloc[-1], highs[f'{key}_highs_slope'].iloc[-1], rel_tol=100)

    def descending_channel(self, key,lows, highs):
        return lows[f'{key}_lows_slope'].iloc[-1] < 0 and highs[f'{key}_highs_slope'].iloc[-1] < 0 and math.isclose(lows[f'{key}_lows_slope'].iloc[-1], highs[f'{key}_highs_slope'].iloc[-1], rel_tol=100)

    def ascending_wedge(self, key,lows, highs):
        return lows[f'{key}_lows_slope'].iloc[-1] > 0 and highs[f'{key}_highs_slope'].iloc[-1] > 0 and highs[f'{key}_highs_slope'].iloc[-1] > lows[f'{key}_lows_slope'].iloc[-1]

    def descending_wedge(self, key,lows, highs):
        return lows[f'{key}_lows_slope'].iloc[-1] < 0 and highs[f'{key}_highs_slope'].iloc[-1] < 0 and highs[f'{key}_highs_slope'].iloc[-1] > lows[f'{key}_lows_slope'].iloc[-1]

    def range_slopes(self, df, key, window, order):
        low_idx, high_idx = self.high_low_idx(df, key, order)
        lows, highs = df.iloc[low_idx].copy(), df.iloc[high_idx].copy()
        lows[f'{key}_lows_slope'] = lows[key].rolling(window=window[0]).apply(self.get_slope, raw=True)
        highs[f'{key}_highs_slope'] = highs[key].rolling(window=window[1]).apply(self.get_slope, raw=True)
        return lows, highs

    def low_idx(self, df, key, order):
        return argrelextrema(df[key].values, np.less_equal, order=order)[0]

    def high_idx(self, df, key, order):
        return argrelextrema(df[key].values, np.greater_equal, order=order)[0]

    def high_low_idx(self, df, key, order):
        return self.low_idx(df, key, order[0]), self.high_idx(df, key, order[1])

    def get_slope(self, array):
        y = np.array(array)
        x = np.arange(len(y))
        slope, intercept, r_value, p_value, std_err = linregress(x,y)
        return slope