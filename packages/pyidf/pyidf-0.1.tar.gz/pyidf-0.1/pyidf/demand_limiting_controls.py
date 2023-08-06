""" Data objects in group "Demand Limiting Controls"
"""

from collections import OrderedDict
import logging
from pyidf.helper import DataObject

logger = logging.getLogger("pyidf")
logger.addHandler(logging.NullHandler())



class DemandManagerAssignmentList(DataObject):

    """ Corresponds to IDD object `DemandManagerAssignmentList`
        a list of meters that can be reported are available after a run on
        the meter dictionary file (.mdd) if the Output:VariableDictionary has been requested.
    """
    schema = {'min-fields': 0,
              'name': u'DemandManagerAssignmentList',
              'pyname': u'DemandManagerAssignmentList',
              'format': None,
              'fields': OrderedDict([(u'name',
                                      {'name': u'Name',
                                       'pyname': u'name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'alpha'}),
                                     (u'meter name',
                                      {'name': u'Meter Name',
                                       'pyname': u'meter_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'external-list'}),
                                     (u'demand limit schedule name',
                                      {'name': u'Demand Limit Schedule Name',
                                       'pyname': u'demand_limit_schedule_name',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'demand limit safety fraction',
                                      {'name': u'Demand Limit Safety Fraction',
                                       'pyname': u'demand_limit_safety_fraction',
                                       'required-field': True,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'billing period schedule name',
                                      {'name': u'Billing Period Schedule Name',
                                       'pyname': u'billing_period_schedule_name',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'peak period schedule name',
                                      {'name': u'Peak Period Schedule Name',
                                       'pyname': u'peak_period_schedule_name',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'demand window length',
                                      {'name': u'Demand Window Length',
                                       'pyname': u'demand_window_length',
                                       'minimum>': 0,
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'integer',
                                       'unit': u'minutes'}),
                                     (u'demand manager priority',
                                      {'name': u'Demand Manager Priority',
                                       'pyname': u'demand_manager_priority',
                                       'required-field': True,
                                       'autosizable': False,
                                       'accepted-values': [u'Sequential',
                                                           u'All'],
                                       'autocalculatable': False,
                                       'type': 'alpha'})]),
              'extensible-fields': OrderedDict([(u'demandmanager 1 object type',
                                                 {'name': u'DemandManager 1 Object Type',
                                                  'pyname': u'demandmanager_1_object_type',
                                                  'required-field': False,
                                                  'autosizable': False,
                                                  'accepted-values': [u'DemandManager:ExteriorLights',
                                                                      u'DemandManager:Lights',
                                                                      u'DemandManager:ElectricEquipment',
                                                                      u'DemandManager:Thermostats'],
                                                  'autocalculatable': False,
                                                  'type': 'alpha'}),
                                                (u'demandmanager 1 name',
                                                 {'name': u'DemandManager 1 Name',
                                                  'pyname': u'demandmanager_1_name',
                                                  'required-field': False,
                                                  'autosizable': False,
                                                  'autocalculatable': False,
                                                  'type': u'object-list'})]),
              'unique-object': False,
              'required-object': False,
              'group': u'Demand Limiting Controls'}

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
    def meter_name(self):
        """Get meter_name.

        Returns:
            str: the value of `meter_name` or None if not set

        """
        return self["Meter Name"]

    @meter_name.setter
    def meter_name(self, value=None):
        """Corresponds to IDD field `Meter Name`

        Args:
            value (str): value for IDD Field `Meter Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Meter Name"] = value

    @property
    def demand_limit_schedule_name(self):
        """Get demand_limit_schedule_name.

        Returns:
            str: the value of `demand_limit_schedule_name` or None if not set

        """
        return self["Demand Limit Schedule Name"]

    @demand_limit_schedule_name.setter
    def demand_limit_schedule_name(self, value=None):
        """Corresponds to IDD field `Demand Limit Schedule Name`

        Args:
            value (str): value for IDD Field `Demand Limit Schedule Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Demand Limit Schedule Name"] = value

    @property
    def demand_limit_safety_fraction(self):
        """Get demand_limit_safety_fraction.

        Returns:
            float: the value of `demand_limit_safety_fraction` or None if not set

        """
        return self["Demand Limit Safety Fraction"]

    @demand_limit_safety_fraction.setter
    def demand_limit_safety_fraction(self, value=None):
        """Corresponds to IDD field `Demand Limit Safety Fraction`

        Args:
            value (float): value for IDD Field `Demand Limit Safety Fraction`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Demand Limit Safety Fraction"] = value

    @property
    def billing_period_schedule_name(self):
        """Get billing_period_schedule_name.

        Returns:
            str: the value of `billing_period_schedule_name` or None if not set

        """
        return self["Billing Period Schedule Name"]

    @billing_period_schedule_name.setter
    def billing_period_schedule_name(self, value=None):
        """  Corresponds to IDD field `Billing Period Schedule Name`
        This field should reference the same schedule as the month schedule name field of the
        UtilityCost:Tariff object, if used.
        If blank, defaults to regular divisions between months.

        Args:
            value (str): value for IDD Field `Billing Period Schedule Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Billing Period Schedule Name"] = value

    @property
    def peak_period_schedule_name(self):
        """Get peak_period_schedule_name.

        Returns:
            str: the value of `peak_period_schedule_name` or None if not set

        """
        return self["Peak Period Schedule Name"]

    @peak_period_schedule_name.setter
    def peak_period_schedule_name(self, value=None):
        """  Corresponds to IDD field `Peak Period Schedule Name`
        This field should reference the same schedule as the period schedule name field of the
        UtilityCost:Tariff object, if used.
        If blank, defaults to always on peak.

        Args:
            value (str): value for IDD Field `Peak Period Schedule Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Peak Period Schedule Name"] = value

    @property
    def demand_window_length(self):
        """Get demand_window_length.

        Returns:
            int: the value of `demand_window_length` or None if not set

        """
        return self["Demand Window Length"]

    @demand_window_length.setter
    def demand_window_length(self, value=None):
        """Corresponds to IDD field `Demand Window Length`

        Args:
            value (int): value for IDD Field `Demand Window Length`
                Units: minutes
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Demand Window Length"] = value

    @property
    def demand_manager_priority(self):
        """Get demand_manager_priority.

        Returns:
            str: the value of `demand_manager_priority` or None if not set

        """
        return self["Demand Manager Priority"]

    @demand_manager_priority.setter
    def demand_manager_priority(self, value=None):
        """Corresponds to IDD field `Demand Manager Priority`

        Args:
            value (str): value for IDD Field `Demand Manager Priority`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Demand Manager Priority"] = value

    def add_extensible(self,
                       demandmanager_1_object_type=None,
                       demandmanager_1_name=None,
                       ):
        """Add values for extensible fields.

        Args:

            demandmanager_1_object_type (str): value for IDD Field `DemandManager 1 Object Type`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

            demandmanager_1_name (str): value for IDD Field `DemandManager 1 Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        """
        vals = []
        demandmanager_1_object_type = self.check_value(
            "DemandManager 1 Object Type",
            demandmanager_1_object_type)
        vals.append(demandmanager_1_object_type)
        demandmanager_1_name = self.check_value(
            "DemandManager 1 Name",
            demandmanager_1_name)
        vals.append(demandmanager_1_name)
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




class DemandManagerExteriorLights(DataObject):

    """ Corresponds to IDD object `DemandManager:ExteriorLights`
        used for demand limiting Exterior:Lights objects.
    """
    schema = {'min-fields': 0,
              'name': u'DemandManager:ExteriorLights',
              'pyname': u'DemandManagerExteriorLights',
              'format': None,
              'fields': OrderedDict([(u'name',
                                      {'name': u'Name',
                                       'pyname': u'name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'alpha'}),
                                     (u'availability schedule name',
                                      {'name': u'Availability Schedule Name',
                                       'pyname': u'availability_schedule_name',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'limit control',
                                      {'name': u'Limit Control',
                                       'pyname': u'limit_control',
                                       'required-field': True,
                                       'autosizable': False,
                                       'accepted-values': [u'Off',
                                                           u'Fixed'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'minimum limit duration',
                                      {'name': u'Minimum Limit Duration',
                                       'pyname': u'minimum_limit_duration',
                                       'minimum>': 0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'integer',
                                       'unit': u'minutes'}),
                                     (u'maximum limit fraction',
                                      {'name': u'Maximum Limit Fraction',
                                       'pyname': u'maximum_limit_fraction',
                                       'maximum': 1.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'limit step change',
                                      {'name': u'Limit Step Change',
                                       'pyname': u'limit_step_change',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'selection control',
                                      {'name': u'Selection Control',
                                       'pyname': u'selection_control',
                                       'required-field': True,
                                       'autosizable': False,
                                       'accepted-values': [u'All',
                                                           u'RotateMany',
                                                           u'RotateOne'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'rotation duration',
                                      {'name': u'Rotation Duration',
                                       'pyname': u'rotation_duration',
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0,
                                       'autocalculatable': False,
                                       'type': u'integer',
                                       'unit': u'minutes'})]),
              'extensible-fields': OrderedDict([(u'exterior lights 1 name',
                                                 {'name': u'Exterior Lights 1 Name',
                                                  'pyname': u'exterior_lights_1_name',
                                                  'required-field': True,
                                                  'autosizable': False,
                                                  'autocalculatable': False,
                                                  'type': u'object-list'})]),
              'unique-object': False,
              'required-object': False,
              'group': u'Demand Limiting Controls'}

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

        Args:
            value (str): value for IDD Field `Availability Schedule Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Availability Schedule Name"] = value

    @property
    def limit_control(self):
        """Get limit_control.

        Returns:
            str: the value of `limit_control` or None if not set

        """
        return self["Limit Control"]

    @limit_control.setter
    def limit_control(self, value=None):
        """Corresponds to IDD field `Limit Control`

        Args:
            value (str): value for IDD Field `Limit Control`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Limit Control"] = value

    @property
    def minimum_limit_duration(self):
        """Get minimum_limit_duration.

        Returns:
            int: the value of `minimum_limit_duration` or None if not set

        """
        return self["Minimum Limit Duration"]

    @minimum_limit_duration.setter
    def minimum_limit_duration(self, value=None):
        """Corresponds to IDD field `Minimum Limit Duration` If blank, duration
        defaults to the timestep.

        Args:
            value (int): value for IDD Field `Minimum Limit Duration`
                Units: minutes
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Minimum Limit Duration"] = value

    @property
    def maximum_limit_fraction(self):
        """Get maximum_limit_fraction.

        Returns:
            float: the value of `maximum_limit_fraction` or None if not set

        """
        return self["Maximum Limit Fraction"]

    @maximum_limit_fraction.setter
    def maximum_limit_fraction(self, value=None):
        """Corresponds to IDD field `Maximum Limit Fraction`

        Args:
            value (float): value for IDD Field `Maximum Limit Fraction`
                value <= 1.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Maximum Limit Fraction"] = value

    @property
    def limit_step_change(self):
        """Get limit_step_change.

        Returns:
            float: the value of `limit_step_change` or None if not set

        """
        return self["Limit Step Change"]

    @limit_step_change.setter
    def limit_step_change(self, value=None):
        """Corresponds to IDD field `Limit Step Change` Not yet implemented.

        Args:
            value (float): value for IDD Field `Limit Step Change`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Limit Step Change"] = value

    @property
    def selection_control(self):
        """Get selection_control.

        Returns:
            str: the value of `selection_control` or None if not set

        """
        return self["Selection Control"]

    @selection_control.setter
    def selection_control(self, value=None):
        """Corresponds to IDD field `Selection Control`

        Args:
            value (str): value for IDD Field `Selection Control`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Selection Control"] = value

    @property
    def rotation_duration(self):
        """Get rotation_duration.

        Returns:
            int: the value of `rotation_duration` or None if not set

        """
        return self["Rotation Duration"]

    @rotation_duration.setter
    def rotation_duration(self, value=None):
        """Corresponds to IDD field `Rotation Duration` If blank, duration
        defaults to the timestep.

        Args:
            value (int): value for IDD Field `Rotation Duration`
                Units: minutes
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Rotation Duration"] = value

    def add_extensible(self,
                       exterior_lights_1_name=None,
                       ):
        """Add values for extensible fields.

        Args:

            exterior_lights_1_name (str): value for IDD Field `Exterior Lights 1 Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        """
        vals = []
        exterior_lights_1_name = self.check_value(
            "Exterior Lights 1 Name",
            exterior_lights_1_name)
        vals.append(exterior_lights_1_name)
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




class DemandManagerLights(DataObject):

    """ Corresponds to IDD object `DemandManager:Lights`
        used for demand limiting Lights objects.
    """
    schema = {'min-fields': 0,
              'name': u'DemandManager:Lights',
              'pyname': u'DemandManagerLights',
              'format': None,
              'fields': OrderedDict([(u'name',
                                      {'name': u'Name',
                                       'pyname': u'name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'alpha'}),
                                     (u'availability schedule name',
                                      {'name': u'Availability Schedule Name',
                                       'pyname': u'availability_schedule_name',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'limit control',
                                      {'name': u'Limit Control',
                                       'pyname': u'limit_control',
                                       'required-field': True,
                                       'autosizable': False,
                                       'accepted-values': [u'Off',
                                                           u'Fixed'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'minimum limit duration',
                                      {'name': u'Minimum Limit Duration',
                                       'pyname': u'minimum_limit_duration',
                                       'minimum>': 0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'integer',
                                       'unit': u'minutes'}),
                                     (u'maximum limit fraction',
                                      {'name': u'Maximum Limit Fraction',
                                       'pyname': u'maximum_limit_fraction',
                                       'maximum': 1.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'limit step change',
                                      {'name': u'Limit Step Change',
                                       'pyname': u'limit_step_change',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'selection control',
                                      {'name': u'Selection Control',
                                       'pyname': u'selection_control',
                                       'required-field': True,
                                       'autosizable': False,
                                       'accepted-values': [u'All',
                                                           u'RotateMany',
                                                           u'RotateOne'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'rotation duration',
                                      {'name': u'Rotation Duration',
                                       'pyname': u'rotation_duration',
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0,
                                       'autocalculatable': False,
                                       'type': u'integer',
                                       'unit': u'minutes'})]),
              'extensible-fields': OrderedDict([(u'lights 1 name',
                                                 {'name': u'Lights 1 Name',
                                                  'pyname': u'lights_1_name',
                                                  'required-field': True,
                                                  'autosizable': False,
                                                  'autocalculatable': False,
                                                  'type': u'object-list'})]),
              'unique-object': False,
              'required-object': False,
              'group': u'Demand Limiting Controls'}

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

        Args:
            value (str): value for IDD Field `Availability Schedule Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Availability Schedule Name"] = value

    @property
    def limit_control(self):
        """Get limit_control.

        Returns:
            str: the value of `limit_control` or None if not set

        """
        return self["Limit Control"]

    @limit_control.setter
    def limit_control(self, value=None):
        """Corresponds to IDD field `Limit Control`

        Args:
            value (str): value for IDD Field `Limit Control`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Limit Control"] = value

    @property
    def minimum_limit_duration(self):
        """Get minimum_limit_duration.

        Returns:
            int: the value of `minimum_limit_duration` or None if not set

        """
        return self["Minimum Limit Duration"]

    @minimum_limit_duration.setter
    def minimum_limit_duration(self, value=None):
        """Corresponds to IDD field `Minimum Limit Duration` If blank, duration
        defaults to the timestep.

        Args:
            value (int): value for IDD Field `Minimum Limit Duration`
                Units: minutes
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Minimum Limit Duration"] = value

    @property
    def maximum_limit_fraction(self):
        """Get maximum_limit_fraction.

        Returns:
            float: the value of `maximum_limit_fraction` or None if not set

        """
        return self["Maximum Limit Fraction"]

    @maximum_limit_fraction.setter
    def maximum_limit_fraction(self, value=None):
        """Corresponds to IDD field `Maximum Limit Fraction`

        Args:
            value (float): value for IDD Field `Maximum Limit Fraction`
                value <= 1.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Maximum Limit Fraction"] = value

    @property
    def limit_step_change(self):
        """Get limit_step_change.

        Returns:
            float: the value of `limit_step_change` or None if not set

        """
        return self["Limit Step Change"]

    @limit_step_change.setter
    def limit_step_change(self, value=None):
        """Corresponds to IDD field `Limit Step Change` Not yet implemented.

        Args:
            value (float): value for IDD Field `Limit Step Change`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Limit Step Change"] = value

    @property
    def selection_control(self):
        """Get selection_control.

        Returns:
            str: the value of `selection_control` or None if not set

        """
        return self["Selection Control"]

    @selection_control.setter
    def selection_control(self, value=None):
        """Corresponds to IDD field `Selection Control`

        Args:
            value (str): value for IDD Field `Selection Control`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Selection Control"] = value

    @property
    def rotation_duration(self):
        """Get rotation_duration.

        Returns:
            int: the value of `rotation_duration` or None if not set

        """
        return self["Rotation Duration"]

    @rotation_duration.setter
    def rotation_duration(self, value=None):
        """Corresponds to IDD field `Rotation Duration` If blank, duration
        defaults to the timestep.

        Args:
            value (int): value for IDD Field `Rotation Duration`
                Units: minutes
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Rotation Duration"] = value

    def add_extensible(self,
                       lights_1_name=None,
                       ):
        """Add values for extensible fields.

        Args:

            lights_1_name (str): value for IDD Field `Lights 1 Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        """
        vals = []
        lights_1_name = self.check_value("Lights 1 Name", lights_1_name)
        vals.append(lights_1_name)
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




class DemandManagerElectricEquipment(DataObject):

    """ Corresponds to IDD object `DemandManager:ElectricEquipment`
        used for demand limiting ElectricEquipment objects.
    """
    schema = {'min-fields': 0,
              'name': u'DemandManager:ElectricEquipment',
              'pyname': u'DemandManagerElectricEquipment',
              'format': None,
              'fields': OrderedDict([(u'name',
                                      {'name': u'Name',
                                       'pyname': u'name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'alpha'}),
                                     (u'availability schedule name',
                                      {'name': u'Availability Schedule Name',
                                       'pyname': u'availability_schedule_name',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'limit control',
                                      {'name': u'Limit Control',
                                       'pyname': u'limit_control',
                                       'required-field': True,
                                       'autosizable': False,
                                       'accepted-values': [u'Off',
                                                           u'Fixed'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'minimum limit duration',
                                      {'name': u'Minimum Limit Duration',
                                       'pyname': u'minimum_limit_duration',
                                       'minimum>': 0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'integer',
                                       'unit': u'minutes'}),
                                     (u'maximum limit fraction',
                                      {'name': u'Maximum Limit Fraction',
                                       'pyname': u'maximum_limit_fraction',
                                       'maximum': 1.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'limit step change',
                                      {'name': u'Limit Step Change',
                                       'pyname': u'limit_step_change',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'selection control',
                                      {'name': u'Selection Control',
                                       'pyname': u'selection_control',
                                       'required-field': True,
                                       'autosizable': False,
                                       'accepted-values': [u'All',
                                                           u'RotateMany',
                                                           u'RotateOne'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'rotation duration',
                                      {'name': u'Rotation Duration',
                                       'pyname': u'rotation_duration',
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0,
                                       'autocalculatable': False,
                                       'type': u'integer',
                                       'unit': u'minutes'})]),
              'extensible-fields': OrderedDict([(u'electric equipment 1 name',
                                                 {'name': u'Electric Equipment 1 Name',
                                                  'pyname': u'electric_equipment_1_name',
                                                  'required-field': True,
                                                  'autosizable': False,
                                                  'autocalculatable': False,
                                                  'type': u'object-list'})]),
              'unique-object': False,
              'required-object': False,
              'group': u'Demand Limiting Controls'}

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

        Args:
            value (str): value for IDD Field `Availability Schedule Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Availability Schedule Name"] = value

    @property
    def limit_control(self):
        """Get limit_control.

        Returns:
            str: the value of `limit_control` or None if not set

        """
        return self["Limit Control"]

    @limit_control.setter
    def limit_control(self, value=None):
        """Corresponds to IDD field `Limit Control`

        Args:
            value (str): value for IDD Field `Limit Control`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Limit Control"] = value

    @property
    def minimum_limit_duration(self):
        """Get minimum_limit_duration.

        Returns:
            int: the value of `minimum_limit_duration` or None if not set

        """
        return self["Minimum Limit Duration"]

    @minimum_limit_duration.setter
    def minimum_limit_duration(self, value=None):
        """Corresponds to IDD field `Minimum Limit Duration` If blank, duration
        defaults to the timestep.

        Args:
            value (int): value for IDD Field `Minimum Limit Duration`
                Units: minutes
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Minimum Limit Duration"] = value

    @property
    def maximum_limit_fraction(self):
        """Get maximum_limit_fraction.

        Returns:
            float: the value of `maximum_limit_fraction` or None if not set

        """
        return self["Maximum Limit Fraction"]

    @maximum_limit_fraction.setter
    def maximum_limit_fraction(self, value=None):
        """Corresponds to IDD field `Maximum Limit Fraction`

        Args:
            value (float): value for IDD Field `Maximum Limit Fraction`
                value <= 1.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Maximum Limit Fraction"] = value

    @property
    def limit_step_change(self):
        """Get limit_step_change.

        Returns:
            float: the value of `limit_step_change` or None if not set

        """
        return self["Limit Step Change"]

    @limit_step_change.setter
    def limit_step_change(self, value=None):
        """Corresponds to IDD field `Limit Step Change` Not yet implemented.

        Args:
            value (float): value for IDD Field `Limit Step Change`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Limit Step Change"] = value

    @property
    def selection_control(self):
        """Get selection_control.

        Returns:
            str: the value of `selection_control` or None if not set

        """
        return self["Selection Control"]

    @selection_control.setter
    def selection_control(self, value=None):
        """Corresponds to IDD field `Selection Control`

        Args:
            value (str): value for IDD Field `Selection Control`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Selection Control"] = value

    @property
    def rotation_duration(self):
        """Get rotation_duration.

        Returns:
            int: the value of `rotation_duration` or None if not set

        """
        return self["Rotation Duration"]

    @rotation_duration.setter
    def rotation_duration(self, value=None):
        """Corresponds to IDD field `Rotation Duration` If blank, duration
        defaults to the timestep.

        Args:
            value (int): value for IDD Field `Rotation Duration`
                Units: minutes
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Rotation Duration"] = value

    def add_extensible(self,
                       electric_equipment_1_name=None,
                       ):
        """Add values for extensible fields.

        Args:

            electric_equipment_1_name (str): value for IDD Field `Electric Equipment 1 Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        """
        vals = []
        electric_equipment_1_name = self.check_value(
            "Electric Equipment 1 Name",
            electric_equipment_1_name)
        vals.append(electric_equipment_1_name)
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




class DemandManagerThermostats(DataObject):

    """ Corresponds to IDD object `DemandManager:Thermostats`
        used for demand limiting ZoneControl:Thermostat objects.
    """
    schema = {'min-fields': 0,
              'name': u'DemandManager:Thermostats',
              'pyname': u'DemandManagerThermostats',
              'format': None,
              'fields': OrderedDict([(u'name',
                                      {'name': u'Name',
                                       'pyname': u'name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'alpha'}),
                                     (u'availability schedule name',
                                      {'name': u'Availability Schedule Name',
                                       'pyname': u'availability_schedule_name',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'reset control',
                                      {'name': u'Reset Control',
                                       'pyname': u'reset_control',
                                       'required-field': True,
                                       'autosizable': False,
                                       'accepted-values': [u'Off',
                                                           u'Fixed'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'minimum reset duration',
                                      {'name': u'Minimum Reset Duration',
                                       'pyname': u'minimum_reset_duration',
                                       'minimum>': 0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'integer',
                                       'unit': u'minutes'}),
                                     (u'maximum heating setpoint reset',
                                      {'name': u'Maximum Heating Setpoint Reset',
                                       'pyname': u'maximum_heating_setpoint_reset',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'C'}),
                                     (u'maximum cooling setpoint reset',
                                      {'name': u'Maximum Cooling Setpoint Reset',
                                       'pyname': u'maximum_cooling_setpoint_reset',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'C'}),
                                     (u'reset step change',
                                      {'name': u'Reset Step Change',
                                       'pyname': u'reset_step_change',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'selection control',
                                      {'name': u'Selection Control',
                                       'pyname': u'selection_control',
                                       'required-field': True,
                                       'autosizable': False,
                                       'accepted-values': [u'All',
                                                           u'RotateMany',
                                                           u'RotateOne'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'rotation duration',
                                      {'name': u'Rotation Duration',
                                       'pyname': u'rotation_duration',
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0,
                                       'autocalculatable': False,
                                       'type': u'integer',
                                       'unit': u'minutes'})]),
              'extensible-fields': OrderedDict([(u'thermostat 1 name',
                                                 {'name': u'Thermostat 1 Name',
                                                  'pyname': u'thermostat_1_name',
                                                  'required-field': True,
                                                  'autosizable': False,
                                                  'autocalculatable': False,
                                                  'type': u'object-list'})]),
              'unique-object': False,
              'required-object': False,
              'group': u'Demand Limiting Controls'}

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

        Args:
            value (str): value for IDD Field `Availability Schedule Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Availability Schedule Name"] = value

    @property
    def reset_control(self):
        """Get reset_control.

        Returns:
            str: the value of `reset_control` or None if not set

        """
        return self["Reset Control"]

    @reset_control.setter
    def reset_control(self, value=None):
        """Corresponds to IDD field `Reset Control`

        Args:
            value (str): value for IDD Field `Reset Control`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Reset Control"] = value

    @property
    def minimum_reset_duration(self):
        """Get minimum_reset_duration.

        Returns:
            int: the value of `minimum_reset_duration` or None if not set

        """
        return self["Minimum Reset Duration"]

    @minimum_reset_duration.setter
    def minimum_reset_duration(self, value=None):
        """Corresponds to IDD field `Minimum Reset Duration` If blank, duration
        defaults to the timestep.

        Args:
            value (int): value for IDD Field `Minimum Reset Duration`
                Units: minutes
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Minimum Reset Duration"] = value

    @property
    def maximum_heating_setpoint_reset(self):
        """Get maximum_heating_setpoint_reset.

        Returns:
            float: the value of `maximum_heating_setpoint_reset` or None if not set

        """
        return self["Maximum Heating Setpoint Reset"]

    @maximum_heating_setpoint_reset.setter
    def maximum_heating_setpoint_reset(self, value=None):
        """Corresponds to IDD field `Maximum Heating Setpoint Reset`

        Args:
            value (float): value for IDD Field `Maximum Heating Setpoint Reset`
                Units: C
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Maximum Heating Setpoint Reset"] = value

    @property
    def maximum_cooling_setpoint_reset(self):
        """Get maximum_cooling_setpoint_reset.

        Returns:
            float: the value of `maximum_cooling_setpoint_reset` or None if not set

        """
        return self["Maximum Cooling Setpoint Reset"]

    @maximum_cooling_setpoint_reset.setter
    def maximum_cooling_setpoint_reset(self, value=None):
        """Corresponds to IDD field `Maximum Cooling Setpoint Reset`

        Args:
            value (float): value for IDD Field `Maximum Cooling Setpoint Reset`
                Units: C
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Maximum Cooling Setpoint Reset"] = value

    @property
    def reset_step_change(self):
        """Get reset_step_change.

        Returns:
            float: the value of `reset_step_change` or None if not set

        """
        return self["Reset Step Change"]

    @reset_step_change.setter
    def reset_step_change(self, value=None):
        """Corresponds to IDD field `Reset Step Change` Not yet implemented.

        Args:
            value (float): value for IDD Field `Reset Step Change`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Reset Step Change"] = value

    @property
    def selection_control(self):
        """Get selection_control.

        Returns:
            str: the value of `selection_control` or None if not set

        """
        return self["Selection Control"]

    @selection_control.setter
    def selection_control(self, value=None):
        """Corresponds to IDD field `Selection Control`

        Args:
            value (str): value for IDD Field `Selection Control`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Selection Control"] = value

    @property
    def rotation_duration(self):
        """Get rotation_duration.

        Returns:
            int: the value of `rotation_duration` or None if not set

        """
        return self["Rotation Duration"]

    @rotation_duration.setter
    def rotation_duration(self, value=None):
        """Corresponds to IDD field `Rotation Duration` If blank, duration
        defaults to the timestep.

        Args:
            value (int): value for IDD Field `Rotation Duration`
                Units: minutes
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Rotation Duration"] = value

    def add_extensible(self,
                       thermostat_1_name=None,
                       ):
        """Add values for extensible fields.

        Args:

            thermostat_1_name (str): value for IDD Field `Thermostat 1 Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        """
        vals = []
        thermostat_1_name = self.check_value(
            "Thermostat 1 Name",
            thermostat_1_name)
        vals.append(thermostat_1_name)
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


