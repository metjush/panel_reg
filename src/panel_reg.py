"""
Wrapper object for all utilities and estimation models

"""

from fixed_effects import FixedEffects
from first_diff import FirstDiff
from panel_builder import PanelBuilder


class PanelReg(object):
    def __init__(self):
        """
        Initialize the object
        :return: nothing
        """
        pass

    def fd(self):
        """
        Returns the First Diff object
        :return: FirstDiff
        """

        return FirstDiff

    def fe(self):
        """
        Returns the FE object
        :return: FixedEffects
        """

        return FixedEffects

    def build(self):
        """
        Returns the panel building object
        :return: PanelBuilder
        """

        return PanelBuilder
