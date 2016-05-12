"""
Fixed Effects for Panel Data
"""

import numpy as np
import pandas as pd
import statsmodels.api as sm


class FixedEffects(object):
    def __init__(self, panel, y, x, time=False):
        """
        Initialize the Fixed Effects class
        :param panel: Pandas Panel where items are entities, major axis is time and minor axis are variables
        :param y: name of the dependent variable
        :param x: name of the independent variables
        :param time: whether to include time effects too
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

        self.y_demeaned = self.y_panel.copy()
        self.x_demeaned = self.x_panel.copy()

        self.result = None

        self.time = time

    def __demean(self):
        """
        Demean all variables
        Depending on self.time, also include time fixed effects
        By default, only include entity fixed effects
        :return: nothing
        """

        if self.time:
            # twoway demeaning
            y_entity_mean = self.y_panel.mean(axis=0)
            y_time_mean = self.y_panel.mean(axis=1)
            y_grand_mean = self.y_panel.mean().mean() # double mean
            self.y_demeaned = self.y_demeaned - y_entity_mean + y_grand_mean # still need to remove time mean
            self.y_demeaned = self.y_demeaned.sub(y_time_mean, axis=0)

            for indvar in self.indvars:
                slice = self.x_panel.loc[:, :, indvar]
                slice_ent_mean = slice.mean(axis=0)
                slice_time_mean = slice.mean(axis=1)
                slice_g_mean = slice_ent_mean.mean()
                self.x_demeaned.loc[:, :, indvar] = self.x_demeaned.loc[:, :, indvar] - slice_ent_mean + slice_g_mean
                self.x_demeaned.loc[:, :, indvar] = self.x_demeaned.loc[:, :, indvar].sub(slice_time_mean, axis=0)
        else:
            # only entity fixed effects
            y_mean = self.y_panel.mean() # ths will give means by entity
            self.y_demeaned = self.y_demeaned - y_mean  # demean y

            for indvar in self.indvars:
                slice = self.x_panel.loc[:, :, indvar]
                slice_mean = slice.mean()
                self.x_demeaned.loc[:, :, indvar] = self.x_demeaned.loc[:, :, indvar] - slice_mean

