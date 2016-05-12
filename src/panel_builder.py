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
        self.variables = None

        self.data_dict = {}
        self.dict_key = 'time'

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
        print('Time dimension set to size %d' % self.dimensions[1])

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
        print('Entity dimension set to size %d' % self.dimensions[0])

    def specify_variables(self, variables):
        """
        specify variable names in the panel
        :param variables: array-like of strings
        :return: nothing
        """

        # convert to np.array
        if type(variables) is pd.Series:
            variables = variables.values
        elif type(variables) is list:
            variables = np.array(variables)
        elif type(variables) is tuple:
            variables = np.array(list(variables))

        assert type(variables) is np.array

        variables = variables.flatten()

        self.variables = variables
        self.dimensions[2] = len(variables)
        print('Variable dimension set to size %d' % self.dimensions[2])

    def frames_by_time(self, use_index=False, use_columns=False, *frames):
        """
        Pass frames (entity * variable) by year as arguments
        :param use_index: whether to use index from dataframes (if they are pandas dataframes)
        :param use_columns: whether to use column names from dataframes (if they are pandas dataframes)
        :param frames: list of frame-like (pandas dataframe or 2D numpy array or multidimensional list)
        :return: nothing
        """

        # check if fits with already supplied times
        count = len(frames)
        if self.dimensions[1] > 0:
            assert count == self.dimensions[1]
        else:
            print('Time dimension not yet set, using the number of passed dataframes: %d' % count)
            print('Setting the time periods to be a list of integers starting from 0')
            self.dimensions[1] = count
            self.time_series = np.arange(count)

        # iterate over each frame
        self.dict_key = 'time'
        checked_indices = False
        for time, frame in zip(self.time_series, frames):
            # check if it is a pandas frame
            if type(frame) is pd.DataFrame:
                frame_values = frame.values

                # check dimensionality and use index/column names if requred
                if not checked_indices:
                    if self.dimensions[0] == 0:
                        print('Entity dimension not yet set, using the number of rows in first dataframe: %d' % frame_values.shape[0])
                        self.dimensions[0] = frame_values.shape[0]
                        self.entities = frame.index.values if use_index else np.arange(self.dimensions[0])
                    if self.dimensions[2] == 0:
                        print('Variable dimension not yet set, using the number of columns in first dataframe: %d' % frame_values.shape[1])
                        self.dimensions[2] = frame_values.shape[1]
                        self.variables = frame.columns.values if use_columns else np.arange(self.dimensions[2])
                    checked_indices = True

                assert frame_values.shape is (self.dimensions[0], self.dimensions[2])

                self.data_dict[time] = pd.DataFrame(frame_values, index=self.entities, columns=self.variables)

            # if it is a multilist
            else:
                if type(frame) is list:
                    frame = np.array(frame)

                # if it is a np.array
                assert type(frame) is np.array

                if not checked_indices:
                    if self.dimensions[0] == 0:
                        print('Entity dimension not yet set, using the number of rows in first dataframe: %d' % frame.shape[0])
                        self.dimensions[0] = frame.shape[0]
                        self.entities = np.arange(self.dimensions[0])
                    if self.dimensions[2] == 0:
                        print('Variable dimension not yet set, using the number of columns in first dataframe: %d' % frame.shape[1])
                        self.dimensions[2] = frame.shape[1]
                        self.variables = np.arange(self.dimensions[2])
                    checked_indices = True

                assert frame.shape is (self.dimensions[0], self.dimensions[2])

                self.data_dict[time] = pd.DataFrame(frame, index=self.entities, columns=self.variables)

    def frames_by_entity(self, use_index=False, use_columns=False, *frames):
        """
        Pass frames (time * variables) by entity as list
        :param use_index: whether to use index from dataframes (time, if they are pandas)
        :param use_columns: whether to use columns from dataframes (variables, if they are pandas)
        :param frames: list of frame-like data
        :return: nothing
        """

        # check if fits with already supplied entities
        count = len(frames)
        if self.dimensions[0] > 0:
            assert count == self.dimensions[0]
        else:
            print('Entity dimension not yet set, using the number of passed dataframes: %d' % count)
            print('Setting the entities to be a list of integers starting from 0')
            self.dimensions[0] = count
            self.entities = np.arange(count)

        # iterate over each frame
        self.dict_key = 'entity'
        checked_indices = False
        for item, frame in zip(self.entities, frames):
            # check if it is a pandas frame
            if type(frame) is pd.DataFrame:
                frame_values = frame.values

                # check dimensionality and use index/column names if requred
                if not checked_indices:
                    if self.dimensions[1] == 0:
                        print('Time dimension not yet set, using the number of rows in first dataframe: %d' % frame_values.shape[0])
                        self.dimensions[1] = frame_values.shape[0]
                        self.time_series = frame.index.values if use_index else np.arange(self.dimensions[0])
                    if self.dimensions[2] == 0:
                        print('Variable dimension not yet set, using the number of columns in first dataframe: %d' % frame_values.shape[1])
                        self.dimensions[2] = frame_values.shape[1]
                        self.variables = frame.columns.values if use_columns else np.arange(self.dimensions[2])
                    checked_indices = True

                assert frame_values.shape is (self.dimensions[1], self.dimensions[2])

                self.data_dict[item] = pd.DataFrame(frame_values, index=self.time_series, columns=self.variables)

            # if it is a multilist
            else:
                if type(frame) is list:
                    frame = np.array(frame)

                # if it is a np.array
                assert type(frame) is np.array

                if not checked_indices:
                    if self.dimensions[1] == 0:
                        print('Time dimension not yet set, using the number of rows in first dataframe: %d' % frame.shape[0])
                        self.dimensions[1] = frame.shape[0]
                        self.time_series = np.arange(self.dimensions[0])
                    if self.dimensions[2] == 0:
                        print('Variable dimension not yet set, using the number of columns in first dataframe: %d' % frame.shape[1])
                        self.dimensions[2] = frame.shape[1]
                        self.variables = np.arange(self.dimensions[2])
                    checked_indices = True

                assert frame.shape is (self.dimensions[1], self.dimensions[2])

                self.data_dict[item] = pd.DataFrame(frame, index=self.time_series, columns=self.variables)

    def panel_from_array(self, multiarray):
        """
        Make panel from 3D numpy array
        :param multiarray: 3D numpy array
        :return: nothing
        """

        pass

    def save_panel(self):
        """
        Take all supplied data and create the final pandas Panel
        :return: pandas Panel
        """

        assert 0 not in self.dimensions
        assert self.data_dict != {}

        if self.dict_key == 'time':
            assert len(self.data_dict) == self.dimensions[1]
            panel = pd.Panel(self.data_dict, index=self.time_series, major_axis=self.entities, minor_axis=self.variables).transpose(1,0,2) # put entities into items
        elif self.dict_key == 'entity':
            assert len(self.data_dict) == self.dimensions[0]
            panel = pd.Panel(self.data_dict, major_axis=self.time_series, index=self.entities, minor_axis=self.variables)
        else:
            # not a dict, but a 3D np array
            panel = pd.Panel(self.data_dict, major_axis=self.time_series, index=self.entities, minor_axis=self.variables)

        print(panel)
        return panel


