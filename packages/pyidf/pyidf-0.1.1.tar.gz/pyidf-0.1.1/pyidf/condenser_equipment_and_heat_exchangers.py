""" Data objects in group "Condenser Equipment and Heat Exchangers"
"""

from collections import OrderedDict
import logging
from pyidf.helper import DataObject

logger = logging.getLogger("pyidf")
logger.addHandler(logging.NullHandler())



class CoolingTowerSingleSpeed(DataObject):

    """ Corresponds to IDD object `CoolingTower:SingleSpeed`
        This tower model is based on Merkel's theory, which is also the basis
        for the tower model in ASHRAE's HVAC1 Toolkit. The closed-circuit cooling tower
        is modeled as a counter flow heat exchanger with a single-speed fan drawing air
        through the tower (induced-draft configuration).
        Added fluid bypass as an additional capacity control. 8/2008.
        For a multi-cell tower, the capacity and air/water flow rate inputs are for the entire tower.
    """
    schema = {'extensible-fields': OrderedDict(),
              'fields': OrderedDict([(u'name',
                                      {'name': u'Name',
                                       'pyname': u'name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'alpha'}),
                                     (u'water inlet node name',
                                      {'name': u'Water Inlet Node Name',
                                       'pyname': u'water_inlet_node_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'node'}),
                                     (u'water outlet node name',
                                      {'name': u'Water Outlet Node Name',
                                       'pyname': u'water_outlet_node_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'node'}),
                                     (u'design water flow rate',
                                      {'name': u'Design Water Flow Rate',
                                       'pyname': u'design_water_flow_rate',
                                       'minimum>': 0.0,
                                       'required-field': False,
                                       'autosizable': True,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'm3/s'}),
                                     (u'design air flow rate',
                                      {'name': u'Design Air Flow Rate',
                                       'pyname': u'design_air_flow_rate',
                                       'minimum>': 0.0,
                                       'required-field': True,
                                       'autosizable': True,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'm3/s'}),
                                     (u'design fan power',
                                      {'name': u'Design Fan Power',
                                       'pyname': u'design_fan_power',
                                       'minimum>': 0.0,
                                       'required-field': True,
                                       'autosizable': True,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'W'}),
                                     (u'design u-factor times area value',
                                      {'name': u'Design U-Factor Times Area Value',
                                       'pyname': u'design_ufactor_times_area_value',
                                       'minimum>': 0.0,
                                       'maximum': 2100000.0,
                                       'required-field': False,
                                       'autosizable': True,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'W/K'}),
                                     (u'free convection air flow rate',
                                      {'name': u'Free Convection Air Flow Rate',
                                       'pyname': u'free_convection_air_flow_rate',
                                       'default': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': True,
                                       'type': u'real',
                                       'unit': u'm3/s'}),
                                     (u'free convection air flow rate sizing factor',
                                      {'name': u'Free Convection Air Flow Rate Sizing Factor',
                                       'pyname': u'free_convection_air_flow_rate_sizing_factor',
                                       'default': 0.1,
                                       'minimum>': 0.0,
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'maximum<': 1.0}),
                                     (u'free convection u-factor times area value',
                                      {'name': u'Free Convection U-Factor Times Area Value',
                                       'pyname': u'free_convection_ufactor_times_area_value',
                                       'default': 0.0,
                                       'maximum': 300000.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': True,
                                       'type': u'real',
                                       'unit': u'W/K'}),
                                     (u'free convection u-factor times area value sizing factor',
                                      {'name': u'Free Convection U-Factor Times Area Value Sizing Factor',
                                       'pyname': u'free_convection_ufactor_times_area_value_sizing_factor',
                                       'default': 0.1,
                                       'minimum>': 0.0,
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'maximum<': 1.0}),
                                     (u'performance input method',
                                      {'name': u'Performance Input Method',
                                       'pyname': u'performance_input_method',
                                       'default': u'UFactorTimesAreaAndDesignWaterFlowRate',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'UFactorTimesAreaAndDesignWaterFlowRate',
                                                           u'NominalCapacity'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'heat rejection capacity and nominal capacity sizing ratio',
                                      {'name': u'Heat Rejection Capacity and Nominal Capacity Sizing Ratio',
                                       'pyname': u'heat_rejection_capacity_and_nominal_capacity_sizing_ratio',
                                       'default': 1.25,
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'nominal capacity',
                                      {'name': u'Nominal Capacity',
                                       'pyname': u'nominal_capacity',
                                       'minimum>': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'W'}),
                                     (u'free convection capacity',
                                      {'name': u'Free Convection Capacity',
                                       'pyname': u'free_convection_capacity',
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': True,
                                       'type': u'real',
                                       'unit': u'W'}),
                                     (u'free convection nominal capacity sizing factor',
                                      {'name': u'Free Convection Nominal Capacity Sizing Factor',
                                       'pyname': u'free_convection_nominal_capacity_sizing_factor',
                                       'default': 0.1,
                                       'minimum>': 0.0,
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'maximum<': 1.0}),
                                     (u'basin heater capacity',
                                      {'name': u'Basin Heater Capacity',
                                       'pyname': u'basin_heater_capacity',
                                       'default': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'W/K'}),
                                     (u'basin heater setpoint temperature',
                                      {'name': u'Basin Heater Setpoint Temperature',
                                       'pyname': u'basin_heater_setpoint_temperature',
                                       'default': 2.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 2.0,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'C'}),
                                     (u'basin heater operating schedule name',
                                      {'name': u'Basin Heater Operating Schedule Name',
                                       'pyname': u'basin_heater_operating_schedule_name',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'evaporation loss mode',
                                      {'name': u'Evaporation Loss Mode',
                                       'pyname': u'evaporation_loss_mode',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'LossFactor',
                                                           u'SaturatedExit'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'evaporation loss factor',
                                      {'name': u'Evaporation Loss Factor',
                                       'pyname': u'evaporation_loss_factor',
                                       'default': 0.2,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'percent/K'}),
                                     (u'drift loss percent',
                                      {'name': u'Drift Loss Percent',
                                       'pyname': u'drift_loss_percent',
                                       'default': 0.008,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'percent'}),
                                     (u'blowdown calculation mode',
                                      {'name': u'Blowdown Calculation Mode',
                                       'pyname': u'blowdown_calculation_mode',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'ConcentrationRatio',
                                                           u'ScheduledRate'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'blowdown concentration ratio',
                                      {'name': u'Blowdown Concentration Ratio',
                                       'pyname': u'blowdown_concentration_ratio',
                                       'default': 3.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 2.0,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'blowdown makeup water usage schedule name',
                                      {'name': u'Blowdown Makeup Water Usage Schedule Name',
                                       'pyname': u'blowdown_makeup_water_usage_schedule_name',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'supply water storage tank name',
                                      {'name': u'Supply Water Storage Tank Name',
                                       'pyname': u'supply_water_storage_tank_name',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'outdoor air inlet node name',
                                      {'name': u'Outdoor Air Inlet Node Name',
                                       'pyname': u'outdoor_air_inlet_node_name',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'node'}),
                                     (u'capacity control',
                                      {'name': u'Capacity Control',
                                       'pyname': u'capacity_control',
                                       'default': u'FanCycling',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'FanCycling',
                                                           u'FluidBypass'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'number of cells',
                                      {'name': u'Number of Cells',
                                       'pyname': u'number_of_cells',
                                       'default': 1,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 1,
                                       'autocalculatable': False,
                                       'type': u'integer'}),
                                     (u'cell control',
                                      {'name': u'Cell Control',
                                       'pyname': u'cell_control',
                                       'default': u'MinimalCell',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'MinimalCell',
                                                           u'MaximalCell'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'cell minimum  water flow rate fraction',
                                      {'name': u'Cell Minimum  Water Flow Rate Fraction',
                                       'pyname': u'cell_minimum_water_flow_rate_fraction',
                                       'default': 0.33,
                                       'minimum>': 0.0,
                                       'maximum': 1.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'cell maximum water flow rate fraction',
                                      {'name': u'Cell Maximum Water Flow Rate Fraction',
                                       'pyname': u'cell_maximum_water_flow_rate_fraction',
                                       'default': 2.5,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 1.0,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'sizing factor',
                                      {'name': u'Sizing Factor',
                                       'pyname': u'sizing_factor',
                                       'default': 1.0,
                                       'minimum>': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'})]),
              'format': None,
              'group': u'Condenser Equipment and Heat Exchangers',
              'min-fields': 16,
              'name': u'CoolingTower:SingleSpeed',
              'pyname': u'CoolingTowerSingleSpeed',
              'required-object': False,
              'unique-object': False}

    @property
    def name(self):
        """Get name.

        Returns:
            str: the value of `name` or None if not set

        """
        return self["Name"]

    @name.setter
    def name(self, value=None):
        """Corresponds to IDD field `Name` Tower Name.

        Args:
            value (str): value for IDD Field `Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Name"] = value

    @property
    def water_inlet_node_name(self):
        """Get water_inlet_node_name.

        Returns:
            str: the value of `water_inlet_node_name` or None if not set

        """
        return self["Water Inlet Node Name"]

    @water_inlet_node_name.setter
    def water_inlet_node_name(self, value=None):
        """Corresponds to IDD field `Water Inlet Node Name` Name of tower water
        inlet node.

        Args:
            value (str): value for IDD Field `Water Inlet Node Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Water Inlet Node Name"] = value

    @property
    def water_outlet_node_name(self):
        """Get water_outlet_node_name.

        Returns:
            str: the value of `water_outlet_node_name` or None if not set

        """
        return self["Water Outlet Node Name"]

    @water_outlet_node_name.setter
    def water_outlet_node_name(self, value=None):
        """Corresponds to IDD field `Water Outlet Node Name` Name of tower
        water outlet node.

        Args:
            value (str): value for IDD Field `Water Outlet Node Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Water Outlet Node Name"] = value

    @property
    def design_water_flow_rate(self):
        """Get design_water_flow_rate.

        Returns:
            float: the value of `design_water_flow_rate` or None if not set

        """
        return self["Design Water Flow Rate"]

    @design_water_flow_rate.setter
    def design_water_flow_rate(self, value=None):
        """Corresponds to IDD field `Design Water Flow Rate` Leave field blank
        if tower performance input method is NominalCapacity.

        Args:
            value (float or "Autosize"): value for IDD Field `Design Water Flow Rate`
                Units: m3/s
                IP-Units: gal/min
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Design Water Flow Rate"] = value

    @property
    def design_air_flow_rate(self):
        """Get design_air_flow_rate.

        Returns:
            float: the value of `design_air_flow_rate` or None if not set

        """
        return self["Design Air Flow Rate"]

    @design_air_flow_rate.setter
    def design_air_flow_rate(self, value=None):
        """Corresponds to IDD field `Design Air Flow Rate`

        Args:
            value (float or "Autosize"): value for IDD Field `Design Air Flow Rate`
                Units: m3/s
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Design Air Flow Rate"] = value

    @property
    def design_fan_power(self):
        """Get design_fan_power.

        Returns:
            float: the value of `design_fan_power` or None if not set

        """
        return self["Design Fan Power"]

    @design_fan_power.setter
    def design_fan_power(self, value=None):
        """Corresponds to IDD field `Design Fan Power` This is the fan motor
        electric input power.

        Args:
            value (float or "Autosize"): value for IDD Field `Design Fan Power`
                Units: W
                IP-Units: W
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Design Fan Power"] = value

    @property
    def design_ufactor_times_area_value(self):
        """Get design_ufactor_times_area_value.

        Returns:
            float: the value of `design_ufactor_times_area_value` or None if not set

        """
        return self["Design U-Factor Times Area Value"]

    @design_ufactor_times_area_value.setter
    def design_ufactor_times_area_value(self, value=None):
        """  Corresponds to IDD field `Design U-Factor Times Area Value`
        Leave field blank if tower performance input method is NominalCapacity

        Args:
            value (float or "Autosize"): value for IDD Field `Design U-Factor Times Area Value`
                Units: W/K
                value <= 2100000.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Design U-Factor Times Area Value"] = value

    @property
    def free_convection_air_flow_rate(self):
        """Get free_convection_air_flow_rate.

        Returns:
            float: the value of `free_convection_air_flow_rate` or None if not set

        """
        return self["Free Convection Air Flow Rate"]

    @free_convection_air_flow_rate.setter
    def free_convection_air_flow_rate(self, value=None):
        """Corresponds to IDD field `Free Convection Air Flow Rate`

        Args:
            value (float or "Autocalculate"): value for IDD Field `Free Convection Air Flow Rate`
                Units: m3/s
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Free Convection Air Flow Rate"] = value

    @property
    def free_convection_air_flow_rate_sizing_factor(self):
        """Get free_convection_air_flow_rate_sizing_factor.

        Returns:
            float: the value of `free_convection_air_flow_rate_sizing_factor` or None if not set

        """
        return self["Free Convection Air Flow Rate Sizing Factor"]

    @free_convection_air_flow_rate_sizing_factor.setter
    def free_convection_air_flow_rate_sizing_factor(self, value=0.1):
        """Corresponds to IDD field `Free Convection Air Flow Rate Sizing
        Factor` This field is only used if the previous field is set to
        autocalculate.

        Args:
            value (float): value for IDD Field `Free Convection Air Flow Rate Sizing Factor`
                Default value: 0.1
                value < 1.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Free Convection Air Flow Rate Sizing Factor"] = value

    @property
    def free_convection_ufactor_times_area_value(self):
        """Get free_convection_ufactor_times_area_value.

        Returns:
            float: the value of `free_convection_ufactor_times_area_value` or None if not set

        """
        return self["Free Convection U-Factor Times Area Value"]

    @free_convection_ufactor_times_area_value.setter
    def free_convection_ufactor_times_area_value(self, value=None):
        """  Corresponds to IDD field `Free Convection U-Factor Times Area Value`

        Args:
            value (float or "Autocalculate"): value for IDD Field `Free Convection U-Factor Times Area Value`
                Units: W/K
                value <= 300000.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Free Convection U-Factor Times Area Value"] = value

    @property
    def free_convection_ufactor_times_area_value_sizing_factor(self):
        """Get free_convection_ufactor_times_area_value_sizing_factor.

        Returns:
            float: the value of `free_convection_ufactor_times_area_value_sizing_factor` or None if not set

        """
        return self["Free Convection U-Factor Times Area Value Sizing Factor"]

    @free_convection_ufactor_times_area_value_sizing_factor.setter
    def free_convection_ufactor_times_area_value_sizing_factor(
            self,
            value=0.1):
        """  Corresponds to IDD field `Free Convection U-Factor Times Area Value Sizing Factor`
        This field is only used if the previous field is set to autocalculate and
        the Performance Input Method is UFactorTimesAreaAndDesignWaterFlowRate

        Args:
            value (float): value for IDD Field `Free Convection U-Factor Times Area Value Sizing Factor`
                Default value: 0.1
                value < 1.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Free Convection U-Factor Times Area Value Sizing Factor"] = value

    @property
    def performance_input_method(self):
        """Get performance_input_method.

        Returns:
            str: the value of `performance_input_method` or None if not set

        """
        return self["Performance Input Method"]

    @performance_input_method.setter
    def performance_input_method(
            self,
            value="UFactorTimesAreaAndDesignWaterFlowRate"):
        """Corresponds to IDD field `Performance Input Method` User can define
        tower thermal performance by specifying the tower UA, the Design Air
        Flow Rate and the Design Water Flow Rate, or by specifying the tower
        nominal capacity.

        Args:
            value (str): value for IDD Field `Performance Input Method`
                Default value: UFactorTimesAreaAndDesignWaterFlowRate
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Performance Input Method"] = value

    @property
    def heat_rejection_capacity_and_nominal_capacity_sizing_ratio(self):
        """Get heat_rejection_capacity_and_nominal_capacity_sizing_ratio.

        Returns:
            float: the value of `heat_rejection_capacity_and_nominal_capacity_sizing_ratio` or None if not set

        """
        return self[
            "Heat Rejection Capacity and Nominal Capacity Sizing Ratio"]

    @heat_rejection_capacity_and_nominal_capacity_sizing_ratio.setter
    def heat_rejection_capacity_and_nominal_capacity_sizing_ratio(
            self,
            value=1.25):
        """Corresponds to IDD field `Heat Rejection Capacity and Nominal
        Capacity Sizing Ratio`

        Args:
            value (float): value for IDD Field `Heat Rejection Capacity and Nominal Capacity Sizing Ratio`
                Default value: 1.25
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self[
            "Heat Rejection Capacity and Nominal Capacity Sizing Ratio"] = value

    @property
    def nominal_capacity(self):
        """Get nominal_capacity.

        Returns:
            float: the value of `nominal_capacity` or None if not set

        """
        return self["Nominal Capacity"]

    @nominal_capacity.setter
    def nominal_capacity(self, value=None):
        """  Corresponds to IDD field `Nominal Capacity`
        Nominal tower capacity with entering water at 35C (95F), leaving water at
        29.44C (85F), entering air at 25.56C (78F) wet-bulb temperature and 35C (95F)
        dry-bulb temperature. Design water flow rate assumed to be 5.382E-8 m3/s per watt
        (3 gpm/ton). Nominal tower capacity times (1.25) gives the actual tower
        heat rejection at these operating conditions.

        Args:
            value (float): value for IDD Field `Nominal Capacity`
                Units: W
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Nominal Capacity"] = value

    @property
    def free_convection_capacity(self):
        """Get free_convection_capacity.

        Returns:
            float: the value of `free_convection_capacity` or None if not set

        """
        return self["Free Convection Capacity"]

    @free_convection_capacity.setter
    def free_convection_capacity(self, value=None):
        """  Corresponds to IDD field `Free Convection Capacity`
        Tower capacity in free convection regime with entering water at 35C (95F),
        leaving water at 29.44C (85F), entering air at 25.56C (78F) wet-bulb temperature
        and 35C (95F) dry-bulb temperature. Design water flow rate assumed to be
        5.382E-8 m3/s per watt of nominal tower capacity (3 gpm/ton). Tower free
        convection capacity times (1.25) gives the actual tower heat rejection at these
        operating conditions.

        Args:
            value (float or "Autocalculate"): value for IDD Field `Free Convection Capacity`
                Units: W
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Free Convection Capacity"] = value

    @property
    def free_convection_nominal_capacity_sizing_factor(self):
        """Get free_convection_nominal_capacity_sizing_factor.

        Returns:
            float: the value of `free_convection_nominal_capacity_sizing_factor` or None if not set

        """
        return self["Free Convection Nominal Capacity Sizing Factor"]

    @free_convection_nominal_capacity_sizing_factor.setter
    def free_convection_nominal_capacity_sizing_factor(self, value=0.1):
        """Corresponds to IDD field `Free Convection Nominal Capacity Sizing
        Factor` This field is only used if the previous field is set to
        autocalculate.

        Args:
            value (float): value for IDD Field `Free Convection Nominal Capacity Sizing Factor`
                Default value: 0.1
                value < 1.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Free Convection Nominal Capacity Sizing Factor"] = value

    @property
    def basin_heater_capacity(self):
        """Get basin_heater_capacity.

        Returns:
            float: the value of `basin_heater_capacity` or None if not set

        """
        return self["Basin Heater Capacity"]

    @basin_heater_capacity.setter
    def basin_heater_capacity(self, value=None):
        """Corresponds to IDD field `Basin Heater Capacity` This heater
        maintains the basin water temperature at the basin heater setpoint
        temperature when the outdoor air temperature falls below the setpoint
        temperature. The basin heater only operates when water is not flowing
        through the tower.

        Args:
            value (float): value for IDD Field `Basin Heater Capacity`
                Units: W/K
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Basin Heater Capacity"] = value

    @property
    def basin_heater_setpoint_temperature(self):
        """Get basin_heater_setpoint_temperature.

        Returns:
            float: the value of `basin_heater_setpoint_temperature` or None if not set

        """
        return self["Basin Heater Setpoint Temperature"]

    @basin_heater_setpoint_temperature.setter
    def basin_heater_setpoint_temperature(self, value=2.0):
        """  Corresponds to IDD field `Basin Heater Setpoint Temperature`
        Enter the outdoor dry-bulb temperature when the basin heater turns on

        Args:
            value (float): value for IDD Field `Basin Heater Setpoint Temperature`
                Units: C
                Default value: 2.0
                value >= 2.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Basin Heater Setpoint Temperature"] = value

    @property
    def basin_heater_operating_schedule_name(self):
        """Get basin_heater_operating_schedule_name.

        Returns:
            str: the value of `basin_heater_operating_schedule_name` or None if not set

        """
        return self["Basin Heater Operating Schedule Name"]

    @basin_heater_operating_schedule_name.setter
    def basin_heater_operating_schedule_name(self, value=None):
        """  Corresponds to IDD field `Basin Heater Operating Schedule Name`
        Schedule values greater than 0 allow the basin heater to operate whenever the outdoor
        air dry-bulb temperature is below the basin heater setpoint temperature.
        If a schedule name is not entered, the basin heater is allowed to operate
        throughout the entire simulation.

        Args:
            value (str): value for IDD Field `Basin Heater Operating Schedule Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Basin Heater Operating Schedule Name"] = value

    @property
    def evaporation_loss_mode(self):
        """Get evaporation_loss_mode.

        Returns:
            str: the value of `evaporation_loss_mode` or None if not set

        """
        return self["Evaporation Loss Mode"]

    @evaporation_loss_mode.setter
    def evaporation_loss_mode(self, value=None):
        """Corresponds to IDD field `Evaporation Loss Mode`

        Args:
            value (str): value for IDD Field `Evaporation Loss Mode`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Evaporation Loss Mode"] = value

    @property
    def evaporation_loss_factor(self):
        """Get evaporation_loss_factor.

        Returns:
            float: the value of `evaporation_loss_factor` or None if not set

        """
        return self["Evaporation Loss Factor"]

    @evaporation_loss_factor.setter
    def evaporation_loss_factor(self, value=0.2):
        """  Corresponds to IDD field `Evaporation Loss Factor`
        Rate of water evaporation from the cooling tower and lost to the outdoor air [%/K]
        Evaporation loss is calculated as percentage of the circulating condenser water rate
        Value entered here is percent-per-degree K of temperature drop in the condenser water
        Typical values are from 0.15 to 0.27 [%/K].

        Args:
            value (float): value for IDD Field `Evaporation Loss Factor`
                Units: percent/K
                Default value: 0.2
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Evaporation Loss Factor"] = value

    @property
    def drift_loss_percent(self):
        """Get drift_loss_percent.

        Returns:
            float: the value of `drift_loss_percent` or None if not set

        """
        return self["Drift Loss Percent"]

    @drift_loss_percent.setter
    def drift_loss_percent(self, value=0.008):
        """  Corresponds to IDD field `Drift Loss Percent`
        Rate of drift loss as a percentage of circulating condenser water flow rate
        Typical values are between 0.002 and 0.2% The default value is 0.008%

        Args:
            value (float): value for IDD Field `Drift Loss Percent`
                Units: percent
                Default value: 0.008
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Drift Loss Percent"] = value

    @property
    def blowdown_calculation_mode(self):
        """Get blowdown_calculation_mode.

        Returns:
            str: the value of `blowdown_calculation_mode` or None if not set

        """
        return self["Blowdown Calculation Mode"]

    @blowdown_calculation_mode.setter
    def blowdown_calculation_mode(self, value=None):
        """Corresponds to IDD field `Blowdown Calculation Mode`

        Args:
            value (str): value for IDD Field `Blowdown Calculation Mode`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Blowdown Calculation Mode"] = value

    @property
    def blowdown_concentration_ratio(self):
        """Get blowdown_concentration_ratio.

        Returns:
            float: the value of `blowdown_concentration_ratio` or None if not set

        """
        return self["Blowdown Concentration Ratio"]

    @blowdown_concentration_ratio.setter
    def blowdown_concentration_ratio(self, value=3.0):
        """  Corresponds to IDD field `Blowdown Concentration Ratio`
        Characterizes the rate of blowdown in the cooling tower.
        Blowdown is water intentionally drained from the tower in order to offset the build up
        of solids in the water that would otherwise occur because of evaporation.
        Ratio of solids in the blowdown water to solids in the make up water.
        Typical values for tower operation are 3 to 5.  The default value is 3.

        Args:
            value (float): value for IDD Field `Blowdown Concentration Ratio`
                Default value: 3.0
                value >= 2.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Blowdown Concentration Ratio"] = value

    @property
    def blowdown_makeup_water_usage_schedule_name(self):
        """Get blowdown_makeup_water_usage_schedule_name.

        Returns:
            str: the value of `blowdown_makeup_water_usage_schedule_name` or None if not set

        """
        return self["Blowdown Makeup Water Usage Schedule Name"]

    @blowdown_makeup_water_usage_schedule_name.setter
    def blowdown_makeup_water_usage_schedule_name(self, value=None):
        """Corresponds to IDD field `Blowdown Makeup Water Usage Schedule Name`
        Makeup water usage due to blowdown results from occasionally draining a
        small amount of water in the tower basin to purge scale or other
        contaminants to reduce their concentration in order to maintain an
        acceptable level of water quality. Schedule values should reflect water
        usage in m3/s.

        Args:
            value (str): value for IDD Field `Blowdown Makeup Water Usage Schedule Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Blowdown Makeup Water Usage Schedule Name"] = value

    @property
    def supply_water_storage_tank_name(self):
        """Get supply_water_storage_tank_name.

        Returns:
            str: the value of `supply_water_storage_tank_name` or None if not set

        """
        return self["Supply Water Storage Tank Name"]

    @supply_water_storage_tank_name.setter
    def supply_water_storage_tank_name(self, value=None):
        """Corresponds to IDD field `Supply Water Storage Tank Name`

        Args:
            value (str): value for IDD Field `Supply Water Storage Tank Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Supply Water Storage Tank Name"] = value

    @property
    def outdoor_air_inlet_node_name(self):
        """Get outdoor_air_inlet_node_name.

        Returns:
            str: the value of `outdoor_air_inlet_node_name` or None if not set

        """
        return self["Outdoor Air Inlet Node Name"]

    @outdoor_air_inlet_node_name.setter
    def outdoor_air_inlet_node_name(self, value=None):
        """Corresponds to IDD field `Outdoor Air Inlet Node Name` Enter the
        name of an outdoor air node.

        Args:
            value (str): value for IDD Field `Outdoor Air Inlet Node Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Outdoor Air Inlet Node Name"] = value

    @property
    def capacity_control(self):
        """Get capacity_control.

        Returns:
            str: the value of `capacity_control` or None if not set

        """
        return self["Capacity Control"]

    @capacity_control.setter
    def capacity_control(self, value="FanCycling"):
        """Corresponds to IDD field `Capacity Control`

        Args:
            value (str): value for IDD Field `Capacity Control`
                Default value: FanCycling
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Capacity Control"] = value

    @property
    def number_of_cells(self):
        """Get number_of_cells.

        Returns:
            int: the value of `number_of_cells` or None if not set

        """
        return self["Number of Cells"]

    @number_of_cells.setter
    def number_of_cells(self, value=1):
        """Corresponds to IDD field `Number of Cells`

        Args:
            value (int): value for IDD Field `Number of Cells`
                Default value: 1
                value >= 1
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Number of Cells"] = value

    @property
    def cell_control(self):
        """Get cell_control.

        Returns:
            str: the value of `cell_control` or None if not set

        """
        return self["Cell Control"]

    @cell_control.setter
    def cell_control(self, value="MinimalCell"):
        """Corresponds to IDD field `Cell Control`

        Args:
            value (str): value for IDD Field `Cell Control`
                Default value: MinimalCell
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Cell Control"] = value

    @property
    def cell_minimum_water_flow_rate_fraction(self):
        """Get cell_minimum_water_flow_rate_fraction.

        Returns:
            float: the value of `cell_minimum_water_flow_rate_fraction` or None if not set

        """
        return self["Cell Minimum  Water Flow Rate Fraction"]

    @cell_minimum_water_flow_rate_fraction.setter
    def cell_minimum_water_flow_rate_fraction(self, value=0.33):
        """Corresponds to IDD field `Cell Minimum  Water Flow Rate Fraction`
        The allowable minimal fraction of the nominal flow rate per cell.

        Args:
            value (float): value for IDD Field `Cell Minimum  Water Flow Rate Fraction`
                Default value: 0.33
                value <= 1.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Cell Minimum  Water Flow Rate Fraction"] = value

    @property
    def cell_maximum_water_flow_rate_fraction(self):
        """Get cell_maximum_water_flow_rate_fraction.

        Returns:
            float: the value of `cell_maximum_water_flow_rate_fraction` or None if not set

        """
        return self["Cell Maximum Water Flow Rate Fraction"]

    @cell_maximum_water_flow_rate_fraction.setter
    def cell_maximum_water_flow_rate_fraction(self, value=2.5):
        """Corresponds to IDD field `Cell Maximum Water Flow Rate Fraction` The
        allowable maximal fraction of the nominal flow rate per cell.

        Args:
            value (float): value for IDD Field `Cell Maximum Water Flow Rate Fraction`
                Default value: 2.5
                value >= 1.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Cell Maximum Water Flow Rate Fraction"] = value

    @property
    def sizing_factor(self):
        """Get sizing_factor.

        Returns:
            float: the value of `sizing_factor` or None if not set

        """
        return self["Sizing Factor"]

    @sizing_factor.setter
    def sizing_factor(self, value=1.0):
        """Corresponds to IDD field `Sizing Factor` Multiplies the autosized
        capacity and flow rates.

        Args:
            value (float): value for IDD Field `Sizing Factor`
                Default value: 1.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Sizing Factor"] = value




class CoolingTowerTwoSpeed(DataObject):

    """ Corresponds to IDD object `CoolingTower:TwoSpeed`
        This tower model is based on Merkel's theory, which is also the basis
        for the tower model in ASHRAE's HVAC1 Toolkit. The closed-circuit cooling tower
        is modeled as a counter flow heat exchanger with a two-speed fan drawing air
        through the tower (induced-draft configuration).
        For a multi-cell tower, the capacity and air/water flow rate inputs are for the entire tower.
    """
    schema = {'extensible-fields': OrderedDict(),
              'fields': OrderedDict([(u'name',
                                      {'name': u'Name',
                                       'pyname': u'name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'alpha'}),
                                     (u'water inlet node name',
                                      {'name': u'Water Inlet Node Name',
                                       'pyname': u'water_inlet_node_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'node'}),
                                     (u'water outlet node name',
                                      {'name': u'Water Outlet Node Name',
                                       'pyname': u'water_outlet_node_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'node'}),
                                     (u'design water flow rate',
                                      {'name': u'Design Water Flow Rate',
                                       'pyname': u'design_water_flow_rate',
                                       'minimum>': 0.0,
                                       'required-field': False,
                                       'autosizable': True,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'm3/s'}),
                                     (u'high fan speed air flow rate',
                                      {'name': u'High Fan Speed Air Flow Rate',
                                       'pyname': u'high_fan_speed_air_flow_rate',
                                       'minimum>': 0.0,
                                       'required-field': True,
                                       'autosizable': True,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'm3/s'}),
                                     (u'high fan speed fan power',
                                      {'name': u'High Fan Speed Fan Power',
                                       'pyname': u'high_fan_speed_fan_power',
                                       'minimum>': 0.0,
                                       'required-field': True,
                                       'autosizable': True,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'W'}),
                                     (u'high fan speed u-factor times area value',
                                      {'name': u'High Fan Speed U-Factor Times Area Value',
                                       'pyname': u'high_fan_speed_ufactor_times_area_value',
                                       'minimum>': 0.0,
                                       'maximum': 2100000.0,
                                       'required-field': False,
                                       'autosizable': True,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'W/K'}),
                                     (u'low fan speed air flow rate',
                                      {'name': u'Low Fan Speed Air Flow Rate',
                                       'pyname': u'low_fan_speed_air_flow_rate',
                                       'minimum>': 0.0,
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': True,
                                       'type': u'real',
                                       'unit': u'm3/s'}),
                                     (u'low fan speed air flow rate sizing factor',
                                      {'name': u'Low Fan Speed Air Flow Rate Sizing Factor',
                                       'pyname': u'low_fan_speed_air_flow_rate_sizing_factor',
                                       'default': 0.5,
                                       'minimum>': 0.0,
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'maximum<': 1.0}),
                                     (u'low fan speed fan power',
                                      {'name': u'Low Fan Speed Fan Power',
                                       'pyname': u'low_fan_speed_fan_power',
                                       'minimum>': 0.0,
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': True,
                                       'type': u'real',
                                       'unit': u'W'}),
                                     (u'low fan speed fan power sizing factor',
                                      {'name': u'Low Fan Speed Fan Power Sizing Factor',
                                       'pyname': u'low_fan_speed_fan_power_sizing_factor',
                                       'default': 0.16,
                                       'minimum>': 0.0,
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'maximum<': 1.0}),
                                     (u'low fan speed u-factor times area value',
                                      {'name': u'Low Fan Speed U-Factor Times Area Value',
                                       'pyname': u'low_fan_speed_ufactor_times_area_value',
                                       'minimum>': 0.0,
                                       'maximum': 300000.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': True,
                                       'type': u'real',
                                       'unit': u'W/K'}),
                                     (u'low fan speed u-factor times area sizing factor',
                                      {'name': u'Low Fan Speed U-Factor Times Area Sizing Factor',
                                       'pyname': u'low_fan_speed_ufactor_times_area_sizing_factor',
                                       'default': 0.6,
                                       'minimum>': 0.0,
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'maximum<': 1.0}),
                                     (u'free convection regime air flow rate',
                                      {'name': u'Free Convection Regime Air Flow Rate',
                                       'pyname': u'free_convection_regime_air_flow_rate',
                                       'default': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': True,
                                       'type': u'real',
                                       'unit': u'm3/s'}),
                                     (u'free convection regime air flow rate sizing factor',
                                      {'name': u'Free Convection Regime Air Flow Rate Sizing Factor',
                                       'pyname': u'free_convection_regime_air_flow_rate_sizing_factor',
                                       'default': 0.1,
                                       'minimum>': 0.0,
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'maximum<': 1.0}),
                                     (u'free convection regime u-factor times area value',
                                      {'name': u'Free Convection Regime U-Factor Times Area Value',
                                       'pyname': u'free_convection_regime_ufactor_times_area_value',
                                       'default': 0.0,
                                       'maximum': 300000.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': True,
                                       'type': u'real',
                                       'unit': u'W/K'}),
                                     (u'free convection u-factor times area value sizing factor',
                                      {'name': u'Free Convection U-Factor Times Area Value Sizing Factor',
                                       'pyname': u'free_convection_ufactor_times_area_value_sizing_factor',
                                       'default': 0.1,
                                       'minimum>': 0.0,
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'maximum<': 1.0}),
                                     (u'performance input method',
                                      {'name': u'Performance Input Method',
                                       'pyname': u'performance_input_method',
                                       'default': u'UFactorTimesAreaAndDesignWaterFlowRate',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'UFactorTimesAreaAndDesignWaterFlowRate',
                                                           u'NominalCapacity'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'heat rejection capacity and nominal capacity sizing ratio',
                                      {'name': u'Heat Rejection Capacity and Nominal Capacity Sizing Ratio',
                                       'pyname': u'heat_rejection_capacity_and_nominal_capacity_sizing_ratio',
                                       'default': 1.25,
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'high speed nominal capacity',
                                      {'name': u'High Speed Nominal Capacity',
                                       'pyname': u'high_speed_nominal_capacity',
                                       'minimum>': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'W'}),
                                     (u'low speed nominal capacity',
                                      {'name': u'Low Speed Nominal Capacity',
                                       'pyname': u'low_speed_nominal_capacity',
                                       'minimum>': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': True,
                                       'type': u'real',
                                       'unit': u'W'}),
                                     (u'low speed nominal capacity sizing factor',
                                      {'name': u'Low Speed Nominal Capacity Sizing Factor',
                                       'pyname': u'low_speed_nominal_capacity_sizing_factor',
                                       'default': 0.5,
                                       'minimum>': 0.0,
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'maximum<': 1.0}),
                                     (u'free convection nominal capacity',
                                      {'name': u'Free Convection Nominal Capacity',
                                       'pyname': u'free_convection_nominal_capacity',
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': True,
                                       'type': u'real',
                                       'unit': u'W'}),
                                     (u'free convection nominal capacity sizing factor',
                                      {'name': u'Free Convection Nominal Capacity Sizing Factor',
                                       'pyname': u'free_convection_nominal_capacity_sizing_factor',
                                       'default': 0.1,
                                       'minimum>': 0.0,
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'maximum<': 1.0}),
                                     (u'basin heater capacity',
                                      {'name': u'Basin Heater Capacity',
                                       'pyname': u'basin_heater_capacity',
                                       'default': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'W/K'}),
                                     (u'basin heater setpoint temperature',
                                      {'name': u'Basin Heater Setpoint Temperature',
                                       'pyname': u'basin_heater_setpoint_temperature',
                                       'default': 2.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 2.0,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'C'}),
                                     (u'basin heater operating schedule name',
                                      {'name': u'Basin Heater Operating Schedule Name',
                                       'pyname': u'basin_heater_operating_schedule_name',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'evaporation loss mode',
                                      {'name': u'Evaporation Loss Mode',
                                       'pyname': u'evaporation_loss_mode',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'LossFactor',
                                                           u'SaturatedExit'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'evaporation loss factor',
                                      {'name': u'Evaporation Loss Factor',
                                       'pyname': u'evaporation_loss_factor',
                                       'default': 0.2,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'percent/K'}),
                                     (u'drift loss percent',
                                      {'name': u'Drift Loss Percent',
                                       'pyname': u'drift_loss_percent',
                                       'default': 0.008,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'percent'}),
                                     (u'blowdown calculation mode',
                                      {'name': u'Blowdown Calculation Mode',
                                       'pyname': u'blowdown_calculation_mode',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'ConcentrationRatio',
                                                           u'ScheduledRate'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'blowdown concentration ratio',
                                      {'name': u'Blowdown Concentration Ratio',
                                       'pyname': u'blowdown_concentration_ratio',
                                       'default': 3.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 2.0,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'blowdown makeup water usage schedule name',
                                      {'name': u'Blowdown Makeup Water Usage Schedule Name',
                                       'pyname': u'blowdown_makeup_water_usage_schedule_name',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'supply water storage tank name',
                                      {'name': u'Supply Water Storage Tank Name',
                                       'pyname': u'supply_water_storage_tank_name',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'outdoor air inlet node name',
                                      {'name': u'Outdoor Air Inlet Node Name',
                                       'pyname': u'outdoor_air_inlet_node_name',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'node'}),
                                     (u'number of cells',
                                      {'name': u'Number of Cells',
                                       'pyname': u'number_of_cells',
                                       'default': 1,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 1,
                                       'autocalculatable': False,
                                       'type': u'integer'}),
                                     (u'cell control',
                                      {'name': u'Cell Control',
                                       'pyname': u'cell_control',
                                       'default': u'MinimalCell',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'MinimalCell',
                                                           u'MaximalCell'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'cell minimum  water flow rate fraction',
                                      {'name': u'Cell Minimum  Water Flow Rate Fraction',
                                       'pyname': u'cell_minimum_water_flow_rate_fraction',
                                       'default': 0.33,
                                       'minimum>': 0.0,
                                       'maximum': 1.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'cell maximum water flow rate fraction',
                                      {'name': u'Cell Maximum Water Flow Rate Fraction',
                                       'pyname': u'cell_maximum_water_flow_rate_fraction',
                                       'default': 2.5,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 1.0,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'sizing factor',
                                      {'name': u'Sizing Factor',
                                       'pyname': u'sizing_factor',
                                       'default': 1.0,
                                       'minimum>': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'})]),
              'format': None,
              'group': u'Condenser Equipment and Heat Exchangers',
              'min-fields': 24,
              'name': u'CoolingTower:TwoSpeed',
              'pyname': u'CoolingTowerTwoSpeed',
              'required-object': False,
              'unique-object': False}

    @property
    def name(self):
        """Get name.

        Returns:
            str: the value of `name` or None if not set

        """
        return self["Name"]

    @name.setter
    def name(self, value=None):
        """Corresponds to IDD field `Name` Tower Name.

        Args:
            value (str): value for IDD Field `Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Name"] = value

    @property
    def water_inlet_node_name(self):
        """Get water_inlet_node_name.

        Returns:
            str: the value of `water_inlet_node_name` or None if not set

        """
        return self["Water Inlet Node Name"]

    @water_inlet_node_name.setter
    def water_inlet_node_name(self, value=None):
        """Corresponds to IDD field `Water Inlet Node Name` Name of tower Water
        Inlet Node.

        Args:
            value (str): value for IDD Field `Water Inlet Node Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Water Inlet Node Name"] = value

    @property
    def water_outlet_node_name(self):
        """Get water_outlet_node_name.

        Returns:
            str: the value of `water_outlet_node_name` or None if not set

        """
        return self["Water Outlet Node Name"]

    @water_outlet_node_name.setter
    def water_outlet_node_name(self, value=None):
        """Corresponds to IDD field `Water Outlet Node Name` Name of tower
        Water Outlet Node.

        Args:
            value (str): value for IDD Field `Water Outlet Node Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Water Outlet Node Name"] = value

    @property
    def design_water_flow_rate(self):
        """Get design_water_flow_rate.

        Returns:
            float: the value of `design_water_flow_rate` or None if not set

        """
        return self["Design Water Flow Rate"]

    @design_water_flow_rate.setter
    def design_water_flow_rate(self, value=None):
        """Corresponds to IDD field `Design Water Flow Rate` Leave field blank
        if Tower Performance Input Method is NominalCapacity.

        Args:
            value (float or "Autosize"): value for IDD Field `Design Water Flow Rate`
                Units: m3/s
                IP-Units: gal/min
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Design Water Flow Rate"] = value

    @property
    def high_fan_speed_air_flow_rate(self):
        """Get high_fan_speed_air_flow_rate.

        Returns:
            float: the value of `high_fan_speed_air_flow_rate` or None if not set

        """
        return self["High Fan Speed Air Flow Rate"]

    @high_fan_speed_air_flow_rate.setter
    def high_fan_speed_air_flow_rate(self, value=None):
        """Corresponds to IDD field `High Fan Speed Air Flow Rate`

        Args:
            value (float or "Autosize"): value for IDD Field `High Fan Speed Air Flow Rate`
                Units: m3/s
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["High Fan Speed Air Flow Rate"] = value

    @property
    def high_fan_speed_fan_power(self):
        """Get high_fan_speed_fan_power.

        Returns:
            float: the value of `high_fan_speed_fan_power` or None if not set

        """
        return self["High Fan Speed Fan Power"]

    @high_fan_speed_fan_power.setter
    def high_fan_speed_fan_power(self, value=None):
        """Corresponds to IDD field `High Fan Speed Fan Power` This is the fan
        motor electric input power at high speed.

        Args:
            value (float or "Autosize"): value for IDD Field `High Fan Speed Fan Power`
                Units: W
                IP-Units: W
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["High Fan Speed Fan Power"] = value

    @property
    def high_fan_speed_ufactor_times_area_value(self):
        """Get high_fan_speed_ufactor_times_area_value.

        Returns:
            float: the value of `high_fan_speed_ufactor_times_area_value` or None if not set

        """
        return self["High Fan Speed U-Factor Times Area Value"]

    @high_fan_speed_ufactor_times_area_value.setter
    def high_fan_speed_ufactor_times_area_value(self, value=None):
        """  Corresponds to IDD field `High Fan Speed U-Factor Times Area Value`
        Leave field blank if Tower Performance Input Method is NominalCapacity

        Args:
            value (float or "Autosize"): value for IDD Field `High Fan Speed U-Factor Times Area Value`
                Units: W/K
                value <= 2100000.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["High Fan Speed U-Factor Times Area Value"] = value

    @property
    def low_fan_speed_air_flow_rate(self):
        """Get low_fan_speed_air_flow_rate.

        Returns:
            float: the value of `low_fan_speed_air_flow_rate` or None if not set

        """
        return self["Low Fan Speed Air Flow Rate"]

    @low_fan_speed_air_flow_rate.setter
    def low_fan_speed_air_flow_rate(self, value=None):
        """Corresponds to IDD field `Low Fan Speed Air Flow Rate` Low speed air
        flow rate must be less than high speed air flow rate Low speed air flow
        rate must be greater than free convection air flow rate.

        Args:
            value (float or "Autocalculate"): value for IDD Field `Low Fan Speed Air Flow Rate`
                Units: m3/s
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Low Fan Speed Air Flow Rate"] = value

    @property
    def low_fan_speed_air_flow_rate_sizing_factor(self):
        """Get low_fan_speed_air_flow_rate_sizing_factor.

        Returns:
            float: the value of `low_fan_speed_air_flow_rate_sizing_factor` or None if not set

        """
        return self["Low Fan Speed Air Flow Rate Sizing Factor"]

    @low_fan_speed_air_flow_rate_sizing_factor.setter
    def low_fan_speed_air_flow_rate_sizing_factor(self, value=0.5):
        """Corresponds to IDD field `Low Fan Speed Air Flow Rate Sizing Factor`
        This field is only used if the previous field is set to autocalculate.

        Args:
            value (float): value for IDD Field `Low Fan Speed Air Flow Rate Sizing Factor`
                Default value: 0.5
                value < 1.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Low Fan Speed Air Flow Rate Sizing Factor"] = value

    @property
    def low_fan_speed_fan_power(self):
        """Get low_fan_speed_fan_power.

        Returns:
            float: the value of `low_fan_speed_fan_power` or None if not set

        """
        return self["Low Fan Speed Fan Power"]

    @low_fan_speed_fan_power.setter
    def low_fan_speed_fan_power(self, value=None):
        """Corresponds to IDD field `Low Fan Speed Fan Power` This is the fan
        motor electric input power at low speed.

        Args:
            value (float or "Autocalculate"): value for IDD Field `Low Fan Speed Fan Power`
                Units: W
                IP-Units: W
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Low Fan Speed Fan Power"] = value

    @property
    def low_fan_speed_fan_power_sizing_factor(self):
        """Get low_fan_speed_fan_power_sizing_factor.

        Returns:
            float: the value of `low_fan_speed_fan_power_sizing_factor` or None if not set

        """
        return self["Low Fan Speed Fan Power Sizing Factor"]

    @low_fan_speed_fan_power_sizing_factor.setter
    def low_fan_speed_fan_power_sizing_factor(self, value=0.16):
        """Corresponds to IDD field `Low Fan Speed Fan Power Sizing Factor`
        This field is only used if the previous field is set to autocalculate.

        Args:
            value (float): value for IDD Field `Low Fan Speed Fan Power Sizing Factor`
                Default value: 0.16
                value < 1.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Low Fan Speed Fan Power Sizing Factor"] = value

    @property
    def low_fan_speed_ufactor_times_area_value(self):
        """Get low_fan_speed_ufactor_times_area_value.

        Returns:
            float: the value of `low_fan_speed_ufactor_times_area_value` or None if not set

        """
        return self["Low Fan Speed U-Factor Times Area Value"]

    @low_fan_speed_ufactor_times_area_value.setter
    def low_fan_speed_ufactor_times_area_value(self, value=None):
        """  Corresponds to IDD field `Low Fan Speed U-Factor Times Area Value`
        Leave field blank if tower Performance Input Method is NominalCapacity
        Low speed tower UA must be less than high speed tower UA
        Low speed tower UA must be greater than free convection tower UA

        Args:
            value (float or "Autocalculate"): value for IDD Field `Low Fan Speed U-Factor Times Area Value`
                Units: W/K
                value <= 300000.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Low Fan Speed U-Factor Times Area Value"] = value

    @property
    def low_fan_speed_ufactor_times_area_sizing_factor(self):
        """Get low_fan_speed_ufactor_times_area_sizing_factor.

        Returns:
            float: the value of `low_fan_speed_ufactor_times_area_sizing_factor` or None if not set

        """
        return self["Low Fan Speed U-Factor Times Area Sizing Factor"]

    @low_fan_speed_ufactor_times_area_sizing_factor.setter
    def low_fan_speed_ufactor_times_area_sizing_factor(self, value=0.6):
        """  Corresponds to IDD field `Low Fan Speed U-Factor Times Area Sizing Factor`
        This field is only used if the previous field is set to autocalculate and
        the Performance Input Method is UFactorTimesAreaAndDesignWaterFlowRate

        Args:
            value (float): value for IDD Field `Low Fan Speed U-Factor Times Area Sizing Factor`
                Default value: 0.6
                value < 1.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Low Fan Speed U-Factor Times Area Sizing Factor"] = value

    @property
    def free_convection_regime_air_flow_rate(self):
        """Get free_convection_regime_air_flow_rate.

        Returns:
            float: the value of `free_convection_regime_air_flow_rate` or None if not set

        """
        return self["Free Convection Regime Air Flow Rate"]

    @free_convection_regime_air_flow_rate.setter
    def free_convection_regime_air_flow_rate(self, value=None):
        """Corresponds to IDD field `Free Convection Regime Air Flow Rate`

        Args:
            value (float or "Autocalculate"): value for IDD Field `Free Convection Regime Air Flow Rate`
                Units: m3/s
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Free Convection Regime Air Flow Rate"] = value

    @property
    def free_convection_regime_air_flow_rate_sizing_factor(self):
        """Get free_convection_regime_air_flow_rate_sizing_factor.

        Returns:
            float: the value of `free_convection_regime_air_flow_rate_sizing_factor` or None if not set

        """
        return self["Free Convection Regime Air Flow Rate Sizing Factor"]

    @free_convection_regime_air_flow_rate_sizing_factor.setter
    def free_convection_regime_air_flow_rate_sizing_factor(self, value=0.1):
        """Corresponds to IDD field `Free Convection Regime Air Flow Rate
        Sizing Factor` This field is only used if the previous field is set to
        autocalculate.

        Args:
            value (float): value for IDD Field `Free Convection Regime Air Flow Rate Sizing Factor`
                Default value: 0.1
                value < 1.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Free Convection Regime Air Flow Rate Sizing Factor"] = value

    @property
    def free_convection_regime_ufactor_times_area_value(self):
        """Get free_convection_regime_ufactor_times_area_value.

        Returns:
            float: the value of `free_convection_regime_ufactor_times_area_value` or None if not set

        """
        return self["Free Convection Regime U-Factor Times Area Value"]

    @free_convection_regime_ufactor_times_area_value.setter
    def free_convection_regime_ufactor_times_area_value(self, value=None):
        """  Corresponds to IDD field `Free Convection Regime U-Factor Times Area Value`
        Leave field blank if Tower Performance Input Method is NominalCapacity

        Args:
            value (float or "Autocalculate"): value for IDD Field `Free Convection Regime U-Factor Times Area Value`
                Units: W/K
                value <= 300000.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Free Convection Regime U-Factor Times Area Value"] = value

    @property
    def free_convection_ufactor_times_area_value_sizing_factor(self):
        """Get free_convection_ufactor_times_area_value_sizing_factor.

        Returns:
            float: the value of `free_convection_ufactor_times_area_value_sizing_factor` or None if not set

        """
        return self["Free Convection U-Factor Times Area Value Sizing Factor"]

    @free_convection_ufactor_times_area_value_sizing_factor.setter
    def free_convection_ufactor_times_area_value_sizing_factor(
            self,
            value=0.1):
        """  Corresponds to IDD field `Free Convection U-Factor Times Area Value Sizing Factor`
        This field is only used if the previous field is set to autocalculate and
        the Performance Input Method is UFactorTimesAreaAndDesignWaterFlowRate

        Args:
            value (float): value for IDD Field `Free Convection U-Factor Times Area Value Sizing Factor`
                Default value: 0.1
                value < 1.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Free Convection U-Factor Times Area Value Sizing Factor"] = value

    @property
    def performance_input_method(self):
        """Get performance_input_method.

        Returns:
            str: the value of `performance_input_method` or None if not set

        """
        return self["Performance Input Method"]

    @performance_input_method.setter
    def performance_input_method(
            self,
            value="UFactorTimesAreaAndDesignWaterFlowRate"):
        """Corresponds to IDD field `Performance Input Method` User can define
        tower thermal performance by specifying the tower UA, the Design Air
        Flow Rate and the Design Water Flow Rate, or by specifying the tower
        nominal capacity.

        Args:
            value (str): value for IDD Field `Performance Input Method`
                Default value: UFactorTimesAreaAndDesignWaterFlowRate
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Performance Input Method"] = value

    @property
    def heat_rejection_capacity_and_nominal_capacity_sizing_ratio(self):
        """Get heat_rejection_capacity_and_nominal_capacity_sizing_ratio.

        Returns:
            float: the value of `heat_rejection_capacity_and_nominal_capacity_sizing_ratio` or None if not set

        """
        return self[
            "Heat Rejection Capacity and Nominal Capacity Sizing Ratio"]

    @heat_rejection_capacity_and_nominal_capacity_sizing_ratio.setter
    def heat_rejection_capacity_and_nominal_capacity_sizing_ratio(
            self,
            value=1.25):
        """Corresponds to IDD field `Heat Rejection Capacity and Nominal
        Capacity Sizing Ratio`

        Args:
            value (float): value for IDD Field `Heat Rejection Capacity and Nominal Capacity Sizing Ratio`
                Default value: 1.25
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self[
            "Heat Rejection Capacity and Nominal Capacity Sizing Ratio"] = value

    @property
    def high_speed_nominal_capacity(self):
        """Get high_speed_nominal_capacity.

        Returns:
            float: the value of `high_speed_nominal_capacity` or None if not set

        """
        return self["High Speed Nominal Capacity"]

    @high_speed_nominal_capacity.setter
    def high_speed_nominal_capacity(self, value=None):
        """  Corresponds to IDD field `High Speed Nominal Capacity`
        Nominal tower capacity with entering water at 35C (95F), leaving water at
        29.44C (85F), entering air at 25.56C (78F) wet-bulb temperature and 35C (95F)
        dry-bulb temperature, with the tower fan operating at high speed. Design water
        flow rate assumed to be 5.382E-8 m3/s per watt(3 gpm/ton). Nominal tower capacity
        times the Heat Rejection Capacity and Nominal Capacity Sizing Ratio (e.g. 1.25)
        gives the actual tower heat rejection at these operating conditions.

        Args:
            value (float): value for IDD Field `High Speed Nominal Capacity`
                Units: W
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["High Speed Nominal Capacity"] = value

    @property
    def low_speed_nominal_capacity(self):
        """Get low_speed_nominal_capacity.

        Returns:
            float: the value of `low_speed_nominal_capacity` or None if not set

        """
        return self["Low Speed Nominal Capacity"]

    @low_speed_nominal_capacity.setter
    def low_speed_nominal_capacity(self, value=None):
        """  Corresponds to IDD field `Low Speed Nominal Capacity`
        Nominal tower capacity with entering water at 35C (95F), leaving water at
        29.44C (85F), entering air at 25.56C (78F) wet-bulb temperature and 35C (95F)
        dry-bulb temperature, with the tower fan operating at low speed. Design water flow
        rate assumed to be 5.382E-8 m3/s per watt of tower high-speed nominal capacity
        (3 gpm/ton). Nominal tower capacity times the Heat Rejection Capacity and Nominal
        Capacity Sizing Ratio (e.g. 1.25) gives the actual tower heat
        rejection at these operating conditions.

        Args:
            value (float or "Autocalculate"): value for IDD Field `Low Speed Nominal Capacity`
                Units: W
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Low Speed Nominal Capacity"] = value

    @property
    def low_speed_nominal_capacity_sizing_factor(self):
        """Get low_speed_nominal_capacity_sizing_factor.

        Returns:
            float: the value of `low_speed_nominal_capacity_sizing_factor` or None if not set

        """
        return self["Low Speed Nominal Capacity Sizing Factor"]

    @low_speed_nominal_capacity_sizing_factor.setter
    def low_speed_nominal_capacity_sizing_factor(self, value=0.5):
        """Corresponds to IDD field `Low Speed Nominal Capacity Sizing Factor`
        This field is only used if the previous field is set to autocalculate.

        Args:
            value (float): value for IDD Field `Low Speed Nominal Capacity Sizing Factor`
                Default value: 0.5
                value < 1.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Low Speed Nominal Capacity Sizing Factor"] = value

    @property
    def free_convection_nominal_capacity(self):
        """Get free_convection_nominal_capacity.

        Returns:
            float: the value of `free_convection_nominal_capacity` or None if not set

        """
        return self["Free Convection Nominal Capacity"]

    @free_convection_nominal_capacity.setter
    def free_convection_nominal_capacity(self, value=None):
        """  Corresponds to IDD field `Free Convection Nominal Capacity`
        Tower capacity in free convection regime with entering water at 35C (95F),
        leaving water at 29.44C (85F), entering air at 25.56C (78F) wet-bulb temperature
        and 35C (95F) dry-bulb temperature. Design water flow rate assumed to be
        5.382E-8 m3/s per watt of tower high-speed nominal capacity (3 gpm/ton). Tower
        free convection capacity times the Heat Rejection Capacity and Nominal Capacity Sizing Ratio
        (e.g. 1.25)  gives the actual tower heat rejection at these operating conditions

        Args:
            value (float or "Autocalculate"): value for IDD Field `Free Convection Nominal Capacity`
                Units: W
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Free Convection Nominal Capacity"] = value

    @property
    def free_convection_nominal_capacity_sizing_factor(self):
        """Get free_convection_nominal_capacity_sizing_factor.

        Returns:
            float: the value of `free_convection_nominal_capacity_sizing_factor` or None if not set

        """
        return self["Free Convection Nominal Capacity Sizing Factor"]

    @free_convection_nominal_capacity_sizing_factor.setter
    def free_convection_nominal_capacity_sizing_factor(self, value=0.1):
        """Corresponds to IDD field `Free Convection Nominal Capacity Sizing
        Factor` This field is only used if the previous field is set to
        autocalculate.

        Args:
            value (float): value for IDD Field `Free Convection Nominal Capacity Sizing Factor`
                Default value: 0.1
                value < 1.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Free Convection Nominal Capacity Sizing Factor"] = value

    @property
    def basin_heater_capacity(self):
        """Get basin_heater_capacity.

        Returns:
            float: the value of `basin_heater_capacity` or None if not set

        """
        return self["Basin Heater Capacity"]

    @basin_heater_capacity.setter
    def basin_heater_capacity(self, value=None):
        """Corresponds to IDD field `Basin Heater Capacity` This heater
        maintains the basin water temperature at the basin heater setpoint
        temperature when the outdoor air temperature falls below the setpoint
        temperature. The basin heater only operates when water is not flowing
        through the tower.

        Args:
            value (float): value for IDD Field `Basin Heater Capacity`
                Units: W/K
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Basin Heater Capacity"] = value

    @property
    def basin_heater_setpoint_temperature(self):
        """Get basin_heater_setpoint_temperature.

        Returns:
            float: the value of `basin_heater_setpoint_temperature` or None if not set

        """
        return self["Basin Heater Setpoint Temperature"]

    @basin_heater_setpoint_temperature.setter
    def basin_heater_setpoint_temperature(self, value=2.0):
        """  Corresponds to IDD field `Basin Heater Setpoint Temperature`
        Enter the outdoor dry-bulb temperature when the basin heater turns on

        Args:
            value (float): value for IDD Field `Basin Heater Setpoint Temperature`
                Units: C
                Default value: 2.0
                value >= 2.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Basin Heater Setpoint Temperature"] = value

    @property
    def basin_heater_operating_schedule_name(self):
        """Get basin_heater_operating_schedule_name.

        Returns:
            str: the value of `basin_heater_operating_schedule_name` or None if not set

        """
        return self["Basin Heater Operating Schedule Name"]

    @basin_heater_operating_schedule_name.setter
    def basin_heater_operating_schedule_name(self, value=None):
        """  Corresponds to IDD field `Basin Heater Operating Schedule Name`
        Schedule values greater than 0 allow the basin heater to operate whenever the outdoor
        air dry-bulb temperature is below the basin heater setpoint temperature.
        If a schedule name is not entered, the basin heater is allowed to operate
        throughout the entire simulation.

        Args:
            value (str): value for IDD Field `Basin Heater Operating Schedule Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Basin Heater Operating Schedule Name"] = value

    @property
    def evaporation_loss_mode(self):
        """Get evaporation_loss_mode.

        Returns:
            str: the value of `evaporation_loss_mode` or None if not set

        """
        return self["Evaporation Loss Mode"]

    @evaporation_loss_mode.setter
    def evaporation_loss_mode(self, value=None):
        """Corresponds to IDD field `Evaporation Loss Mode`

        Args:
            value (str): value for IDD Field `Evaporation Loss Mode`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Evaporation Loss Mode"] = value

    @property
    def evaporation_loss_factor(self):
        """Get evaporation_loss_factor.

        Returns:
            float: the value of `evaporation_loss_factor` or None if not set

        """
        return self["Evaporation Loss Factor"]

    @evaporation_loss_factor.setter
    def evaporation_loss_factor(self, value=0.2):
        """  Corresponds to IDD field `Evaporation Loss Factor`
        Rate of water evaporated from the cooling tower and lost to the outdoor air [%/K]
        Evaporation loss is calculated as percentage of the circulating condenser water rate
        Value entered here is percent-per-degree K of temperature drop in the condenser water
        Typical values are from 0.15 to 0.27 [%/K].

        Args:
            value (float): value for IDD Field `Evaporation Loss Factor`
                Units: percent/K
                Default value: 0.2
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Evaporation Loss Factor"] = value

    @property
    def drift_loss_percent(self):
        """Get drift_loss_percent.

        Returns:
            float: the value of `drift_loss_percent` or None if not set

        """
        return self["Drift Loss Percent"]

    @drift_loss_percent.setter
    def drift_loss_percent(self, value=0.008):
        """  Corresponds to IDD field `Drift Loss Percent`
        Rate of drift loss as a percentage of circulating condenser water flow rate
        Typical values are between 0.002 and 0.2% The default value is 0.008%

        Args:
            value (float): value for IDD Field `Drift Loss Percent`
                Units: percent
                Default value: 0.008
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Drift Loss Percent"] = value

    @property
    def blowdown_calculation_mode(self):
        """Get blowdown_calculation_mode.

        Returns:
            str: the value of `blowdown_calculation_mode` or None if not set

        """
        return self["Blowdown Calculation Mode"]

    @blowdown_calculation_mode.setter
    def blowdown_calculation_mode(self, value=None):
        """Corresponds to IDD field `Blowdown Calculation Mode`

        Args:
            value (str): value for IDD Field `Blowdown Calculation Mode`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Blowdown Calculation Mode"] = value

    @property
    def blowdown_concentration_ratio(self):
        """Get blowdown_concentration_ratio.

        Returns:
            float: the value of `blowdown_concentration_ratio` or None if not set

        """
        return self["Blowdown Concentration Ratio"]

    @blowdown_concentration_ratio.setter
    def blowdown_concentration_ratio(self, value=3.0):
        """  Corresponds to IDD field `Blowdown Concentration Ratio`
        Characterizes the rate of blowdown in the cooling tower.
        Blowdown is water intentionally drained from the tower in order to offset the build up
        of solids in the water that would otherwise occur because of evaporation.
        Ratio of solids in the blowdown water to solids in the make up water.
        Typical values for tower operation are 3 to 5.  The default value is 3.

        Args:
            value (float): value for IDD Field `Blowdown Concentration Ratio`
                Default value: 3.0
                value >= 2.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Blowdown Concentration Ratio"] = value

    @property
    def blowdown_makeup_water_usage_schedule_name(self):
        """Get blowdown_makeup_water_usage_schedule_name.

        Returns:
            str: the value of `blowdown_makeup_water_usage_schedule_name` or None if not set

        """
        return self["Blowdown Makeup Water Usage Schedule Name"]

    @blowdown_makeup_water_usage_schedule_name.setter
    def blowdown_makeup_water_usage_schedule_name(self, value=None):
        """Corresponds to IDD field `Blowdown Makeup Water Usage Schedule Name`
        Makeup water usage due to blowdown results from occasionally draining
        some amount of water in the tower basin to purge scale or other
        contaminants to reduce their concentration in order to maintain an
        acceptable level of water quality. Schedule values should reflect water
        usage in m3/s.

        Args:
            value (str): value for IDD Field `Blowdown Makeup Water Usage Schedule Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Blowdown Makeup Water Usage Schedule Name"] = value

    @property
    def supply_water_storage_tank_name(self):
        """Get supply_water_storage_tank_name.

        Returns:
            str: the value of `supply_water_storage_tank_name` or None if not set

        """
        return self["Supply Water Storage Tank Name"]

    @supply_water_storage_tank_name.setter
    def supply_water_storage_tank_name(self, value=None):
        """Corresponds to IDD field `Supply Water Storage Tank Name`

        Args:
            value (str): value for IDD Field `Supply Water Storage Tank Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Supply Water Storage Tank Name"] = value

    @property
    def outdoor_air_inlet_node_name(self):
        """Get outdoor_air_inlet_node_name.

        Returns:
            str: the value of `outdoor_air_inlet_node_name` or None if not set

        """
        return self["Outdoor Air Inlet Node Name"]

    @outdoor_air_inlet_node_name.setter
    def outdoor_air_inlet_node_name(self, value=None):
        """Corresponds to IDD field `Outdoor Air Inlet Node Name` Enter the
        name of an outdoor air node.

        Args:
            value (str): value for IDD Field `Outdoor Air Inlet Node Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Outdoor Air Inlet Node Name"] = value

    @property
    def number_of_cells(self):
        """Get number_of_cells.

        Returns:
            int: the value of `number_of_cells` or None if not set

        """
        return self["Number of Cells"]

    @number_of_cells.setter
    def number_of_cells(self, value=1):
        """Corresponds to IDD field `Number of Cells`

        Args:
            value (int): value for IDD Field `Number of Cells`
                Default value: 1
                value >= 1
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Number of Cells"] = value

    @property
    def cell_control(self):
        """Get cell_control.

        Returns:
            str: the value of `cell_control` or None if not set

        """
        return self["Cell Control"]

    @cell_control.setter
    def cell_control(self, value="MinimalCell"):
        """Corresponds to IDD field `Cell Control`

        Args:
            value (str): value for IDD Field `Cell Control`
                Default value: MinimalCell
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Cell Control"] = value

    @property
    def cell_minimum_water_flow_rate_fraction(self):
        """Get cell_minimum_water_flow_rate_fraction.

        Returns:
            float: the value of `cell_minimum_water_flow_rate_fraction` or None if not set

        """
        return self["Cell Minimum  Water Flow Rate Fraction"]

    @cell_minimum_water_flow_rate_fraction.setter
    def cell_minimum_water_flow_rate_fraction(self, value=0.33):
        """Corresponds to IDD field `Cell Minimum  Water Flow Rate Fraction`
        The allowable mininal fraction of the nominal flow rate per cell.

        Args:
            value (float): value for IDD Field `Cell Minimum  Water Flow Rate Fraction`
                Default value: 0.33
                value <= 1.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Cell Minimum  Water Flow Rate Fraction"] = value

    @property
    def cell_maximum_water_flow_rate_fraction(self):
        """Get cell_maximum_water_flow_rate_fraction.

        Returns:
            float: the value of `cell_maximum_water_flow_rate_fraction` or None if not set

        """
        return self["Cell Maximum Water Flow Rate Fraction"]

    @cell_maximum_water_flow_rate_fraction.setter
    def cell_maximum_water_flow_rate_fraction(self, value=2.5):
        """Corresponds to IDD field `Cell Maximum Water Flow Rate Fraction` The
        allowable maximal fraction of the nominal flow rate per cell.

        Args:
            value (float): value for IDD Field `Cell Maximum Water Flow Rate Fraction`
                Default value: 2.5
                value >= 1.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Cell Maximum Water Flow Rate Fraction"] = value

    @property
    def sizing_factor(self):
        """Get sizing_factor.

        Returns:
            float: the value of `sizing_factor` or None if not set

        """
        return self["Sizing Factor"]

    @sizing_factor.setter
    def sizing_factor(self, value=1.0):
        """Corresponds to IDD field `Sizing Factor` Multiplies the autosized
        capacity and flow rates.

        Args:
            value (float): value for IDD Field `Sizing Factor`
                Default value: 1.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Sizing Factor"] = value




class CoolingTowerVariableSpeedMerkel(DataObject):

    """ Corresponds to IDD object `CoolingTower:VariableSpeed:Merkel`
        This tower model is based on Merkel's theory, which is also the basis
        for the tower model in ASHRAE's HVAC1 Toolkit. The closed-circuit cooling tower
        is modeled as a counter flow heat exchanger with a variable-speed fan drawing air
        through the tower (induced-draft configuration).
        For a multi-cell tower, the capacity and air/water flow rate inputs are for the entire tower.
    """
    schema = {'extensible-fields': OrderedDict(),
              'fields': OrderedDict([(u'name',
                                      {'name': u'Name',
                                       'pyname': u'name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'alpha'}),
                                     (u'water inlet node name',
                                      {'name': u'Water Inlet Node Name',
                                       'pyname': u'water_inlet_node_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'node'}),
                                     (u'water outlet node name',
                                      {'name': u'Water Outlet Node Name',
                                       'pyname': u'water_outlet_node_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'node'}),
                                     (u'performance input method',
                                      {'name': u'Performance Input Method',
                                       'pyname': u'performance_input_method',
                                       'default': u'NominalCapacity',
                                       'required-field': True,
                                       'autosizable': False,
                                       'accepted-values': [u'UFactorTimesAreaAndDesignWaterFlowRate',
                                                           u'NominalCapacity'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'heat rejection capacity and nominal capacity sizing ratio',
                                      {'name': u'Heat Rejection Capacity and Nominal Capacity Sizing Ratio',
                                       'pyname': u'heat_rejection_capacity_and_nominal_capacity_sizing_ratio',
                                       'default': 1.25,
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'nominal capacity',
                                      {'name': u'Nominal Capacity',
                                       'pyname': u'nominal_capacity',
                                       'minimum>': 0.0,
                                       'required-field': False,
                                       'autosizable': True,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'W'}),
                                     (u'free convection nominal capacity',
                                      {'name': u'Free Convection Nominal Capacity',
                                       'pyname': u'free_convection_nominal_capacity',
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': True,
                                       'type': u'real',
                                       'unit': u'W'}),
                                     (u'free convection nominal capacity sizing factor',
                                      {'name': u'Free Convection Nominal Capacity Sizing Factor',
                                       'pyname': u'free_convection_nominal_capacity_sizing_factor',
                                       'default': 0.1,
                                       'minimum>': 0.0,
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'maximum<': 1.0}),
                                     (u'design water flow rate',
                                      {'name': u'Design Water Flow Rate',
                                       'pyname': u'design_water_flow_rate',
                                       'minimum>': 0.0,
                                       'required-field': True,
                                       'autosizable': True,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'm3/s'}),
                                     (u'design water flow rate per unit of nominal capacity',
                                      {'name': u'Design Water Flow Rate per Unit of Nominal Capacity',
                                       'pyname': u'design_water_flow_rate_per_unit_of_nominal_capacity',
                                       'default': 5.382e-08,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'm3/s-W'}),
                                     (u'design air flow rate',
                                      {'name': u'Design Air Flow Rate',
                                       'pyname': u'design_air_flow_rate',
                                       'minimum>': 0.0,
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': True,
                                       'type': u'real',
                                       'unit': u'm3/s'}),
                                     (u'design air flow rate per unit of nominal capacity',
                                      {'name': u'Design Air Flow Rate Per Unit of Nominal Capacity',
                                       'pyname': u'design_air_flow_rate_per_unit_of_nominal_capacity',
                                       'default': 2.76316e-05,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'm3/s-W'}),
                                     (u'minimum air flow rate ratio',
                                      {'name': u'Minimum Air Flow Rate Ratio',
                                       'pyname': u'minimum_air_flow_rate_ratio',
                                       'default': 0.2,
                                       'maximum': 0.5,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.1,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'design fan power',
                                      {'name': u'Design Fan Power',
                                       'pyname': u'design_fan_power',
                                       'minimum>': 0.0,
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': True,
                                       'type': u'real',
                                       'unit': u'W'}),
                                     (u'design fan power per unit of nominal capacity',
                                      {'name': u'Design Fan Power Per Unit of Nominal Capacity',
                                       'pyname': u'design_fan_power_per_unit_of_nominal_capacity',
                                       'default': 0.0105,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'dimensionless'}),
                                     (u'fan power modifier function of air flow rate ratio curve name',
                                      {'name': u'Fan Power Modifier Function of Air Flow Rate Ratio Curve Name',
                                       'pyname': u'fan_power_modifier_function_of_air_flow_rate_ratio_curve_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'free convection regime air flow rate',
                                      {'name': u'Free Convection Regime Air Flow Rate',
                                       'pyname': u'free_convection_regime_air_flow_rate',
                                       'default': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': True,
                                       'type': u'real',
                                       'unit': u'm3/s'}),
                                     (u'free convection regime air flow rate sizing factor',
                                      {'name': u'Free Convection Regime Air Flow Rate Sizing Factor',
                                       'pyname': u'free_convection_regime_air_flow_rate_sizing_factor',
                                       'default': 0.1,
                                       'minimum>': 0.0,
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'maximum<': 1.0}),
                                     (u'design air flow rate u-factor times area value',
                                      {'name': u'Design Air Flow Rate U-Factor Times Area Value',
                                       'pyname': u'design_air_flow_rate_ufactor_times_area_value',
                                       'required-field': False,
                                       'autosizable': True,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'W/K'}),
                                     (u'free convection regime u-factor times area value',
                                      {'name': u'Free Convection Regime U-Factor Times Area Value',
                                       'pyname': u'free_convection_regime_ufactor_times_area_value',
                                       'default': 0.0,
                                       'maximum': 300000.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': True,
                                       'type': u'real',
                                       'unit': u'W/K'}),
                                     (u'free convection u-factor times area value sizing factor',
                                      {'name': u'Free Convection U-Factor Times Area Value Sizing Factor',
                                       'pyname': u'free_convection_ufactor_times_area_value_sizing_factor',
                                       'default': 0.1,
                                       'minimum>': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'maximum<': 1.0}),
                                     (u'u-factor times area modifier function of air flow ratio curve name',
                                      {'name': u'U-Factor Times Area Modifier Function of Air Flow Ratio Curve Name',
                                       'pyname': u'ufactor_times_area_modifier_function_of_air_flow_ratio_curve_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'u-factor times area modifier function of wetbulb temperature difference curve name',
                                      {'name': u'U-Factor Times Area Modifier Function of Wetbulb Temperature Difference Curve Name',
                                       'pyname': u'ufactor_times_area_modifier_function_of_wetbulb_temperature_difference_curve_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'u-factor times area modifier function of water flow ratio curve name',
                                      {'name': u'U-Factor Times Area Modifier Function of Water Flow Ratio Curve Name',
                                       'pyname': u'ufactor_times_area_modifier_function_of_water_flow_ratio_curve_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'basin heater capacity',
                                      {'name': u'Basin Heater Capacity',
                                       'pyname': u'basin_heater_capacity',
                                       'default': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'W/K'}),
                                     (u'basin heater setpoint temperature',
                                      {'name': u'Basin Heater Setpoint Temperature',
                                       'pyname': u'basin_heater_setpoint_temperature',
                                       'default': 2.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 2.0,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'C'}),
                                     (u'basin heater operating schedule name',
                                      {'name': u'Basin Heater Operating Schedule Name',
                                       'pyname': u'basin_heater_operating_schedule_name',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'evaporation loss mode',
                                      {'name': u'Evaporation Loss Mode',
                                       'pyname': u'evaporation_loss_mode',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'LossFactor',
                                                           u'SaturatedExit'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'evaporation loss factor',
                                      {'name': u'Evaporation Loss Factor',
                                       'pyname': u'evaporation_loss_factor',
                                       'default': 0.2,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'percent/K'}),
                                     (u'drift loss percent',
                                      {'name': u'Drift Loss Percent',
                                       'pyname': u'drift_loss_percent',
                                       'default': 0.008,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'percent'}),
                                     (u'blowdown calculation mode',
                                      {'name': u'Blowdown Calculation Mode',
                                       'pyname': u'blowdown_calculation_mode',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'ConcentrationRatio',
                                                           u'ScheduledRate'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'blowdown concentration ratio',
                                      {'name': u'Blowdown Concentration Ratio',
                                       'pyname': u'blowdown_concentration_ratio',
                                       'default': 3.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 2.0,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'blowdown makeup water usage schedule name',
                                      {'name': u'Blowdown Makeup Water Usage Schedule Name',
                                       'pyname': u'blowdown_makeup_water_usage_schedule_name',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'supply water storage tank name',
                                      {'name': u'Supply Water Storage Tank Name',
                                       'pyname': u'supply_water_storage_tank_name',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'outdoor air inlet node name',
                                      {'name': u'Outdoor Air Inlet Node Name',
                                       'pyname': u'outdoor_air_inlet_node_name',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'node'}),
                                     (u'number of cells',
                                      {'name': u'Number of Cells',
                                       'pyname': u'number_of_cells',
                                       'default': 1,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 1,
                                       'autocalculatable': False,
                                       'type': u'integer'}),
                                     (u'cell control',
                                      {'name': u'Cell Control',
                                       'pyname': u'cell_control',
                                       'default': u'MinimalCell',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'MinimalCell',
                                                           u'MaximalCell'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'cell minimum  water flow rate fraction',
                                      {'name': u'Cell Minimum  Water Flow Rate Fraction',
                                       'pyname': u'cell_minimum_water_flow_rate_fraction',
                                       'default': 0.33,
                                       'minimum>': 0.0,
                                       'maximum': 1.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'cell maximum water flow rate fraction',
                                      {'name': u'Cell Maximum Water Flow Rate Fraction',
                                       'pyname': u'cell_maximum_water_flow_rate_fraction',
                                       'default': 2.5,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 1.0,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'sizing factor',
                                      {'name': u'Sizing Factor',
                                       'pyname': u'sizing_factor',
                                       'default': 1.0,
                                       'minimum>': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'})]),
              'format': None,
              'group': u'Condenser Equipment and Heat Exchangers',
              'min-fields': 24,
              'name': u'CoolingTower:VariableSpeed:Merkel',
              'pyname': u'CoolingTowerVariableSpeedMerkel',
              'required-object': False,
              'unique-object': False}

    @property
    def name(self):
        """Get name.

        Returns:
            str: the value of `name` or None if not set

        """
        return self["Name"]

    @name.setter
    def name(self, value=None):
        """Corresponds to IDD field `Name` Tower Name.

        Args:
            value (str): value for IDD Field `Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Name"] = value

    @property
    def water_inlet_node_name(self):
        """Get water_inlet_node_name.

        Returns:
            str: the value of `water_inlet_node_name` or None if not set

        """
        return self["Water Inlet Node Name"]

    @water_inlet_node_name.setter
    def water_inlet_node_name(self, value=None):
        """Corresponds to IDD field `Water Inlet Node Name` Name of tower water
        inlet node.

        Args:
            value (str): value for IDD Field `Water Inlet Node Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Water Inlet Node Name"] = value

    @property
    def water_outlet_node_name(self):
        """Get water_outlet_node_name.

        Returns:
            str: the value of `water_outlet_node_name` or None if not set

        """
        return self["Water Outlet Node Name"]

    @water_outlet_node_name.setter
    def water_outlet_node_name(self, value=None):
        """Corresponds to IDD field `Water Outlet Node Name` Name of tower
        water outlet node.

        Args:
            value (str): value for IDD Field `Water Outlet Node Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Water Outlet Node Name"] = value

    @property
    def performance_input_method(self):
        """Get performance_input_method.

        Returns:
            str: the value of `performance_input_method` or None if not set

        """
        return self["Performance Input Method"]

    @performance_input_method.setter
    def performance_input_method(self, value="NominalCapacity"):
        """Corresponds to IDD field `Performance Input Method` User can define
        tower thermal performance by specifying the tower UA, the Design Air
        Flow Rate and the Design Water Flow Rate, or by specifying the tower
        nominal capacity.

        Args:
            value (str): value for IDD Field `Performance Input Method`
                Default value: NominalCapacity
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Performance Input Method"] = value

    @property
    def heat_rejection_capacity_and_nominal_capacity_sizing_ratio(self):
        """Get heat_rejection_capacity_and_nominal_capacity_sizing_ratio.

        Returns:
            float: the value of `heat_rejection_capacity_and_nominal_capacity_sizing_ratio` or None if not set

        """
        return self[
            "Heat Rejection Capacity and Nominal Capacity Sizing Ratio"]

    @heat_rejection_capacity_and_nominal_capacity_sizing_ratio.setter
    def heat_rejection_capacity_and_nominal_capacity_sizing_ratio(
            self,
            value=1.25):
        """Corresponds to IDD field `Heat Rejection Capacity and Nominal
        Capacity Sizing Ratio`

        Args:
            value (float): value for IDD Field `Heat Rejection Capacity and Nominal Capacity Sizing Ratio`
                Default value: 1.25
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self[
            "Heat Rejection Capacity and Nominal Capacity Sizing Ratio"] = value

    @property
    def nominal_capacity(self):
        """Get nominal_capacity.

        Returns:
            float: the value of `nominal_capacity` or None if not set

        """
        return self["Nominal Capacity"]

    @nominal_capacity.setter
    def nominal_capacity(self, value=None):
        """  Corresponds to IDD field `Nominal Capacity`
        Nominal tower capacity with entering water at 35C (95F), leaving water at
        29.44C (85F), entering air at 25.56C (78F) wet-bulb temperature and 35C (95F)
        dry-bulb temperature, with the tower fan operating at Design Air Flow Rate (full speed). Design water
        flow rate is as set in Design Water Flow Rate per Unit of Nominal Capacity. Nominal tower capacity
        times the Heat Rejection Capacity and Nominal Capacity Sizing Ratio (e.g. 1.25)
        gives the actual tower heat rejection at these operating conditions.

        Args:
            value (float or "Autosize"): value for IDD Field `Nominal Capacity`
                Units: W
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Nominal Capacity"] = value

    @property
    def free_convection_nominal_capacity(self):
        """Get free_convection_nominal_capacity.

        Returns:
            float: the value of `free_convection_nominal_capacity` or None if not set

        """
        return self["Free Convection Nominal Capacity"]

    @free_convection_nominal_capacity.setter
    def free_convection_nominal_capacity(self, value=None):
        """  Corresponds to IDD field `Free Convection Nominal Capacity`
        required field when performance method is NominalCapacity
        Tower capacity in free convection regime with entering water at 35C (95F),
        leaving water at 29.44C (85F), entering air at 25.56C (78F) wet-bulb temperature
        and 35C (95F) dry-bulb temperature. Design water flow rate is as set
        in Design Water Flow Rate per Unit of Nominal Capacity. Tower
        free convection capacity times the Heat Rejection Capacity and Nominal Capacity Sizing Ratio
        (e.g. 1.25)  gives the actual tower heat rejection at these operating conditions

        Args:
            value (float or "Autocalculate"): value for IDD Field `Free Convection Nominal Capacity`
                Units: W
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Free Convection Nominal Capacity"] = value

    @property
    def free_convection_nominal_capacity_sizing_factor(self):
        """Get free_convection_nominal_capacity_sizing_factor.

        Returns:
            float: the value of `free_convection_nominal_capacity_sizing_factor` or None if not set

        """
        return self["Free Convection Nominal Capacity Sizing Factor"]

    @free_convection_nominal_capacity_sizing_factor.setter
    def free_convection_nominal_capacity_sizing_factor(self, value=0.1):
        """Corresponds to IDD field `Free Convection Nominal Capacity Sizing
        Factor` This field is only used if the previous field is set to
        autocalculate.

        Args:
            value (float): value for IDD Field `Free Convection Nominal Capacity Sizing Factor`
                Default value: 0.1
                value < 1.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Free Convection Nominal Capacity Sizing Factor"] = value

    @property
    def design_water_flow_rate(self):
        """Get design_water_flow_rate.

        Returns:
            float: the value of `design_water_flow_rate` or None if not set

        """
        return self["Design Water Flow Rate"]

    @design_water_flow_rate.setter
    def design_water_flow_rate(self, value=None):
        """Corresponds to IDD field `Design Water Flow Rate`

        Args:
            value (float or "Autosize"): value for IDD Field `Design Water Flow Rate`
                Units: m3/s
                IP-Units: gal/min
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Design Water Flow Rate"] = value

    @property
    def design_water_flow_rate_per_unit_of_nominal_capacity(self):
        """Get design_water_flow_rate_per_unit_of_nominal_capacity.

        Returns:
            float: the value of `design_water_flow_rate_per_unit_of_nominal_capacity` or None if not set

        """
        return self["Design Water Flow Rate per Unit of Nominal Capacity"]

    @design_water_flow_rate_per_unit_of_nominal_capacity.setter
    def design_water_flow_rate_per_unit_of_nominal_capacity(
            self,
            value=5.382e-08):
        """Corresponds to IDD field `Design Water Flow Rate per Unit of Nominal
        Capacity` This field is only used if the previous is set to
        autocalculate and performance input method is NominalCapacity.

        Args:
            value (float): value for IDD Field `Design Water Flow Rate per Unit of Nominal Capacity`
                Units: m3/s-W
                Default value: 5.382e-08
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Design Water Flow Rate per Unit of Nominal Capacity"] = value

    @property
    def design_air_flow_rate(self):
        """Get design_air_flow_rate.

        Returns:
            float: the value of `design_air_flow_rate` or None if not set

        """
        return self["Design Air Flow Rate"]

    @design_air_flow_rate.setter
    def design_air_flow_rate(self, value=None):
        """Corresponds to IDD field `Design Air Flow Rate` This is the air flow
        rate at full fan speed.

        Args:
            value (float or "Autocalculate"): value for IDD Field `Design Air Flow Rate`
                Units: m3/s
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Design Air Flow Rate"] = value

    @property
    def design_air_flow_rate_per_unit_of_nominal_capacity(self):
        """Get design_air_flow_rate_per_unit_of_nominal_capacity.

        Returns:
            float: the value of `design_air_flow_rate_per_unit_of_nominal_capacity` or None if not set

        """
        return self["Design Air Flow Rate Per Unit of Nominal Capacity"]

    @design_air_flow_rate_per_unit_of_nominal_capacity.setter
    def design_air_flow_rate_per_unit_of_nominal_capacity(
            self,
            value=2.76316e-05):
        """Corresponds to IDD field `Design Air Flow Rate Per Unit of Nominal
        Capacity` This field is only used if the previous is set to
        autocalculate When field is left blank the default scaling factor is
        adjusted for elevation to increase volume flow at altitude When field
        has a value the scaling factor is used without adjusting for elevation.

        Args:
            value (float): value for IDD Field `Design Air Flow Rate Per Unit of Nominal Capacity`
                Units: m3/s-W
                Default value: 2.76316e-05
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Design Air Flow Rate Per Unit of Nominal Capacity"] = value

    @property
    def minimum_air_flow_rate_ratio(self):
        """Get minimum_air_flow_rate_ratio.

        Returns:
            float: the value of `minimum_air_flow_rate_ratio` or None if not set

        """
        return self["Minimum Air Flow Rate Ratio"]

    @minimum_air_flow_rate_ratio.setter
    def minimum_air_flow_rate_ratio(self, value=0.2):
        """  Corresponds to IDD field `Minimum Air Flow Rate Ratio`
        Enter the minimum air flow rate ratio. This is typically determined by the variable
        speed drive that controls the fan motor speed. Valid entries are from 0.1 to 0.5.

        Args:
            value (float): value for IDD Field `Minimum Air Flow Rate Ratio`
                Default value: 0.2
                value >= 0.1
                value <= 0.5
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Minimum Air Flow Rate Ratio"] = value

    @property
    def design_fan_power(self):
        """Get design_fan_power.

        Returns:
            float: the value of `design_fan_power` or None if not set

        """
        return self["Design Fan Power"]

    @design_fan_power.setter
    def design_fan_power(self, value=None):
        """Corresponds to IDD field `Design Fan Power` This is the fan motor
        electric input power at high speed.

        Args:
            value (float or "Autocalculate"): value for IDD Field `Design Fan Power`
                Units: W
                IP-Units: W
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Design Fan Power"] = value

    @property
    def design_fan_power_per_unit_of_nominal_capacity(self):
        """Get design_fan_power_per_unit_of_nominal_capacity.

        Returns:
            float: the value of `design_fan_power_per_unit_of_nominal_capacity` or None if not set

        """
        return self["Design Fan Power Per Unit of Nominal Capacity"]

    @design_fan_power_per_unit_of_nominal_capacity.setter
    def design_fan_power_per_unit_of_nominal_capacity(self, value=0.0105):
        """Corresponds to IDD field `Design Fan Power Per Unit of Nominal
        Capacity` This field is only used if the previous is set to
        autocalculate.

        [W/W] Watts of fan power per Watt of tower nominal capacity

        Args:
            value (float): value for IDD Field `Design Fan Power Per Unit of Nominal Capacity`
                Units: dimensionless
                Default value: 0.0105
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Design Fan Power Per Unit of Nominal Capacity"] = value

    @property
    def fan_power_modifier_function_of_air_flow_rate_ratio_curve_name(self):
        """Get fan_power_modifier_function_of_air_flow_rate_ratio_curve_name.

        Returns:
            str: the value of `fan_power_modifier_function_of_air_flow_rate_ratio_curve_name` or None if not set

        """
        return self[
            "Fan Power Modifier Function of Air Flow Rate Ratio Curve Name"]

    @fan_power_modifier_function_of_air_flow_rate_ratio_curve_name.setter
    def fan_power_modifier_function_of_air_flow_rate_ratio_curve_name(
            self,
            value=None):
        """  Corresponds to IDD field `Fan Power Modifier Function of Air Flow Rate Ratio Curve Name`
        Any curve or table with one independent variable can be used:
        Curve:Linear, Curve:Quadratic, Curve:Cubic, Curve:Quartic, Curve:Exponent,
        Curve:ExponentialSkewNormal, Curve:Sigmoid, Curve:RectuangularHyperbola1,
        Curve:RectangularHyperbola2, Curve:ExponentialDecay, Curve:DoubleExponentialDecay,
        Table:OneIndependentVariable
        cubic curve = a + b*AFR + c*AFR**2 + d*AFR**3
        quartic curve = a + b*AFR + c*AFR**2 + d*AFR**3 + e*AFR**4
        x = AFR = Ratio of current operating air flow rate to Design Air Flow Rate

        Args:
            value (str): value for IDD Field `Fan Power Modifier Function of Air Flow Rate Ratio Curve Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self[
            "Fan Power Modifier Function of Air Flow Rate Ratio Curve Name"] = value

    @property
    def free_convection_regime_air_flow_rate(self):
        """Get free_convection_regime_air_flow_rate.

        Returns:
            float: the value of `free_convection_regime_air_flow_rate` or None if not set

        """
        return self["Free Convection Regime Air Flow Rate"]

    @free_convection_regime_air_flow_rate.setter
    def free_convection_regime_air_flow_rate(self, value=None):
        """Corresponds to IDD field `Free Convection Regime Air Flow Rate`

        Args:
            value (float or "Autocalculate"): value for IDD Field `Free Convection Regime Air Flow Rate`
                Units: m3/s
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Free Convection Regime Air Flow Rate"] = value

    @property
    def free_convection_regime_air_flow_rate_sizing_factor(self):
        """Get free_convection_regime_air_flow_rate_sizing_factor.

        Returns:
            float: the value of `free_convection_regime_air_flow_rate_sizing_factor` or None if not set

        """
        return self["Free Convection Regime Air Flow Rate Sizing Factor"]

    @free_convection_regime_air_flow_rate_sizing_factor.setter
    def free_convection_regime_air_flow_rate_sizing_factor(self, value=0.1):
        """Corresponds to IDD field `Free Convection Regime Air Flow Rate
        Sizing Factor` This field is only used if the previous field is set to
        autocalculate.

        Args:
            value (float): value for IDD Field `Free Convection Regime Air Flow Rate Sizing Factor`
                Default value: 0.1
                value < 1.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Free Convection Regime Air Flow Rate Sizing Factor"] = value

    @property
    def design_air_flow_rate_ufactor_times_area_value(self):
        """Get design_air_flow_rate_ufactor_times_area_value.

        Returns:
            float: the value of `design_air_flow_rate_ufactor_times_area_value` or None if not set

        """
        return self["Design Air Flow Rate U-Factor Times Area Value"]

    @design_air_flow_rate_ufactor_times_area_value.setter
    def design_air_flow_rate_ufactor_times_area_value(self, value=None):
        """  Corresponds to IDD field `Design Air Flow Rate U-Factor Times Area Value`
        required field when performance method is UFactorTimesAreaAndDesignWaterFlowRate
        when performance method is NominalCapacity the program will solve for this UA

        Args:
            value (float or "Autosize"): value for IDD Field `Design Air Flow Rate U-Factor Times Area Value`
                Units: W/K
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Design Air Flow Rate U-Factor Times Area Value"] = value

    @property
    def free_convection_regime_ufactor_times_area_value(self):
        """Get free_convection_regime_ufactor_times_area_value.

        Returns:
            float: the value of `free_convection_regime_ufactor_times_area_value` or None if not set

        """
        return self["Free Convection Regime U-Factor Times Area Value"]

    @free_convection_regime_ufactor_times_area_value.setter
    def free_convection_regime_ufactor_times_area_value(self, value=None):
        """  Corresponds to IDD field `Free Convection Regime U-Factor Times Area Value`
        required field when performance input method is UFactorTimesAreaAndDesignWaterFlowRate
        Leave field blank if performance input method is NominalCapacity

        Args:
            value (float or "Autocalculate"): value for IDD Field `Free Convection Regime U-Factor Times Area Value`
                Units: W/K
                value <= 300000.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Free Convection Regime U-Factor Times Area Value"] = value

    @property
    def free_convection_ufactor_times_area_value_sizing_factor(self):
        """Get free_convection_ufactor_times_area_value_sizing_factor.

        Returns:
            float: the value of `free_convection_ufactor_times_area_value_sizing_factor` or None if not set

        """
        return self["Free Convection U-Factor Times Area Value Sizing Factor"]

    @free_convection_ufactor_times_area_value_sizing_factor.setter
    def free_convection_ufactor_times_area_value_sizing_factor(
            self,
            value=0.1):
        """  Corresponds to IDD field `Free Convection U-Factor Times Area Value Sizing Factor`
        required field when performance input method is UFactorTimesAreaAndDesignWaterFlowRate
        This field is only used if the previous field is set to autocalculate and
        the performance input method is UFactorTimesAreaAndDesignWaterFlowRate

        Args:
            value (float): value for IDD Field `Free Convection U-Factor Times Area Value Sizing Factor`
                Default value: 0.1
                value < 1.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Free Convection U-Factor Times Area Value Sizing Factor"] = value

    @property
    def ufactor_times_area_modifier_function_of_air_flow_ratio_curve_name(
            self):
        """Get
        ufactor_times_area_modifier_function_of_air_flow_ratio_curve_name.

        Returns:
            str: the value of `ufactor_times_area_modifier_function_of_air_flow_ratio_curve_name` or None if not set

        """
        return self[
            "U-Factor Times Area Modifier Function of Air Flow Ratio Curve Name"]

    @ufactor_times_area_modifier_function_of_air_flow_ratio_curve_name.setter
    def ufactor_times_area_modifier_function_of_air_flow_ratio_curve_name(
            self,
            value=None):
        """  Corresponds to IDD field `U-Factor Times Area Modifier Function of Air Flow Ratio Curve Name`
        This curve describes how tower's design UA changes with variable air flow rate
        Any curve or table with one independent variable can be used:
        Curve:Linear, Curve:Quadratic, Curve:Cubic, Curve:Quartic, Curve:Exponent,
        Curve:ExponentialSkewNormal, Curve:Sigmoid, Curve:RectuangularHyperbola1,
        Curve:RectangularHyperbola2, Curve:ExponentialDecay, Curve:DoubleExponentialDecay,
        Table:OneIndependentVariable
        cubic curve = a + b*AFR + c*AFR**2 + d*AFR**3
        quartic curve = a + b*AFR + c*AFR**2 + d*AFR**3 + e*AFR**4
        x = AFR = Ratio of current operating air flow rate to Design Air Flow Rate

        Args:
            value (str): value for IDD Field `U-Factor Times Area Modifier Function of Air Flow Ratio Curve Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self[
            "U-Factor Times Area Modifier Function of Air Flow Ratio Curve Name"] = value

    @property
    def ufactor_times_area_modifier_function_of_wetbulb_temperature_difference_curve_name(
            self):
        """Get ufactor_times_area_modifier_function_of_wetbulb_temperature_diff
        erence_curve_name.

        Returns:
            str: the value of `ufactor_times_area_modifier_function_of_wetbulb_temperature_difference_curve_name` or None if not set

        """
        return self[
            "U-Factor Times Area Modifier Function of Wetbulb Temperature Difference Curve Name"]

    @ufactor_times_area_modifier_function_of_wetbulb_temperature_difference_curve_name.setter
    def ufactor_times_area_modifier_function_of_wetbulb_temperature_difference_curve_name(
            self,
            value=None):
        """  Corresponds to IDD field `U-Factor Times Area Modifier Function of Wetbulb Temperature Difference Curve Name`
        curve describes how tower UA changes with outdoor air wetbulb temperature difference from design wetbulb
        Any curve or table with one independent variable can be used:
        Curve:Linear, Curve:Quadratic, Curve:Cubic, Curve:Quartic, Curve:Exponent,
        Curve:ExponentialSkewNormal, Curve:Sigmoid, Curve:RectuangularHyperbola1,
        Curve:RectangularHyperbola2, Curve:ExponentialDecay, Curve:DoubleExponentialDecay,
        Table:OneIndependentVariable
        cubic curve = a + b*DeltaWB + c*DeltaWB**2 + d*DeltaWB**3
        quartic curve = a + b*DeltaWB + c*DeltaWB**2 + d*DeltaWB**3 + e*DeltaWB**4
        x = DeltaWB = (design wetbulb temperature in C - current wetbulb temperature in C)
        where design wetbulb temperature of entering air is 25.56C (78F)

        Args:
            value (str): value for IDD Field `U-Factor Times Area Modifier Function of Wetbulb Temperature Difference Curve Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self[
            "U-Factor Times Area Modifier Function of Wetbulb Temperature Difference Curve Name"] = value

    @property
    def ufactor_times_area_modifier_function_of_water_flow_ratio_curve_name(
            self):
        """Get
        ufactor_times_area_modifier_function_of_water_flow_ratio_curve_name.

        Returns:
            str: the value of `ufactor_times_area_modifier_function_of_water_flow_ratio_curve_name` or None if not set

        """
        return self[
            "U-Factor Times Area Modifier Function of Water Flow Ratio Curve Name"]

    @ufactor_times_area_modifier_function_of_water_flow_ratio_curve_name.setter
    def ufactor_times_area_modifier_function_of_water_flow_ratio_curve_name(
            self,
            value=None):
        """  Corresponds to IDD field `U-Factor Times Area Modifier Function of Water Flow Ratio Curve Name`
        curve describes how tower UA changes with the flow rate of condenser water through the tower
        Any curve or table with one independent variable can be used:
        Curve:Linear, Curve:Quadratic, Curve:Cubic, Curve:Quartic, Curve:Exponent,
        Curve:ExponentialSkewNormal, Curve:Sigmoid, Curve:RectuangularHyperbola1,
        Curve:RectangularHyperbola2, Curve:ExponentialDecay, Curve:DoubleExponentialDecay,
        Table:OneIndependentVariable
        cubic curve = a + b*WFR + c*WFR**2 + d*WFR**3
        quartic curve = a + b*WFR + c*WFR**2 + d*WFR**3 + e*WFR**4
        x = WFR = Ratio of current operationg water flow rate to Design Water Flow Rate

        Args:
            value (str): value for IDD Field `U-Factor Times Area Modifier Function of Water Flow Ratio Curve Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self[
            "U-Factor Times Area Modifier Function of Water Flow Ratio Curve Name"] = value

    @property
    def basin_heater_capacity(self):
        """Get basin_heater_capacity.

        Returns:
            float: the value of `basin_heater_capacity` or None if not set

        """
        return self["Basin Heater Capacity"]

    @basin_heater_capacity.setter
    def basin_heater_capacity(self, value=None):
        """Corresponds to IDD field `Basin Heater Capacity` This heater
        maintains the basin water temperature at the basin heater setpoint
        temperature when the outdoor air temperature falls below the setpoint
        temperature. The basin heater only operates when water is not flowing
        through the tower.

        Args:
            value (float): value for IDD Field `Basin Heater Capacity`
                Units: W/K
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Basin Heater Capacity"] = value

    @property
    def basin_heater_setpoint_temperature(self):
        """Get basin_heater_setpoint_temperature.

        Returns:
            float: the value of `basin_heater_setpoint_temperature` or None if not set

        """
        return self["Basin Heater Setpoint Temperature"]

    @basin_heater_setpoint_temperature.setter
    def basin_heater_setpoint_temperature(self, value=2.0):
        """  Corresponds to IDD field `Basin Heater Setpoint Temperature`
        Enter the outdoor dry-bulb temperature when the basin heater turns on

        Args:
            value (float): value for IDD Field `Basin Heater Setpoint Temperature`
                Units: C
                Default value: 2.0
                value >= 2.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Basin Heater Setpoint Temperature"] = value

    @property
    def basin_heater_operating_schedule_name(self):
        """Get basin_heater_operating_schedule_name.

        Returns:
            str: the value of `basin_heater_operating_schedule_name` or None if not set

        """
        return self["Basin Heater Operating Schedule Name"]

    @basin_heater_operating_schedule_name.setter
    def basin_heater_operating_schedule_name(self, value=None):
        """  Corresponds to IDD field `Basin Heater Operating Schedule Name`
        Schedule values greater than 0 allow the basin heater to operate whenever the outdoor
        air dry-bulb temperature is below the basin heater setpoint temperature.
        If a schedule name is not entered, the basin heater is allowed to operate
        throughout the entire simulation.

        Args:
            value (str): value for IDD Field `Basin Heater Operating Schedule Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Basin Heater Operating Schedule Name"] = value

    @property
    def evaporation_loss_mode(self):
        """Get evaporation_loss_mode.

        Returns:
            str: the value of `evaporation_loss_mode` or None if not set

        """
        return self["Evaporation Loss Mode"]

    @evaporation_loss_mode.setter
    def evaporation_loss_mode(self, value=None):
        """Corresponds to IDD field `Evaporation Loss Mode`

        Args:
            value (str): value for IDD Field `Evaporation Loss Mode`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Evaporation Loss Mode"] = value

    @property
    def evaporation_loss_factor(self):
        """Get evaporation_loss_factor.

        Returns:
            float: the value of `evaporation_loss_factor` or None if not set

        """
        return self["Evaporation Loss Factor"]

    @evaporation_loss_factor.setter
    def evaporation_loss_factor(self, value=0.2):
        """  Corresponds to IDD field `Evaporation Loss Factor`
        Rate of water evaporated from the cooling tower and lost to the outdoor air [%/K]
        Evaporation loss is calculated as percentage of the circulating condenser water rate
        Value entered here is percent-per-degree K of temperature drop in the condenser water
        Typical values are from 0.15 to 0.27 [%/K].

        Args:
            value (float): value for IDD Field `Evaporation Loss Factor`
                Units: percent/K
                Default value: 0.2
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Evaporation Loss Factor"] = value

    @property
    def drift_loss_percent(self):
        """Get drift_loss_percent.

        Returns:
            float: the value of `drift_loss_percent` or None if not set

        """
        return self["Drift Loss Percent"]

    @drift_loss_percent.setter
    def drift_loss_percent(self, value=0.008):
        """  Corresponds to IDD field `Drift Loss Percent`
        Rate of drift loss as a percentage of circulating condenser water flow rate
        Typical values are between 0.002 and 0.2% The default value is 0.008%

        Args:
            value (float): value for IDD Field `Drift Loss Percent`
                Units: percent
                Default value: 0.008
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Drift Loss Percent"] = value

    @property
    def blowdown_calculation_mode(self):
        """Get blowdown_calculation_mode.

        Returns:
            str: the value of `blowdown_calculation_mode` or None if not set

        """
        return self["Blowdown Calculation Mode"]

    @blowdown_calculation_mode.setter
    def blowdown_calculation_mode(self, value=None):
        """Corresponds to IDD field `Blowdown Calculation Mode`

        Args:
            value (str): value for IDD Field `Blowdown Calculation Mode`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Blowdown Calculation Mode"] = value

    @property
    def blowdown_concentration_ratio(self):
        """Get blowdown_concentration_ratio.

        Returns:
            float: the value of `blowdown_concentration_ratio` or None if not set

        """
        return self["Blowdown Concentration Ratio"]

    @blowdown_concentration_ratio.setter
    def blowdown_concentration_ratio(self, value=3.0):
        """  Corresponds to IDD field `Blowdown Concentration Ratio`
        Characterizes the rate of blowdown in the cooling tower.
        Blowdown is water intentionally drained from the tower in order to offset the build up
        of solids in the water that would otherwise occur because of evaporation.
        Ratio of solids in the blowdown water to solids in the make up water.
        Typical values for tower operation are 3 to 5.  The default value is 3.

        Args:
            value (float): value for IDD Field `Blowdown Concentration Ratio`
                Default value: 3.0
                value >= 2.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Blowdown Concentration Ratio"] = value

    @property
    def blowdown_makeup_water_usage_schedule_name(self):
        """Get blowdown_makeup_water_usage_schedule_name.

        Returns:
            str: the value of `blowdown_makeup_water_usage_schedule_name` or None if not set

        """
        return self["Blowdown Makeup Water Usage Schedule Name"]

    @blowdown_makeup_water_usage_schedule_name.setter
    def blowdown_makeup_water_usage_schedule_name(self, value=None):
        """Corresponds to IDD field `Blowdown Makeup Water Usage Schedule Name`
        Makeup water usage due to blowdown results from occasionally draining
        some amount of water in the tower basin to purge scale or other
        contaminants to reduce their concentration in order to maintain an
        acceptable level of water quality. Schedule values should reflect water
        usage in m3/s.

        Args:
            value (str): value for IDD Field `Blowdown Makeup Water Usage Schedule Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Blowdown Makeup Water Usage Schedule Name"] = value

    @property
    def supply_water_storage_tank_name(self):
        """Get supply_water_storage_tank_name.

        Returns:
            str: the value of `supply_water_storage_tank_name` or None if not set

        """
        return self["Supply Water Storage Tank Name"]

    @supply_water_storage_tank_name.setter
    def supply_water_storage_tank_name(self, value=None):
        """Corresponds to IDD field `Supply Water Storage Tank Name`

        Args:
            value (str): value for IDD Field `Supply Water Storage Tank Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Supply Water Storage Tank Name"] = value

    @property
    def outdoor_air_inlet_node_name(self):
        """Get outdoor_air_inlet_node_name.

        Returns:
            str: the value of `outdoor_air_inlet_node_name` or None if not set

        """
        return self["Outdoor Air Inlet Node Name"]

    @outdoor_air_inlet_node_name.setter
    def outdoor_air_inlet_node_name(self, value=None):
        """Corresponds to IDD field `Outdoor Air Inlet Node Name` Enter the
        name of an outdoor air node.

        Args:
            value (str): value for IDD Field `Outdoor Air Inlet Node Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Outdoor Air Inlet Node Name"] = value

    @property
    def number_of_cells(self):
        """Get number_of_cells.

        Returns:
            int: the value of `number_of_cells` or None if not set

        """
        return self["Number of Cells"]

    @number_of_cells.setter
    def number_of_cells(self, value=1):
        """Corresponds to IDD field `Number of Cells`

        Args:
            value (int): value for IDD Field `Number of Cells`
                Default value: 1
                value >= 1
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Number of Cells"] = value

    @property
    def cell_control(self):
        """Get cell_control.

        Returns:
            str: the value of `cell_control` or None if not set

        """
        return self["Cell Control"]

    @cell_control.setter
    def cell_control(self, value="MinimalCell"):
        """Corresponds to IDD field `Cell Control`

        Args:
            value (str): value for IDD Field `Cell Control`
                Default value: MinimalCell
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Cell Control"] = value

    @property
    def cell_minimum_water_flow_rate_fraction(self):
        """Get cell_minimum_water_flow_rate_fraction.

        Returns:
            float: the value of `cell_minimum_water_flow_rate_fraction` or None if not set

        """
        return self["Cell Minimum  Water Flow Rate Fraction"]

    @cell_minimum_water_flow_rate_fraction.setter
    def cell_minimum_water_flow_rate_fraction(self, value=0.33):
        """Corresponds to IDD field `Cell Minimum  Water Flow Rate Fraction`
        The allowable mininal fraction of the nominal flow rate per cell.

        Args:
            value (float): value for IDD Field `Cell Minimum  Water Flow Rate Fraction`
                Default value: 0.33
                value <= 1.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Cell Minimum  Water Flow Rate Fraction"] = value

    @property
    def cell_maximum_water_flow_rate_fraction(self):
        """Get cell_maximum_water_flow_rate_fraction.

        Returns:
            float: the value of `cell_maximum_water_flow_rate_fraction` or None if not set

        """
        return self["Cell Maximum Water Flow Rate Fraction"]

    @cell_maximum_water_flow_rate_fraction.setter
    def cell_maximum_water_flow_rate_fraction(self, value=2.5):
        """Corresponds to IDD field `Cell Maximum Water Flow Rate Fraction` The
        allowable maximal fraction of the nominal flow rate per cell.

        Args:
            value (float): value for IDD Field `Cell Maximum Water Flow Rate Fraction`
                Default value: 2.5
                value >= 1.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Cell Maximum Water Flow Rate Fraction"] = value

    @property
    def sizing_factor(self):
        """Get sizing_factor.

        Returns:
            float: the value of `sizing_factor` or None if not set

        """
        return self["Sizing Factor"]

    @sizing_factor.setter
    def sizing_factor(self, value=1.0):
        """Corresponds to IDD field `Sizing Factor` Multiplies the autosized
        capacity and flow rates.

        Args:
            value (float): value for IDD Field `Sizing Factor`
                Default value: 1.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Sizing Factor"] = value




class CoolingTowerVariableSpeed(DataObject):

    """ Corresponds to IDD object `CoolingTower:VariableSpeed`
        This tower model is based on purely empirical algorithms derived from manufacturer's
        performance data or field measurements. The user can select from two existing
        algorithms (CoolTools or YorkCalc), or they can enter their own correlation for
        approach temperature by using a variable speed tower model coefficient object.
        For a multi-cell tower, the capacity and air/water flow rate inputs are for the entire tower.
    """
    schema = {'extensible-fields': OrderedDict(),
              'fields': OrderedDict([(u'name',
                                      {'name': u'Name',
                                       'pyname': u'name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'alpha'}),
                                     (u'water inlet node name',
                                      {'name': u'Water Inlet Node Name',
                                       'pyname': u'water_inlet_node_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'node'}),
                                     (u'water outlet node name',
                                      {'name': u'Water Outlet Node Name',
                                       'pyname': u'water_outlet_node_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'node'}),
                                     (u'model type',
                                      {'name': u'Model Type',
                                       'pyname': u'model_type',
                                       'default': u'YorkCalc',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'CoolToolsCrossFlow',
                                                           u'CoolToolsUserDefined',
                                                           u'YorkCalc',
                                                           u'YorkCalcUserDefined'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'model coefficient name',
                                      {'name': u'Model Coefficient Name',
                                       'pyname': u'model_coefficient_name',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'design inlet air wet-bulb temperature',
                                      {'name': u'Design Inlet Air Wet-Bulb Temperature',
                                       'pyname': u'design_inlet_air_wetbulb_temperature',
                                       'default': 25.6,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 20.0,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'C'}),
                                     (u'design approach temperature',
                                      {'name': u'Design Approach Temperature',
                                       'pyname': u'design_approach_temperature',
                                       'default': 3.9,
                                       'minimum>': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'deltaC'}),
                                     (u'design range temperature',
                                      {'name': u'Design Range Temperature',
                                       'pyname': u'design_range_temperature',
                                       'default': 5.6,
                                       'minimum>': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'deltaC'}),
                                     (u'design water flow rate',
                                      {'name': u'Design Water Flow Rate',
                                       'pyname': u'design_water_flow_rate',
                                       'minimum>': 0.0,
                                       'required-field': True,
                                       'autosizable': True,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'm3/s'}),
                                     (u'design air flow rate',
                                      {'name': u'Design Air Flow Rate',
                                       'pyname': u'design_air_flow_rate',
                                       'minimum>': 0.0,
                                       'required-field': True,
                                       'autosizable': True,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'm3/s'}),
                                     (u'design fan power',
                                      {'name': u'Design Fan Power',
                                       'pyname': u'design_fan_power',
                                       'minimum>': 0.0,
                                       'required-field': True,
                                       'autosizable': True,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'W'}),
                                     (u'fan power ratio function of air flow rate ratio curve name',
                                      {'name': u'Fan Power Ratio Function of Air Flow Rate Ratio Curve Name',
                                       'pyname': u'fan_power_ratio_function_of_air_flow_rate_ratio_curve_name',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'minimum air flow rate ratio',
                                      {'name': u'Minimum Air Flow Rate Ratio',
                                       'pyname': u'minimum_air_flow_rate_ratio',
                                       'default': 0.2,
                                       'maximum': 0.5,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.2,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'fraction of tower capacity in free convection regime',
                                      {'name': u'Fraction of Tower Capacity in Free Convection Regime',
                                       'pyname': u'fraction_of_tower_capacity_in_free_convection_regime',
                                       'default': 0.125,
                                       'maximum': 0.2,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'basin heater capacity',
                                      {'name': u'Basin Heater Capacity',
                                       'pyname': u'basin_heater_capacity',
                                       'default': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'W/K'}),
                                     (u'basin heater setpoint temperature',
                                      {'name': u'Basin Heater Setpoint Temperature',
                                       'pyname': u'basin_heater_setpoint_temperature',
                                       'default': 2.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 2.0,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'C'}),
                                     (u'basin heater operating schedule name',
                                      {'name': u'Basin Heater Operating Schedule Name',
                                       'pyname': u'basin_heater_operating_schedule_name',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'evaporation loss mode',
                                      {'name': u'Evaporation Loss Mode',
                                       'pyname': u'evaporation_loss_mode',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'LossFactor',
                                                           u'SaturatedExit'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'evaporation loss factor',
                                      {'name': u'Evaporation Loss Factor',
                                       'pyname': u'evaporation_loss_factor',
                                       'default': 0.2,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'percent/K'}),
                                     (u'drift loss percent',
                                      {'name': u'Drift Loss Percent',
                                       'pyname': u'drift_loss_percent',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'percent'}),
                                     (u'blowdown calculation mode',
                                      {'name': u'Blowdown Calculation Mode',
                                       'pyname': u'blowdown_calculation_mode',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'ConcentrationRatio',
                                                           u'ScheduledRate'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'blowdown concentration ratio',
                                      {'name': u'Blowdown Concentration Ratio',
                                       'pyname': u'blowdown_concentration_ratio',
                                       'default': 3.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 2.0,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'blowdown makeup water usage schedule name',
                                      {'name': u'Blowdown Makeup Water Usage Schedule Name',
                                       'pyname': u'blowdown_makeup_water_usage_schedule_name',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'supply water storage tank name',
                                      {'name': u'Supply Water Storage Tank Name',
                                       'pyname': u'supply_water_storage_tank_name',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'outdoor air inlet node name',
                                      {'name': u'Outdoor Air Inlet Node Name',
                                       'pyname': u'outdoor_air_inlet_node_name',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'node'}),
                                     (u'number of cells',
                                      {'name': u'Number of Cells',
                                       'pyname': u'number_of_cells',
                                       'default': 1,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 1,
                                       'autocalculatable': False,
                                       'type': u'integer'}),
                                     (u'cell control',
                                      {'name': u'Cell Control',
                                       'pyname': u'cell_control',
                                       'default': u'MinimalCell',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'MinimalCell',
                                                           u'MaximalCell'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'cell minimum  water flow rate fraction',
                                      {'name': u'Cell Minimum  Water Flow Rate Fraction',
                                       'pyname': u'cell_minimum_water_flow_rate_fraction',
                                       'default': 0.33,
                                       'minimum>': 0.0,
                                       'maximum': 1.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'cell maximum water flow rate fraction',
                                      {'name': u'Cell Maximum Water Flow Rate Fraction',
                                       'pyname': u'cell_maximum_water_flow_rate_fraction',
                                       'default': 2.5,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 1.0,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'sizing factor',
                                      {'name': u'Sizing Factor',
                                       'pyname': u'sizing_factor',
                                       'default': 1.0,
                                       'minimum>': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'})]),
              'format': None,
              'group': u'Condenser Equipment and Heat Exchangers',
              'min-fields': 15,
              'name': u'CoolingTower:VariableSpeed',
              'pyname': u'CoolingTowerVariableSpeed',
              'required-object': False,
              'unique-object': False}

    @property
    def name(self):
        """Get name.

        Returns:
            str: the value of `name` or None if not set

        """
        return self["Name"]

    @name.setter
    def name(self, value=None):
        """Corresponds to IDD field `Name` Tower Name.

        Args:
            value (str): value for IDD Field `Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Name"] = value

    @property
    def water_inlet_node_name(self):
        """Get water_inlet_node_name.

        Returns:
            str: the value of `water_inlet_node_name` or None if not set

        """
        return self["Water Inlet Node Name"]

    @water_inlet_node_name.setter
    def water_inlet_node_name(self, value=None):
        """Corresponds to IDD field `Water Inlet Node Name` Name of tower water
        inlet node.

        Args:
            value (str): value for IDD Field `Water Inlet Node Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Water Inlet Node Name"] = value

    @property
    def water_outlet_node_name(self):
        """Get water_outlet_node_name.

        Returns:
            str: the value of `water_outlet_node_name` or None if not set

        """
        return self["Water Outlet Node Name"]

    @water_outlet_node_name.setter
    def water_outlet_node_name(self, value=None):
        """Corresponds to IDD field `Water Outlet Node Name` Name of tower
        water outlet node.

        Args:
            value (str): value for IDD Field `Water Outlet Node Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Water Outlet Node Name"] = value

    @property
    def model_type(self):
        """Get model_type.

        Returns:
            str: the value of `model_type` or None if not set

        """
        return self["Model Type"]

    @model_type.setter
    def model_type(self, value="YorkCalc"):
        """Corresponds to IDD field `Model Type` Determines the coefficients
        and form of the equation for calculating approach temperature.

        Args:
            value (str): value for IDD Field `Model Type`
                Default value: YorkCalc
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Model Type"] = value

    @property
    def model_coefficient_name(self):
        """Get model_coefficient_name.

        Returns:
            str: the value of `model_coefficient_name` or None if not set

        """
        return self["Model Coefficient Name"]

    @model_coefficient_name.setter
    def model_coefficient_name(self, value=None):
        """Corresponds to IDD field `Model Coefficient Name` Name of the tower
        model coefficient object. Used only when tower Model Type is either
        CoolToolsUserDefined or YorkCalcUserDefined.

        Args:
            value (str): value for IDD Field `Model Coefficient Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Model Coefficient Name"] = value

    @property
    def design_inlet_air_wetbulb_temperature(self):
        """Get design_inlet_air_wetbulb_temperature.

        Returns:
            float: the value of `design_inlet_air_wetbulb_temperature` or None if not set

        """
        return self["Design Inlet Air Wet-Bulb Temperature"]

    @design_inlet_air_wetbulb_temperature.setter
    def design_inlet_air_wetbulb_temperature(self, value=25.6):
        """  Corresponds to IDD field `Design Inlet Air Wet-Bulb Temperature`
        Enter the tower's design inlet air wet-bulb temperature

        Args:
            value (float): value for IDD Field `Design Inlet Air Wet-Bulb Temperature`
                Units: C
                Default value: 25.6
                value >= 20.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Design Inlet Air Wet-Bulb Temperature"] = value

    @property
    def design_approach_temperature(self):
        """Get design_approach_temperature.

        Returns:
            float: the value of `design_approach_temperature` or None if not set

        """
        return self["Design Approach Temperature"]

    @design_approach_temperature.setter
    def design_approach_temperature(self, value=3.9):
        """  Corresponds to IDD field `Design Approach Temperature`
        Enter the approach temperature corresponding to the design inlet air
        wet-bulb temperature and design range temperature.
        Design approach temp = outlet water temperature minus inlet air wet-bulb temperature
        at design conditions.

        Args:
            value (float): value for IDD Field `Design Approach Temperature`
                Units: deltaC
                Default value: 3.9
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Design Approach Temperature"] = value

    @property
    def design_range_temperature(self):
        """Get design_range_temperature.

        Returns:
            float: the value of `design_range_temperature` or None if not set

        """
        return self["Design Range Temperature"]

    @design_range_temperature.setter
    def design_range_temperature(self, value=5.6):
        """  Corresponds to IDD field `Design Range Temperature`
        Enter the range temperature corresponding to the design inlet air
        wet-bulb temperature and design approach temperature.
        Design range = inlet water temperature minus outlet water temperature
        at design conditions.

        Args:
            value (float): value for IDD Field `Design Range Temperature`
                Units: deltaC
                Default value: 5.6
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Design Range Temperature"] = value

    @property
    def design_water_flow_rate(self):
        """Get design_water_flow_rate.

        Returns:
            float: the value of `design_water_flow_rate` or None if not set

        """
        return self["Design Water Flow Rate"]

    @design_water_flow_rate.setter
    def design_water_flow_rate(self, value=None):
        """Corresponds to IDD field `Design Water Flow Rate` Water flow rate
        through the tower at design conditions.

        Args:
            value (float or "Autosize"): value for IDD Field `Design Water Flow Rate`
                Units: m3/s
                IP-Units: gal/min
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Design Water Flow Rate"] = value

    @property
    def design_air_flow_rate(self):
        """Get design_air_flow_rate.

        Returns:
            float: the value of `design_air_flow_rate` or None if not set

        """
        return self["Design Air Flow Rate"]

    @design_air_flow_rate.setter
    def design_air_flow_rate(self, value=None):
        """Corresponds to IDD field `Design Air Flow Rate` Design (maximum) air
        flow rate through the tower.

        Args:
            value (float or "Autosize"): value for IDD Field `Design Air Flow Rate`
                Units: m3/s
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Design Air Flow Rate"] = value

    @property
    def design_fan_power(self):
        """Get design_fan_power.

        Returns:
            float: the value of `design_fan_power` or None if not set

        """
        return self["Design Fan Power"]

    @design_fan_power.setter
    def design_fan_power(self, value=None):
        """  Corresponds to IDD field `Design Fan Power`
        Enter the fan motor electric input power at design (max) air flow through the tower
        Standard conversion for horsepower is 1 HP = 745.7 W

        Args:
            value (float or "Autosize"): value for IDD Field `Design Fan Power`
                Units: W
                IP-Units: W
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Design Fan Power"] = value

    @property
    def fan_power_ratio_function_of_air_flow_rate_ratio_curve_name(self):
        """Get fan_power_ratio_function_of_air_flow_rate_ratio_curve_name.

        Returns:
            str: the value of `fan_power_ratio_function_of_air_flow_rate_ratio_curve_name` or None if not set

        """
        return self[
            "Fan Power Ratio Function of Air Flow Rate Ratio Curve Name"]

    @fan_power_ratio_function_of_air_flow_rate_ratio_curve_name.setter
    def fan_power_ratio_function_of_air_flow_rate_ratio_curve_name(
            self,
            value=None):
        """  Corresponds to IDD field `Fan Power Ratio Function of Air Flow Rate Ratio Curve Name`
        Table:OneIndependentVariable object can also be used
        FPR = a + b*AFR + c*AFR**2 + d*AFR**3
        FPR = fraction of the design fan power
        AFR = fraction of the design air flow rate
        If left blank, then fan power is assumed to be proportional to
        (air flow rate ratio)^3

        Args:
            value (str): value for IDD Field `Fan Power Ratio Function of Air Flow Rate Ratio Curve Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self[
            "Fan Power Ratio Function of Air Flow Rate Ratio Curve Name"] = value

    @property
    def minimum_air_flow_rate_ratio(self):
        """Get minimum_air_flow_rate_ratio.

        Returns:
            float: the value of `minimum_air_flow_rate_ratio` or None if not set

        """
        return self["Minimum Air Flow Rate Ratio"]

    @minimum_air_flow_rate_ratio.setter
    def minimum_air_flow_rate_ratio(self, value=0.2):
        """  Corresponds to IDD field `Minimum Air Flow Rate Ratio`
        Enter the minimum air flow rate ratio. This is typically determined by the variable
        speed drive that controls the fan motor speed. Valid entries are from 0.2 to 0.5.

        Args:
            value (float): value for IDD Field `Minimum Air Flow Rate Ratio`
                Default value: 0.2
                value >= 0.2
                value <= 0.5
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Minimum Air Flow Rate Ratio"] = value

    @property
    def fraction_of_tower_capacity_in_free_convection_regime(self):
        """Get fraction_of_tower_capacity_in_free_convection_regime.

        Returns:
            float: the value of `fraction_of_tower_capacity_in_free_convection_regime` or None if not set

        """
        return self["Fraction of Tower Capacity in Free Convection Regime"]

    @fraction_of_tower_capacity_in_free_convection_regime.setter
    def fraction_of_tower_capacity_in_free_convection_regime(
            self,
            value=0.125):
        """  Corresponds to IDD field `Fraction of Tower Capacity in Free Convection Regime`
        Enter the fraction of tower capacity in the free convection regime. This is the
        fraction of the tower capacity, at the current inlet air wet-bulb temperature,
        that is available when the tower fan is off. Manufacturers typically estimate the
        free convection capacity at approximately 10-15%. Values are entered as a fraction
        and can range from 0 to 0.2.

        Args:
            value (float): value for IDD Field `Fraction of Tower Capacity in Free Convection Regime`
                Default value: 0.125
                value <= 0.2
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Fraction of Tower Capacity in Free Convection Regime"] = value

    @property
    def basin_heater_capacity(self):
        """Get basin_heater_capacity.

        Returns:
            float: the value of `basin_heater_capacity` or None if not set

        """
        return self["Basin Heater Capacity"]

    @basin_heater_capacity.setter
    def basin_heater_capacity(self, value=None):
        """Corresponds to IDD field `Basin Heater Capacity` This heater
        maintains the basin water temperature at the basin heater setpoint
        temperature when the outdoor air temperature falls below the setpoint
        temperature. The basin heater only operates when water is not flowing
        through the tower.

        Args:
            value (float): value for IDD Field `Basin Heater Capacity`
                Units: W/K
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Basin Heater Capacity"] = value

    @property
    def basin_heater_setpoint_temperature(self):
        """Get basin_heater_setpoint_temperature.

        Returns:
            float: the value of `basin_heater_setpoint_temperature` or None if not set

        """
        return self["Basin Heater Setpoint Temperature"]

    @basin_heater_setpoint_temperature.setter
    def basin_heater_setpoint_temperature(self, value=2.0):
        """  Corresponds to IDD field `Basin Heater Setpoint Temperature`
        Enter the outdoor dry-bulb temperature when the basin heater turns on

        Args:
            value (float): value for IDD Field `Basin Heater Setpoint Temperature`
                Units: C
                Default value: 2.0
                value >= 2.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Basin Heater Setpoint Temperature"] = value

    @property
    def basin_heater_operating_schedule_name(self):
        """Get basin_heater_operating_schedule_name.

        Returns:
            str: the value of `basin_heater_operating_schedule_name` or None if not set

        """
        return self["Basin Heater Operating Schedule Name"]

    @basin_heater_operating_schedule_name.setter
    def basin_heater_operating_schedule_name(self, value=None):
        """  Corresponds to IDD field `Basin Heater Operating Schedule Name`
        Schedule values greater than 0 allow the basin heater to operate whenever the outdoor
        air dry-bulb temperature is below the basin heater setpoint temperature.
        If a schedule name is not entered, the basin heater is allowed to operate
        throughout the entire simulation.

        Args:
            value (str): value for IDD Field `Basin Heater Operating Schedule Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Basin Heater Operating Schedule Name"] = value

    @property
    def evaporation_loss_mode(self):
        """Get evaporation_loss_mode.

        Returns:
            str: the value of `evaporation_loss_mode` or None if not set

        """
        return self["Evaporation Loss Mode"]

    @evaporation_loss_mode.setter
    def evaporation_loss_mode(self, value=None):
        """Corresponds to IDD field `Evaporation Loss Mode`

        Args:
            value (str): value for IDD Field `Evaporation Loss Mode`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Evaporation Loss Mode"] = value

    @property
    def evaporation_loss_factor(self):
        """Get evaporation_loss_factor.

        Returns:
            float: the value of `evaporation_loss_factor` or None if not set

        """
        return self["Evaporation Loss Factor"]

    @evaporation_loss_factor.setter
    def evaporation_loss_factor(self, value=0.2):
        """  Corresponds to IDD field `Evaporation Loss Factor`
        Rate of water evaporated from the cooling tower and lost to the outdoor air [%/K]
        Evaporation loss is calculated as percentage of the circulating condenser water rate
        Value entered here is percent-per-degree K of temperature drop in the condenser water
        Typical values are from 0.15 to 0.27 [percent/K].

        Args:
            value (float): value for IDD Field `Evaporation Loss Factor`
                Units: percent/K
                Default value: 0.2
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Evaporation Loss Factor"] = value

    @property
    def drift_loss_percent(self):
        """Get drift_loss_percent.

        Returns:
            float: the value of `drift_loss_percent` or None if not set

        """
        return self["Drift Loss Percent"]

    @drift_loss_percent.setter
    def drift_loss_percent(self, value=None):
        """  Corresponds to IDD field `Drift Loss Percent`
        Rate of drift loss as a percentage of circulating condenser water flow rate
        Typical values are between 0.002 and 0.2% The default value is 0.008%

        Args:
            value (float): value for IDD Field `Drift Loss Percent`
                Units: percent
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Drift Loss Percent"] = value

    @property
    def blowdown_calculation_mode(self):
        """Get blowdown_calculation_mode.

        Returns:
            str: the value of `blowdown_calculation_mode` or None if not set

        """
        return self["Blowdown Calculation Mode"]

    @blowdown_calculation_mode.setter
    def blowdown_calculation_mode(self, value=None):
        """Corresponds to IDD field `Blowdown Calculation Mode`

        Args:
            value (str): value for IDD Field `Blowdown Calculation Mode`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Blowdown Calculation Mode"] = value

    @property
    def blowdown_concentration_ratio(self):
        """Get blowdown_concentration_ratio.

        Returns:
            float: the value of `blowdown_concentration_ratio` or None if not set

        """
        return self["Blowdown Concentration Ratio"]

    @blowdown_concentration_ratio.setter
    def blowdown_concentration_ratio(self, value=3.0):
        """  Corresponds to IDD field `Blowdown Concentration Ratio`
        Characterizes the rate of blowdown in the cooling tower.
        Blowdown is water intentionally drained from the tower in order to offset the build up
        of solids in the water that would otherwise occur because of evaporation.
        Ratio of solids in the blowdown water to solids in the make up water.
        Typical values for tower operation are 3 to 5.  The default value is 3.

        Args:
            value (float): value for IDD Field `Blowdown Concentration Ratio`
                Default value: 3.0
                value >= 2.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Blowdown Concentration Ratio"] = value

    @property
    def blowdown_makeup_water_usage_schedule_name(self):
        """Get blowdown_makeup_water_usage_schedule_name.

        Returns:
            str: the value of `blowdown_makeup_water_usage_schedule_name` or None if not set

        """
        return self["Blowdown Makeup Water Usage Schedule Name"]

    @blowdown_makeup_water_usage_schedule_name.setter
    def blowdown_makeup_water_usage_schedule_name(self, value=None):
        """Corresponds to IDD field `Blowdown Makeup Water Usage Schedule Name`
        Makeup water usage due to blowdown results from occasionally draining a
        small amount of water in the tower basin to purge scale or other
        contaminants to reduce their concentration in order to maintain an
        acceptable level of water quality. Schedule values should reflect water
        usage in m3/s.

        Args:
            value (str): value for IDD Field `Blowdown Makeup Water Usage Schedule Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Blowdown Makeup Water Usage Schedule Name"] = value

    @property
    def supply_water_storage_tank_name(self):
        """Get supply_water_storage_tank_name.

        Returns:
            str: the value of `supply_water_storage_tank_name` or None if not set

        """
        return self["Supply Water Storage Tank Name"]

    @supply_water_storage_tank_name.setter
    def supply_water_storage_tank_name(self, value=None):
        """Corresponds to IDD field `Supply Water Storage Tank Name`

        Args:
            value (str): value for IDD Field `Supply Water Storage Tank Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Supply Water Storage Tank Name"] = value

    @property
    def outdoor_air_inlet_node_name(self):
        """Get outdoor_air_inlet_node_name.

        Returns:
            str: the value of `outdoor_air_inlet_node_name` or None if not set

        """
        return self["Outdoor Air Inlet Node Name"]

    @outdoor_air_inlet_node_name.setter
    def outdoor_air_inlet_node_name(self, value=None):
        """Corresponds to IDD field `Outdoor Air Inlet Node Name` Enter the
        name of an outdoor air node.

        Args:
            value (str): value for IDD Field `Outdoor Air Inlet Node Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Outdoor Air Inlet Node Name"] = value

    @property
    def number_of_cells(self):
        """Get number_of_cells.

        Returns:
            int: the value of `number_of_cells` or None if not set

        """
        return self["Number of Cells"]

    @number_of_cells.setter
    def number_of_cells(self, value=1):
        """Corresponds to IDD field `Number of Cells`

        Args:
            value (int): value for IDD Field `Number of Cells`
                Default value: 1
                value >= 1
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Number of Cells"] = value

    @property
    def cell_control(self):
        """Get cell_control.

        Returns:
            str: the value of `cell_control` or None if not set

        """
        return self["Cell Control"]

    @cell_control.setter
    def cell_control(self, value="MinimalCell"):
        """Corresponds to IDD field `Cell Control`

        Args:
            value (str): value for IDD Field `Cell Control`
                Default value: MinimalCell
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Cell Control"] = value

    @property
    def cell_minimum_water_flow_rate_fraction(self):
        """Get cell_minimum_water_flow_rate_fraction.

        Returns:
            float: the value of `cell_minimum_water_flow_rate_fraction` or None if not set

        """
        return self["Cell Minimum  Water Flow Rate Fraction"]

    @cell_minimum_water_flow_rate_fraction.setter
    def cell_minimum_water_flow_rate_fraction(self, value=0.33):
        """Corresponds to IDD field `Cell Minimum  Water Flow Rate Fraction`
        The allowable mininal fraction of the nominal flow rate per cell.

        Args:
            value (float): value for IDD Field `Cell Minimum  Water Flow Rate Fraction`
                Default value: 0.33
                value <= 1.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Cell Minimum  Water Flow Rate Fraction"] = value

    @property
    def cell_maximum_water_flow_rate_fraction(self):
        """Get cell_maximum_water_flow_rate_fraction.

        Returns:
            float: the value of `cell_maximum_water_flow_rate_fraction` or None if not set

        """
        return self["Cell Maximum Water Flow Rate Fraction"]

    @cell_maximum_water_flow_rate_fraction.setter
    def cell_maximum_water_flow_rate_fraction(self, value=2.5):
        """Corresponds to IDD field `Cell Maximum Water Flow Rate Fraction` The
        allowable maximal fraction of the nominal flow rate per cell.

        Args:
            value (float): value for IDD Field `Cell Maximum Water Flow Rate Fraction`
                Default value: 2.5
                value >= 1.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Cell Maximum Water Flow Rate Fraction"] = value

    @property
    def sizing_factor(self):
        """Get sizing_factor.

        Returns:
            float: the value of `sizing_factor` or None if not set

        """
        return self["Sizing Factor"]

    @sizing_factor.setter
    def sizing_factor(self, value=1.0):
        """Corresponds to IDD field `Sizing Factor` Multiplies the autosized
        capacity and flow rates.

        Args:
            value (float): value for IDD Field `Sizing Factor`
                Default value: 1.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Sizing Factor"] = value




class CoolingTowerPerformanceCoolTools(DataObject):

    """ Corresponds to IDD object `CoolingTowerPerformance:CoolTools`
        This object is used to define coefficients for the approach temperature
        correlation for a variable speed cooling tower when tower Model Type is
        specified as CoolToolsUserDefined in the object CoolingTower:VariableSpeed.
    """
    schema = {'extensible-fields': OrderedDict(),
              'fields': OrderedDict([(u'name',
                                      {'name': u'Name',
                                       'pyname': u'name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'alpha'}),
                                     (u'minimum inlet air wet-bulb temperature',
                                      {'name': u'Minimum Inlet Air Wet-Bulb Temperature',
                                       'pyname': u'minimum_inlet_air_wetbulb_temperature',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'C'}),
                                     (u'maximum inlet air wet-bulb temperature',
                                      {'name': u'Maximum Inlet Air Wet-Bulb Temperature',
                                       'pyname': u'maximum_inlet_air_wetbulb_temperature',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'C'}),
                                     (u'minimum range temperature',
                                      {'name': u'Minimum Range Temperature',
                                       'pyname': u'minimum_range_temperature',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'deltaC'}),
                                     (u'maximum range temperature',
                                      {'name': u'Maximum Range Temperature',
                                       'pyname': u'maximum_range_temperature',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'deltaC'}),
                                     (u'minimum approach temperature',
                                      {'name': u'Minimum Approach Temperature',
                                       'pyname': u'minimum_approach_temperature',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'deltaC'}),
                                     (u'maximum approach temperature',
                                      {'name': u'Maximum Approach Temperature',
                                       'pyname': u'maximum_approach_temperature',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'deltaC'}),
                                     (u'minimum water flow rate ratio',
                                      {'name': u'Minimum Water Flow Rate Ratio',
                                       'pyname': u'minimum_water_flow_rate_ratio',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'maximum water flow rate ratio',
                                      {'name': u'Maximum Water Flow Rate Ratio',
                                       'pyname': u'maximum_water_flow_rate_ratio',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient 1',
                                      {'name': u'Coefficient 1',
                                       'pyname': u'coefficient_1',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient 2',
                                      {'name': u'Coefficient 2',
                                       'pyname': u'coefficient_2',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient 3',
                                      {'name': u'Coefficient 3',
                                       'pyname': u'coefficient_3',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient 4',
                                      {'name': u'Coefficient 4',
                                       'pyname': u'coefficient_4',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient 5',
                                      {'name': u'Coefficient 5',
                                       'pyname': u'coefficient_5',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient 6',
                                      {'name': u'Coefficient 6',
                                       'pyname': u'coefficient_6',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient 7',
                                      {'name': u'Coefficient 7',
                                       'pyname': u'coefficient_7',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient 8',
                                      {'name': u'Coefficient 8',
                                       'pyname': u'coefficient_8',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient 9',
                                      {'name': u'Coefficient 9',
                                       'pyname': u'coefficient_9',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient 10',
                                      {'name': u'Coefficient 10',
                                       'pyname': u'coefficient_10',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient 11',
                                      {'name': u'Coefficient 11',
                                       'pyname': u'coefficient_11',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient 12',
                                      {'name': u'Coefficient 12',
                                       'pyname': u'coefficient_12',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient 13',
                                      {'name': u'Coefficient 13',
                                       'pyname': u'coefficient_13',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient 14',
                                      {'name': u'Coefficient 14',
                                       'pyname': u'coefficient_14',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient 15',
                                      {'name': u'Coefficient 15',
                                       'pyname': u'coefficient_15',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient 16',
                                      {'name': u'Coefficient 16',
                                       'pyname': u'coefficient_16',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient 17',
                                      {'name': u'Coefficient 17',
                                       'pyname': u'coefficient_17',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient 18',
                                      {'name': u'Coefficient 18',
                                       'pyname': u'coefficient_18',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient 19',
                                      {'name': u'Coefficient 19',
                                       'pyname': u'coefficient_19',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient 20',
                                      {'name': u'Coefficient 20',
                                       'pyname': u'coefficient_20',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient 21',
                                      {'name': u'Coefficient 21',
                                       'pyname': u'coefficient_21',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient 22',
                                      {'name': u'Coefficient 22',
                                       'pyname': u'coefficient_22',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient 23',
                                      {'name': u'Coefficient 23',
                                       'pyname': u'coefficient_23',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient 24',
                                      {'name': u'Coefficient 24',
                                       'pyname': u'coefficient_24',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient 25',
                                      {'name': u'Coefficient 25',
                                       'pyname': u'coefficient_25',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient 26',
                                      {'name': u'Coefficient 26',
                                       'pyname': u'coefficient_26',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient 27',
                                      {'name': u'Coefficient 27',
                                       'pyname': u'coefficient_27',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient 28',
                                      {'name': u'Coefficient 28',
                                       'pyname': u'coefficient_28',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient 29',
                                      {'name': u'Coefficient 29',
                                       'pyname': u'coefficient_29',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient 30',
                                      {'name': u'Coefficient 30',
                                       'pyname': u'coefficient_30',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient 31',
                                      {'name': u'Coefficient 31',
                                       'pyname': u'coefficient_31',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient 32',
                                      {'name': u'Coefficient 32',
                                       'pyname': u'coefficient_32',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient 33',
                                      {'name': u'Coefficient 33',
                                       'pyname': u'coefficient_33',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient 34',
                                      {'name': u'Coefficient 34',
                                       'pyname': u'coefficient_34',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient 35',
                                      {'name': u'Coefficient 35',
                                       'pyname': u'coefficient_35',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'})]),
              'format': None,
              'group': u'Condenser Equipment and Heat Exchangers',
              'min-fields': 44,
              'name': u'CoolingTowerPerformance:CoolTools',
              'pyname': u'CoolingTowerPerformanceCoolTools',
              'required-object': False,
              'unique-object': False}

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
    def minimum_inlet_air_wetbulb_temperature(self):
        """Get minimum_inlet_air_wetbulb_temperature.

        Returns:
            float: the value of `minimum_inlet_air_wetbulb_temperature` or None if not set

        """
        return self["Minimum Inlet Air Wet-Bulb Temperature"]

    @minimum_inlet_air_wetbulb_temperature.setter
    def minimum_inlet_air_wetbulb_temperature(self, value=None):
        """  Corresponds to IDD field `Minimum Inlet Air Wet-Bulb Temperature`
        Minimum valid inlet air wet-bulb temperature for this approach
        temperature correlation.

        Args:
            value (float): value for IDD Field `Minimum Inlet Air Wet-Bulb Temperature`
                Units: C
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Minimum Inlet Air Wet-Bulb Temperature"] = value

    @property
    def maximum_inlet_air_wetbulb_temperature(self):
        """Get maximum_inlet_air_wetbulb_temperature.

        Returns:
            float: the value of `maximum_inlet_air_wetbulb_temperature` or None if not set

        """
        return self["Maximum Inlet Air Wet-Bulb Temperature"]

    @maximum_inlet_air_wetbulb_temperature.setter
    def maximum_inlet_air_wetbulb_temperature(self, value=None):
        """  Corresponds to IDD field `Maximum Inlet Air Wet-Bulb Temperature`
        Maximum valid inlet air wet-bulb temperature for this approach
        temperature correlation.

        Args:
            value (float): value for IDD Field `Maximum Inlet Air Wet-Bulb Temperature`
                Units: C
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Maximum Inlet Air Wet-Bulb Temperature"] = value

    @property
    def minimum_range_temperature(self):
        """Get minimum_range_temperature.

        Returns:
            float: the value of `minimum_range_temperature` or None if not set

        """
        return self["Minimum Range Temperature"]

    @minimum_range_temperature.setter
    def minimum_range_temperature(self, value=None):
        """Corresponds to IDD field `Minimum Range Temperature` Minimum valid
        range temperature for this approach temperature correlation.

        Args:
            value (float): value for IDD Field `Minimum Range Temperature`
                Units: deltaC
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Minimum Range Temperature"] = value

    @property
    def maximum_range_temperature(self):
        """Get maximum_range_temperature.

        Returns:
            float: the value of `maximum_range_temperature` or None if not set

        """
        return self["Maximum Range Temperature"]

    @maximum_range_temperature.setter
    def maximum_range_temperature(self, value=None):
        """Corresponds to IDD field `Maximum Range Temperature` Maximum valid
        range temperature for this approach temperature correlation.

        Args:
            value (float): value for IDD Field `Maximum Range Temperature`
                Units: deltaC
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Maximum Range Temperature"] = value

    @property
    def minimum_approach_temperature(self):
        """Get minimum_approach_temperature.

        Returns:
            float: the value of `minimum_approach_temperature` or None if not set

        """
        return self["Minimum Approach Temperature"]

    @minimum_approach_temperature.setter
    def minimum_approach_temperature(self, value=None):
        """Corresponds to IDD field `Minimum Approach Temperature` Minimum
        valid approach temperature for this correlation.

        Args:
            value (float): value for IDD Field `Minimum Approach Temperature`
                Units: deltaC
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Minimum Approach Temperature"] = value

    @property
    def maximum_approach_temperature(self):
        """Get maximum_approach_temperature.

        Returns:
            float: the value of `maximum_approach_temperature` or None if not set

        """
        return self["Maximum Approach Temperature"]

    @maximum_approach_temperature.setter
    def maximum_approach_temperature(self, value=None):
        """Corresponds to IDD field `Maximum Approach Temperature` Maximum
        valid approach temperature for this correlation.

        Args:
            value (float): value for IDD Field `Maximum Approach Temperature`
                Units: deltaC
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Maximum Approach Temperature"] = value

    @property
    def minimum_water_flow_rate_ratio(self):
        """Get minimum_water_flow_rate_ratio.

        Returns:
            float: the value of `minimum_water_flow_rate_ratio` or None if not set

        """
        return self["Minimum Water Flow Rate Ratio"]

    @minimum_water_flow_rate_ratio.setter
    def minimum_water_flow_rate_ratio(self, value=None):
        """Corresponds to IDD field `Minimum Water Flow Rate Ratio` Minimum
        valid water flow rate ratio for this approach temperature correlation.

        Args:
            value (float): value for IDD Field `Minimum Water Flow Rate Ratio`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Minimum Water Flow Rate Ratio"] = value

    @property
    def maximum_water_flow_rate_ratio(self):
        """Get maximum_water_flow_rate_ratio.

        Returns:
            float: the value of `maximum_water_flow_rate_ratio` or None if not set

        """
        return self["Maximum Water Flow Rate Ratio"]

    @maximum_water_flow_rate_ratio.setter
    def maximum_water_flow_rate_ratio(self, value=None):
        """Corresponds to IDD field `Maximum Water Flow Rate Ratio` Maximum
        valid water flow rate ratio for this approach temperature correlation.

        Args:
            value (float): value for IDD Field `Maximum Water Flow Rate Ratio`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Maximum Water Flow Rate Ratio"] = value

    @property
    def coefficient_1(self):
        """Get coefficient_1.

        Returns:
            float: the value of `coefficient_1` or None if not set

        """
        return self["Coefficient 1"]

    @coefficient_1.setter
    def coefficient_1(self, value=None):
        """Corresponds to IDD field `Coefficient 1`

        Args:
            value (float): value for IDD Field `Coefficient 1`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient 1"] = value

    @property
    def coefficient_2(self):
        """Get coefficient_2.

        Returns:
            float: the value of `coefficient_2` or None if not set

        """
        return self["Coefficient 2"]

    @coefficient_2.setter
    def coefficient_2(self, value=None):
        """Corresponds to IDD field `Coefficient 2`

        Args:
            value (float): value for IDD Field `Coefficient 2`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient 2"] = value

    @property
    def coefficient_3(self):
        """Get coefficient_3.

        Returns:
            float: the value of `coefficient_3` or None if not set

        """
        return self["Coefficient 3"]

    @coefficient_3.setter
    def coefficient_3(self, value=None):
        """Corresponds to IDD field `Coefficient 3`

        Args:
            value (float): value for IDD Field `Coefficient 3`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient 3"] = value

    @property
    def coefficient_4(self):
        """Get coefficient_4.

        Returns:
            float: the value of `coefficient_4` or None if not set

        """
        return self["Coefficient 4"]

    @coefficient_4.setter
    def coefficient_4(self, value=None):
        """Corresponds to IDD field `Coefficient 4`

        Args:
            value (float): value for IDD Field `Coefficient 4`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient 4"] = value

    @property
    def coefficient_5(self):
        """Get coefficient_5.

        Returns:
            float: the value of `coefficient_5` or None if not set

        """
        return self["Coefficient 5"]

    @coefficient_5.setter
    def coefficient_5(self, value=None):
        """Corresponds to IDD field `Coefficient 5`

        Args:
            value (float): value for IDD Field `Coefficient 5`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient 5"] = value

    @property
    def coefficient_6(self):
        """Get coefficient_6.

        Returns:
            float: the value of `coefficient_6` or None if not set

        """
        return self["Coefficient 6"]

    @coefficient_6.setter
    def coefficient_6(self, value=None):
        """Corresponds to IDD field `Coefficient 6`

        Args:
            value (float): value for IDD Field `Coefficient 6`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient 6"] = value

    @property
    def coefficient_7(self):
        """Get coefficient_7.

        Returns:
            float: the value of `coefficient_7` or None if not set

        """
        return self["Coefficient 7"]

    @coefficient_7.setter
    def coefficient_7(self, value=None):
        """Corresponds to IDD field `Coefficient 7`

        Args:
            value (float): value for IDD Field `Coefficient 7`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient 7"] = value

    @property
    def coefficient_8(self):
        """Get coefficient_8.

        Returns:
            float: the value of `coefficient_8` or None if not set

        """
        return self["Coefficient 8"]

    @coefficient_8.setter
    def coefficient_8(self, value=None):
        """Corresponds to IDD field `Coefficient 8`

        Args:
            value (float): value for IDD Field `Coefficient 8`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient 8"] = value

    @property
    def coefficient_9(self):
        """Get coefficient_9.

        Returns:
            float: the value of `coefficient_9` or None if not set

        """
        return self["Coefficient 9"]

    @coefficient_9.setter
    def coefficient_9(self, value=None):
        """Corresponds to IDD field `Coefficient 9`

        Args:
            value (float): value for IDD Field `Coefficient 9`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient 9"] = value

    @property
    def coefficient_10(self):
        """Get coefficient_10.

        Returns:
            float: the value of `coefficient_10` or None if not set

        """
        return self["Coefficient 10"]

    @coefficient_10.setter
    def coefficient_10(self, value=None):
        """Corresponds to IDD field `Coefficient 10`

        Args:
            value (float): value for IDD Field `Coefficient 10`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient 10"] = value

    @property
    def coefficient_11(self):
        """Get coefficient_11.

        Returns:
            float: the value of `coefficient_11` or None if not set

        """
        return self["Coefficient 11"]

    @coefficient_11.setter
    def coefficient_11(self, value=None):
        """Corresponds to IDD field `Coefficient 11`

        Args:
            value (float): value for IDD Field `Coefficient 11`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient 11"] = value

    @property
    def coefficient_12(self):
        """Get coefficient_12.

        Returns:
            float: the value of `coefficient_12` or None if not set

        """
        return self["Coefficient 12"]

    @coefficient_12.setter
    def coefficient_12(self, value=None):
        """Corresponds to IDD field `Coefficient 12`

        Args:
            value (float): value for IDD Field `Coefficient 12`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient 12"] = value

    @property
    def coefficient_13(self):
        """Get coefficient_13.

        Returns:
            float: the value of `coefficient_13` or None if not set

        """
        return self["Coefficient 13"]

    @coefficient_13.setter
    def coefficient_13(self, value=None):
        """Corresponds to IDD field `Coefficient 13`

        Args:
            value (float): value for IDD Field `Coefficient 13`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient 13"] = value

    @property
    def coefficient_14(self):
        """Get coefficient_14.

        Returns:
            float: the value of `coefficient_14` or None if not set

        """
        return self["Coefficient 14"]

    @coefficient_14.setter
    def coefficient_14(self, value=None):
        """Corresponds to IDD field `Coefficient 14`

        Args:
            value (float): value for IDD Field `Coefficient 14`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient 14"] = value

    @property
    def coefficient_15(self):
        """Get coefficient_15.

        Returns:
            float: the value of `coefficient_15` or None if not set

        """
        return self["Coefficient 15"]

    @coefficient_15.setter
    def coefficient_15(self, value=None):
        """Corresponds to IDD field `Coefficient 15`

        Args:
            value (float): value for IDD Field `Coefficient 15`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient 15"] = value

    @property
    def coefficient_16(self):
        """Get coefficient_16.

        Returns:
            float: the value of `coefficient_16` or None if not set

        """
        return self["Coefficient 16"]

    @coefficient_16.setter
    def coefficient_16(self, value=None):
        """Corresponds to IDD field `Coefficient 16`

        Args:
            value (float): value for IDD Field `Coefficient 16`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient 16"] = value

    @property
    def coefficient_17(self):
        """Get coefficient_17.

        Returns:
            float: the value of `coefficient_17` or None if not set

        """
        return self["Coefficient 17"]

    @coefficient_17.setter
    def coefficient_17(self, value=None):
        """Corresponds to IDD field `Coefficient 17`

        Args:
            value (float): value for IDD Field `Coefficient 17`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient 17"] = value

    @property
    def coefficient_18(self):
        """Get coefficient_18.

        Returns:
            float: the value of `coefficient_18` or None if not set

        """
        return self["Coefficient 18"]

    @coefficient_18.setter
    def coefficient_18(self, value=None):
        """Corresponds to IDD field `Coefficient 18`

        Args:
            value (float): value for IDD Field `Coefficient 18`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient 18"] = value

    @property
    def coefficient_19(self):
        """Get coefficient_19.

        Returns:
            float: the value of `coefficient_19` or None if not set

        """
        return self["Coefficient 19"]

    @coefficient_19.setter
    def coefficient_19(self, value=None):
        """Corresponds to IDD field `Coefficient 19`

        Args:
            value (float): value for IDD Field `Coefficient 19`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient 19"] = value

    @property
    def coefficient_20(self):
        """Get coefficient_20.

        Returns:
            float: the value of `coefficient_20` or None if not set

        """
        return self["Coefficient 20"]

    @coefficient_20.setter
    def coefficient_20(self, value=None):
        """Corresponds to IDD field `Coefficient 20`

        Args:
            value (float): value for IDD Field `Coefficient 20`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient 20"] = value

    @property
    def coefficient_21(self):
        """Get coefficient_21.

        Returns:
            float: the value of `coefficient_21` or None if not set

        """
        return self["Coefficient 21"]

    @coefficient_21.setter
    def coefficient_21(self, value=None):
        """Corresponds to IDD field `Coefficient 21`

        Args:
            value (float): value for IDD Field `Coefficient 21`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient 21"] = value

    @property
    def coefficient_22(self):
        """Get coefficient_22.

        Returns:
            float: the value of `coefficient_22` or None if not set

        """
        return self["Coefficient 22"]

    @coefficient_22.setter
    def coefficient_22(self, value=None):
        """Corresponds to IDD field `Coefficient 22`

        Args:
            value (float): value for IDD Field `Coefficient 22`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient 22"] = value

    @property
    def coefficient_23(self):
        """Get coefficient_23.

        Returns:
            float: the value of `coefficient_23` or None if not set

        """
        return self["Coefficient 23"]

    @coefficient_23.setter
    def coefficient_23(self, value=None):
        """Corresponds to IDD field `Coefficient 23`

        Args:
            value (float): value for IDD Field `Coefficient 23`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient 23"] = value

    @property
    def coefficient_24(self):
        """Get coefficient_24.

        Returns:
            float: the value of `coefficient_24` or None if not set

        """
        return self["Coefficient 24"]

    @coefficient_24.setter
    def coefficient_24(self, value=None):
        """Corresponds to IDD field `Coefficient 24`

        Args:
            value (float): value for IDD Field `Coefficient 24`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient 24"] = value

    @property
    def coefficient_25(self):
        """Get coefficient_25.

        Returns:
            float: the value of `coefficient_25` or None if not set

        """
        return self["Coefficient 25"]

    @coefficient_25.setter
    def coefficient_25(self, value=None):
        """Corresponds to IDD field `Coefficient 25`

        Args:
            value (float): value for IDD Field `Coefficient 25`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient 25"] = value

    @property
    def coefficient_26(self):
        """Get coefficient_26.

        Returns:
            float: the value of `coefficient_26` or None if not set

        """
        return self["Coefficient 26"]

    @coefficient_26.setter
    def coefficient_26(self, value=None):
        """Corresponds to IDD field `Coefficient 26`

        Args:
            value (float): value for IDD Field `Coefficient 26`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient 26"] = value

    @property
    def coefficient_27(self):
        """Get coefficient_27.

        Returns:
            float: the value of `coefficient_27` or None if not set

        """
        return self["Coefficient 27"]

    @coefficient_27.setter
    def coefficient_27(self, value=None):
        """Corresponds to IDD field `Coefficient 27`

        Args:
            value (float): value for IDD Field `Coefficient 27`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient 27"] = value

    @property
    def coefficient_28(self):
        """Get coefficient_28.

        Returns:
            float: the value of `coefficient_28` or None if not set

        """
        return self["Coefficient 28"]

    @coefficient_28.setter
    def coefficient_28(self, value=None):
        """Corresponds to IDD field `Coefficient 28`

        Args:
            value (float): value for IDD Field `Coefficient 28`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient 28"] = value

    @property
    def coefficient_29(self):
        """Get coefficient_29.

        Returns:
            float: the value of `coefficient_29` or None if not set

        """
        return self["Coefficient 29"]

    @coefficient_29.setter
    def coefficient_29(self, value=None):
        """Corresponds to IDD field `Coefficient 29`

        Args:
            value (float): value for IDD Field `Coefficient 29`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient 29"] = value

    @property
    def coefficient_30(self):
        """Get coefficient_30.

        Returns:
            float: the value of `coefficient_30` or None if not set

        """
        return self["Coefficient 30"]

    @coefficient_30.setter
    def coefficient_30(self, value=None):
        """Corresponds to IDD field `Coefficient 30`

        Args:
            value (float): value for IDD Field `Coefficient 30`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient 30"] = value

    @property
    def coefficient_31(self):
        """Get coefficient_31.

        Returns:
            float: the value of `coefficient_31` or None if not set

        """
        return self["Coefficient 31"]

    @coefficient_31.setter
    def coefficient_31(self, value=None):
        """Corresponds to IDD field `Coefficient 31`

        Args:
            value (float): value for IDD Field `Coefficient 31`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient 31"] = value

    @property
    def coefficient_32(self):
        """Get coefficient_32.

        Returns:
            float: the value of `coefficient_32` or None if not set

        """
        return self["Coefficient 32"]

    @coefficient_32.setter
    def coefficient_32(self, value=None):
        """Corresponds to IDD field `Coefficient 32`

        Args:
            value (float): value for IDD Field `Coefficient 32`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient 32"] = value

    @property
    def coefficient_33(self):
        """Get coefficient_33.

        Returns:
            float: the value of `coefficient_33` or None if not set

        """
        return self["Coefficient 33"]

    @coefficient_33.setter
    def coefficient_33(self, value=None):
        """Corresponds to IDD field `Coefficient 33`

        Args:
            value (float): value for IDD Field `Coefficient 33`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient 33"] = value

    @property
    def coefficient_34(self):
        """Get coefficient_34.

        Returns:
            float: the value of `coefficient_34` or None if not set

        """
        return self["Coefficient 34"]

    @coefficient_34.setter
    def coefficient_34(self, value=None):
        """Corresponds to IDD field `Coefficient 34`

        Args:
            value (float): value for IDD Field `Coefficient 34`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient 34"] = value

    @property
    def coefficient_35(self):
        """Get coefficient_35.

        Returns:
            float: the value of `coefficient_35` or None if not set

        """
        return self["Coefficient 35"]

    @coefficient_35.setter
    def coefficient_35(self, value=None):
        """Corresponds to IDD field `Coefficient 35`

        Args:
            value (float): value for IDD Field `Coefficient 35`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient 35"] = value




class CoolingTowerPerformanceYorkCalc(DataObject):

    """ Corresponds to IDD object `CoolingTowerPerformance:YorkCalc`
        This object is used to define coefficients for the approach temperature
        correlation for a variable speed cooling tower when tower Model Type is
        specified as YorkCalcUserDefined in the object CoolingTower:VariableSpeed.
    """
    schema = {'extensible-fields': OrderedDict(),
              'fields': OrderedDict([(u'name',
                                      {'name': u'Name',
                                       'pyname': u'name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'alpha'}),
                                     (u'minimum inlet air wet-bulb temperature',
                                      {'name': u'Minimum Inlet Air Wet-Bulb Temperature',
                                       'pyname': u'minimum_inlet_air_wetbulb_temperature',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'C'}),
                                     (u'maximum inlet air wet-bulb temperature',
                                      {'name': u'Maximum Inlet Air Wet-Bulb Temperature',
                                       'pyname': u'maximum_inlet_air_wetbulb_temperature',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'C'}),
                                     (u'minimum range temperature',
                                      {'name': u'Minimum Range Temperature',
                                       'pyname': u'minimum_range_temperature',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'deltaC'}),
                                     (u'maximum range temperature',
                                      {'name': u'Maximum Range Temperature',
                                       'pyname': u'maximum_range_temperature',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'deltaC'}),
                                     (u'minimum approach temperature',
                                      {'name': u'Minimum Approach Temperature',
                                       'pyname': u'minimum_approach_temperature',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'deltaC'}),
                                     (u'maximum approach temperature',
                                      {'name': u'Maximum Approach Temperature',
                                       'pyname': u'maximum_approach_temperature',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'deltaC'}),
                                     (u'minimum water flow rate ratio',
                                      {'name': u'Minimum Water Flow Rate Ratio',
                                       'pyname': u'minimum_water_flow_rate_ratio',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'maximum water flow rate ratio',
                                      {'name': u'Maximum Water Flow Rate Ratio',
                                       'pyname': u'maximum_water_flow_rate_ratio',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'maximum liquid to gas ratio',
                                      {'name': u'Maximum Liquid to Gas Ratio',
                                       'pyname': u'maximum_liquid_to_gas_ratio',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient 1',
                                      {'name': u'Coefficient 1',
                                       'pyname': u'coefficient_1',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient 2',
                                      {'name': u'Coefficient 2',
                                       'pyname': u'coefficient_2',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient 3',
                                      {'name': u'Coefficient 3',
                                       'pyname': u'coefficient_3',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient 4',
                                      {'name': u'Coefficient 4',
                                       'pyname': u'coefficient_4',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient 5',
                                      {'name': u'Coefficient 5',
                                       'pyname': u'coefficient_5',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient 6',
                                      {'name': u'Coefficient 6',
                                       'pyname': u'coefficient_6',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient 7',
                                      {'name': u'Coefficient 7',
                                       'pyname': u'coefficient_7',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient 8',
                                      {'name': u'Coefficient 8',
                                       'pyname': u'coefficient_8',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient 9',
                                      {'name': u'Coefficient 9',
                                       'pyname': u'coefficient_9',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient 10',
                                      {'name': u'Coefficient 10',
                                       'pyname': u'coefficient_10',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient 11',
                                      {'name': u'Coefficient 11',
                                       'pyname': u'coefficient_11',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient 12',
                                      {'name': u'Coefficient 12',
                                       'pyname': u'coefficient_12',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient 13',
                                      {'name': u'Coefficient 13',
                                       'pyname': u'coefficient_13',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient 14',
                                      {'name': u'Coefficient 14',
                                       'pyname': u'coefficient_14',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient 15',
                                      {'name': u'Coefficient 15',
                                       'pyname': u'coefficient_15',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient 16',
                                      {'name': u'Coefficient 16',
                                       'pyname': u'coefficient_16',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient 17',
                                      {'name': u'Coefficient 17',
                                       'pyname': u'coefficient_17',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient 18',
                                      {'name': u'Coefficient 18',
                                       'pyname': u'coefficient_18',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient 19',
                                      {'name': u'Coefficient 19',
                                       'pyname': u'coefficient_19',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient 20',
                                      {'name': u'Coefficient 20',
                                       'pyname': u'coefficient_20',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient 21',
                                      {'name': u'Coefficient 21',
                                       'pyname': u'coefficient_21',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient 22',
                                      {'name': u'Coefficient 22',
                                       'pyname': u'coefficient_22',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient 23',
                                      {'name': u'Coefficient 23',
                                       'pyname': u'coefficient_23',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient 24',
                                      {'name': u'Coefficient 24',
                                       'pyname': u'coefficient_24',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient 25',
                                      {'name': u'Coefficient 25',
                                       'pyname': u'coefficient_25',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient 26',
                                      {'name': u'Coefficient 26',
                                       'pyname': u'coefficient_26',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'coefficient 27',
                                      {'name': u'Coefficient 27',
                                       'pyname': u'coefficient_27',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'})]),
              'format': None,
              'group': u'Condenser Equipment and Heat Exchangers',
              'min-fields': 37,
              'name': u'CoolingTowerPerformance:YorkCalc',
              'pyname': u'CoolingTowerPerformanceYorkCalc',
              'required-object': False,
              'unique-object': False}

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
    def minimum_inlet_air_wetbulb_temperature(self):
        """Get minimum_inlet_air_wetbulb_temperature.

        Returns:
            float: the value of `minimum_inlet_air_wetbulb_temperature` or None if not set

        """
        return self["Minimum Inlet Air Wet-Bulb Temperature"]

    @minimum_inlet_air_wetbulb_temperature.setter
    def minimum_inlet_air_wetbulb_temperature(self, value=None):
        """  Corresponds to IDD field `Minimum Inlet Air Wet-Bulb Temperature`
        Minimum valid inlet air wet-bulb temperature for this approach
        temperature correlation.

        Args:
            value (float): value for IDD Field `Minimum Inlet Air Wet-Bulb Temperature`
                Units: C
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Minimum Inlet Air Wet-Bulb Temperature"] = value

    @property
    def maximum_inlet_air_wetbulb_temperature(self):
        """Get maximum_inlet_air_wetbulb_temperature.

        Returns:
            float: the value of `maximum_inlet_air_wetbulb_temperature` or None if not set

        """
        return self["Maximum Inlet Air Wet-Bulb Temperature"]

    @maximum_inlet_air_wetbulb_temperature.setter
    def maximum_inlet_air_wetbulb_temperature(self, value=None):
        """  Corresponds to IDD field `Maximum Inlet Air Wet-Bulb Temperature`
        Maximum valid inlet air wet-bulb temperature for this approach
        temperature correlation.

        Args:
            value (float): value for IDD Field `Maximum Inlet Air Wet-Bulb Temperature`
                Units: C
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Maximum Inlet Air Wet-Bulb Temperature"] = value

    @property
    def minimum_range_temperature(self):
        """Get minimum_range_temperature.

        Returns:
            float: the value of `minimum_range_temperature` or None if not set

        """
        return self["Minimum Range Temperature"]

    @minimum_range_temperature.setter
    def minimum_range_temperature(self, value=None):
        """Corresponds to IDD field `Minimum Range Temperature` Minimum valid
        range temperature for this approach temperature correlation.

        Args:
            value (float): value for IDD Field `Minimum Range Temperature`
                Units: deltaC
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Minimum Range Temperature"] = value

    @property
    def maximum_range_temperature(self):
        """Get maximum_range_temperature.

        Returns:
            float: the value of `maximum_range_temperature` or None if not set

        """
        return self["Maximum Range Temperature"]

    @maximum_range_temperature.setter
    def maximum_range_temperature(self, value=None):
        """Corresponds to IDD field `Maximum Range Temperature` Maximum valid
        range temperature for this approach temperature correlation.

        Args:
            value (float): value for IDD Field `Maximum Range Temperature`
                Units: deltaC
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Maximum Range Temperature"] = value

    @property
    def minimum_approach_temperature(self):
        """Get minimum_approach_temperature.

        Returns:
            float: the value of `minimum_approach_temperature` or None if not set

        """
        return self["Minimum Approach Temperature"]

    @minimum_approach_temperature.setter
    def minimum_approach_temperature(self, value=None):
        """Corresponds to IDD field `Minimum Approach Temperature` Minimum
        valid approach temperature for this correlation.

        Args:
            value (float): value for IDD Field `Minimum Approach Temperature`
                Units: deltaC
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Minimum Approach Temperature"] = value

    @property
    def maximum_approach_temperature(self):
        """Get maximum_approach_temperature.

        Returns:
            float: the value of `maximum_approach_temperature` or None if not set

        """
        return self["Maximum Approach Temperature"]

    @maximum_approach_temperature.setter
    def maximum_approach_temperature(self, value=None):
        """Corresponds to IDD field `Maximum Approach Temperature` Maximum
        valid approach temperature for this correlation.

        Args:
            value (float): value for IDD Field `Maximum Approach Temperature`
                Units: deltaC
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Maximum Approach Temperature"] = value

    @property
    def minimum_water_flow_rate_ratio(self):
        """Get minimum_water_flow_rate_ratio.

        Returns:
            float: the value of `minimum_water_flow_rate_ratio` or None if not set

        """
        return self["Minimum Water Flow Rate Ratio"]

    @minimum_water_flow_rate_ratio.setter
    def minimum_water_flow_rate_ratio(self, value=None):
        """Corresponds to IDD field `Minimum Water Flow Rate Ratio` Minimum
        valid water flow rate ratio for this approach temperature correlation.

        Args:
            value (float): value for IDD Field `Minimum Water Flow Rate Ratio`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Minimum Water Flow Rate Ratio"] = value

    @property
    def maximum_water_flow_rate_ratio(self):
        """Get maximum_water_flow_rate_ratio.

        Returns:
            float: the value of `maximum_water_flow_rate_ratio` or None if not set

        """
        return self["Maximum Water Flow Rate Ratio"]

    @maximum_water_flow_rate_ratio.setter
    def maximum_water_flow_rate_ratio(self, value=None):
        """Corresponds to IDD field `Maximum Water Flow Rate Ratio` Maximum
        valid water flow rate ratio for this approach temperature correlation.

        Args:
            value (float): value for IDD Field `Maximum Water Flow Rate Ratio`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Maximum Water Flow Rate Ratio"] = value

    @property
    def maximum_liquid_to_gas_ratio(self):
        """Get maximum_liquid_to_gas_ratio.

        Returns:
            float: the value of `maximum_liquid_to_gas_ratio` or None if not set

        """
        return self["Maximum Liquid to Gas Ratio"]

    @maximum_liquid_to_gas_ratio.setter
    def maximum_liquid_to_gas_ratio(self, value=None):
        """Corresponds to IDD field `Maximum Liquid to Gas Ratio` Maximum
        liquid (water) to gas (air) ratio for this approach temperature
        correlation.

        Args:
            value (float): value for IDD Field `Maximum Liquid to Gas Ratio`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Maximum Liquid to Gas Ratio"] = value

    @property
    def coefficient_1(self):
        """Get coefficient_1.

        Returns:
            float: the value of `coefficient_1` or None if not set

        """
        return self["Coefficient 1"]

    @coefficient_1.setter
    def coefficient_1(self, value=None):
        """Corresponds to IDD field `Coefficient 1`

        Args:
            value (float): value for IDD Field `Coefficient 1`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient 1"] = value

    @property
    def coefficient_2(self):
        """Get coefficient_2.

        Returns:
            float: the value of `coefficient_2` or None if not set

        """
        return self["Coefficient 2"]

    @coefficient_2.setter
    def coefficient_2(self, value=None):
        """Corresponds to IDD field `Coefficient 2`

        Args:
            value (float): value for IDD Field `Coefficient 2`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient 2"] = value

    @property
    def coefficient_3(self):
        """Get coefficient_3.

        Returns:
            float: the value of `coefficient_3` or None if not set

        """
        return self["Coefficient 3"]

    @coefficient_3.setter
    def coefficient_3(self, value=None):
        """Corresponds to IDD field `Coefficient 3`

        Args:
            value (float): value for IDD Field `Coefficient 3`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient 3"] = value

    @property
    def coefficient_4(self):
        """Get coefficient_4.

        Returns:
            float: the value of `coefficient_4` or None if not set

        """
        return self["Coefficient 4"]

    @coefficient_4.setter
    def coefficient_4(self, value=None):
        """Corresponds to IDD field `Coefficient 4`

        Args:
            value (float): value for IDD Field `Coefficient 4`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient 4"] = value

    @property
    def coefficient_5(self):
        """Get coefficient_5.

        Returns:
            float: the value of `coefficient_5` or None if not set

        """
        return self["Coefficient 5"]

    @coefficient_5.setter
    def coefficient_5(self, value=None):
        """Corresponds to IDD field `Coefficient 5`

        Args:
            value (float): value for IDD Field `Coefficient 5`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient 5"] = value

    @property
    def coefficient_6(self):
        """Get coefficient_6.

        Returns:
            float: the value of `coefficient_6` or None if not set

        """
        return self["Coefficient 6"]

    @coefficient_6.setter
    def coefficient_6(self, value=None):
        """Corresponds to IDD field `Coefficient 6`

        Args:
            value (float): value for IDD Field `Coefficient 6`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient 6"] = value

    @property
    def coefficient_7(self):
        """Get coefficient_7.

        Returns:
            float: the value of `coefficient_7` or None if not set

        """
        return self["Coefficient 7"]

    @coefficient_7.setter
    def coefficient_7(self, value=None):
        """Corresponds to IDD field `Coefficient 7`

        Args:
            value (float): value for IDD Field `Coefficient 7`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient 7"] = value

    @property
    def coefficient_8(self):
        """Get coefficient_8.

        Returns:
            float: the value of `coefficient_8` or None if not set

        """
        return self["Coefficient 8"]

    @coefficient_8.setter
    def coefficient_8(self, value=None):
        """Corresponds to IDD field `Coefficient 8`

        Args:
            value (float): value for IDD Field `Coefficient 8`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient 8"] = value

    @property
    def coefficient_9(self):
        """Get coefficient_9.

        Returns:
            float: the value of `coefficient_9` or None if not set

        """
        return self["Coefficient 9"]

    @coefficient_9.setter
    def coefficient_9(self, value=None):
        """Corresponds to IDD field `Coefficient 9`

        Args:
            value (float): value for IDD Field `Coefficient 9`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient 9"] = value

    @property
    def coefficient_10(self):
        """Get coefficient_10.

        Returns:
            float: the value of `coefficient_10` or None if not set

        """
        return self["Coefficient 10"]

    @coefficient_10.setter
    def coefficient_10(self, value=None):
        """Corresponds to IDD field `Coefficient 10`

        Args:
            value (float): value for IDD Field `Coefficient 10`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient 10"] = value

    @property
    def coefficient_11(self):
        """Get coefficient_11.

        Returns:
            float: the value of `coefficient_11` or None if not set

        """
        return self["Coefficient 11"]

    @coefficient_11.setter
    def coefficient_11(self, value=None):
        """Corresponds to IDD field `Coefficient 11`

        Args:
            value (float): value for IDD Field `Coefficient 11`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient 11"] = value

    @property
    def coefficient_12(self):
        """Get coefficient_12.

        Returns:
            float: the value of `coefficient_12` or None if not set

        """
        return self["Coefficient 12"]

    @coefficient_12.setter
    def coefficient_12(self, value=None):
        """Corresponds to IDD field `Coefficient 12`

        Args:
            value (float): value for IDD Field `Coefficient 12`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient 12"] = value

    @property
    def coefficient_13(self):
        """Get coefficient_13.

        Returns:
            float: the value of `coefficient_13` or None if not set

        """
        return self["Coefficient 13"]

    @coefficient_13.setter
    def coefficient_13(self, value=None):
        """Corresponds to IDD field `Coefficient 13`

        Args:
            value (float): value for IDD Field `Coefficient 13`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient 13"] = value

    @property
    def coefficient_14(self):
        """Get coefficient_14.

        Returns:
            float: the value of `coefficient_14` or None if not set

        """
        return self["Coefficient 14"]

    @coefficient_14.setter
    def coefficient_14(self, value=None):
        """Corresponds to IDD field `Coefficient 14`

        Args:
            value (float): value for IDD Field `Coefficient 14`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient 14"] = value

    @property
    def coefficient_15(self):
        """Get coefficient_15.

        Returns:
            float: the value of `coefficient_15` or None if not set

        """
        return self["Coefficient 15"]

    @coefficient_15.setter
    def coefficient_15(self, value=None):
        """Corresponds to IDD field `Coefficient 15`

        Args:
            value (float): value for IDD Field `Coefficient 15`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient 15"] = value

    @property
    def coefficient_16(self):
        """Get coefficient_16.

        Returns:
            float: the value of `coefficient_16` or None if not set

        """
        return self["Coefficient 16"]

    @coefficient_16.setter
    def coefficient_16(self, value=None):
        """Corresponds to IDD field `Coefficient 16`

        Args:
            value (float): value for IDD Field `Coefficient 16`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient 16"] = value

    @property
    def coefficient_17(self):
        """Get coefficient_17.

        Returns:
            float: the value of `coefficient_17` or None if not set

        """
        return self["Coefficient 17"]

    @coefficient_17.setter
    def coefficient_17(self, value=None):
        """Corresponds to IDD field `Coefficient 17`

        Args:
            value (float): value for IDD Field `Coefficient 17`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient 17"] = value

    @property
    def coefficient_18(self):
        """Get coefficient_18.

        Returns:
            float: the value of `coefficient_18` or None if not set

        """
        return self["Coefficient 18"]

    @coefficient_18.setter
    def coefficient_18(self, value=None):
        """Corresponds to IDD field `Coefficient 18`

        Args:
            value (float): value for IDD Field `Coefficient 18`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient 18"] = value

    @property
    def coefficient_19(self):
        """Get coefficient_19.

        Returns:
            float: the value of `coefficient_19` or None if not set

        """
        return self["Coefficient 19"]

    @coefficient_19.setter
    def coefficient_19(self, value=None):
        """Corresponds to IDD field `Coefficient 19`

        Args:
            value (float): value for IDD Field `Coefficient 19`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient 19"] = value

    @property
    def coefficient_20(self):
        """Get coefficient_20.

        Returns:
            float: the value of `coefficient_20` or None if not set

        """
        return self["Coefficient 20"]

    @coefficient_20.setter
    def coefficient_20(self, value=None):
        """Corresponds to IDD field `Coefficient 20`

        Args:
            value (float): value for IDD Field `Coefficient 20`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient 20"] = value

    @property
    def coefficient_21(self):
        """Get coefficient_21.

        Returns:
            float: the value of `coefficient_21` or None if not set

        """
        return self["Coefficient 21"]

    @coefficient_21.setter
    def coefficient_21(self, value=None):
        """Corresponds to IDD field `Coefficient 21`

        Args:
            value (float): value for IDD Field `Coefficient 21`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient 21"] = value

    @property
    def coefficient_22(self):
        """Get coefficient_22.

        Returns:
            float: the value of `coefficient_22` or None if not set

        """
        return self["Coefficient 22"]

    @coefficient_22.setter
    def coefficient_22(self, value=None):
        """Corresponds to IDD field `Coefficient 22`

        Args:
            value (float): value for IDD Field `Coefficient 22`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient 22"] = value

    @property
    def coefficient_23(self):
        """Get coefficient_23.

        Returns:
            float: the value of `coefficient_23` or None if not set

        """
        return self["Coefficient 23"]

    @coefficient_23.setter
    def coefficient_23(self, value=None):
        """Corresponds to IDD field `Coefficient 23`

        Args:
            value (float): value for IDD Field `Coefficient 23`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient 23"] = value

    @property
    def coefficient_24(self):
        """Get coefficient_24.

        Returns:
            float: the value of `coefficient_24` or None if not set

        """
        return self["Coefficient 24"]

    @coefficient_24.setter
    def coefficient_24(self, value=None):
        """Corresponds to IDD field `Coefficient 24`

        Args:
            value (float): value for IDD Field `Coefficient 24`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient 24"] = value

    @property
    def coefficient_25(self):
        """Get coefficient_25.

        Returns:
            float: the value of `coefficient_25` or None if not set

        """
        return self["Coefficient 25"]

    @coefficient_25.setter
    def coefficient_25(self, value=None):
        """Corresponds to IDD field `Coefficient 25`

        Args:
            value (float): value for IDD Field `Coefficient 25`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient 25"] = value

    @property
    def coefficient_26(self):
        """Get coefficient_26.

        Returns:
            float: the value of `coefficient_26` or None if not set

        """
        return self["Coefficient 26"]

    @coefficient_26.setter
    def coefficient_26(self, value=None):
        """Corresponds to IDD field `Coefficient 26`

        Args:
            value (float): value for IDD Field `Coefficient 26`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient 26"] = value

    @property
    def coefficient_27(self):
        """Get coefficient_27.

        Returns:
            float: the value of `coefficient_27` or None if not set

        """
        return self["Coefficient 27"]

    @coefficient_27.setter
    def coefficient_27(self, value=None):
        """Corresponds to IDD field `Coefficient 27`

        Args:
            value (float): value for IDD Field `Coefficient 27`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient 27"] = value




class EvaporativeFluidCoolerSingleSpeed(DataObject):

    """ Corresponds to IDD object `EvaporativeFluidCooler:SingleSpeed`
        This model is based on Merkel's theory, which is also the basis
        for the cooling tower model in EnergyPlus. The Evaporative fluid cooler
        is modeled as a counter flow heat exchanger.
    """
    schema = {'extensible-fields': OrderedDict(),
              'fields': OrderedDict([(u'name',
                                      {'name': u'Name',
                                       'pyname': u'name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'alpha'}),
                                     (u'water inlet node name',
                                      {'name': u'Water Inlet Node Name',
                                       'pyname': u'water_inlet_node_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'node'}),
                                     (u'water outlet node name',
                                      {'name': u'Water Outlet Node Name',
                                       'pyname': u'water_outlet_node_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'node'}),
                                     (u'design air flow rate',
                                      {'name': u'Design Air Flow Rate',
                                       'pyname': u'design_air_flow_rate',
                                       'minimum>': 0.0,
                                       'required-field': True,
                                       'autosizable': True,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'm3/s'}),
                                     (u'design air flow rate fan power',
                                      {'name': u'Design Air Flow Rate Fan Power',
                                       'pyname': u'design_air_flow_rate_fan_power',
                                       'minimum>': 0.0,
                                       'required-field': True,
                                       'autosizable': True,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'W'}),
                                     (u'design spray water flow rate',
                                      {'name': u'Design Spray Water Flow Rate',
                                       'pyname': u'design_spray_water_flow_rate',
                                       'minimum>': 0.0,
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'm3/s'}),
                                     (u'performance input method',
                                      {'name': u'Performance Input Method',
                                       'pyname': u'performance_input_method',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'UFactorTimesAreaAndDesignWaterFlowRate',
                                                           u'StandardDesignCapacity',
                                                           u'UserSpecifiedDesignCapacity'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'outdoor air inlet node name',
                                      {'name': u'Outdoor Air Inlet Node Name',
                                       'pyname': u'outdoor_air_inlet_node_name',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'node'}),
                                     (u'heat rejection capacity and nominal capacity sizing ratio',
                                      {'name': u'Heat Rejection Capacity and Nominal Capacity Sizing Ratio',
                                       'pyname': u'heat_rejection_capacity_and_nominal_capacity_sizing_ratio',
                                       'default': 1.25,
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'standard design capacity',
                                      {'name': u'Standard Design Capacity',
                                       'pyname': u'standard_design_capacity',
                                       'minimum>': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'W'}),
                                     (u'design air flow rate u-factor times area value',
                                      {'name': u'Design Air Flow Rate U-factor Times Area Value',
                                       'pyname': u'design_air_flow_rate_ufactor_times_area_value',
                                       'minimum>': 0.0,
                                       'maximum': 2100000.0,
                                       'required-field': False,
                                       'autosizable': True,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'W/K'}),
                                     (u'design water flow rate',
                                      {'name': u'Design Water Flow Rate',
                                       'pyname': u'design_water_flow_rate',
                                       'minimum>': 0.0,
                                       'required-field': False,
                                       'autosizable': True,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'm3/s'}),
                                     (u'user specified design capacity',
                                      {'name': u'User Specified Design Capacity',
                                       'pyname': u'user_specified_design_capacity',
                                       'minimum>': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'W'}),
                                     (u'design entering water temperature',
                                      {'name': u'Design Entering Water Temperature',
                                       'pyname': u'design_entering_water_temperature',
                                       'minimum>': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'C'}),
                                     (u'design entering air temperature',
                                      {'name': u'Design Entering Air Temperature',
                                       'pyname': u'design_entering_air_temperature',
                                       'minimum>': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'C'}),
                                     (u'design entering air wet-bulb temperature',
                                      {'name': u'Design Entering Air Wet-bulb Temperature',
                                       'pyname': u'design_entering_air_wetbulb_temperature',
                                       'minimum>': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'C'}),
                                     (u'capacity control',
                                      {'name': u'Capacity Control',
                                       'pyname': u'capacity_control',
                                       'default': u'FanCycling',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'FanCycling',
                                                           u'FluidBypass'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'sizing factor',
                                      {'name': u'Sizing Factor',
                                       'pyname': u'sizing_factor',
                                       'default': 1.0,
                                       'minimum>': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'evaporation loss mode',
                                      {'name': u'Evaporation Loss Mode',
                                       'pyname': u'evaporation_loss_mode',
                                       'default': u'SaturatedExit',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'LossFactor',
                                                           u'SaturatedExit'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'evaporation loss factor',
                                      {'name': u'Evaporation Loss Factor',
                                       'pyname': u'evaporation_loss_factor',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'percent/K'}),
                                     (u'drift loss percent',
                                      {'name': u'Drift Loss Percent',
                                       'pyname': u'drift_loss_percent',
                                       'default': 0.008,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'percent'}),
                                     (u'blowdown calculation mode',
                                      {'name': u'Blowdown Calculation Mode',
                                       'pyname': u'blowdown_calculation_mode',
                                       'default': u'ConcentrationRatio',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'ConcentrationRatio',
                                                           u'ScheduledRate'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'blowdown concentration ratio',
                                      {'name': u'Blowdown Concentration Ratio',
                                       'pyname': u'blowdown_concentration_ratio',
                                       'default': 3.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 2.0,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'blowdown makeup water usage schedule name',
                                      {'name': u'Blowdown Makeup Water Usage Schedule Name',
                                       'pyname': u'blowdown_makeup_water_usage_schedule_name',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'supply water storage tank name',
                                      {'name': u'Supply Water Storage Tank Name',
                                       'pyname': u'supply_water_storage_tank_name',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'})]),
              'format': None,
              'group': u'Condenser Equipment and Heat Exchangers',
              'min-fields': 10,
              'name': u'EvaporativeFluidCooler:SingleSpeed',
              'pyname': u'EvaporativeFluidCoolerSingleSpeed',
              'required-object': False,
              'unique-object': False}

    @property
    def name(self):
        """Get name.

        Returns:
            str: the value of `name` or None if not set

        """
        return self["Name"]

    @name.setter
    def name(self, value=None):
        """Corresponds to IDD field `Name` Fluid Cooler Name.

        Args:
            value (str): value for IDD Field `Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Name"] = value

    @property
    def water_inlet_node_name(self):
        """Get water_inlet_node_name.

        Returns:
            str: the value of `water_inlet_node_name` or None if not set

        """
        return self["Water Inlet Node Name"]

    @water_inlet_node_name.setter
    def water_inlet_node_name(self, value=None):
        """Corresponds to IDD field `Water Inlet Node Name` Name of Fluid
        Cooler water inlet node.

        Args:
            value (str): value for IDD Field `Water Inlet Node Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Water Inlet Node Name"] = value

    @property
    def water_outlet_node_name(self):
        """Get water_outlet_node_name.

        Returns:
            str: the value of `water_outlet_node_name` or None if not set

        """
        return self["Water Outlet Node Name"]

    @water_outlet_node_name.setter
    def water_outlet_node_name(self, value=None):
        """Corresponds to IDD field `Water Outlet Node Name` Name of Fluid
        Cooler water outlet node.

        Args:
            value (str): value for IDD Field `Water Outlet Node Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Water Outlet Node Name"] = value

    @property
    def design_air_flow_rate(self):
        """Get design_air_flow_rate.

        Returns:
            float: the value of `design_air_flow_rate` or None if not set

        """
        return self["Design Air Flow Rate"]

    @design_air_flow_rate.setter
    def design_air_flow_rate(self, value=None):
        """Corresponds to IDD field `Design Air Flow Rate`

        Args:
            value (float or "Autosize"): value for IDD Field `Design Air Flow Rate`
                Units: m3/s
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Design Air Flow Rate"] = value

    @property
    def design_air_flow_rate_fan_power(self):
        """Get design_air_flow_rate_fan_power.

        Returns:
            float: the value of `design_air_flow_rate_fan_power` or None if not set

        """
        return self["Design Air Flow Rate Fan Power"]

    @design_air_flow_rate_fan_power.setter
    def design_air_flow_rate_fan_power(self, value=None):
        """Corresponds to IDD field `Design Air Flow Rate Fan Power` This is
        the fan motor electric input power.

        Args:
            value (float or "Autosize"): value for IDD Field `Design Air Flow Rate Fan Power`
                Units: W
                IP-Units: W
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Design Air Flow Rate Fan Power"] = value

    @property
    def design_spray_water_flow_rate(self):
        """Get design_spray_water_flow_rate.

        Returns:
            float: the value of `design_spray_water_flow_rate` or None if not set

        """
        return self["Design Spray Water Flow Rate"]

    @design_spray_water_flow_rate.setter
    def design_spray_water_flow_rate(self, value=None):
        """Corresponds to IDD field `Design Spray Water Flow Rate`

        Args:
            value (float): value for IDD Field `Design Spray Water Flow Rate`
                Units: m3/s
                IP-Units: gal/min
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Design Spray Water Flow Rate"] = value

    @property
    def performance_input_method(self):
        """Get performance_input_method.

        Returns:
            str: the value of `performance_input_method` or None if not set

        """
        return self["Performance Input Method"]

    @performance_input_method.setter
    def performance_input_method(self, value=None):
        """Corresponds to IDD field `Performance Input Method` User can define
        fluid cooler thermal performance by specifying the fluid cooler UA and
        the Design Water Flow Rate, or by specifying the fluid cooler Standard
        Design Capacity or by specifying Design Capacity for Non standard
        conditions.

        Args:
            value (str): value for IDD Field `Performance Input Method`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Performance Input Method"] = value

    @property
    def outdoor_air_inlet_node_name(self):
        """Get outdoor_air_inlet_node_name.

        Returns:
            str: the value of `outdoor_air_inlet_node_name` or None if not set

        """
        return self["Outdoor Air Inlet Node Name"]

    @outdoor_air_inlet_node_name.setter
    def outdoor_air_inlet_node_name(self, value=None):
        """Corresponds to IDD field `Outdoor Air Inlet Node Name` Enter the
        name of an outdoor air node.

        Args:
            value (str): value for IDD Field `Outdoor Air Inlet Node Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Outdoor Air Inlet Node Name"] = value

    @property
    def heat_rejection_capacity_and_nominal_capacity_sizing_ratio(self):
        """Get heat_rejection_capacity_and_nominal_capacity_sizing_ratio.

        Returns:
            float: the value of `heat_rejection_capacity_and_nominal_capacity_sizing_ratio` or None if not set

        """
        return self[
            "Heat Rejection Capacity and Nominal Capacity Sizing Ratio"]

    @heat_rejection_capacity_and_nominal_capacity_sizing_ratio.setter
    def heat_rejection_capacity_and_nominal_capacity_sizing_ratio(
            self,
            value=1.25):
        """Corresponds to IDD field `Heat Rejection Capacity and Nominal
        Capacity Sizing Ratio`

        Args:
            value (float): value for IDD Field `Heat Rejection Capacity and Nominal Capacity Sizing Ratio`
                Default value: 1.25
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self[
            "Heat Rejection Capacity and Nominal Capacity Sizing Ratio"] = value

    @property
    def standard_design_capacity(self):
        """Get standard_design_capacity.

        Returns:
            float: the value of `standard_design_capacity` or None if not set

        """
        return self["Standard Design Capacity"]

    @standard_design_capacity.setter
    def standard_design_capacity(self, value=None):
        """  Corresponds to IDD field `Standard Design Capacity`
        Standard design capacity with entering water at 35C (95F), leaving water at
        29.44C (85F), entering air at 25.56C (78F) wet-bulb temperature and 35C (95F)
        dry-bulb temperature. Design water flow rate assumed to be 5.382E-8 m3/s per watt
        (3 gpm/ton). Standard design capacity times the Heat Rejection Capacity and
        Nominal Capacity Sizing Ratio (e.g. 1.25) gives the actual fluid cooler
        heat rejection at these operating conditions.
        Only used for Performance Input Method = StandardDesignCapacity;
        for other input methods, this field is ignored.
        The standard conditions mentioned above for Standard design capacity are already
        specified in the EnergyPlus. So the input fields such as design entering water
        temp., design entering air wet-bulb and dry-bulb temp. and design water flow rate, if
        provided in the input, will be ignored for the StandardDesignCapacity performance input
        method. Also, the standard conditions are for water as a fluid type so this performance input
        method can only be used with water as a fluid type (as specified in CondenserLoop object).

        Args:
            value (float): value for IDD Field `Standard Design Capacity`
                Units: W
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Standard Design Capacity"] = value

    @property
    def design_air_flow_rate_ufactor_times_area_value(self):
        """Get design_air_flow_rate_ufactor_times_area_value.

        Returns:
            float: the value of `design_air_flow_rate_ufactor_times_area_value` or None if not set

        """
        return self["Design Air Flow Rate U-factor Times Area Value"]

    @design_air_flow_rate_ufactor_times_area_value.setter
    def design_air_flow_rate_ufactor_times_area_value(self, value=None):
        """  Corresponds to IDD field `Design Air Flow Rate U-factor Times Area Value`
        Only used for Performance Input Method = UFactorTimesAreaAndDesignWaterFlowRate;
        for other Performance Input Methods, this field is ignored.

        Args:
            value (float or "Autosize"): value for IDD Field `Design Air Flow Rate U-factor Times Area Value`
                Units: W/K
                value <= 2100000.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Design Air Flow Rate U-factor Times Area Value"] = value

    @property
    def design_water_flow_rate(self):
        """Get design_water_flow_rate.

        Returns:
            float: the value of `design_water_flow_rate` or None if not set

        """
        return self["Design Water Flow Rate"]

    @design_water_flow_rate.setter
    def design_water_flow_rate(self, value=None):
        """  Corresponds to IDD field `Design Water Flow Rate`
        Input value is ignored if fluid cooler Performance Input Method= StandardDesignCapacity.

        Args:
            value (float or "Autosize"): value for IDD Field `Design Water Flow Rate`
                Units: m3/s
                IP-Units: gal/min
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Design Water Flow Rate"] = value

    @property
    def user_specified_design_capacity(self):
        """Get user_specified_design_capacity.

        Returns:
            float: the value of `user_specified_design_capacity` or None if not set

        """
        return self["User Specified Design Capacity"]

    @user_specified_design_capacity.setter
    def user_specified_design_capacity(self, value=None):
        """  Corresponds to IDD field `User Specified Design Capacity`
        Only used for Performance Input Method = UserSpecifiedDesignCapacity;
        for other Performance Input Methods, this field is ignored.

        Args:
            value (float): value for IDD Field `User Specified Design Capacity`
                Units: W
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["User Specified Design Capacity"] = value

    @property
    def design_entering_water_temperature(self):
        """Get design_entering_water_temperature.

        Returns:
            float: the value of `design_entering_water_temperature` or None if not set

        """
        return self["Design Entering Water Temperature"]

    @design_entering_water_temperature.setter
    def design_entering_water_temperature(self, value=None):
        """  Corresponds to IDD field `Design Entering Water Temperature`
        Only used for Performance Input Method = UserSpecifiedDesignCapacity;
        for other Performance Input Methods, this field is ignored.
        Design Entering Water Temperature must be greater than Design Entering Air Temperature.

        Args:
            value (float): value for IDD Field `Design Entering Water Temperature`
                Units: C
                IP-Units: F
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Design Entering Water Temperature"] = value

    @property
    def design_entering_air_temperature(self):
        """Get design_entering_air_temperature.

        Returns:
            float: the value of `design_entering_air_temperature` or None if not set

        """
        return self["Design Entering Air Temperature"]

    @design_entering_air_temperature.setter
    def design_entering_air_temperature(self, value=None):
        """  Corresponds to IDD field `Design Entering Air Temperature`
        Only used for Performance Input Method = UserSpecifiedDesignCapacity;
        for other Performance Input Methods, this field is ignored.
        Design Entering Air Temperature must be greater than Design Entering Air Wet-bulb
        Temperature.

        Args:
            value (float): value for IDD Field `Design Entering Air Temperature`
                Units: C
                IP-Units: F
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Design Entering Air Temperature"] = value

    @property
    def design_entering_air_wetbulb_temperature(self):
        """Get design_entering_air_wetbulb_temperature.

        Returns:
            float: the value of `design_entering_air_wetbulb_temperature` or None if not set

        """
        return self["Design Entering Air Wet-bulb Temperature"]

    @design_entering_air_wetbulb_temperature.setter
    def design_entering_air_wetbulb_temperature(self, value=None):
        """  Corresponds to IDD field `Design Entering Air Wet-bulb Temperature`
        Only used for Performance Input Method = UserSpecifiedDesignCapacity;
        for other Performance Input Methods, this field is ignored.
        Design Entering Air Wet-bulb Temperature must be less than Design Entering Air
        Temperature.

        Args:
            value (float): value for IDD Field `Design Entering Air Wet-bulb Temperature`
                Units: C
                IP-Units: F
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Design Entering Air Wet-bulb Temperature"] = value

    @property
    def capacity_control(self):
        """Get capacity_control.

        Returns:
            str: the value of `capacity_control` or None if not set

        """
        return self["Capacity Control"]

    @capacity_control.setter
    def capacity_control(self, value="FanCycling"):
        """Corresponds to IDD field `Capacity Control`

        Args:
            value (str): value for IDD Field `Capacity Control`
                Default value: FanCycling
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Capacity Control"] = value

    @property
    def sizing_factor(self):
        """Get sizing_factor.

        Returns:
            float: the value of `sizing_factor` or None if not set

        """
        return self["Sizing Factor"]

    @sizing_factor.setter
    def sizing_factor(self, value=1.0):
        """Corresponds to IDD field `Sizing Factor` Multiplies the autosized
        capacity and flow rates.

        Args:
            value (float): value for IDD Field `Sizing Factor`
                Default value: 1.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Sizing Factor"] = value

    @property
    def evaporation_loss_mode(self):
        """Get evaporation_loss_mode.

        Returns:
            str: the value of `evaporation_loss_mode` or None if not set

        """
        return self["Evaporation Loss Mode"]

    @evaporation_loss_mode.setter
    def evaporation_loss_mode(self, value="SaturatedExit"):
        """Corresponds to IDD field `Evaporation Loss Mode`

        Args:
            value (str): value for IDD Field `Evaporation Loss Mode`
                Default value: SaturatedExit
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Evaporation Loss Mode"] = value

    @property
    def evaporation_loss_factor(self):
        """Get evaporation_loss_factor.

        Returns:
            float: the value of `evaporation_loss_factor` or None if not set

        """
        return self["Evaporation Loss Factor"]

    @evaporation_loss_factor.setter
    def evaporation_loss_factor(self, value=None):
        """Corresponds to IDD field `Evaporation Loss Factor` Rate of water
        evaporation from the Fluid Cooler and lost to the outdoor air [%/K]
        Empirical correlation is used to calculate default loss factor if it
        not explicitly provided.

        Args:
            value (float): value for IDD Field `Evaporation Loss Factor`
                Units: percent/K
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Evaporation Loss Factor"] = value

    @property
    def drift_loss_percent(self):
        """Get drift_loss_percent.

        Returns:
            float: the value of `drift_loss_percent` or None if not set

        """
        return self["Drift Loss Percent"]

    @drift_loss_percent.setter
    def drift_loss_percent(self, value=0.008):
        """Corresponds to IDD field `Drift Loss Percent` Rate of drift loss as
        a percentage of circulating spray water flow rate Default value for
        this field in under investigation. For now Cooling towers drift loss
        percent default value is taken here.

        Args:
            value (float): value for IDD Field `Drift Loss Percent`
                Units: percent
                Default value: 0.008
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Drift Loss Percent"] = value

    @property
    def blowdown_calculation_mode(self):
        """Get blowdown_calculation_mode.

        Returns:
            str: the value of `blowdown_calculation_mode` or None if not set

        """
        return self["Blowdown Calculation Mode"]

    @blowdown_calculation_mode.setter
    def blowdown_calculation_mode(self, value="ConcentrationRatio"):
        """Corresponds to IDD field `Blowdown Calculation Mode`

        Args:
            value (str): value for IDD Field `Blowdown Calculation Mode`
                Default value: ConcentrationRatio
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Blowdown Calculation Mode"] = value

    @property
    def blowdown_concentration_ratio(self):
        """Get blowdown_concentration_ratio.

        Returns:
            float: the value of `blowdown_concentration_ratio` or None if not set

        """
        return self["Blowdown Concentration Ratio"]

    @blowdown_concentration_ratio.setter
    def blowdown_concentration_ratio(self, value=3.0):
        """Corresponds to IDD field `Blowdown Concentration Ratio`
        Characterizes the rate of blowdown in the Evaporative Fluid Cooler.
        Blowdown is water intentionally drained from the basin in order to
        offset the build up of solids in the water that would otherwise occur
        because of evaporation. Ratio of solids in the blowdown water to solids
        in the make up water. Default value for this field in under
        investigation. For now Cooling towers Blowdown Concentration Ratio
        percent default value is taken here.

        Args:
            value (float): value for IDD Field `Blowdown Concentration Ratio`
                Default value: 3.0
                value >= 2.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Blowdown Concentration Ratio"] = value

    @property
    def blowdown_makeup_water_usage_schedule_name(self):
        """Get blowdown_makeup_water_usage_schedule_name.

        Returns:
            str: the value of `blowdown_makeup_water_usage_schedule_name` or None if not set

        """
        return self["Blowdown Makeup Water Usage Schedule Name"]

    @blowdown_makeup_water_usage_schedule_name.setter
    def blowdown_makeup_water_usage_schedule_name(self, value=None):
        """Corresponds to IDD field `Blowdown Makeup Water Usage Schedule Name`
        Makeup water usage due to blowdown results from occasionally draining a
        small amount of water in the Fluid Cooler basin to purge scale or other
        contaminants to reduce their concentration in order to maintain an
        acceptable level of water quality. Schedule values should reflect water
        usage in m3/s.

        Args:
            value (str): value for IDD Field `Blowdown Makeup Water Usage Schedule Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Blowdown Makeup Water Usage Schedule Name"] = value

    @property
    def supply_water_storage_tank_name(self):
        """Get supply_water_storage_tank_name.

        Returns:
            str: the value of `supply_water_storage_tank_name` or None if not set

        """
        return self["Supply Water Storage Tank Name"]

    @supply_water_storage_tank_name.setter
    def supply_water_storage_tank_name(self, value=None):
        """Corresponds to IDD field `Supply Water Storage Tank Name`

        Args:
            value (str): value for IDD Field `Supply Water Storage Tank Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Supply Water Storage Tank Name"] = value




class EvaporativeFluidCoolerTwoSpeed(DataObject):

    """ Corresponds to IDD object `EvaporativeFluidCooler:TwoSpeed`
        This model is based on Merkel's theory, which is also the basis
        for the cooling tower model in EnergyPlus. The Evaporative fluid cooler
        is modeled as a counter flow heat exchanger.
    """
    schema = {'extensible-fields': OrderedDict(),
              'fields': OrderedDict([(u'name',
                                      {'name': u'Name',
                                       'pyname': u'name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'alpha'}),
                                     (u'water inlet node name',
                                      {'name': u'Water Inlet Node Name',
                                       'pyname': u'water_inlet_node_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'node'}),
                                     (u'water outlet node name',
                                      {'name': u'Water Outlet Node Name',
                                       'pyname': u'water_outlet_node_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'node'}),
                                     (u'high fan speed air flow rate',
                                      {'name': u'High Fan Speed Air Flow Rate',
                                       'pyname': u'high_fan_speed_air_flow_rate',
                                       'minimum>': 0.0,
                                       'required-field': True,
                                       'autosizable': True,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'm3/s'}),
                                     (u'high fan speed fan power',
                                      {'name': u'High Fan Speed Fan Power',
                                       'pyname': u'high_fan_speed_fan_power',
                                       'minimum>': 0.0,
                                       'required-field': True,
                                       'autosizable': True,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'W'}),
                                     (u'low fan speed air flow rate',
                                      {'name': u'Low Fan Speed Air Flow Rate',
                                       'pyname': u'low_fan_speed_air_flow_rate',
                                       'minimum>': 0.0,
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': True,
                                       'type': u'real',
                                       'unit': u'm3/s'}),
                                     (u'low fan speed air flow rate sizing factor',
                                      {'name': u'Low Fan Speed Air Flow Rate Sizing Factor',
                                       'pyname': u'low_fan_speed_air_flow_rate_sizing_factor',
                                       'default': 0.5,
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'low fan speed fan power',
                                      {'name': u'Low Fan Speed Fan Power',
                                       'pyname': u'low_fan_speed_fan_power',
                                       'minimum>': 0.0,
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': True,
                                       'type': u'real',
                                       'unit': u'W'}),
                                     (u'low fan speed fan power sizing factor',
                                      {'name': u'Low Fan Speed Fan Power Sizing Factor',
                                       'pyname': u'low_fan_speed_fan_power_sizing_factor',
                                       'default': 0.16,
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'design spray water flow rate',
                                      {'name': u'Design Spray Water Flow Rate',
                                       'pyname': u'design_spray_water_flow_rate',
                                       'minimum>': 0.0,
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'm3/s'}),
                                     (u'performance input method',
                                      {'name': u'Performance Input Method',
                                       'pyname': u'performance_input_method',
                                       'required-field': True,
                                       'autosizable': False,
                                       'accepted-values': [u'UFactorTimesAreaAndDesignWaterFlowRate',
                                                           u'StandardDesignCapacity',
                                                           u'UserSpecifiedDesignCapacity'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'outdoor air inlet node name',
                                      {'name': u'Outdoor Air Inlet Node Name',
                                       'pyname': u'outdoor_air_inlet_node_name',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'node'}),
                                     (u'heat rejection capacity and nominal capacity sizing ratio',
                                      {'name': u'Heat Rejection Capacity and Nominal Capacity Sizing Ratio',
                                       'pyname': u'heat_rejection_capacity_and_nominal_capacity_sizing_ratio',
                                       'default': 1.25,
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'high speed standard design capacity',
                                      {'name': u'High Speed Standard Design Capacity',
                                       'pyname': u'high_speed_standard_design_capacity',
                                       'minimum>': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'W'}),
                                     (u'low speed standard design capacity',
                                      {'name': u'Low Speed Standard Design Capacity',
                                       'pyname': u'low_speed_standard_design_capacity',
                                       'minimum>': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': True,
                                       'type': u'real',
                                       'unit': u'W'}),
                                     (u'low speed standard capacity sizing factor',
                                      {'name': u'Low Speed Standard Capacity Sizing Factor',
                                       'pyname': u'low_speed_standard_capacity_sizing_factor',
                                       'default': 0.5,
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'high fan speed u-factor times area value',
                                      {'name': u'High Fan Speed U-factor Times Area Value',
                                       'pyname': u'high_fan_speed_ufactor_times_area_value',
                                       'minimum>': 0.0,
                                       'maximum': 2100000.0,
                                       'required-field': False,
                                       'autosizable': True,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'W/K'}),
                                     (u'low fan speed u-factor times area value',
                                      {'name': u'Low Fan Speed U-factor Times Area Value',
                                       'pyname': u'low_fan_speed_ufactor_times_area_value',
                                       'minimum>': 0.0,
                                       'maximum': 300000.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': True,
                                       'type': u'real',
                                       'unit': u'W/K'}),
                                     (u'low fan speed u-factor times area sizing factor',
                                      {'name': u'Low Fan Speed U-Factor Times Area Sizing Factor',
                                       'pyname': u'low_fan_speed_ufactor_times_area_sizing_factor',
                                       'default': 0.6,
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'design water flow rate',
                                      {'name': u'Design Water Flow Rate',
                                       'pyname': u'design_water_flow_rate',
                                       'minimum>': 0.0,
                                       'required-field': False,
                                       'autosizable': True,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'm3/s'}),
                                     (u'high speed user specified design capacity',
                                      {'name': u'High Speed User Specified Design Capacity',
                                       'pyname': u'high_speed_user_specified_design_capacity',
                                       'minimum>': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'W'}),
                                     (u'low speed user specified design capacity',
                                      {'name': u'Low Speed User Specified Design Capacity',
                                       'pyname': u'low_speed_user_specified_design_capacity',
                                       'minimum>': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': True,
                                       'type': u'real',
                                       'unit': u'W'}),
                                     (u'low speed user specified design capacity sizing factor',
                                      {'name': u'Low Speed User Specified Design Capacity Sizing Factor',
                                       'pyname': u'low_speed_user_specified_design_capacity_sizing_factor',
                                       'default': 0.5,
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'design entering water temperature',
                                      {'name': u'Design Entering Water Temperature',
                                       'pyname': u'design_entering_water_temperature',
                                       'minimum>': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'C'}),
                                     (u'design entering air temperature',
                                      {'name': u'Design Entering Air Temperature',
                                       'pyname': u'design_entering_air_temperature',
                                       'minimum>': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'C'}),
                                     (u'design entering air wet-bulb temperature',
                                      {'name': u'Design Entering Air Wet-bulb Temperature',
                                       'pyname': u'design_entering_air_wetbulb_temperature',
                                       'minimum>': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'C'}),
                                     (u'high speed sizing factor',
                                      {'name': u'High Speed Sizing Factor',
                                       'pyname': u'high_speed_sizing_factor',
                                       'default': 1.0,
                                       'minimum>': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'evaporation loss mode',
                                      {'name': u'Evaporation Loss Mode',
                                       'pyname': u'evaporation_loss_mode',
                                       'default': u'SaturatedExit',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'LossFactor',
                                                           u'SaturatedExit'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'evaporation loss factor',
                                      {'name': u'Evaporation Loss Factor',
                                       'pyname': u'evaporation_loss_factor',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'percent/K'}),
                                     (u'drift loss percent',
                                      {'name': u'Drift Loss Percent',
                                       'pyname': u'drift_loss_percent',
                                       'default': 0.008,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'percent'}),
                                     (u'blowdown calculation mode',
                                      {'name': u'Blowdown Calculation Mode',
                                       'pyname': u'blowdown_calculation_mode',
                                       'default': u'ConcentrationRatio',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'ConcentrationRatio',
                                                           u'ScheduledRate'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'blowdown concentration ratio',
                                      {'name': u'Blowdown Concentration Ratio',
                                       'pyname': u'blowdown_concentration_ratio',
                                       'default': 3.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 2.0,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'blowdown makeup water usage schedule name',
                                      {'name': u'Blowdown Makeup Water Usage Schedule Name',
                                       'pyname': u'blowdown_makeup_water_usage_schedule_name',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'supply water storage tank name',
                                      {'name': u'Supply Water Storage Tank Name',
                                       'pyname': u'supply_water_storage_tank_name',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'})]),
              'format': None,
              'group': u'Condenser Equipment and Heat Exchangers',
              'min-fields': 23,
              'name': u'EvaporativeFluidCooler:TwoSpeed',
              'pyname': u'EvaporativeFluidCoolerTwoSpeed',
              'required-object': False,
              'unique-object': False}

    @property
    def name(self):
        """Get name.

        Returns:
            str: the value of `name` or None if not set

        """
        return self["Name"]

    @name.setter
    def name(self, value=None):
        """Corresponds to IDD field `Name` fluid cooler name.

        Args:
            value (str): value for IDD Field `Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Name"] = value

    @property
    def water_inlet_node_name(self):
        """Get water_inlet_node_name.

        Returns:
            str: the value of `water_inlet_node_name` or None if not set

        """
        return self["Water Inlet Node Name"]

    @water_inlet_node_name.setter
    def water_inlet_node_name(self, value=None):
        """Corresponds to IDD field `Water Inlet Node Name` Name of fluid
        cooler water inlet node.

        Args:
            value (str): value for IDD Field `Water Inlet Node Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Water Inlet Node Name"] = value

    @property
    def water_outlet_node_name(self):
        """Get water_outlet_node_name.

        Returns:
            str: the value of `water_outlet_node_name` or None if not set

        """
        return self["Water Outlet Node Name"]

    @water_outlet_node_name.setter
    def water_outlet_node_name(self, value=None):
        """Corresponds to IDD field `Water Outlet Node Name` Name of fluid
        cooler water outlet node.

        Args:
            value (str): value for IDD Field `Water Outlet Node Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Water Outlet Node Name"] = value

    @property
    def high_fan_speed_air_flow_rate(self):
        """Get high_fan_speed_air_flow_rate.

        Returns:
            float: the value of `high_fan_speed_air_flow_rate` or None if not set

        """
        return self["High Fan Speed Air Flow Rate"]

    @high_fan_speed_air_flow_rate.setter
    def high_fan_speed_air_flow_rate(self, value=None):
        """Corresponds to IDD field `High Fan Speed Air Flow Rate`

        Args:
            value (float or "Autosize"): value for IDD Field `High Fan Speed Air Flow Rate`
                Units: m3/s
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["High Fan Speed Air Flow Rate"] = value

    @property
    def high_fan_speed_fan_power(self):
        """Get high_fan_speed_fan_power.

        Returns:
            float: the value of `high_fan_speed_fan_power` or None if not set

        """
        return self["High Fan Speed Fan Power"]

    @high_fan_speed_fan_power.setter
    def high_fan_speed_fan_power(self, value=None):
        """Corresponds to IDD field `High Fan Speed Fan Power` This is the fan
        motor electric input power at high speed.

        Args:
            value (float or "Autosize"): value for IDD Field `High Fan Speed Fan Power`
                Units: W
                IP-Units: W
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["High Fan Speed Fan Power"] = value

    @property
    def low_fan_speed_air_flow_rate(self):
        """Get low_fan_speed_air_flow_rate.

        Returns:
            float: the value of `low_fan_speed_air_flow_rate` or None if not set

        """
        return self["Low Fan Speed Air Flow Rate"]

    @low_fan_speed_air_flow_rate.setter
    def low_fan_speed_air_flow_rate(self, value=None):
        """Corresponds to IDD field `Low Fan Speed Air Flow Rate` Low speed air
        flow rate must be less than high speed air flow rate.

        Args:
            value (float or "Autocalculate"): value for IDD Field `Low Fan Speed Air Flow Rate`
                Units: m3/s
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Low Fan Speed Air Flow Rate"] = value

    @property
    def low_fan_speed_air_flow_rate_sizing_factor(self):
        """Get low_fan_speed_air_flow_rate_sizing_factor.

        Returns:
            float: the value of `low_fan_speed_air_flow_rate_sizing_factor` or None if not set

        """
        return self["Low Fan Speed Air Flow Rate Sizing Factor"]

    @low_fan_speed_air_flow_rate_sizing_factor.setter
    def low_fan_speed_air_flow_rate_sizing_factor(self, value=0.5):
        """Corresponds to IDD field `Low Fan Speed Air Flow Rate Sizing Factor`
        This field is only used if the previous field is set to autocalculate.

        Args:
            value (float): value for IDD Field `Low Fan Speed Air Flow Rate Sizing Factor`
                Default value: 0.5
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Low Fan Speed Air Flow Rate Sizing Factor"] = value

    @property
    def low_fan_speed_fan_power(self):
        """Get low_fan_speed_fan_power.

        Returns:
            float: the value of `low_fan_speed_fan_power` or None if not set

        """
        return self["Low Fan Speed Fan Power"]

    @low_fan_speed_fan_power.setter
    def low_fan_speed_fan_power(self, value=None):
        """Corresponds to IDD field `Low Fan Speed Fan Power` This is the fan
        motor electric input power at low speed.

        Args:
            value (float or "Autocalculate"): value for IDD Field `Low Fan Speed Fan Power`
                Units: W
                IP-Units: W
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Low Fan Speed Fan Power"] = value

    @property
    def low_fan_speed_fan_power_sizing_factor(self):
        """Get low_fan_speed_fan_power_sizing_factor.

        Returns:
            float: the value of `low_fan_speed_fan_power_sizing_factor` or None if not set

        """
        return self["Low Fan Speed Fan Power Sizing Factor"]

    @low_fan_speed_fan_power_sizing_factor.setter
    def low_fan_speed_fan_power_sizing_factor(self, value=0.16):
        """Corresponds to IDD field `Low Fan Speed Fan Power Sizing Factor`
        This field is only used if the previous field is set to autocalculate.

        Args:
            value (float): value for IDD Field `Low Fan Speed Fan Power Sizing Factor`
                Default value: 0.16
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Low Fan Speed Fan Power Sizing Factor"] = value

    @property
    def design_spray_water_flow_rate(self):
        """Get design_spray_water_flow_rate.

        Returns:
            float: the value of `design_spray_water_flow_rate` or None if not set

        """
        return self["Design Spray Water Flow Rate"]

    @design_spray_water_flow_rate.setter
    def design_spray_water_flow_rate(self, value=None):
        """Corresponds to IDD field `Design Spray Water Flow Rate`

        Args:
            value (float): value for IDD Field `Design Spray Water Flow Rate`
                Units: m3/s
                IP-Units: gal/min
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Design Spray Water Flow Rate"] = value

    @property
    def performance_input_method(self):
        """Get performance_input_method.

        Returns:
            str: the value of `performance_input_method` or None if not set

        """
        return self["Performance Input Method"]

    @performance_input_method.setter
    def performance_input_method(self, value=None):
        """Corresponds to IDD field `Performance Input Method` User can define
        fluid cooler thermal performance by specifying the fluid cooler UA and
        the Design Water Flow Rate, or by specifying the fluid cooler Standard
        Design Capacity or by specifying Design Capacity for Non standard
        conditions.

        Args:
            value (str): value for IDD Field `Performance Input Method`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Performance Input Method"] = value

    @property
    def outdoor_air_inlet_node_name(self):
        """Get outdoor_air_inlet_node_name.

        Returns:
            str: the value of `outdoor_air_inlet_node_name` or None if not set

        """
        return self["Outdoor Air Inlet Node Name"]

    @outdoor_air_inlet_node_name.setter
    def outdoor_air_inlet_node_name(self, value=None):
        """Corresponds to IDD field `Outdoor Air Inlet Node Name` Enter the
        name of an outdoor air node.

        Args:
            value (str): value for IDD Field `Outdoor Air Inlet Node Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Outdoor Air Inlet Node Name"] = value

    @property
    def heat_rejection_capacity_and_nominal_capacity_sizing_ratio(self):
        """Get heat_rejection_capacity_and_nominal_capacity_sizing_ratio.

        Returns:
            float: the value of `heat_rejection_capacity_and_nominal_capacity_sizing_ratio` or None if not set

        """
        return self[
            "Heat Rejection Capacity and Nominal Capacity Sizing Ratio"]

    @heat_rejection_capacity_and_nominal_capacity_sizing_ratio.setter
    def heat_rejection_capacity_and_nominal_capacity_sizing_ratio(
            self,
            value=1.25):
        """Corresponds to IDD field `Heat Rejection Capacity and Nominal
        Capacity Sizing Ratio`

        Args:
            value (float): value for IDD Field `Heat Rejection Capacity and Nominal Capacity Sizing Ratio`
                Default value: 1.25
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self[
            "Heat Rejection Capacity and Nominal Capacity Sizing Ratio"] = value

    @property
    def high_speed_standard_design_capacity(self):
        """Get high_speed_standard_design_capacity.

        Returns:
            float: the value of `high_speed_standard_design_capacity` or None if not set

        """
        return self["High Speed Standard Design Capacity"]

    @high_speed_standard_design_capacity.setter
    def high_speed_standard_design_capacity(self, value=None):
        """  Corresponds to IDD field `High Speed Standard Design Capacity`
        Standard design capacity with entering water at 35C (95F), leaving water at
        29.44C (85F), entering air at 25.56C (78F) wet-bulb temperature and 35C (95F)
        dry-bulb temperature. Design water flow rate assumed to be 5.382E-8 m3/s per watt
        (3 gpm/ton). Standard design capacity times the Heat Rejection Capacity and
        Nominal Capacity Sizing Ratio (e.g. 1.25) gives the actual fluid cooler
        heat rejection at these operating conditions.
        Only used for Performance Input Method = StandardDesignCapacity;
        for other input methods, this field is ignored.
        The standard conditions mentioned above for Standard design capacity are already
        specified in the EnergyPlus. So the input fields such as design entering water
        temp., design entering air wet-bulb and dry-bulb temp. and design water flow rate, if
        provided in the input, will be ignored for the StandardDesignCapacity performance input
        method. Also, the standard conditions are for water as a fluid type so this performance input
        method can only be used with water as a fluid type (as specified in CondenserLoop object).

        Args:
            value (float): value for IDD Field `High Speed Standard Design Capacity`
                Units: W
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["High Speed Standard Design Capacity"] = value

    @property
    def low_speed_standard_design_capacity(self):
        """Get low_speed_standard_design_capacity.

        Returns:
            float: the value of `low_speed_standard_design_capacity` or None if not set

        """
        return self["Low Speed Standard Design Capacity"]

    @low_speed_standard_design_capacity.setter
    def low_speed_standard_design_capacity(self, value=None):
        """  Corresponds to IDD field `Low Speed Standard Design Capacity`
        Standard design capacity with entering water at 35C (95F), leaving water at
        29.44C (85F), entering air at 25.56C (78F) wet-bulb temperature and 35C (95F)
        dry-bulb temperature. Design water flow rate assumed to be 5.382E-8 m3/s per watt
        (3 gpm/ton). Standard design capacity times the Heat Rejection Capacity and
        Nominal Capacity Sizing Ratio (e.g. 1.25) gives the actual fluid cooler
        heat rejection at these operating conditions.
        Only used for Performance Input Method = StandardDesignCapacity;
        for other input methods, this field is ignored.
        The standard conditions mentioned above for Standard design capacity are already
        specified in the EnergyPlus. So the input fields such as design entering water
        temp., design entering air wet-bulb and dry-bulb temp. and design water flow rate, if
        provided in the input, will be ignored for the StandardDesignCapacity performance input
        method. Also, the standard conditions are for water as a fluid type so this performance input
        method can only be used with water as a fluid type (as specified in CondenserLoop object).

        Args:
            value (float or "Autocalculate"): value for IDD Field `Low Speed Standard Design Capacity`
                Units: W
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Low Speed Standard Design Capacity"] = value

    @property
    def low_speed_standard_capacity_sizing_factor(self):
        """Get low_speed_standard_capacity_sizing_factor.

        Returns:
            float: the value of `low_speed_standard_capacity_sizing_factor` or None if not set

        """
        return self["Low Speed Standard Capacity Sizing Factor"]

    @low_speed_standard_capacity_sizing_factor.setter
    def low_speed_standard_capacity_sizing_factor(self, value=0.5):
        """Corresponds to IDD field `Low Speed Standard Capacity Sizing Factor`
        This field is only used if the previous field is set to autocalculate.

        Args:
            value (float): value for IDD Field `Low Speed Standard Capacity Sizing Factor`
                Default value: 0.5
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Low Speed Standard Capacity Sizing Factor"] = value

    @property
    def high_fan_speed_ufactor_times_area_value(self):
        """Get high_fan_speed_ufactor_times_area_value.

        Returns:
            float: the value of `high_fan_speed_ufactor_times_area_value` or None if not set

        """
        return self["High Fan Speed U-factor Times Area Value"]

    @high_fan_speed_ufactor_times_area_value.setter
    def high_fan_speed_ufactor_times_area_value(self, value=None):
        """  Corresponds to IDD field `High Fan Speed U-factor Times Area Value`
        Only used for Performance Input Method = UFactorTimesAreaAndDesignWaterFlowRate;
        for other Performance Input Methods, this field is ignored.

        Args:
            value (float or "Autosize"): value for IDD Field `High Fan Speed U-factor Times Area Value`
                Units: W/K
                value <= 2100000.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["High Fan Speed U-factor Times Area Value"] = value

    @property
    def low_fan_speed_ufactor_times_area_value(self):
        """Get low_fan_speed_ufactor_times_area_value.

        Returns:
            float: the value of `low_fan_speed_ufactor_times_area_value` or None if not set

        """
        return self["Low Fan Speed U-factor Times Area Value"]

    @low_fan_speed_ufactor_times_area_value.setter
    def low_fan_speed_ufactor_times_area_value(self, value=None):
        """  Corresponds to IDD field `Low Fan Speed U-factor Times Area Value`
        Only used for Performance Input Method = UFactorTimesAreaAndDesignWaterFlowRate;
        for other input methods, this field is ignored.
        Low speed fluid cooler UA must be less than high speed fluid cooler UA

        Args:
            value (float or "Autocalculate"): value for IDD Field `Low Fan Speed U-factor Times Area Value`
                Units: W/K
                value <= 300000.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Low Fan Speed U-factor Times Area Value"] = value

    @property
    def low_fan_speed_ufactor_times_area_sizing_factor(self):
        """Get low_fan_speed_ufactor_times_area_sizing_factor.

        Returns:
            float: the value of `low_fan_speed_ufactor_times_area_sizing_factor` or None if not set

        """
        return self["Low Fan Speed U-Factor Times Area Sizing Factor"]

    @low_fan_speed_ufactor_times_area_sizing_factor.setter
    def low_fan_speed_ufactor_times_area_sizing_factor(self, value=0.6):
        """  Corresponds to IDD field `Low Fan Speed U-Factor Times Area Sizing Factor`
        This field is only used if the previous field is set to autocalculate and
        the Performance Input Method is UFactorTimesAreaAndDesignWaterFlowRate

        Args:
            value (float): value for IDD Field `Low Fan Speed U-Factor Times Area Sizing Factor`
                Default value: 0.6
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Low Fan Speed U-Factor Times Area Sizing Factor"] = value

    @property
    def design_water_flow_rate(self):
        """Get design_water_flow_rate.

        Returns:
            float: the value of `design_water_flow_rate` or None if not set

        """
        return self["Design Water Flow Rate"]

    @design_water_flow_rate.setter
    def design_water_flow_rate(self, value=None):
        """  Corresponds to IDD field `Design Water Flow Rate`
        Input value is ignored if fluid cooler Performance Input Method= StandardDesignCapacity

        Args:
            value (float or "Autosize"): value for IDD Field `Design Water Flow Rate`
                Units: m3/s
                IP-Units: gal/min
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Design Water Flow Rate"] = value

    @property
    def high_speed_user_specified_design_capacity(self):
        """Get high_speed_user_specified_design_capacity.

        Returns:
            float: the value of `high_speed_user_specified_design_capacity` or None if not set

        """
        return self["High Speed User Specified Design Capacity"]

    @high_speed_user_specified_design_capacity.setter
    def high_speed_user_specified_design_capacity(self, value=None):
        """  Corresponds to IDD field `High Speed User Specified Design Capacity`
        Only used for Performance Input Method = UserSpecifiedDesignCapacity;
        for other Performance Input Methods, this field is ignored.

        Args:
            value (float): value for IDD Field `High Speed User Specified Design Capacity`
                Units: W
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["High Speed User Specified Design Capacity"] = value

    @property
    def low_speed_user_specified_design_capacity(self):
        """Get low_speed_user_specified_design_capacity.

        Returns:
            float: the value of `low_speed_user_specified_design_capacity` or None if not set

        """
        return self["Low Speed User Specified Design Capacity"]

    @low_speed_user_specified_design_capacity.setter
    def low_speed_user_specified_design_capacity(self, value=None):
        """  Corresponds to IDD field `Low Speed User Specified Design Capacity`
        Only used for Performance Input Method = UserSpecifiedDesignCapacity;
        for other Performance Input Methods, this field is ignored.

        Args:
            value (float or "Autocalculate"): value for IDD Field `Low Speed User Specified Design Capacity`
                Units: W
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Low Speed User Specified Design Capacity"] = value

    @property
    def low_speed_user_specified_design_capacity_sizing_factor(self):
        """Get low_speed_user_specified_design_capacity_sizing_factor.

        Returns:
            float: the value of `low_speed_user_specified_design_capacity_sizing_factor` or None if not set

        """
        return self["Low Speed User Specified Design Capacity Sizing Factor"]

    @low_speed_user_specified_design_capacity_sizing_factor.setter
    def low_speed_user_specified_design_capacity_sizing_factor(
            self,
            value=0.5):
        """Corresponds to IDD field `Low Speed User Specified Design Capacity
        Sizing Factor` This field is only used if the previous field is set to
        autocalculate.

        Args:
            value (float): value for IDD Field `Low Speed User Specified Design Capacity Sizing Factor`
                Default value: 0.5
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Low Speed User Specified Design Capacity Sizing Factor"] = value

    @property
    def design_entering_water_temperature(self):
        """Get design_entering_water_temperature.

        Returns:
            float: the value of `design_entering_water_temperature` or None if not set

        """
        return self["Design Entering Water Temperature"]

    @design_entering_water_temperature.setter
    def design_entering_water_temperature(self, value=None):
        """  Corresponds to IDD field `Design Entering Water Temperature`
        Only used for Performance Input Method = UserSpecifiedDesignCapacity;
        for other Performance Input Methods, this field is ignored.
        Design Entering Water Temperature must be greater than Design Entering Air Temperature.

        Args:
            value (float): value for IDD Field `Design Entering Water Temperature`
                Units: C
                IP-Units: F
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Design Entering Water Temperature"] = value

    @property
    def design_entering_air_temperature(self):
        """Get design_entering_air_temperature.

        Returns:
            float: the value of `design_entering_air_temperature` or None if not set

        """
        return self["Design Entering Air Temperature"]

    @design_entering_air_temperature.setter
    def design_entering_air_temperature(self, value=None):
        """  Corresponds to IDD field `Design Entering Air Temperature`
        Only used for Performance Input Method = UserSpecifiedDesignCapacity;
        for other Performance Input Methods, this field is ignored.
        Design Entering Air Temperature must be greater than Design Entering Air Wet-bulb
        Temperature.

        Args:
            value (float): value for IDD Field `Design Entering Air Temperature`
                Units: C
                IP-Units: F
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Design Entering Air Temperature"] = value

    @property
    def design_entering_air_wetbulb_temperature(self):
        """Get design_entering_air_wetbulb_temperature.

        Returns:
            float: the value of `design_entering_air_wetbulb_temperature` or None if not set

        """
        return self["Design Entering Air Wet-bulb Temperature"]

    @design_entering_air_wetbulb_temperature.setter
    def design_entering_air_wetbulb_temperature(self, value=None):
        """  Corresponds to IDD field `Design Entering Air Wet-bulb Temperature`
        Only used for Performance Input Method = UserSpecifiedDesignCapacity;
        for other Performance Input Methods, this field is ignored.
        Design Entering Air Wet-bulb Temperature must be less than Design Entering Air
        Temperature.

        Args:
            value (float): value for IDD Field `Design Entering Air Wet-bulb Temperature`
                Units: C
                IP-Units: F
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Design Entering Air Wet-bulb Temperature"] = value

    @property
    def high_speed_sizing_factor(self):
        """Get high_speed_sizing_factor.

        Returns:
            float: the value of `high_speed_sizing_factor` or None if not set

        """
        return self["High Speed Sizing Factor"]

    @high_speed_sizing_factor.setter
    def high_speed_sizing_factor(self, value=1.0):
        """Corresponds to IDD field `High Speed Sizing Factor` Multiplies the
        autosized capacity and flow rates.

        Args:
            value (float): value for IDD Field `High Speed Sizing Factor`
                Default value: 1.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["High Speed Sizing Factor"] = value

    @property
    def evaporation_loss_mode(self):
        """Get evaporation_loss_mode.

        Returns:
            str: the value of `evaporation_loss_mode` or None if not set

        """
        return self["Evaporation Loss Mode"]

    @evaporation_loss_mode.setter
    def evaporation_loss_mode(self, value="SaturatedExit"):
        """Corresponds to IDD field `Evaporation Loss Mode`

        Args:
            value (str): value for IDD Field `Evaporation Loss Mode`
                Default value: SaturatedExit
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Evaporation Loss Mode"] = value

    @property
    def evaporation_loss_factor(self):
        """Get evaporation_loss_factor.

        Returns:
            float: the value of `evaporation_loss_factor` or None if not set

        """
        return self["Evaporation Loss Factor"]

    @evaporation_loss_factor.setter
    def evaporation_loss_factor(self, value=None):
        """Corresponds to IDD field `Evaporation Loss Factor` Rate of water
        evaporation from the Fluid Cooler and lost to the outdoor air [%/K]
        Empirical correlation is used to calculate default loss factor if it
        not explicitly provided.

        Args:
            value (float): value for IDD Field `Evaporation Loss Factor`
                Units: percent/K
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Evaporation Loss Factor"] = value

    @property
    def drift_loss_percent(self):
        """Get drift_loss_percent.

        Returns:
            float: the value of `drift_loss_percent` or None if not set

        """
        return self["Drift Loss Percent"]

    @drift_loss_percent.setter
    def drift_loss_percent(self, value=0.008):
        """Corresponds to IDD field `Drift Loss Percent` Default value is under
        investigation. For now cooling towers default value is taken.

        Args:
            value (float): value for IDD Field `Drift Loss Percent`
                Units: percent
                Default value: 0.008
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Drift Loss Percent"] = value

    @property
    def blowdown_calculation_mode(self):
        """Get blowdown_calculation_mode.

        Returns:
            str: the value of `blowdown_calculation_mode` or None if not set

        """
        return self["Blowdown Calculation Mode"]

    @blowdown_calculation_mode.setter
    def blowdown_calculation_mode(self, value="ConcentrationRatio"):
        """Corresponds to IDD field `Blowdown Calculation Mode`

        Args:
            value (str): value for IDD Field `Blowdown Calculation Mode`
                Default value: ConcentrationRatio
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Blowdown Calculation Mode"] = value

    @property
    def blowdown_concentration_ratio(self):
        """Get blowdown_concentration_ratio.

        Returns:
            float: the value of `blowdown_concentration_ratio` or None if not set

        """
        return self["Blowdown Concentration Ratio"]

    @blowdown_concentration_ratio.setter
    def blowdown_concentration_ratio(self, value=3.0):
        """Corresponds to IDD field `Blowdown Concentration Ratio`
        Characterizes the rate of blowdown in the Evaporative Fluid Cooler.
        Blowdown is water intentionally drained from the Evaporative Fluid
        Cooler in order to offset the build up of solids in the water that
        would otherwise occur because of evaporation. Ratio of solids in the
        blowdown water to solids in the make up water. Default value is under
        investigation. For now cooling towers default value is taken.

        Args:
            value (float): value for IDD Field `Blowdown Concentration Ratio`
                Default value: 3.0
                value >= 2.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Blowdown Concentration Ratio"] = value

    @property
    def blowdown_makeup_water_usage_schedule_name(self):
        """Get blowdown_makeup_water_usage_schedule_name.

        Returns:
            str: the value of `blowdown_makeup_water_usage_schedule_name` or None if not set

        """
        return self["Blowdown Makeup Water Usage Schedule Name"]

    @blowdown_makeup_water_usage_schedule_name.setter
    def blowdown_makeup_water_usage_schedule_name(self, value=None):
        """Corresponds to IDD field `Blowdown Makeup Water Usage Schedule Name`
        Makeup water usage due to blowdown results from occasionally draining
        some amount of water in the Evaporative Fluid Cooler basin to purge
        scale or other contaminants to reduce their concentration in order to
        maintain an acceptable level of water quality. Schedule values should
        reflect water usage in m3/s.

        Args:
            value (str): value for IDD Field `Blowdown Makeup Water Usage Schedule Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Blowdown Makeup Water Usage Schedule Name"] = value

    @property
    def supply_water_storage_tank_name(self):
        """Get supply_water_storage_tank_name.

        Returns:
            str: the value of `supply_water_storage_tank_name` or None if not set

        """
        return self["Supply Water Storage Tank Name"]

    @supply_water_storage_tank_name.setter
    def supply_water_storage_tank_name(self, value=None):
        """Corresponds to IDD field `Supply Water Storage Tank Name`

        Args:
            value (str): value for IDD Field `Supply Water Storage Tank Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Supply Water Storage Tank Name"] = value




class FluidCoolerSingleSpeed(DataObject):

    """ Corresponds to IDD object `FluidCooler:SingleSpeed`
        The fluid cooler is modeled as a cross flow heat exchanger (both streams unmixed) with
        single-speed fans (induced draft configuration).
    """
    schema = {'extensible-fields': OrderedDict(),
              'fields': OrderedDict([(u'name',
                                      {'name': u'Name',
                                       'pyname': u'name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'alpha'}),
                                     (u'water inlet node name',
                                      {'name': u'Water Inlet Node Name',
                                       'pyname': u'water_inlet_node_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'node'}),
                                     (u'water outlet node name',
                                      {'name': u'Water Outlet Node Name',
                                       'pyname': u'water_outlet_node_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'node'}),
                                     (u'performance input method',
                                      {'name': u'Performance Input Method',
                                       'pyname': u'performance_input_method',
                                       'default': u'NominalCapacity',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'UFactorTimesAreaAndDesignWaterFlowRate',
                                                           u'NominalCapacity'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'design air flow rate u-factor times area value',
                                      {'name': u'Design Air Flow Rate U-factor Times Area Value',
                                       'pyname': u'design_air_flow_rate_ufactor_times_area_value',
                                       'minimum>': 0.0,
                                       'maximum': 2100000.0,
                                       'required-field': False,
                                       'autosizable': True,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'W/K'}),
                                     (u'nominal capacity',
                                      {'name': u'Nominal Capacity',
                                       'pyname': u'nominal_capacity',
                                       'minimum>': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'W'}),
                                     (u'design entering water temperature',
                                      {'name': u'Design Entering Water Temperature',
                                       'pyname': u'design_entering_water_temperature',
                                       'minimum>': 0.0,
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'C'}),
                                     (u'design entering air temperature',
                                      {'name': u'Design Entering Air Temperature',
                                       'pyname': u'design_entering_air_temperature',
                                       'minimum>': 0.0,
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'C'}),
                                     (u'design entering air wetbulb temperature',
                                      {'name': u'Design Entering Air Wetbulb Temperature',
                                       'pyname': u'design_entering_air_wetbulb_temperature',
                                       'minimum>': 0.0,
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'C'}),
                                     (u'design water flow rate',
                                      {'name': u'Design Water Flow Rate',
                                       'pyname': u'design_water_flow_rate',
                                       'minimum>': 0.0,
                                       'required-field': True,
                                       'autosizable': True,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'm3/s'}),
                                     (u'design air flow rate',
                                      {'name': u'Design Air Flow Rate',
                                       'pyname': u'design_air_flow_rate',
                                       'minimum>': 0.0,
                                       'required-field': True,
                                       'autosizable': True,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'm3/s'}),
                                     (u'design air flow rate fan power',
                                      {'name': u'Design Air Flow Rate Fan Power',
                                       'pyname': u'design_air_flow_rate_fan_power',
                                       'minimum>': 0.0,
                                       'required-field': True,
                                       'autosizable': True,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'W'}),
                                     (u'outdoor air inlet node name',
                                      {'name': u'Outdoor Air Inlet Node Name',
                                       'pyname': u'outdoor_air_inlet_node_name',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'node'})]),
              'format': None,
              'group': u'Condenser Equipment and Heat Exchangers',
              'min-fields': 12,
              'name': u'FluidCooler:SingleSpeed',
              'pyname': u'FluidCoolerSingleSpeed',
              'required-object': False,
              'unique-object': False}

    @property
    def name(self):
        """Get name.

        Returns:
            str: the value of `name` or None if not set

        """
        return self["Name"]

    @name.setter
    def name(self, value=None):
        """Corresponds to IDD field `Name` fluid cooler name.

        Args:
            value (str): value for IDD Field `Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Name"] = value

    @property
    def water_inlet_node_name(self):
        """Get water_inlet_node_name.

        Returns:
            str: the value of `water_inlet_node_name` or None if not set

        """
        return self["Water Inlet Node Name"]

    @water_inlet_node_name.setter
    def water_inlet_node_name(self, value=None):
        """Corresponds to IDD field `Water Inlet Node Name` Name of fluid
        cooler water inlet node.

        Args:
            value (str): value for IDD Field `Water Inlet Node Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Water Inlet Node Name"] = value

    @property
    def water_outlet_node_name(self):
        """Get water_outlet_node_name.

        Returns:
            str: the value of `water_outlet_node_name` or None if not set

        """
        return self["Water Outlet Node Name"]

    @water_outlet_node_name.setter
    def water_outlet_node_name(self, value=None):
        """Corresponds to IDD field `Water Outlet Node Name` Name of fluid
        cooler water outlet node.

        Args:
            value (str): value for IDD Field `Water Outlet Node Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Water Outlet Node Name"] = value

    @property
    def performance_input_method(self):
        """Get performance_input_method.

        Returns:
            str: the value of `performance_input_method` or None if not set

        """
        return self["Performance Input Method"]

    @performance_input_method.setter
    def performance_input_method(self, value="NominalCapacity"):
        """Corresponds to IDD field `Performance Input Method` User can define
        fluid cooler thermal performance by specifying the fluid cooler UA and
        the Design Water Flow Rate, or by specifying the fluid cooler nominal
        capacity.

        Args:
            value (str): value for IDD Field `Performance Input Method`
                Default value: NominalCapacity
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Performance Input Method"] = value

    @property
    def design_air_flow_rate_ufactor_times_area_value(self):
        """Get design_air_flow_rate_ufactor_times_area_value.

        Returns:
            float: the value of `design_air_flow_rate_ufactor_times_area_value` or None if not set

        """
        return self["Design Air Flow Rate U-factor Times Area Value"]

    @design_air_flow_rate_ufactor_times_area_value.setter
    def design_air_flow_rate_ufactor_times_area_value(self, value=None):
        """  Corresponds to IDD field `Design Air Flow Rate U-factor Times Area Value`
        Leave field blank if fluid cooler Performance Input Method is NominalCapacity

        Args:
            value (float or "Autosize"): value for IDD Field `Design Air Flow Rate U-factor Times Area Value`
                Units: W/K
                value <= 2100000.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Design Air Flow Rate U-factor Times Area Value"] = value

    @property
    def nominal_capacity(self):
        """Get nominal_capacity.

        Returns:
            float: the value of `nominal_capacity` or None if not set

        """
        return self["Nominal Capacity"]

    @nominal_capacity.setter
    def nominal_capacity(self, value=None):
        """Corresponds to IDD field `Nominal Capacity` Nominal fluid cooler
        capacity.

        Args:
            value (float): value for IDD Field `Nominal Capacity`
                Units: W
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Nominal Capacity"] = value

    @property
    def design_entering_water_temperature(self):
        """Get design_entering_water_temperature.

        Returns:
            float: the value of `design_entering_water_temperature` or None if not set

        """
        return self["Design Entering Water Temperature"]

    @design_entering_water_temperature.setter
    def design_entering_water_temperature(self, value=None):
        """Corresponds to IDD field `Design Entering Water Temperature` Design
        Entering Water Temperature must be specified for both the performance
        input methods and its value must be greater than Design Entering Air
        Temperature.

        Args:
            value (float): value for IDD Field `Design Entering Water Temperature`
                Units: C
                IP-Units: F
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Design Entering Water Temperature"] = value

    @property
    def design_entering_air_temperature(self):
        """Get design_entering_air_temperature.

        Returns:
            float: the value of `design_entering_air_temperature` or None if not set

        """
        return self["Design Entering Air Temperature"]

    @design_entering_air_temperature.setter
    def design_entering_air_temperature(self, value=None):
        """  Corresponds to IDD field `Design Entering Air Temperature`
        Design Entering Air Temperature must be specified for both the performance input methods and
        its value must be greater than Design Entering Air Wet-bulb Temperature.

        Args:
            value (float): value for IDD Field `Design Entering Air Temperature`
                Units: C
                IP-Units: F
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Design Entering Air Temperature"] = value

    @property
    def design_entering_air_wetbulb_temperature(self):
        """Get design_entering_air_wetbulb_temperature.

        Returns:
            float: the value of `design_entering_air_wetbulb_temperature` or None if not set

        """
        return self["Design Entering Air Wetbulb Temperature"]

    @design_entering_air_wetbulb_temperature.setter
    def design_entering_air_wetbulb_temperature(self, value=None):
        """  Corresponds to IDD field `Design Entering Air Wetbulb Temperature`
        Design Entering Air Wet-bulb Temperature must be specified for both the performance input methods and
        its value must be less than Design Entering Air Temperature.

        Args:
            value (float): value for IDD Field `Design Entering Air Wetbulb Temperature`
                Units: C
                IP-Units: F
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Design Entering Air Wetbulb Temperature"] = value

    @property
    def design_water_flow_rate(self):
        """Get design_water_flow_rate.

        Returns:
            float: the value of `design_water_flow_rate` or None if not set

        """
        return self["Design Water Flow Rate"]

    @design_water_flow_rate.setter
    def design_water_flow_rate(self, value=None):
        """Corresponds to IDD field `Design Water Flow Rate`

        Args:
            value (float or "Autosize"): value for IDD Field `Design Water Flow Rate`
                Units: m3/s
                IP-Units: gal/min
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Design Water Flow Rate"] = value

    @property
    def design_air_flow_rate(self):
        """Get design_air_flow_rate.

        Returns:
            float: the value of `design_air_flow_rate` or None if not set

        """
        return self["Design Air Flow Rate"]

    @design_air_flow_rate.setter
    def design_air_flow_rate(self, value=None):
        """Corresponds to IDD field `Design Air Flow Rate`

        Args:
            value (float or "Autosize"): value for IDD Field `Design Air Flow Rate`
                Units: m3/s
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Design Air Flow Rate"] = value

    @property
    def design_air_flow_rate_fan_power(self):
        """Get design_air_flow_rate_fan_power.

        Returns:
            float: the value of `design_air_flow_rate_fan_power` or None if not set

        """
        return self["Design Air Flow Rate Fan Power"]

    @design_air_flow_rate_fan_power.setter
    def design_air_flow_rate_fan_power(self, value=None):
        """Corresponds to IDD field `Design Air Flow Rate Fan Power` This is
        the fan motor electric input power.

        Args:
            value (float or "Autosize"): value for IDD Field `Design Air Flow Rate Fan Power`
                Units: W
                IP-Units: W
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Design Air Flow Rate Fan Power"] = value

    @property
    def outdoor_air_inlet_node_name(self):
        """Get outdoor_air_inlet_node_name.

        Returns:
            str: the value of `outdoor_air_inlet_node_name` or None if not set

        """
        return self["Outdoor Air Inlet Node Name"]

    @outdoor_air_inlet_node_name.setter
    def outdoor_air_inlet_node_name(self, value=None):
        """Corresponds to IDD field `Outdoor Air Inlet Node Name` Enter the
        name of an outdoor air node.

        Args:
            value (str): value for IDD Field `Outdoor Air Inlet Node Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Outdoor Air Inlet Node Name"] = value




class FluidCoolerTwoSpeed(DataObject):

    """ Corresponds to IDD object `FluidCooler:TwoSpeed`
        The fluid cooler is modeled as a cross flow heat exchanger (both streams unmixed) with
        two-speed fans (induced draft configuration).
    """
    schema = {'extensible-fields': OrderedDict(),
              'fields': OrderedDict([(u'name',
                                      {'name': u'Name',
                                       'pyname': u'name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'alpha'}),
                                     (u'water inlet node name',
                                      {'name': u'Water Inlet Node Name',
                                       'pyname': u'water_inlet_node_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'node'}),
                                     (u'water outlet node name',
                                      {'name': u'Water Outlet Node Name',
                                       'pyname': u'water_outlet_node_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'node'}),
                                     (u'performance input method',
                                      {'name': u'Performance Input Method',
                                       'pyname': u'performance_input_method',
                                       'default': u'NominalCapacity',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'UFactorTimesAreaAndDesignWaterFlowRate',
                                                           u'NominalCapacity'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'high fan speed u-factor times area value',
                                      {'name': u'High Fan Speed U-factor Times Area Value',
                                       'pyname': u'high_fan_speed_ufactor_times_area_value',
                                       'minimum>': 0.0,
                                       'maximum': 2100000.0,
                                       'required-field': False,
                                       'autosizable': True,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'W/K'}),
                                     (u'low fan speed u-factor times area value',
                                      {'name': u'Low Fan Speed U-factor Times Area Value',
                                       'pyname': u'low_fan_speed_ufactor_times_area_value',
                                       'minimum>': 0.0,
                                       'maximum': 300000.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': True,
                                       'type': u'real',
                                       'unit': u'W/K'}),
                                     (u'low fan speed u-factor times area sizing factor',
                                      {'name': u'Low Fan Speed U-Factor Times Area Sizing Factor',
                                       'pyname': u'low_fan_speed_ufactor_times_area_sizing_factor',
                                       'default': 0.6,
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'high speed nominal capacity',
                                      {'name': u'High Speed Nominal Capacity',
                                       'pyname': u'high_speed_nominal_capacity',
                                       'minimum>': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'W'}),
                                     (u'low speed nominal capacity',
                                      {'name': u'Low Speed Nominal Capacity',
                                       'pyname': u'low_speed_nominal_capacity',
                                       'minimum>': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': True,
                                       'type': u'real',
                                       'unit': u'W'}),
                                     (u'low speed nominal capacity sizing factor',
                                      {'name': u'Low Speed Nominal Capacity Sizing Factor',
                                       'pyname': u'low_speed_nominal_capacity_sizing_factor',
                                       'default': 0.5,
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'design entering water temperature',
                                      {'name': u'Design Entering Water Temperature',
                                       'pyname': u'design_entering_water_temperature',
                                       'minimum>': 0.0,
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'C'}),
                                     (u'design entering air temperature',
                                      {'name': u'Design Entering Air Temperature',
                                       'pyname': u'design_entering_air_temperature',
                                       'minimum>': 0.0,
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'C'}),
                                     (u'design entering air wet-bulb temperature',
                                      {'name': u'Design Entering Air Wet-bulb Temperature',
                                       'pyname': u'design_entering_air_wetbulb_temperature',
                                       'minimum>': 0.0,
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'C'}),
                                     (u'design water flow rate',
                                      {'name': u'Design Water Flow Rate',
                                       'pyname': u'design_water_flow_rate',
                                       'minimum>': 0.0,
                                       'required-field': True,
                                       'autosizable': True,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'm3/s'}),
                                     (u'high fan speed air flow rate',
                                      {'name': u'High Fan Speed Air Flow Rate',
                                       'pyname': u'high_fan_speed_air_flow_rate',
                                       'minimum>': 0.0,
                                       'required-field': True,
                                       'autosizable': True,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'm3/s'}),
                                     (u'high fan speed fan power',
                                      {'name': u'High Fan Speed Fan Power',
                                       'pyname': u'high_fan_speed_fan_power',
                                       'minimum>': 0.0,
                                       'required-field': True,
                                       'autosizable': True,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'W'}),
                                     (u'low fan speed air flow rate',
                                      {'name': u'Low Fan Speed Air Flow Rate',
                                       'pyname': u'low_fan_speed_air_flow_rate',
                                       'minimum>': 0.0,
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': True,
                                       'type': u'real',
                                       'unit': u'm3/s'}),
                                     (u'low fan speed air flow rate sizing factor',
                                      {'name': u'Low Fan Speed Air Flow Rate Sizing Factor',
                                       'pyname': u'low_fan_speed_air_flow_rate_sizing_factor',
                                       'default': 0.5,
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'low fan speed fan power',
                                      {'name': u'Low Fan Speed Fan Power',
                                       'pyname': u'low_fan_speed_fan_power',
                                       'minimum>': 0.0,
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': True,
                                       'type': u'real',
                                       'unit': u'W'}),
                                     (u'low fan speed fan power sizing factor',
                                      {'name': u'Low Fan Speed Fan Power Sizing Factor',
                                       'pyname': u'low_fan_speed_fan_power_sizing_factor',
                                       'default': 0.16,
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'outdoor air inlet node name',
                                      {'name': u'Outdoor Air Inlet Node Name',
                                       'pyname': u'outdoor_air_inlet_node_name',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'node'})]),
              'format': None,
              'group': u'Condenser Equipment and Heat Exchangers',
              'min-fields': 20,
              'name': u'FluidCooler:TwoSpeed',
              'pyname': u'FluidCoolerTwoSpeed',
              'required-object': False,
              'unique-object': False}

    @property
    def name(self):
        """Get name.

        Returns:
            str: the value of `name` or None if not set

        """
        return self["Name"]

    @name.setter
    def name(self, value=None):
        """Corresponds to IDD field `Name` fluid cooler name.

        Args:
            value (str): value for IDD Field `Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Name"] = value

    @property
    def water_inlet_node_name(self):
        """Get water_inlet_node_name.

        Returns:
            str: the value of `water_inlet_node_name` or None if not set

        """
        return self["Water Inlet Node Name"]

    @water_inlet_node_name.setter
    def water_inlet_node_name(self, value=None):
        """Corresponds to IDD field `Water Inlet Node Name` Name of fluid
        cooler water inlet node.

        Args:
            value (str): value for IDD Field `Water Inlet Node Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Water Inlet Node Name"] = value

    @property
    def water_outlet_node_name(self):
        """Get water_outlet_node_name.

        Returns:
            str: the value of `water_outlet_node_name` or None if not set

        """
        return self["Water Outlet Node Name"]

    @water_outlet_node_name.setter
    def water_outlet_node_name(self, value=None):
        """Corresponds to IDD field `Water Outlet Node Name` Name of fluid
        cooler water outlet node.

        Args:
            value (str): value for IDD Field `Water Outlet Node Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Water Outlet Node Name"] = value

    @property
    def performance_input_method(self):
        """Get performance_input_method.

        Returns:
            str: the value of `performance_input_method` or None if not set

        """
        return self["Performance Input Method"]

    @performance_input_method.setter
    def performance_input_method(self, value="NominalCapacity"):
        """Corresponds to IDD field `Performance Input Method` User can define
        fluid cooler thermal performance by specifying the fluid cooler UA and
        the Design Water Flow Rate, or by specifying the fluid cooler nominal
        capacity.

        Args:
            value (str): value for IDD Field `Performance Input Method`
                Default value: NominalCapacity
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Performance Input Method"] = value

    @property
    def high_fan_speed_ufactor_times_area_value(self):
        """Get high_fan_speed_ufactor_times_area_value.

        Returns:
            float: the value of `high_fan_speed_ufactor_times_area_value` or None if not set

        """
        return self["High Fan Speed U-factor Times Area Value"]

    @high_fan_speed_ufactor_times_area_value.setter
    def high_fan_speed_ufactor_times_area_value(self, value=None):
        """  Corresponds to IDD field `High Fan Speed U-factor Times Area Value`
        Leave field blank if fluid cooler Performance Input Method is NominalCapacity

        Args:
            value (float or "Autosize"): value for IDD Field `High Fan Speed U-factor Times Area Value`
                Units: W/K
                value <= 2100000.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["High Fan Speed U-factor Times Area Value"] = value

    @property
    def low_fan_speed_ufactor_times_area_value(self):
        """Get low_fan_speed_ufactor_times_area_value.

        Returns:
            float: the value of `low_fan_speed_ufactor_times_area_value` or None if not set

        """
        return self["Low Fan Speed U-factor Times Area Value"]

    @low_fan_speed_ufactor_times_area_value.setter
    def low_fan_speed_ufactor_times_area_value(self, value=None):
        """  Corresponds to IDD field `Low Fan Speed U-factor Times Area Value`
        Leave field blank if fluid cooler Performance Input Method is NominalCapacity
        Low speed fluid cooler UA must be less than high speed fluid cooler UA
        Low speed fluid cooler UA must be greater than free convection fluid cooler UA

        Args:
            value (float or "Autocalculate"): value for IDD Field `Low Fan Speed U-factor Times Area Value`
                Units: W/K
                value <= 300000.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Low Fan Speed U-factor Times Area Value"] = value

    @property
    def low_fan_speed_ufactor_times_area_sizing_factor(self):
        """Get low_fan_speed_ufactor_times_area_sizing_factor.

        Returns:
            float: the value of `low_fan_speed_ufactor_times_area_sizing_factor` or None if not set

        """
        return self["Low Fan Speed U-Factor Times Area Sizing Factor"]

    @low_fan_speed_ufactor_times_area_sizing_factor.setter
    def low_fan_speed_ufactor_times_area_sizing_factor(self, value=0.6):
        """  Corresponds to IDD field `Low Fan Speed U-Factor Times Area Sizing Factor`
        This field is only used if the previous field is set to autocalculate and
        the Performance Input Method is UFactorTimesAreaAndDesignWaterFlowRate

        Args:
            value (float): value for IDD Field `Low Fan Speed U-Factor Times Area Sizing Factor`
                Default value: 0.6
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Low Fan Speed U-Factor Times Area Sizing Factor"] = value

    @property
    def high_speed_nominal_capacity(self):
        """Get high_speed_nominal_capacity.

        Returns:
            float: the value of `high_speed_nominal_capacity` or None if not set

        """
        return self["High Speed Nominal Capacity"]

    @high_speed_nominal_capacity.setter
    def high_speed_nominal_capacity(self, value=None):
        """Corresponds to IDD field `High Speed Nominal Capacity` Nominal fluid
        cooler capacity at high fan speed.

        Args:
            value (float): value for IDD Field `High Speed Nominal Capacity`
                Units: W
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["High Speed Nominal Capacity"] = value

    @property
    def low_speed_nominal_capacity(self):
        """Get low_speed_nominal_capacity.

        Returns:
            float: the value of `low_speed_nominal_capacity` or None if not set

        """
        return self["Low Speed Nominal Capacity"]

    @low_speed_nominal_capacity.setter
    def low_speed_nominal_capacity(self, value=None):
        """Corresponds to IDD field `Low Speed Nominal Capacity` Nominal fluid
        cooler capacity at low fan speed.

        Args:
            value (float or "Autocalculate"): value for IDD Field `Low Speed Nominal Capacity`
                Units: W
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Low Speed Nominal Capacity"] = value

    @property
    def low_speed_nominal_capacity_sizing_factor(self):
        """Get low_speed_nominal_capacity_sizing_factor.

        Returns:
            float: the value of `low_speed_nominal_capacity_sizing_factor` or None if not set

        """
        return self["Low Speed Nominal Capacity Sizing Factor"]

    @low_speed_nominal_capacity_sizing_factor.setter
    def low_speed_nominal_capacity_sizing_factor(self, value=0.5):
        """Corresponds to IDD field `Low Speed Nominal Capacity Sizing Factor`
        This field is only used if the previous field is set to autocalculate
        and the Performance Input Method is NominalCapacity.

        Args:
            value (float): value for IDD Field `Low Speed Nominal Capacity Sizing Factor`
                Default value: 0.5
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Low Speed Nominal Capacity Sizing Factor"] = value

    @property
    def design_entering_water_temperature(self):
        """Get design_entering_water_temperature.

        Returns:
            float: the value of `design_entering_water_temperature` or None if not set

        """
        return self["Design Entering Water Temperature"]

    @design_entering_water_temperature.setter
    def design_entering_water_temperature(self, value=None):
        """Corresponds to IDD field `Design Entering Water Temperature` Design
        Entering Water Temperature must be specified for both the performance
        input methods and its value must be greater than Design Entering Air
        Temperature.

        Args:
            value (float): value for IDD Field `Design Entering Water Temperature`
                Units: C
                IP-Units: F
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Design Entering Water Temperature"] = value

    @property
    def design_entering_air_temperature(self):
        """Get design_entering_air_temperature.

        Returns:
            float: the value of `design_entering_air_temperature` or None if not set

        """
        return self["Design Entering Air Temperature"]

    @design_entering_air_temperature.setter
    def design_entering_air_temperature(self, value=None):
        """  Corresponds to IDD field `Design Entering Air Temperature`
        Design Entering Air Temperature must be specified for both the performance input methods and
        its value must be greater than Design Entering Air Wet-bulb Temperature.

        Args:
            value (float): value for IDD Field `Design Entering Air Temperature`
                Units: C
                IP-Units: F
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Design Entering Air Temperature"] = value

    @property
    def design_entering_air_wetbulb_temperature(self):
        """Get design_entering_air_wetbulb_temperature.

        Returns:
            float: the value of `design_entering_air_wetbulb_temperature` or None if not set

        """
        return self["Design Entering Air Wet-bulb Temperature"]

    @design_entering_air_wetbulb_temperature.setter
    def design_entering_air_wetbulb_temperature(self, value=None):
        """  Corresponds to IDD field `Design Entering Air Wet-bulb Temperature`
        Design Entering Air Wet-bulb Temperature must be specified for both the performance input methods and
        its value must be less than Design Entering Air Temperature.

        Args:
            value (float): value for IDD Field `Design Entering Air Wet-bulb Temperature`
                Units: C
                IP-Units: F
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Design Entering Air Wet-bulb Temperature"] = value

    @property
    def design_water_flow_rate(self):
        """Get design_water_flow_rate.

        Returns:
            float: the value of `design_water_flow_rate` or None if not set

        """
        return self["Design Water Flow Rate"]

    @design_water_flow_rate.setter
    def design_water_flow_rate(self, value=None):
        """Corresponds to IDD field `Design Water Flow Rate`

        Args:
            value (float or "Autosize"): value for IDD Field `Design Water Flow Rate`
                Units: m3/s
                IP-Units: gal/min
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Design Water Flow Rate"] = value

    @property
    def high_fan_speed_air_flow_rate(self):
        """Get high_fan_speed_air_flow_rate.

        Returns:
            float: the value of `high_fan_speed_air_flow_rate` or None if not set

        """
        return self["High Fan Speed Air Flow Rate"]

    @high_fan_speed_air_flow_rate.setter
    def high_fan_speed_air_flow_rate(self, value=None):
        """Corresponds to IDD field `High Fan Speed Air Flow Rate` Air Flow
        Rate at High Fan Speed must be greater than Air Flow Rate at Low Fan
        Speed.

        Args:
            value (float or "Autosize"): value for IDD Field `High Fan Speed Air Flow Rate`
                Units: m3/s
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["High Fan Speed Air Flow Rate"] = value

    @property
    def high_fan_speed_fan_power(self):
        """Get high_fan_speed_fan_power.

        Returns:
            float: the value of `high_fan_speed_fan_power` or None if not set

        """
        return self["High Fan Speed Fan Power"]

    @high_fan_speed_fan_power.setter
    def high_fan_speed_fan_power(self, value=None):
        """Corresponds to IDD field `High Fan Speed Fan Power` This is the fan
        motor electric input power at high speed.

        Args:
            value (float or "Autosize"): value for IDD Field `High Fan Speed Fan Power`
                Units: W
                IP-Units: W
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["High Fan Speed Fan Power"] = value

    @property
    def low_fan_speed_air_flow_rate(self):
        """Get low_fan_speed_air_flow_rate.

        Returns:
            float: the value of `low_fan_speed_air_flow_rate` or None if not set

        """
        return self["Low Fan Speed Air Flow Rate"]

    @low_fan_speed_air_flow_rate.setter
    def low_fan_speed_air_flow_rate(self, value=None):
        """Corresponds to IDD field `Low Fan Speed Air Flow Rate` Air Flow Rate
        at Low Fan Speed must be less than Air Flow Rate at High Fan Speed.

        Args:
            value (float or "Autocalculate"): value for IDD Field `Low Fan Speed Air Flow Rate`
                Units: m3/s
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Low Fan Speed Air Flow Rate"] = value

    @property
    def low_fan_speed_air_flow_rate_sizing_factor(self):
        """Get low_fan_speed_air_flow_rate_sizing_factor.

        Returns:
            float: the value of `low_fan_speed_air_flow_rate_sizing_factor` or None if not set

        """
        return self["Low Fan Speed Air Flow Rate Sizing Factor"]

    @low_fan_speed_air_flow_rate_sizing_factor.setter
    def low_fan_speed_air_flow_rate_sizing_factor(self, value=0.5):
        """Corresponds to IDD field `Low Fan Speed Air Flow Rate Sizing Factor`
        This field is only used if the previous field is set to autocalculate.

        Args:
            value (float): value for IDD Field `Low Fan Speed Air Flow Rate Sizing Factor`
                Default value: 0.5
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Low Fan Speed Air Flow Rate Sizing Factor"] = value

    @property
    def low_fan_speed_fan_power(self):
        """Get low_fan_speed_fan_power.

        Returns:
            float: the value of `low_fan_speed_fan_power` or None if not set

        """
        return self["Low Fan Speed Fan Power"]

    @low_fan_speed_fan_power.setter
    def low_fan_speed_fan_power(self, value=None):
        """Corresponds to IDD field `Low Fan Speed Fan Power` This is the fan
        motor electric input power at low speed.

        Args:
            value (float or "Autocalculate"): value for IDD Field `Low Fan Speed Fan Power`
                Units: W
                IP-Units: W
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Low Fan Speed Fan Power"] = value

    @property
    def low_fan_speed_fan_power_sizing_factor(self):
        """Get low_fan_speed_fan_power_sizing_factor.

        Returns:
            float: the value of `low_fan_speed_fan_power_sizing_factor` or None if not set

        """
        return self["Low Fan Speed Fan Power Sizing Factor"]

    @low_fan_speed_fan_power_sizing_factor.setter
    def low_fan_speed_fan_power_sizing_factor(self, value=0.16):
        """Corresponds to IDD field `Low Fan Speed Fan Power Sizing Factor`
        This field is only used if the previous field is set to autocalculate.

        Args:
            value (float): value for IDD Field `Low Fan Speed Fan Power Sizing Factor`
                Default value: 0.16
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Low Fan Speed Fan Power Sizing Factor"] = value

    @property
    def outdoor_air_inlet_node_name(self):
        """Get outdoor_air_inlet_node_name.

        Returns:
            str: the value of `outdoor_air_inlet_node_name` or None if not set

        """
        return self["Outdoor Air Inlet Node Name"]

    @outdoor_air_inlet_node_name.setter
    def outdoor_air_inlet_node_name(self, value=None):
        """Corresponds to IDD field `Outdoor Air Inlet Node Name`

        Args:
            value (str): value for IDD Field `Outdoor Air Inlet Node Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Outdoor Air Inlet Node Name"] = value




class GroundHeatExchangerVertical(DataObject):

    """ Corresponds to IDD object `GroundHeatExchanger:Vertical`
        Variable short time step vertical ground heat exchanger model based on
        Yavuztruk, C., J.D.Spitler. 1999. A Short Time Step response Factor Model for
        Vertical Ground Loop Heat Exchangers
        The Fluid Type in the associated condenser loop must be same for which the
        g-functions below are calculated.
    """
    schema = {'extensible-fields': OrderedDict(),
              'fields': OrderedDict([(u'name',
                                      {'name': u'Name',
                                       'pyname': u'name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'inlet node name',
                                      {'name': u'Inlet Node Name',
                                       'pyname': u'inlet_node_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'node'}),
                                     (u'outlet node name',
                                      {'name': u'Outlet Node Name',
                                       'pyname': u'outlet_node_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'node'}),
                                     (u'maximum flow rate',
                                      {'name': u'Maximum Flow Rate',
                                       'pyname': u'maximum_flow_rate',
                                       'minimum>': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm3/s'}),
                                     (u'number of bore holes',
                                      {'name': u'Number of Bore Holes',
                                       'pyname': u'number_of_bore_holes',
                                       'minimum>': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real'}),
                                     (u'bore hole length',
                                      {'name': u'Bore Hole Length',
                                       'pyname': u'bore_hole_length',
                                       'minimum>': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'bore hole radius',
                                      {'name': u'Bore Hole Radius',
                                       'pyname': u'bore_hole_radius',
                                       'minimum>': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'ground thermal conductivity',
                                      {'name': u'Ground Thermal Conductivity',
                                       'pyname': u'ground_thermal_conductivity',
                                       'minimum>': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'W/m-K'}),
                                     (u'ground thermal heat capacity',
                                      {'name': u'Ground Thermal Heat Capacity',
                                       'pyname': u'ground_thermal_heat_capacity',
                                       'minimum>': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'J/m3-K'}),
                                     (u'ground temperature',
                                      {'name': u'Ground Temperature',
                                       'pyname': u'ground_temperature',
                                       'minimum>': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'C'}),
                                     (u'design flow rate',
                                      {'name': u'Design Flow Rate',
                                       'pyname': u'design_flow_rate',
                                       'minimum>': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm3/s'}),
                                     (u'grout thermal conductivity',
                                      {'name': u'Grout Thermal Conductivity',
                                       'pyname': u'grout_thermal_conductivity',
                                       'minimum>': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'W/m-K'}),
                                     (u'pipe thermal conductivity',
                                      {'name': u'Pipe Thermal Conductivity',
                                       'pyname': u'pipe_thermal_conductivity',
                                       'minimum>': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'W/m-K'}),
                                     (u'pipe out diameter',
                                      {'name': u'Pipe Out Diameter',
                                       'pyname': u'pipe_out_diameter',
                                       'minimum>': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'u-tube distance',
                                      {'name': u'U-Tube Distance',
                                       'pyname': u'utube_distance',
                                       'minimum>': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'pipe thickness',
                                      {'name': u'Pipe Thickness',
                                       'pyname': u'pipe_thickness',
                                       'minimum>': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'maximum length of simulation',
                                      {'name': u'Maximum Length of Simulation',
                                       'pyname': u'maximum_length_of_simulation',
                                       'minimum>': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real'}),
                                     (u'g-function reference ratio',
                                      {'name': u'G-Function Reference Ratio',
                                       'pyname': u'gfunction_reference_ratio',
                                       'default': 0.0005,
                                       'minimum>': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'dimensionless'}),
                                     (u'number of data pairs of the g function',
                                      {'name': u'Number of Data Pairs of the G Function',
                                       'pyname': u'number_of_data_pairs_of_the_g_function',
                                       'minimum>': 0.0,
                                       'maximum': 100.0,
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real'}),
                                     (u'g-function ln(t/ts) value 1',
                                      {'name': u'G-Function Ln(T/Ts) Value 1',
                                       'pyname': u'gfunction_lnt_or_ts_value_1',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 1',
                                      {'name': u'G-Function G Value 1',
                                       'pyname': u'gfunction_g_value_1',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 2',
                                      {'name': u'G-Function Ln(T/Ts) Value 2',
                                       'pyname': u'gfunction_lnt_or_ts_value_2',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 2',
                                      {'name': u'G-Function G Value 2',
                                       'pyname': u'gfunction_g_value_2',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 3',
                                      {'name': u'G-Function Ln(T/Ts) Value 3',
                                       'pyname': u'gfunction_lnt_or_ts_value_3',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 3',
                                      {'name': u'G-Function G Value 3',
                                       'pyname': u'gfunction_g_value_3',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 4',
                                      {'name': u'G-Function Ln(T/Ts) Value 4',
                                       'pyname': u'gfunction_lnt_or_ts_value_4',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 4',
                                      {'name': u'G-Function G Value 4',
                                       'pyname': u'gfunction_g_value_4',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 5',
                                      {'name': u'G-Function Ln(T/Ts) Value 5',
                                       'pyname': u'gfunction_lnt_or_ts_value_5',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 5',
                                      {'name': u'G-Function G Value 5',
                                       'pyname': u'gfunction_g_value_5',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 6',
                                      {'name': u'G-Function Ln(T/Ts) Value 6',
                                       'pyname': u'gfunction_lnt_or_ts_value_6',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 6',
                                      {'name': u'G-Function G Value 6',
                                       'pyname': u'gfunction_g_value_6',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 7',
                                      {'name': u'G-Function Ln(T/Ts) Value 7',
                                       'pyname': u'gfunction_lnt_or_ts_value_7',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 7',
                                      {'name': u'G-Function G Value 7',
                                       'pyname': u'gfunction_g_value_7',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 8',
                                      {'name': u'G-Function Ln(T/Ts) Value 8',
                                       'pyname': u'gfunction_lnt_or_ts_value_8',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 8',
                                      {'name': u'G-Function G Value 8',
                                       'pyname': u'gfunction_g_value_8',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 9',
                                      {'name': u'G-Function Ln(T/Ts) Value 9',
                                       'pyname': u'gfunction_lnt_or_ts_value_9',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 9',
                                      {'name': u'G-Function G Value 9',
                                       'pyname': u'gfunction_g_value_9',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 10',
                                      {'name': u'G-Function Ln(T/Ts) Value 10',
                                       'pyname': u'gfunction_lnt_or_ts_value_10',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 10',
                                      {'name': u'G-Function G Value 10',
                                       'pyname': u'gfunction_g_value_10',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 11',
                                      {'name': u'G-Function Ln(T/Ts) Value 11',
                                       'pyname': u'gfunction_lnt_or_ts_value_11',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 11',
                                      {'name': u'G-Function G Value 11',
                                       'pyname': u'gfunction_g_value_11',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 12',
                                      {'name': u'G-Function Ln(T/Ts) Value 12',
                                       'pyname': u'gfunction_lnt_or_ts_value_12',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 12',
                                      {'name': u'G-Function G Value 12',
                                       'pyname': u'gfunction_g_value_12',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 13',
                                      {'name': u'G-Function Ln(T/Ts) Value 13',
                                       'pyname': u'gfunction_lnt_or_ts_value_13',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 13',
                                      {'name': u'G-Function G Value 13',
                                       'pyname': u'gfunction_g_value_13',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 14',
                                      {'name': u'G-Function Ln(T/Ts) Value 14',
                                       'pyname': u'gfunction_lnt_or_ts_value_14',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 14',
                                      {'name': u'G-Function G Value 14',
                                       'pyname': u'gfunction_g_value_14',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 15',
                                      {'name': u'G-Function Ln(T/Ts) Value 15',
                                       'pyname': u'gfunction_lnt_or_ts_value_15',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 15',
                                      {'name': u'G-Function G Value 15',
                                       'pyname': u'gfunction_g_value_15',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 16',
                                      {'name': u'G-Function Ln(T/Ts) Value 16',
                                       'pyname': u'gfunction_lnt_or_ts_value_16',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 16',
                                      {'name': u'G-Function G Value 16',
                                       'pyname': u'gfunction_g_value_16',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 17',
                                      {'name': u'G-Function Ln(T/Ts) Value 17',
                                       'pyname': u'gfunction_lnt_or_ts_value_17',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 17',
                                      {'name': u'G-Function G Value 17',
                                       'pyname': u'gfunction_g_value_17',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 18',
                                      {'name': u'G-Function Ln(T/Ts) Value 18',
                                       'pyname': u'gfunction_lnt_or_ts_value_18',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 18',
                                      {'name': u'G-Function G Value 18',
                                       'pyname': u'gfunction_g_value_18',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 19',
                                      {'name': u'G-Function Ln(T/Ts) Value 19',
                                       'pyname': u'gfunction_lnt_or_ts_value_19',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 19',
                                      {'name': u'G-Function G Value 19',
                                       'pyname': u'gfunction_g_value_19',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 20',
                                      {'name': u'G-Function Ln(T/Ts) Value 20',
                                       'pyname': u'gfunction_lnt_or_ts_value_20',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 20',
                                      {'name': u'G-Function G Value 20',
                                       'pyname': u'gfunction_g_value_20',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 21',
                                      {'name': u'G-Function Ln(T/Ts) Value 21',
                                       'pyname': u'gfunction_lnt_or_ts_value_21',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 21',
                                      {'name': u'G-Function G Value 21',
                                       'pyname': u'gfunction_g_value_21',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 22',
                                      {'name': u'G-Function Ln(T/Ts) Value 22',
                                       'pyname': u'gfunction_lnt_or_ts_value_22',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 22',
                                      {'name': u'G-Function G Value 22',
                                       'pyname': u'gfunction_g_value_22',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 23',
                                      {'name': u'G-Function Ln(T/Ts) Value 23',
                                       'pyname': u'gfunction_lnt_or_ts_value_23',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 23',
                                      {'name': u'G-Function G Value 23',
                                       'pyname': u'gfunction_g_value_23',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 24',
                                      {'name': u'G-Function Ln(T/Ts) Value 24',
                                       'pyname': u'gfunction_lnt_or_ts_value_24',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 24',
                                      {'name': u'G-Function G Value 24',
                                       'pyname': u'gfunction_g_value_24',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 25',
                                      {'name': u'G-Function Ln(T/Ts) Value 25',
                                       'pyname': u'gfunction_lnt_or_ts_value_25',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 25',
                                      {'name': u'G-Function G Value 25',
                                       'pyname': u'gfunction_g_value_25',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 26',
                                      {'name': u'G-Function Ln(T/Ts) Value 26',
                                       'pyname': u'gfunction_lnt_or_ts_value_26',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 26',
                                      {'name': u'G-Function G Value 26',
                                       'pyname': u'gfunction_g_value_26',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 27',
                                      {'name': u'G-Function Ln(T/Ts) Value 27',
                                       'pyname': u'gfunction_lnt_or_ts_value_27',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 27',
                                      {'name': u'G-Function G Value 27',
                                       'pyname': u'gfunction_g_value_27',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 28',
                                      {'name': u'G-Function Ln(T/Ts) Value 28',
                                       'pyname': u'gfunction_lnt_or_ts_value_28',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 28',
                                      {'name': u'G-Function G Value 28',
                                       'pyname': u'gfunction_g_value_28',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 29',
                                      {'name': u'G-Function Ln(T/Ts) Value 29',
                                       'pyname': u'gfunction_lnt_or_ts_value_29',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 29',
                                      {'name': u'G-Function G Value 29',
                                       'pyname': u'gfunction_g_value_29',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 30',
                                      {'name': u'G-Function Ln(T/Ts) Value 30',
                                       'pyname': u'gfunction_lnt_or_ts_value_30',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 30',
                                      {'name': u'G-Function G Value 30',
                                       'pyname': u'gfunction_g_value_30',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 31',
                                      {'name': u'G-Function Ln(T/Ts) Value 31',
                                       'pyname': u'gfunction_lnt_or_ts_value_31',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 31',
                                      {'name': u'G-Function G Value 31',
                                       'pyname': u'gfunction_g_value_31',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 32',
                                      {'name': u'G-Function Ln(T/Ts) Value 32',
                                       'pyname': u'gfunction_lnt_or_ts_value_32',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 32',
                                      {'name': u'G-Function G Value 32',
                                       'pyname': u'gfunction_g_value_32',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 33',
                                      {'name': u'G-Function Ln(T/Ts) Value 33',
                                       'pyname': u'gfunction_lnt_or_ts_value_33',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 33',
                                      {'name': u'G-Function G Value 33',
                                       'pyname': u'gfunction_g_value_33',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 34',
                                      {'name': u'G-Function Ln(T/Ts) Value 34',
                                       'pyname': u'gfunction_lnt_or_ts_value_34',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 34',
                                      {'name': u'G-Function G Value 34',
                                       'pyname': u'gfunction_g_value_34',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 35',
                                      {'name': u'G-Function Ln(T/Ts) Value 35',
                                       'pyname': u'gfunction_lnt_or_ts_value_35',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 35',
                                      {'name': u'G-Function G Value 35',
                                       'pyname': u'gfunction_g_value_35',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 36',
                                      {'name': u'G-Function Ln(T/Ts) Value 36',
                                       'pyname': u'gfunction_lnt_or_ts_value_36',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 36',
                                      {'name': u'G-Function G Value 36',
                                       'pyname': u'gfunction_g_value_36',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 37',
                                      {'name': u'G-Function Ln(T/Ts) Value 37',
                                       'pyname': u'gfunction_lnt_or_ts_value_37',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 37',
                                      {'name': u'G-Function G Value 37',
                                       'pyname': u'gfunction_g_value_37',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 38',
                                      {'name': u'G-Function Ln(T/Ts) Value 38',
                                       'pyname': u'gfunction_lnt_or_ts_value_38',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 38',
                                      {'name': u'G-Function G Value 38',
                                       'pyname': u'gfunction_g_value_38',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 39',
                                      {'name': u'G-Function Ln(T/Ts) Value 39',
                                       'pyname': u'gfunction_lnt_or_ts_value_39',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 39',
                                      {'name': u'G-Function G Value 39',
                                       'pyname': u'gfunction_g_value_39',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 40',
                                      {'name': u'G-Function Ln(T/Ts) Value 40',
                                       'pyname': u'gfunction_lnt_or_ts_value_40',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 40',
                                      {'name': u'G-Function G Value 40',
                                       'pyname': u'gfunction_g_value_40',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 41',
                                      {'name': u'G-Function Ln(T/Ts) Value 41',
                                       'pyname': u'gfunction_lnt_or_ts_value_41',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 41',
                                      {'name': u'G-Function G Value 41',
                                       'pyname': u'gfunction_g_value_41',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 42',
                                      {'name': u'G-Function Ln(T/Ts) Value 42',
                                       'pyname': u'gfunction_lnt_or_ts_value_42',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 42',
                                      {'name': u'G-Function G Value 42',
                                       'pyname': u'gfunction_g_value_42',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 43',
                                      {'name': u'G-Function Ln(T/Ts) Value 43',
                                       'pyname': u'gfunction_lnt_or_ts_value_43',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 43',
                                      {'name': u'G-Function G Value 43',
                                       'pyname': u'gfunction_g_value_43',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 44',
                                      {'name': u'G-Function Ln(T/Ts) Value 44',
                                       'pyname': u'gfunction_lnt_or_ts_value_44',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 44',
                                      {'name': u'G-Function G Value 44',
                                       'pyname': u'gfunction_g_value_44',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 45',
                                      {'name': u'G-Function Ln(T/Ts) Value 45',
                                       'pyname': u'gfunction_lnt_or_ts_value_45',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 45',
                                      {'name': u'G-Function G Value 45',
                                       'pyname': u'gfunction_g_value_45',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 46',
                                      {'name': u'G-Function Ln(T/Ts) Value 46',
                                       'pyname': u'gfunction_lnt_or_ts_value_46',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 46',
                                      {'name': u'G-Function G Value 46',
                                       'pyname': u'gfunction_g_value_46',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 47',
                                      {'name': u'G-Function Ln(T/Ts) Value 47',
                                       'pyname': u'gfunction_lnt_or_ts_value_47',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 47',
                                      {'name': u'G-Function G Value 47',
                                       'pyname': u'gfunction_g_value_47',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 48',
                                      {'name': u'G-Function Ln(T/Ts) Value 48',
                                       'pyname': u'gfunction_lnt_or_ts_value_48',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 48',
                                      {'name': u'G-Function G Value 48',
                                       'pyname': u'gfunction_g_value_48',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 49',
                                      {'name': u'G-Function Ln(T/Ts) Value 49',
                                       'pyname': u'gfunction_lnt_or_ts_value_49',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 49',
                                      {'name': u'G-Function G Value 49',
                                       'pyname': u'gfunction_g_value_49',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 50',
                                      {'name': u'G-Function Ln(T/Ts) Value 50',
                                       'pyname': u'gfunction_lnt_or_ts_value_50',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 50',
                                      {'name': u'G-Function G Value 50',
                                       'pyname': u'gfunction_g_value_50',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 51',
                                      {'name': u'G-Function Ln(T/Ts) Value 51',
                                       'pyname': u'gfunction_lnt_or_ts_value_51',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 51',
                                      {'name': u'G-Function G Value 51',
                                       'pyname': u'gfunction_g_value_51',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 52',
                                      {'name': u'G-Function Ln(T/Ts) Value 52',
                                       'pyname': u'gfunction_lnt_or_ts_value_52',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 52',
                                      {'name': u'G-Function G Value 52',
                                       'pyname': u'gfunction_g_value_52',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 53',
                                      {'name': u'G-Function Ln(T/Ts) Value 53',
                                       'pyname': u'gfunction_lnt_or_ts_value_53',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 53',
                                      {'name': u'G-Function G Value 53',
                                       'pyname': u'gfunction_g_value_53',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 54',
                                      {'name': u'G-Function Ln(T/Ts) Value 54',
                                       'pyname': u'gfunction_lnt_or_ts_value_54',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 54',
                                      {'name': u'G-Function G Value 54',
                                       'pyname': u'gfunction_g_value_54',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 55',
                                      {'name': u'G-Function Ln(T/Ts) Value 55',
                                       'pyname': u'gfunction_lnt_or_ts_value_55',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 55',
                                      {'name': u'G-Function G Value 55',
                                       'pyname': u'gfunction_g_value_55',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 56',
                                      {'name': u'G-Function Ln(T/Ts) Value 56',
                                       'pyname': u'gfunction_lnt_or_ts_value_56',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 56',
                                      {'name': u'G-Function G Value 56',
                                       'pyname': u'gfunction_g_value_56',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 57',
                                      {'name': u'G-Function Ln(T/Ts) Value 57',
                                       'pyname': u'gfunction_lnt_or_ts_value_57',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 57',
                                      {'name': u'G-Function G Value 57',
                                       'pyname': u'gfunction_g_value_57',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 58',
                                      {'name': u'G-Function Ln(T/Ts) Value 58',
                                       'pyname': u'gfunction_lnt_or_ts_value_58',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 58',
                                      {'name': u'G-Function G Value 58',
                                       'pyname': u'gfunction_g_value_58',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 59',
                                      {'name': u'G-Function Ln(T/Ts) Value 59',
                                       'pyname': u'gfunction_lnt_or_ts_value_59',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 59',
                                      {'name': u'G-Function G Value 59',
                                       'pyname': u'gfunction_g_value_59',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 60',
                                      {'name': u'G-Function Ln(T/Ts) Value 60',
                                       'pyname': u'gfunction_lnt_or_ts_value_60',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 60',
                                      {'name': u'G-Function G Value 60',
                                       'pyname': u'gfunction_g_value_60',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 61',
                                      {'name': u'G-Function Ln(T/Ts) Value 61',
                                       'pyname': u'gfunction_lnt_or_ts_value_61',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 61',
                                      {'name': u'G-Function G Value 61',
                                       'pyname': u'gfunction_g_value_61',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 62',
                                      {'name': u'G-Function Ln(T/Ts) Value 62',
                                       'pyname': u'gfunction_lnt_or_ts_value_62',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 62',
                                      {'name': u'G-Function G Value 62',
                                       'pyname': u'gfunction_g_value_62',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 63',
                                      {'name': u'G-Function Ln(T/Ts) Value 63',
                                       'pyname': u'gfunction_lnt_or_ts_value_63',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 63',
                                      {'name': u'G-Function G Value 63',
                                       'pyname': u'gfunction_g_value_63',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 64',
                                      {'name': u'G-Function Ln(T/Ts) Value 64',
                                       'pyname': u'gfunction_lnt_or_ts_value_64',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 64',
                                      {'name': u'G-Function G Value 64',
                                       'pyname': u'gfunction_g_value_64',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 65',
                                      {'name': u'G-Function Ln(T/Ts) Value 65',
                                       'pyname': u'gfunction_lnt_or_ts_value_65',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 65',
                                      {'name': u'G-Function G Value 65',
                                       'pyname': u'gfunction_g_value_65',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 66',
                                      {'name': u'G-Function Ln(T/Ts) Value 66',
                                       'pyname': u'gfunction_lnt_or_ts_value_66',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 66',
                                      {'name': u'G-Function G Value 66',
                                       'pyname': u'gfunction_g_value_66',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 67',
                                      {'name': u'G-Function Ln(T/Ts) Value 67',
                                       'pyname': u'gfunction_lnt_or_ts_value_67',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 67',
                                      {'name': u'G-Function G Value 67',
                                       'pyname': u'gfunction_g_value_67',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 68',
                                      {'name': u'G-Function Ln(T/Ts) Value 68',
                                       'pyname': u'gfunction_lnt_or_ts_value_68',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 68',
                                      {'name': u'G-Function G Value 68',
                                       'pyname': u'gfunction_g_value_68',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 69',
                                      {'name': u'G-Function Ln(T/Ts) Value 69',
                                       'pyname': u'gfunction_lnt_or_ts_value_69',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 69',
                                      {'name': u'G-Function G Value 69',
                                       'pyname': u'gfunction_g_value_69',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 70',
                                      {'name': u'G-Function Ln(T/Ts) Value 70',
                                       'pyname': u'gfunction_lnt_or_ts_value_70',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 70',
                                      {'name': u'G-Function G Value 70',
                                       'pyname': u'gfunction_g_value_70',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 71',
                                      {'name': u'G-Function Ln(T/Ts) Value 71',
                                       'pyname': u'gfunction_lnt_or_ts_value_71',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 71',
                                      {'name': u'G-Function G Value 71',
                                       'pyname': u'gfunction_g_value_71',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 72',
                                      {'name': u'G-Function Ln(T/Ts) Value 72',
                                       'pyname': u'gfunction_lnt_or_ts_value_72',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 72',
                                      {'name': u'G-Function G Value 72',
                                       'pyname': u'gfunction_g_value_72',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 73',
                                      {'name': u'G-Function Ln(T/Ts) Value 73',
                                       'pyname': u'gfunction_lnt_or_ts_value_73',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 73',
                                      {'name': u'G-Function G Value 73',
                                       'pyname': u'gfunction_g_value_73',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 74',
                                      {'name': u'G-Function Ln(T/Ts) Value 74',
                                       'pyname': u'gfunction_lnt_or_ts_value_74',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 74',
                                      {'name': u'G-Function G Value 74',
                                       'pyname': u'gfunction_g_value_74',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 75',
                                      {'name': u'G-Function Ln(T/Ts) Value 75',
                                       'pyname': u'gfunction_lnt_or_ts_value_75',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 75',
                                      {'name': u'G-Function G Value 75',
                                       'pyname': u'gfunction_g_value_75',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 76',
                                      {'name': u'G-Function Ln(T/Ts) Value 76',
                                       'pyname': u'gfunction_lnt_or_ts_value_76',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 76',
                                      {'name': u'G-Function G Value 76',
                                       'pyname': u'gfunction_g_value_76',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 77',
                                      {'name': u'G-Function Ln(T/Ts) Value 77',
                                       'pyname': u'gfunction_lnt_or_ts_value_77',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 77',
                                      {'name': u'G-Function G Value 77',
                                       'pyname': u'gfunction_g_value_77',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 78',
                                      {'name': u'G-Function Ln(T/Ts) Value 78',
                                       'pyname': u'gfunction_lnt_or_ts_value_78',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 78',
                                      {'name': u'G-Function G Value 78',
                                       'pyname': u'gfunction_g_value_78',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 79',
                                      {'name': u'G-Function Ln(T/Ts) Value 79',
                                       'pyname': u'gfunction_lnt_or_ts_value_79',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 79',
                                      {'name': u'G-Function G Value 79',
                                       'pyname': u'gfunction_g_value_79',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 80',
                                      {'name': u'G-Function Ln(T/Ts) Value 80',
                                       'pyname': u'gfunction_lnt_or_ts_value_80',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 80',
                                      {'name': u'G-Function G Value 80',
                                       'pyname': u'gfunction_g_value_80',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 81',
                                      {'name': u'G-Function Ln(T/Ts) Value 81',
                                       'pyname': u'gfunction_lnt_or_ts_value_81',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 81',
                                      {'name': u'G-Function G Value 81',
                                       'pyname': u'gfunction_g_value_81',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 82',
                                      {'name': u'G-Function Ln(T/Ts) Value 82',
                                       'pyname': u'gfunction_lnt_or_ts_value_82',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 82',
                                      {'name': u'G-Function G Value 82',
                                       'pyname': u'gfunction_g_value_82',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 83',
                                      {'name': u'G-Function Ln(T/Ts) Value 83',
                                       'pyname': u'gfunction_lnt_or_ts_value_83',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 83',
                                      {'name': u'G-Function G Value 83',
                                       'pyname': u'gfunction_g_value_83',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 84',
                                      {'name': u'G-Function Ln(T/Ts) Value 84',
                                       'pyname': u'gfunction_lnt_or_ts_value_84',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 84',
                                      {'name': u'G-Function G Value 84',
                                       'pyname': u'gfunction_g_value_84',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 85',
                                      {'name': u'G-Function Ln(T/Ts) Value 85',
                                       'pyname': u'gfunction_lnt_or_ts_value_85',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 85',
                                      {'name': u'G-Function G Value 85',
                                       'pyname': u'gfunction_g_value_85',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 86',
                                      {'name': u'G-Function Ln(T/Ts) Value 86',
                                       'pyname': u'gfunction_lnt_or_ts_value_86',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 86',
                                      {'name': u'G-Function G Value 86',
                                       'pyname': u'gfunction_g_value_86',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 87',
                                      {'name': u'G-Function Ln(T/Ts) Value 87',
                                       'pyname': u'gfunction_lnt_or_ts_value_87',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 87',
                                      {'name': u'G-Function G Value 87',
                                       'pyname': u'gfunction_g_value_87',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 88',
                                      {'name': u'G-Function Ln(T/Ts) Value 88',
                                       'pyname': u'gfunction_lnt_or_ts_value_88',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 88',
                                      {'name': u'G-Function G Value 88',
                                       'pyname': u'gfunction_g_value_88',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 89',
                                      {'name': u'G-Function Ln(T/Ts) Value 89',
                                       'pyname': u'gfunction_lnt_or_ts_value_89',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 89',
                                      {'name': u'G-Function G Value 89',
                                       'pyname': u'gfunction_g_value_89',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 90',
                                      {'name': u'G-Function Ln(T/Ts) Value 90',
                                       'pyname': u'gfunction_lnt_or_ts_value_90',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 90',
                                      {'name': u'G-Function G Value 90',
                                       'pyname': u'gfunction_g_value_90',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 91',
                                      {'name': u'G-Function Ln(T/Ts) Value 91',
                                       'pyname': u'gfunction_lnt_or_ts_value_91',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 91',
                                      {'name': u'G-Function G Value 91',
                                       'pyname': u'gfunction_g_value_91',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 92',
                                      {'name': u'G-Function Ln(T/Ts) Value 92',
                                       'pyname': u'gfunction_lnt_or_ts_value_92',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 92',
                                      {'name': u'G-Function G Value 92',
                                       'pyname': u'gfunction_g_value_92',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 93',
                                      {'name': u'G-Function Ln(T/Ts) Value 93',
                                       'pyname': u'gfunction_lnt_or_ts_value_93',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 93',
                                      {'name': u'G-Function G Value 93',
                                       'pyname': u'gfunction_g_value_93',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 94',
                                      {'name': u'G-Function Ln(T/Ts) Value 94',
                                       'pyname': u'gfunction_lnt_or_ts_value_94',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 94',
                                      {'name': u'G-Function G Value 94',
                                       'pyname': u'gfunction_g_value_94',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 95',
                                      {'name': u'G-Function Ln(T/Ts) Value 95',
                                       'pyname': u'gfunction_lnt_or_ts_value_95',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 95',
                                      {'name': u'G-Function G Value 95',
                                       'pyname': u'gfunction_g_value_95',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 96',
                                      {'name': u'G-Function Ln(T/Ts) Value 96',
                                       'pyname': u'gfunction_lnt_or_ts_value_96',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 96',
                                      {'name': u'G-Function G Value 96',
                                       'pyname': u'gfunction_g_value_96',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 97',
                                      {'name': u'G-Function Ln(T/Ts) Value 97',
                                       'pyname': u'gfunction_lnt_or_ts_value_97',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 97',
                                      {'name': u'G-Function G Value 97',
                                       'pyname': u'gfunction_g_value_97',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 98',
                                      {'name': u'G-Function Ln(T/Ts) Value 98',
                                       'pyname': u'gfunction_lnt_or_ts_value_98',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 98',
                                      {'name': u'G-Function G Value 98',
                                       'pyname': u'gfunction_g_value_98',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 99',
                                      {'name': u'G-Function Ln(T/Ts) Value 99',
                                       'pyname': u'gfunction_lnt_or_ts_value_99',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 99',
                                      {'name': u'G-Function G Value 99',
                                       'pyname': u'gfunction_g_value_99',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function ln(t/ts) value 100',
                                      {'name': u'G-Function Ln(T/Ts) Value 100',
                                       'pyname': u'gfunction_lnt_or_ts_value_100',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'g-function g value 100',
                                      {'name': u'G-Function G Value 100',
                                       'pyname': u'gfunction_g_value_100',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'})]),
              'format': None,
              'group': u'Condenser Equipment and Heat Exchangers',
              'min-fields': 21,
              'name': u'GroundHeatExchanger:Vertical',
              'pyname': u'GroundHeatExchangerVertical',
              'required-object': False,
              'unique-object': False}

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
    def inlet_node_name(self):
        """Get inlet_node_name.

        Returns:
            str: the value of `inlet_node_name` or None if not set

        """
        return self["Inlet Node Name"]

    @inlet_node_name.setter
    def inlet_node_name(self, value=None):
        """Corresponds to IDD field `Inlet Node Name`

        Args:
            value (str): value for IDD Field `Inlet Node Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Inlet Node Name"] = value

    @property
    def outlet_node_name(self):
        """Get outlet_node_name.

        Returns:
            str: the value of `outlet_node_name` or None if not set

        """
        return self["Outlet Node Name"]

    @outlet_node_name.setter
    def outlet_node_name(self, value=None):
        """Corresponds to IDD field `Outlet Node Name`

        Args:
            value (str): value for IDD Field `Outlet Node Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Outlet Node Name"] = value

    @property
    def maximum_flow_rate(self):
        """Get maximum_flow_rate.

        Returns:
            float: the value of `maximum_flow_rate` or None if not set

        """
        return self["Maximum Flow Rate"]

    @maximum_flow_rate.setter
    def maximum_flow_rate(self, value=None):
        """Corresponds to IDD field `Maximum Flow Rate`

        Args:
            value (float): value for IDD Field `Maximum Flow Rate`
                Units: m3/s
                IP-Units: gal/min
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Maximum Flow Rate"] = value

    @property
    def number_of_bore_holes(self):
        """Get number_of_bore_holes.

        Returns:
            float: the value of `number_of_bore_holes` or None if not set

        """
        return self["Number of Bore Holes"]

    @number_of_bore_holes.setter
    def number_of_bore_holes(self, value=None):
        """Corresponds to IDD field `Number of Bore Holes`

        Args:
            value (float): value for IDD Field `Number of Bore Holes`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Number of Bore Holes"] = value

    @property
    def bore_hole_length(self):
        """Get bore_hole_length.

        Returns:
            float: the value of `bore_hole_length` or None if not set

        """
        return self["Bore Hole Length"]

    @bore_hole_length.setter
    def bore_hole_length(self, value=None):
        """Corresponds to IDD field `Bore Hole Length`

        Args:
            value (float): value for IDD Field `Bore Hole Length`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Bore Hole Length"] = value

    @property
    def bore_hole_radius(self):
        """Get bore_hole_radius.

        Returns:
            float: the value of `bore_hole_radius` or None if not set

        """
        return self["Bore Hole Radius"]

    @bore_hole_radius.setter
    def bore_hole_radius(self, value=None):
        """Corresponds to IDD field `Bore Hole Radius`

        Args:
            value (float): value for IDD Field `Bore Hole Radius`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Bore Hole Radius"] = value

    @property
    def ground_thermal_conductivity(self):
        """Get ground_thermal_conductivity.

        Returns:
            float: the value of `ground_thermal_conductivity` or None if not set

        """
        return self["Ground Thermal Conductivity"]

    @ground_thermal_conductivity.setter
    def ground_thermal_conductivity(self, value=None):
        """Corresponds to IDD field `Ground Thermal Conductivity`

        Args:
            value (float): value for IDD Field `Ground Thermal Conductivity`
                Units: W/m-K
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Ground Thermal Conductivity"] = value

    @property
    def ground_thermal_heat_capacity(self):
        """Get ground_thermal_heat_capacity.

        Returns:
            float: the value of `ground_thermal_heat_capacity` or None if not set

        """
        return self["Ground Thermal Heat Capacity"]

    @ground_thermal_heat_capacity.setter
    def ground_thermal_heat_capacity(self, value=None):
        """Corresponds to IDD field `Ground Thermal Heat Capacity`

        Args:
            value (float): value for IDD Field `Ground Thermal Heat Capacity`
                Units: J/m3-K
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Ground Thermal Heat Capacity"] = value

    @property
    def ground_temperature(self):
        """Get ground_temperature.

        Returns:
            float: the value of `ground_temperature` or None if not set

        """
        return self["Ground Temperature"]

    @ground_temperature.setter
    def ground_temperature(self, value=None):
        """Corresponds to IDD field `Ground Temperature`

        Args:
            value (float): value for IDD Field `Ground Temperature`
                Units: C
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Ground Temperature"] = value

    @property
    def design_flow_rate(self):
        """Get design_flow_rate.

        Returns:
            float: the value of `design_flow_rate` or None if not set

        """
        return self["Design Flow Rate"]

    @design_flow_rate.setter
    def design_flow_rate(self, value=None):
        """Corresponds to IDD field `Design Flow Rate`

        Args:
            value (float): value for IDD Field `Design Flow Rate`
                Units: m3/s
                IP-Units: gal/min
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Design Flow Rate"] = value

    @property
    def grout_thermal_conductivity(self):
        """Get grout_thermal_conductivity.

        Returns:
            float: the value of `grout_thermal_conductivity` or None if not set

        """
        return self["Grout Thermal Conductivity"]

    @grout_thermal_conductivity.setter
    def grout_thermal_conductivity(self, value=None):
        """Corresponds to IDD field `Grout Thermal Conductivity`

        Args:
            value (float): value for IDD Field `Grout Thermal Conductivity`
                Units: W/m-K
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Grout Thermal Conductivity"] = value

    @property
    def pipe_thermal_conductivity(self):
        """Get pipe_thermal_conductivity.

        Returns:
            float: the value of `pipe_thermal_conductivity` or None if not set

        """
        return self["Pipe Thermal Conductivity"]

    @pipe_thermal_conductivity.setter
    def pipe_thermal_conductivity(self, value=None):
        """Corresponds to IDD field `Pipe Thermal Conductivity`

        Args:
            value (float): value for IDD Field `Pipe Thermal Conductivity`
                Units: W/m-K
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Pipe Thermal Conductivity"] = value

    @property
    def pipe_out_diameter(self):
        """Get pipe_out_diameter.

        Returns:
            float: the value of `pipe_out_diameter` or None if not set

        """
        return self["Pipe Out Diameter"]

    @pipe_out_diameter.setter
    def pipe_out_diameter(self, value=None):
        """Corresponds to IDD field `Pipe Out Diameter`

        Args:
            value (float): value for IDD Field `Pipe Out Diameter`
                Units: m
                IP-Units: in
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Pipe Out Diameter"] = value

    @property
    def utube_distance(self):
        """Get utube_distance.

        Returns:
            float: the value of `utube_distance` or None if not set

        """
        return self["U-Tube Distance"]

    @utube_distance.setter
    def utube_distance(self, value=None):
        """  Corresponds to IDD field `U-Tube Distance`

        Args:
            value (float): value for IDD Field `U-Tube Distance`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["U-Tube Distance"] = value

    @property
    def pipe_thickness(self):
        """Get pipe_thickness.

        Returns:
            float: the value of `pipe_thickness` or None if not set

        """
        return self["Pipe Thickness"]

    @pipe_thickness.setter
    def pipe_thickness(self, value=None):
        """Corresponds to IDD field `Pipe Thickness`

        Args:
            value (float): value for IDD Field `Pipe Thickness`
                Units: m
                IP-Units: in
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Pipe Thickness"] = value

    @property
    def maximum_length_of_simulation(self):
        """Get maximum_length_of_simulation.

        Returns:
            float: the value of `maximum_length_of_simulation` or None if not set

        """
        return self["Maximum Length of Simulation"]

    @maximum_length_of_simulation.setter
    def maximum_length_of_simulation(self, value=None):
        """Corresponds to IDD field `Maximum Length of Simulation`

        Args:
            value (float): value for IDD Field `Maximum Length of Simulation`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Maximum Length of Simulation"] = value

    @property
    def gfunction_reference_ratio(self):
        """Get gfunction_reference_ratio.

        Returns:
            float: the value of `gfunction_reference_ratio` or None if not set

        """
        return self["G-Function Reference Ratio"]

    @gfunction_reference_ratio.setter
    def gfunction_reference_ratio(self, value=0.0005):
        """  Corresponds to IDD field `G-Function Reference Ratio`

        Args:
            value (float): value for IDD Field `G-Function Reference Ratio`
                Units: dimensionless
                Default value: 0.0005
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Reference Ratio"] = value

    @property
    def number_of_data_pairs_of_the_g_function(self):
        """Get number_of_data_pairs_of_the_g_function.

        Returns:
            float: the value of `number_of_data_pairs_of_the_g_function` or None if not set

        """
        return self["Number of Data Pairs of the G Function"]

    @number_of_data_pairs_of_the_g_function.setter
    def number_of_data_pairs_of_the_g_function(self, value=None):
        """Corresponds to IDD field `Number of Data Pairs of the G Function`

        Args:
            value (float): value for IDD Field `Number of Data Pairs of the G Function`
                value <= 100.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Number of Data Pairs of the G Function"] = value

    @property
    def gfunction_lnt_or_ts_value_1(self):
        """Get gfunction_lnt_or_ts_value_1.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_1` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 1"]

    @gfunction_lnt_or_ts_value_1.setter
    def gfunction_lnt_or_ts_value_1(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 1`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 1`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 1"] = value

    @property
    def gfunction_g_value_1(self):
        """Get gfunction_g_value_1.

        Returns:
            float: the value of `gfunction_g_value_1` or None if not set

        """
        return self["G-Function G Value 1"]

    @gfunction_g_value_1.setter
    def gfunction_g_value_1(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 1`

        Args:
            value (float): value for IDD Field `G-Function G Value 1`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 1"] = value

    @property
    def gfunction_lnt_or_ts_value_2(self):
        """Get gfunction_lnt_or_ts_value_2.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_2` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 2"]

    @gfunction_lnt_or_ts_value_2.setter
    def gfunction_lnt_or_ts_value_2(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 2`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 2`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 2"] = value

    @property
    def gfunction_g_value_2(self):
        """Get gfunction_g_value_2.

        Returns:
            float: the value of `gfunction_g_value_2` or None if not set

        """
        return self["G-Function G Value 2"]

    @gfunction_g_value_2.setter
    def gfunction_g_value_2(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 2`

        Args:
            value (float): value for IDD Field `G-Function G Value 2`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 2"] = value

    @property
    def gfunction_lnt_or_ts_value_3(self):
        """Get gfunction_lnt_or_ts_value_3.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_3` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 3"]

    @gfunction_lnt_or_ts_value_3.setter
    def gfunction_lnt_or_ts_value_3(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 3`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 3`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 3"] = value

    @property
    def gfunction_g_value_3(self):
        """Get gfunction_g_value_3.

        Returns:
            float: the value of `gfunction_g_value_3` or None if not set

        """
        return self["G-Function G Value 3"]

    @gfunction_g_value_3.setter
    def gfunction_g_value_3(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 3`

        Args:
            value (float): value for IDD Field `G-Function G Value 3`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 3"] = value

    @property
    def gfunction_lnt_or_ts_value_4(self):
        """Get gfunction_lnt_or_ts_value_4.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_4` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 4"]

    @gfunction_lnt_or_ts_value_4.setter
    def gfunction_lnt_or_ts_value_4(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 4`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 4`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 4"] = value

    @property
    def gfunction_g_value_4(self):
        """Get gfunction_g_value_4.

        Returns:
            float: the value of `gfunction_g_value_4` or None if not set

        """
        return self["G-Function G Value 4"]

    @gfunction_g_value_4.setter
    def gfunction_g_value_4(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 4`

        Args:
            value (float): value for IDD Field `G-Function G Value 4`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 4"] = value

    @property
    def gfunction_lnt_or_ts_value_5(self):
        """Get gfunction_lnt_or_ts_value_5.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_5` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 5"]

    @gfunction_lnt_or_ts_value_5.setter
    def gfunction_lnt_or_ts_value_5(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 5`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 5`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 5"] = value

    @property
    def gfunction_g_value_5(self):
        """Get gfunction_g_value_5.

        Returns:
            float: the value of `gfunction_g_value_5` or None if not set

        """
        return self["G-Function G Value 5"]

    @gfunction_g_value_5.setter
    def gfunction_g_value_5(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 5`

        Args:
            value (float): value for IDD Field `G-Function G Value 5`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 5"] = value

    @property
    def gfunction_lnt_or_ts_value_6(self):
        """Get gfunction_lnt_or_ts_value_6.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_6` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 6"]

    @gfunction_lnt_or_ts_value_6.setter
    def gfunction_lnt_or_ts_value_6(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 6`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 6`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 6"] = value

    @property
    def gfunction_g_value_6(self):
        """Get gfunction_g_value_6.

        Returns:
            float: the value of `gfunction_g_value_6` or None if not set

        """
        return self["G-Function G Value 6"]

    @gfunction_g_value_6.setter
    def gfunction_g_value_6(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 6`

        Args:
            value (float): value for IDD Field `G-Function G Value 6`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 6"] = value

    @property
    def gfunction_lnt_or_ts_value_7(self):
        """Get gfunction_lnt_or_ts_value_7.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_7` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 7"]

    @gfunction_lnt_or_ts_value_7.setter
    def gfunction_lnt_or_ts_value_7(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 7`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 7`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 7"] = value

    @property
    def gfunction_g_value_7(self):
        """Get gfunction_g_value_7.

        Returns:
            float: the value of `gfunction_g_value_7` or None if not set

        """
        return self["G-Function G Value 7"]

    @gfunction_g_value_7.setter
    def gfunction_g_value_7(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 7`

        Args:
            value (float): value for IDD Field `G-Function G Value 7`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 7"] = value

    @property
    def gfunction_lnt_or_ts_value_8(self):
        """Get gfunction_lnt_or_ts_value_8.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_8` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 8"]

    @gfunction_lnt_or_ts_value_8.setter
    def gfunction_lnt_or_ts_value_8(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 8`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 8`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 8"] = value

    @property
    def gfunction_g_value_8(self):
        """Get gfunction_g_value_8.

        Returns:
            float: the value of `gfunction_g_value_8` or None if not set

        """
        return self["G-Function G Value 8"]

    @gfunction_g_value_8.setter
    def gfunction_g_value_8(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 8`

        Args:
            value (float): value for IDD Field `G-Function G Value 8`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 8"] = value

    @property
    def gfunction_lnt_or_ts_value_9(self):
        """Get gfunction_lnt_or_ts_value_9.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_9` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 9"]

    @gfunction_lnt_or_ts_value_9.setter
    def gfunction_lnt_or_ts_value_9(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 9`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 9`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 9"] = value

    @property
    def gfunction_g_value_9(self):
        """Get gfunction_g_value_9.

        Returns:
            float: the value of `gfunction_g_value_9` or None if not set

        """
        return self["G-Function G Value 9"]

    @gfunction_g_value_9.setter
    def gfunction_g_value_9(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 9`

        Args:
            value (float): value for IDD Field `G-Function G Value 9`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 9"] = value

    @property
    def gfunction_lnt_or_ts_value_10(self):
        """Get gfunction_lnt_or_ts_value_10.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_10` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 10"]

    @gfunction_lnt_or_ts_value_10.setter
    def gfunction_lnt_or_ts_value_10(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 10`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 10`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 10"] = value

    @property
    def gfunction_g_value_10(self):
        """Get gfunction_g_value_10.

        Returns:
            float: the value of `gfunction_g_value_10` or None if not set

        """
        return self["G-Function G Value 10"]

    @gfunction_g_value_10.setter
    def gfunction_g_value_10(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 10`

        Args:
            value (float): value for IDD Field `G-Function G Value 10`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 10"] = value

    @property
    def gfunction_lnt_or_ts_value_11(self):
        """Get gfunction_lnt_or_ts_value_11.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_11` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 11"]

    @gfunction_lnt_or_ts_value_11.setter
    def gfunction_lnt_or_ts_value_11(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 11`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 11`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 11"] = value

    @property
    def gfunction_g_value_11(self):
        """Get gfunction_g_value_11.

        Returns:
            float: the value of `gfunction_g_value_11` or None if not set

        """
        return self["G-Function G Value 11"]

    @gfunction_g_value_11.setter
    def gfunction_g_value_11(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 11`

        Args:
            value (float): value for IDD Field `G-Function G Value 11`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 11"] = value

    @property
    def gfunction_lnt_or_ts_value_12(self):
        """Get gfunction_lnt_or_ts_value_12.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_12` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 12"]

    @gfunction_lnt_or_ts_value_12.setter
    def gfunction_lnt_or_ts_value_12(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 12`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 12`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 12"] = value

    @property
    def gfunction_g_value_12(self):
        """Get gfunction_g_value_12.

        Returns:
            float: the value of `gfunction_g_value_12` or None if not set

        """
        return self["G-Function G Value 12"]

    @gfunction_g_value_12.setter
    def gfunction_g_value_12(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 12`

        Args:
            value (float): value for IDD Field `G-Function G Value 12`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 12"] = value

    @property
    def gfunction_lnt_or_ts_value_13(self):
        """Get gfunction_lnt_or_ts_value_13.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_13` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 13"]

    @gfunction_lnt_or_ts_value_13.setter
    def gfunction_lnt_or_ts_value_13(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 13`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 13`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 13"] = value

    @property
    def gfunction_g_value_13(self):
        """Get gfunction_g_value_13.

        Returns:
            float: the value of `gfunction_g_value_13` or None if not set

        """
        return self["G-Function G Value 13"]

    @gfunction_g_value_13.setter
    def gfunction_g_value_13(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 13`

        Args:
            value (float): value for IDD Field `G-Function G Value 13`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 13"] = value

    @property
    def gfunction_lnt_or_ts_value_14(self):
        """Get gfunction_lnt_or_ts_value_14.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_14` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 14"]

    @gfunction_lnt_or_ts_value_14.setter
    def gfunction_lnt_or_ts_value_14(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 14`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 14`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 14"] = value

    @property
    def gfunction_g_value_14(self):
        """Get gfunction_g_value_14.

        Returns:
            float: the value of `gfunction_g_value_14` or None if not set

        """
        return self["G-Function G Value 14"]

    @gfunction_g_value_14.setter
    def gfunction_g_value_14(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 14`

        Args:
            value (float): value for IDD Field `G-Function G Value 14`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 14"] = value

    @property
    def gfunction_lnt_or_ts_value_15(self):
        """Get gfunction_lnt_or_ts_value_15.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_15` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 15"]

    @gfunction_lnt_or_ts_value_15.setter
    def gfunction_lnt_or_ts_value_15(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 15`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 15`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 15"] = value

    @property
    def gfunction_g_value_15(self):
        """Get gfunction_g_value_15.

        Returns:
            float: the value of `gfunction_g_value_15` or None if not set

        """
        return self["G-Function G Value 15"]

    @gfunction_g_value_15.setter
    def gfunction_g_value_15(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 15`

        Args:
            value (float): value for IDD Field `G-Function G Value 15`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 15"] = value

    @property
    def gfunction_lnt_or_ts_value_16(self):
        """Get gfunction_lnt_or_ts_value_16.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_16` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 16"]

    @gfunction_lnt_or_ts_value_16.setter
    def gfunction_lnt_or_ts_value_16(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 16`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 16`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 16"] = value

    @property
    def gfunction_g_value_16(self):
        """Get gfunction_g_value_16.

        Returns:
            float: the value of `gfunction_g_value_16` or None if not set

        """
        return self["G-Function G Value 16"]

    @gfunction_g_value_16.setter
    def gfunction_g_value_16(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 16`

        Args:
            value (float): value for IDD Field `G-Function G Value 16`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 16"] = value

    @property
    def gfunction_lnt_or_ts_value_17(self):
        """Get gfunction_lnt_or_ts_value_17.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_17` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 17"]

    @gfunction_lnt_or_ts_value_17.setter
    def gfunction_lnt_or_ts_value_17(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 17`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 17`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 17"] = value

    @property
    def gfunction_g_value_17(self):
        """Get gfunction_g_value_17.

        Returns:
            float: the value of `gfunction_g_value_17` or None if not set

        """
        return self["G-Function G Value 17"]

    @gfunction_g_value_17.setter
    def gfunction_g_value_17(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 17`

        Args:
            value (float): value for IDD Field `G-Function G Value 17`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 17"] = value

    @property
    def gfunction_lnt_or_ts_value_18(self):
        """Get gfunction_lnt_or_ts_value_18.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_18` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 18"]

    @gfunction_lnt_or_ts_value_18.setter
    def gfunction_lnt_or_ts_value_18(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 18`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 18`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 18"] = value

    @property
    def gfunction_g_value_18(self):
        """Get gfunction_g_value_18.

        Returns:
            float: the value of `gfunction_g_value_18` or None if not set

        """
        return self["G-Function G Value 18"]

    @gfunction_g_value_18.setter
    def gfunction_g_value_18(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 18`

        Args:
            value (float): value for IDD Field `G-Function G Value 18`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 18"] = value

    @property
    def gfunction_lnt_or_ts_value_19(self):
        """Get gfunction_lnt_or_ts_value_19.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_19` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 19"]

    @gfunction_lnt_or_ts_value_19.setter
    def gfunction_lnt_or_ts_value_19(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 19`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 19`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 19"] = value

    @property
    def gfunction_g_value_19(self):
        """Get gfunction_g_value_19.

        Returns:
            float: the value of `gfunction_g_value_19` or None if not set

        """
        return self["G-Function G Value 19"]

    @gfunction_g_value_19.setter
    def gfunction_g_value_19(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 19`

        Args:
            value (float): value for IDD Field `G-Function G Value 19`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 19"] = value

    @property
    def gfunction_lnt_or_ts_value_20(self):
        """Get gfunction_lnt_or_ts_value_20.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_20` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 20"]

    @gfunction_lnt_or_ts_value_20.setter
    def gfunction_lnt_or_ts_value_20(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 20`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 20`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 20"] = value

    @property
    def gfunction_g_value_20(self):
        """Get gfunction_g_value_20.

        Returns:
            float: the value of `gfunction_g_value_20` or None if not set

        """
        return self["G-Function G Value 20"]

    @gfunction_g_value_20.setter
    def gfunction_g_value_20(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 20`

        Args:
            value (float): value for IDD Field `G-Function G Value 20`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 20"] = value

    @property
    def gfunction_lnt_or_ts_value_21(self):
        """Get gfunction_lnt_or_ts_value_21.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_21` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 21"]

    @gfunction_lnt_or_ts_value_21.setter
    def gfunction_lnt_or_ts_value_21(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 21`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 21`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 21"] = value

    @property
    def gfunction_g_value_21(self):
        """Get gfunction_g_value_21.

        Returns:
            float: the value of `gfunction_g_value_21` or None if not set

        """
        return self["G-Function G Value 21"]

    @gfunction_g_value_21.setter
    def gfunction_g_value_21(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 21`

        Args:
            value (float): value for IDD Field `G-Function G Value 21`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 21"] = value

    @property
    def gfunction_lnt_or_ts_value_22(self):
        """Get gfunction_lnt_or_ts_value_22.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_22` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 22"]

    @gfunction_lnt_or_ts_value_22.setter
    def gfunction_lnt_or_ts_value_22(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 22`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 22`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 22"] = value

    @property
    def gfunction_g_value_22(self):
        """Get gfunction_g_value_22.

        Returns:
            float: the value of `gfunction_g_value_22` or None if not set

        """
        return self["G-Function G Value 22"]

    @gfunction_g_value_22.setter
    def gfunction_g_value_22(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 22`

        Args:
            value (float): value for IDD Field `G-Function G Value 22`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 22"] = value

    @property
    def gfunction_lnt_or_ts_value_23(self):
        """Get gfunction_lnt_or_ts_value_23.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_23` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 23"]

    @gfunction_lnt_or_ts_value_23.setter
    def gfunction_lnt_or_ts_value_23(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 23`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 23`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 23"] = value

    @property
    def gfunction_g_value_23(self):
        """Get gfunction_g_value_23.

        Returns:
            float: the value of `gfunction_g_value_23` or None if not set

        """
        return self["G-Function G Value 23"]

    @gfunction_g_value_23.setter
    def gfunction_g_value_23(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 23`

        Args:
            value (float): value for IDD Field `G-Function G Value 23`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 23"] = value

    @property
    def gfunction_lnt_or_ts_value_24(self):
        """Get gfunction_lnt_or_ts_value_24.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_24` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 24"]

    @gfunction_lnt_or_ts_value_24.setter
    def gfunction_lnt_or_ts_value_24(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 24`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 24`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 24"] = value

    @property
    def gfunction_g_value_24(self):
        """Get gfunction_g_value_24.

        Returns:
            float: the value of `gfunction_g_value_24` or None if not set

        """
        return self["G-Function G Value 24"]

    @gfunction_g_value_24.setter
    def gfunction_g_value_24(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 24`

        Args:
            value (float): value for IDD Field `G-Function G Value 24`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 24"] = value

    @property
    def gfunction_lnt_or_ts_value_25(self):
        """Get gfunction_lnt_or_ts_value_25.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_25` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 25"]

    @gfunction_lnt_or_ts_value_25.setter
    def gfunction_lnt_or_ts_value_25(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 25`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 25`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 25"] = value

    @property
    def gfunction_g_value_25(self):
        """Get gfunction_g_value_25.

        Returns:
            float: the value of `gfunction_g_value_25` or None if not set

        """
        return self["G-Function G Value 25"]

    @gfunction_g_value_25.setter
    def gfunction_g_value_25(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 25`

        Args:
            value (float): value for IDD Field `G-Function G Value 25`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 25"] = value

    @property
    def gfunction_lnt_or_ts_value_26(self):
        """Get gfunction_lnt_or_ts_value_26.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_26` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 26"]

    @gfunction_lnt_or_ts_value_26.setter
    def gfunction_lnt_or_ts_value_26(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 26`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 26`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 26"] = value

    @property
    def gfunction_g_value_26(self):
        """Get gfunction_g_value_26.

        Returns:
            float: the value of `gfunction_g_value_26` or None if not set

        """
        return self["G-Function G Value 26"]

    @gfunction_g_value_26.setter
    def gfunction_g_value_26(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 26`

        Args:
            value (float): value for IDD Field `G-Function G Value 26`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 26"] = value

    @property
    def gfunction_lnt_or_ts_value_27(self):
        """Get gfunction_lnt_or_ts_value_27.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_27` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 27"]

    @gfunction_lnt_or_ts_value_27.setter
    def gfunction_lnt_or_ts_value_27(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 27`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 27`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 27"] = value

    @property
    def gfunction_g_value_27(self):
        """Get gfunction_g_value_27.

        Returns:
            float: the value of `gfunction_g_value_27` or None if not set

        """
        return self["G-Function G Value 27"]

    @gfunction_g_value_27.setter
    def gfunction_g_value_27(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 27`

        Args:
            value (float): value for IDD Field `G-Function G Value 27`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 27"] = value

    @property
    def gfunction_lnt_or_ts_value_28(self):
        """Get gfunction_lnt_or_ts_value_28.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_28` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 28"]

    @gfunction_lnt_or_ts_value_28.setter
    def gfunction_lnt_or_ts_value_28(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 28`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 28`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 28"] = value

    @property
    def gfunction_g_value_28(self):
        """Get gfunction_g_value_28.

        Returns:
            float: the value of `gfunction_g_value_28` or None if not set

        """
        return self["G-Function G Value 28"]

    @gfunction_g_value_28.setter
    def gfunction_g_value_28(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 28`

        Args:
            value (float): value for IDD Field `G-Function G Value 28`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 28"] = value

    @property
    def gfunction_lnt_or_ts_value_29(self):
        """Get gfunction_lnt_or_ts_value_29.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_29` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 29"]

    @gfunction_lnt_or_ts_value_29.setter
    def gfunction_lnt_or_ts_value_29(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 29`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 29`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 29"] = value

    @property
    def gfunction_g_value_29(self):
        """Get gfunction_g_value_29.

        Returns:
            float: the value of `gfunction_g_value_29` or None if not set

        """
        return self["G-Function G Value 29"]

    @gfunction_g_value_29.setter
    def gfunction_g_value_29(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 29`

        Args:
            value (float): value for IDD Field `G-Function G Value 29`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 29"] = value

    @property
    def gfunction_lnt_or_ts_value_30(self):
        """Get gfunction_lnt_or_ts_value_30.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_30` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 30"]

    @gfunction_lnt_or_ts_value_30.setter
    def gfunction_lnt_or_ts_value_30(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 30`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 30`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 30"] = value

    @property
    def gfunction_g_value_30(self):
        """Get gfunction_g_value_30.

        Returns:
            float: the value of `gfunction_g_value_30` or None if not set

        """
        return self["G-Function G Value 30"]

    @gfunction_g_value_30.setter
    def gfunction_g_value_30(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 30`

        Args:
            value (float): value for IDD Field `G-Function G Value 30`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 30"] = value

    @property
    def gfunction_lnt_or_ts_value_31(self):
        """Get gfunction_lnt_or_ts_value_31.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_31` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 31"]

    @gfunction_lnt_or_ts_value_31.setter
    def gfunction_lnt_or_ts_value_31(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 31`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 31`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 31"] = value

    @property
    def gfunction_g_value_31(self):
        """Get gfunction_g_value_31.

        Returns:
            float: the value of `gfunction_g_value_31` or None if not set

        """
        return self["G-Function G Value 31"]

    @gfunction_g_value_31.setter
    def gfunction_g_value_31(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 31`

        Args:
            value (float): value for IDD Field `G-Function G Value 31`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 31"] = value

    @property
    def gfunction_lnt_or_ts_value_32(self):
        """Get gfunction_lnt_or_ts_value_32.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_32` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 32"]

    @gfunction_lnt_or_ts_value_32.setter
    def gfunction_lnt_or_ts_value_32(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 32`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 32`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 32"] = value

    @property
    def gfunction_g_value_32(self):
        """Get gfunction_g_value_32.

        Returns:
            float: the value of `gfunction_g_value_32` or None if not set

        """
        return self["G-Function G Value 32"]

    @gfunction_g_value_32.setter
    def gfunction_g_value_32(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 32`

        Args:
            value (float): value for IDD Field `G-Function G Value 32`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 32"] = value

    @property
    def gfunction_lnt_or_ts_value_33(self):
        """Get gfunction_lnt_or_ts_value_33.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_33` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 33"]

    @gfunction_lnt_or_ts_value_33.setter
    def gfunction_lnt_or_ts_value_33(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 33`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 33`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 33"] = value

    @property
    def gfunction_g_value_33(self):
        """Get gfunction_g_value_33.

        Returns:
            float: the value of `gfunction_g_value_33` or None if not set

        """
        return self["G-Function G Value 33"]

    @gfunction_g_value_33.setter
    def gfunction_g_value_33(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 33`

        Args:
            value (float): value for IDD Field `G-Function G Value 33`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 33"] = value

    @property
    def gfunction_lnt_or_ts_value_34(self):
        """Get gfunction_lnt_or_ts_value_34.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_34` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 34"]

    @gfunction_lnt_or_ts_value_34.setter
    def gfunction_lnt_or_ts_value_34(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 34`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 34`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 34"] = value

    @property
    def gfunction_g_value_34(self):
        """Get gfunction_g_value_34.

        Returns:
            float: the value of `gfunction_g_value_34` or None if not set

        """
        return self["G-Function G Value 34"]

    @gfunction_g_value_34.setter
    def gfunction_g_value_34(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 34`

        Args:
            value (float): value for IDD Field `G-Function G Value 34`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 34"] = value

    @property
    def gfunction_lnt_or_ts_value_35(self):
        """Get gfunction_lnt_or_ts_value_35.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_35` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 35"]

    @gfunction_lnt_or_ts_value_35.setter
    def gfunction_lnt_or_ts_value_35(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 35`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 35`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 35"] = value

    @property
    def gfunction_g_value_35(self):
        """Get gfunction_g_value_35.

        Returns:
            float: the value of `gfunction_g_value_35` or None if not set

        """
        return self["G-Function G Value 35"]

    @gfunction_g_value_35.setter
    def gfunction_g_value_35(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 35`

        Args:
            value (float): value for IDD Field `G-Function G Value 35`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 35"] = value

    @property
    def gfunction_lnt_or_ts_value_36(self):
        """Get gfunction_lnt_or_ts_value_36.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_36` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 36"]

    @gfunction_lnt_or_ts_value_36.setter
    def gfunction_lnt_or_ts_value_36(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 36`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 36`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 36"] = value

    @property
    def gfunction_g_value_36(self):
        """Get gfunction_g_value_36.

        Returns:
            float: the value of `gfunction_g_value_36` or None if not set

        """
        return self["G-Function G Value 36"]

    @gfunction_g_value_36.setter
    def gfunction_g_value_36(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 36`

        Args:
            value (float): value for IDD Field `G-Function G Value 36`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 36"] = value

    @property
    def gfunction_lnt_or_ts_value_37(self):
        """Get gfunction_lnt_or_ts_value_37.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_37` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 37"]

    @gfunction_lnt_or_ts_value_37.setter
    def gfunction_lnt_or_ts_value_37(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 37`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 37`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 37"] = value

    @property
    def gfunction_g_value_37(self):
        """Get gfunction_g_value_37.

        Returns:
            float: the value of `gfunction_g_value_37` or None if not set

        """
        return self["G-Function G Value 37"]

    @gfunction_g_value_37.setter
    def gfunction_g_value_37(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 37`

        Args:
            value (float): value for IDD Field `G-Function G Value 37`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 37"] = value

    @property
    def gfunction_lnt_or_ts_value_38(self):
        """Get gfunction_lnt_or_ts_value_38.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_38` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 38"]

    @gfunction_lnt_or_ts_value_38.setter
    def gfunction_lnt_or_ts_value_38(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 38`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 38`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 38"] = value

    @property
    def gfunction_g_value_38(self):
        """Get gfunction_g_value_38.

        Returns:
            float: the value of `gfunction_g_value_38` or None if not set

        """
        return self["G-Function G Value 38"]

    @gfunction_g_value_38.setter
    def gfunction_g_value_38(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 38`

        Args:
            value (float): value for IDD Field `G-Function G Value 38`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 38"] = value

    @property
    def gfunction_lnt_or_ts_value_39(self):
        """Get gfunction_lnt_or_ts_value_39.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_39` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 39"]

    @gfunction_lnt_or_ts_value_39.setter
    def gfunction_lnt_or_ts_value_39(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 39`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 39`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 39"] = value

    @property
    def gfunction_g_value_39(self):
        """Get gfunction_g_value_39.

        Returns:
            float: the value of `gfunction_g_value_39` or None if not set

        """
        return self["G-Function G Value 39"]

    @gfunction_g_value_39.setter
    def gfunction_g_value_39(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 39`

        Args:
            value (float): value for IDD Field `G-Function G Value 39`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 39"] = value

    @property
    def gfunction_lnt_or_ts_value_40(self):
        """Get gfunction_lnt_or_ts_value_40.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_40` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 40"]

    @gfunction_lnt_or_ts_value_40.setter
    def gfunction_lnt_or_ts_value_40(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 40`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 40`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 40"] = value

    @property
    def gfunction_g_value_40(self):
        """Get gfunction_g_value_40.

        Returns:
            float: the value of `gfunction_g_value_40` or None if not set

        """
        return self["G-Function G Value 40"]

    @gfunction_g_value_40.setter
    def gfunction_g_value_40(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 40`

        Args:
            value (float): value for IDD Field `G-Function G Value 40`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 40"] = value

    @property
    def gfunction_lnt_or_ts_value_41(self):
        """Get gfunction_lnt_or_ts_value_41.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_41` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 41"]

    @gfunction_lnt_or_ts_value_41.setter
    def gfunction_lnt_or_ts_value_41(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 41`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 41`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 41"] = value

    @property
    def gfunction_g_value_41(self):
        """Get gfunction_g_value_41.

        Returns:
            float: the value of `gfunction_g_value_41` or None if not set

        """
        return self["G-Function G Value 41"]

    @gfunction_g_value_41.setter
    def gfunction_g_value_41(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 41`

        Args:
            value (float): value for IDD Field `G-Function G Value 41`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 41"] = value

    @property
    def gfunction_lnt_or_ts_value_42(self):
        """Get gfunction_lnt_or_ts_value_42.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_42` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 42"]

    @gfunction_lnt_or_ts_value_42.setter
    def gfunction_lnt_or_ts_value_42(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 42`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 42`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 42"] = value

    @property
    def gfunction_g_value_42(self):
        """Get gfunction_g_value_42.

        Returns:
            float: the value of `gfunction_g_value_42` or None if not set

        """
        return self["G-Function G Value 42"]

    @gfunction_g_value_42.setter
    def gfunction_g_value_42(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 42`

        Args:
            value (float): value for IDD Field `G-Function G Value 42`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 42"] = value

    @property
    def gfunction_lnt_or_ts_value_43(self):
        """Get gfunction_lnt_or_ts_value_43.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_43` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 43"]

    @gfunction_lnt_or_ts_value_43.setter
    def gfunction_lnt_or_ts_value_43(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 43`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 43`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 43"] = value

    @property
    def gfunction_g_value_43(self):
        """Get gfunction_g_value_43.

        Returns:
            float: the value of `gfunction_g_value_43` or None if not set

        """
        return self["G-Function G Value 43"]

    @gfunction_g_value_43.setter
    def gfunction_g_value_43(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 43`

        Args:
            value (float): value for IDD Field `G-Function G Value 43`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 43"] = value

    @property
    def gfunction_lnt_or_ts_value_44(self):
        """Get gfunction_lnt_or_ts_value_44.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_44` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 44"]

    @gfunction_lnt_or_ts_value_44.setter
    def gfunction_lnt_or_ts_value_44(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 44`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 44`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 44"] = value

    @property
    def gfunction_g_value_44(self):
        """Get gfunction_g_value_44.

        Returns:
            float: the value of `gfunction_g_value_44` or None if not set

        """
        return self["G-Function G Value 44"]

    @gfunction_g_value_44.setter
    def gfunction_g_value_44(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 44`

        Args:
            value (float): value for IDD Field `G-Function G Value 44`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 44"] = value

    @property
    def gfunction_lnt_or_ts_value_45(self):
        """Get gfunction_lnt_or_ts_value_45.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_45` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 45"]

    @gfunction_lnt_or_ts_value_45.setter
    def gfunction_lnt_or_ts_value_45(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 45`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 45`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 45"] = value

    @property
    def gfunction_g_value_45(self):
        """Get gfunction_g_value_45.

        Returns:
            float: the value of `gfunction_g_value_45` or None if not set

        """
        return self["G-Function G Value 45"]

    @gfunction_g_value_45.setter
    def gfunction_g_value_45(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 45`

        Args:
            value (float): value for IDD Field `G-Function G Value 45`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 45"] = value

    @property
    def gfunction_lnt_or_ts_value_46(self):
        """Get gfunction_lnt_or_ts_value_46.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_46` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 46"]

    @gfunction_lnt_or_ts_value_46.setter
    def gfunction_lnt_or_ts_value_46(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 46`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 46`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 46"] = value

    @property
    def gfunction_g_value_46(self):
        """Get gfunction_g_value_46.

        Returns:
            float: the value of `gfunction_g_value_46` or None if not set

        """
        return self["G-Function G Value 46"]

    @gfunction_g_value_46.setter
    def gfunction_g_value_46(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 46`

        Args:
            value (float): value for IDD Field `G-Function G Value 46`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 46"] = value

    @property
    def gfunction_lnt_or_ts_value_47(self):
        """Get gfunction_lnt_or_ts_value_47.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_47` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 47"]

    @gfunction_lnt_or_ts_value_47.setter
    def gfunction_lnt_or_ts_value_47(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 47`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 47`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 47"] = value

    @property
    def gfunction_g_value_47(self):
        """Get gfunction_g_value_47.

        Returns:
            float: the value of `gfunction_g_value_47` or None if not set

        """
        return self["G-Function G Value 47"]

    @gfunction_g_value_47.setter
    def gfunction_g_value_47(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 47`

        Args:
            value (float): value for IDD Field `G-Function G Value 47`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 47"] = value

    @property
    def gfunction_lnt_or_ts_value_48(self):
        """Get gfunction_lnt_or_ts_value_48.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_48` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 48"]

    @gfunction_lnt_or_ts_value_48.setter
    def gfunction_lnt_or_ts_value_48(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 48`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 48`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 48"] = value

    @property
    def gfunction_g_value_48(self):
        """Get gfunction_g_value_48.

        Returns:
            float: the value of `gfunction_g_value_48` or None if not set

        """
        return self["G-Function G Value 48"]

    @gfunction_g_value_48.setter
    def gfunction_g_value_48(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 48`

        Args:
            value (float): value for IDD Field `G-Function G Value 48`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 48"] = value

    @property
    def gfunction_lnt_or_ts_value_49(self):
        """Get gfunction_lnt_or_ts_value_49.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_49` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 49"]

    @gfunction_lnt_or_ts_value_49.setter
    def gfunction_lnt_or_ts_value_49(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 49`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 49`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 49"] = value

    @property
    def gfunction_g_value_49(self):
        """Get gfunction_g_value_49.

        Returns:
            float: the value of `gfunction_g_value_49` or None if not set

        """
        return self["G-Function G Value 49"]

    @gfunction_g_value_49.setter
    def gfunction_g_value_49(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 49`

        Args:
            value (float): value for IDD Field `G-Function G Value 49`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 49"] = value

    @property
    def gfunction_lnt_or_ts_value_50(self):
        """Get gfunction_lnt_or_ts_value_50.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_50` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 50"]

    @gfunction_lnt_or_ts_value_50.setter
    def gfunction_lnt_or_ts_value_50(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 50`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 50`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 50"] = value

    @property
    def gfunction_g_value_50(self):
        """Get gfunction_g_value_50.

        Returns:
            float: the value of `gfunction_g_value_50` or None if not set

        """
        return self["G-Function G Value 50"]

    @gfunction_g_value_50.setter
    def gfunction_g_value_50(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 50`

        Args:
            value (float): value for IDD Field `G-Function G Value 50`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 50"] = value

    @property
    def gfunction_lnt_or_ts_value_51(self):
        """Get gfunction_lnt_or_ts_value_51.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_51` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 51"]

    @gfunction_lnt_or_ts_value_51.setter
    def gfunction_lnt_or_ts_value_51(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 51`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 51`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 51"] = value

    @property
    def gfunction_g_value_51(self):
        """Get gfunction_g_value_51.

        Returns:
            float: the value of `gfunction_g_value_51` or None if not set

        """
        return self["G-Function G Value 51"]

    @gfunction_g_value_51.setter
    def gfunction_g_value_51(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 51`

        Args:
            value (float): value for IDD Field `G-Function G Value 51`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 51"] = value

    @property
    def gfunction_lnt_or_ts_value_52(self):
        """Get gfunction_lnt_or_ts_value_52.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_52` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 52"]

    @gfunction_lnt_or_ts_value_52.setter
    def gfunction_lnt_or_ts_value_52(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 52`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 52`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 52"] = value

    @property
    def gfunction_g_value_52(self):
        """Get gfunction_g_value_52.

        Returns:
            float: the value of `gfunction_g_value_52` or None if not set

        """
        return self["G-Function G Value 52"]

    @gfunction_g_value_52.setter
    def gfunction_g_value_52(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 52`

        Args:
            value (float): value for IDD Field `G-Function G Value 52`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 52"] = value

    @property
    def gfunction_lnt_or_ts_value_53(self):
        """Get gfunction_lnt_or_ts_value_53.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_53` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 53"]

    @gfunction_lnt_or_ts_value_53.setter
    def gfunction_lnt_or_ts_value_53(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 53`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 53`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 53"] = value

    @property
    def gfunction_g_value_53(self):
        """Get gfunction_g_value_53.

        Returns:
            float: the value of `gfunction_g_value_53` or None if not set

        """
        return self["G-Function G Value 53"]

    @gfunction_g_value_53.setter
    def gfunction_g_value_53(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 53`

        Args:
            value (float): value for IDD Field `G-Function G Value 53`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 53"] = value

    @property
    def gfunction_lnt_or_ts_value_54(self):
        """Get gfunction_lnt_or_ts_value_54.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_54` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 54"]

    @gfunction_lnt_or_ts_value_54.setter
    def gfunction_lnt_or_ts_value_54(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 54`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 54`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 54"] = value

    @property
    def gfunction_g_value_54(self):
        """Get gfunction_g_value_54.

        Returns:
            float: the value of `gfunction_g_value_54` or None if not set

        """
        return self["G-Function G Value 54"]

    @gfunction_g_value_54.setter
    def gfunction_g_value_54(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 54`

        Args:
            value (float): value for IDD Field `G-Function G Value 54`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 54"] = value

    @property
    def gfunction_lnt_or_ts_value_55(self):
        """Get gfunction_lnt_or_ts_value_55.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_55` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 55"]

    @gfunction_lnt_or_ts_value_55.setter
    def gfunction_lnt_or_ts_value_55(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 55`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 55`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 55"] = value

    @property
    def gfunction_g_value_55(self):
        """Get gfunction_g_value_55.

        Returns:
            float: the value of `gfunction_g_value_55` or None if not set

        """
        return self["G-Function G Value 55"]

    @gfunction_g_value_55.setter
    def gfunction_g_value_55(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 55`

        Args:
            value (float): value for IDD Field `G-Function G Value 55`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 55"] = value

    @property
    def gfunction_lnt_or_ts_value_56(self):
        """Get gfunction_lnt_or_ts_value_56.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_56` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 56"]

    @gfunction_lnt_or_ts_value_56.setter
    def gfunction_lnt_or_ts_value_56(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 56`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 56`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 56"] = value

    @property
    def gfunction_g_value_56(self):
        """Get gfunction_g_value_56.

        Returns:
            float: the value of `gfunction_g_value_56` or None if not set

        """
        return self["G-Function G Value 56"]

    @gfunction_g_value_56.setter
    def gfunction_g_value_56(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 56`

        Args:
            value (float): value for IDD Field `G-Function G Value 56`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 56"] = value

    @property
    def gfunction_lnt_or_ts_value_57(self):
        """Get gfunction_lnt_or_ts_value_57.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_57` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 57"]

    @gfunction_lnt_or_ts_value_57.setter
    def gfunction_lnt_or_ts_value_57(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 57`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 57`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 57"] = value

    @property
    def gfunction_g_value_57(self):
        """Get gfunction_g_value_57.

        Returns:
            float: the value of `gfunction_g_value_57` or None if not set

        """
        return self["G-Function G Value 57"]

    @gfunction_g_value_57.setter
    def gfunction_g_value_57(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 57`

        Args:
            value (float): value for IDD Field `G-Function G Value 57`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 57"] = value

    @property
    def gfunction_lnt_or_ts_value_58(self):
        """Get gfunction_lnt_or_ts_value_58.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_58` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 58"]

    @gfunction_lnt_or_ts_value_58.setter
    def gfunction_lnt_or_ts_value_58(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 58`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 58`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 58"] = value

    @property
    def gfunction_g_value_58(self):
        """Get gfunction_g_value_58.

        Returns:
            float: the value of `gfunction_g_value_58` or None if not set

        """
        return self["G-Function G Value 58"]

    @gfunction_g_value_58.setter
    def gfunction_g_value_58(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 58`

        Args:
            value (float): value for IDD Field `G-Function G Value 58`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 58"] = value

    @property
    def gfunction_lnt_or_ts_value_59(self):
        """Get gfunction_lnt_or_ts_value_59.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_59` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 59"]

    @gfunction_lnt_or_ts_value_59.setter
    def gfunction_lnt_or_ts_value_59(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 59`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 59`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 59"] = value

    @property
    def gfunction_g_value_59(self):
        """Get gfunction_g_value_59.

        Returns:
            float: the value of `gfunction_g_value_59` or None if not set

        """
        return self["G-Function G Value 59"]

    @gfunction_g_value_59.setter
    def gfunction_g_value_59(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 59`

        Args:
            value (float): value for IDD Field `G-Function G Value 59`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 59"] = value

    @property
    def gfunction_lnt_or_ts_value_60(self):
        """Get gfunction_lnt_or_ts_value_60.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_60` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 60"]

    @gfunction_lnt_or_ts_value_60.setter
    def gfunction_lnt_or_ts_value_60(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 60`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 60`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 60"] = value

    @property
    def gfunction_g_value_60(self):
        """Get gfunction_g_value_60.

        Returns:
            float: the value of `gfunction_g_value_60` or None if not set

        """
        return self["G-Function G Value 60"]

    @gfunction_g_value_60.setter
    def gfunction_g_value_60(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 60`

        Args:
            value (float): value for IDD Field `G-Function G Value 60`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 60"] = value

    @property
    def gfunction_lnt_or_ts_value_61(self):
        """Get gfunction_lnt_or_ts_value_61.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_61` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 61"]

    @gfunction_lnt_or_ts_value_61.setter
    def gfunction_lnt_or_ts_value_61(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 61`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 61`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 61"] = value

    @property
    def gfunction_g_value_61(self):
        """Get gfunction_g_value_61.

        Returns:
            float: the value of `gfunction_g_value_61` or None if not set

        """
        return self["G-Function G Value 61"]

    @gfunction_g_value_61.setter
    def gfunction_g_value_61(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 61`

        Args:
            value (float): value for IDD Field `G-Function G Value 61`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 61"] = value

    @property
    def gfunction_lnt_or_ts_value_62(self):
        """Get gfunction_lnt_or_ts_value_62.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_62` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 62"]

    @gfunction_lnt_or_ts_value_62.setter
    def gfunction_lnt_or_ts_value_62(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 62`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 62`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 62"] = value

    @property
    def gfunction_g_value_62(self):
        """Get gfunction_g_value_62.

        Returns:
            float: the value of `gfunction_g_value_62` or None if not set

        """
        return self["G-Function G Value 62"]

    @gfunction_g_value_62.setter
    def gfunction_g_value_62(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 62`

        Args:
            value (float): value for IDD Field `G-Function G Value 62`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 62"] = value

    @property
    def gfunction_lnt_or_ts_value_63(self):
        """Get gfunction_lnt_or_ts_value_63.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_63` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 63"]

    @gfunction_lnt_or_ts_value_63.setter
    def gfunction_lnt_or_ts_value_63(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 63`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 63`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 63"] = value

    @property
    def gfunction_g_value_63(self):
        """Get gfunction_g_value_63.

        Returns:
            float: the value of `gfunction_g_value_63` or None if not set

        """
        return self["G-Function G Value 63"]

    @gfunction_g_value_63.setter
    def gfunction_g_value_63(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 63`

        Args:
            value (float): value for IDD Field `G-Function G Value 63`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 63"] = value

    @property
    def gfunction_lnt_or_ts_value_64(self):
        """Get gfunction_lnt_or_ts_value_64.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_64` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 64"]

    @gfunction_lnt_or_ts_value_64.setter
    def gfunction_lnt_or_ts_value_64(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 64`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 64`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 64"] = value

    @property
    def gfunction_g_value_64(self):
        """Get gfunction_g_value_64.

        Returns:
            float: the value of `gfunction_g_value_64` or None if not set

        """
        return self["G-Function G Value 64"]

    @gfunction_g_value_64.setter
    def gfunction_g_value_64(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 64`

        Args:
            value (float): value for IDD Field `G-Function G Value 64`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 64"] = value

    @property
    def gfunction_lnt_or_ts_value_65(self):
        """Get gfunction_lnt_or_ts_value_65.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_65` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 65"]

    @gfunction_lnt_or_ts_value_65.setter
    def gfunction_lnt_or_ts_value_65(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 65`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 65`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 65"] = value

    @property
    def gfunction_g_value_65(self):
        """Get gfunction_g_value_65.

        Returns:
            float: the value of `gfunction_g_value_65` or None if not set

        """
        return self["G-Function G Value 65"]

    @gfunction_g_value_65.setter
    def gfunction_g_value_65(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 65`

        Args:
            value (float): value for IDD Field `G-Function G Value 65`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 65"] = value

    @property
    def gfunction_lnt_or_ts_value_66(self):
        """Get gfunction_lnt_or_ts_value_66.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_66` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 66"]

    @gfunction_lnt_or_ts_value_66.setter
    def gfunction_lnt_or_ts_value_66(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 66`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 66`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 66"] = value

    @property
    def gfunction_g_value_66(self):
        """Get gfunction_g_value_66.

        Returns:
            float: the value of `gfunction_g_value_66` or None if not set

        """
        return self["G-Function G Value 66"]

    @gfunction_g_value_66.setter
    def gfunction_g_value_66(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 66`

        Args:
            value (float): value for IDD Field `G-Function G Value 66`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 66"] = value

    @property
    def gfunction_lnt_or_ts_value_67(self):
        """Get gfunction_lnt_or_ts_value_67.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_67` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 67"]

    @gfunction_lnt_or_ts_value_67.setter
    def gfunction_lnt_or_ts_value_67(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 67`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 67`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 67"] = value

    @property
    def gfunction_g_value_67(self):
        """Get gfunction_g_value_67.

        Returns:
            float: the value of `gfunction_g_value_67` or None if not set

        """
        return self["G-Function G Value 67"]

    @gfunction_g_value_67.setter
    def gfunction_g_value_67(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 67`

        Args:
            value (float): value for IDD Field `G-Function G Value 67`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 67"] = value

    @property
    def gfunction_lnt_or_ts_value_68(self):
        """Get gfunction_lnt_or_ts_value_68.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_68` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 68"]

    @gfunction_lnt_or_ts_value_68.setter
    def gfunction_lnt_or_ts_value_68(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 68`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 68`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 68"] = value

    @property
    def gfunction_g_value_68(self):
        """Get gfunction_g_value_68.

        Returns:
            float: the value of `gfunction_g_value_68` or None if not set

        """
        return self["G-Function G Value 68"]

    @gfunction_g_value_68.setter
    def gfunction_g_value_68(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 68`

        Args:
            value (float): value for IDD Field `G-Function G Value 68`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 68"] = value

    @property
    def gfunction_lnt_or_ts_value_69(self):
        """Get gfunction_lnt_or_ts_value_69.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_69` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 69"]

    @gfunction_lnt_or_ts_value_69.setter
    def gfunction_lnt_or_ts_value_69(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 69`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 69`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 69"] = value

    @property
    def gfunction_g_value_69(self):
        """Get gfunction_g_value_69.

        Returns:
            float: the value of `gfunction_g_value_69` or None if not set

        """
        return self["G-Function G Value 69"]

    @gfunction_g_value_69.setter
    def gfunction_g_value_69(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 69`

        Args:
            value (float): value for IDD Field `G-Function G Value 69`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 69"] = value

    @property
    def gfunction_lnt_or_ts_value_70(self):
        """Get gfunction_lnt_or_ts_value_70.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_70` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 70"]

    @gfunction_lnt_or_ts_value_70.setter
    def gfunction_lnt_or_ts_value_70(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 70`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 70`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 70"] = value

    @property
    def gfunction_g_value_70(self):
        """Get gfunction_g_value_70.

        Returns:
            float: the value of `gfunction_g_value_70` or None if not set

        """
        return self["G-Function G Value 70"]

    @gfunction_g_value_70.setter
    def gfunction_g_value_70(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 70`

        Args:
            value (float): value for IDD Field `G-Function G Value 70`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 70"] = value

    @property
    def gfunction_lnt_or_ts_value_71(self):
        """Get gfunction_lnt_or_ts_value_71.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_71` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 71"]

    @gfunction_lnt_or_ts_value_71.setter
    def gfunction_lnt_or_ts_value_71(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 71`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 71`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 71"] = value

    @property
    def gfunction_g_value_71(self):
        """Get gfunction_g_value_71.

        Returns:
            float: the value of `gfunction_g_value_71` or None if not set

        """
        return self["G-Function G Value 71"]

    @gfunction_g_value_71.setter
    def gfunction_g_value_71(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 71`

        Args:
            value (float): value for IDD Field `G-Function G Value 71`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 71"] = value

    @property
    def gfunction_lnt_or_ts_value_72(self):
        """Get gfunction_lnt_or_ts_value_72.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_72` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 72"]

    @gfunction_lnt_or_ts_value_72.setter
    def gfunction_lnt_or_ts_value_72(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 72`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 72`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 72"] = value

    @property
    def gfunction_g_value_72(self):
        """Get gfunction_g_value_72.

        Returns:
            float: the value of `gfunction_g_value_72` or None if not set

        """
        return self["G-Function G Value 72"]

    @gfunction_g_value_72.setter
    def gfunction_g_value_72(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 72`

        Args:
            value (float): value for IDD Field `G-Function G Value 72`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 72"] = value

    @property
    def gfunction_lnt_or_ts_value_73(self):
        """Get gfunction_lnt_or_ts_value_73.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_73` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 73"]

    @gfunction_lnt_or_ts_value_73.setter
    def gfunction_lnt_or_ts_value_73(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 73`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 73`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 73"] = value

    @property
    def gfunction_g_value_73(self):
        """Get gfunction_g_value_73.

        Returns:
            float: the value of `gfunction_g_value_73` or None if not set

        """
        return self["G-Function G Value 73"]

    @gfunction_g_value_73.setter
    def gfunction_g_value_73(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 73`

        Args:
            value (float): value for IDD Field `G-Function G Value 73`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 73"] = value

    @property
    def gfunction_lnt_or_ts_value_74(self):
        """Get gfunction_lnt_or_ts_value_74.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_74` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 74"]

    @gfunction_lnt_or_ts_value_74.setter
    def gfunction_lnt_or_ts_value_74(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 74`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 74`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 74"] = value

    @property
    def gfunction_g_value_74(self):
        """Get gfunction_g_value_74.

        Returns:
            float: the value of `gfunction_g_value_74` or None if not set

        """
        return self["G-Function G Value 74"]

    @gfunction_g_value_74.setter
    def gfunction_g_value_74(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 74`

        Args:
            value (float): value for IDD Field `G-Function G Value 74`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 74"] = value

    @property
    def gfunction_lnt_or_ts_value_75(self):
        """Get gfunction_lnt_or_ts_value_75.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_75` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 75"]

    @gfunction_lnt_or_ts_value_75.setter
    def gfunction_lnt_or_ts_value_75(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 75`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 75`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 75"] = value

    @property
    def gfunction_g_value_75(self):
        """Get gfunction_g_value_75.

        Returns:
            float: the value of `gfunction_g_value_75` or None if not set

        """
        return self["G-Function G Value 75"]

    @gfunction_g_value_75.setter
    def gfunction_g_value_75(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 75`

        Args:
            value (float): value for IDD Field `G-Function G Value 75`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 75"] = value

    @property
    def gfunction_lnt_or_ts_value_76(self):
        """Get gfunction_lnt_or_ts_value_76.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_76` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 76"]

    @gfunction_lnt_or_ts_value_76.setter
    def gfunction_lnt_or_ts_value_76(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 76`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 76`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 76"] = value

    @property
    def gfunction_g_value_76(self):
        """Get gfunction_g_value_76.

        Returns:
            float: the value of `gfunction_g_value_76` or None if not set

        """
        return self["G-Function G Value 76"]

    @gfunction_g_value_76.setter
    def gfunction_g_value_76(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 76`

        Args:
            value (float): value for IDD Field `G-Function G Value 76`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 76"] = value

    @property
    def gfunction_lnt_or_ts_value_77(self):
        """Get gfunction_lnt_or_ts_value_77.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_77` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 77"]

    @gfunction_lnt_or_ts_value_77.setter
    def gfunction_lnt_or_ts_value_77(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 77`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 77`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 77"] = value

    @property
    def gfunction_g_value_77(self):
        """Get gfunction_g_value_77.

        Returns:
            float: the value of `gfunction_g_value_77` or None if not set

        """
        return self["G-Function G Value 77"]

    @gfunction_g_value_77.setter
    def gfunction_g_value_77(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 77`

        Args:
            value (float): value for IDD Field `G-Function G Value 77`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 77"] = value

    @property
    def gfunction_lnt_or_ts_value_78(self):
        """Get gfunction_lnt_or_ts_value_78.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_78` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 78"]

    @gfunction_lnt_or_ts_value_78.setter
    def gfunction_lnt_or_ts_value_78(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 78`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 78`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 78"] = value

    @property
    def gfunction_g_value_78(self):
        """Get gfunction_g_value_78.

        Returns:
            float: the value of `gfunction_g_value_78` or None if not set

        """
        return self["G-Function G Value 78"]

    @gfunction_g_value_78.setter
    def gfunction_g_value_78(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 78`

        Args:
            value (float): value for IDD Field `G-Function G Value 78`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 78"] = value

    @property
    def gfunction_lnt_or_ts_value_79(self):
        """Get gfunction_lnt_or_ts_value_79.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_79` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 79"]

    @gfunction_lnt_or_ts_value_79.setter
    def gfunction_lnt_or_ts_value_79(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 79`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 79`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 79"] = value

    @property
    def gfunction_g_value_79(self):
        """Get gfunction_g_value_79.

        Returns:
            float: the value of `gfunction_g_value_79` or None if not set

        """
        return self["G-Function G Value 79"]

    @gfunction_g_value_79.setter
    def gfunction_g_value_79(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 79`

        Args:
            value (float): value for IDD Field `G-Function G Value 79`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 79"] = value

    @property
    def gfunction_lnt_or_ts_value_80(self):
        """Get gfunction_lnt_or_ts_value_80.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_80` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 80"]

    @gfunction_lnt_or_ts_value_80.setter
    def gfunction_lnt_or_ts_value_80(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 80`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 80`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 80"] = value

    @property
    def gfunction_g_value_80(self):
        """Get gfunction_g_value_80.

        Returns:
            float: the value of `gfunction_g_value_80` or None if not set

        """
        return self["G-Function G Value 80"]

    @gfunction_g_value_80.setter
    def gfunction_g_value_80(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 80`

        Args:
            value (float): value for IDD Field `G-Function G Value 80`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 80"] = value

    @property
    def gfunction_lnt_or_ts_value_81(self):
        """Get gfunction_lnt_or_ts_value_81.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_81` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 81"]

    @gfunction_lnt_or_ts_value_81.setter
    def gfunction_lnt_or_ts_value_81(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 81`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 81`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 81"] = value

    @property
    def gfunction_g_value_81(self):
        """Get gfunction_g_value_81.

        Returns:
            float: the value of `gfunction_g_value_81` or None if not set

        """
        return self["G-Function G Value 81"]

    @gfunction_g_value_81.setter
    def gfunction_g_value_81(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 81`

        Args:
            value (float): value for IDD Field `G-Function G Value 81`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 81"] = value

    @property
    def gfunction_lnt_or_ts_value_82(self):
        """Get gfunction_lnt_or_ts_value_82.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_82` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 82"]

    @gfunction_lnt_or_ts_value_82.setter
    def gfunction_lnt_or_ts_value_82(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 82`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 82`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 82"] = value

    @property
    def gfunction_g_value_82(self):
        """Get gfunction_g_value_82.

        Returns:
            float: the value of `gfunction_g_value_82` or None if not set

        """
        return self["G-Function G Value 82"]

    @gfunction_g_value_82.setter
    def gfunction_g_value_82(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 82`

        Args:
            value (float): value for IDD Field `G-Function G Value 82`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 82"] = value

    @property
    def gfunction_lnt_or_ts_value_83(self):
        """Get gfunction_lnt_or_ts_value_83.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_83` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 83"]

    @gfunction_lnt_or_ts_value_83.setter
    def gfunction_lnt_or_ts_value_83(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 83`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 83`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 83"] = value

    @property
    def gfunction_g_value_83(self):
        """Get gfunction_g_value_83.

        Returns:
            float: the value of `gfunction_g_value_83` or None if not set

        """
        return self["G-Function G Value 83"]

    @gfunction_g_value_83.setter
    def gfunction_g_value_83(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 83`

        Args:
            value (float): value for IDD Field `G-Function G Value 83`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 83"] = value

    @property
    def gfunction_lnt_or_ts_value_84(self):
        """Get gfunction_lnt_or_ts_value_84.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_84` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 84"]

    @gfunction_lnt_or_ts_value_84.setter
    def gfunction_lnt_or_ts_value_84(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 84`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 84`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 84"] = value

    @property
    def gfunction_g_value_84(self):
        """Get gfunction_g_value_84.

        Returns:
            float: the value of `gfunction_g_value_84` or None if not set

        """
        return self["G-Function G Value 84"]

    @gfunction_g_value_84.setter
    def gfunction_g_value_84(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 84`

        Args:
            value (float): value for IDD Field `G-Function G Value 84`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 84"] = value

    @property
    def gfunction_lnt_or_ts_value_85(self):
        """Get gfunction_lnt_or_ts_value_85.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_85` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 85"]

    @gfunction_lnt_or_ts_value_85.setter
    def gfunction_lnt_or_ts_value_85(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 85`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 85`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 85"] = value

    @property
    def gfunction_g_value_85(self):
        """Get gfunction_g_value_85.

        Returns:
            float: the value of `gfunction_g_value_85` or None if not set

        """
        return self["G-Function G Value 85"]

    @gfunction_g_value_85.setter
    def gfunction_g_value_85(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 85`

        Args:
            value (float): value for IDD Field `G-Function G Value 85`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 85"] = value

    @property
    def gfunction_lnt_or_ts_value_86(self):
        """Get gfunction_lnt_or_ts_value_86.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_86` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 86"]

    @gfunction_lnt_or_ts_value_86.setter
    def gfunction_lnt_or_ts_value_86(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 86`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 86`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 86"] = value

    @property
    def gfunction_g_value_86(self):
        """Get gfunction_g_value_86.

        Returns:
            float: the value of `gfunction_g_value_86` or None if not set

        """
        return self["G-Function G Value 86"]

    @gfunction_g_value_86.setter
    def gfunction_g_value_86(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 86`

        Args:
            value (float): value for IDD Field `G-Function G Value 86`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 86"] = value

    @property
    def gfunction_lnt_or_ts_value_87(self):
        """Get gfunction_lnt_or_ts_value_87.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_87` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 87"]

    @gfunction_lnt_or_ts_value_87.setter
    def gfunction_lnt_or_ts_value_87(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 87`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 87`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 87"] = value

    @property
    def gfunction_g_value_87(self):
        """Get gfunction_g_value_87.

        Returns:
            float: the value of `gfunction_g_value_87` or None if not set

        """
        return self["G-Function G Value 87"]

    @gfunction_g_value_87.setter
    def gfunction_g_value_87(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 87`

        Args:
            value (float): value for IDD Field `G-Function G Value 87`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 87"] = value

    @property
    def gfunction_lnt_or_ts_value_88(self):
        """Get gfunction_lnt_or_ts_value_88.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_88` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 88"]

    @gfunction_lnt_or_ts_value_88.setter
    def gfunction_lnt_or_ts_value_88(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 88`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 88`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 88"] = value

    @property
    def gfunction_g_value_88(self):
        """Get gfunction_g_value_88.

        Returns:
            float: the value of `gfunction_g_value_88` or None if not set

        """
        return self["G-Function G Value 88"]

    @gfunction_g_value_88.setter
    def gfunction_g_value_88(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 88`

        Args:
            value (float): value for IDD Field `G-Function G Value 88`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 88"] = value

    @property
    def gfunction_lnt_or_ts_value_89(self):
        """Get gfunction_lnt_or_ts_value_89.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_89` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 89"]

    @gfunction_lnt_or_ts_value_89.setter
    def gfunction_lnt_or_ts_value_89(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 89`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 89`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 89"] = value

    @property
    def gfunction_g_value_89(self):
        """Get gfunction_g_value_89.

        Returns:
            float: the value of `gfunction_g_value_89` or None if not set

        """
        return self["G-Function G Value 89"]

    @gfunction_g_value_89.setter
    def gfunction_g_value_89(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 89`

        Args:
            value (float): value for IDD Field `G-Function G Value 89`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 89"] = value

    @property
    def gfunction_lnt_or_ts_value_90(self):
        """Get gfunction_lnt_or_ts_value_90.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_90` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 90"]

    @gfunction_lnt_or_ts_value_90.setter
    def gfunction_lnt_or_ts_value_90(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 90`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 90`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 90"] = value

    @property
    def gfunction_g_value_90(self):
        """Get gfunction_g_value_90.

        Returns:
            float: the value of `gfunction_g_value_90` or None if not set

        """
        return self["G-Function G Value 90"]

    @gfunction_g_value_90.setter
    def gfunction_g_value_90(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 90`

        Args:
            value (float): value for IDD Field `G-Function G Value 90`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 90"] = value

    @property
    def gfunction_lnt_or_ts_value_91(self):
        """Get gfunction_lnt_or_ts_value_91.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_91` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 91"]

    @gfunction_lnt_or_ts_value_91.setter
    def gfunction_lnt_or_ts_value_91(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 91`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 91`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 91"] = value

    @property
    def gfunction_g_value_91(self):
        """Get gfunction_g_value_91.

        Returns:
            float: the value of `gfunction_g_value_91` or None if not set

        """
        return self["G-Function G Value 91"]

    @gfunction_g_value_91.setter
    def gfunction_g_value_91(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 91`

        Args:
            value (float): value for IDD Field `G-Function G Value 91`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 91"] = value

    @property
    def gfunction_lnt_or_ts_value_92(self):
        """Get gfunction_lnt_or_ts_value_92.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_92` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 92"]

    @gfunction_lnt_or_ts_value_92.setter
    def gfunction_lnt_or_ts_value_92(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 92`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 92`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 92"] = value

    @property
    def gfunction_g_value_92(self):
        """Get gfunction_g_value_92.

        Returns:
            float: the value of `gfunction_g_value_92` or None if not set

        """
        return self["G-Function G Value 92"]

    @gfunction_g_value_92.setter
    def gfunction_g_value_92(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 92`

        Args:
            value (float): value for IDD Field `G-Function G Value 92`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 92"] = value

    @property
    def gfunction_lnt_or_ts_value_93(self):
        """Get gfunction_lnt_or_ts_value_93.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_93` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 93"]

    @gfunction_lnt_or_ts_value_93.setter
    def gfunction_lnt_or_ts_value_93(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 93`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 93`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 93"] = value

    @property
    def gfunction_g_value_93(self):
        """Get gfunction_g_value_93.

        Returns:
            float: the value of `gfunction_g_value_93` or None if not set

        """
        return self["G-Function G Value 93"]

    @gfunction_g_value_93.setter
    def gfunction_g_value_93(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 93`

        Args:
            value (float): value for IDD Field `G-Function G Value 93`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 93"] = value

    @property
    def gfunction_lnt_or_ts_value_94(self):
        """Get gfunction_lnt_or_ts_value_94.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_94` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 94"]

    @gfunction_lnt_or_ts_value_94.setter
    def gfunction_lnt_or_ts_value_94(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 94`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 94`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 94"] = value

    @property
    def gfunction_g_value_94(self):
        """Get gfunction_g_value_94.

        Returns:
            float: the value of `gfunction_g_value_94` or None if not set

        """
        return self["G-Function G Value 94"]

    @gfunction_g_value_94.setter
    def gfunction_g_value_94(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 94`

        Args:
            value (float): value for IDD Field `G-Function G Value 94`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 94"] = value

    @property
    def gfunction_lnt_or_ts_value_95(self):
        """Get gfunction_lnt_or_ts_value_95.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_95` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 95"]

    @gfunction_lnt_or_ts_value_95.setter
    def gfunction_lnt_or_ts_value_95(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 95`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 95`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 95"] = value

    @property
    def gfunction_g_value_95(self):
        """Get gfunction_g_value_95.

        Returns:
            float: the value of `gfunction_g_value_95` or None if not set

        """
        return self["G-Function G Value 95"]

    @gfunction_g_value_95.setter
    def gfunction_g_value_95(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 95`

        Args:
            value (float): value for IDD Field `G-Function G Value 95`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 95"] = value

    @property
    def gfunction_lnt_or_ts_value_96(self):
        """Get gfunction_lnt_or_ts_value_96.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_96` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 96"]

    @gfunction_lnt_or_ts_value_96.setter
    def gfunction_lnt_or_ts_value_96(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 96`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 96`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 96"] = value

    @property
    def gfunction_g_value_96(self):
        """Get gfunction_g_value_96.

        Returns:
            float: the value of `gfunction_g_value_96` or None if not set

        """
        return self["G-Function G Value 96"]

    @gfunction_g_value_96.setter
    def gfunction_g_value_96(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 96`

        Args:
            value (float): value for IDD Field `G-Function G Value 96`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 96"] = value

    @property
    def gfunction_lnt_or_ts_value_97(self):
        """Get gfunction_lnt_or_ts_value_97.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_97` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 97"]

    @gfunction_lnt_or_ts_value_97.setter
    def gfunction_lnt_or_ts_value_97(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 97`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 97`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 97"] = value

    @property
    def gfunction_g_value_97(self):
        """Get gfunction_g_value_97.

        Returns:
            float: the value of `gfunction_g_value_97` or None if not set

        """
        return self["G-Function G Value 97"]

    @gfunction_g_value_97.setter
    def gfunction_g_value_97(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 97`

        Args:
            value (float): value for IDD Field `G-Function G Value 97`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 97"] = value

    @property
    def gfunction_lnt_or_ts_value_98(self):
        """Get gfunction_lnt_or_ts_value_98.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_98` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 98"]

    @gfunction_lnt_or_ts_value_98.setter
    def gfunction_lnt_or_ts_value_98(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 98`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 98`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 98"] = value

    @property
    def gfunction_g_value_98(self):
        """Get gfunction_g_value_98.

        Returns:
            float: the value of `gfunction_g_value_98` or None if not set

        """
        return self["G-Function G Value 98"]

    @gfunction_g_value_98.setter
    def gfunction_g_value_98(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 98`

        Args:
            value (float): value for IDD Field `G-Function G Value 98`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 98"] = value

    @property
    def gfunction_lnt_or_ts_value_99(self):
        """Get gfunction_lnt_or_ts_value_99.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_99` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 99"]

    @gfunction_lnt_or_ts_value_99.setter
    def gfunction_lnt_or_ts_value_99(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 99`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 99`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 99"] = value

    @property
    def gfunction_g_value_99(self):
        """Get gfunction_g_value_99.

        Returns:
            float: the value of `gfunction_g_value_99` or None if not set

        """
        return self["G-Function G Value 99"]

    @gfunction_g_value_99.setter
    def gfunction_g_value_99(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 99`

        Args:
            value (float): value for IDD Field `G-Function G Value 99`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 99"] = value

    @property
    def gfunction_lnt_or_ts_value_100(self):
        """Get gfunction_lnt_or_ts_value_100.

        Returns:
            float: the value of `gfunction_lnt_or_ts_value_100` or None if not set

        """
        return self["G-Function Ln(T/Ts) Value 100"]

    @gfunction_lnt_or_ts_value_100.setter
    def gfunction_lnt_or_ts_value_100(self, value=None):
        """  Corresponds to IDD field `G-Function Ln(T/Ts) Value 100`

        Args:
            value (float): value for IDD Field `G-Function Ln(T/Ts) Value 100`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function Ln(T/Ts) Value 100"] = value

    @property
    def gfunction_g_value_100(self):
        """Get gfunction_g_value_100.

        Returns:
            float: the value of `gfunction_g_value_100` or None if not set

        """
        return self["G-Function G Value 100"]

    @gfunction_g_value_100.setter
    def gfunction_g_value_100(self, value=None):
        """  Corresponds to IDD field `G-Function G Value 100`

        Args:
            value (float): value for IDD Field `G-Function G Value 100`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["G-Function G Value 100"] = value




class GroundHeatExchangerPond(DataObject):

    """ Corresponds to IDD object `GroundHeatExchanger:Pond`
        A model of a shallow pond with immersed pipe loops.
        Typically used in hybrid geothermal systems and included in the condenser loop.
        This component may also be used as a simple solar collector.
    """
    schema = {'extensible-fields': OrderedDict(),
              'fields': OrderedDict([(u'name',
                                      {'name': u'Name',
                                       'pyname': u'name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'fluid inlet node name',
                                      {'name': u'Fluid Inlet Node Name',
                                       'pyname': u'fluid_inlet_node_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'node'}),
                                     (u'fluid outlet node name',
                                      {'name': u'Fluid Outlet Node Name',
                                       'pyname': u'fluid_outlet_node_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'node'}),
                                     (u'pond depth',
                                      {'name': u'Pond Depth',
                                       'pyname': u'pond_depth',
                                       'minimum>': 0.0,
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'm'}),
                                     (u'pond area',
                                      {'name': u'Pond Area',
                                       'pyname': u'pond_area',
                                       'minimum>': 0.0,
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'm2'}),
                                     (u'hydronic tubing inside diameter',
                                      {'name': u'Hydronic Tubing Inside Diameter',
                                       'pyname': u'hydronic_tubing_inside_diameter',
                                       'minimum>': 0.0,
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'm'}),
                                     (u'hydronic tubing outside diameter',
                                      {'name': u'Hydronic Tubing Outside Diameter',
                                       'pyname': u'hydronic_tubing_outside_diameter',
                                       'minimum>': 0.0,
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'm'}),
                                     (u'hydronic tubing thermal conductivity',
                                      {'name': u'Hydronic Tubing Thermal Conductivity',
                                       'pyname': u'hydronic_tubing_thermal_conductivity',
                                       'minimum>': 0.0,
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'W/m-K'}),
                                     (u'ground thermal conductivity',
                                      {'name': u'Ground Thermal Conductivity',
                                       'pyname': u'ground_thermal_conductivity',
                                       'minimum>': 0.0,
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'W/m2-K'}),
                                     (u'number of tubing circuits',
                                      {'name': u'Number of Tubing Circuits',
                                       'pyname': u'number_of_tubing_circuits',
                                       'required-field': True,
                                       'autosizable': False,
                                       'minimum': 1,
                                       'autocalculatable': False,
                                       'type': u'integer'}),
                                     (u'length of each tubing circuit',
                                      {'name': u'Length of Each Tubing Circuit',
                                       'pyname': u'length_of_each_tubing_circuit',
                                       'required-field': True,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'm'})]),
              'format': None,
              'group': u'Condenser Equipment and Heat Exchangers',
              'min-fields': 0,
              'name': u'GroundHeatExchanger:Pond',
              'pyname': u'GroundHeatExchangerPond',
              'required-object': False,
              'unique-object': False}

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
    def fluid_inlet_node_name(self):
        """Get fluid_inlet_node_name.

        Returns:
            str: the value of `fluid_inlet_node_name` or None if not set

        """
        return self["Fluid Inlet Node Name"]

    @fluid_inlet_node_name.setter
    def fluid_inlet_node_name(self, value=None):
        """Corresponds to IDD field `Fluid Inlet Node Name`

        Args:
            value (str): value for IDD Field `Fluid Inlet Node Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Fluid Inlet Node Name"] = value

    @property
    def fluid_outlet_node_name(self):
        """Get fluid_outlet_node_name.

        Returns:
            str: the value of `fluid_outlet_node_name` or None if not set

        """
        return self["Fluid Outlet Node Name"]

    @fluid_outlet_node_name.setter
    def fluid_outlet_node_name(self, value=None):
        """Corresponds to IDD field `Fluid Outlet Node Name`

        Args:
            value (str): value for IDD Field `Fluid Outlet Node Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Fluid Outlet Node Name"] = value

    @property
    def pond_depth(self):
        """Get pond_depth.

        Returns:
            float: the value of `pond_depth` or None if not set

        """
        return self["Pond Depth"]

    @pond_depth.setter
    def pond_depth(self, value=None):
        """Corresponds to IDD field `Pond Depth`

        Args:
            value (float): value for IDD Field `Pond Depth`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Pond Depth"] = value

    @property
    def pond_area(self):
        """Get pond_area.

        Returns:
            float: the value of `pond_area` or None if not set

        """
        return self["Pond Area"]

    @pond_area.setter
    def pond_area(self, value=None):
        """Corresponds to IDD field `Pond Area`

        Args:
            value (float): value for IDD Field `Pond Area`
                Units: m2
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Pond Area"] = value

    @property
    def hydronic_tubing_inside_diameter(self):
        """Get hydronic_tubing_inside_diameter.

        Returns:
            float: the value of `hydronic_tubing_inside_diameter` or None if not set

        """
        return self["Hydronic Tubing Inside Diameter"]

    @hydronic_tubing_inside_diameter.setter
    def hydronic_tubing_inside_diameter(self, value=None):
        """Corresponds to IDD field `Hydronic Tubing Inside Diameter`

        Args:
            value (float): value for IDD Field `Hydronic Tubing Inside Diameter`
                Units: m
                IP-Units: in
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Hydronic Tubing Inside Diameter"] = value

    @property
    def hydronic_tubing_outside_diameter(self):
        """Get hydronic_tubing_outside_diameter.

        Returns:
            float: the value of `hydronic_tubing_outside_diameter` or None if not set

        """
        return self["Hydronic Tubing Outside Diameter"]

    @hydronic_tubing_outside_diameter.setter
    def hydronic_tubing_outside_diameter(self, value=None):
        """Corresponds to IDD field `Hydronic Tubing Outside Diameter`

        Args:
            value (float): value for IDD Field `Hydronic Tubing Outside Diameter`
                Units: m
                IP-Units: in
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Hydronic Tubing Outside Diameter"] = value

    @property
    def hydronic_tubing_thermal_conductivity(self):
        """Get hydronic_tubing_thermal_conductivity.

        Returns:
            float: the value of `hydronic_tubing_thermal_conductivity` or None if not set

        """
        return self["Hydronic Tubing Thermal Conductivity"]

    @hydronic_tubing_thermal_conductivity.setter
    def hydronic_tubing_thermal_conductivity(self, value=None):
        """Corresponds to IDD field `Hydronic Tubing Thermal Conductivity`

        Args:
            value (float): value for IDD Field `Hydronic Tubing Thermal Conductivity`
                Units: W/m-K
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Hydronic Tubing Thermal Conductivity"] = value

    @property
    def ground_thermal_conductivity(self):
        """Get ground_thermal_conductivity.

        Returns:
            float: the value of `ground_thermal_conductivity` or None if not set

        """
        return self["Ground Thermal Conductivity"]

    @ground_thermal_conductivity.setter
    def ground_thermal_conductivity(self, value=None):
        """Corresponds to IDD field `Ground Thermal Conductivity`

        Args:
            value (float): value for IDD Field `Ground Thermal Conductivity`
                Units: W/m2-K
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Ground Thermal Conductivity"] = value

    @property
    def number_of_tubing_circuits(self):
        """Get number_of_tubing_circuits.

        Returns:
            int: the value of `number_of_tubing_circuits` or None if not set

        """
        return self["Number of Tubing Circuits"]

    @number_of_tubing_circuits.setter
    def number_of_tubing_circuits(self, value=None):
        """Corresponds to IDD field `Number of Tubing Circuits`

        Args:
            value (int): value for IDD Field `Number of Tubing Circuits`
                value >= 1
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Number of Tubing Circuits"] = value

    @property
    def length_of_each_tubing_circuit(self):
        """Get length_of_each_tubing_circuit.

        Returns:
            float: the value of `length_of_each_tubing_circuit` or None if not set

        """
        return self["Length of Each Tubing Circuit"]

    @length_of_each_tubing_circuit.setter
    def length_of_each_tubing_circuit(self, value=None):
        """Corresponds to IDD field `Length of Each Tubing Circuit`

        Args:
            value (float): value for IDD Field `Length of Each Tubing Circuit`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Length of Each Tubing Circuit"] = value




class GroundHeatExchangerSurface(DataObject):

    """ Corresponds to IDD object `GroundHeatExchanger:Surface`
        A hydronic surface/panel consisting of a multi-layer construction with embedded rows of tubes.
        Typically used in hybrid geothermal systems and included in the condenser loop.
        This component may also be used as a simple solar collector.
        The bottom surface may be defined as ground-coupled or exposed to wind (eg. bridge deck).
    """
    schema = {'extensible-fields': OrderedDict(),
              'fields': OrderedDict([(u'name',
                                      {'name': u'Name',
                                       'pyname': u'name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'construction name',
                                      {'name': u'Construction Name',
                                       'pyname': u'construction_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'fluid inlet node name',
                                      {'name': u'Fluid Inlet Node Name',
                                       'pyname': u'fluid_inlet_node_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'node'}),
                                     (u'fluid outlet node name',
                                      {'name': u'Fluid Outlet Node Name',
                                       'pyname': u'fluid_outlet_node_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'node'}),
                                     (u'hydronic tubing inside diameter',
                                      {'name': u'Hydronic Tubing Inside Diameter',
                                       'pyname': u'hydronic_tubing_inside_diameter',
                                       'minimum>': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'm'}),
                                     (u'number of tubing circuits',
                                      {'name': u'Number of Tubing Circuits',
                                       'pyname': u'number_of_tubing_circuits',
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 1,
                                       'autocalculatable': False,
                                       'type': u'integer'}),
                                     (u'hydronic tube spacing',
                                      {'name': u'Hydronic Tube Spacing',
                                       'pyname': u'hydronic_tube_spacing',
                                       'minimum>': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'm'}),
                                     (u'surface length',
                                      {'name': u'Surface Length',
                                       'pyname': u'surface_length',
                                       'minimum>': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'm'}),
                                     (u'surface width',
                                      {'name': u'Surface Width',
                                       'pyname': u'surface_width',
                                       'minimum>': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'm'}),
                                     (u'lower surface environment',
                                      {'name': u'Lower Surface Environment',
                                       'pyname': u'lower_surface_environment',
                                       'default': u'Ground',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'Ground',
                                                           u'Exposed'],
                                       'autocalculatable': False,
                                       'type': 'alpha'})]),
              'format': None,
              'group': u'Condenser Equipment and Heat Exchangers',
              'min-fields': 0,
              'name': u'GroundHeatExchanger:Surface',
              'pyname': u'GroundHeatExchangerSurface',
              'required-object': False,
              'unique-object': False}

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
    def construction_name(self):
        """Get construction_name.

        Returns:
            str: the value of `construction_name` or None if not set

        """
        return self["Construction Name"]

    @construction_name.setter
    def construction_name(self, value=None):
        """Corresponds to IDD field `Construction Name`

        Args:
            value (str): value for IDD Field `Construction Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Construction Name"] = value

    @property
    def fluid_inlet_node_name(self):
        """Get fluid_inlet_node_name.

        Returns:
            str: the value of `fluid_inlet_node_name` or None if not set

        """
        return self["Fluid Inlet Node Name"]

    @fluid_inlet_node_name.setter
    def fluid_inlet_node_name(self, value=None):
        """Corresponds to IDD field `Fluid Inlet Node Name`

        Args:
            value (str): value for IDD Field `Fluid Inlet Node Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Fluid Inlet Node Name"] = value

    @property
    def fluid_outlet_node_name(self):
        """Get fluid_outlet_node_name.

        Returns:
            str: the value of `fluid_outlet_node_name` or None if not set

        """
        return self["Fluid Outlet Node Name"]

    @fluid_outlet_node_name.setter
    def fluid_outlet_node_name(self, value=None):
        """Corresponds to IDD field `Fluid Outlet Node Name`

        Args:
            value (str): value for IDD Field `Fluid Outlet Node Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Fluid Outlet Node Name"] = value

    @property
    def hydronic_tubing_inside_diameter(self):
        """Get hydronic_tubing_inside_diameter.

        Returns:
            float: the value of `hydronic_tubing_inside_diameter` or None if not set

        """
        return self["Hydronic Tubing Inside Diameter"]

    @hydronic_tubing_inside_diameter.setter
    def hydronic_tubing_inside_diameter(self, value=None):
        """Corresponds to IDD field `Hydronic Tubing Inside Diameter`

        Args:
            value (float): value for IDD Field `Hydronic Tubing Inside Diameter`
                Units: m
                IP-Units: in
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Hydronic Tubing Inside Diameter"] = value

    @property
    def number_of_tubing_circuits(self):
        """Get number_of_tubing_circuits.

        Returns:
            int: the value of `number_of_tubing_circuits` or None if not set

        """
        return self["Number of Tubing Circuits"]

    @number_of_tubing_circuits.setter
    def number_of_tubing_circuits(self, value=None):
        """Corresponds to IDD field `Number of Tubing Circuits`

        Args:
            value (int): value for IDD Field `Number of Tubing Circuits`
                value >= 1
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Number of Tubing Circuits"] = value

    @property
    def hydronic_tube_spacing(self):
        """Get hydronic_tube_spacing.

        Returns:
            float: the value of `hydronic_tube_spacing` or None if not set

        """
        return self["Hydronic Tube Spacing"]

    @hydronic_tube_spacing.setter
    def hydronic_tube_spacing(self, value=None):
        """Corresponds to IDD field `Hydronic Tube Spacing`

        Args:
            value (float): value for IDD Field `Hydronic Tube Spacing`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Hydronic Tube Spacing"] = value

    @property
    def surface_length(self):
        """Get surface_length.

        Returns:
            float: the value of `surface_length` or None if not set

        """
        return self["Surface Length"]

    @surface_length.setter
    def surface_length(self, value=None):
        """Corresponds to IDD field `Surface Length`

        Args:
            value (float): value for IDD Field `Surface Length`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Surface Length"] = value

    @property
    def surface_width(self):
        """Get surface_width.

        Returns:
            float: the value of `surface_width` or None if not set

        """
        return self["Surface Width"]

    @surface_width.setter
    def surface_width(self, value=None):
        """Corresponds to IDD field `Surface Width`

        Args:
            value (float): value for IDD Field `Surface Width`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Surface Width"] = value

    @property
    def lower_surface_environment(self):
        """Get lower_surface_environment.

        Returns:
            str: the value of `lower_surface_environment` or None if not set

        """
        return self["Lower Surface Environment"]

    @lower_surface_environment.setter
    def lower_surface_environment(self, value="Ground"):
        """Corresponds to IDD field `Lower Surface Environment`

        Args:
            value (str): value for IDD Field `Lower Surface Environment`
                Default value: Ground
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Lower Surface Environment"] = value




class GroundHeatExchangerHorizontalTrench(DataObject):

    """ Corresponds to IDD object `GroundHeatExchanger:HorizontalTrench`
        This models a horizontal heat exchanger placed in a series of trenches
        The model uses the PipingSystem:Underground underlying algorithms,
        but provides a more usable input interface.
    """
    schema = {'extensible-fields': OrderedDict(),
              'fields': OrderedDict([(u'name',
                                      {'name': u'Name',
                                       'pyname': u'name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'inlet node name',
                                      {'name': u'Inlet Node Name',
                                       'pyname': u'inlet_node_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'node'}),
                                     (u'outlet node name',
                                      {'name': u'Outlet Node Name',
                                       'pyname': u'outlet_node_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'node'}),
                                     (u'design flow rate',
                                      {'name': u'Design Flow Rate',
                                       'pyname': u'design_flow_rate',
                                       'minimum>': 0.0,
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'm3/s'}),
                                     (u'trench length in pipe axial direction',
                                      {'name': u'Trench Length in Pipe Axial Direction',
                                       'pyname': u'trench_length_in_pipe_axial_direction',
                                       'default': 50.0,
                                       'minimum>': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'm'}),
                                     (u'number of trenches',
                                      {'name': u'Number of Trenches',
                                       'pyname': u'number_of_trenches',
                                       'default': 1,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 1,
                                       'autocalculatable': False,
                                       'type': u'integer'}),
                                     (u'horizontal spacing between pipes',
                                      {'name': u'Horizontal Spacing Between Pipes',
                                       'pyname': u'horizontal_spacing_between_pipes',
                                       'default': 1.0,
                                       'minimum>': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'm'}),
                                     (u'pipe inner diameter',
                                      {'name': u'Pipe Inner Diameter',
                                       'pyname': u'pipe_inner_diameter',
                                       'default': 0.016,
                                       'minimum>': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'm'}),
                                     (u'pipe outer diameter',
                                      {'name': u'Pipe Outer Diameter',
                                       'pyname': u'pipe_outer_diameter',
                                       'default': 0.026,
                                       'minimum>': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'm'}),
                                     (u'burial depth',
                                      {'name': u'Burial Depth',
                                       'pyname': u'burial_depth',
                                       'default': 1.5,
                                       'minimum>': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'm'}),
                                     (u'soil thermal conductivity',
                                      {'name': u'Soil Thermal Conductivity',
                                       'pyname': u'soil_thermal_conductivity',
                                       'default': 1.08,
                                       'minimum>': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'W/m-K'}),
                                     (u'soil density',
                                      {'name': u'Soil Density',
                                       'pyname': u'soil_density',
                                       'default': 962.0,
                                       'minimum>': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'kg/m3'}),
                                     (u'soil specific heat',
                                      {'name': u'Soil Specific Heat',
                                       'pyname': u'soil_specific_heat',
                                       'default': 2576.0,
                                       'minimum>': 0.0,
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'J/kg-K'}),
                                     (u'pipe thermal conductivity',
                                      {'name': u'Pipe Thermal Conductivity',
                                       'pyname': u'pipe_thermal_conductivity',
                                       'default': 0.3895,
                                       'minimum>': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'W/m-K'}),
                                     (u'pipe density',
                                      {'name': u'Pipe Density',
                                       'pyname': u'pipe_density',
                                       'default': 641.0,
                                       'minimum>': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'kg/m3'}),
                                     (u'pipe specific heat',
                                      {'name': u'Pipe Specific Heat',
                                       'pyname': u'pipe_specific_heat',
                                       'default': 2405.0,
                                       'minimum>': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'J/kg-K'}),
                                     (u'soil moisture content percent',
                                      {'name': u'Soil Moisture Content Percent',
                                       'pyname': u'soil_moisture_content_percent',
                                       'default': 30.0,
                                       'maximum': 100.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'percent'}),
                                     (u'soil moisture content percent at saturation',
                                      {'name': u'Soil Moisture Content Percent at Saturation',
                                       'pyname': u'soil_moisture_content_percent_at_saturation',
                                       'default': 50.0,
                                       'maximum': 100.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'percent'}),
                                     (u'kusuda-achenbach average surface temperature',
                                      {'name': u'Kusuda-Achenbach Average Surface Temperature',
                                       'pyname': u'kusudaachenbach_average_surface_temperature',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'C'}),
                                     (u'kusuda-achenbach average amplitude of surface temperature',
                                      {'name': u'Kusuda-Achenbach Average Amplitude of Surface Temperature',
                                       'pyname': u'kusudaachenbach_average_amplitude_of_surface_temperature',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'C'}),
                                     (u'kusuda-achenbach phase shift of minimum surface temperature',
                                      {'name': u'Kusuda-Achenbach Phase Shift of Minimum Surface Temperature',
                                       'pyname': u'kusudaachenbach_phase_shift_of_minimum_surface_temperature',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'days'}),
                                     (u'evapotranspiration ground cover parameter',
                                      {'name': u'Evapotranspiration Ground Cover Parameter',
                                       'pyname': u'evapotranspiration_ground_cover_parameter',
                                       'default': 0.4,
                                       'maximum': 1.5,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': u'real'})]),
              'format': None,
              'group': u'Condenser Equipment and Heat Exchangers',
              'min-fields': 0,
              'name': u'GroundHeatExchanger:HorizontalTrench',
              'pyname': u'GroundHeatExchangerHorizontalTrench',
              'required-object': False,
              'unique-object': False}

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
    def inlet_node_name(self):
        """Get inlet_node_name.

        Returns:
            str: the value of `inlet_node_name` or None if not set

        """
        return self["Inlet Node Name"]

    @inlet_node_name.setter
    def inlet_node_name(self, value=None):
        """Corresponds to IDD field `Inlet Node Name`

        Args:
            value (str): value for IDD Field `Inlet Node Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Inlet Node Name"] = value

    @property
    def outlet_node_name(self):
        """Get outlet_node_name.

        Returns:
            str: the value of `outlet_node_name` or None if not set

        """
        return self["Outlet Node Name"]

    @outlet_node_name.setter
    def outlet_node_name(self, value=None):
        """Corresponds to IDD field `Outlet Node Name`

        Args:
            value (str): value for IDD Field `Outlet Node Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Outlet Node Name"] = value

    @property
    def design_flow_rate(self):
        """Get design_flow_rate.

        Returns:
            float: the value of `design_flow_rate` or None if not set

        """
        return self["Design Flow Rate"]

    @design_flow_rate.setter
    def design_flow_rate(self, value=None):
        """Corresponds to IDD field `Design Flow Rate`

        Args:
            value (float): value for IDD Field `Design Flow Rate`
                Units: m3/s
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Design Flow Rate"] = value

    @property
    def trench_length_in_pipe_axial_direction(self):
        """Get trench_length_in_pipe_axial_direction.

        Returns:
            float: the value of `trench_length_in_pipe_axial_direction` or None if not set

        """
        return self["Trench Length in Pipe Axial Direction"]

    @trench_length_in_pipe_axial_direction.setter
    def trench_length_in_pipe_axial_direction(self, value=50.0):
        """Corresponds to IDD field `Trench Length in Pipe Axial Direction`
        This is the total pipe axial length of the heat exchanger If all pipe
        trenches are parallel, this is the length of a single trench.  If a
        single, long run of pipe is used with one trench, this is the full
        length of the pipe run.

        Args:
            value (float): value for IDD Field `Trench Length in Pipe Axial Direction`
                Units: m
                IP-Units: ft
                Default value: 50.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Trench Length in Pipe Axial Direction"] = value

    @property
    def number_of_trenches(self):
        """Get number_of_trenches.

        Returns:
            int: the value of `number_of_trenches` or None if not set

        """
        return self["Number of Trenches"]

    @number_of_trenches.setter
    def number_of_trenches(self, value=1):
        """Corresponds to IDD field `Number of Trenches` This is the number of
        horizontal legs that will be used in the entire heat exchanger, one
        pipe per trench.

        Args:
            value (int): value for IDD Field `Number of Trenches`
                Default value: 1
                value >= 1
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Number of Trenches"] = value

    @property
    def horizontal_spacing_between_pipes(self):
        """Get horizontal_spacing_between_pipes.

        Returns:
            float: the value of `horizontal_spacing_between_pipes` or None if not set

        """
        return self["Horizontal Spacing Between Pipes"]

    @horizontal_spacing_between_pipes.setter
    def horizontal_spacing_between_pipes(self, value=1.0):
        """Corresponds to IDD field `Horizontal Spacing Between Pipes` This
        represents the average horizontal spacing between any two trenches for
        heat exchangers that have multiple trenches.

        Args:
            value (float): value for IDD Field `Horizontal Spacing Between Pipes`
                Units: m
                Default value: 1.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Horizontal Spacing Between Pipes"] = value

    @property
    def pipe_inner_diameter(self):
        """Get pipe_inner_diameter.

        Returns:
            float: the value of `pipe_inner_diameter` or None if not set

        """
        return self["Pipe Inner Diameter"]

    @pipe_inner_diameter.setter
    def pipe_inner_diameter(self, value=0.016):
        """Corresponds to IDD field `Pipe Inner Diameter`

        Args:
            value (float): value for IDD Field `Pipe Inner Diameter`
                Units: m
                IP-Units: in
                Default value: 0.016
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Pipe Inner Diameter"] = value

    @property
    def pipe_outer_diameter(self):
        """Get pipe_outer_diameter.

        Returns:
            float: the value of `pipe_outer_diameter` or None if not set

        """
        return self["Pipe Outer Diameter"]

    @pipe_outer_diameter.setter
    def pipe_outer_diameter(self, value=0.026):
        """Corresponds to IDD field `Pipe Outer Diameter`

        Args:
            value (float): value for IDD Field `Pipe Outer Diameter`
                Units: m
                IP-Units: in
                Default value: 0.026
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Pipe Outer Diameter"] = value

    @property
    def burial_depth(self):
        """Get burial_depth.

        Returns:
            float: the value of `burial_depth` or None if not set

        """
        return self["Burial Depth"]

    @burial_depth.setter
    def burial_depth(self, value=1.5):
        """Corresponds to IDD field `Burial Depth` This is the burial depth of
        the pipes, or the trenches containing the pipes.

        Args:
            value (float): value for IDD Field `Burial Depth`
                Units: m
                IP-Units: ft
                Default value: 1.5
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Burial Depth"] = value

    @property
    def soil_thermal_conductivity(self):
        """Get soil_thermal_conductivity.

        Returns:
            float: the value of `soil_thermal_conductivity` or None if not set

        """
        return self["Soil Thermal Conductivity"]

    @soil_thermal_conductivity.setter
    def soil_thermal_conductivity(self, value=1.08):
        """Corresponds to IDD field `Soil Thermal Conductivity`

        Args:
            value (float): value for IDD Field `Soil Thermal Conductivity`
                Units: W/m-K
                Default value: 1.08
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Soil Thermal Conductivity"] = value

    @property
    def soil_density(self):
        """Get soil_density.

        Returns:
            float: the value of `soil_density` or None if not set

        """
        return self["Soil Density"]

    @soil_density.setter
    def soil_density(self, value=962.0):
        """Corresponds to IDD field `Soil Density`

        Args:
            value (float): value for IDD Field `Soil Density`
                Units: kg/m3
                Default value: 962.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Soil Density"] = value

    @property
    def soil_specific_heat(self):
        """Get soil_specific_heat.

        Returns:
            float: the value of `soil_specific_heat` or None if not set

        """
        return self["Soil Specific Heat"]

    @soil_specific_heat.setter
    def soil_specific_heat(self, value=2576.0):
        """Corresponds to IDD field `Soil Specific Heat`

        Args:
            value (float): value for IDD Field `Soil Specific Heat`
                Units: J/kg-K
                Default value: 2576.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Soil Specific Heat"] = value

    @property
    def pipe_thermal_conductivity(self):
        """Get pipe_thermal_conductivity.

        Returns:
            float: the value of `pipe_thermal_conductivity` or None if not set

        """
        return self["Pipe Thermal Conductivity"]

    @pipe_thermal_conductivity.setter
    def pipe_thermal_conductivity(self, value=0.3895):
        """Corresponds to IDD field `Pipe Thermal Conductivity`

        Args:
            value (float): value for IDD Field `Pipe Thermal Conductivity`
                Units: W/m-K
                Default value: 0.3895
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Pipe Thermal Conductivity"] = value

    @property
    def pipe_density(self):
        """Get pipe_density.

        Returns:
            float: the value of `pipe_density` or None if not set

        """
        return self["Pipe Density"]

    @pipe_density.setter
    def pipe_density(self, value=641.0):
        """Corresponds to IDD field `Pipe Density`

        Args:
            value (float): value for IDD Field `Pipe Density`
                Units: kg/m3
                Default value: 641.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Pipe Density"] = value

    @property
    def pipe_specific_heat(self):
        """Get pipe_specific_heat.

        Returns:
            float: the value of `pipe_specific_heat` or None if not set

        """
        return self["Pipe Specific Heat"]

    @pipe_specific_heat.setter
    def pipe_specific_heat(self, value=2405.0):
        """Corresponds to IDD field `Pipe Specific Heat`

        Args:
            value (float): value for IDD Field `Pipe Specific Heat`
                Units: J/kg-K
                Default value: 2405.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Pipe Specific Heat"] = value

    @property
    def soil_moisture_content_percent(self):
        """Get soil_moisture_content_percent.

        Returns:
            float: the value of `soil_moisture_content_percent` or None if not set

        """
        return self["Soil Moisture Content Percent"]

    @soil_moisture_content_percent.setter
    def soil_moisture_content_percent(self, value=30.0):
        """Corresponds to IDD field `Soil Moisture Content Percent`

        Args:
            value (float): value for IDD Field `Soil Moisture Content Percent`
                Units: percent
                Default value: 30.0
                value <= 100.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Soil Moisture Content Percent"] = value

    @property
    def soil_moisture_content_percent_at_saturation(self):
        """Get soil_moisture_content_percent_at_saturation.

        Returns:
            float: the value of `soil_moisture_content_percent_at_saturation` or None if not set

        """
        return self["Soil Moisture Content Percent at Saturation"]

    @soil_moisture_content_percent_at_saturation.setter
    def soil_moisture_content_percent_at_saturation(self, value=50.0):
        """Corresponds to IDD field `Soil Moisture Content Percent at
        Saturation`

        Args:
            value (float): value for IDD Field `Soil Moisture Content Percent at Saturation`
                Units: percent
                Default value: 50.0
                value <= 100.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Soil Moisture Content Percent at Saturation"] = value

    @property
    def kusudaachenbach_average_surface_temperature(self):
        """Get kusudaachenbach_average_surface_temperature.

        Returns:
            float: the value of `kusudaachenbach_average_surface_temperature` or None if not set

        """
        return self["Kusuda-Achenbach Average Surface Temperature"]

    @kusudaachenbach_average_surface_temperature.setter
    def kusudaachenbach_average_surface_temperature(self, value=None):
        """  Corresponds to IDD field `Kusuda-Achenbach Average Surface Temperature`
        This is the parameter for average annual surface temperature
        This is an optional input in that if it is missing, a
        Site:GroundTemperature:Shallow object must be found in the input
        The undisturbed ground temperature will be approximated from this object

        Args:
            value (float): value for IDD Field `Kusuda-Achenbach Average Surface Temperature`
                Units: C
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Kusuda-Achenbach Average Surface Temperature"] = value

    @property
    def kusudaachenbach_average_amplitude_of_surface_temperature(self):
        """Get kusudaachenbach_average_amplitude_of_surface_temperature.

        Returns:
            float: the value of `kusudaachenbach_average_amplitude_of_surface_temperature` or None if not set

        """
        return self[
            "Kusuda-Achenbach Average Amplitude of Surface Temperature"]

    @kusudaachenbach_average_amplitude_of_surface_temperature.setter
    def kusudaachenbach_average_amplitude_of_surface_temperature(
            self,
            value=None):
        """  Corresponds to IDD field `Kusuda-Achenbach Average Amplitude of Surface Temperature`
        This is the parameter for annual average amplitude from average surface temperature
        This is an optional input in that if it is missing, a
        Site:GroundTemperature:Shallow object must be found in the input
        The undisturbed ground temperature will be approximated from this object

        Args:
            value (float): value for IDD Field `Kusuda-Achenbach Average Amplitude of Surface Temperature`
                Units: C
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self[
            "Kusuda-Achenbach Average Amplitude of Surface Temperature"] = value

    @property
    def kusudaachenbach_phase_shift_of_minimum_surface_temperature(self):
        """Get kusudaachenbach_phase_shift_of_minimum_surface_temperature.

        Returns:
            float: the value of `kusudaachenbach_phase_shift_of_minimum_surface_temperature` or None if not set

        """
        return self[
            "Kusuda-Achenbach Phase Shift of Minimum Surface Temperature"]

    @kusudaachenbach_phase_shift_of_minimum_surface_temperature.setter
    def kusudaachenbach_phase_shift_of_minimum_surface_temperature(
            self,
            value=None):
        """  Corresponds to IDD field `Kusuda-Achenbach Phase Shift of Minimum Surface Temperature`
        This is the parameter for phase shift from minimum surface temperature
        This is an optional input in that if it is missing, a
        Site:GroundTemperature:Shallow object must be found in the input
        The undisturbed ground temperature will be approximated from this object

        Args:
            value (float): value for IDD Field `Kusuda-Achenbach Phase Shift of Minimum Surface Temperature`
                Units: days
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self[
            "Kusuda-Achenbach Phase Shift of Minimum Surface Temperature"] = value

    @property
    def evapotranspiration_ground_cover_parameter(self):
        """Get evapotranspiration_ground_cover_parameter.

        Returns:
            float: the value of `evapotranspiration_ground_cover_parameter` or None if not set

        """
        return self["Evapotranspiration Ground Cover Parameter"]

    @evapotranspiration_ground_cover_parameter.setter
    def evapotranspiration_ground_cover_parameter(self, value=0.4):
        """  Corresponds to IDD field `Evapotranspiration Ground Cover Parameter`
        This specifies the ground cover effects during evapotranspiration
        calculations.  The value roughly represents the following cases:
        = 0   : concrete or other solid, non-permeable ground surface material
        = 0.5 : short grass, much like a manicured lawn
        = 1   : standard reference state (12 cm grass)
        = 1.5 : wild growth

        Args:
            value (float): value for IDD Field `Evapotranspiration Ground Cover Parameter`
                Default value: 0.4
                value <= 1.5
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Evapotranspiration Ground Cover Parameter"] = value




class HeatExchangerFluidToFluid(DataObject):

    """ Corresponds to IDD object `HeatExchanger:FluidToFluid`
        A fluid/fluid heat exchanger designed to couple the supply side of one loop to the demand side of another loop
        Loops can be either plant or condenser loops but no air side connections are allowed
    """
    schema = {'extensible-fields': OrderedDict(),
              'fields': OrderedDict([(u'name',
                                      {'name': u'Name',
                                       'pyname': u'name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'availability schedule name',
                                      {'name': u'Availability Schedule Name',
                                       'pyname': u'availability_schedule_name',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'loop demand side inlet node name',
                                      {'name': u'Loop Demand Side Inlet Node Name',
                                       'pyname': u'loop_demand_side_inlet_node_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'node'}),
                                     (u'loop demand side outlet node name',
                                      {'name': u'Loop Demand Side Outlet Node Name',
                                       'pyname': u'loop_demand_side_outlet_node_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'node'}),
                                     (u'loop demand side design flow rate',
                                      {'name': u'Loop Demand Side Design Flow Rate',
                                       'pyname': u'loop_demand_side_design_flow_rate',
                                       'minimum>': 0.0,
                                       'required-field': True,
                                       'autosizable': True,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'm3/s'}),
                                     (u'loop supply side inlet node name',
                                      {'name': u'Loop Supply Side Inlet Node Name',
                                       'pyname': u'loop_supply_side_inlet_node_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'node'}),
                                     (u'loop supply side outlet node name',
                                      {'name': u'Loop Supply Side Outlet Node Name',
                                       'pyname': u'loop_supply_side_outlet_node_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'node'}),
                                     (u'loop supply side design flow rate',
                                      {'name': u'Loop Supply Side Design Flow Rate',
                                       'pyname': u'loop_supply_side_design_flow_rate',
                                       'minimum>': 0.0,
                                       'required-field': True,
                                       'autosizable': True,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'm3/s'}),
                                     (u'heat exchange model type',
                                      {'name': u'Heat Exchange Model Type',
                                       'pyname': u'heat_exchange_model_type',
                                       'default': u'Ideal',
                                       'required-field': True,
                                       'autosizable': False,
                                       'accepted-values': [u'CrossFlowBothUnMixed',
                                                           u'CrossFlowBothMixed',
                                                           u'CrossFlowSupplyMixedDemandUnMixed',
                                                           u'CrossFlowSupplyUnMixedDemandMixed',
                                                           u'ParallelFlow',
                                                           u'CounterFlow',
                                                           u'Ideal'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'heat exchanger u-factor times area value',
                                      {'name': u'Heat Exchanger U-Factor Times Area Value',
                                       'pyname': u'heat_exchanger_ufactor_times_area_value',
                                       'minimum>': 0.0,
                                       'required-field': True,
                                       'autosizable': True,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'W/k'}),
                                     (u'control type',
                                      {'name': u'Control Type',
                                       'pyname': u'control_type',
                                       'default': u'UncontrolledOn',
                                       'required-field': True,
                                       'autosizable': False,
                                       'accepted-values': [u'UncontrolledOn',
                                                           u'OperationSchemeModulated',
                                                           u'OperationSchemeOnOff',
                                                           u'HeatingSetpointModulated',
                                                           u'HeatingSetpointOnOff',
                                                           u'CoolingSetpointModulated',
                                                           u'CoolingSetpointOnOff',
                                                           u'DualDeadbandSetpointModulated',
                                                           u'DualDeadbandSetpointOnOff',
                                                           u'CoolingDifferentialOnOff',
                                                           u'CoolingSetpointOnOffWithComponentOverride'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'heat exchanger setpoint node name',
                                      {'name': u'Heat Exchanger Setpoint Node Name',
                                       'pyname': u'heat_exchanger_setpoint_node_name',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'node'}),
                                     (u'minimum temperature difference to activate heat exchanger',
                                      {'name': u'Minimum Temperature Difference to Activate Heat Exchanger',
                                       'pyname': u'minimum_temperature_difference_to_activate_heat_exchanger',
                                       'default': 0.01,
                                       'maximum': 50.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'deltaC'}),
                                     (u'heat transfer metering end use type',
                                      {'name': u'Heat Transfer Metering End Use Type',
                                       'pyname': u'heat_transfer_metering_end_use_type',
                                       'default': u'LoopToLoop',
                                       'required-field': True,
                                       'autosizable': False,
                                       'accepted-values': [u'FreeCooling',
                                                           u'HeatRecovery',
                                                           u'HeatRejection',
                                                           u'HeatRecoveryForCooling',
                                                           u'HeatRecoveryForHeating',
                                                           u'LoopToLoop'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'component override loop supply side inlet node name',
                                      {'name': u'Component Override Loop Supply Side Inlet Node Name',
                                       'pyname': u'component_override_loop_supply_side_inlet_node_name',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'node'}),
                                     (u'component override loop demand side inlet node name',
                                      {'name': u'Component Override Loop Demand Side Inlet Node Name',
                                       'pyname': u'component_override_loop_demand_side_inlet_node_name',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'node'}),
                                     (u'component override cooling control temperature mode',
                                      {'name': u'Component Override Cooling Control Temperature Mode',
                                       'pyname': u'component_override_cooling_control_temperature_mode',
                                       'default': u'Loop',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'WetBulbTemperature',
                                                           u'DryBulbTemperature',
                                                           u'Loop'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'sizing factor',
                                      {'name': u'Sizing Factor',
                                       'pyname': u'sizing_factor',
                                       'default': 1.0,
                                       'minimum>': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'operation minimum temperature limit',
                                      {'name': u'Operation Minimum Temperature Limit',
                                       'pyname': u'operation_minimum_temperature_limit',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'C'}),
                                     (u'operation maximum temperature limit',
                                      {'name': u'Operation Maximum Temperature Limit',
                                       'pyname': u'operation_maximum_temperature_limit',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'C'})]),
              'format': None,
              'group': u'Condenser Equipment and Heat Exchangers',
              'min-fields': 14,
              'name': u'HeatExchanger:FluidToFluid',
              'pyname': u'HeatExchangerFluidToFluid',
              'required-object': False,
              'unique-object': False}

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
    def availability_schedule_name(self):
        """Get availability_schedule_name.

        Returns:
            str: the value of `availability_schedule_name` or None if not set

        """
        return self["Availability Schedule Name"]

    @availability_schedule_name.setter
    def availability_schedule_name(self, value=None):
        """Corresponds to IDD field `Availability Schedule Name` Availability
        schedule name for this system. Schedule value > 0 means the system is
        available. If this field is blank, the system is always available.
        default is that heat exchanger is on.

        Args:
            value (str): value for IDD Field `Availability Schedule Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Availability Schedule Name"] = value

    @property
    def loop_demand_side_inlet_node_name(self):
        """Get loop_demand_side_inlet_node_name.

        Returns:
            str: the value of `loop_demand_side_inlet_node_name` or None if not set

        """
        return self["Loop Demand Side Inlet Node Name"]

    @loop_demand_side_inlet_node_name.setter
    def loop_demand_side_inlet_node_name(self, value=None):
        """Corresponds to IDD field `Loop Demand Side Inlet Node Name` This
        connection is to the demand side of a loop and is the inlet to the heat
        exchanger.

        Args:
            value (str): value for IDD Field `Loop Demand Side Inlet Node Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Loop Demand Side Inlet Node Name"] = value

    @property
    def loop_demand_side_outlet_node_name(self):
        """Get loop_demand_side_outlet_node_name.

        Returns:
            str: the value of `loop_demand_side_outlet_node_name` or None if not set

        """
        return self["Loop Demand Side Outlet Node Name"]

    @loop_demand_side_outlet_node_name.setter
    def loop_demand_side_outlet_node_name(self, value=None):
        """Corresponds to IDD field `Loop Demand Side Outlet Node Name` This
        connection is to the demand side of a loop.

        Args:
            value (str): value for IDD Field `Loop Demand Side Outlet Node Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Loop Demand Side Outlet Node Name"] = value

    @property
    def loop_demand_side_design_flow_rate(self):
        """Get loop_demand_side_design_flow_rate.

        Returns:
            float: the value of `loop_demand_side_design_flow_rate` or None if not set

        """
        return self["Loop Demand Side Design Flow Rate"]

    @loop_demand_side_design_flow_rate.setter
    def loop_demand_side_design_flow_rate(self, value=None):
        """Corresponds to IDD field `Loop Demand Side Design Flow Rate`

        Args:
            value (float or "Autosize"): value for IDD Field `Loop Demand Side Design Flow Rate`
                Units: m3/s
                IP-Units: gal/min
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Loop Demand Side Design Flow Rate"] = value

    @property
    def loop_supply_side_inlet_node_name(self):
        """Get loop_supply_side_inlet_node_name.

        Returns:
            str: the value of `loop_supply_side_inlet_node_name` or None if not set

        """
        return self["Loop Supply Side Inlet Node Name"]

    @loop_supply_side_inlet_node_name.setter
    def loop_supply_side_inlet_node_name(self, value=None):
        """Corresponds to IDD field `Loop Supply Side Inlet Node Name`

        Args:
            value (str): value for IDD Field `Loop Supply Side Inlet Node Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Loop Supply Side Inlet Node Name"] = value

    @property
    def loop_supply_side_outlet_node_name(self):
        """Get loop_supply_side_outlet_node_name.

        Returns:
            str: the value of `loop_supply_side_outlet_node_name` or None if not set

        """
        return self["Loop Supply Side Outlet Node Name"]

    @loop_supply_side_outlet_node_name.setter
    def loop_supply_side_outlet_node_name(self, value=None):
        """Corresponds to IDD field `Loop Supply Side Outlet Node Name`

        Args:
            value (str): value for IDD Field `Loop Supply Side Outlet Node Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Loop Supply Side Outlet Node Name"] = value

    @property
    def loop_supply_side_design_flow_rate(self):
        """Get loop_supply_side_design_flow_rate.

        Returns:
            float: the value of `loop_supply_side_design_flow_rate` or None if not set

        """
        return self["Loop Supply Side Design Flow Rate"]

    @loop_supply_side_design_flow_rate.setter
    def loop_supply_side_design_flow_rate(self, value=None):
        """Corresponds to IDD field `Loop Supply Side Design Flow Rate`

        Args:
            value (float or "Autosize"): value for IDD Field `Loop Supply Side Design Flow Rate`
                Units: m3/s
                IP-Units: gal/min
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Loop Supply Side Design Flow Rate"] = value

    @property
    def heat_exchange_model_type(self):
        """Get heat_exchange_model_type.

        Returns:
            str: the value of `heat_exchange_model_type` or None if not set

        """
        return self["Heat Exchange Model Type"]

    @heat_exchange_model_type.setter
    def heat_exchange_model_type(self, value="Ideal"):
        """Corresponds to IDD field `Heat Exchange Model Type`

        Args:
            value (str): value for IDD Field `Heat Exchange Model Type`
                Default value: Ideal
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Heat Exchange Model Type"] = value

    @property
    def heat_exchanger_ufactor_times_area_value(self):
        """Get heat_exchanger_ufactor_times_area_value.

        Returns:
            float: the value of `heat_exchanger_ufactor_times_area_value` or None if not set

        """
        return self["Heat Exchanger U-Factor Times Area Value"]

    @heat_exchanger_ufactor_times_area_value.setter
    def heat_exchanger_ufactor_times_area_value(self, value=None):
        """  Corresponds to IDD field `Heat Exchanger U-Factor Times Area Value`

        Args:
            value (float or "Autosize"): value for IDD Field `Heat Exchanger U-Factor Times Area Value`
                Units: W/k
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Heat Exchanger U-Factor Times Area Value"] = value

    @property
    def control_type(self):
        """Get control_type.

        Returns:
            str: the value of `control_type` or None if not set

        """
        return self["Control Type"]

    @control_type.setter
    def control_type(self, value="UncontrolledOn"):
        """Corresponds to IDD field `Control Type`

        Args:
            value (str): value for IDD Field `Control Type`
                Default value: UncontrolledOn
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Control Type"] = value

    @property
    def heat_exchanger_setpoint_node_name(self):
        """Get heat_exchanger_setpoint_node_name.

        Returns:
            str: the value of `heat_exchanger_setpoint_node_name` or None if not set

        """
        return self["Heat Exchanger Setpoint Node Name"]

    @heat_exchanger_setpoint_node_name.setter
    def heat_exchanger_setpoint_node_name(self, value=None):
        """  Corresponds to IDD field `Heat Exchanger Setpoint Node Name`
        Setpoint node is needed with any Control Type that is "*Setpoint*"

        Args:
            value (str): value for IDD Field `Heat Exchanger Setpoint Node Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Heat Exchanger Setpoint Node Name"] = value

    @property
    def minimum_temperature_difference_to_activate_heat_exchanger(self):
        """Get minimum_temperature_difference_to_activate_heat_exchanger.

        Returns:
            float: the value of `minimum_temperature_difference_to_activate_heat_exchanger` or None if not set

        """
        return self[
            "Minimum Temperature Difference to Activate Heat Exchanger"]

    @minimum_temperature_difference_to_activate_heat_exchanger.setter
    def minimum_temperature_difference_to_activate_heat_exchanger(
            self,
            value=0.01):
        """Corresponds to IDD field `Minimum Temperature Difference to Activate
        Heat Exchanger` Tolerance between control temperatures used to
        determine if heat exchanger should run.

        Args:
            value (float): value for IDD Field `Minimum Temperature Difference to Activate Heat Exchanger`
                Units: deltaC
                Default value: 0.01
                value <= 50.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self[
            "Minimum Temperature Difference to Activate Heat Exchanger"] = value

    @property
    def heat_transfer_metering_end_use_type(self):
        """Get heat_transfer_metering_end_use_type.

        Returns:
            str: the value of `heat_transfer_metering_end_use_type` or None if not set

        """
        return self["Heat Transfer Metering End Use Type"]

    @heat_transfer_metering_end_use_type.setter
    def heat_transfer_metering_end_use_type(self, value="LoopToLoop"):
        """Corresponds to IDD field `Heat Transfer Metering End Use Type` This
        feild controls end use reporting for heat transfer meters.

        Args:
            value (str): value for IDD Field `Heat Transfer Metering End Use Type`
                Default value: LoopToLoop
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Heat Transfer Metering End Use Type"] = value

    @property
    def component_override_loop_supply_side_inlet_node_name(self):
        """Get component_override_loop_supply_side_inlet_node_name.

        Returns:
            str: the value of `component_override_loop_supply_side_inlet_node_name` or None if not set

        """
        return self["Component Override Loop Supply Side Inlet Node Name"]

    @component_override_loop_supply_side_inlet_node_name.setter
    def component_override_loop_supply_side_inlet_node_name(self, value=None):
        """Corresponds to IDD field `Component Override Loop Supply Side Inlet
        Node Name` This field is only used if Control Type is set to
        CoolingSetpointOnOffWithComponentOverride.

        Args:
            value (str): value for IDD Field `Component Override Loop Supply Side Inlet Node Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Component Override Loop Supply Side Inlet Node Name"] = value

    @property
    def component_override_loop_demand_side_inlet_node_name(self):
        """Get component_override_loop_demand_side_inlet_node_name.

        Returns:
            str: the value of `component_override_loop_demand_side_inlet_node_name` or None if not set

        """
        return self["Component Override Loop Demand Side Inlet Node Name"]

    @component_override_loop_demand_side_inlet_node_name.setter
    def component_override_loop_demand_side_inlet_node_name(self, value=None):
        """Corresponds to IDD field `Component Override Loop Demand Side Inlet
        Node Name` This field is only used if Control Type is set to
        CoolingSetpointOnOffWithComponentOverride.

        Args:
            value (str): value for IDD Field `Component Override Loop Demand Side Inlet Node Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Component Override Loop Demand Side Inlet Node Name"] = value

    @property
    def component_override_cooling_control_temperature_mode(self):
        """Get component_override_cooling_control_temperature_mode.

        Returns:
            str: the value of `component_override_cooling_control_temperature_mode` or None if not set

        """
        return self["Component Override Cooling Control Temperature Mode"]

    @component_override_cooling_control_temperature_mode.setter
    def component_override_cooling_control_temperature_mode(
            self,
            value="Loop"):
        """Corresponds to IDD field `Component Override Cooling Control
        Temperature Mode` This field is only used if Control Type is set to
        CoolingSetpointOnOffWithComponentOverride.

        Args:
            value (str): value for IDD Field `Component Override Cooling Control Temperature Mode`
                Default value: Loop
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Component Override Cooling Control Temperature Mode"] = value

    @property
    def sizing_factor(self):
        """Get sizing_factor.

        Returns:
            float: the value of `sizing_factor` or None if not set

        """
        return self["Sizing Factor"]

    @sizing_factor.setter
    def sizing_factor(self, value=1.0):
        """Corresponds to IDD field `Sizing Factor` Multiplies the autosized
        flow rates for this device.

        Args:
            value (float): value for IDD Field `Sizing Factor`
                Default value: 1.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Sizing Factor"] = value

    @property
    def operation_minimum_temperature_limit(self):
        """Get operation_minimum_temperature_limit.

        Returns:
            float: the value of `operation_minimum_temperature_limit` or None if not set

        """
        return self["Operation Minimum Temperature Limit"]

    @operation_minimum_temperature_limit.setter
    def operation_minimum_temperature_limit(self, value=None):
        """Corresponds to IDD field `Operation Minimum Temperature Limit` Lower
        limit on inlet temperatures, heat exchanger will not operate if either
        inlet is below this limit.

        Args:
            value (float): value for IDD Field `Operation Minimum Temperature Limit`
                Units: C
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Operation Minimum Temperature Limit"] = value

    @property
    def operation_maximum_temperature_limit(self):
        """Get operation_maximum_temperature_limit.

        Returns:
            float: the value of `operation_maximum_temperature_limit` or None if not set

        """
        return self["Operation Maximum Temperature Limit"]

    @operation_maximum_temperature_limit.setter
    def operation_maximum_temperature_limit(self, value=None):
        """Corresponds to IDD field `Operation Maximum Temperature Limit` Upper
        limit on inlet temperatures, heat exchanger will not operate if either
        inlet is above this limit.

        Args:
            value (float): value for IDD Field `Operation Maximum Temperature Limit`
                Units: C
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Operation Maximum Temperature Limit"] = value


