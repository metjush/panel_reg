"""
Build a Pandas panel from disparate data sources
Pandas dataframes
Numpy arrays
...

A utility for simplifying work with FE/FD classes
"""

import pandas as pd
import numpy as np


class PanelBuilder(object):
    def __init__(self):
        """
        Initialize the object
        At first, don't specify anything, there will be functions to set everything
        Only create placeholders
        :return: nothing
        """

        self.time_series = None
        self.entities = None
        self.data_dict = {}

        self.dimensions = [0,0,0] # items * times * variables

        self.panel = None

    def specify_times(self, times):
        """
        specify the time series in the panel
        :param times: array-like (np.array, pd.Series, list) of integers or strings (if in a format like 2015M1 or 2014Q3
        :return: nothing
        """

        # convert to np.array
        if type(times) is pd.Series:
            times = times.values
        elif type(times) is list:
            times = np.array(times)
        elif type(times) is tuple:
            times = np.array(list(times))

        assert type(times) is np.array

        times = times.flatten() # just in case if it were passed as (1,x) or something

        self.time_series = times
        self.dimensions[1] = len(times)

    def specify_entities(self, entities):
        """
        specify the list of entities in the panel
        :param entities: array-like of integers or strings (can be an ID, or a name)
        :return: nothing
        """

        # convert to np.array
        if type(entities) is pd.Series:
            entities = entities.values
        elif type(entities) is list:
            entities = np.array(entities)
        elif type(entities) is tuple:
            entities = np.array(list(entities))

        assert type(entities) is np.array

        entities = entities.flatten()

        self.entities = entities
        self.dimensions[0] = len(entities)
