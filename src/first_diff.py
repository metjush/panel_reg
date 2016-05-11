"""
First Differences for Panel data
"""

import numpy as np
import pandas as pd
import statsmodels.api as sm


class FirstDiff(object):
    def __init__(self, panel, y, x):
        """
        Initialize the first difference class
        :param panel: Pandas Panel where items are entities, major axis is time and minor axis are variables
        :param y: name of the dependent variable
        :param x: name of the independent variables
        :return: nothing
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

        self.y_panel = self.panel.loc[:, :, self.depvar].astype(np.float)
        self.x_panel = self.panel.loc[:, :, self.indvars].astype(np.float)

        self.result = None

    def __first_diff(self):
        """
        First difference the supplied data
        :return: nothing
        """

        self.fd_y = self.y_panel.diff(1)
        self.fd_x = self.x_panel.copy()
        for indvar in self.indvars:
            slice = self.x_panel.loc[:,:,indvar].diff(1)
            self.fd_x.loc[:,:,indvar] = slice

    def estimate(self):
        """
        Estimate the first differenced OLS
        :return: results
        """
        # first difference data
        self.__first_diff()

        # first, make a dataframe out of the panel of indvars
        x_dataframe = self.fd_x.transpose(2,0,1).to_frame(False) # set to False to not drop NaNs
        # unstack the depvar dataframe into a series
        y_series = self.fd_y.unstack()

        # fit regression model with statsmodels
        results = sm.OLS(y_series.values, x_dataframe.values, missing='drop').fit()

        print(results.summary(self.depvar, self.indvars))

        self.result = results

