""" Data objects in group "Performance Curves"
"""

from collections import OrderedDict
import logging
from pyidf.helper import DataObject

logger = logging.getLogger("pyidf")
logger.addHandler(logging.NullHandler())



class CurveLinear(DataObject):

    """ Corresponds to IDD object `Curve:Linear`
        Linear curve with one independent variable.
        Input for the linear curve consists of a curve name, the two coefficients, and the
        maximum and minimum valid independent variable values. Optional inputs for
        curve minimum and maximum may be used to limit the output of the performance curve.
        curve = C1 + C2*x
    """
    schema = {'min-fields': 0,
              'name': u'Curve:Linear',
              'pyname': u'CurveLinear',
              'format': None,
              'fields': OrderedDict([(u'name',
                                      {'name': u'Name',
                                       'pyname': u'name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'alpha'}),
                                     (u'coefficient1 constant',
                                      {'name': u'Coefficient1 Constant',
                                       'pyname': u'coefficient1_constant',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient2 x',
                                      {'name': u'Coefficient2 x',
                                       'pyname': u'coefficient2_x',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'minimum value of x',
                                      {'name': u'Minimum Value of x',
                                       'pyname': u'minimum_value_of_x',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'maximum value of x',
                                      {'name': u'Maximum Value of x',
                                       'pyname': u'maximum_value_of_x',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'minimum curve output',
                                      {'name': u'Minimum Curve Output',
                                       'pyname': u'minimum_curve_output',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'maximum curve output',
                                      {'name': u'Maximum Curve Output',
                                       'pyname': u'maximum_curve_output',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'input unit type for x',
                                      {'name': u'Input Unit Type for X',
                                       'pyname': u'input_unit_type_for_x',
                                       'default': u'Dimensionless',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'Dimensionless',
                                                           u'Temperature',
                                                           u'VolumetricFlow',
                                                           u'Pressure',
                                                           u'MassFlow',
                                                           u'Power',
                                                           u'Distance'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'output unit type',
                                      {'name': u'Output Unit Type',
                                       'pyname': u'output_unit_type',
                                       'default': u'Dimensionless',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'Dimensionless',
                                                           u'Capacity',
                                                           u'Power'],
                                       'autocalculatable': False,
                                       'type': 'alpha'})]),
              'extensible-fields': OrderedDict(),
              'unique-object': False,
              'required-object': False,
              'group': u'Performance Curves'}

    @property
    def name(self):
        """Get name.

        Returns:
            str: the value of `name` or None if not set

        """
        return self["Name"]

    @name.setter
    def name(self, value=None):
        """Corresponds to IDD field `Name`

        Args:
            value (str): value for IDD Field `Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Name"] = value

    @property
    def coefficient1_constant(self):
        """Get coefficient1_constant.

        Returns:
            float: the value of `coefficient1_constant` or None if not set

        """
        return self["Coefficient1 Constant"]

    @coefficient1_constant.setter
    def coefficient1_constant(self, value=None):
        """Corresponds to IDD field `Coefficient1 Constant`

        Args:
            value (float): value for IDD Field `Coefficient1 Constant`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient1 Constant"] = value

    @property
    def coefficient2_x(self):
        """Get coefficient2_x.

        Returns:
            float: the value of `coefficient2_x` or None if not set

        """
        return self["Coefficient2 x"]

    @coefficient2_x.setter
    def coefficient2_x(self, value=None):
        """Corresponds to IDD field `Coefficient2 x`

        Args:
            value (float): value for IDD Field `Coefficient2 x`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient2 x"] = value

    @property
    def minimum_value_of_x(self):
        """Get minimum_value_of_x.

        Returns:
            float: the value of `minimum_value_of_x` or None if not set

        """
        return self["Minimum Value of x"]

    @minimum_value_of_x.setter
    def minimum_value_of_x(self, value=None):
        """Corresponds to IDD field `Minimum Value of x`

        Args:
            value (float): value for IDD Field `Minimum Value of x`
                Units are based on field `A2`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Minimum Value of x"] = value

    @property
    def maximum_value_of_x(self):
        """Get maximum_value_of_x.

        Returns:
            float: the value of `maximum_value_of_x` or None if not set

        """
        return self["Maximum Value of x"]

    @maximum_value_of_x.setter
    def maximum_value_of_x(self, value=None):
        """Corresponds to IDD field `Maximum Value of x`

        Args:
            value (float): value for IDD Field `Maximum Value of x`
                Units are based on field `A2`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Maximum Value of x"] = value

    @property
    def minimum_curve_output(self):
        """Get minimum_curve_output.

        Returns:
            float: the value of `minimum_curve_output` or None if not set

        """
        return self["Minimum Curve Output"]

    @minimum_curve_output.setter
    def minimum_curve_output(self, value=None):
        """Corresponds to IDD field `Minimum Curve Output` Specify the minimum
        value calculated by this curve object.

        Args:
            value (float): value for IDD Field `Minimum Curve Output`
                Units are based on field `A3`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Minimum Curve Output"] = value

    @property
    def maximum_curve_output(self):
        """Get maximum_curve_output.

        Returns:
            float: the value of `maximum_curve_output` or None if not set

        """
        return self["Maximum Curve Output"]

    @maximum_curve_output.setter
    def maximum_curve_output(self, value=None):
        """Corresponds to IDD field `Maximum Curve Output` Specify the maximum
        value calculated by this curve object.

        Args:
            value (float): value for IDD Field `Maximum Curve Output`
                Units are based on field `A3`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Maximum Curve Output"] = value

    @property
    def input_unit_type_for_x(self):
        """Get input_unit_type_for_x.

        Returns:
            str: the value of `input_unit_type_for_x` or None if not set

        """
        return self["Input Unit Type for X"]

    @input_unit_type_for_x.setter
    def input_unit_type_for_x(self, value="Dimensionless"):
        """Corresponds to IDD field `Input Unit Type for X`

        Args:
            value (str): value for IDD Field `Input Unit Type for X`
                Default value: Dimensionless
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Input Unit Type for X"] = value

    @property
    def output_unit_type(self):
        """Get output_unit_type.

        Returns:
            str: the value of `output_unit_type` or None if not set

        """
        return self["Output Unit Type"]

    @output_unit_type.setter
    def output_unit_type(self, value="Dimensionless"):
        """Corresponds to IDD field `Output Unit Type`

        Args:
            value (str): value for IDD Field `Output Unit Type`
                Default value: Dimensionless
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Output Unit Type"] = value




class CurveQuadLinear(DataObject):

    """ Corresponds to IDD object `Curve:QuadLinear`
        Linear curve with four independent variables.
        Input for the linear curve consists of a curve name, the two coefficients, and the
        maximum and minimum valid independent variable values. Optional inputs for curve
        minimum and maximum may be used to limit the output of the performance curve.
        curve = C1 + C2*w + C3*x + C4*y + C5*z
    """
    schema = {'min-fields': 0,
              'name': u'Curve:QuadLinear',
              'pyname': u'CurveQuadLinear',
              'format': None,
              'fields': OrderedDict([(u'name',
                                      {'name': u'Name',
                                       'pyname': u'name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'alpha'}),
                                     (u'coefficient1 constant',
                                      {'name': u'Coefficient1 Constant',
                                       'pyname': u'coefficient1_constant',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient2 w',
                                      {'name': u'Coefficient2 w',
                                       'pyname': u'coefficient2_w',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient3 x',
                                      {'name': u'Coefficient3 x',
                                       'pyname': u'coefficient3_x',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient4 y',
                                      {'name': u'Coefficient4 y',
                                       'pyname': u'coefficient4_y',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient5 z',
                                      {'name': u'Coefficient5 z',
                                       'pyname': u'coefficient5_z',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'minimum value of w',
                                      {'name': u'Minimum Value of w',
                                       'pyname': u'minimum_value_of_w',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'maximum value of w',
                                      {'name': u'Maximum Value of w',
                                       'pyname': u'maximum_value_of_w',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'minimum value of x',
                                      {'name': u'Minimum Value of x',
                                       'pyname': u'minimum_value_of_x',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'maximum value of x',
                                      {'name': u'Maximum Value of x',
                                       'pyname': u'maximum_value_of_x',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'minimum value of y',
                                      {'name': u'Minimum Value of y',
                                       'pyname': u'minimum_value_of_y',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'maximum value of y',
                                      {'name': u'Maximum Value of y',
                                       'pyname': u'maximum_value_of_y',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'minimum value of z',
                                      {'name': u'Minimum Value of z',
                                       'pyname': u'minimum_value_of_z',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'maximum value of z',
                                      {'name': u'Maximum Value of z',
                                       'pyname': u'maximum_value_of_z',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'minimum curve output',
                                      {'name': u'Minimum Curve Output',
                                       'pyname': u'minimum_curve_output',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'maximum curve output',
                                      {'name': u'Maximum Curve Output',
                                       'pyname': u'maximum_curve_output',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'input unit type for w',
                                      {'name': u'Input Unit Type for w',
                                       'pyname': u'input_unit_type_for_w',
                                       'default': u'Dimensionless',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'Dimensionless',
                                                           u'Temperature',
                                                           u'VolumetricFlow',
                                                           u'MassFlow',
                                                           u'Power',
                                                           u'Distance',
                                                           u'VolumetricFlowPerPower'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'input unit type for x',
                                      {'name': u'Input Unit Type for x',
                                       'pyname': u'input_unit_type_for_x',
                                       'default': u'Dimensionless',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'Dimensionless',
                                                           u'Temperature',
                                                           u'VolumetricFlow',
                                                           u'MassFlow',
                                                           u'Power',
                                                           u'Distance',
                                                           u'VolumetricFlowPerPower'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'input unit type for y',
                                      {'name': u'Input Unit Type for y',
                                       'pyname': u'input_unit_type_for_y',
                                       'default': u'Dimensionless',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'Dimensionless',
                                                           u'Temperature',
                                                           u'VolumetricFlow',
                                                           u'MassFlow',
                                                           u'Power',
                                                           u'Distance',
                                                           u'VolumetricFlowPerPower'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'input unit type for z',
                                      {'name': u'Input Unit Type for z',
                                       'pyname': u'input_unit_type_for_z',
                                       'default': u'Dimensionless',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'Dimensionless',
                                                           u'Temperature',
                                                           u'VolumetricFlow',
                                                           u'MassFlow',
                                                           u'Power',
                                                           u'Distance',
                                                           u'VolumetricFlowPerPower'],
                                       'autocalculatable': False,
                                       'type': 'alpha'})]),
              'extensible-fields': OrderedDict(),
              'unique-object': False,
              'required-object': False,
              'group': u'Performance Curves'}

    @property
    def name(self):
        """Get name.

        Returns:
            str: the value of `name` or None if not set

        """
        return self["Name"]

    @name.setter
    def name(self, value=None):
        """Corresponds to IDD field `Name`

        Args:
            value (str): value for IDD Field `Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Name"] = value

    @property
    def coefficient1_constant(self):
        """Get coefficient1_constant.

        Returns:
            float: the value of `coefficient1_constant` or None if not set

        """
        return self["Coefficient1 Constant"]

    @coefficient1_constant.setter
    def coefficient1_constant(self, value=None):
        """Corresponds to IDD field `Coefficient1 Constant`

        Args:
            value (float): value for IDD Field `Coefficient1 Constant`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient1 Constant"] = value

    @property
    def coefficient2_w(self):
        """Get coefficient2_w.

        Returns:
            float: the value of `coefficient2_w` or None if not set

        """
        return self["Coefficient2 w"]

    @coefficient2_w.setter
    def coefficient2_w(self, value=None):
        """Corresponds to IDD field `Coefficient2 w`

        Args:
            value (float): value for IDD Field `Coefficient2 w`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient2 w"] = value

    @property
    def coefficient3_x(self):
        """Get coefficient3_x.

        Returns:
            float: the value of `coefficient3_x` or None if not set

        """
        return self["Coefficient3 x"]

    @coefficient3_x.setter
    def coefficient3_x(self, value=None):
        """Corresponds to IDD field `Coefficient3 x`

        Args:
            value (float): value for IDD Field `Coefficient3 x`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient3 x"] = value

    @property
    def coefficient4_y(self):
        """Get coefficient4_y.

        Returns:
            float: the value of `coefficient4_y` or None if not set

        """
        return self["Coefficient4 y"]

    @coefficient4_y.setter
    def coefficient4_y(self, value=None):
        """Corresponds to IDD field `Coefficient4 y`

        Args:
            value (float): value for IDD Field `Coefficient4 y`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient4 y"] = value

    @property
    def coefficient5_z(self):
        """Get coefficient5_z.

        Returns:
            float: the value of `coefficient5_z` or None if not set

        """
        return self["Coefficient5 z"]

    @coefficient5_z.setter
    def coefficient5_z(self, value=None):
        """Corresponds to IDD field `Coefficient5 z`

        Args:
            value (float): value for IDD Field `Coefficient5 z`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient5 z"] = value

    @property
    def minimum_value_of_w(self):
        """Get minimum_value_of_w.

        Returns:
            float: the value of `minimum_value_of_w` or None if not set

        """
        return self["Minimum Value of w"]

    @minimum_value_of_w.setter
    def minimum_value_of_w(self, value=None):
        """Corresponds to IDD field `Minimum Value of w`

        Args:
            value (float): value for IDD Field `Minimum Value of w`
                Units are based on field `A2`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Minimum Value of w"] = value

    @property
    def maximum_value_of_w(self):
        """Get maximum_value_of_w.

        Returns:
            float: the value of `maximum_value_of_w` or None if not set

        """
        return self["Maximum Value of w"]

    @maximum_value_of_w.setter
    def maximum_value_of_w(self, value=None):
        """Corresponds to IDD field `Maximum Value of w`

        Args:
            value (float): value for IDD Field `Maximum Value of w`
                Units are based on field `A2`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Maximum Value of w"] = value

    @property
    def minimum_value_of_x(self):
        """Get minimum_value_of_x.

        Returns:
            float: the value of `minimum_value_of_x` or None if not set

        """
        return self["Minimum Value of x"]

    @minimum_value_of_x.setter
    def minimum_value_of_x(self, value=None):
        """Corresponds to IDD field `Minimum Value of x`

        Args:
            value (float): value for IDD Field `Minimum Value of x`
                Units are based on field `A3`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Minimum Value of x"] = value

    @property
    def maximum_value_of_x(self):
        """Get maximum_value_of_x.

        Returns:
            float: the value of `maximum_value_of_x` or None if not set

        """
        return self["Maximum Value of x"]

    @maximum_value_of_x.setter
    def maximum_value_of_x(self, value=None):
        """Corresponds to IDD field `Maximum Value of x`

        Args:
            value (float): value for IDD Field `Maximum Value of x`
                Units are based on field `A3`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Maximum Value of x"] = value

    @property
    def minimum_value_of_y(self):
        """Get minimum_value_of_y.

        Returns:
            float: the value of `minimum_value_of_y` or None if not set

        """
        return self["Minimum Value of y"]

    @minimum_value_of_y.setter
    def minimum_value_of_y(self, value=None):
        """Corresponds to IDD field `Minimum Value of y`

        Args:
            value (float): value for IDD Field `Minimum Value of y`
                Units are based on field `A4`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Minimum Value of y"] = value

    @property
    def maximum_value_of_y(self):
        """Get maximum_value_of_y.

        Returns:
            float: the value of `maximum_value_of_y` or None if not set

        """
        return self["Maximum Value of y"]

    @maximum_value_of_y.setter
    def maximum_value_of_y(self, value=None):
        """Corresponds to IDD field `Maximum Value of y`

        Args:
            value (float): value for IDD Field `Maximum Value of y`
                Units are based on field `A4`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Maximum Value of y"] = value

    @property
    def minimum_value_of_z(self):
        """Get minimum_value_of_z.

        Returns:
            float: the value of `minimum_value_of_z` or None if not set

        """
        return self["Minimum Value of z"]

    @minimum_value_of_z.setter
    def minimum_value_of_z(self, value=None):
        """Corresponds to IDD field `Minimum Value of z`

        Args:
            value (float): value for IDD Field `Minimum Value of z`
                Units are based on field `A5`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Minimum Value of z"] = value

    @property
    def maximum_value_of_z(self):
        """Get maximum_value_of_z.

        Returns:
            float: the value of `maximum_value_of_z` or None if not set

        """
        return self["Maximum Value of z"]

    @maximum_value_of_z.setter
    def maximum_value_of_z(self, value=None):
        """Corresponds to IDD field `Maximum Value of z`

        Args:
            value (float): value for IDD Field `Maximum Value of z`
                Units are based on field `A5`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Maximum Value of z"] = value

    @property
    def minimum_curve_output(self):
        """Get minimum_curve_output.

        Returns:
            float: the value of `minimum_curve_output` or None if not set

        """
        return self["Minimum Curve Output"]

    @minimum_curve_output.setter
    def minimum_curve_output(self, value=None):
        """Corresponds to IDD field `Minimum Curve Output` Specify the minimum
        value calculated by this curve object.

        Args:
            value (float): value for IDD Field `Minimum Curve Output`
                Units are based on field `A4`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Minimum Curve Output"] = value

    @property
    def maximum_curve_output(self):
        """Get maximum_curve_output.

        Returns:
            float: the value of `maximum_curve_output` or None if not set

        """
        return self["Maximum Curve Output"]

    @maximum_curve_output.setter
    def maximum_curve_output(self, value=None):
        """Corresponds to IDD field `Maximum Curve Output` Specify the maximum
        value calculated by this curve object.

        Args:
            value (float): value for IDD Field `Maximum Curve Output`
                Units are based on field `A4`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Maximum Curve Output"] = value

    @property
    def input_unit_type_for_w(self):
        """Get input_unit_type_for_w.

        Returns:
            str: the value of `input_unit_type_for_w` or None if not set

        """
        return self["Input Unit Type for w"]

    @input_unit_type_for_w.setter
    def input_unit_type_for_w(self, value="Dimensionless"):
        """Corresponds to IDD field `Input Unit Type for w`

        Args:
            value (str): value for IDD Field `Input Unit Type for w`
                Default value: Dimensionless
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Input Unit Type for w"] = value

    @property
    def input_unit_type_for_x(self):
        """Get input_unit_type_for_x.

        Returns:
            str: the value of `input_unit_type_for_x` or None if not set

        """
        return self["Input Unit Type for x"]

    @input_unit_type_for_x.setter
    def input_unit_type_for_x(self, value="Dimensionless"):
        """Corresponds to IDD field `Input Unit Type for x`

        Args:
            value (str): value for IDD Field `Input Unit Type for x`
                Default value: Dimensionless
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Input Unit Type for x"] = value

    @property
    def input_unit_type_for_y(self):
        """Get input_unit_type_for_y.

        Returns:
            str: the value of `input_unit_type_for_y` or None if not set

        """
        return self["Input Unit Type for y"]

    @input_unit_type_for_y.setter
    def input_unit_type_for_y(self, value="Dimensionless"):
        """Corresponds to IDD field `Input Unit Type for y`

        Args:
            value (str): value for IDD Field `Input Unit Type for y`
                Default value: Dimensionless
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Input Unit Type for y"] = value

    @property
    def input_unit_type_for_z(self):
        """Get input_unit_type_for_z.

        Returns:
            str: the value of `input_unit_type_for_z` or None if not set

        """
        return self["Input Unit Type for z"]

    @input_unit_type_for_z.setter
    def input_unit_type_for_z(self, value="Dimensionless"):
        """Corresponds to IDD field `Input Unit Type for z`

        Args:
            value (str): value for IDD Field `Input Unit Type for z`
                Default value: Dimensionless
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Input Unit Type for z"] = value




class CurveQuadratic(DataObject):

    """ Corresponds to IDD object `Curve:Quadratic`
        Quadratic curve with one independent variable.
        Input for a quadratic curve consists of the curve name, the three coefficients, and
        the maximum and minimum valid independent variable values. Optional inputs for curve
        minimum and maximum may be used to limit the output of the performance curve.
        curve = C1 + C2*x + C3*x**2
    """
    schema = {'min-fields': 0,
              'name': u'Curve:Quadratic',
              'pyname': u'CurveQuadratic',
              'format': None,
              'fields': OrderedDict([(u'name',
                                      {'name': u'Name',
                                       'pyname': u'name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'alpha'}),
                                     (u'coefficient1 constant',
                                      {'name': u'Coefficient1 Constant',
                                       'pyname': u'coefficient1_constant',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient2 x',
                                      {'name': u'Coefficient2 x',
                                       'pyname': u'coefficient2_x',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient3 x**2',
                                      {'name': u'Coefficient3 x**2',
                                       'pyname': u'coefficient3_x2',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'minimum value of x',
                                      {'name': u'Minimum Value of x',
                                       'pyname': u'minimum_value_of_x',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'maximum value of x',
                                      {'name': u'Maximum Value of x',
                                       'pyname': u'maximum_value_of_x',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'minimum curve output',
                                      {'name': u'Minimum Curve Output',
                                       'pyname': u'minimum_curve_output',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'maximum curve output',
                                      {'name': u'Maximum Curve Output',
                                       'pyname': u'maximum_curve_output',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'input unit type for x',
                                      {'name': u'Input Unit Type for X',
                                       'pyname': u'input_unit_type_for_x',
                                       'default': u'Dimensionless',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'Dimensionless',
                                                           u'Temperature',
                                                           u'VolumetricFlow',
                                                           u'MassFlow',
                                                           u'Power',
                                                           u'Distance'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'output unit type',
                                      {'name': u'Output Unit Type',
                                       'pyname': u'output_unit_type',
                                       'default': u'Dimensionless',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'Dimensionless',
                                                           u'Capacity',
                                                           u'Power'],
                                       'autocalculatable': False,
                                       'type': 'alpha'})]),
              'extensible-fields': OrderedDict(),
              'unique-object': False,
              'required-object': False,
              'group': u'Performance Curves'}

    @property
    def name(self):
        """Get name.

        Returns:
            str: the value of `name` or None if not set

        """
        return self["Name"]

    @name.setter
    def name(self, value=None):
        """Corresponds to IDD field `Name`

        Args:
            value (str): value for IDD Field `Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Name"] = value

    @property
    def coefficient1_constant(self):
        """Get coefficient1_constant.

        Returns:
            float: the value of `coefficient1_constant` or None if not set

        """
        return self["Coefficient1 Constant"]

    @coefficient1_constant.setter
    def coefficient1_constant(self, value=None):
        """Corresponds to IDD field `Coefficient1 Constant`

        Args:
            value (float): value for IDD Field `Coefficient1 Constant`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient1 Constant"] = value

    @property
    def coefficient2_x(self):
        """Get coefficient2_x.

        Returns:
            float: the value of `coefficient2_x` or None if not set

        """
        return self["Coefficient2 x"]

    @coefficient2_x.setter
    def coefficient2_x(self, value=None):
        """Corresponds to IDD field `Coefficient2 x`

        Args:
            value (float): value for IDD Field `Coefficient2 x`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient2 x"] = value

    @property
    def coefficient3_x2(self):
        """Get coefficient3_x2.

        Returns:
            float: the value of `coefficient3_x2` or None if not set

        """
        return self["Coefficient3 x**2"]

    @coefficient3_x2.setter
    def coefficient3_x2(self, value=None):
        """  Corresponds to IDD field `Coefficient3 x**2`

        Args:
            value (float): value for IDD Field `Coefficient3 x**2`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Coefficient3 x**2"] = value

    @property
    def minimum_value_of_x(self):
        """Get minimum_value_of_x.

        Returns:
            float: the value of `minimum_value_of_x` or None if not set

        """
        return self["Minimum Value of x"]

    @minimum_value_of_x.setter
    def minimum_value_of_x(self, value=None):
        """Corresponds to IDD field `Minimum Value of x`

        Args:
            value (float): value for IDD Field `Minimum Value of x`
                Units are based on field `A2`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Minimum Value of x"] = value

    @property
    def maximum_value_of_x(self):
        """Get maximum_value_of_x.

        Returns:
            float: the value of `maximum_value_of_x` or None if not set

        """
        return self["Maximum Value of x"]

    @maximum_value_of_x.setter
    def maximum_value_of_x(self, value=None):
        """Corresponds to IDD field `Maximum Value of x`

        Args:
            value (float): value for IDD Field `Maximum Value of x`
                Units are based on field `A2`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Maximum Value of x"] = value

    @property
    def minimum_curve_output(self):
        """Get minimum_curve_output.

        Returns:
            float: the value of `minimum_curve_output` or None if not set

        """
        return self["Minimum Curve Output"]

    @minimum_curve_output.setter
    def minimum_curve_output(self, value=None):
        """Corresponds to IDD field `Minimum Curve Output` Specify the minimum
        value calculated by this curve object.

        Args:
            value (float): value for IDD Field `Minimum Curve Output`
                Units are based on field `A3`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Minimum Curve Output"] = value

    @property
    def maximum_curve_output(self):
        """Get maximum_curve_output.

        Returns:
            float: the value of `maximum_curve_output` or None if not set

        """
        return self["Maximum Curve Output"]

    @maximum_curve_output.setter
    def maximum_curve_output(self, value=None):
        """Corresponds to IDD field `Maximum Curve Output` Specify the maximum
        value calculated by this curve object.

        Args:
            value (float): value for IDD Field `Maximum Curve Output`
                Units are based on field `A3`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Maximum Curve Output"] = value

    @property
    def input_unit_type_for_x(self):
        """Get input_unit_type_for_x.

        Returns:
            str: the value of `input_unit_type_for_x` or None if not set

        """
        return self["Input Unit Type for X"]

    @input_unit_type_for_x.setter
    def input_unit_type_for_x(self, value="Dimensionless"):
        """Corresponds to IDD field `Input Unit Type for X`

        Args:
            value (str): value for IDD Field `Input Unit Type for X`
                Default value: Dimensionless
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Input Unit Type for X"] = value

    @property
    def output_unit_type(self):
        """Get output_unit_type.

        Returns:
            str: the value of `output_unit_type` or None if not set

        """
        return self["Output Unit Type"]

    @output_unit_type.setter
    def output_unit_type(self, value="Dimensionless"):
        """Corresponds to IDD field `Output Unit Type`

        Args:
            value (str): value for IDD Field `Output Unit Type`
                Default value: Dimensionless
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Output Unit Type"] = value




class CurveCubic(DataObject):

    """ Corresponds to IDD object `Curve:Cubic`
        Cubic curve with one independent variable.
        Input for a cubic curve consists of the curve name, the 4 coefficients, and the
        maximum and minimum valid independent variable values. Optional inputs for curve
        minimum and maximum may be used to limit the output of the performance curve.
        curve = C1 + C2*x + C3*x**2 + C4*x**3
    """
    schema = {'min-fields': 0,
              'name': u'Curve:Cubic',
              'pyname': u'CurveCubic',
              'format': None,
              'fields': OrderedDict([(u'name',
                                      {'name': u'Name',
                                       'pyname': u'name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'alpha'}),
                                     (u'coefficient1 constant',
                                      {'name': u'Coefficient1 Constant',
                                       'pyname': u'coefficient1_constant',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient2 x',
                                      {'name': u'Coefficient2 x',
                                       'pyname': u'coefficient2_x',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient3 x**2',
                                      {'name': u'Coefficient3 x**2',
                                       'pyname': u'coefficient3_x2',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient4 x**3',
                                      {'name': u'Coefficient4 x**3',
                                       'pyname': u'coefficient4_x3',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'minimum value of x',
                                      {'name': u'Minimum Value of x',
                                       'pyname': u'minimum_value_of_x',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'maximum value of x',
                                      {'name': u'Maximum Value of x',
                                       'pyname': u'maximum_value_of_x',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'minimum curve output',
                                      {'name': u'Minimum Curve Output',
                                       'pyname': u'minimum_curve_output',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'maximum curve output',
                                      {'name': u'Maximum Curve Output',
                                       'pyname': u'maximum_curve_output',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'input unit type for x',
                                      {'name': u'Input Unit Type for X',
                                       'pyname': u'input_unit_type_for_x',
                                       'default': u'Dimensionless',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'Dimensionless',
                                                           u'Temperature',
                                                           u'VolumetricFlow',
                                                           u'MassFlow',
                                                           u'Power',
                                                           u'Distance'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'output unit type',
                                      {'name': u'Output Unit Type',
                                       'pyname': u'output_unit_type',
                                       'default': u'Dimensionless',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'Dimensionless',
                                                           u'Capacity',
                                                           u'Power'],
                                       'autocalculatable': False,
                                       'type': 'alpha'})]),
              'extensible-fields': OrderedDict(),
              'unique-object': False,
              'required-object': False,
              'group': u'Performance Curves'}

    @property
    def name(self):
        """Get name.

        Returns:
            str: the value of `name` or None if not set

        """
        return self["Name"]

    @name.setter
    def name(self, value=None):
        """Corresponds to IDD field `Name`

        Args:
            value (str): value for IDD Field `Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Name"] = value

    @property
    def coefficient1_constant(self):
        """Get coefficient1_constant.

        Returns:
            float: the value of `coefficient1_constant` or None if not set

        """
        return self["Coefficient1 Constant"]

    @coefficient1_constant.setter
    def coefficient1_constant(self, value=None):
        """Corresponds to IDD field `Coefficient1 Constant`

        Args:
            value (float): value for IDD Field `Coefficient1 Constant`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient1 Constant"] = value

    @property
    def coefficient2_x(self):
        """Get coefficient2_x.

        Returns:
            float: the value of `coefficient2_x` or None if not set

        """
        return self["Coefficient2 x"]

    @coefficient2_x.setter
    def coefficient2_x(self, value=None):
        """Corresponds to IDD field `Coefficient2 x`

        Args:
            value (float): value for IDD Field `Coefficient2 x`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient2 x"] = value

    @property
    def coefficient3_x2(self):
        """Get coefficient3_x2.

        Returns:
            float: the value of `coefficient3_x2` or None if not set

        """
        return self["Coefficient3 x**2"]

    @coefficient3_x2.setter
    def coefficient3_x2(self, value=None):
        """  Corresponds to IDD field `Coefficient3 x**2`

        Args:
            value (float): value for IDD Field `Coefficient3 x**2`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Coefficient3 x**2"] = value

    @property
    def coefficient4_x3(self):
        """Get coefficient4_x3.

        Returns:
            float: the value of `coefficient4_x3` or None if not set

        """
        return self["Coefficient4 x**3"]

    @coefficient4_x3.setter
    def coefficient4_x3(self, value=None):
        """  Corresponds to IDD field `Coefficient4 x**3`

        Args:
            value (float): value for IDD Field `Coefficient4 x**3`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Coefficient4 x**3"] = value

    @property
    def minimum_value_of_x(self):
        """Get minimum_value_of_x.

        Returns:
            float: the value of `minimum_value_of_x` or None if not set

        """
        return self["Minimum Value of x"]

    @minimum_value_of_x.setter
    def minimum_value_of_x(self, value=None):
        """Corresponds to IDD field `Minimum Value of x`

        Args:
            value (float): value for IDD Field `Minimum Value of x`
                Units are based on field `A2`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Minimum Value of x"] = value

    @property
    def maximum_value_of_x(self):
        """Get maximum_value_of_x.

        Returns:
            float: the value of `maximum_value_of_x` or None if not set

        """
        return self["Maximum Value of x"]

    @maximum_value_of_x.setter
    def maximum_value_of_x(self, value=None):
        """Corresponds to IDD field `Maximum Value of x`

        Args:
            value (float): value for IDD Field `Maximum Value of x`
                Units are based on field `A2`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Maximum Value of x"] = value

    @property
    def minimum_curve_output(self):
        """Get minimum_curve_output.

        Returns:
            float: the value of `minimum_curve_output` or None if not set

        """
        return self["Minimum Curve Output"]

    @minimum_curve_output.setter
    def minimum_curve_output(self, value=None):
        """Corresponds to IDD field `Minimum Curve Output` Specify the minimum
        value calculated by this curve object.

        Args:
            value (float): value for IDD Field `Minimum Curve Output`
                Units are based on field `A3`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Minimum Curve Output"] = value

    @property
    def maximum_curve_output(self):
        """Get maximum_curve_output.

        Returns:
            float: the value of `maximum_curve_output` or None if not set

        """
        return self["Maximum Curve Output"]

    @maximum_curve_output.setter
    def maximum_curve_output(self, value=None):
        """Corresponds to IDD field `Maximum Curve Output` Specify the maximum
        value calculated by this curve object.

        Args:
            value (float): value for IDD Field `Maximum Curve Output`
                Units are based on field `A3`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Maximum Curve Output"] = value

    @property
    def input_unit_type_for_x(self):
        """Get input_unit_type_for_x.

        Returns:
            str: the value of `input_unit_type_for_x` or None if not set

        """
        return self["Input Unit Type for X"]

    @input_unit_type_for_x.setter
    def input_unit_type_for_x(self, value="Dimensionless"):
        """Corresponds to IDD field `Input Unit Type for X`

        Args:
            value (str): value for IDD Field `Input Unit Type for X`
                Default value: Dimensionless
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Input Unit Type for X"] = value

    @property
    def output_unit_type(self):
        """Get output_unit_type.

        Returns:
            str: the value of `output_unit_type` or None if not set

        """
        return self["Output Unit Type"]

    @output_unit_type.setter
    def output_unit_type(self, value="Dimensionless"):
        """Corresponds to IDD field `Output Unit Type`

        Args:
            value (str): value for IDD Field `Output Unit Type`
                Default value: Dimensionless
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Output Unit Type"] = value




class CurveQuartic(DataObject):

    """ Corresponds to IDD object `Curve:Quartic`
        Quartic (fourth order polynomial) curve with one independent variable.
        Input for a Quartic curve consists of the curve name, the
        five coefficients, and the maximum and minimum valid independent variable values.
        Optional inputs for curve minimum and maximum may be used to limit the
        output of the performance curve.
        curve = C1 + C2*x + C3*x**2 + C4*x**3 + C5*x**4
    """
    schema = {'min-fields': 0,
              'name': u'Curve:Quartic',
              'pyname': u'CurveQuartic',
              'format': None,
              'fields': OrderedDict([(u'name',
                                      {'name': u'Name',
                                       'pyname': u'name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'alpha'}),
                                     (u'coefficient1 constant',
                                      {'name': u'Coefficient1 Constant',
                                       'pyname': u'coefficient1_constant',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient2 x',
                                      {'name': u'Coefficient2 x',
                                       'pyname': u'coefficient2_x',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient3 x**2',
                                      {'name': u'Coefficient3 x**2',
                                       'pyname': u'coefficient3_x2',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient4 x**3',
                                      {'name': u'Coefficient4 x**3',
                                       'pyname': u'coefficient4_x3',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient5 x**4',
                                      {'name': u'Coefficient5 x**4',
                                       'pyname': u'coefficient5_x4',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'minimum value of x',
                                      {'name': u'Minimum Value of x',
                                       'pyname': u'minimum_value_of_x',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'maximum value of x',
                                      {'name': u'Maximum Value of x',
                                       'pyname': u'maximum_value_of_x',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'minimum curve output',
                                      {'name': u'Minimum Curve Output',
                                       'pyname': u'minimum_curve_output',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'maximum curve output',
                                      {'name': u'Maximum Curve Output',
                                       'pyname': u'maximum_curve_output',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'input unit type for x',
                                      {'name': u'Input Unit Type for X',
                                       'pyname': u'input_unit_type_for_x',
                                       'default': u'Dimensionless',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'Dimensionless',
                                                           u'Temperature',
                                                           u'VolumetricFlow',
                                                           u'MassFlow',
                                                           u'Power',
                                                           u'Distance'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'output unit type',
                                      {'name': u'Output Unit Type',
                                       'pyname': u'output_unit_type',
                                       'default': u'Dimensionless',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'Dimensionless',
                                                           u'Capacity',
                                                           u'Power'],
                                       'autocalculatable': False,
                                       'type': 'alpha'})]),
              'extensible-fields': OrderedDict(),
              'unique-object': False,
              'required-object': False,
              'group': u'Performance Curves'}

    @property
    def name(self):
        """Get name.

        Returns:
            str: the value of `name` or None if not set

        """
        return self["Name"]

    @name.setter
    def name(self, value=None):
        """Corresponds to IDD field `Name`

        Args:
            value (str): value for IDD Field `Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Name"] = value

    @property
    def coefficient1_constant(self):
        """Get coefficient1_constant.

        Returns:
            float: the value of `coefficient1_constant` or None if not set

        """
        return self["Coefficient1 Constant"]

    @coefficient1_constant.setter
    def coefficient1_constant(self, value=None):
        """Corresponds to IDD field `Coefficient1 Constant`

        Args:
            value (float): value for IDD Field `Coefficient1 Constant`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient1 Constant"] = value

    @property
    def coefficient2_x(self):
        """Get coefficient2_x.

        Returns:
            float: the value of `coefficient2_x` or None if not set

        """
        return self["Coefficient2 x"]

    @coefficient2_x.setter
    def coefficient2_x(self, value=None):
        """Corresponds to IDD field `Coefficient2 x`

        Args:
            value (float): value for IDD Field `Coefficient2 x`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient2 x"] = value

    @property
    def coefficient3_x2(self):
        """Get coefficient3_x2.

        Returns:
            float: the value of `coefficient3_x2` or None if not set

        """
        return self["Coefficient3 x**2"]

    @coefficient3_x2.setter
    def coefficient3_x2(self, value=None):
        """  Corresponds to IDD field `Coefficient3 x**2`

        Args:
            value (float): value for IDD Field `Coefficient3 x**2`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Coefficient3 x**2"] = value

    @property
    def coefficient4_x3(self):
        """Get coefficient4_x3.

        Returns:
            float: the value of `coefficient4_x3` or None if not set

        """
        return self["Coefficient4 x**3"]

    @coefficient4_x3.setter
    def coefficient4_x3(self, value=None):
        """  Corresponds to IDD field `Coefficient4 x**3`

        Args:
            value (float): value for IDD Field `Coefficient4 x**3`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Coefficient4 x**3"] = value

    @property
    def coefficient5_x4(self):
        """Get coefficient5_x4.

        Returns:
            float: the value of `coefficient5_x4` or None if not set

        """
        return self["Coefficient5 x**4"]

    @coefficient5_x4.setter
    def coefficient5_x4(self, value=None):
        """  Corresponds to IDD field `Coefficient5 x**4`

        Args:
            value (float): value for IDD Field `Coefficient5 x**4`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Coefficient5 x**4"] = value

    @property
    def minimum_value_of_x(self):
        """Get minimum_value_of_x.

        Returns:
            float: the value of `minimum_value_of_x` or None if not set

        """
        return self["Minimum Value of x"]

    @minimum_value_of_x.setter
    def minimum_value_of_x(self, value=None):
        """Corresponds to IDD field `Minimum Value of x`

        Args:
            value (float): value for IDD Field `Minimum Value of x`
                Units are based on field `A2`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Minimum Value of x"] = value

    @property
    def maximum_value_of_x(self):
        """Get maximum_value_of_x.

        Returns:
            float: the value of `maximum_value_of_x` or None if not set

        """
        return self["Maximum Value of x"]

    @maximum_value_of_x.setter
    def maximum_value_of_x(self, value=None):
        """Corresponds to IDD field `Maximum Value of x`

        Args:
            value (float): value for IDD Field `Maximum Value of x`
                Units are based on field `A2`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Maximum Value of x"] = value

    @property
    def minimum_curve_output(self):
        """Get minimum_curve_output.

        Returns:
            float: the value of `minimum_curve_output` or None if not set

        """
        return self["Minimum Curve Output"]

    @minimum_curve_output.setter
    def minimum_curve_output(self, value=None):
        """Corresponds to IDD field `Minimum Curve Output` Specify the minimum
        value calculated by this curve object.

        Args:
            value (float): value for IDD Field `Minimum Curve Output`
                Units are based on field `A3`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Minimum Curve Output"] = value

    @property
    def maximum_curve_output(self):
        """Get maximum_curve_output.

        Returns:
            float: the value of `maximum_curve_output` or None if not set

        """
        return self["Maximum Curve Output"]

    @maximum_curve_output.setter
    def maximum_curve_output(self, value=None):
        """Corresponds to IDD field `Maximum Curve Output` Specify the maximum
        value calculated by this curve object.

        Args:
            value (float): value for IDD Field `Maximum Curve Output`
                Units are based on field `A3`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Maximum Curve Output"] = value

    @property
    def input_unit_type_for_x(self):
        """Get input_unit_type_for_x.

        Returns:
            str: the value of `input_unit_type_for_x` or None if not set

        """
        return self["Input Unit Type for X"]

    @input_unit_type_for_x.setter
    def input_unit_type_for_x(self, value="Dimensionless"):
        """Corresponds to IDD field `Input Unit Type for X`

        Args:
            value (str): value for IDD Field `Input Unit Type for X`
                Default value: Dimensionless
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Input Unit Type for X"] = value

    @property
    def output_unit_type(self):
        """Get output_unit_type.

        Returns:
            str: the value of `output_unit_type` or None if not set

        """
        return self["Output Unit Type"]

    @output_unit_type.setter
    def output_unit_type(self, value="Dimensionless"):
        """Corresponds to IDD field `Output Unit Type`

        Args:
            value (str): value for IDD Field `Output Unit Type`
                Default value: Dimensionless
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Output Unit Type"] = value




class CurveExponent(DataObject):

    """ Corresponds to IDD object `Curve:Exponent`
        Exponent curve with one independent variable.
        Input for a exponent curve consists of the curve name, the 3 coefficients, and the
        maximum and minimum valid independent variable values. Optional inputs for curve
        minimum and maximum may be used to limit the output of the performance curve.
        curve = C1 + C2*x**C3
        The independent variable x is raised to the C3 power, multiplied by C2, and C1 is added to the result.
    """
    schema = {'min-fields': 6,
              'name': u'Curve:Exponent',
              'pyname': u'CurveExponent',
              'format': None,
              'fields': OrderedDict([(u'name',
                                      {'name': u'Name',
                                       'pyname': u'name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'alpha'}),
                                     (u'coefficient1 constant',
                                      {'name': u'Coefficient1 Constant',
                                       'pyname': u'coefficient1_constant',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient2 constant',
                                      {'name': u'Coefficient2 Constant',
                                       'pyname': u'coefficient2_constant',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient3 constant',
                                      {'name': u'Coefficient3 Constant',
                                       'pyname': u'coefficient3_constant',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'minimum value of x',
                                      {'name': u'Minimum Value of x',
                                       'pyname': u'minimum_value_of_x',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'maximum value of x',
                                      {'name': u'Maximum Value of x',
                                       'pyname': u'maximum_value_of_x',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'minimum curve output',
                                      {'name': u'Minimum Curve Output',
                                       'pyname': u'minimum_curve_output',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'maximum curve output',
                                      {'name': u'Maximum Curve Output',
                                       'pyname': u'maximum_curve_output',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'input unit type for x',
                                      {'name': u'Input Unit Type for X',
                                       'pyname': u'input_unit_type_for_x',
                                       'default': u'Dimensionless',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'Dimensionless',
                                                           u'Temperature',
                                                           u'VolumetricFlow',
                                                           u'MassFlow',
                                                           u'Power',
                                                           u'Distance'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'output unit type',
                                      {'name': u'Output Unit Type',
                                       'pyname': u'output_unit_type',
                                       'default': u'Dimensionless',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'Dimensionless',
                                                           u'Capacity',
                                                           u'Power'],
                                       'autocalculatable': False,
                                       'type': 'alpha'})]),
              'extensible-fields': OrderedDict(),
              'unique-object': False,
              'required-object': False,
              'group': u'Performance Curves'}

    @property
    def name(self):
        """Get name.

        Returns:
            str: the value of `name` or None if not set

        """
        return self["Name"]

    @name.setter
    def name(self, value=None):
        """Corresponds to IDD field `Name`

        Args:
            value (str): value for IDD Field `Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Name"] = value

    @property
    def coefficient1_constant(self):
        """Get coefficient1_constant.

        Returns:
            float: the value of `coefficient1_constant` or None if not set

        """
        return self["Coefficient1 Constant"]

    @coefficient1_constant.setter
    def coefficient1_constant(self, value=None):
        """Corresponds to IDD field `Coefficient1 Constant`

        Args:
            value (float): value for IDD Field `Coefficient1 Constant`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient1 Constant"] = value

    @property
    def coefficient2_constant(self):
        """Get coefficient2_constant.

        Returns:
            float: the value of `coefficient2_constant` or None if not set

        """
        return self["Coefficient2 Constant"]

    @coefficient2_constant.setter
    def coefficient2_constant(self, value=None):
        """Corresponds to IDD field `Coefficient2 Constant`

        Args:
            value (float): value for IDD Field `Coefficient2 Constant`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient2 Constant"] = value

    @property
    def coefficient3_constant(self):
        """Get coefficient3_constant.

        Returns:
            float: the value of `coefficient3_constant` or None if not set

        """
        return self["Coefficient3 Constant"]

    @coefficient3_constant.setter
    def coefficient3_constant(self, value=None):
        """Corresponds to IDD field `Coefficient3 Constant`

        Args:
            value (float): value for IDD Field `Coefficient3 Constant`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient3 Constant"] = value

    @property
    def minimum_value_of_x(self):
        """Get minimum_value_of_x.

        Returns:
            float: the value of `minimum_value_of_x` or None if not set

        """
        return self["Minimum Value of x"]

    @minimum_value_of_x.setter
    def minimum_value_of_x(self, value=None):
        """Corresponds to IDD field `Minimum Value of x` Specify the minimum
        value of the independent variable x allowed.

        Args:
            value (float): value for IDD Field `Minimum Value of x`
                Units are based on field `A2`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Minimum Value of x"] = value

    @property
    def maximum_value_of_x(self):
        """Get maximum_value_of_x.

        Returns:
            float: the value of `maximum_value_of_x` or None if not set

        """
        return self["Maximum Value of x"]

    @maximum_value_of_x.setter
    def maximum_value_of_x(self, value=None):
        """Corresponds to IDD field `Maximum Value of x` Specify the maximum
        value of the independent variable x allowed.

        Args:
            value (float): value for IDD Field `Maximum Value of x`
                Units are based on field `A2`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Maximum Value of x"] = value

    @property
    def minimum_curve_output(self):
        """Get minimum_curve_output.

        Returns:
            float: the value of `minimum_curve_output` or None if not set

        """
        return self["Minimum Curve Output"]

    @minimum_curve_output.setter
    def minimum_curve_output(self, value=None):
        """Corresponds to IDD field `Minimum Curve Output` Specify the minimum
        value calculated by this curve object.

        Args:
            value (float): value for IDD Field `Minimum Curve Output`
                Units are based on field `A3`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Minimum Curve Output"] = value

    @property
    def maximum_curve_output(self):
        """Get maximum_curve_output.

        Returns:
            float: the value of `maximum_curve_output` or None if not set

        """
        return self["Maximum Curve Output"]

    @maximum_curve_output.setter
    def maximum_curve_output(self, value=None):
        """Corresponds to IDD field `Maximum Curve Output` Specify the maximum
        value calculated by this curve object.

        Args:
            value (float): value for IDD Field `Maximum Curve Output`
                Units are based on field `A3`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Maximum Curve Output"] = value

    @property
    def input_unit_type_for_x(self):
        """Get input_unit_type_for_x.

        Returns:
            str: the value of `input_unit_type_for_x` or None if not set

        """
        return self["Input Unit Type for X"]

    @input_unit_type_for_x.setter
    def input_unit_type_for_x(self, value="Dimensionless"):
        """Corresponds to IDD field `Input Unit Type for X`

        Args:
            value (str): value for IDD Field `Input Unit Type for X`
                Default value: Dimensionless
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Input Unit Type for X"] = value

    @property
    def output_unit_type(self):
        """Get output_unit_type.

        Returns:
            str: the value of `output_unit_type` or None if not set

        """
        return self["Output Unit Type"]

    @output_unit_type.setter
    def output_unit_type(self, value="Dimensionless"):
        """Corresponds to IDD field `Output Unit Type`

        Args:
            value (str): value for IDD Field `Output Unit Type`
                Default value: Dimensionless
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Output Unit Type"] = value




class CurveBicubic(DataObject):

    """ Corresponds to IDD object `Curve:Bicubic`
        Cubic curve with two independent variables. Input consists of the
        curve name, the ten coefficients, and the minimum and maximum values for each of
        the independent variables. Optional inputs for curve minimum and maximum may
        be used to limit the output of the performance curve.
        curve = C1 + C2*x + C3*x**2 + C4*y + C5*y**2 + C6*x*y + C7*x**3 + C8*y**3 + C9*x**2*y
        + C10*x*y**2
    """
    schema = {'min-fields': 0,
              'name': u'Curve:Bicubic',
              'pyname': u'CurveBicubic',
              'format': None,
              'fields': OrderedDict([(u'name',
                                      {'name': u'Name',
                                       'pyname': u'name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'alpha'}),
                                     (u'coefficient1 constant',
                                      {'name': u'Coefficient1 Constant',
                                       'pyname': u'coefficient1_constant',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient2 x',
                                      {'name': u'Coefficient2 x',
                                       'pyname': u'coefficient2_x',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient3 x**2',
                                      {'name': u'Coefficient3 x**2',
                                       'pyname': u'coefficient3_x2',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient4 y',
                                      {'name': u'Coefficient4 y',
                                       'pyname': u'coefficient4_y',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient5 y**2',
                                      {'name': u'Coefficient5 y**2',
                                       'pyname': u'coefficient5_y2',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient6 x*y',
                                      {'name': u'Coefficient6 x*y',
                                       'pyname': u'coefficient6_xy',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient7 x**3',
                                      {'name': u'Coefficient7 x**3',
                                       'pyname': u'coefficient7_x3',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient8 y**3',
                                      {'name': u'Coefficient8 y**3',
                                       'pyname': u'coefficient8_y3',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient9 x**2*y',
                                      {'name': u'Coefficient9 x**2*y',
                                       'pyname': u'coefficient9_x2y',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient10 x*y**2',
                                      {'name': u'Coefficient10 x*y**2',
                                       'pyname': u'coefficient10_xy2',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'minimum value of x',
                                      {'name': u'Minimum Value of x',
                                       'pyname': u'minimum_value_of_x',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'maximum value of x',
                                      {'name': u'Maximum Value of x',
                                       'pyname': u'maximum_value_of_x',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'minimum value of y',
                                      {'name': u'Minimum Value of y',
                                       'pyname': u'minimum_value_of_y',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'maximum value of y',
                                      {'name': u'Maximum Value of y',
                                       'pyname': u'maximum_value_of_y',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'minimum curve output',
                                      {'name': u'Minimum Curve Output',
                                       'pyname': u'minimum_curve_output',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'maximum curve output',
                                      {'name': u'Maximum Curve Output',
                                       'pyname': u'maximum_curve_output',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'input unit type for x',
                                      {'name': u'Input Unit Type for X',
                                       'pyname': u'input_unit_type_for_x',
                                       'default': u'Dimensionless',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'Dimensionless',
                                                           u'Temperature',
                                                           u'VolumetricFlow',
                                                           u'MassFlow',
                                                           u'Power',
                                                           u'Distance'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'input unit type for y',
                                      {'name': u'Input Unit Type for Y',
                                       'pyname': u'input_unit_type_for_y',
                                       'default': u'Dimensionless',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'Dimensionless',
                                                           u'Temperature',
                                                           u'VolumetricFlow',
                                                           u'MassFlow',
                                                           u'Power',
                                                           u'Distance'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'output unit type',
                                      {'name': u'Output Unit Type',
                                       'pyname': u'output_unit_type',
                                       'default': u'Dimensionless',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'Dimensionless',
                                                           u'Capacity',
                                                           u'Power'],
                                       'autocalculatable': False,
                                       'type': 'alpha'})]),
              'extensible-fields': OrderedDict(),
              'unique-object': False,
              'required-object': False,
              'group': u'Performance Curves'}

    @property
    def name(self):
        """Get name.

        Returns:
            str: the value of `name` or None if not set

        """
        return self["Name"]

    @name.setter
    def name(self, value=None):
        """Corresponds to IDD field `Name`

        Args:
            value (str): value for IDD Field `Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Name"] = value

    @property
    def coefficient1_constant(self):
        """Get coefficient1_constant.

        Returns:
            float: the value of `coefficient1_constant` or None if not set

        """
        return self["Coefficient1 Constant"]

    @coefficient1_constant.setter
    def coefficient1_constant(self, value=None):
        """Corresponds to IDD field `Coefficient1 Constant`

        Args:
            value (float): value for IDD Field `Coefficient1 Constant`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient1 Constant"] = value

    @property
    def coefficient2_x(self):
        """Get coefficient2_x.

        Returns:
            float: the value of `coefficient2_x` or None if not set

        """
        return self["Coefficient2 x"]

    @coefficient2_x.setter
    def coefficient2_x(self, value=None):
        """Corresponds to IDD field `Coefficient2 x`

        Args:
            value (float): value for IDD Field `Coefficient2 x`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient2 x"] = value

    @property
    def coefficient3_x2(self):
        """Get coefficient3_x2.

        Returns:
            float: the value of `coefficient3_x2` or None if not set

        """
        return self["Coefficient3 x**2"]

    @coefficient3_x2.setter
    def coefficient3_x2(self, value=None):
        """  Corresponds to IDD field `Coefficient3 x**2`

        Args:
            value (float): value for IDD Field `Coefficient3 x**2`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Coefficient3 x**2"] = value

    @property
    def coefficient4_y(self):
        """Get coefficient4_y.

        Returns:
            float: the value of `coefficient4_y` or None if not set

        """
        return self["Coefficient4 y"]

    @coefficient4_y.setter
    def coefficient4_y(self, value=None):
        """Corresponds to IDD field `Coefficient4 y`

        Args:
            value (float): value for IDD Field `Coefficient4 y`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient4 y"] = value

    @property
    def coefficient5_y2(self):
        """Get coefficient5_y2.

        Returns:
            float: the value of `coefficient5_y2` or None if not set

        """
        return self["Coefficient5 y**2"]

    @coefficient5_y2.setter
    def coefficient5_y2(self, value=None):
        """  Corresponds to IDD field `Coefficient5 y**2`

        Args:
            value (float): value for IDD Field `Coefficient5 y**2`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Coefficient5 y**2"] = value

    @property
    def coefficient6_xy(self):
        """Get coefficient6_xy.

        Returns:
            float: the value of `coefficient6_xy` or None if not set

        """
        return self["Coefficient6 x*y"]

    @coefficient6_xy.setter
    def coefficient6_xy(self, value=None):
        """  Corresponds to IDD field `Coefficient6 x*y`

        Args:
            value (float): value for IDD Field `Coefficient6 x*y`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Coefficient6 x*y"] = value

    @property
    def coefficient7_x3(self):
        """Get coefficient7_x3.

        Returns:
            float: the value of `coefficient7_x3` or None if not set

        """
        return self["Coefficient7 x**3"]

    @coefficient7_x3.setter
    def coefficient7_x3(self, value=None):
        """  Corresponds to IDD field `Coefficient7 x**3`

        Args:
            value (float): value for IDD Field `Coefficient7 x**3`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Coefficient7 x**3"] = value

    @property
    def coefficient8_y3(self):
        """Get coefficient8_y3.

        Returns:
            float: the value of `coefficient8_y3` or None if not set

        """
        return self["Coefficient8 y**3"]

    @coefficient8_y3.setter
    def coefficient8_y3(self, value=None):
        """  Corresponds to IDD field `Coefficient8 y**3`

        Args:
            value (float): value for IDD Field `Coefficient8 y**3`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Coefficient8 y**3"] = value

    @property
    def coefficient9_x2y(self):
        """Get coefficient9_x2y.

        Returns:
            float: the value of `coefficient9_x2y` or None if not set

        """
        return self["Coefficient9 x**2*y"]

    @coefficient9_x2y.setter
    def coefficient9_x2y(self, value=None):
        """  Corresponds to IDD field `Coefficient9 x**2*y`

        Args:
            value (float): value for IDD Field `Coefficient9 x**2*y`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Coefficient9 x**2*y"] = value

    @property
    def coefficient10_xy2(self):
        """Get coefficient10_xy2.

        Returns:
            float: the value of `coefficient10_xy2` or None if not set

        """
        return self["Coefficient10 x*y**2"]

    @coefficient10_xy2.setter
    def coefficient10_xy2(self, value=None):
        """  Corresponds to IDD field `Coefficient10 x*y**2`

        Args:
            value (float): value for IDD Field `Coefficient10 x*y**2`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Coefficient10 x*y**2"] = value

    @property
    def minimum_value_of_x(self):
        """Get minimum_value_of_x.

        Returns:
            float: the value of `minimum_value_of_x` or None if not set

        """
        return self["Minimum Value of x"]

    @minimum_value_of_x.setter
    def minimum_value_of_x(self, value=None):
        """Corresponds to IDD field `Minimum Value of x`

        Args:
            value (float): value for IDD Field `Minimum Value of x`
                Units are based on field `A2`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Minimum Value of x"] = value

    @property
    def maximum_value_of_x(self):
        """Get maximum_value_of_x.

        Returns:
            float: the value of `maximum_value_of_x` or None if not set

        """
        return self["Maximum Value of x"]

    @maximum_value_of_x.setter
    def maximum_value_of_x(self, value=None):
        """Corresponds to IDD field `Maximum Value of x`

        Args:
            value (float): value for IDD Field `Maximum Value of x`
                Units are based on field `A2`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Maximum Value of x"] = value

    @property
    def minimum_value_of_y(self):
        """Get minimum_value_of_y.

        Returns:
            float: the value of `minimum_value_of_y` or None if not set

        """
        return self["Minimum Value of y"]

    @minimum_value_of_y.setter
    def minimum_value_of_y(self, value=None):
        """Corresponds to IDD field `Minimum Value of y`

        Args:
            value (float): value for IDD Field `Minimum Value of y`
                Units are based on field `A3`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Minimum Value of y"] = value

    @property
    def maximum_value_of_y(self):
        """Get maximum_value_of_y.

        Returns:
            float: the value of `maximum_value_of_y` or None if not set

        """
        return self["Maximum Value of y"]

    @maximum_value_of_y.setter
    def maximum_value_of_y(self, value=None):
        """Corresponds to IDD field `Maximum Value of y`

        Args:
            value (float): value for IDD Field `Maximum Value of y`
                Units are based on field `A3`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Maximum Value of y"] = value

    @property
    def minimum_curve_output(self):
        """Get minimum_curve_output.

        Returns:
            float: the value of `minimum_curve_output` or None if not set

        """
        return self["Minimum Curve Output"]

    @minimum_curve_output.setter
    def minimum_curve_output(self, value=None):
        """Corresponds to IDD field `Minimum Curve Output` Specify the minimum
        value calculated by this curve object.

        Args:
            value (float): value for IDD Field `Minimum Curve Output`
                Units are based on field `A4`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Minimum Curve Output"] = value

    @property
    def maximum_curve_output(self):
        """Get maximum_curve_output.

        Returns:
            float: the value of `maximum_curve_output` or None if not set

        """
        return self["Maximum Curve Output"]

    @maximum_curve_output.setter
    def maximum_curve_output(self, value=None):
        """Corresponds to IDD field `Maximum Curve Output` Specify the maximum
        value calculated by this curve object.

        Args:
            value (float): value for IDD Field `Maximum Curve Output`
                Units are based on field `A4`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Maximum Curve Output"] = value

    @property
    def input_unit_type_for_x(self):
        """Get input_unit_type_for_x.

        Returns:
            str: the value of `input_unit_type_for_x` or None if not set

        """
        return self["Input Unit Type for X"]

    @input_unit_type_for_x.setter
    def input_unit_type_for_x(self, value="Dimensionless"):
        """Corresponds to IDD field `Input Unit Type for X`

        Args:
            value (str): value for IDD Field `Input Unit Type for X`
                Default value: Dimensionless
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Input Unit Type for X"] = value

    @property
    def input_unit_type_for_y(self):
        """Get input_unit_type_for_y.

        Returns:
            str: the value of `input_unit_type_for_y` or None if not set

        """
        return self["Input Unit Type for Y"]

    @input_unit_type_for_y.setter
    def input_unit_type_for_y(self, value="Dimensionless"):
        """Corresponds to IDD field `Input Unit Type for Y`

        Args:
            value (str): value for IDD Field `Input Unit Type for Y`
                Default value: Dimensionless
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Input Unit Type for Y"] = value

    @property
    def output_unit_type(self):
        """Get output_unit_type.

        Returns:
            str: the value of `output_unit_type` or None if not set

        """
        return self["Output Unit Type"]

    @output_unit_type.setter
    def output_unit_type(self, value="Dimensionless"):
        """Corresponds to IDD field `Output Unit Type`

        Args:
            value (str): value for IDD Field `Output Unit Type`
                Default value: Dimensionless
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Output Unit Type"] = value




class CurveBiquadratic(DataObject):

    """ Corresponds to IDD object `Curve:Biquadratic`
        Quadratic curve with two independent variables. Input consists of the curve name, the
        six coefficients, and min and max values for each of the independent variables.
        Optional inputs for curve minimum and maximum may be used to limit the
        output of the performance curve.
        curve = C1 + C2*x + C3*x**2 + C4*y + C5*y**2 + C6*x*y
    """
    schema = {'min-fields': 0,
              'name': u'Curve:Biquadratic',
              'pyname': u'CurveBiquadratic',
              'format': None,
              'fields': OrderedDict([(u'name',
                                      {'name': u'Name',
                                       'pyname': u'name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'alpha'}),
                                     (u'coefficient1 constant',
                                      {'name': u'Coefficient1 Constant',
                                       'pyname': u'coefficient1_constant',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient2 x',
                                      {'name': u'Coefficient2 x',
                                       'pyname': u'coefficient2_x',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient3 x**2',
                                      {'name': u'Coefficient3 x**2',
                                       'pyname': u'coefficient3_x2',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient4 y',
                                      {'name': u'Coefficient4 y',
                                       'pyname': u'coefficient4_y',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient5 y**2',
                                      {'name': u'Coefficient5 y**2',
                                       'pyname': u'coefficient5_y2',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient6 x*y',
                                      {'name': u'Coefficient6 x*y',
                                       'pyname': u'coefficient6_xy',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'minimum value of x',
                                      {'name': u'Minimum Value of x',
                                       'pyname': u'minimum_value_of_x',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'maximum value of x',
                                      {'name': u'Maximum Value of x',
                                       'pyname': u'maximum_value_of_x',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'minimum value of y',
                                      {'name': u'Minimum Value of y',
                                       'pyname': u'minimum_value_of_y',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'maximum value of y',
                                      {'name': u'Maximum Value of y',
                                       'pyname': u'maximum_value_of_y',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'minimum curve output',
                                      {'name': u'Minimum Curve Output',
                                       'pyname': u'minimum_curve_output',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'maximum curve output',
                                      {'name': u'Maximum Curve Output',
                                       'pyname': u'maximum_curve_output',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'input unit type for x',
                                      {'name': u'Input Unit Type for X',
                                       'pyname': u'input_unit_type_for_x',
                                       'default': u'Dimensionless',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'Dimensionless',
                                                           u'Temperature',
                                                           u'VolumetricFlow',
                                                           u'MassFlow',
                                                           u'Power',
                                                           u'Distance'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'input unit type for y',
                                      {'name': u'Input Unit Type for Y',
                                       'pyname': u'input_unit_type_for_y',
                                       'default': u'Dimensionless',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'Dimensionless',
                                                           u'Temperature',
                                                           u'VolumetricFlow',
                                                           u'MassFlow',
                                                           u'Power',
                                                           u'Distance'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'output unit type',
                                      {'name': u'Output Unit Type',
                                       'pyname': u'output_unit_type',
                                       'default': u'Dimensionless',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'Dimensionless',
                                                           u'Capacity',
                                                           u'Power'],
                                       'autocalculatable': False,
                                       'type': 'alpha'})]),
              'extensible-fields': OrderedDict(),
              'unique-object': False,
              'required-object': False,
              'group': u'Performance Curves'}

    @property
    def name(self):
        """Get name.

        Returns:
            str: the value of `name` or None if not set

        """
        return self["Name"]

    @name.setter
    def name(self, value=None):
        """Corresponds to IDD field `Name`

        Args:
            value (str): value for IDD Field `Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Name"] = value

    @property
    def coefficient1_constant(self):
        """Get coefficient1_constant.

        Returns:
            float: the value of `coefficient1_constant` or None if not set

        """
        return self["Coefficient1 Constant"]

    @coefficient1_constant.setter
    def coefficient1_constant(self, value=None):
        """Corresponds to IDD field `Coefficient1 Constant`

        Args:
            value (float): value for IDD Field `Coefficient1 Constant`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient1 Constant"] = value

    @property
    def coefficient2_x(self):
        """Get coefficient2_x.

        Returns:
            float: the value of `coefficient2_x` or None if not set

        """
        return self["Coefficient2 x"]

    @coefficient2_x.setter
    def coefficient2_x(self, value=None):
        """Corresponds to IDD field `Coefficient2 x`

        Args:
            value (float): value for IDD Field `Coefficient2 x`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient2 x"] = value

    @property
    def coefficient3_x2(self):
        """Get coefficient3_x2.

        Returns:
            float: the value of `coefficient3_x2` or None if not set

        """
        return self["Coefficient3 x**2"]

    @coefficient3_x2.setter
    def coefficient3_x2(self, value=None):
        """  Corresponds to IDD field `Coefficient3 x**2`

        Args:
            value (float): value for IDD Field `Coefficient3 x**2`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Coefficient3 x**2"] = value

    @property
    def coefficient4_y(self):
        """Get coefficient4_y.

        Returns:
            float: the value of `coefficient4_y` or None if not set

        """
        return self["Coefficient4 y"]

    @coefficient4_y.setter
    def coefficient4_y(self, value=None):
        """Corresponds to IDD field `Coefficient4 y`

        Args:
            value (float): value for IDD Field `Coefficient4 y`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient4 y"] = value

    @property
    def coefficient5_y2(self):
        """Get coefficient5_y2.

        Returns:
            float: the value of `coefficient5_y2` or None if not set

        """
        return self["Coefficient5 y**2"]

    @coefficient5_y2.setter
    def coefficient5_y2(self, value=None):
        """  Corresponds to IDD field `Coefficient5 y**2`

        Args:
            value (float): value for IDD Field `Coefficient5 y**2`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Coefficient5 y**2"] = value

    @property
    def coefficient6_xy(self):
        """Get coefficient6_xy.

        Returns:
            float: the value of `coefficient6_xy` or None if not set

        """
        return self["Coefficient6 x*y"]

    @coefficient6_xy.setter
    def coefficient6_xy(self, value=None):
        """  Corresponds to IDD field `Coefficient6 x*y`

        Args:
            value (float): value for IDD Field `Coefficient6 x*y`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Coefficient6 x*y"] = value

    @property
    def minimum_value_of_x(self):
        """Get minimum_value_of_x.

        Returns:
            float: the value of `minimum_value_of_x` or None if not set

        """
        return self["Minimum Value of x"]

    @minimum_value_of_x.setter
    def minimum_value_of_x(self, value=None):
        """Corresponds to IDD field `Minimum Value of x`

        Args:
            value (float): value for IDD Field `Minimum Value of x`
                Units are based on field `A2`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Minimum Value of x"] = value

    @property
    def maximum_value_of_x(self):
        """Get maximum_value_of_x.

        Returns:
            float: the value of `maximum_value_of_x` or None if not set

        """
        return self["Maximum Value of x"]

    @maximum_value_of_x.setter
    def maximum_value_of_x(self, value=None):
        """Corresponds to IDD field `Maximum Value of x`

        Args:
            value (float): value for IDD Field `Maximum Value of x`
                Units are based on field `A2`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Maximum Value of x"] = value

    @property
    def minimum_value_of_y(self):
        """Get minimum_value_of_y.

        Returns:
            float: the value of `minimum_value_of_y` or None if not set

        """
        return self["Minimum Value of y"]

    @minimum_value_of_y.setter
    def minimum_value_of_y(self, value=None):
        """Corresponds to IDD field `Minimum Value of y`

        Args:
            value (float): value for IDD Field `Minimum Value of y`
                Units are based on field `A3`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Minimum Value of y"] = value

    @property
    def maximum_value_of_y(self):
        """Get maximum_value_of_y.

        Returns:
            float: the value of `maximum_value_of_y` or None if not set

        """
        return self["Maximum Value of y"]

    @maximum_value_of_y.setter
    def maximum_value_of_y(self, value=None):
        """Corresponds to IDD field `Maximum Value of y`

        Args:
            value (float): value for IDD Field `Maximum Value of y`
                Units are based on field `A3`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Maximum Value of y"] = value

    @property
    def minimum_curve_output(self):
        """Get minimum_curve_output.

        Returns:
            float: the value of `minimum_curve_output` or None if not set

        """
        return self["Minimum Curve Output"]

    @minimum_curve_output.setter
    def minimum_curve_output(self, value=None):
        """Corresponds to IDD field `Minimum Curve Output` Specify the minimum
        value calculated by this curve object.

        Args:
            value (float): value for IDD Field `Minimum Curve Output`
                Units are based on field `A4`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Minimum Curve Output"] = value

    @property
    def maximum_curve_output(self):
        """Get maximum_curve_output.

        Returns:
            float: the value of `maximum_curve_output` or None if not set

        """
        return self["Maximum Curve Output"]

    @maximum_curve_output.setter
    def maximum_curve_output(self, value=None):
        """Corresponds to IDD field `Maximum Curve Output` Specify the maximum
        value calculated by this curve object.

        Args:
            value (float): value for IDD Field `Maximum Curve Output`
                Units are based on field `A4`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Maximum Curve Output"] = value

    @property
    def input_unit_type_for_x(self):
        """Get input_unit_type_for_x.

        Returns:
            str: the value of `input_unit_type_for_x` or None if not set

        """
        return self["Input Unit Type for X"]

    @input_unit_type_for_x.setter
    def input_unit_type_for_x(self, value="Dimensionless"):
        """Corresponds to IDD field `Input Unit Type for X`

        Args:
            value (str): value for IDD Field `Input Unit Type for X`
                Default value: Dimensionless
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Input Unit Type for X"] = value

    @property
    def input_unit_type_for_y(self):
        """Get input_unit_type_for_y.

        Returns:
            str: the value of `input_unit_type_for_y` or None if not set

        """
        return self["Input Unit Type for Y"]

    @input_unit_type_for_y.setter
    def input_unit_type_for_y(self, value="Dimensionless"):
        """Corresponds to IDD field `Input Unit Type for Y`

        Args:
            value (str): value for IDD Field `Input Unit Type for Y`
                Default value: Dimensionless
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Input Unit Type for Y"] = value

    @property
    def output_unit_type(self):
        """Get output_unit_type.

        Returns:
            str: the value of `output_unit_type` or None if not set

        """
        return self["Output Unit Type"]

    @output_unit_type.setter
    def output_unit_type(self, value="Dimensionless"):
        """Corresponds to IDD field `Output Unit Type`

        Args:
            value (str): value for IDD Field `Output Unit Type`
                Default value: Dimensionless
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Output Unit Type"] = value




class CurveQuadraticLinear(DataObject):

    """ Corresponds to IDD object `Curve:QuadraticLinear`
        Quadratic-linear curve with two independent variables. Input consists of the curve
        name, the six coefficients, and min and max values for each of the independent
        variables. Optional inputs for curve minimum and maximum may be used to limit the
        output of the performance curve.
        curve = (C1 + C2*x + C3*x**2) + (C4 + C5*x + C6*x**2)*y
    """
    schema = {'min-fields': 0,
              'name': u'Curve:QuadraticLinear',
              'pyname': u'CurveQuadraticLinear',
              'format': None,
              'fields': OrderedDict([(u'name',
                                      {'name': u'Name',
                                       'pyname': u'name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'alpha'}),
                                     (u'coefficient1 constant',
                                      {'name': u'Coefficient1 Constant',
                                       'pyname': u'coefficient1_constant',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient2 x',
                                      {'name': u'Coefficient2 x',
                                       'pyname': u'coefficient2_x',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient3 x**2',
                                      {'name': u'Coefficient3 x**2',
                                       'pyname': u'coefficient3_x2',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient4 y',
                                      {'name': u'Coefficient4 y',
                                       'pyname': u'coefficient4_y',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient5 x*y',
                                      {'name': u'Coefficient5 x*y',
                                       'pyname': u'coefficient5_xy',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient6 x**2*y',
                                      {'name': u'Coefficient6 x**2*y',
                                       'pyname': u'coefficient6_x2y',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'minimum value of x',
                                      {'name': u'Minimum Value of x',
                                       'pyname': u'minimum_value_of_x',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'maximum value of x',
                                      {'name': u'Maximum Value of x',
                                       'pyname': u'maximum_value_of_x',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'minimum value of y',
                                      {'name': u'Minimum Value of y',
                                       'pyname': u'minimum_value_of_y',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'maximum value of y',
                                      {'name': u'Maximum Value of y',
                                       'pyname': u'maximum_value_of_y',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'minimum curve output',
                                      {'name': u'Minimum Curve Output',
                                       'pyname': u'minimum_curve_output',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'maximum curve output',
                                      {'name': u'Maximum Curve Output',
                                       'pyname': u'maximum_curve_output',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'input unit type for x',
                                      {'name': u'Input Unit Type for X',
                                       'pyname': u'input_unit_type_for_x',
                                       'default': u'Dimensionless',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'Dimensionless',
                                                           u'Temperature',
                                                           u'VolumetricFlow',
                                                           u'MassFlow',
                                                           u'Power',
                                                           u'Distance'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'input unit type for y',
                                      {'name': u'Input Unit Type for Y',
                                       'pyname': u'input_unit_type_for_y',
                                       'default': u'Dimensionless',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'Dimensionless',
                                                           u'Temperature',
                                                           u'VolumetricFlow',
                                                           u'MassFlow',
                                                           u'Power',
                                                           u'Distance'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'output unit type',
                                      {'name': u'Output Unit Type',
                                       'pyname': u'output_unit_type',
                                       'default': u'Dimensionless',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'Dimensionless',
                                                           u'Capacity',
                                                           u'Power'],
                                       'autocalculatable': False,
                                       'type': 'alpha'})]),
              'extensible-fields': OrderedDict(),
              'unique-object': False,
              'required-object': False,
              'group': u'Performance Curves'}

    @property
    def name(self):
        """Get name.

        Returns:
            str: the value of `name` or None if not set

        """
        return self["Name"]

    @name.setter
    def name(self, value=None):
        """Corresponds to IDD field `Name`

        Args:
            value (str): value for IDD Field `Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Name"] = value

    @property
    def coefficient1_constant(self):
        """Get coefficient1_constant.

        Returns:
            float: the value of `coefficient1_constant` or None if not set

        """
        return self["Coefficient1 Constant"]

    @coefficient1_constant.setter
    def coefficient1_constant(self, value=None):
        """Corresponds to IDD field `Coefficient1 Constant`

        Args:
            value (float): value for IDD Field `Coefficient1 Constant`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient1 Constant"] = value

    @property
    def coefficient2_x(self):
        """Get coefficient2_x.

        Returns:
            float: the value of `coefficient2_x` or None if not set

        """
        return self["Coefficient2 x"]

    @coefficient2_x.setter
    def coefficient2_x(self, value=None):
        """Corresponds to IDD field `Coefficient2 x`

        Args:
            value (float): value for IDD Field `Coefficient2 x`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient2 x"] = value

    @property
    def coefficient3_x2(self):
        """Get coefficient3_x2.

        Returns:
            float: the value of `coefficient3_x2` or None if not set

        """
        return self["Coefficient3 x**2"]

    @coefficient3_x2.setter
    def coefficient3_x2(self, value=None):
        """  Corresponds to IDD field `Coefficient3 x**2`

        Args:
            value (float): value for IDD Field `Coefficient3 x**2`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Coefficient3 x**2"] = value

    @property
    def coefficient4_y(self):
        """Get coefficient4_y.

        Returns:
            float: the value of `coefficient4_y` or None if not set

        """
        return self["Coefficient4 y"]

    @coefficient4_y.setter
    def coefficient4_y(self, value=None):
        """Corresponds to IDD field `Coefficient4 y`

        Args:
            value (float): value for IDD Field `Coefficient4 y`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient4 y"] = value

    @property
    def coefficient5_xy(self):
        """Get coefficient5_xy.

        Returns:
            float: the value of `coefficient5_xy` or None if not set

        """
        return self["Coefficient5 x*y"]

    @coefficient5_xy.setter
    def coefficient5_xy(self, value=None):
        """  Corresponds to IDD field `Coefficient5 x*y`

        Args:
            value (float): value for IDD Field `Coefficient5 x*y`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Coefficient5 x*y"] = value

    @property
    def coefficient6_x2y(self):
        """Get coefficient6_x2y.

        Returns:
            float: the value of `coefficient6_x2y` or None if not set

        """
        return self["Coefficient6 x**2*y"]

    @coefficient6_x2y.setter
    def coefficient6_x2y(self, value=None):
        """  Corresponds to IDD field `Coefficient6 x**2*y`

        Args:
            value (float): value for IDD Field `Coefficient6 x**2*y`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Coefficient6 x**2*y"] = value

    @property
    def minimum_value_of_x(self):
        """Get minimum_value_of_x.

        Returns:
            float: the value of `minimum_value_of_x` or None if not set

        """
        return self["Minimum Value of x"]

    @minimum_value_of_x.setter
    def minimum_value_of_x(self, value=None):
        """Corresponds to IDD field `Minimum Value of x`

        Args:
            value (float): value for IDD Field `Minimum Value of x`
                Units are based on field `A2`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Minimum Value of x"] = value

    @property
    def maximum_value_of_x(self):
        """Get maximum_value_of_x.

        Returns:
            float: the value of `maximum_value_of_x` or None if not set

        """
        return self["Maximum Value of x"]

    @maximum_value_of_x.setter
    def maximum_value_of_x(self, value=None):
        """Corresponds to IDD field `Maximum Value of x`

        Args:
            value (float): value for IDD Field `Maximum Value of x`
                Units are based on field `A2`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Maximum Value of x"] = value

    @property
    def minimum_value_of_y(self):
        """Get minimum_value_of_y.

        Returns:
            float: the value of `minimum_value_of_y` or None if not set

        """
        return self["Minimum Value of y"]

    @minimum_value_of_y.setter
    def minimum_value_of_y(self, value=None):
        """Corresponds to IDD field `Minimum Value of y`

        Args:
            value (float): value for IDD Field `Minimum Value of y`
                Units are based on field `A3`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Minimum Value of y"] = value

    @property
    def maximum_value_of_y(self):
        """Get maximum_value_of_y.

        Returns:
            float: the value of `maximum_value_of_y` or None if not set

        """
        return self["Maximum Value of y"]

    @maximum_value_of_y.setter
    def maximum_value_of_y(self, value=None):
        """Corresponds to IDD field `Maximum Value of y`

        Args:
            value (float): value for IDD Field `Maximum Value of y`
                Units are based on field `A3`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Maximum Value of y"] = value

    @property
    def minimum_curve_output(self):
        """Get minimum_curve_output.

        Returns:
            float: the value of `minimum_curve_output` or None if not set

        """
        return self["Minimum Curve Output"]

    @minimum_curve_output.setter
    def minimum_curve_output(self, value=None):
        """Corresponds to IDD field `Minimum Curve Output` Specify the minimum
        value calculated by this curve object.

        Args:
            value (float): value for IDD Field `Minimum Curve Output`
                Units are based on field `A4`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Minimum Curve Output"] = value

    @property
    def maximum_curve_output(self):
        """Get maximum_curve_output.

        Returns:
            float: the value of `maximum_curve_output` or None if not set

        """
        return self["Maximum Curve Output"]

    @maximum_curve_output.setter
    def maximum_curve_output(self, value=None):
        """Corresponds to IDD field `Maximum Curve Output` Specify the maximum
        value calculated by this curve object.

        Args:
            value (float): value for IDD Field `Maximum Curve Output`
                Units are based on field `A4`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Maximum Curve Output"] = value

    @property
    def input_unit_type_for_x(self):
        """Get input_unit_type_for_x.

        Returns:
            str: the value of `input_unit_type_for_x` or None if not set

        """
        return self["Input Unit Type for X"]

    @input_unit_type_for_x.setter
    def input_unit_type_for_x(self, value="Dimensionless"):
        """Corresponds to IDD field `Input Unit Type for X`

        Args:
            value (str): value for IDD Field `Input Unit Type for X`
                Default value: Dimensionless
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Input Unit Type for X"] = value

    @property
    def input_unit_type_for_y(self):
        """Get input_unit_type_for_y.

        Returns:
            str: the value of `input_unit_type_for_y` or None if not set

        """
        return self["Input Unit Type for Y"]

    @input_unit_type_for_y.setter
    def input_unit_type_for_y(self, value="Dimensionless"):
        """Corresponds to IDD field `Input Unit Type for Y`

        Args:
            value (str): value for IDD Field `Input Unit Type for Y`
                Default value: Dimensionless
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Input Unit Type for Y"] = value

    @property
    def output_unit_type(self):
        """Get output_unit_type.

        Returns:
            str: the value of `output_unit_type` or None if not set

        """
        return self["Output Unit Type"]

    @output_unit_type.setter
    def output_unit_type(self, value="Dimensionless"):
        """Corresponds to IDD field `Output Unit Type`

        Args:
            value (str): value for IDD Field `Output Unit Type`
                Default value: Dimensionless
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Output Unit Type"] = value




class CurveTriquadratic(DataObject):

    """ Corresponds to IDD object `Curve:Triquadratic`
        Quadratic curve with three independent variables. Input consists of the curve name,
        the twenty seven coefficients, and min and max values for each of the independent
        variables. Optional inputs for curve minimum and maximum may be used to
        limit the output of the performance curve.
        curve = a0 + a1*x**2 + a2*x + a3*y**2 + a4*y
        + a5*z**2 + a6*z + a7*x**2*y**2 + a8*x*y
        + a9*x*y**2 + a10*x**2*y + a11*x**2*z**2
        + a12*x*z + a13*x*z**2 + a14*x**2*z + a15*y**2*z**2
        + a16*y*z + a17*y*z**2 + a18*y**2*z + a19*x**2*y**2*z**2
        + a20*x**2*y**2*z + a21*x**2*y*z**2 + a22*x*y**2*z**2
        + a23*x**2*y*z + a24*x*y**2*z + a25*x*y*z**2 +a26*x*y*z
    """
    schema = {'min-fields': 0,
              'name': u'Curve:Triquadratic',
              'pyname': u'CurveTriquadratic',
              'format': None,
              'fields': OrderedDict([(u'name',
                                      {'name': u'Name',
                                       'pyname': u'name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'alpha'}),
                                     (u'coefficient1 constant',
                                      {'name': u'Coefficient1 Constant',
                                       'pyname': u'coefficient1_constant',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient2 x**2',
                                      {'name': u'Coefficient2 x**2',
                                       'pyname': u'coefficient2_x2',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient3 x',
                                      {'name': u'Coefficient3 x',
                                       'pyname': u'coefficient3_x',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient4 y**2',
                                      {'name': u'Coefficient4 y**2',
                                       'pyname': u'coefficient4_y2',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient5 y',
                                      {'name': u'Coefficient5 y',
                                       'pyname': u'coefficient5_y',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient6 z**2',
                                      {'name': u'Coefficient6 z**2',
                                       'pyname': u'coefficient6_z2',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient7 z',
                                      {'name': u'Coefficient7 z',
                                       'pyname': u'coefficient7_z',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient8 x**2*y**2',
                                      {'name': u'Coefficient8 x**2*y**2',
                                       'pyname': u'coefficient8_x2y2',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient9 x*y',
                                      {'name': u'Coefficient9 x*y',
                                       'pyname': u'coefficient9_xy',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient10 x*y**2',
                                      {'name': u'Coefficient10 x*y**2',
                                       'pyname': u'coefficient10_xy2',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient11 x**2*y',
                                      {'name': u'Coefficient11 x**2*y',
                                       'pyname': u'coefficient11_x2y',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient12 x**2*z**2',
                                      {'name': u'Coefficient12 x**2*z**2',
                                       'pyname': u'coefficient12_x2z2',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient13 x*z',
                                      {'name': u'Coefficient13 x*z',
                                       'pyname': u'coefficient13_xz',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient14 x*z**2',
                                      {'name': u'Coefficient14 x*z**2',
                                       'pyname': u'coefficient14_xz2',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient15 x**2*z',
                                      {'name': u'Coefficient15 x**2*z',
                                       'pyname': u'coefficient15_x2z',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient16 y**2*z**2',
                                      {'name': u'Coefficient16 y**2*z**2',
                                       'pyname': u'coefficient16_y2z2',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient17 y*z',
                                      {'name': u'Coefficient17 y*z',
                                       'pyname': u'coefficient17_yz',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient18 y*z**2',
                                      {'name': u'Coefficient18 y*z**2',
                                       'pyname': u'coefficient18_yz2',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient19 y**2*z',
                                      {'name': u'Coefficient19 y**2*z',
                                       'pyname': u'coefficient19_y2z',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient20 x**2*y**2*z**2',
                                      {'name': u'Coefficient20 x**2*y**2*z**2',
                                       'pyname': u'coefficient20_x2y2z2',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient21 x**2*y**2*z',
                                      {'name': u'Coefficient21 x**2*y**2*z',
                                       'pyname': u'coefficient21_x2y2z',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient22 x**2*y*z**2',
                                      {'name': u'Coefficient22 x**2*y*z**2',
                                       'pyname': u'coefficient22_x2yz2',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient23 x*y**2*z**2',
                                      {'name': u'Coefficient23 x*y**2*z**2',
                                       'pyname': u'coefficient23_xy2z2',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient24 x**2*y*z',
                                      {'name': u'Coefficient24 x**2*y*z',
                                       'pyname': u'coefficient24_x2yz',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient25 x*y**2*z',
                                      {'name': u'Coefficient25 x*y**2*z',
                                       'pyname': u'coefficient25_xy2z',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient26 x*y*z**2',
                                      {'name': u'Coefficient26 x*y*z**2',
                                       'pyname': u'coefficient26_xyz2',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient27 x*y*z',
                                      {'name': u'Coefficient27 x*y*z',
                                       'pyname': u'coefficient27_xyz',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'minimum value of x',
                                      {'name': u'Minimum Value of x',
                                       'pyname': u'minimum_value_of_x',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'maximum value of x',
                                      {'name': u'Maximum Value of x',
                                       'pyname': u'maximum_value_of_x',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'minimum value of y',
                                      {'name': u'Minimum Value of y',
                                       'pyname': u'minimum_value_of_y',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'maximum value of y',
                                      {'name': u'Maximum Value of y',
                                       'pyname': u'maximum_value_of_y',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'minimum value of z',
                                      {'name': u'Minimum Value of z',
                                       'pyname': u'minimum_value_of_z',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'maximum value of z',
                                      {'name': u'Maximum Value of z',
                                       'pyname': u'maximum_value_of_z',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'minimum curve output',
                                      {'name': u'Minimum Curve Output',
                                       'pyname': u'minimum_curve_output',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'maximum curve output',
                                      {'name': u'Maximum Curve Output',
                                       'pyname': u'maximum_curve_output',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'input unit type for x',
                                      {'name': u'Input Unit Type for X',
                                       'pyname': u'input_unit_type_for_x',
                                       'default': u'Dimensionless',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'Dimensionless',
                                                           u'Temperature',
                                                           u'VolumetricFlow',
                                                           u'MassFlow',
                                                           u'Power',
                                                           u'Distance'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'input unit type for y',
                                      {'name': u'Input Unit Type for Y',
                                       'pyname': u'input_unit_type_for_y',
                                       'default': u'Dimensionless',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'Dimensionless',
                                                           u'Temperature',
                                                           u'VolumetricFlow',
                                                           u'MassFlow',
                                                           u'Power',
                                                           u'Distance'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'input unit type for z',
                                      {'name': u'Input Unit Type for Z',
                                       'pyname': u'input_unit_type_for_z',
                                       'default': u'Dimensionless',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'Dimensionless',
                                                           u'Temperature',
                                                           u'VolumetricFlow',
                                                           u'MassFlow',
                                                           u'Power',
                                                           u'Distance'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'output unit type',
                                      {'name': u'Output Unit Type',
                                       'pyname': u'output_unit_type',
                                       'default': u'Dimensionless',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'Dimensionless',
                                                           u'Capacity',
                                                           u'Power'],
                                       'autocalculatable': False,
                                       'type': 'alpha'})]),
              'extensible-fields': OrderedDict(),
              'unique-object': False,
              'required-object': False,
              'group': u'Performance Curves'}

    @property
    def name(self):
        """Get name.

        Returns:
            str: the value of `name` or None if not set

        """
        return self["Name"]

    @name.setter
    def name(self, value=None):
        """Corresponds to IDD field `Name`

        Args:
            value (str): value for IDD Field `Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Name"] = value

    @property
    def coefficient1_constant(self):
        """Get coefficient1_constant.

        Returns:
            float: the value of `coefficient1_constant` or None if not set

        """
        return self["Coefficient1 Constant"]

    @coefficient1_constant.setter
    def coefficient1_constant(self, value=None):
        """Corresponds to IDD field `Coefficient1 Constant`

        Args:
            value (float): value for IDD Field `Coefficient1 Constant`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient1 Constant"] = value

    @property
    def coefficient2_x2(self):
        """Get coefficient2_x2.

        Returns:
            float: the value of `coefficient2_x2` or None if not set

        """
        return self["Coefficient2 x**2"]

    @coefficient2_x2.setter
    def coefficient2_x2(self, value=None):
        """  Corresponds to IDD field `Coefficient2 x**2`

        Args:
            value (float): value for IDD Field `Coefficient2 x**2`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Coefficient2 x**2"] = value

    @property
    def coefficient3_x(self):
        """Get coefficient3_x.

        Returns:
            float: the value of `coefficient3_x` or None if not set

        """
        return self["Coefficient3 x"]

    @coefficient3_x.setter
    def coefficient3_x(self, value=None):
        """Corresponds to IDD field `Coefficient3 x`

        Args:
            value (float): value for IDD Field `Coefficient3 x`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient3 x"] = value

    @property
    def coefficient4_y2(self):
        """Get coefficient4_y2.

        Returns:
            float: the value of `coefficient4_y2` or None if not set

        """
        return self["Coefficient4 y**2"]

    @coefficient4_y2.setter
    def coefficient4_y2(self, value=None):
        """  Corresponds to IDD field `Coefficient4 y**2`

        Args:
            value (float): value for IDD Field `Coefficient4 y**2`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Coefficient4 y**2"] = value

    @property
    def coefficient5_y(self):
        """Get coefficient5_y.

        Returns:
            float: the value of `coefficient5_y` or None if not set

        """
        return self["Coefficient5 y"]

    @coefficient5_y.setter
    def coefficient5_y(self, value=None):
        """Corresponds to IDD field `Coefficient5 y`

        Args:
            value (float): value for IDD Field `Coefficient5 y`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient5 y"] = value

    @property
    def coefficient6_z2(self):
        """Get coefficient6_z2.

        Returns:
            float: the value of `coefficient6_z2` or None if not set

        """
        return self["Coefficient6 z**2"]

    @coefficient6_z2.setter
    def coefficient6_z2(self, value=None):
        """  Corresponds to IDD field `Coefficient6 z**2`

        Args:
            value (float): value for IDD Field `Coefficient6 z**2`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Coefficient6 z**2"] = value

    @property
    def coefficient7_z(self):
        """Get coefficient7_z.

        Returns:
            float: the value of `coefficient7_z` or None if not set

        """
        return self["Coefficient7 z"]

    @coefficient7_z.setter
    def coefficient7_z(self, value=None):
        """Corresponds to IDD field `Coefficient7 z`

        Args:
            value (float): value for IDD Field `Coefficient7 z`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient7 z"] = value

    @property
    def coefficient8_x2y2(self):
        """Get coefficient8_x2y2.

        Returns:
            float: the value of `coefficient8_x2y2` or None if not set

        """
        return self["Coefficient8 x**2*y**2"]

    @coefficient8_x2y2.setter
    def coefficient8_x2y2(self, value=None):
        """  Corresponds to IDD field `Coefficient8 x**2*y**2`

        Args:
            value (float): value for IDD Field `Coefficient8 x**2*y**2`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Coefficient8 x**2*y**2"] = value

    @property
    def coefficient9_xy(self):
        """Get coefficient9_xy.

        Returns:
            float: the value of `coefficient9_xy` or None if not set

        """
        return self["Coefficient9 x*y"]

    @coefficient9_xy.setter
    def coefficient9_xy(self, value=None):
        """  Corresponds to IDD field `Coefficient9 x*y`

        Args:
            value (float): value for IDD Field `Coefficient9 x*y`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Coefficient9 x*y"] = value

    @property
    def coefficient10_xy2(self):
        """Get coefficient10_xy2.

        Returns:
            float: the value of `coefficient10_xy2` or None if not set

        """
        return self["Coefficient10 x*y**2"]

    @coefficient10_xy2.setter
    def coefficient10_xy2(self, value=None):
        """  Corresponds to IDD field `Coefficient10 x*y**2`

        Args:
            value (float): value for IDD Field `Coefficient10 x*y**2`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Coefficient10 x*y**2"] = value

    @property
    def coefficient11_x2y(self):
        """Get coefficient11_x2y.

        Returns:
            float: the value of `coefficient11_x2y` or None if not set

        """
        return self["Coefficient11 x**2*y"]

    @coefficient11_x2y.setter
    def coefficient11_x2y(self, value=None):
        """  Corresponds to IDD field `Coefficient11 x**2*y`

        Args:
            value (float): value for IDD Field `Coefficient11 x**2*y`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Coefficient11 x**2*y"] = value

    @property
    def coefficient12_x2z2(self):
        """Get coefficient12_x2z2.

        Returns:
            float: the value of `coefficient12_x2z2` or None if not set

        """
        return self["Coefficient12 x**2*z**2"]

    @coefficient12_x2z2.setter
    def coefficient12_x2z2(self, value=None):
        """  Corresponds to IDD field `Coefficient12 x**2*z**2`

        Args:
            value (float): value for IDD Field `Coefficient12 x**2*z**2`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Coefficient12 x**2*z**2"] = value

    @property
    def coefficient13_xz(self):
        """Get coefficient13_xz.

        Returns:
            float: the value of `coefficient13_xz` or None if not set

        """
        return self["Coefficient13 x*z"]

    @coefficient13_xz.setter
    def coefficient13_xz(self, value=None):
        """  Corresponds to IDD field `Coefficient13 x*z`

        Args:
            value (float): value for IDD Field `Coefficient13 x*z`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Coefficient13 x*z"] = value

    @property
    def coefficient14_xz2(self):
        """Get coefficient14_xz2.

        Returns:
            float: the value of `coefficient14_xz2` or None if not set

        """
        return self["Coefficient14 x*z**2"]

    @coefficient14_xz2.setter
    def coefficient14_xz2(self, value=None):
        """  Corresponds to IDD field `Coefficient14 x*z**2`

        Args:
            value (float): value for IDD Field `Coefficient14 x*z**2`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Coefficient14 x*z**2"] = value

    @property
    def coefficient15_x2z(self):
        """Get coefficient15_x2z.

        Returns:
            float: the value of `coefficient15_x2z` or None if not set

        """
        return self["Coefficient15 x**2*z"]

    @coefficient15_x2z.setter
    def coefficient15_x2z(self, value=None):
        """  Corresponds to IDD field `Coefficient15 x**2*z`

        Args:
            value (float): value for IDD Field `Coefficient15 x**2*z`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Coefficient15 x**2*z"] = value

    @property
    def coefficient16_y2z2(self):
        """Get coefficient16_y2z2.

        Returns:
            float: the value of `coefficient16_y2z2` or None if not set

        """
        return self["Coefficient16 y**2*z**2"]

    @coefficient16_y2z2.setter
    def coefficient16_y2z2(self, value=None):
        """  Corresponds to IDD field `Coefficient16 y**2*z**2`

        Args:
            value (float): value for IDD Field `Coefficient16 y**2*z**2`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Coefficient16 y**2*z**2"] = value

    @property
    def coefficient17_yz(self):
        """Get coefficient17_yz.

        Returns:
            float: the value of `coefficient17_yz` or None if not set

        """
        return self["Coefficient17 y*z"]

    @coefficient17_yz.setter
    def coefficient17_yz(self, value=None):
        """  Corresponds to IDD field `Coefficient17 y*z`

        Args:
            value (float): value for IDD Field `Coefficient17 y*z`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Coefficient17 y*z"] = value

    @property
    def coefficient18_yz2(self):
        """Get coefficient18_yz2.

        Returns:
            float: the value of `coefficient18_yz2` or None if not set

        """
        return self["Coefficient18 y*z**2"]

    @coefficient18_yz2.setter
    def coefficient18_yz2(self, value=None):
        """  Corresponds to IDD field `Coefficient18 y*z**2`

        Args:
            value (float): value for IDD Field `Coefficient18 y*z**2`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Coefficient18 y*z**2"] = value

    @property
    def coefficient19_y2z(self):
        """Get coefficient19_y2z.

        Returns:
            float: the value of `coefficient19_y2z` or None if not set

        """
        return self["Coefficient19 y**2*z"]

    @coefficient19_y2z.setter
    def coefficient19_y2z(self, value=None):
        """  Corresponds to IDD field `Coefficient19 y**2*z`

        Args:
            value (float): value for IDD Field `Coefficient19 y**2*z`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Coefficient19 y**2*z"] = value

    @property
    def coefficient20_x2y2z2(self):
        """Get coefficient20_x2y2z2.

        Returns:
            float: the value of `coefficient20_x2y2z2` or None if not set

        """
        return self["Coefficient20 x**2*y**2*z**2"]

    @coefficient20_x2y2z2.setter
    def coefficient20_x2y2z2(self, value=None):
        """  Corresponds to IDD field `Coefficient20 x**2*y**2*z**2`

        Args:
            value (float): value for IDD Field `Coefficient20 x**2*y**2*z**2`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Coefficient20 x**2*y**2*z**2"] = value

    @property
    def coefficient21_x2y2z(self):
        """Get coefficient21_x2y2z.

        Returns:
            float: the value of `coefficient21_x2y2z` or None if not set

        """
        return self["Coefficient21 x**2*y**2*z"]

    @coefficient21_x2y2z.setter
    def coefficient21_x2y2z(self, value=None):
        """  Corresponds to IDD field `Coefficient21 x**2*y**2*z`

        Args:
            value (float): value for IDD Field `Coefficient21 x**2*y**2*z`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Coefficient21 x**2*y**2*z"] = value

    @property
    def coefficient22_x2yz2(self):
        """Get coefficient22_x2yz2.

        Returns:
            float: the value of `coefficient22_x2yz2` or None if not set

        """
        return self["Coefficient22 x**2*y*z**2"]

    @coefficient22_x2yz2.setter
    def coefficient22_x2yz2(self, value=None):
        """  Corresponds to IDD field `Coefficient22 x**2*y*z**2`

        Args:
            value (float): value for IDD Field `Coefficient22 x**2*y*z**2`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Coefficient22 x**2*y*z**2"] = value

    @property
    def coefficient23_xy2z2(self):
        """Get coefficient23_xy2z2.

        Returns:
            float: the value of `coefficient23_xy2z2` or None if not set

        """
        return self["Coefficient23 x*y**2*z**2"]

    @coefficient23_xy2z2.setter
    def coefficient23_xy2z2(self, value=None):
        """  Corresponds to IDD field `Coefficient23 x*y**2*z**2`

        Args:
            value (float): value for IDD Field `Coefficient23 x*y**2*z**2`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Coefficient23 x*y**2*z**2"] = value

    @property
    def coefficient24_x2yz(self):
        """Get coefficient24_x2yz.

        Returns:
            float: the value of `coefficient24_x2yz` or None if not set

        """
        return self["Coefficient24 x**2*y*z"]

    @coefficient24_x2yz.setter
    def coefficient24_x2yz(self, value=None):
        """  Corresponds to IDD field `Coefficient24 x**2*y*z`

        Args:
            value (float): value for IDD Field `Coefficient24 x**2*y*z`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Coefficient24 x**2*y*z"] = value

    @property
    def coefficient25_xy2z(self):
        """Get coefficient25_xy2z.

        Returns:
            float: the value of `coefficient25_xy2z` or None if not set

        """
        return self["Coefficient25 x*y**2*z"]

    @coefficient25_xy2z.setter
    def coefficient25_xy2z(self, value=None):
        """  Corresponds to IDD field `Coefficient25 x*y**2*z`

        Args:
            value (float): value for IDD Field `Coefficient25 x*y**2*z`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Coefficient25 x*y**2*z"] = value

    @property
    def coefficient26_xyz2(self):
        """Get coefficient26_xyz2.

        Returns:
            float: the value of `coefficient26_xyz2` or None if not set

        """
        return self["Coefficient26 x*y*z**2"]

    @coefficient26_xyz2.setter
    def coefficient26_xyz2(self, value=None):
        """  Corresponds to IDD field `Coefficient26 x*y*z**2`

        Args:
            value (float): value for IDD Field `Coefficient26 x*y*z**2`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Coefficient26 x*y*z**2"] = value

    @property
    def coefficient27_xyz(self):
        """Get coefficient27_xyz.

        Returns:
            float: the value of `coefficient27_xyz` or None if not set

        """
        return self["Coefficient27 x*y*z"]

    @coefficient27_xyz.setter
    def coefficient27_xyz(self, value=None):
        """  Corresponds to IDD field `Coefficient27 x*y*z`

        Args:
            value (float): value for IDD Field `Coefficient27 x*y*z`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Coefficient27 x*y*z"] = value

    @property
    def minimum_value_of_x(self):
        """Get minimum_value_of_x.

        Returns:
            float: the value of `minimum_value_of_x` or None if not set

        """
        return self["Minimum Value of x"]

    @minimum_value_of_x.setter
    def minimum_value_of_x(self, value=None):
        """Corresponds to IDD field `Minimum Value of x`

        Args:
            value (float): value for IDD Field `Minimum Value of x`
                Units are based on field `A2`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Minimum Value of x"] = value

    @property
    def maximum_value_of_x(self):
        """Get maximum_value_of_x.

        Returns:
            float: the value of `maximum_value_of_x` or None if not set

        """
        return self["Maximum Value of x"]

    @maximum_value_of_x.setter
    def maximum_value_of_x(self, value=None):
        """Corresponds to IDD field `Maximum Value of x`

        Args:
            value (float): value for IDD Field `Maximum Value of x`
                Units are based on field `A2`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Maximum Value of x"] = value

    @property
    def minimum_value_of_y(self):
        """Get minimum_value_of_y.

        Returns:
            float: the value of `minimum_value_of_y` or None if not set

        """
        return self["Minimum Value of y"]

    @minimum_value_of_y.setter
    def minimum_value_of_y(self, value=None):
        """Corresponds to IDD field `Minimum Value of y`

        Args:
            value (float): value for IDD Field `Minimum Value of y`
                Units are based on field `A3`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Minimum Value of y"] = value

    @property
    def maximum_value_of_y(self):
        """Get maximum_value_of_y.

        Returns:
            float: the value of `maximum_value_of_y` or None if not set

        """
        return self["Maximum Value of y"]

    @maximum_value_of_y.setter
    def maximum_value_of_y(self, value=None):
        """Corresponds to IDD field `Maximum Value of y`

        Args:
            value (float): value for IDD Field `Maximum Value of y`
                Units are based on field `A3`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Maximum Value of y"] = value

    @property
    def minimum_value_of_z(self):
        """Get minimum_value_of_z.

        Returns:
            float: the value of `minimum_value_of_z` or None if not set

        """
        return self["Minimum Value of z"]

    @minimum_value_of_z.setter
    def minimum_value_of_z(self, value=None):
        """Corresponds to IDD field `Minimum Value of z`

        Args:
            value (float): value for IDD Field `Minimum Value of z`
                Units are based on field `A4`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Minimum Value of z"] = value

    @property
    def maximum_value_of_z(self):
        """Get maximum_value_of_z.

        Returns:
            float: the value of `maximum_value_of_z` or None if not set

        """
        return self["Maximum Value of z"]

    @maximum_value_of_z.setter
    def maximum_value_of_z(self, value=None):
        """Corresponds to IDD field `Maximum Value of z`

        Args:
            value (float): value for IDD Field `Maximum Value of z`
                Units are based on field `A4`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Maximum Value of z"] = value

    @property
    def minimum_curve_output(self):
        """Get minimum_curve_output.

        Returns:
            float: the value of `minimum_curve_output` or None if not set

        """
        return self["Minimum Curve Output"]

    @minimum_curve_output.setter
    def minimum_curve_output(self, value=None):
        """Corresponds to IDD field `Minimum Curve Output` Specify the minimum
        value calculated by this curve object.

        Args:
            value (float): value for IDD Field `Minimum Curve Output`
                Units are based on field `A5`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Minimum Curve Output"] = value

    @property
    def maximum_curve_output(self):
        """Get maximum_curve_output.

        Returns:
            float: the value of `maximum_curve_output` or None if not set

        """
        return self["Maximum Curve Output"]

    @maximum_curve_output.setter
    def maximum_curve_output(self, value=None):
        """Corresponds to IDD field `Maximum Curve Output` Specify the maximum
        value calculated by this curve object.

        Args:
            value (float): value for IDD Field `Maximum Curve Output`
                Units are based on field `A5`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Maximum Curve Output"] = value

    @property
    def input_unit_type_for_x(self):
        """Get input_unit_type_for_x.

        Returns:
            str: the value of `input_unit_type_for_x` or None if not set

        """
        return self["Input Unit Type for X"]

    @input_unit_type_for_x.setter
    def input_unit_type_for_x(self, value="Dimensionless"):
        """Corresponds to IDD field `Input Unit Type for X`

        Args:
            value (str): value for IDD Field `Input Unit Type for X`
                Default value: Dimensionless
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Input Unit Type for X"] = value

    @property
    def input_unit_type_for_y(self):
        """Get input_unit_type_for_y.

        Returns:
            str: the value of `input_unit_type_for_y` or None if not set

        """
        return self["Input Unit Type for Y"]

    @input_unit_type_for_y.setter
    def input_unit_type_for_y(self, value="Dimensionless"):
        """Corresponds to IDD field `Input Unit Type for Y`

        Args:
            value (str): value for IDD Field `Input Unit Type for Y`
                Default value: Dimensionless
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Input Unit Type for Y"] = value

    @property
    def input_unit_type_for_z(self):
        """Get input_unit_type_for_z.

        Returns:
            str: the value of `input_unit_type_for_z` or None if not set

        """
        return self["Input Unit Type for Z"]

    @input_unit_type_for_z.setter
    def input_unit_type_for_z(self, value="Dimensionless"):
        """Corresponds to IDD field `Input Unit Type for Z`

        Args:
            value (str): value for IDD Field `Input Unit Type for Z`
                Default value: Dimensionless
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Input Unit Type for Z"] = value

    @property
    def output_unit_type(self):
        """Get output_unit_type.

        Returns:
            str: the value of `output_unit_type` or None if not set

        """
        return self["Output Unit Type"]

    @output_unit_type.setter
    def output_unit_type(self, value="Dimensionless"):
        """Corresponds to IDD field `Output Unit Type`

        Args:
            value (str): value for IDD Field `Output Unit Type`
                Default value: Dimensionless
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Output Unit Type"] = value




class CurveFunctionalPressureDrop(DataObject):

    """ Corresponds to IDD object `Curve:Functional:PressureDrop`
        Sets up curve information for minor loss and/or friction
        calculations in plant pressure simulations
        Expression: DeltaP = {K + f*(L/D)} * (rho * V^2) / 2
    """
    schema = {'min-fields': 5,
              'name': u'Curve:Functional:PressureDrop',
              'pyname': u'CurveFunctionalPressureDrop',
              'format': None,
              'fields': OrderedDict([(u'name',
                                      {'name': u'Name',
                                       'pyname': u'name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'alpha'}),
                                     (u'diameter',
                                      {'name': u'Diameter',
                                       'pyname': u'diameter',
                                       'minimum>': 0.0,
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'm'}),
                                     (u'minor loss coefficient',
                                      {'name': u'Minor Loss Coefficient',
                                       'pyname': u'minor_loss_coefficient',
                                       'minimum>': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'dimensionless'}),
                                     (u'length',
                                      {'name': u'Length',
                                       'pyname': u'length',
                                       'minimum>': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'm'}),
                                     (u'roughness',
                                      {'name': u'Roughness',
                                       'pyname': u'roughness',
                                       'minimum>': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'm'}),
                                     (u'fixed friction factor',
                                      {'name': u'Fixed Friction Factor',
                                       'pyname': u'fixed_friction_factor',
                                       'minimum>': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real'})]),
              'extensible-fields': OrderedDict(),
              'unique-object': False,
              'required-object': False,
              'group': u'Performance Curves'}

    @property
    def name(self):
        """Get name.

        Returns:
            str: the value of `name` or None if not set

        """
        return self["Name"]

    @name.setter
    def name(self, value=None):
        """Corresponds to IDD field `Name`

        Args:
            value (str): value for IDD Field `Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Name"] = value

    @property
    def diameter(self):
        """Get diameter.

        Returns:
            float: the value of `diameter` or None if not set

        """
        return self["Diameter"]

    @diameter.setter
    def diameter(self, value=None):
        """Corresponds to IDD field `Diameter` "D" in above expression, used to
        also calculate local velocity.

        Args:
            value (float): value for IDD Field `Diameter`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Diameter"] = value

    @property
    def minor_loss_coefficient(self):
        """Get minor_loss_coefficient.

        Returns:
            float: the value of `minor_loss_coefficient` or None if not set

        """
        return self["Minor Loss Coefficient"]

    @minor_loss_coefficient.setter
    def minor_loss_coefficient(self, value=None):
        """Corresponds to IDD field `Minor Loss Coefficient` "K" in above
        expression.

        Args:
            value (float): value for IDD Field `Minor Loss Coefficient`
                Units: dimensionless
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Minor Loss Coefficient"] = value

    @property
    def length(self):
        """Get length.

        Returns:
            float: the value of `length` or None if not set

        """
        return self["Length"]

    @length.setter
    def length(self, value=None):
        """Corresponds to IDD field `Length` "L" in above expression.

        Args:
            value (float): value for IDD Field `Length`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Length"] = value

    @property
    def roughness(self):
        """Get roughness.

        Returns:
            float: the value of `roughness` or None if not set

        """
        return self["Roughness"]

    @roughness.setter
    def roughness(self, value=None):
        """  Corresponds to IDD field `Roughness`
        This will be used to calculate "f" from Moody-chart approximations

        Args:
            value (float): value for IDD Field `Roughness`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Roughness"] = value

    @property
    def fixed_friction_factor(self):
        """Get fixed_friction_factor.

        Returns:
            float: the value of `fixed_friction_factor` or None if not set

        """
        return self["Fixed Friction Factor"]

    @fixed_friction_factor.setter
    def fixed_friction_factor(self, value=None):
        """  Corresponds to IDD field `Fixed Friction Factor`
        Optional way to set a constant value for "f", instead of using
        internal Moody-chart approximations

        Args:
            value (float): value for IDD Field `Fixed Friction Factor`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Fixed Friction Factor"] = value




class CurveFanPressureRise(DataObject):

    """ Corresponds to IDD object `Curve:FanPressureRise`
        Special curve type with two independent variables.
        Input for the fan total pressure rise curve consists of the curve name, the four
        coefficients, and the maximum and minimum valid independent variable values. Optional
        inputs for the curve minimum and maximum may be used to limit the output of the
        performance curve.
        curve = C1*Qfan**2+C2*Qfan+C3*Qfan*(Psm-Po)**0.5+C4*(Psm-Po)
        Po assumed to be zero
        See InputOut Reference for curve details
    """
    schema = {'min-fields': 0,
              'name': u'Curve:FanPressureRise',
              'pyname': u'CurveFanPressureRise',
              'format': None,
              'fields': OrderedDict([(u'name',
                                      {'name': u'Name',
                                       'pyname': u'name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'alpha'}),
                                     (u'coefficient1 c1',
                                      {'name': u'Coefficient1 C1',
                                       'pyname': u'coefficient1_c1',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient2 c2',
                                      {'name': u'Coefficient2 C2',
                                       'pyname': u'coefficient2_c2',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient3 c3',
                                      {'name': u'Coefficient3 C3',
                                       'pyname': u'coefficient3_c3',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient4 c4',
                                      {'name': u'Coefficient4 C4',
                                       'pyname': u'coefficient4_c4',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'minimum value of qfan',
                                      {'name': u'Minimum Value of Qfan',
                                       'pyname': u'minimum_value_of_qfan',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'm3/s'}),
                                     (u'maximum value of qfan',
                                      {'name': u'Maximum Value of Qfan',
                                       'pyname': u'maximum_value_of_qfan',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'm3/s'}),
                                     (u'minimum value of psm',
                                      {'name': u'Minimum Value of Psm',
                                       'pyname': u'minimum_value_of_psm',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'Pa'}),
                                     (u'maximum value of psm',
                                      {'name': u'Maximum Value of Psm',
                                       'pyname': u'maximum_value_of_psm',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'Pa'}),
                                     (u'minimum curve output',
                                      {'name': u'Minimum Curve Output',
                                       'pyname': u'minimum_curve_output',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'Pa'}),
                                     (u'maximum curve output',
                                      {'name': u'Maximum Curve Output',
                                       'pyname': u'maximum_curve_output',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'Pa'})]),
              'extensible-fields': OrderedDict(),
              'unique-object': False,
              'required-object': False,
              'group': u'Performance Curves'}

    @property
    def name(self):
        """Get name.

        Returns:
            str: the value of `name` or None if not set

        """
        return self["Name"]

    @name.setter
    def name(self, value=None):
        """Corresponds to IDD field `Name`

        Args:
            value (str): value for IDD Field `Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Name"] = value

    @property
    def coefficient1_c1(self):
        """Get coefficient1_c1.

        Returns:
            float: the value of `coefficient1_c1` or None if not set

        """
        return self["Coefficient1 C1"]

    @coefficient1_c1.setter
    def coefficient1_c1(self, value=None):
        """Corresponds to IDD field `Coefficient1 C1`

        Args:
            value (float): value for IDD Field `Coefficient1 C1`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient1 C1"] = value

    @property
    def coefficient2_c2(self):
        """Get coefficient2_c2.

        Returns:
            float: the value of `coefficient2_c2` or None if not set

        """
        return self["Coefficient2 C2"]

    @coefficient2_c2.setter
    def coefficient2_c2(self, value=None):
        """Corresponds to IDD field `Coefficient2 C2`

        Args:
            value (float): value for IDD Field `Coefficient2 C2`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient2 C2"] = value

    @property
    def coefficient3_c3(self):
        """Get coefficient3_c3.

        Returns:
            float: the value of `coefficient3_c3` or None if not set

        """
        return self["Coefficient3 C3"]

    @coefficient3_c3.setter
    def coefficient3_c3(self, value=None):
        """Corresponds to IDD field `Coefficient3 C3`

        Args:
            value (float): value for IDD Field `Coefficient3 C3`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient3 C3"] = value

    @property
    def coefficient4_c4(self):
        """Get coefficient4_c4.

        Returns:
            float: the value of `coefficient4_c4` or None if not set

        """
        return self["Coefficient4 C4"]

    @coefficient4_c4.setter
    def coefficient4_c4(self, value=None):
        """Corresponds to IDD field `Coefficient4 C4`

        Args:
            value (float): value for IDD Field `Coefficient4 C4`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient4 C4"] = value

    @property
    def minimum_value_of_qfan(self):
        """Get minimum_value_of_qfan.

        Returns:
            float: the value of `minimum_value_of_qfan` or None if not set

        """
        return self["Minimum Value of Qfan"]

    @minimum_value_of_qfan.setter
    def minimum_value_of_qfan(self, value=None):
        """Corresponds to IDD field `Minimum Value of Qfan`

        Args:
            value (float): value for IDD Field `Minimum Value of Qfan`
                Units: m3/s
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Minimum Value of Qfan"] = value

    @property
    def maximum_value_of_qfan(self):
        """Get maximum_value_of_qfan.

        Returns:
            float: the value of `maximum_value_of_qfan` or None if not set

        """
        return self["Maximum Value of Qfan"]

    @maximum_value_of_qfan.setter
    def maximum_value_of_qfan(self, value=None):
        """Corresponds to IDD field `Maximum Value of Qfan`

        Args:
            value (float): value for IDD Field `Maximum Value of Qfan`
                Units: m3/s
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Maximum Value of Qfan"] = value

    @property
    def minimum_value_of_psm(self):
        """Get minimum_value_of_psm.

        Returns:
            float: the value of `minimum_value_of_psm` or None if not set

        """
        return self["Minimum Value of Psm"]

    @minimum_value_of_psm.setter
    def minimum_value_of_psm(self, value=None):
        """Corresponds to IDD field `Minimum Value of Psm`

        Args:
            value (float): value for IDD Field `Minimum Value of Psm`
                Units: Pa
                IP-Units: Pa
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Minimum Value of Psm"] = value

    @property
    def maximum_value_of_psm(self):
        """Get maximum_value_of_psm.

        Returns:
            float: the value of `maximum_value_of_psm` or None if not set

        """
        return self["Maximum Value of Psm"]

    @maximum_value_of_psm.setter
    def maximum_value_of_psm(self, value=None):
        """Corresponds to IDD field `Maximum Value of Psm`

        Args:
            value (float): value for IDD Field `Maximum Value of Psm`
                Units: Pa
                IP-Units: Pa
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Maximum Value of Psm"] = value

    @property
    def minimum_curve_output(self):
        """Get minimum_curve_output.

        Returns:
            float: the value of `minimum_curve_output` or None if not set

        """
        return self["Minimum Curve Output"]

    @minimum_curve_output.setter
    def minimum_curve_output(self, value=None):
        """Corresponds to IDD field `Minimum Curve Output` Specify the minimum
        value calculated by this curve object.

        Args:
            value (float): value for IDD Field `Minimum Curve Output`
                Units: Pa
                IP-Units: Pa
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Minimum Curve Output"] = value

    @property
    def maximum_curve_output(self):
        """Get maximum_curve_output.

        Returns:
            float: the value of `maximum_curve_output` or None if not set

        """
        return self["Maximum Curve Output"]

    @maximum_curve_output.setter
    def maximum_curve_output(self, value=None):
        """Corresponds to IDD field `Maximum Curve Output` Specify the maximum
        value calculated by this curve object.

        Args:
            value (float): value for IDD Field `Maximum Curve Output`
                Units: Pa
                IP-Units: Pa
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Maximum Curve Output"] = value




class CurveExponentialSkewNormal(DataObject):

    """ Corresponds to IDD object `Curve:ExponentialSkewNormal`
        Exponential-modified skew normal curve with one independent variable.
        Input consists of the curve name, the four coefficients, and the maximum
        and minimum valid independent variable values. Optional inputs for the curve minimum
        and maximum may be used to limit the output of the performance curve.
        curve = see Input Output Reference
    """
    schema = {'min-fields': 0,
              'name': u'Curve:ExponentialSkewNormal',
              'pyname': u'CurveExponentialSkewNormal',
              'format': None,
              'fields': OrderedDict([(u'name',
                                      {'name': u'Name',
                                       'pyname': u'name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'alpha'}),
                                     (u'coefficient1 c1',
                                      {'name': u'Coefficient1 C1',
                                       'pyname': u'coefficient1_c1',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient2 c2',
                                      {'name': u'Coefficient2 C2',
                                       'pyname': u'coefficient2_c2',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient3 c3',
                                      {'name': u'Coefficient3 C3',
                                       'pyname': u'coefficient3_c3',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient4 c4',
                                      {'name': u'Coefficient4 C4',
                                       'pyname': u'coefficient4_c4',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'minimum value of x',
                                      {'name': u'Minimum Value of x',
                                       'pyname': u'minimum_value_of_x',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'maximum value of x',
                                      {'name': u'Maximum Value of x',
                                       'pyname': u'maximum_value_of_x',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'minimum curve output',
                                      {'name': u'Minimum Curve Output',
                                       'pyname': u'minimum_curve_output',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'maximum curve output',
                                      {'name': u'Maximum Curve Output',
                                       'pyname': u'maximum_curve_output',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'input unit type for x',
                                      {'name': u'Input Unit Type for x',
                                       'pyname': u'input_unit_type_for_x',
                                       'default': u'Dimensionless',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'Dimensionless'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'output unit type',
                                      {'name': u'Output Unit Type',
                                       'pyname': u'output_unit_type',
                                       'default': u'Dimensionless',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'Dimensionless'],
                                       'autocalculatable': False,
                                       'type': 'alpha'})]),
              'extensible-fields': OrderedDict(),
              'unique-object': False,
              'required-object': False,
              'group': u'Performance Curves'}

    @property
    def name(self):
        """Get name.

        Returns:
            str: the value of `name` or None if not set

        """
        return self["Name"]

    @name.setter
    def name(self, value=None):
        """Corresponds to IDD field `Name` See InputOut Reference for curve
        description.

        Args:
            value (str): value for IDD Field `Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Name"] = value

    @property
    def coefficient1_c1(self):
        """Get coefficient1_c1.

        Returns:
            float: the value of `coefficient1_c1` or None if not set

        """
        return self["Coefficient1 C1"]

    @coefficient1_c1.setter
    def coefficient1_c1(self, value=None):
        """Corresponds to IDD field `Coefficient1 C1`

        Args:
            value (float): value for IDD Field `Coefficient1 C1`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient1 C1"] = value

    @property
    def coefficient2_c2(self):
        """Get coefficient2_c2.

        Returns:
            float: the value of `coefficient2_c2` or None if not set

        """
        return self["Coefficient2 C2"]

    @coefficient2_c2.setter
    def coefficient2_c2(self, value=None):
        """Corresponds to IDD field `Coefficient2 C2`

        Args:
            value (float): value for IDD Field `Coefficient2 C2`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient2 C2"] = value

    @property
    def coefficient3_c3(self):
        """Get coefficient3_c3.

        Returns:
            float: the value of `coefficient3_c3` or None if not set

        """
        return self["Coefficient3 C3"]

    @coefficient3_c3.setter
    def coefficient3_c3(self, value=None):
        """Corresponds to IDD field `Coefficient3 C3`

        Args:
            value (float): value for IDD Field `Coefficient3 C3`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient3 C3"] = value

    @property
    def coefficient4_c4(self):
        """Get coefficient4_c4.

        Returns:
            float: the value of `coefficient4_c4` or None if not set

        """
        return self["Coefficient4 C4"]

    @coefficient4_c4.setter
    def coefficient4_c4(self, value=None):
        """Corresponds to IDD field `Coefficient4 C4`

        Args:
            value (float): value for IDD Field `Coefficient4 C4`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient4 C4"] = value

    @property
    def minimum_value_of_x(self):
        """Get minimum_value_of_x.

        Returns:
            float: the value of `minimum_value_of_x` or None if not set

        """
        return self["Minimum Value of x"]

    @minimum_value_of_x.setter
    def minimum_value_of_x(self, value=None):
        """Corresponds to IDD field `Minimum Value of x`

        Args:
            value (float): value for IDD Field `Minimum Value of x`
                Units are based on field `A2`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Minimum Value of x"] = value

    @property
    def maximum_value_of_x(self):
        """Get maximum_value_of_x.

        Returns:
            float: the value of `maximum_value_of_x` or None if not set

        """
        return self["Maximum Value of x"]

    @maximum_value_of_x.setter
    def maximum_value_of_x(self, value=None):
        """Corresponds to IDD field `Maximum Value of x`

        Args:
            value (float): value for IDD Field `Maximum Value of x`
                Units are based on field `A2`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Maximum Value of x"] = value

    @property
    def minimum_curve_output(self):
        """Get minimum_curve_output.

        Returns:
            float: the value of `minimum_curve_output` or None if not set

        """
        return self["Minimum Curve Output"]

    @minimum_curve_output.setter
    def minimum_curve_output(self, value=None):
        """Corresponds to IDD field `Minimum Curve Output` Specify the minimum
        value calculated by this curve object.

        Args:
            value (float): value for IDD Field `Minimum Curve Output`
                Units are based on field `A3`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Minimum Curve Output"] = value

    @property
    def maximum_curve_output(self):
        """Get maximum_curve_output.

        Returns:
            float: the value of `maximum_curve_output` or None if not set

        """
        return self["Maximum Curve Output"]

    @maximum_curve_output.setter
    def maximum_curve_output(self, value=None):
        """Corresponds to IDD field `Maximum Curve Output` Specify the maximum
        value calculated by this curve object.

        Args:
            value (float): value for IDD Field `Maximum Curve Output`
                Units are based on field `A3`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Maximum Curve Output"] = value

    @property
    def input_unit_type_for_x(self):
        """Get input_unit_type_for_x.

        Returns:
            str: the value of `input_unit_type_for_x` or None if not set

        """
        return self["Input Unit Type for x"]

    @input_unit_type_for_x.setter
    def input_unit_type_for_x(self, value="Dimensionless"):
        """Corresponds to IDD field `Input Unit Type for x`

        Args:
            value (str): value for IDD Field `Input Unit Type for x`
                Default value: Dimensionless
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Input Unit Type for x"] = value

    @property
    def output_unit_type(self):
        """Get output_unit_type.

        Returns:
            str: the value of `output_unit_type` or None if not set

        """
        return self["Output Unit Type"]

    @output_unit_type.setter
    def output_unit_type(self, value="Dimensionless"):
        """Corresponds to IDD field `Output Unit Type`

        Args:
            value (str): value for IDD Field `Output Unit Type`
                Default value: Dimensionless
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Output Unit Type"] = value




class CurveSigmoid(DataObject):

    """ Corresponds to IDD object `Curve:Sigmoid`
        Sigmoid curve with one independent variable.
        Input consists of the curve name, the five coefficients, and the maximum and minimum
        valid independent variable values. Optional inputs for the curve minimum and maximum
        may be used to limit the output of the performance curve.
        curve = C1+C2/[1+exp((C3-x)/C4)]**C5
    """
    schema = {'min-fields': 0,
              'name': u'Curve:Sigmoid',
              'pyname': u'CurveSigmoid',
              'format': None,
              'fields': OrderedDict([(u'name',
                                      {'name': u'Name',
                                       'pyname': u'name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'alpha'}),
                                     (u'coefficient1 c1',
                                      {'name': u'Coefficient1 C1',
                                       'pyname': u'coefficient1_c1',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient2 c2',
                                      {'name': u'Coefficient2 C2',
                                       'pyname': u'coefficient2_c2',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient3 c3',
                                      {'name': u'Coefficient3 C3',
                                       'pyname': u'coefficient3_c3',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient4 c4',
                                      {'name': u'Coefficient4 C4',
                                       'pyname': u'coefficient4_c4',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient5 c5',
                                      {'name': u'Coefficient5 C5',
                                       'pyname': u'coefficient5_c5',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'minimum value of x',
                                      {'name': u'Minimum Value of x',
                                       'pyname': u'minimum_value_of_x',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'maximum value of x',
                                      {'name': u'Maximum Value of x',
                                       'pyname': u'maximum_value_of_x',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'minimum curve output',
                                      {'name': u'Minimum Curve Output',
                                       'pyname': u'minimum_curve_output',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'maximum curve output',
                                      {'name': u'Maximum Curve Output',
                                       'pyname': u'maximum_curve_output',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'input unit type for x',
                                      {'name': u'Input Unit Type for x',
                                       'pyname': u'input_unit_type_for_x',
                                       'default': u'Dimensionless',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'Dimensionless'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'output unit type',
                                      {'name': u'Output Unit Type',
                                       'pyname': u'output_unit_type',
                                       'default': u'Dimensionless',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'Dimensionless'],
                                       'autocalculatable': False,
                                       'type': 'alpha'})]),
              'extensible-fields': OrderedDict(),
              'unique-object': False,
              'required-object': False,
              'group': u'Performance Curves'}

    @property
    def name(self):
        """Get name.

        Returns:
            str: the value of `name` or None if not set

        """
        return self["Name"]

    @name.setter
    def name(self, value=None):
        """Corresponds to IDD field `Name` See InputOut Reference for curve
        description.

        Args:
            value (str): value for IDD Field `Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Name"] = value

    @property
    def coefficient1_c1(self):
        """Get coefficient1_c1.

        Returns:
            float: the value of `coefficient1_c1` or None if not set

        """
        return self["Coefficient1 C1"]

    @coefficient1_c1.setter
    def coefficient1_c1(self, value=None):
        """Corresponds to IDD field `Coefficient1 C1`

        Args:
            value (float): value for IDD Field `Coefficient1 C1`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient1 C1"] = value

    @property
    def coefficient2_c2(self):
        """Get coefficient2_c2.

        Returns:
            float: the value of `coefficient2_c2` or None if not set

        """
        return self["Coefficient2 C2"]

    @coefficient2_c2.setter
    def coefficient2_c2(self, value=None):
        """Corresponds to IDD field `Coefficient2 C2`

        Args:
            value (float): value for IDD Field `Coefficient2 C2`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient2 C2"] = value

    @property
    def coefficient3_c3(self):
        """Get coefficient3_c3.

        Returns:
            float: the value of `coefficient3_c3` or None if not set

        """
        return self["Coefficient3 C3"]

    @coefficient3_c3.setter
    def coefficient3_c3(self, value=None):
        """Corresponds to IDD field `Coefficient3 C3`

        Args:
            value (float): value for IDD Field `Coefficient3 C3`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient3 C3"] = value

    @property
    def coefficient4_c4(self):
        """Get coefficient4_c4.

        Returns:
            float: the value of `coefficient4_c4` or None if not set

        """
        return self["Coefficient4 C4"]

    @coefficient4_c4.setter
    def coefficient4_c4(self, value=None):
        """Corresponds to IDD field `Coefficient4 C4`

        Args:
            value (float): value for IDD Field `Coefficient4 C4`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient4 C4"] = value

    @property
    def coefficient5_c5(self):
        """Get coefficient5_c5.

        Returns:
            float: the value of `coefficient5_c5` or None if not set

        """
        return self["Coefficient5 C5"]

    @coefficient5_c5.setter
    def coefficient5_c5(self, value=None):
        """Corresponds to IDD field `Coefficient5 C5`

        Args:
            value (float): value for IDD Field `Coefficient5 C5`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient5 C5"] = value

    @property
    def minimum_value_of_x(self):
        """Get minimum_value_of_x.

        Returns:
            float: the value of `minimum_value_of_x` or None if not set

        """
        return self["Minimum Value of x"]

    @minimum_value_of_x.setter
    def minimum_value_of_x(self, value=None):
        """Corresponds to IDD field `Minimum Value of x`

        Args:
            value (float): value for IDD Field `Minimum Value of x`
                Units are based on field `A2`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Minimum Value of x"] = value

    @property
    def maximum_value_of_x(self):
        """Get maximum_value_of_x.

        Returns:
            float: the value of `maximum_value_of_x` or None if not set

        """
        return self["Maximum Value of x"]

    @maximum_value_of_x.setter
    def maximum_value_of_x(self, value=None):
        """Corresponds to IDD field `Maximum Value of x`

        Args:
            value (float): value for IDD Field `Maximum Value of x`
                Units are based on field `A2`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Maximum Value of x"] = value

    @property
    def minimum_curve_output(self):
        """Get minimum_curve_output.

        Returns:
            float: the value of `minimum_curve_output` or None if not set

        """
        return self["Minimum Curve Output"]

    @minimum_curve_output.setter
    def minimum_curve_output(self, value=None):
        """Corresponds to IDD field `Minimum Curve Output` Specify the minimum
        value calculated by this curve object.

        Args:
            value (float): value for IDD Field `Minimum Curve Output`
                Units are based on field `A3`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Minimum Curve Output"] = value

    @property
    def maximum_curve_output(self):
        """Get maximum_curve_output.

        Returns:
            float: the value of `maximum_curve_output` or None if not set

        """
        return self["Maximum Curve Output"]

    @maximum_curve_output.setter
    def maximum_curve_output(self, value=None):
        """Corresponds to IDD field `Maximum Curve Output` Specify the maximum
        value calculated by this curve object.

        Args:
            value (float): value for IDD Field `Maximum Curve Output`
                Units are based on field `A3`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Maximum Curve Output"] = value

    @property
    def input_unit_type_for_x(self):
        """Get input_unit_type_for_x.

        Returns:
            str: the value of `input_unit_type_for_x` or None if not set

        """
        return self["Input Unit Type for x"]

    @input_unit_type_for_x.setter
    def input_unit_type_for_x(self, value="Dimensionless"):
        """Corresponds to IDD field `Input Unit Type for x`

        Args:
            value (str): value for IDD Field `Input Unit Type for x`
                Default value: Dimensionless
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Input Unit Type for x"] = value

    @property
    def output_unit_type(self):
        """Get output_unit_type.

        Returns:
            str: the value of `output_unit_type` or None if not set

        """
        return self["Output Unit Type"]

    @output_unit_type.setter
    def output_unit_type(self, value="Dimensionless"):
        """Corresponds to IDD field `Output Unit Type`

        Args:
            value (str): value for IDD Field `Output Unit Type`
                Default value: Dimensionless
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Output Unit Type"] = value




class CurveRectangularHyperbola1(DataObject):

    """ Corresponds to IDD object `Curve:RectangularHyperbola1`
        Rectangular hyperbola type 1 curve with one independent variable.
        Input consists of the curve name, the three coefficients, and the maximum and
        minimum valid independent variable values. Optional inputs for the curve minimum and
        maximum may be used to limit the output of the performance curve.
        curve = ((C1*x)/(C2+x))+C3
    """
    schema = {'min-fields': 0,
              'name': u'Curve:RectangularHyperbola1',
              'pyname': u'CurveRectangularHyperbola1',
              'format': None,
              'fields': OrderedDict([(u'name',
                                      {'name': u'Name',
                                       'pyname': u'name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'alpha'}),
                                     (u'coefficient1 c1',
                                      {'name': u'Coefficient1 C1',
                                       'pyname': u'coefficient1_c1',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient2 c2',
                                      {'name': u'Coefficient2 C2',
                                       'pyname': u'coefficient2_c2',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient3 c3',
                                      {'name': u'Coefficient3 C3',
                                       'pyname': u'coefficient3_c3',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'minimum value of x',
                                      {'name': u'Minimum Value of x',
                                       'pyname': u'minimum_value_of_x',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'maximum value of x',
                                      {'name': u'Maximum Value of x',
                                       'pyname': u'maximum_value_of_x',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'minimum curve output',
                                      {'name': u'Minimum Curve Output',
                                       'pyname': u'minimum_curve_output',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'maximum curve output',
                                      {'name': u'Maximum Curve Output',
                                       'pyname': u'maximum_curve_output',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'input unit type for x',
                                      {'name': u'Input Unit Type for x',
                                       'pyname': u'input_unit_type_for_x',
                                       'default': u'Dimensionless',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'Dimensionless'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'output unit type',
                                      {'name': u'Output Unit Type',
                                       'pyname': u'output_unit_type',
                                       'default': u'Dimensionless',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'Dimensionless'],
                                       'autocalculatable': False,
                                       'type': 'alpha'})]),
              'extensible-fields': OrderedDict(),
              'unique-object': False,
              'required-object': False,
              'group': u'Performance Curves'}

    @property
    def name(self):
        """Get name.

        Returns:
            str: the value of `name` or None if not set

        """
        return self["Name"]

    @name.setter
    def name(self, value=None):
        """Corresponds to IDD field `Name`

        Args:
            value (str): value for IDD Field `Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Name"] = value

    @property
    def coefficient1_c1(self):
        """Get coefficient1_c1.

        Returns:
            float: the value of `coefficient1_c1` or None if not set

        """
        return self["Coefficient1 C1"]

    @coefficient1_c1.setter
    def coefficient1_c1(self, value=None):
        """Corresponds to IDD field `Coefficient1 C1`

        Args:
            value (float): value for IDD Field `Coefficient1 C1`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient1 C1"] = value

    @property
    def coefficient2_c2(self):
        """Get coefficient2_c2.

        Returns:
            float: the value of `coefficient2_c2` or None if not set

        """
        return self["Coefficient2 C2"]

    @coefficient2_c2.setter
    def coefficient2_c2(self, value=None):
        """Corresponds to IDD field `Coefficient2 C2`

        Args:
            value (float): value for IDD Field `Coefficient2 C2`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient2 C2"] = value

    @property
    def coefficient3_c3(self):
        """Get coefficient3_c3.

        Returns:
            float: the value of `coefficient3_c3` or None if not set

        """
        return self["Coefficient3 C3"]

    @coefficient3_c3.setter
    def coefficient3_c3(self, value=None):
        """Corresponds to IDD field `Coefficient3 C3`

        Args:
            value (float): value for IDD Field `Coefficient3 C3`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient3 C3"] = value

    @property
    def minimum_value_of_x(self):
        """Get minimum_value_of_x.

        Returns:
            float: the value of `minimum_value_of_x` or None if not set

        """
        return self["Minimum Value of x"]

    @minimum_value_of_x.setter
    def minimum_value_of_x(self, value=None):
        """Corresponds to IDD field `Minimum Value of x`

        Args:
            value (float): value for IDD Field `Minimum Value of x`
                Units are based on field `A2`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Minimum Value of x"] = value

    @property
    def maximum_value_of_x(self):
        """Get maximum_value_of_x.

        Returns:
            float: the value of `maximum_value_of_x` or None if not set

        """
        return self["Maximum Value of x"]

    @maximum_value_of_x.setter
    def maximum_value_of_x(self, value=None):
        """Corresponds to IDD field `Maximum Value of x`

        Args:
            value (float): value for IDD Field `Maximum Value of x`
                Units are based on field `A2`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Maximum Value of x"] = value

    @property
    def minimum_curve_output(self):
        """Get minimum_curve_output.

        Returns:
            float: the value of `minimum_curve_output` or None if not set

        """
        return self["Minimum Curve Output"]

    @minimum_curve_output.setter
    def minimum_curve_output(self, value=None):
        """Corresponds to IDD field `Minimum Curve Output` Specify the minimum
        value calculated by this curve object.

        Args:
            value (float): value for IDD Field `Minimum Curve Output`
                Units are based on field `A3`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Minimum Curve Output"] = value

    @property
    def maximum_curve_output(self):
        """Get maximum_curve_output.

        Returns:
            float: the value of `maximum_curve_output` or None if not set

        """
        return self["Maximum Curve Output"]

    @maximum_curve_output.setter
    def maximum_curve_output(self, value=None):
        """Corresponds to IDD field `Maximum Curve Output` Specify the maximum
        value calculated by this curve object.

        Args:
            value (float): value for IDD Field `Maximum Curve Output`
                Units are based on field `A3`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Maximum Curve Output"] = value

    @property
    def input_unit_type_for_x(self):
        """Get input_unit_type_for_x.

        Returns:
            str: the value of `input_unit_type_for_x` or None if not set

        """
        return self["Input Unit Type for x"]

    @input_unit_type_for_x.setter
    def input_unit_type_for_x(self, value="Dimensionless"):
        """Corresponds to IDD field `Input Unit Type for x`

        Args:
            value (str): value for IDD Field `Input Unit Type for x`
                Default value: Dimensionless
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Input Unit Type for x"] = value

    @property
    def output_unit_type(self):
        """Get output_unit_type.

        Returns:
            str: the value of `output_unit_type` or None if not set

        """
        return self["Output Unit Type"]

    @output_unit_type.setter
    def output_unit_type(self, value="Dimensionless"):
        """Corresponds to IDD field `Output Unit Type`

        Args:
            value (str): value for IDD Field `Output Unit Type`
                Default value: Dimensionless
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Output Unit Type"] = value




class CurveRectangularHyperbola2(DataObject):

    """ Corresponds to IDD object `Curve:RectangularHyperbola2`
        Rectangular hyperbola type 2 curve with one independent variable.
        Input consists of the curve name, the three coefficients, and the maximum and
        minimum valid independent variable values. Optional inputs for the curve minimum and
        maximum may be used to limit the output of the performance curve.
        curve = ((C1*x)/(C2+x))+(C3*x)
    """
    schema = {'min-fields': 0,
              'name': u'Curve:RectangularHyperbola2',
              'pyname': u'CurveRectangularHyperbola2',
              'format': None,
              'fields': OrderedDict([(u'name',
                                      {'name': u'Name',
                                       'pyname': u'name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'alpha'}),
                                     (u'coefficient1 c1',
                                      {'name': u'Coefficient1 C1',
                                       'pyname': u'coefficient1_c1',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient2 c2',
                                      {'name': u'Coefficient2 C2',
                                       'pyname': u'coefficient2_c2',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient3 c3',
                                      {'name': u'Coefficient3 C3',
                                       'pyname': u'coefficient3_c3',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'minimum value of x',
                                      {'name': u'Minimum Value of x',
                                       'pyname': u'minimum_value_of_x',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'maximum value of x',
                                      {'name': u'Maximum Value of x',
                                       'pyname': u'maximum_value_of_x',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'minimum curve output',
                                      {'name': u'Minimum Curve Output',
                                       'pyname': u'minimum_curve_output',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'maximum curve output',
                                      {'name': u'Maximum Curve Output',
                                       'pyname': u'maximum_curve_output',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'input unit type for x',
                                      {'name': u'Input Unit Type for x',
                                       'pyname': u'input_unit_type_for_x',
                                       'default': u'Dimensionless',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'Dimensionless'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'output unit type',
                                      {'name': u'Output Unit Type',
                                       'pyname': u'output_unit_type',
                                       'default': u'Dimensionless',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'Dimensionless'],
                                       'autocalculatable': False,
                                       'type': 'alpha'})]),
              'extensible-fields': OrderedDict(),
              'unique-object': False,
              'required-object': False,
              'group': u'Performance Curves'}

    @property
    def name(self):
        """Get name.

        Returns:
            str: the value of `name` or None if not set

        """
        return self["Name"]

    @name.setter
    def name(self, value=None):
        """Corresponds to IDD field `Name`

        Args:
            value (str): value for IDD Field `Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Name"] = value

    @property
    def coefficient1_c1(self):
        """Get coefficient1_c1.

        Returns:
            float: the value of `coefficient1_c1` or None if not set

        """
        return self["Coefficient1 C1"]

    @coefficient1_c1.setter
    def coefficient1_c1(self, value=None):
        """Corresponds to IDD field `Coefficient1 C1`

        Args:
            value (float): value for IDD Field `Coefficient1 C1`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient1 C1"] = value

    @property
    def coefficient2_c2(self):
        """Get coefficient2_c2.

        Returns:
            float: the value of `coefficient2_c2` or None if not set

        """
        return self["Coefficient2 C2"]

    @coefficient2_c2.setter
    def coefficient2_c2(self, value=None):
        """Corresponds to IDD field `Coefficient2 C2`

        Args:
            value (float): value for IDD Field `Coefficient2 C2`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient2 C2"] = value

    @property
    def coefficient3_c3(self):
        """Get coefficient3_c3.

        Returns:
            float: the value of `coefficient3_c3` or None if not set

        """
        return self["Coefficient3 C3"]

    @coefficient3_c3.setter
    def coefficient3_c3(self, value=None):
        """Corresponds to IDD field `Coefficient3 C3`

        Args:
            value (float): value for IDD Field `Coefficient3 C3`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient3 C3"] = value

    @property
    def minimum_value_of_x(self):
        """Get minimum_value_of_x.

        Returns:
            float: the value of `minimum_value_of_x` or None if not set

        """
        return self["Minimum Value of x"]

    @minimum_value_of_x.setter
    def minimum_value_of_x(self, value=None):
        """Corresponds to IDD field `Minimum Value of x`

        Args:
            value (float): value for IDD Field `Minimum Value of x`
                Units are based on field `A2`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Minimum Value of x"] = value

    @property
    def maximum_value_of_x(self):
        """Get maximum_value_of_x.

        Returns:
            float: the value of `maximum_value_of_x` or None if not set

        """
        return self["Maximum Value of x"]

    @maximum_value_of_x.setter
    def maximum_value_of_x(self, value=None):
        """Corresponds to IDD field `Maximum Value of x`

        Args:
            value (float): value for IDD Field `Maximum Value of x`
                Units are based on field `A2`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Maximum Value of x"] = value

    @property
    def minimum_curve_output(self):
        """Get minimum_curve_output.

        Returns:
            float: the value of `minimum_curve_output` or None if not set

        """
        return self["Minimum Curve Output"]

    @minimum_curve_output.setter
    def minimum_curve_output(self, value=None):
        """Corresponds to IDD field `Minimum Curve Output` Specify the minimum
        value calculated by this curve object.

        Args:
            value (float): value for IDD Field `Minimum Curve Output`
                Units are based on field `A3`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Minimum Curve Output"] = value

    @property
    def maximum_curve_output(self):
        """Get maximum_curve_output.

        Returns:
            float: the value of `maximum_curve_output` or None if not set

        """
        return self["Maximum Curve Output"]

    @maximum_curve_output.setter
    def maximum_curve_output(self, value=None):
        """Corresponds to IDD field `Maximum Curve Output` Specify the maximum
        value calculated by this curve object.

        Args:
            value (float): value for IDD Field `Maximum Curve Output`
                Units are based on field `A3`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Maximum Curve Output"] = value

    @property
    def input_unit_type_for_x(self):
        """Get input_unit_type_for_x.

        Returns:
            str: the value of `input_unit_type_for_x` or None if not set

        """
        return self["Input Unit Type for x"]

    @input_unit_type_for_x.setter
    def input_unit_type_for_x(self, value="Dimensionless"):
        """Corresponds to IDD field `Input Unit Type for x`

        Args:
            value (str): value for IDD Field `Input Unit Type for x`
                Default value: Dimensionless
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Input Unit Type for x"] = value

    @property
    def output_unit_type(self):
        """Get output_unit_type.

        Returns:
            str: the value of `output_unit_type` or None if not set

        """
        return self["Output Unit Type"]

    @output_unit_type.setter
    def output_unit_type(self, value="Dimensionless"):
        """Corresponds to IDD field `Output Unit Type`

        Args:
            value (str): value for IDD Field `Output Unit Type`
                Default value: Dimensionless
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Output Unit Type"] = value




class CurveExponentialDecay(DataObject):

    """ Corresponds to IDD object `Curve:ExponentialDecay`
        Exponential decay curve with one independent variable.
        Input consists of the curve name, the three coefficients, and the maximum and minimum
        valid independent variable values. Optional inputs for the curve minimum and
        maximum may be used to limit the output of the performance curve.
        curve = C1+C2*exp(C3*x)
    """
    schema = {'min-fields': 0,
              'name': u'Curve:ExponentialDecay',
              'pyname': u'CurveExponentialDecay',
              'format': None,
              'fields': OrderedDict([(u'name',
                                      {'name': u'Name',
                                       'pyname': u'name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'alpha'}),
                                     (u'coefficient1 c1',
                                      {'name': u'Coefficient1 C1',
                                       'pyname': u'coefficient1_c1',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient2 c2',
                                      {'name': u'Coefficient2 C2',
                                       'pyname': u'coefficient2_c2',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient3 c3',
                                      {'name': u'Coefficient3 C3',
                                       'pyname': u'coefficient3_c3',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'minimum value of x',
                                      {'name': u'Minimum Value of x',
                                       'pyname': u'minimum_value_of_x',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'maximum value of x',
                                      {'name': u'Maximum Value of x',
                                       'pyname': u'maximum_value_of_x',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'minimum curve output',
                                      {'name': u'Minimum Curve Output',
                                       'pyname': u'minimum_curve_output',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'maximum curve output',
                                      {'name': u'Maximum Curve Output',
                                       'pyname': u'maximum_curve_output',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'input unit type for x',
                                      {'name': u'Input Unit Type for x',
                                       'pyname': u'input_unit_type_for_x',
                                       'default': u'Dimensionless',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'Dimensionless'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'output unit type',
                                      {'name': u'Output Unit Type',
                                       'pyname': u'output_unit_type',
                                       'default': u'Dimensionless',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'Dimensionless'],
                                       'autocalculatable': False,
                                       'type': 'alpha'})]),
              'extensible-fields': OrderedDict(),
              'unique-object': False,
              'required-object': False,
              'group': u'Performance Curves'}

    @property
    def name(self):
        """Get name.

        Returns:
            str: the value of `name` or None if not set

        """
        return self["Name"]

    @name.setter
    def name(self, value=None):
        """Corresponds to IDD field `Name`

        Args:
            value (str): value for IDD Field `Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Name"] = value

    @property
    def coefficient1_c1(self):
        """Get coefficient1_c1.

        Returns:
            float: the value of `coefficient1_c1` or None if not set

        """
        return self["Coefficient1 C1"]

    @coefficient1_c1.setter
    def coefficient1_c1(self, value=None):
        """Corresponds to IDD field `Coefficient1 C1`

        Args:
            value (float): value for IDD Field `Coefficient1 C1`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient1 C1"] = value

    @property
    def coefficient2_c2(self):
        """Get coefficient2_c2.

        Returns:
            float: the value of `coefficient2_c2` or None if not set

        """
        return self["Coefficient2 C2"]

    @coefficient2_c2.setter
    def coefficient2_c2(self, value=None):
        """Corresponds to IDD field `Coefficient2 C2`

        Args:
            value (float): value for IDD Field `Coefficient2 C2`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient2 C2"] = value

    @property
    def coefficient3_c3(self):
        """Get coefficient3_c3.

        Returns:
            float: the value of `coefficient3_c3` or None if not set

        """
        return self["Coefficient3 C3"]

    @coefficient3_c3.setter
    def coefficient3_c3(self, value=None):
        """Corresponds to IDD field `Coefficient3 C3`

        Args:
            value (float): value for IDD Field `Coefficient3 C3`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient3 C3"] = value

    @property
    def minimum_value_of_x(self):
        """Get minimum_value_of_x.

        Returns:
            float: the value of `minimum_value_of_x` or None if not set

        """
        return self["Minimum Value of x"]

    @minimum_value_of_x.setter
    def minimum_value_of_x(self, value=None):
        """Corresponds to IDD field `Minimum Value of x`

        Args:
            value (float): value for IDD Field `Minimum Value of x`
                Units are based on field `A2`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Minimum Value of x"] = value

    @property
    def maximum_value_of_x(self):
        """Get maximum_value_of_x.

        Returns:
            float: the value of `maximum_value_of_x` or None if not set

        """
        return self["Maximum Value of x"]

    @maximum_value_of_x.setter
    def maximum_value_of_x(self, value=None):
        """Corresponds to IDD field `Maximum Value of x`

        Args:
            value (float): value for IDD Field `Maximum Value of x`
                Units are based on field `A2`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Maximum Value of x"] = value

    @property
    def minimum_curve_output(self):
        """Get minimum_curve_output.

        Returns:
            float: the value of `minimum_curve_output` or None if not set

        """
        return self["Minimum Curve Output"]

    @minimum_curve_output.setter
    def minimum_curve_output(self, value=None):
        """Corresponds to IDD field `Minimum Curve Output` Specify the minimum
        value calculated by this curve object.

        Args:
            value (float): value for IDD Field `Minimum Curve Output`
                Units are based on field `A3`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Minimum Curve Output"] = value

    @property
    def maximum_curve_output(self):
        """Get maximum_curve_output.

        Returns:
            float: the value of `maximum_curve_output` or None if not set

        """
        return self["Maximum Curve Output"]

    @maximum_curve_output.setter
    def maximum_curve_output(self, value=None):
        """Corresponds to IDD field `Maximum Curve Output` Specify the maximum
        value calculated by this curve object.

        Args:
            value (float): value for IDD Field `Maximum Curve Output`
                Units are based on field `A3`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Maximum Curve Output"] = value

    @property
    def input_unit_type_for_x(self):
        """Get input_unit_type_for_x.

        Returns:
            str: the value of `input_unit_type_for_x` or None if not set

        """
        return self["Input Unit Type for x"]

    @input_unit_type_for_x.setter
    def input_unit_type_for_x(self, value="Dimensionless"):
        """Corresponds to IDD field `Input Unit Type for x`

        Args:
            value (str): value for IDD Field `Input Unit Type for x`
                Default value: Dimensionless
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Input Unit Type for x"] = value

    @property
    def output_unit_type(self):
        """Get output_unit_type.

        Returns:
            str: the value of `output_unit_type` or None if not set

        """
        return self["Output Unit Type"]

    @output_unit_type.setter
    def output_unit_type(self, value="Dimensionless"):
        """Corresponds to IDD field `Output Unit Type`

        Args:
            value (str): value for IDD Field `Output Unit Type`
                Default value: Dimensionless
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Output Unit Type"] = value




class CurveDoubleExponentialDecay(DataObject):

    """ Corresponds to IDD object `Curve:DoubleExponentialDecay`
        Double exponential decay curve with one independent variable.
        Input consists of the curve name, the five coefficients, and the maximum and minimum
        valid independent variable values. Optional inputs for the curve minimum and
        maximum may be used to limit the output of the performance curve.
        curve = C1+C2*exp(C3*x)+C4*exp(C5*x)
    """
    schema = {'min-fields': 0,
              'name': u'Curve:DoubleExponentialDecay',
              'pyname': u'CurveDoubleExponentialDecay',
              'format': None,
              'fields': OrderedDict([(u'name',
                                      {'name': u'Name',
                                       'pyname': u'name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'alpha'}),
                                     (u'coefficient1 c1',
                                      {'name': u'Coefficient1 C1',
                                       'pyname': u'coefficient1_c1',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient2 c2',
                                      {'name': u'Coefficient2 C2',
                                       'pyname': u'coefficient2_c2',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient3 c3',
                                      {'name': u'Coefficient3 C3',
                                       'pyname': u'coefficient3_c3',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient3 c4',
                                      {'name': u'Coefficient3 C4',
                                       'pyname': u'coefficient3_c4',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient3 c5',
                                      {'name': u'Coefficient3 C5',
                                       'pyname': u'coefficient3_c5',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'minimum value of x',
                                      {'name': u'Minimum Value of x',
                                       'pyname': u'minimum_value_of_x',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'maximum value of x',
                                      {'name': u'Maximum Value of x',
                                       'pyname': u'maximum_value_of_x',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'minimum curve output',
                                      {'name': u'Minimum Curve Output',
                                       'pyname': u'minimum_curve_output',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'maximum curve output',
                                      {'name': u'Maximum Curve Output',
                                       'pyname': u'maximum_curve_output',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'input unit type for x',
                                      {'name': u'Input Unit Type for x',
                                       'pyname': u'input_unit_type_for_x',
                                       'default': u'Dimensionless',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'Dimensionless'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'output unit type',
                                      {'name': u'Output Unit Type',
                                       'pyname': u'output_unit_type',
                                       'default': u'Dimensionless',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'Dimensionless'],
                                       'autocalculatable': False,
                                       'type': 'alpha'})]),
              'extensible-fields': OrderedDict(),
              'unique-object': False,
              'required-object': False,
              'group': u'Performance Curves'}

    @property
    def name(self):
        """Get name.

        Returns:
            str: the value of `name` or None if not set

        """
        return self["Name"]

    @name.setter
    def name(self, value=None):
        """Corresponds to IDD field `Name`

        Args:
            value (str): value for IDD Field `Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Name"] = value

    @property
    def coefficient1_c1(self):
        """Get coefficient1_c1.

        Returns:
            float: the value of `coefficient1_c1` or None if not set

        """
        return self["Coefficient1 C1"]

    @coefficient1_c1.setter
    def coefficient1_c1(self, value=None):
        """Corresponds to IDD field `Coefficient1 C1`

        Args:
            value (float): value for IDD Field `Coefficient1 C1`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient1 C1"] = value

    @property
    def coefficient2_c2(self):
        """Get coefficient2_c2.

        Returns:
            float: the value of `coefficient2_c2` or None if not set

        """
        return self["Coefficient2 C2"]

    @coefficient2_c2.setter
    def coefficient2_c2(self, value=None):
        """Corresponds to IDD field `Coefficient2 C2`

        Args:
            value (float): value for IDD Field `Coefficient2 C2`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient2 C2"] = value

    @property
    def coefficient3_c3(self):
        """Get coefficient3_c3.

        Returns:
            float: the value of `coefficient3_c3` or None if not set

        """
        return self["Coefficient3 C3"]

    @coefficient3_c3.setter
    def coefficient3_c3(self, value=None):
        """Corresponds to IDD field `Coefficient3 C3`

        Args:
            value (float): value for IDD Field `Coefficient3 C3`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient3 C3"] = value

    @property
    def coefficient3_c4(self):
        """Get coefficient3_c4.

        Returns:
            float: the value of `coefficient3_c4` or None if not set

        """
        return self["Coefficient3 C4"]

    @coefficient3_c4.setter
    def coefficient3_c4(self, value=None):
        """Corresponds to IDD field `Coefficient3 C4`

        Args:
            value (float): value for IDD Field `Coefficient3 C4`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient3 C4"] = value

    @property
    def coefficient3_c5(self):
        """Get coefficient3_c5.

        Returns:
            float: the value of `coefficient3_c5` or None if not set

        """
        return self["Coefficient3 C5"]

    @coefficient3_c5.setter
    def coefficient3_c5(self, value=None):
        """Corresponds to IDD field `Coefficient3 C5`

        Args:
            value (float): value for IDD Field `Coefficient3 C5`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient3 C5"] = value

    @property
    def minimum_value_of_x(self):
        """Get minimum_value_of_x.

        Returns:
            float: the value of `minimum_value_of_x` or None if not set

        """
        return self["Minimum Value of x"]

    @minimum_value_of_x.setter
    def minimum_value_of_x(self, value=None):
        """Corresponds to IDD field `Minimum Value of x`

        Args:
            value (float): value for IDD Field `Minimum Value of x`
                Units are based on field `A2`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Minimum Value of x"] = value

    @property
    def maximum_value_of_x(self):
        """Get maximum_value_of_x.

        Returns:
            float: the value of `maximum_value_of_x` or None if not set

        """
        return self["Maximum Value of x"]

    @maximum_value_of_x.setter
    def maximum_value_of_x(self, value=None):
        """Corresponds to IDD field `Maximum Value of x`

        Args:
            value (float): value for IDD Field `Maximum Value of x`
                Units are based on field `A2`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Maximum Value of x"] = value

    @property
    def minimum_curve_output(self):
        """Get minimum_curve_output.

        Returns:
            float: the value of `minimum_curve_output` or None if not set

        """
        return self["Minimum Curve Output"]

    @minimum_curve_output.setter
    def minimum_curve_output(self, value=None):
        """Corresponds to IDD field `Minimum Curve Output` Specify the minimum
        value calculated by this curve object.

        Args:
            value (float): value for IDD Field `Minimum Curve Output`
                Units are based on field `A3`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Minimum Curve Output"] = value

    @property
    def maximum_curve_output(self):
        """Get maximum_curve_output.

        Returns:
            float: the value of `maximum_curve_output` or None if not set

        """
        return self["Maximum Curve Output"]

    @maximum_curve_output.setter
    def maximum_curve_output(self, value=None):
        """Corresponds to IDD field `Maximum Curve Output` Specify the maximum
        value calculated by this curve object.

        Args:
            value (float): value for IDD Field `Maximum Curve Output`
                Units are based on field `A3`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Maximum Curve Output"] = value

    @property
    def input_unit_type_for_x(self):
        """Get input_unit_type_for_x.

        Returns:
            str: the value of `input_unit_type_for_x` or None if not set

        """
        return self["Input Unit Type for x"]

    @input_unit_type_for_x.setter
    def input_unit_type_for_x(self, value="Dimensionless"):
        """Corresponds to IDD field `Input Unit Type for x`

        Args:
            value (str): value for IDD Field `Input Unit Type for x`
                Default value: Dimensionless
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Input Unit Type for x"] = value

    @property
    def output_unit_type(self):
        """Get output_unit_type.

        Returns:
            str: the value of `output_unit_type` or None if not set

        """
        return self["Output Unit Type"]

    @output_unit_type.setter
    def output_unit_type(self, value="Dimensionless"):
        """Corresponds to IDD field `Output Unit Type`

        Args:
            value (str): value for IDD Field `Output Unit Type`
                Default value: Dimensionless
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Output Unit Type"] = value


