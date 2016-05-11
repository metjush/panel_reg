"""
First Differences for Panel data
"""

import numpy as np
import pandas as pd


class FirstDiff(object):
    def __init__(self, panel, y, x):
        """
        Initialize the first difference class
        :param panel: Pandas Panel where items are entities, major axis is time and minor axis are variables
        :param y: name of the dependent variable
        :param x: name of the independent variables
        :return:
        """

        assert type(panel) is pd.Panel

        self.panel = panel

        self.variables = panel.axes[2].tolist()  # get minor axis
        self.times = panel.axes[1].tolist()  # get major axis
        self.entities = panel.axes[0].tolist()  # get entities

        assert y in self.variables

        if type(x) is str:
            x = [x]

        for indvar in x:
            assert indvar in self.variables
            assert indvar != y

        self.depvar = y
        self.indvars = x

        self.y_panel = self.panel.loc[:, :, self.depvar]
        self.x_panel = self.panel.loc[:, :, self.indvars]
