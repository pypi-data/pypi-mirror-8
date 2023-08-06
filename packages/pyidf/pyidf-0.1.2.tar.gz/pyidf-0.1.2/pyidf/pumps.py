""" Data objects in group "Pumps"
"""

from collections import OrderedDict
import logging
from pyidf.helper import DataObject

logger = logging.getLogger("pyidf")
logger.addHandler(logging.NullHandler())



class BranchList(DataObject):

    """ Corresponds to IDD object `BranchList`
        Branches MUST be listed in Flow order: Inlet branch, then parallel branches, then Outlet branch.
        Branches are simulated in the order listed.  Branch names cannot be duplicated within a single branch list.
    """
    schema = {'extensible-fields': OrderedDict([(u'branch name',
                                                 {'name': u'Branch Name',
                                                  'pyname': u'branch_name',
                                                  'required-field': False,
                                                  'autosizable': False,
                                                  'autocalculatable': False,
                                                  'type': u'object-list'})]),
              'fields': OrderedDict([(u'name',
                                      {'name': u'Name',
                                       'pyname': u'name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'alpha'})]),
              'format': None,
              'group': u'Pumps',
              'min-fields': 2,
              'name': u'BranchList',
              'pyname': u'BranchList',
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

    def add_extensible(self,
                       branch_name=None,
                       ):
        """Add values for extensible fields.

        Args:

            branch_name (str): value for IDD Field `Branch Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        """
        vals = []
        branch_name = self.check_value("Branch Name", branch_name)
        vals.append(branch_name)
        self._extdata.append(vals)

    @property
    def extensibles(self):
        """Get list of all extensibles."""
        return self._extdata

    @extensibles.setter
    def extensibles(self, extensibles):
        """Replaces extensible fields with `extensibles`

        Args:
            extensibles (list): nested list of extensible values

        """
        self._extdata = []
        for ext in extensibles:
            self.add_extensible(*ext)




class PumpVariableSpeed(DataObject):

    """ Corresponds to IDD object `Pump:VariableSpeed`
        This pump model is described in the ASHRAE secondary HVAC toolkit.
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
                                     (u'rated flow rate',
                                      {'name': u'Rated Flow Rate',
                                       'pyname': u'rated_flow_rate',
                                       'minimum>': 0.0,
                                       'required-field': False,
                                       'autosizable': True,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm3/s'}),
                                     (u'rated pump head',
                                      {'name': u'Rated Pump Head',
                                       'pyname': u'rated_pump_head',
                                       'default': 179352.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'Pa'}),
                                     (u'rated power consumption',
                                      {'name': u'Rated Power Consumption',
                                       'pyname': u'rated_power_consumption',
                                       'required-field': False,
                                       'autosizable': True,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'W'}),
                                     (u'motor efficiency',
                                      {'name': u'Motor Efficiency',
                                       'pyname': u'motor_efficiency',
                                       'default': 0.9,
                                       'minimum>': 0.0,
                                       'maximum': 1.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'fraction of motor inefficiencies to fluid stream',
                                      {'name': u'Fraction of Motor Inefficiencies to Fluid Stream',
                                       'pyname': u'fraction_of_motor_inefficiencies_to_fluid_stream',
                                       'default': 0.0,
                                       'maximum': 1.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': 'real'}),
                                     (u'coefficient 1 of the part load performance curve',
                                      {'name': u'Coefficient 1 of the Part Load Performance Curve',
                                       'pyname': u'coefficient_1_of_the_part_load_performance_curve',
                                       'default': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real'}),
                                     (u'coefficient 2 of the part load performance curve',
                                      {'name': u'Coefficient 2 of the Part Load Performance Curve',
                                       'pyname': u'coefficient_2_of_the_part_load_performance_curve',
                                       'default': 1.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real'}),
                                     (u'coefficient 3 of the part load performance curve',
                                      {'name': u'Coefficient 3 of the Part Load Performance Curve',
                                       'pyname': u'coefficient_3_of_the_part_load_performance_curve',
                                       'default': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real'}),
                                     (u'coefficient 4 of the part load performance curve',
                                      {'name': u'Coefficient 4 of the Part Load Performance Curve',
                                       'pyname': u'coefficient_4_of_the_part_load_performance_curve',
                                       'default': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real'}),
                                     (u'minimum flow rate',
                                      {'name': u'Minimum Flow Rate',
                                       'pyname': u'minimum_flow_rate',
                                       'default': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm3/s'}),
                                     (u'pump control type',
                                      {'name': u'Pump Control Type',
                                       'pyname': u'pump_control_type',
                                       'default': u'Continuous',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'Continuous',
                                                           u'Intermittent'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'pump flow rate schedule name',
                                      {'name': u'Pump Flow Rate Schedule Name',
                                       'pyname': u'pump_flow_rate_schedule_name',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'pump curve name',
                                      {'name': u'Pump Curve Name',
                                       'pyname': u'pump_curve_name',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'impeller diameter',
                                      {'name': u'Impeller Diameter',
                                       'pyname': u'impeller_diameter',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'm'}),
                                     (u'vfd control type',
                                      {'name': u'VFD Control Type',
                                       'pyname': u'vfd_control_type',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'ManualControl',
                                                           u'PressureSetpointControl'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'pump rpm schedule name',
                                      {'name': u'Pump rpm Schedule Name',
                                       'pyname': u'pump_rpm_schedule_name',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'minimum pressure schedule',
                                      {'name': u'Minimum Pressure Schedule',
                                       'pyname': u'minimum_pressure_schedule',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list',
                                       'unit': u'Pa'}),
                                     (u'maximum pressure schedule',
                                      {'name': u'Maximum Pressure Schedule',
                                       'pyname': u'maximum_pressure_schedule',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list',
                                       'unit': u'Pa'}),
                                     (u'minimum rpm schedule',
                                      {'name': u'Minimum RPM Schedule',
                                       'pyname': u'minimum_rpm_schedule',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list',
                                       'unit': u'Rotations Per Minute'}),
                                     (u'maximum rpm schedule',
                                      {'name': u'Maximum RPM Schedule',
                                       'pyname': u'maximum_rpm_schedule',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list',
                                       'unit': u'Rotations Per Minute'}),
                                     (u'zone name',
                                      {'name': u'Zone Name',
                                       'pyname': u'zone_name',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'Object-list'}),
                                     (u'skin loss radiative fraction',
                                      {'name': u'Skin Loss Radiative Fraction',
                                       'pyname': u'skin_loss_radiative_fraction',
                                       'maximum': 1.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': u'real'})]),
              'format': None,
              'group': u'Pumps',
              'min-fields': 14,
              'name': u'Pump:VariableSpeed',
              'pyname': u'PumpVariableSpeed',
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
    def rated_flow_rate(self):
        """Get rated_flow_rate.

        Returns:
            float: the value of `rated_flow_rate` or None if not set

        """
        return self["Rated Flow Rate"]

    @rated_flow_rate.setter
    def rated_flow_rate(self, value=None):
        """Corresponds to IDD field `Rated Flow Rate`

        Args:
            value (float or "Autosize"): value for IDD Field `Rated Flow Rate`
                Units: m3/s
                IP-Units: gal/min
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Rated Flow Rate"] = value

    @property
    def rated_pump_head(self):
        """Get rated_pump_head.

        Returns:
            float: the value of `rated_pump_head` or None if not set

        """
        return self["Rated Pump Head"]

    @rated_pump_head.setter
    def rated_pump_head(self, value=179352.0):
        """Corresponds to IDD field `Rated Pump Head` default head is 60 feet.

        Args:
            value (float): value for IDD Field `Rated Pump Head`
                Units: Pa
                IP-Units: ftH2O
                Default value: 179352.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Rated Pump Head"] = value

    @property
    def rated_power_consumption(self):
        """Get rated_power_consumption.

        Returns:
            float: the value of `rated_power_consumption` or None if not set

        """
        return self["Rated Power Consumption"]

    @rated_power_consumption.setter
    def rated_power_consumption(self, value=None):
        """  Corresponds to IDD field `Rated Power Consumption`
        If this field is autosized, an impeller efficiency of 0.78 is assumed.
        autosized Rated Power Consumption = Rated Flow Rate * Rated Pump Head / (0.78 * Motor Efficiency)

        Args:
            value (float or "Autosize"): value for IDD Field `Rated Power Consumption`
                Units: W
                IP-Units: W
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Rated Power Consumption"] = value

    @property
    def motor_efficiency(self):
        """Get motor_efficiency.

        Returns:
            float: the value of `motor_efficiency` or None if not set

        """
        return self["Motor Efficiency"]

    @motor_efficiency.setter
    def motor_efficiency(self, value=0.9):
        """  Corresponds to IDD field `Motor Efficiency`
        This is the motor efficiency only. When the Rated Power Consumption if autosized,
        an impeller efficiency of 0.78 is assumed in addition to the motor efficiency.

        Args:
            value (float): value for IDD Field `Motor Efficiency`
                Default value: 0.9
                value <= 1.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Motor Efficiency"] = value

    @property
    def fraction_of_motor_inefficiencies_to_fluid_stream(self):
        """Get fraction_of_motor_inefficiencies_to_fluid_stream.

        Returns:
            float: the value of `fraction_of_motor_inefficiencies_to_fluid_stream` or None if not set

        """
        return self["Fraction of Motor Inefficiencies to Fluid Stream"]

    @fraction_of_motor_inefficiencies_to_fluid_stream.setter
    def fraction_of_motor_inefficiencies_to_fluid_stream(self, value=None):
        """Corresponds to IDD field `Fraction of Motor Inefficiencies to Fluid
        Stream`

        Args:
            value (float): value for IDD Field `Fraction of Motor Inefficiencies to Fluid Stream`
                value <= 1.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Fraction of Motor Inefficiencies to Fluid Stream"] = value

    @property
    def coefficient_1_of_the_part_load_performance_curve(self):
        """Get coefficient_1_of_the_part_load_performance_curve.

        Returns:
            float: the value of `coefficient_1_of_the_part_load_performance_curve` or None if not set

        """
        return self["Coefficient 1 of the Part Load Performance Curve"]

    @coefficient_1_of_the_part_load_performance_curve.setter
    def coefficient_1_of_the_part_load_performance_curve(self, value=None):
        """Corresponds to IDD field `Coefficient 1 of the Part Load Performance
        Curve`

        Args:
            value (float): value for IDD Field `Coefficient 1 of the Part Load Performance Curve`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient 1 of the Part Load Performance Curve"] = value

    @property
    def coefficient_2_of_the_part_load_performance_curve(self):
        """Get coefficient_2_of_the_part_load_performance_curve.

        Returns:
            float: the value of `coefficient_2_of_the_part_load_performance_curve` or None if not set

        """
        return self["Coefficient 2 of the Part Load Performance Curve"]

    @coefficient_2_of_the_part_load_performance_curve.setter
    def coefficient_2_of_the_part_load_performance_curve(self, value=1.0):
        """Corresponds to IDD field `Coefficient 2 of the Part Load Performance
        Curve`

        Args:
            value (float): value for IDD Field `Coefficient 2 of the Part Load Performance Curve`
                Default value: 1.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient 2 of the Part Load Performance Curve"] = value

    @property
    def coefficient_3_of_the_part_load_performance_curve(self):
        """Get coefficient_3_of_the_part_load_performance_curve.

        Returns:
            float: the value of `coefficient_3_of_the_part_load_performance_curve` or None if not set

        """
        return self["Coefficient 3 of the Part Load Performance Curve"]

    @coefficient_3_of_the_part_load_performance_curve.setter
    def coefficient_3_of_the_part_load_performance_curve(self, value=None):
        """Corresponds to IDD field `Coefficient 3 of the Part Load Performance
        Curve`

        Args:
            value (float): value for IDD Field `Coefficient 3 of the Part Load Performance Curve`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient 3 of the Part Load Performance Curve"] = value

    @property
    def coefficient_4_of_the_part_load_performance_curve(self):
        """Get coefficient_4_of_the_part_load_performance_curve.

        Returns:
            float: the value of `coefficient_4_of_the_part_load_performance_curve` or None if not set

        """
        return self["Coefficient 4 of the Part Load Performance Curve"]

    @coefficient_4_of_the_part_load_performance_curve.setter
    def coefficient_4_of_the_part_load_performance_curve(self, value=None):
        """Corresponds to IDD field `Coefficient 4 of the Part Load Performance
        Curve`

        Args:
            value (float): value for IDD Field `Coefficient 4 of the Part Load Performance Curve`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient 4 of the Part Load Performance Curve"] = value

    @property
    def minimum_flow_rate(self):
        """Get minimum_flow_rate.

        Returns:
            float: the value of `minimum_flow_rate` or None if not set

        """
        return self["Minimum Flow Rate"]

    @minimum_flow_rate.setter
    def minimum_flow_rate(self, value=None):
        """Corresponds to IDD field `Minimum Flow Rate` This value can be zero
        and will be defaulted to that if not specified.

        Args:
            value (float): value for IDD Field `Minimum Flow Rate`
                Units: m3/s
                IP-Units: gal/min
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Minimum Flow Rate"] = value

    @property
    def pump_control_type(self):
        """Get pump_control_type.

        Returns:
            str: the value of `pump_control_type` or None if not set

        """
        return self["Pump Control Type"]

    @pump_control_type.setter
    def pump_control_type(self, value="Continuous"):
        """Corresponds to IDD field `Pump Control Type`

        Args:
            value (str): value for IDD Field `Pump Control Type`
                Default value: Continuous
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Pump Control Type"] = value

    @property
    def pump_flow_rate_schedule_name(self):
        """Get pump_flow_rate_schedule_name.

        Returns:
            str: the value of `pump_flow_rate_schedule_name` or None if not set

        """
        return self["Pump Flow Rate Schedule Name"]

    @pump_flow_rate_schedule_name.setter
    def pump_flow_rate_schedule_name(self, value=None):
        """Corresponds to IDD field `Pump Flow Rate Schedule Name` Modifies the
        rated flow rate of the pump on a time basis. Default is that the pump
        is on and runs according to its other operational requirements
        specified above.  The schedule is for special pump operations.

        Args:
            value (str): value for IDD Field `Pump Flow Rate Schedule Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Pump Flow Rate Schedule Name"] = value

    @property
    def pump_curve_name(self):
        """Get pump_curve_name.

        Returns:
            str: the value of `pump_curve_name` or None if not set

        """
        return self["Pump Curve Name"]

    @pump_curve_name.setter
    def pump_curve_name(self, value=None):
        """  Corresponds to IDD field `Pump Curve Name`
        This references any single independent variable polynomial curve in order to
        do pressure vs. flow calculations for this pump.  The available types are then:
        Linear, Quadratic, Cubic, and Quartic
        The non-dimensional pump pressure relationship is of the following form:
        (psi = C4*phi^4 + C3*phi^3 + C2*phi^2 + C1*phi + C0)
        Where the nondimensional variables are defined as:
        delP = rho * ((N/60)^2) * (D^2) * psi
        mdot = rho * (N/60) * (D^3) * phi
        Table:OneIndependentVariable object can also be used

        Args:
            value (str): value for IDD Field `Pump Curve Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Pump Curve Name"] = value

    @property
    def impeller_diameter(self):
        """Get impeller_diameter.

        Returns:
            float: the value of `impeller_diameter` or None if not set

        """
        return self["Impeller Diameter"]

    @impeller_diameter.setter
    def impeller_diameter(self, value=None):
        """Corresponds to IDD field `Impeller Diameter` "D" in above expression
        in field A6.

        Args:
            value (float): value for IDD Field `Impeller Diameter`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Impeller Diameter"] = value

    @property
    def vfd_control_type(self):
        """Get vfd_control_type.

        Returns:
            str: the value of `vfd_control_type` or None if not set

        """
        return self["VFD Control Type"]

    @vfd_control_type.setter
    def vfd_control_type(self, value=None):
        """Corresponds to IDD field `VFD Control Type`

        Args:
            value (str): value for IDD Field `VFD Control Type`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["VFD Control Type"] = value

    @property
    def pump_rpm_schedule_name(self):
        """Get pump_rpm_schedule_name.

        Returns:
            str: the value of `pump_rpm_schedule_name` or None if not set

        """
        return self["Pump rpm Schedule Name"]

    @pump_rpm_schedule_name.setter
    def pump_rpm_schedule_name(self, value=None):
        """Corresponds to IDD field `Pump rpm Schedule Name` Modifies the rpm
        of the pump on a time basis. Default is that the pump is on and runs
        according to its other operational requirements specified above.  The
        schedule is for special pump operations.

        Args:
            value (str): value for IDD Field `Pump rpm Schedule Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Pump rpm Schedule Name"] = value

    @property
    def minimum_pressure_schedule(self):
        """Get minimum_pressure_schedule.

        Returns:
            str: the value of `minimum_pressure_schedule` or None if not set

        """
        return self["Minimum Pressure Schedule"]

    @minimum_pressure_schedule.setter
    def minimum_pressure_schedule(self, value=None):
        """Corresponds to IDD field `Minimum Pressure Schedule`

        Args:
            value (str): value for IDD Field `Minimum Pressure Schedule`
                Units: Pa
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Minimum Pressure Schedule"] = value

    @property
    def maximum_pressure_schedule(self):
        """Get maximum_pressure_schedule.

        Returns:
            str: the value of `maximum_pressure_schedule` or None if not set

        """
        return self["Maximum Pressure Schedule"]

    @maximum_pressure_schedule.setter
    def maximum_pressure_schedule(self, value=None):
        """Corresponds to IDD field `Maximum Pressure Schedule`

        Args:
            value (str): value for IDD Field `Maximum Pressure Schedule`
                Units: Pa
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Maximum Pressure Schedule"] = value

    @property
    def minimum_rpm_schedule(self):
        """Get minimum_rpm_schedule.

        Returns:
            str: the value of `minimum_rpm_schedule` or None if not set

        """
        return self["Minimum RPM Schedule"]

    @minimum_rpm_schedule.setter
    def minimum_rpm_schedule(self, value=None):
        """Corresponds to IDD field `Minimum RPM Schedule`

        Args:
            value (str): value for IDD Field `Minimum RPM Schedule`
                Units: Rotations Per Minute
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Minimum RPM Schedule"] = value

    @property
    def maximum_rpm_schedule(self):
        """Get maximum_rpm_schedule.

        Returns:
            str: the value of `maximum_rpm_schedule` or None if not set

        """
        return self["Maximum RPM Schedule"]

    @maximum_rpm_schedule.setter
    def maximum_rpm_schedule(self, value=None):
        """Corresponds to IDD field `Maximum RPM Schedule`

        Args:
            value (str): value for IDD Field `Maximum RPM Schedule`
                Units: Rotations Per Minute
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Maximum RPM Schedule"] = value

    @property
    def zone_name(self):
        """Get zone_name.

        Returns:
            str: the value of `zone_name` or None if not set

        """
        return self["Zone Name"]

    @zone_name.setter
    def zone_name(self, value=None):
        """Corresponds to IDD field `Zone Name` optional, if used pump losses
        transfered to zone as internal gains.

        Args:
            value (str): value for IDD Field `Zone Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Zone Name"] = value

    @property
    def skin_loss_radiative_fraction(self):
        """Get skin_loss_radiative_fraction.

        Returns:
            float: the value of `skin_loss_radiative_fraction` or None if not set

        """
        return self["Skin Loss Radiative Fraction"]

    @skin_loss_radiative_fraction.setter
    def skin_loss_radiative_fraction(self, value=None):
        """Corresponds to IDD field `Skin Loss Radiative Fraction` optional. If
        zone identified in previous field then this determines the split
        between convection and radiation for the skin losses.

        Args:
            value (float): value for IDD Field `Skin Loss Radiative Fraction`
                value <= 1.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Skin Loss Radiative Fraction"] = value




class PumpConstantSpeed(DataObject):

    """ Corresponds to IDD object `Pump:ConstantSpeed`
        This pump model is described in the ASHRAE secondary HVAC toolkit.
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
                                     (u'rated flow rate',
                                      {'name': u'Rated Flow Rate',
                                       'pyname': u'rated_flow_rate',
                                       'minimum>': 0.0,
                                       'required-field': False,
                                       'autosizable': True,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm3/s'}),
                                     (u'rated pump head',
                                      {'name': u'Rated Pump Head',
                                       'pyname': u'rated_pump_head',
                                       'default': 179352.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'Pa'}),
                                     (u'rated power consumption',
                                      {'name': u'Rated Power Consumption',
                                       'pyname': u'rated_power_consumption',
                                       'required-field': False,
                                       'autosizable': True,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'W'}),
                                     (u'motor efficiency',
                                      {'name': u'Motor Efficiency',
                                       'pyname': u'motor_efficiency',
                                       'default': 0.9,
                                       'minimum>': 0.0,
                                       'maximum': 1.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'fraction of motor inefficiencies to fluid stream',
                                      {'name': u'Fraction of Motor Inefficiencies to Fluid Stream',
                                       'pyname': u'fraction_of_motor_inefficiencies_to_fluid_stream',
                                       'default': 0.0,
                                       'maximum': 1.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': 'real'}),
                                     (u'pump control type',
                                      {'name': u'Pump Control Type',
                                       'pyname': u'pump_control_type',
                                       'default': u'Continuous',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'Continuous',
                                                           u'Intermittent'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'pump flow rate schedule name',
                                      {'name': u'Pump Flow Rate Schedule Name',
                                       'pyname': u'pump_flow_rate_schedule_name',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'pump curve name',
                                      {'name': u'Pump Curve Name',
                                       'pyname': u'pump_curve_name',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'impeller diameter',
                                      {'name': u'Impeller Diameter',
                                       'pyname': u'impeller_diameter',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'm'}),
                                     (u'rotational speed',
                                      {'name': u'Rotational Speed',
                                       'pyname': u'rotational_speed',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'rev/min'}),
                                     (u'zone name',
                                      {'name': u'Zone Name',
                                       'pyname': u'zone_name',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'Object-list'}),
                                     (u'skin loss radiative fraction',
                                      {'name': u'Skin Loss Radiative Fraction',
                                       'pyname': u'skin_loss_radiative_fraction',
                                       'maximum': 1.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': u'real'})]),
              'format': None,
              'group': u'Pumps',
              'min-fields': 9,
              'name': u'Pump:ConstantSpeed',
              'pyname': u'PumpConstantSpeed',
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
    def rated_flow_rate(self):
        """Get rated_flow_rate.

        Returns:
            float: the value of `rated_flow_rate` or None if not set

        """
        return self["Rated Flow Rate"]

    @rated_flow_rate.setter
    def rated_flow_rate(self, value=None):
        """Corresponds to IDD field `Rated Flow Rate`

        Args:
            value (float or "Autosize"): value for IDD Field `Rated Flow Rate`
                Units: m3/s
                IP-Units: gal/min
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Rated Flow Rate"] = value

    @property
    def rated_pump_head(self):
        """Get rated_pump_head.

        Returns:
            float: the value of `rated_pump_head` or None if not set

        """
        return self["Rated Pump Head"]

    @rated_pump_head.setter
    def rated_pump_head(self, value=179352.0):
        """Corresponds to IDD field `Rated Pump Head` default head is 60 feet.

        Args:
            value (float): value for IDD Field `Rated Pump Head`
                Units: Pa
                IP-Units: ftH2O
                Default value: 179352.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Rated Pump Head"] = value

    @property
    def rated_power_consumption(self):
        """Get rated_power_consumption.

        Returns:
            float: the value of `rated_power_consumption` or None if not set

        """
        return self["Rated Power Consumption"]

    @rated_power_consumption.setter
    def rated_power_consumption(self, value=None):
        """  Corresponds to IDD field `Rated Power Consumption`
        If this field is autosized, an impeller efficiency of 0.78 is assumed.
        autosized Rated Power Consumption = Rated Flow Rate * Rated Pump Head / (0.78 * Motor Efficiency)

        Args:
            value (float or "Autosize"): value for IDD Field `Rated Power Consumption`
                Units: W
                IP-Units: W
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Rated Power Consumption"] = value

    @property
    def motor_efficiency(self):
        """Get motor_efficiency.

        Returns:
            float: the value of `motor_efficiency` or None if not set

        """
        return self["Motor Efficiency"]

    @motor_efficiency.setter
    def motor_efficiency(self, value=0.9):
        """  Corresponds to IDD field `Motor Efficiency`
        This is the motor efficiency only. When the Rated Power Consumption if autosized,
        an impeller efficiency of 0.78 is assumed in addition to the motor efficiency.

        Args:
            value (float): value for IDD Field `Motor Efficiency`
                Default value: 0.9
                value <= 1.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Motor Efficiency"] = value

    @property
    def fraction_of_motor_inefficiencies_to_fluid_stream(self):
        """Get fraction_of_motor_inefficiencies_to_fluid_stream.

        Returns:
            float: the value of `fraction_of_motor_inefficiencies_to_fluid_stream` or None if not set

        """
        return self["Fraction of Motor Inefficiencies to Fluid Stream"]

    @fraction_of_motor_inefficiencies_to_fluid_stream.setter
    def fraction_of_motor_inefficiencies_to_fluid_stream(self, value=None):
        """Corresponds to IDD field `Fraction of Motor Inefficiencies to Fluid
        Stream`

        Args:
            value (float): value for IDD Field `Fraction of Motor Inefficiencies to Fluid Stream`
                value <= 1.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Fraction of Motor Inefficiencies to Fluid Stream"] = value

    @property
    def pump_control_type(self):
        """Get pump_control_type.

        Returns:
            str: the value of `pump_control_type` or None if not set

        """
        return self["Pump Control Type"]

    @pump_control_type.setter
    def pump_control_type(self, value="Continuous"):
        """Corresponds to IDD field `Pump Control Type`

        Args:
            value (str): value for IDD Field `Pump Control Type`
                Default value: Continuous
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Pump Control Type"] = value

    @property
    def pump_flow_rate_schedule_name(self):
        """Get pump_flow_rate_schedule_name.

        Returns:
            str: the value of `pump_flow_rate_schedule_name` or None if not set

        """
        return self["Pump Flow Rate Schedule Name"]

    @pump_flow_rate_schedule_name.setter
    def pump_flow_rate_schedule_name(self, value=None):
        """Corresponds to IDD field `Pump Flow Rate Schedule Name` Modifies the
        rated flow rate of the pump on a time basis. Default is that the pump
        is on and runs according to its other operational requirements
        specified above.  The schedule is for special pump operations.

        Args:
            value (str): value for IDD Field `Pump Flow Rate Schedule Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Pump Flow Rate Schedule Name"] = value

    @property
    def pump_curve_name(self):
        """Get pump_curve_name.

        Returns:
            str: the value of `pump_curve_name` or None if not set

        """
        return self["Pump Curve Name"]

    @pump_curve_name.setter
    def pump_curve_name(self, value=None):
        """  Corresponds to IDD field `Pump Curve Name`
        This references any single independent variable polynomial curve in order to
        do pressure vs. flow calculations for this pump.  The available types are then:
        Linear, Quadratic, Cubic, and Quartic
        The non-dimensional pump pressure relationship is of the following form:
        (psi = C4*phi^4 + C3*phi^3 + C2*phi^2 + C1*phi + C0)
        Where the nondimensional variables are defined as:
        delP = rho * ((N/60)^2) * (D^2) * psi
        mdot = rho * (N/60) * (D^3) * phi
        Table:OneIndependentVariable object can also be used

        Args:
            value (str): value for IDD Field `Pump Curve Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Pump Curve Name"] = value

    @property
    def impeller_diameter(self):
        """Get impeller_diameter.

        Returns:
            float: the value of `impeller_diameter` or None if not set

        """
        return self["Impeller Diameter"]

    @impeller_diameter.setter
    def impeller_diameter(self, value=None):
        """Corresponds to IDD field `Impeller Diameter` "D" in above expression
        in field A6.

        Args:
            value (float): value for IDD Field `Impeller Diameter`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Impeller Diameter"] = value

    @property
    def rotational_speed(self):
        """Get rotational_speed.

        Returns:
            float: the value of `rotational_speed` or None if not set

        """
        return self["Rotational Speed"]

    @rotational_speed.setter
    def rotational_speed(self, value=None):
        """Corresponds to IDD field `Rotational Speed` "N" in above expression
        in field A6.

        Args:
            value (float): value for IDD Field `Rotational Speed`
                Units: rev/min
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Rotational Speed"] = value

    @property
    def zone_name(self):
        """Get zone_name.

        Returns:
            str: the value of `zone_name` or None if not set

        """
        return self["Zone Name"]

    @zone_name.setter
    def zone_name(self, value=None):
        """Corresponds to IDD field `Zone Name` optional, if used pump losses
        transfered to zone as internal gains.

        Args:
            value (str): value for IDD Field `Zone Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Zone Name"] = value

    @property
    def skin_loss_radiative_fraction(self):
        """Get skin_loss_radiative_fraction.

        Returns:
            float: the value of `skin_loss_radiative_fraction` or None if not set

        """
        return self["Skin Loss Radiative Fraction"]

    @skin_loss_radiative_fraction.setter
    def skin_loss_radiative_fraction(self, value=None):
        """Corresponds to IDD field `Skin Loss Radiative Fraction` optional. If
        zone identified in previous field then this determines the split
        between convection and radiation for the skin losses.

        Args:
            value (float): value for IDD Field `Skin Loss Radiative Fraction`
                value <= 1.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Skin Loss Radiative Fraction"] = value




class PumpVariableSpeedCondensate(DataObject):

    """ Corresponds to IDD object `Pump:VariableSpeed:Condensate`
        This pump model is described in the ASHRAE secondary HVAC toolkit.
        Variable Speed Condensate pump for Steam Systems
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
                                     (u'rated flow rate',
                                      {'name': u'Rated Flow Rate',
                                       'pyname': u'rated_flow_rate',
                                       'minimum>': 0.0,
                                       'required-field': False,
                                       'autosizable': True,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm3/s'}),
                                     (u'rated pump head',
                                      {'name': u'Rated Pump Head',
                                       'pyname': u'rated_pump_head',
                                       'default': 179352.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'Pa'}),
                                     (u'rated power consumption',
                                      {'name': u'Rated Power Consumption',
                                       'pyname': u'rated_power_consumption',
                                       'required-field': False,
                                       'autosizable': True,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'W'}),
                                     (u'motor efficiency',
                                      {'name': u'Motor Efficiency',
                                       'pyname': u'motor_efficiency',
                                       'default': 0.9,
                                       'minimum>': 0.0,
                                       'maximum': 1.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'fraction of motor inefficiencies to fluid stream',
                                      {'name': u'Fraction of Motor Inefficiencies to Fluid Stream',
                                       'pyname': u'fraction_of_motor_inefficiencies_to_fluid_stream',
                                       'default': 0.0,
                                       'maximum': 1.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': 'real'}),
                                     (u'coefficient 1 of the part load performance curve',
                                      {'name': u'Coefficient 1 of the Part Load Performance Curve',
                                       'pyname': u'coefficient_1_of_the_part_load_performance_curve',
                                       'default': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real'}),
                                     (u'coefficient 2 of the part load performance curve',
                                      {'name': u'Coefficient 2 of the Part Load Performance Curve',
                                       'pyname': u'coefficient_2_of_the_part_load_performance_curve',
                                       'default': 1.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real'}),
                                     (u'coefficient 3 of the part load performance curve',
                                      {'name': u'Coefficient 3 of the Part Load Performance Curve',
                                       'pyname': u'coefficient_3_of_the_part_load_performance_curve',
                                       'default': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real'}),
                                     (u'coefficient 4 of the part load performance curve',
                                      {'name': u'Coefficient 4 of the Part Load Performance Curve',
                                       'pyname': u'coefficient_4_of_the_part_load_performance_curve',
                                       'default': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real'}),
                                     (u'pump flow rate schedule name',
                                      {'name': u'Pump Flow Rate Schedule Name',
                                       'pyname': u'pump_flow_rate_schedule_name',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'zone name',
                                      {'name': u'Zone Name',
                                       'pyname': u'zone_name',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'Object-list'}),
                                     (u'skin loss radiative fraction',
                                      {'name': u'Skin Loss Radiative Fraction',
                                       'pyname': u'skin_loss_radiative_fraction',
                                       'maximum': 1.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': u'real'})]),
              'format': None,
              'group': u'Pumps',
              'min-fields': 13,
              'name': u'Pump:VariableSpeed:Condensate',
              'pyname': u'PumpVariableSpeedCondensate',
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
    def rated_flow_rate(self):
        """Get rated_flow_rate.

        Returns:
            float: the value of `rated_flow_rate` or None if not set

        """
        return self["Rated Flow Rate"]

    @rated_flow_rate.setter
    def rated_flow_rate(self, value=None):
        """Corresponds to IDD field `Rated Flow Rate`

        Args:
            value (float or "Autosize"): value for IDD Field `Rated Flow Rate`
                Units: m3/s
                IP-Units: gal/min
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Rated Flow Rate"] = value

    @property
    def rated_pump_head(self):
        """Get rated_pump_head.

        Returns:
            float: the value of `rated_pump_head` or None if not set

        """
        return self["Rated Pump Head"]

    @rated_pump_head.setter
    def rated_pump_head(self, value=179352.0):
        """Corresponds to IDD field `Rated Pump Head` default head is 60 feet.

        Args:
            value (float): value for IDD Field `Rated Pump Head`
                Units: Pa
                IP-Units: ftH2O
                Default value: 179352.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Rated Pump Head"] = value

    @property
    def rated_power_consumption(self):
        """Get rated_power_consumption.

        Returns:
            float: the value of `rated_power_consumption` or None if not set

        """
        return self["Rated Power Consumption"]

    @rated_power_consumption.setter
    def rated_power_consumption(self, value=None):
        """  Corresponds to IDD field `Rated Power Consumption`
        If this field is autosized, an impeller efficiency of 0.78 is assumed.
        autosized Rated Power Consumption = Rated Flow Rate * Rated Pump Head / (0.78 * Motor Efficiency)

        Args:
            value (float or "Autosize"): value for IDD Field `Rated Power Consumption`
                Units: W
                IP-Units: W
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Rated Power Consumption"] = value

    @property
    def motor_efficiency(self):
        """Get motor_efficiency.

        Returns:
            float: the value of `motor_efficiency` or None if not set

        """
        return self["Motor Efficiency"]

    @motor_efficiency.setter
    def motor_efficiency(self, value=0.9):
        """  Corresponds to IDD field `Motor Efficiency`
        This is the motor efficiency only. When the Rated Power Consumption if autosized,
        an impeller efficiency of 0.78 is assumed in addition to the motor efficiency.

        Args:
            value (float): value for IDD Field `Motor Efficiency`
                Default value: 0.9
                value <= 1.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Motor Efficiency"] = value

    @property
    def fraction_of_motor_inefficiencies_to_fluid_stream(self):
        """Get fraction_of_motor_inefficiencies_to_fluid_stream.

        Returns:
            float: the value of `fraction_of_motor_inefficiencies_to_fluid_stream` or None if not set

        """
        return self["Fraction of Motor Inefficiencies to Fluid Stream"]

    @fraction_of_motor_inefficiencies_to_fluid_stream.setter
    def fraction_of_motor_inefficiencies_to_fluid_stream(self, value=None):
        """Corresponds to IDD field `Fraction of Motor Inefficiencies to Fluid
        Stream`

        Args:
            value (float): value for IDD Field `Fraction of Motor Inefficiencies to Fluid Stream`
                value <= 1.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Fraction of Motor Inefficiencies to Fluid Stream"] = value

    @property
    def coefficient_1_of_the_part_load_performance_curve(self):
        """Get coefficient_1_of_the_part_load_performance_curve.

        Returns:
            float: the value of `coefficient_1_of_the_part_load_performance_curve` or None if not set

        """
        return self["Coefficient 1 of the Part Load Performance Curve"]

    @coefficient_1_of_the_part_load_performance_curve.setter
    def coefficient_1_of_the_part_load_performance_curve(self, value=None):
        """Corresponds to IDD field `Coefficient 1 of the Part Load Performance
        Curve`

        Args:
            value (float): value for IDD Field `Coefficient 1 of the Part Load Performance Curve`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient 1 of the Part Load Performance Curve"] = value

    @property
    def coefficient_2_of_the_part_load_performance_curve(self):
        """Get coefficient_2_of_the_part_load_performance_curve.

        Returns:
            float: the value of `coefficient_2_of_the_part_load_performance_curve` or None if not set

        """
        return self["Coefficient 2 of the Part Load Performance Curve"]

    @coefficient_2_of_the_part_load_performance_curve.setter
    def coefficient_2_of_the_part_load_performance_curve(self, value=1.0):
        """Corresponds to IDD field `Coefficient 2 of the Part Load Performance
        Curve`

        Args:
            value (float): value for IDD Field `Coefficient 2 of the Part Load Performance Curve`
                Default value: 1.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient 2 of the Part Load Performance Curve"] = value

    @property
    def coefficient_3_of_the_part_load_performance_curve(self):
        """Get coefficient_3_of_the_part_load_performance_curve.

        Returns:
            float: the value of `coefficient_3_of_the_part_load_performance_curve` or None if not set

        """
        return self["Coefficient 3 of the Part Load Performance Curve"]

    @coefficient_3_of_the_part_load_performance_curve.setter
    def coefficient_3_of_the_part_load_performance_curve(self, value=None):
        """Corresponds to IDD field `Coefficient 3 of the Part Load Performance
        Curve`

        Args:
            value (float): value for IDD Field `Coefficient 3 of the Part Load Performance Curve`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient 3 of the Part Load Performance Curve"] = value

    @property
    def coefficient_4_of_the_part_load_performance_curve(self):
        """Get coefficient_4_of_the_part_load_performance_curve.

        Returns:
            float: the value of `coefficient_4_of_the_part_load_performance_curve` or None if not set

        """
        return self["Coefficient 4 of the Part Load Performance Curve"]

    @coefficient_4_of_the_part_load_performance_curve.setter
    def coefficient_4_of_the_part_load_performance_curve(self, value=None):
        """Corresponds to IDD field `Coefficient 4 of the Part Load Performance
        Curve`

        Args:
            value (float): value for IDD Field `Coefficient 4 of the Part Load Performance Curve`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient 4 of the Part Load Performance Curve"] = value

    @property
    def pump_flow_rate_schedule_name(self):
        """Get pump_flow_rate_schedule_name.

        Returns:
            str: the value of `pump_flow_rate_schedule_name` or None if not set

        """
        return self["Pump Flow Rate Schedule Name"]

    @pump_flow_rate_schedule_name.setter
    def pump_flow_rate_schedule_name(self, value=None):
        """Corresponds to IDD field `Pump Flow Rate Schedule Name` Modifies the
        rated flow rate of the pump on a time basis. Default is that the pump
        is on and runs according to its other operational requirements
        specified above.  The schedule is for special pump operations.

        Args:
            value (str): value for IDD Field `Pump Flow Rate Schedule Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Pump Flow Rate Schedule Name"] = value

    @property
    def zone_name(self):
        """Get zone_name.

        Returns:
            str: the value of `zone_name` or None if not set

        """
        return self["Zone Name"]

    @zone_name.setter
    def zone_name(self, value=None):
        """Corresponds to IDD field `Zone Name` optional, if used pump losses
        transfered to zone as internal gains.

        Args:
            value (str): value for IDD Field `Zone Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Zone Name"] = value

    @property
    def skin_loss_radiative_fraction(self):
        """Get skin_loss_radiative_fraction.

        Returns:
            float: the value of `skin_loss_radiative_fraction` or None if not set

        """
        return self["Skin Loss Radiative Fraction"]

    @skin_loss_radiative_fraction.setter
    def skin_loss_radiative_fraction(self, value=None):
        """Corresponds to IDD field `Skin Loss Radiative Fraction` optional. If
        zone identified in previous field then this determines the split
        between convection and radiation for the skin losses.

        Args:
            value (float): value for IDD Field `Skin Loss Radiative Fraction`
                value <= 1.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Skin Loss Radiative Fraction"] = value




class HeaderedPumpsConstantSpeed(DataObject):

    """ Corresponds to IDD object `HeaderedPumps:ConstantSpeed`
        This Headered pump object describes a pump bank with more than 1 pump in parallel
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
                                     (u'total rated flow rate',
                                      {'name': u'Total Rated Flow Rate',
                                       'pyname': u'total_rated_flow_rate',
                                       'minimum>': 0.0,
                                       'required-field': False,
                                       'autosizable': True,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm3/s'}),
                                     (u'number of pumps in bank',
                                      {'name': u'Number of Pumps in Bank',
                                       'pyname': u'number_of_pumps_in_bank',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'integer'}),
                                     (u'flow sequencing control scheme',
                                      {'name': u'Flow Sequencing Control Scheme',
                                       'pyname': u'flow_sequencing_control_scheme',
                                       'default': u'Sequential',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'Sequential'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'rated pump head',
                                      {'name': u'Rated Pump Head',
                                       'pyname': u'rated_pump_head',
                                       'default': 179352.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'Pa'}),
                                     (u'rated power consumption',
                                      {'name': u'Rated Power Consumption',
                                       'pyname': u'rated_power_consumption',
                                       'required-field': False,
                                       'autosizable': True,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'W'}),
                                     (u'motor efficiency',
                                      {'name': u'Motor Efficiency',
                                       'pyname': u'motor_efficiency',
                                       'default': 0.9,
                                       'minimum>': 0.0,
                                       'maximum': 1.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'fraction of motor inefficiencies to fluid stream',
                                      {'name': u'Fraction of Motor Inefficiencies to Fluid Stream',
                                       'pyname': u'fraction_of_motor_inefficiencies_to_fluid_stream',
                                       'default': 0.0,
                                       'maximum': 1.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': 'real'}),
                                     (u'pump control type',
                                      {'name': u'Pump Control Type',
                                       'pyname': u'pump_control_type',
                                       'default': u'Continuous',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'Continuous',
                                                           u'Intermittent'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'pump flow rate schedule name',
                                      {'name': u'Pump Flow Rate Schedule Name',
                                       'pyname': u'pump_flow_rate_schedule_name',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'zone name',
                                      {'name': u'Zone Name',
                                       'pyname': u'zone_name',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'Object-list'}),
                                     (u'skin loss radiative fraction',
                                      {'name': u'Skin Loss Radiative Fraction',
                                       'pyname': u'skin_loss_radiative_fraction',
                                       'maximum': 1.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': u'real'})]),
              'format': None,
              'group': u'Pumps',
              'min-fields': 9,
              'name': u'HeaderedPumps:ConstantSpeed',
              'pyname': u'HeaderedPumpsConstantSpeed',
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
    def total_rated_flow_rate(self):
        """Get total_rated_flow_rate.

        Returns:
            float: the value of `total_rated_flow_rate` or None if not set

        """
        return self["Total Rated Flow Rate"]

    @total_rated_flow_rate.setter
    def total_rated_flow_rate(self, value=None):
        """Corresponds to IDD field `Total Rated Flow Rate` If the field is not
        autosized set to the flow rate to the total flow when all pumps are
        running at full load.

        Args:
            value (float or "Autosize"): value for IDD Field `Total Rated Flow Rate`
                Units: m3/s
                IP-Units: gal/min
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Total Rated Flow Rate"] = value

    @property
    def number_of_pumps_in_bank(self):
        """Get number_of_pumps_in_bank.

        Returns:
            int: the value of `number_of_pumps_in_bank` or None if not set

        """
        return self["Number of Pumps in Bank"]

    @number_of_pumps_in_bank.setter
    def number_of_pumps_in_bank(self, value=None):
        """Corresponds to IDD field `Number of Pumps in Bank`

        Args:
            value (int): value for IDD Field `Number of Pumps in Bank`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Number of Pumps in Bank"] = value

    @property
    def flow_sequencing_control_scheme(self):
        """Get flow_sequencing_control_scheme.

        Returns:
            str: the value of `flow_sequencing_control_scheme` or None if not set

        """
        return self["Flow Sequencing Control Scheme"]

    @flow_sequencing_control_scheme.setter
    def flow_sequencing_control_scheme(self, value="Sequential"):
        """Corresponds to IDD field `Flow Sequencing Control Scheme`

        Args:
            value (str): value for IDD Field `Flow Sequencing Control Scheme`
                Default value: Sequential
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Flow Sequencing Control Scheme"] = value

    @property
    def rated_pump_head(self):
        """Get rated_pump_head.

        Returns:
            float: the value of `rated_pump_head` or None if not set

        """
        return self["Rated Pump Head"]

    @rated_pump_head.setter
    def rated_pump_head(self, value=179352.0):
        """Corresponds to IDD field `Rated Pump Head` default head is 60 feet.

        Args:
            value (float): value for IDD Field `Rated Pump Head`
                Units: Pa
                IP-Units: ftH2O
                Default value: 179352.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Rated Pump Head"] = value

    @property
    def rated_power_consumption(self):
        """Get rated_power_consumption.

        Returns:
            float: the value of `rated_power_consumption` or None if not set

        """
        return self["Rated Power Consumption"]

    @rated_power_consumption.setter
    def rated_power_consumption(self, value=None):
        """  Corresponds to IDD field `Rated Power Consumption`
        If the field is not autosized set to the power consumed by the pump bank
        when all the pumps are running at nominal flow
        If this field is autosized, an impeller efficiency of 0.78 is assumed.
        autosized Rated Power Consumption = Total Rated Flow Rate * Rated Pump Head / (0.78 * Motor Efficiency)

        Args:
            value (float or "Autosize"): value for IDD Field `Rated Power Consumption`
                Units: W
                IP-Units: W
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Rated Power Consumption"] = value

    @property
    def motor_efficiency(self):
        """Get motor_efficiency.

        Returns:
            float: the value of `motor_efficiency` or None if not set

        """
        return self["Motor Efficiency"]

    @motor_efficiency.setter
    def motor_efficiency(self, value=0.9):
        """  Corresponds to IDD field `Motor Efficiency`
        This is the motor efficiency only. When the Rated Power Consumption if autosized,
        an impeller efficiency of 0.78 is assumed in addition to the motor efficiency.

        Args:
            value (float): value for IDD Field `Motor Efficiency`
                Default value: 0.9
                value <= 1.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Motor Efficiency"] = value

    @property
    def fraction_of_motor_inefficiencies_to_fluid_stream(self):
        """Get fraction_of_motor_inefficiencies_to_fluid_stream.

        Returns:
            float: the value of `fraction_of_motor_inefficiencies_to_fluid_stream` or None if not set

        """
        return self["Fraction of Motor Inefficiencies to Fluid Stream"]

    @fraction_of_motor_inefficiencies_to_fluid_stream.setter
    def fraction_of_motor_inefficiencies_to_fluid_stream(self, value=None):
        """Corresponds to IDD field `Fraction of Motor Inefficiencies to Fluid
        Stream`

        Args:
            value (float): value for IDD Field `Fraction of Motor Inefficiencies to Fluid Stream`
                value <= 1.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Fraction of Motor Inefficiencies to Fluid Stream"] = value

    @property
    def pump_control_type(self):
        """Get pump_control_type.

        Returns:
            str: the value of `pump_control_type` or None if not set

        """
        return self["Pump Control Type"]

    @pump_control_type.setter
    def pump_control_type(self, value="Continuous"):
        """Corresponds to IDD field `Pump Control Type`

        Args:
            value (str): value for IDD Field `Pump Control Type`
                Default value: Continuous
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Pump Control Type"] = value

    @property
    def pump_flow_rate_schedule_name(self):
        """Get pump_flow_rate_schedule_name.

        Returns:
            str: the value of `pump_flow_rate_schedule_name` or None if not set

        """
        return self["Pump Flow Rate Schedule Name"]

    @pump_flow_rate_schedule_name.setter
    def pump_flow_rate_schedule_name(self, value=None):
        """Corresponds to IDD field `Pump Flow Rate Schedule Name` Modifies the
        rated flow rate of the pump on a time basis. Default is that the pump
        is on and runs according to its other operational requirements
        specified above.  The schedule is for special pump operations.

        Args:
            value (str): value for IDD Field `Pump Flow Rate Schedule Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Pump Flow Rate Schedule Name"] = value

    @property
    def zone_name(self):
        """Get zone_name.

        Returns:
            str: the value of `zone_name` or None if not set

        """
        return self["Zone Name"]

    @zone_name.setter
    def zone_name(self, value=None):
        """Corresponds to IDD field `Zone Name` optional, if used pump losses
        transfered to zone as internal gains.

        Args:
            value (str): value for IDD Field `Zone Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Zone Name"] = value

    @property
    def skin_loss_radiative_fraction(self):
        """Get skin_loss_radiative_fraction.

        Returns:
            float: the value of `skin_loss_radiative_fraction` or None if not set

        """
        return self["Skin Loss Radiative Fraction"]

    @skin_loss_radiative_fraction.setter
    def skin_loss_radiative_fraction(self, value=None):
        """Corresponds to IDD field `Skin Loss Radiative Fraction` optional. If
        zone identified in previous field then this determines the split
        between convection and radiation for the skin losses.

        Args:
            value (float): value for IDD Field `Skin Loss Radiative Fraction`
                value <= 1.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Skin Loss Radiative Fraction"] = value




class HeaderedPumpsVariableSpeed(DataObject):

    """ Corresponds to IDD object `HeaderedPumps:VariableSpeed`
        This Headered pump object describes a pump bank with more than 1 pump in parallel
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
                                     (u'total rated flow rate',
                                      {'name': u'Total Rated Flow Rate',
                                       'pyname': u'total_rated_flow_rate',
                                       'minimum>': 0.0,
                                       'required-field': False,
                                       'autosizable': True,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm3/s'}),
                                     (u'number of pumps in bank',
                                      {'name': u'Number of Pumps in Bank',
                                       'pyname': u'number_of_pumps_in_bank',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'integer'}),
                                     (u'flow sequencing control scheme',
                                      {'name': u'Flow Sequencing Control Scheme',
                                       'pyname': u'flow_sequencing_control_scheme',
                                       'default': u'Sequential',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'Sequential'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'rated pump head',
                                      {'name': u'Rated Pump Head',
                                       'pyname': u'rated_pump_head',
                                       'default': 179352.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'Pa'}),
                                     (u'rated power consumption',
                                      {'name': u'Rated Power Consumption',
                                       'pyname': u'rated_power_consumption',
                                       'required-field': False,
                                       'autosizable': True,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'W'}),
                                     (u'motor efficiency',
                                      {'name': u'Motor Efficiency',
                                       'pyname': u'motor_efficiency',
                                       'default': 0.9,
                                       'minimum>': 0.0,
                                       'maximum': 1.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'fraction of motor inefficiencies to fluid stream',
                                      {'name': u'Fraction of Motor Inefficiencies to Fluid Stream',
                                       'pyname': u'fraction_of_motor_inefficiencies_to_fluid_stream',
                                       'default': 0.0,
                                       'maximum': 1.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': 'real'}),
                                     (u'coefficient 1 of the part load performance curve',
                                      {'name': u'Coefficient 1 of the Part Load Performance Curve',
                                       'pyname': u'coefficient_1_of_the_part_load_performance_curve',
                                       'default': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real'}),
                                     (u'coefficient 2 of the part load performance curve',
                                      {'name': u'Coefficient 2 of the Part Load Performance Curve',
                                       'pyname': u'coefficient_2_of_the_part_load_performance_curve',
                                       'default': 1.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real'}),
                                     (u'coefficient 3 of the part load performance curve',
                                      {'name': u'Coefficient 3 of the Part Load Performance Curve',
                                       'pyname': u'coefficient_3_of_the_part_load_performance_curve',
                                       'default': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real'}),
                                     (u'coefficient 4 of the part load performance curve',
                                      {'name': u'Coefficient 4 of the Part Load Performance Curve',
                                       'pyname': u'coefficient_4_of_the_part_load_performance_curve',
                                       'default': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real'}),
                                     (u'minimum flow rate fraction',
                                      {'name': u'Minimum Flow Rate Fraction',
                                       'pyname': u'minimum_flow_rate_fraction',
                                       'default': 0.0,
                                       'maximum': 1.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': 'real'}),
                                     (u'pump control type',
                                      {'name': u'Pump Control Type',
                                       'pyname': u'pump_control_type',
                                       'default': u'Continuous',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'Continuous',
                                                           u'Intermittent'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'pump flow rate schedule name',
                                      {'name': u'Pump Flow Rate Schedule Name',
                                       'pyname': u'pump_flow_rate_schedule_name',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'zone name',
                                      {'name': u'Zone Name',
                                       'pyname': u'zone_name',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'Object-list'}),
                                     (u'skin loss radiative fraction',
                                      {'name': u'Skin Loss Radiative Fraction',
                                       'pyname': u'skin_loss_radiative_fraction',
                                       'maximum': 1.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': u'real'})]),
              'format': None,
              'group': u'Pumps',
              'min-fields': 14,
              'name': u'HeaderedPumps:VariableSpeed',
              'pyname': u'HeaderedPumpsVariableSpeed',
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
    def total_rated_flow_rate(self):
        """Get total_rated_flow_rate.

        Returns:
            float: the value of `total_rated_flow_rate` or None if not set

        """
        return self["Total Rated Flow Rate"]

    @total_rated_flow_rate.setter
    def total_rated_flow_rate(self, value=None):
        """Corresponds to IDD field `Total Rated Flow Rate` If the field is not
        autosized set to the flow rate to the total flow when all pumps are
        running at full load.

        Args:
            value (float or "Autosize"): value for IDD Field `Total Rated Flow Rate`
                Units: m3/s
                IP-Units: gal/min
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Total Rated Flow Rate"] = value

    @property
    def number_of_pumps_in_bank(self):
        """Get number_of_pumps_in_bank.

        Returns:
            int: the value of `number_of_pumps_in_bank` or None if not set

        """
        return self["Number of Pumps in Bank"]

    @number_of_pumps_in_bank.setter
    def number_of_pumps_in_bank(self, value=None):
        """Corresponds to IDD field `Number of Pumps in Bank`

        Args:
            value (int): value for IDD Field `Number of Pumps in Bank`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Number of Pumps in Bank"] = value

    @property
    def flow_sequencing_control_scheme(self):
        """Get flow_sequencing_control_scheme.

        Returns:
            str: the value of `flow_sequencing_control_scheme` or None if not set

        """
        return self["Flow Sequencing Control Scheme"]

    @flow_sequencing_control_scheme.setter
    def flow_sequencing_control_scheme(self, value="Sequential"):
        """Corresponds to IDD field `Flow Sequencing Control Scheme`

        Args:
            value (str): value for IDD Field `Flow Sequencing Control Scheme`
                Default value: Sequential
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Flow Sequencing Control Scheme"] = value

    @property
    def rated_pump_head(self):
        """Get rated_pump_head.

        Returns:
            float: the value of `rated_pump_head` or None if not set

        """
        return self["Rated Pump Head"]

    @rated_pump_head.setter
    def rated_pump_head(self, value=179352.0):
        """Corresponds to IDD field `Rated Pump Head` default head is 60 feet.

        Args:
            value (float): value for IDD Field `Rated Pump Head`
                Units: Pa
                IP-Units: ftH2O
                Default value: 179352.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Rated Pump Head"] = value

    @property
    def rated_power_consumption(self):
        """Get rated_power_consumption.

        Returns:
            float: the value of `rated_power_consumption` or None if not set

        """
        return self["Rated Power Consumption"]

    @rated_power_consumption.setter
    def rated_power_consumption(self, value=None):
        """  Corresponds to IDD field `Rated Power Consumption`
        If the field is not autosized set to the power consumed by the pump bank
        when all the pumps are running at nominal flow
        If this field is autosized, an impeller efficiency of 0.78 is assumed.
        autosized Rated Power Consumption = Total Rated Flow Rate * Rated Pump Head / (0.78 * Motor Efficiency)

        Args:
            value (float or "Autosize"): value for IDD Field `Rated Power Consumption`
                Units: W
                IP-Units: W
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Rated Power Consumption"] = value

    @property
    def motor_efficiency(self):
        """Get motor_efficiency.

        Returns:
            float: the value of `motor_efficiency` or None if not set

        """
        return self["Motor Efficiency"]

    @motor_efficiency.setter
    def motor_efficiency(self, value=0.9):
        """  Corresponds to IDD field `Motor Efficiency`
        This is the motor efficiency only. When the Rated Power Consumption if autosized,
        an impeller efficiency of 0.78 is assumed in addition to the motor efficiency.

        Args:
            value (float): value for IDD Field `Motor Efficiency`
                Default value: 0.9
                value <= 1.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Motor Efficiency"] = value

    @property
    def fraction_of_motor_inefficiencies_to_fluid_stream(self):
        """Get fraction_of_motor_inefficiencies_to_fluid_stream.

        Returns:
            float: the value of `fraction_of_motor_inefficiencies_to_fluid_stream` or None if not set

        """
        return self["Fraction of Motor Inefficiencies to Fluid Stream"]

    @fraction_of_motor_inefficiencies_to_fluid_stream.setter
    def fraction_of_motor_inefficiencies_to_fluid_stream(self, value=None):
        """Corresponds to IDD field `Fraction of Motor Inefficiencies to Fluid
        Stream`

        Args:
            value (float): value for IDD Field `Fraction of Motor Inefficiencies to Fluid Stream`
                value <= 1.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Fraction of Motor Inefficiencies to Fluid Stream"] = value

    @property
    def coefficient_1_of_the_part_load_performance_curve(self):
        """Get coefficient_1_of_the_part_load_performance_curve.

        Returns:
            float: the value of `coefficient_1_of_the_part_load_performance_curve` or None if not set

        """
        return self["Coefficient 1 of the Part Load Performance Curve"]

    @coefficient_1_of_the_part_load_performance_curve.setter
    def coefficient_1_of_the_part_load_performance_curve(self, value=None):
        """Corresponds to IDD field `Coefficient 1 of the Part Load Performance
        Curve`

        Args:
            value (float): value for IDD Field `Coefficient 1 of the Part Load Performance Curve`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient 1 of the Part Load Performance Curve"] = value

    @property
    def coefficient_2_of_the_part_load_performance_curve(self):
        """Get coefficient_2_of_the_part_load_performance_curve.

        Returns:
            float: the value of `coefficient_2_of_the_part_load_performance_curve` or None if not set

        """
        return self["Coefficient 2 of the Part Load Performance Curve"]

    @coefficient_2_of_the_part_load_performance_curve.setter
    def coefficient_2_of_the_part_load_performance_curve(self, value=1.0):
        """Corresponds to IDD field `Coefficient 2 of the Part Load Performance
        Curve`

        Args:
            value (float): value for IDD Field `Coefficient 2 of the Part Load Performance Curve`
                Default value: 1.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient 2 of the Part Load Performance Curve"] = value

    @property
    def coefficient_3_of_the_part_load_performance_curve(self):
        """Get coefficient_3_of_the_part_load_performance_curve.

        Returns:
            float: the value of `coefficient_3_of_the_part_load_performance_curve` or None if not set

        """
        return self["Coefficient 3 of the Part Load Performance Curve"]

    @coefficient_3_of_the_part_load_performance_curve.setter
    def coefficient_3_of_the_part_load_performance_curve(self, value=None):
        """Corresponds to IDD field `Coefficient 3 of the Part Load Performance
        Curve`

        Args:
            value (float): value for IDD Field `Coefficient 3 of the Part Load Performance Curve`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient 3 of the Part Load Performance Curve"] = value

    @property
    def coefficient_4_of_the_part_load_performance_curve(self):
        """Get coefficient_4_of_the_part_load_performance_curve.

        Returns:
            float: the value of `coefficient_4_of_the_part_load_performance_curve` or None if not set

        """
        return self["Coefficient 4 of the Part Load Performance Curve"]

    @coefficient_4_of_the_part_load_performance_curve.setter
    def coefficient_4_of_the_part_load_performance_curve(self, value=None):
        """Corresponds to IDD field `Coefficient 4 of the Part Load Performance
        Curve`

        Args:
            value (float): value for IDD Field `Coefficient 4 of the Part Load Performance Curve`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Coefficient 4 of the Part Load Performance Curve"] = value

    @property
    def minimum_flow_rate_fraction(self):
        """Get minimum_flow_rate_fraction.

        Returns:
            float: the value of `minimum_flow_rate_fraction` or None if not set

        """
        return self["Minimum Flow Rate Fraction"]

    @minimum_flow_rate_fraction.setter
    def minimum_flow_rate_fraction(self, value=None):
        """Corresponds to IDD field `Minimum Flow Rate Fraction` This value can
        be zero and will be defaulted to that if not specified.

        Args:
            value (float): value for IDD Field `Minimum Flow Rate Fraction`
                value <= 1.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Minimum Flow Rate Fraction"] = value

    @property
    def pump_control_type(self):
        """Get pump_control_type.

        Returns:
            str: the value of `pump_control_type` or None if not set

        """
        return self["Pump Control Type"]

    @pump_control_type.setter
    def pump_control_type(self, value="Continuous"):
        """Corresponds to IDD field `Pump Control Type`

        Args:
            value (str): value for IDD Field `Pump Control Type`
                Default value: Continuous
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Pump Control Type"] = value

    @property
    def pump_flow_rate_schedule_name(self):
        """Get pump_flow_rate_schedule_name.

        Returns:
            str: the value of `pump_flow_rate_schedule_name` or None if not set

        """
        return self["Pump Flow Rate Schedule Name"]

    @pump_flow_rate_schedule_name.setter
    def pump_flow_rate_schedule_name(self, value=None):
        """Corresponds to IDD field `Pump Flow Rate Schedule Name` Modifies the
        rated flow rate of the pump on a time basis. Default is that the pump
        is on and runs according to its other operational requirements
        specified above.  The schedule is for special pump operations.

        Args:
            value (str): value for IDD Field `Pump Flow Rate Schedule Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Pump Flow Rate Schedule Name"] = value

    @property
    def zone_name(self):
        """Get zone_name.

        Returns:
            str: the value of `zone_name` or None if not set

        """
        return self["Zone Name"]

    @zone_name.setter
    def zone_name(self, value=None):
        """Corresponds to IDD field `Zone Name` optional, if used pump losses
        transfered to zone as internal gains.

        Args:
            value (str): value for IDD Field `Zone Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Zone Name"] = value

    @property
    def skin_loss_radiative_fraction(self):
        """Get skin_loss_radiative_fraction.

        Returns:
            float: the value of `skin_loss_radiative_fraction` or None if not set

        """
        return self["Skin Loss Radiative Fraction"]

    @skin_loss_radiative_fraction.setter
    def skin_loss_radiative_fraction(self, value=None):
        """Corresponds to IDD field `Skin Loss Radiative Fraction` optional. If
        zone identified in previous field then this determines the split
        between convection and radiation for the skin losses.

        Args:
            value (float): value for IDD Field `Skin Loss Radiative Fraction`
                value <= 1.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Skin Loss Radiative Fraction"] = value


