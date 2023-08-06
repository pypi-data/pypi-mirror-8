""" Data objects in group "Node"
"""

from collections import OrderedDict
import logging
from pyidf.helper import DataObject

logger = logging.getLogger("pyidf")
logger.addHandler(logging.NullHandler())



class Branch(DataObject):

    """ Corresponds to IDD object `Branch`
        List components on the branch in simulation and connection order
        Note: this should NOT include splitters or mixers which define
        endpoints of branches
    """
    schema = {'min-fields': 0,
              'name': u'Branch',
              'pyname': u'Branch',
              'format': None,
              'fields': OrderedDict([(u'name',
                                      {'name': u'Name',
                                       'pyname': u'name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'maximum flow rate',
                                      {'name': u'Maximum Flow Rate',
                                       'pyname': u'maximum_flow_rate',
                                       'default': 0.0,
                                       'required-field': False,
                                       'autosizable': True,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm3/s'}),
                                     (u'pressure drop curve name',
                                      {'name': u'Pressure Drop Curve Name',
                                       'pyname': u'pressure_drop_curve_name',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'})]),
              'extensible-fields': OrderedDict([(u'component 1 object type',
                                                 {'name': u'Component 1 Object Type',
                                                  'pyname': u'component_1_object_type',
                                                  'required-field': True,
                                                  'autosizable': False,
                                                  'autocalculatable': False,
                                                  'type': 'alpha'}),
                                                (u'component 1 name',
                                                 {'name': u'Component 1 Name',
                                                  'pyname': u'component_1_name',
                                                  'required-field': True,
                                                  'autosizable': False,
                                                  'autocalculatable': False,
                                                  'type': 'alpha'}),
                                                (u'component 1 inlet node name',
                                                 {'name': u'Component 1 Inlet Node Name',
                                                  'pyname': u'component_1_inlet_node_name',
                                                  'required-field': True,
                                                  'autosizable': False,
                                                  'autocalculatable': False,
                                                  'type': u'node'}),
                                                (u'component 1 outlet node name',
                                                 {'name': u'Component 1 Outlet Node Name',
                                                  'pyname': u'component_1_outlet_node_name',
                                                  'required-field': True,
                                                  'autosizable': False,
                                                  'autocalculatable': False,
                                                  'type': u'node'}),
                                                (u'component 1 branch control type',
                                                 {'name': u'Component 1 Branch Control Type',
                                                  'pyname': u'component_1_branch_control_type',
                                                  'required-field': False,
                                                  'autosizable': False,
                                                  'autocalculatable': False,
                                                  'type': 'alpha'})]),
              'unique-object': False,
              'required-object': False,
              'group': u'Node'}

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
            value (float or "Autosize"): value for IDD Field `Maximum Flow Rate`
                Units: m3/s
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Maximum Flow Rate"] = value

    @property
    def pressure_drop_curve_name(self):
        """Get pressure_drop_curve_name.

        Returns:
            str: the value of `pressure_drop_curve_name` or None if not set

        """
        return self["Pressure Drop Curve Name"]

    @pressure_drop_curve_name.setter
    def pressure_drop_curve_name(self, value=None):
        """  Corresponds to IDD field `Pressure Drop Curve Name`
        Optional field to include this branch in plant pressure drop calculations
        This field is only relevant for branches in PlantLoops and CondenserLoops
        Air loops do not account for pressure drop using this field
        Valid curve types are: Curve:Functional:PressureDrop or
        one of Curve:{Linear,Quadratic,Cubic,Exponent}')
        Table:OneIndependentVariable object can also be used

        Args:
            value (str): value for IDD Field `Pressure Drop Curve Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Pressure Drop Curve Name"] = value

    def add_extensible(self,
                       component_1_object_type=None,
                       component_1_name=None,
                       component_1_inlet_node_name=None,
                       component_1_outlet_node_name=None,
                       component_1_branch_control_type=None,
                       ):
        """Add values for extensible fields.

        Args:

            component_1_object_type (str): value for IDD Field `Component 1 Object Type`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

            component_1_name (str): value for IDD Field `Component 1 Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

            component_1_inlet_node_name (str): value for IDD Field `Component 1 Inlet Node Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

            component_1_outlet_node_name (str): value for IDD Field `Component 1 Outlet Node Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

            component_1_branch_control_type (str): value for IDD Field `Component 1 Branch Control Type`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        """
        vals = []
        component_1_object_type = self.check_value(
            "Component 1 Object Type",
            component_1_object_type)
        vals.append(component_1_object_type)
        component_1_name = self.check_value(
            "Component 1 Name",
            component_1_name)
        vals.append(component_1_name)
        component_1_inlet_node_name = self.check_value(
            "Component 1 Inlet Node Name",
            component_1_inlet_node_name)
        vals.append(component_1_inlet_node_name)
        component_1_outlet_node_name = self.check_value(
            "Component 1 Outlet Node Name",
            component_1_outlet_node_name)
        vals.append(component_1_outlet_node_name)
        component_1_branch_control_type = self.check_value(
            "Component 1 Branch Control Type",
            component_1_branch_control_type)
        vals.append(component_1_branch_control_type)
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




class ConnectorSplitter(DataObject):

    """ Corresponds to IDD object `Connector:Splitter`
        Split one air/water stream into N outlet streams.  Branch names cannot be duplicated
        within a single Splitter list.
    """
    schema = {'min-fields': 3,
              'name': u'Connector:Splitter',
              'pyname': u'ConnectorSplitter',
              'format': None,
              'fields': OrderedDict([(u'name',
                                      {'name': u'Name',
                                       'pyname': u'name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'inlet branch name',
                                      {'name': u'Inlet Branch Name',
                                       'pyname': u'inlet_branch_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'})]),
              'extensible-fields': OrderedDict([(u'outlet branch name',
                                                 {'name': u'Outlet Branch Name',
                                                  'pyname': u'outlet_branch_name',
                                                  'required-field': False,
                                                  'autosizable': False,
                                                  'autocalculatable': False,
                                                  'type': u'object-list'})]),
              'unique-object': False,
              'required-object': False,
              'group': u'Node'}

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
    def inlet_branch_name(self):
        """Get inlet_branch_name.

        Returns:
            str: the value of `inlet_branch_name` or None if not set

        """
        return self["Inlet Branch Name"]

    @inlet_branch_name.setter
    def inlet_branch_name(self, value=None):
        """Corresponds to IDD field `Inlet Branch Name`

        Args:
            value (str): value for IDD Field `Inlet Branch Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Inlet Branch Name"] = value

    def add_extensible(self,
                       outlet_branch_name=None,
                       ):
        """Add values for extensible fields.

        Args:

            outlet_branch_name (str): value for IDD Field `Outlet Branch Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        """
        vals = []
        outlet_branch_name = self.check_value(
            "Outlet Branch Name",
            outlet_branch_name)
        vals.append(outlet_branch_name)
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




class ConnectorMixer(DataObject):

    """ Corresponds to IDD object `Connector:Mixer`
        Mix N inlet air/water streams into one.  Branch names cannot be duplicated within
        a single mixer list.
    """
    schema = {'min-fields': 3,
              'name': u'Connector:Mixer',
              'pyname': u'ConnectorMixer',
              'format': None,
              'fields': OrderedDict([(u'name',
                                      {'name': u'Name',
                                       'pyname': u'name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'outlet branch name',
                                      {'name': u'Outlet Branch Name',
                                       'pyname': u'outlet_branch_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'})]),
              'extensible-fields': OrderedDict([(u'inlet branch name',
                                                 {'name': u'Inlet Branch Name',
                                                  'pyname': u'inlet_branch_name',
                                                  'required-field': False,
                                                  'autosizable': False,
                                                  'autocalculatable': False,
                                                  'type': u'object-list'})]),
              'unique-object': False,
              'required-object': False,
              'group': u'Node'}

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
    def outlet_branch_name(self):
        """Get outlet_branch_name.

        Returns:
            str: the value of `outlet_branch_name` or None if not set

        """
        return self["Outlet Branch Name"]

    @outlet_branch_name.setter
    def outlet_branch_name(self, value=None):
        """Corresponds to IDD field `Outlet Branch Name`

        Args:
            value (str): value for IDD Field `Outlet Branch Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Outlet Branch Name"] = value

    def add_extensible(self,
                       inlet_branch_name=None,
                       ):
        """Add values for extensible fields.

        Args:

            inlet_branch_name (str): value for IDD Field `Inlet Branch Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        """
        vals = []
        inlet_branch_name = self.check_value(
            "Inlet Branch Name",
            inlet_branch_name)
        vals.append(inlet_branch_name)
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




class ConnectorList(DataObject):

    """ Corresponds to IDD object `ConnectorList`
        only two connectors allowed per loop
        if two entered, one must be Connector:Splitter and one must be Connector:Mixer
    """
    schema = {'min-fields': 0,
              'name': u'ConnectorList',
              'pyname': u'ConnectorList',
              'format': None,
              'fields': OrderedDict([(u'name',
                                      {'name': u'Name',
                                       'pyname': u'name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'connector 1 object type',
                                      {'name': u'Connector 1 Object Type',
                                       'pyname': u'connector_1_object_type',
                                       'required-field': True,
                                       'autosizable': False,
                                       'accepted-values': [u'Connector:Splitter',
                                                           u'Connector:Mixer'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'connector 1 name',
                                      {'name': u'Connector 1 Name',
                                       'pyname': u'connector_1_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'connector 2 object type',
                                      {'name': u'Connector 2 Object Type',
                                       'pyname': u'connector_2_object_type',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'Connector:Splitter',
                                                           u'Connector:Mixer'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'connector 2 name',
                                      {'name': u'Connector 2 Name',
                                       'pyname': u'connector_2_name',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'alpha'})]),
              'extensible-fields': OrderedDict(),
              'unique-object': False,
              'required-object': False,
              'group': u'Node'}

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
    def connector_1_object_type(self):
        """Get connector_1_object_type.

        Returns:
            str: the value of `connector_1_object_type` or None if not set

        """
        return self["Connector 1 Object Type"]

    @connector_1_object_type.setter
    def connector_1_object_type(self, value=None):
        """Corresponds to IDD field `Connector 1 Object Type`

        Args:
            value (str): value for IDD Field `Connector 1 Object Type`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Connector 1 Object Type"] = value

    @property
    def connector_1_name(self):
        """Get connector_1_name.

        Returns:
            str: the value of `connector_1_name` or None if not set

        """
        return self["Connector 1 Name"]

    @connector_1_name.setter
    def connector_1_name(self, value=None):
        """Corresponds to IDD field `Connector 1 Name`

        Args:
            value (str): value for IDD Field `Connector 1 Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Connector 1 Name"] = value

    @property
    def connector_2_object_type(self):
        """Get connector_2_object_type.

        Returns:
            str: the value of `connector_2_object_type` or None if not set

        """
        return self["Connector 2 Object Type"]

    @connector_2_object_type.setter
    def connector_2_object_type(self, value=None):
        """Corresponds to IDD field `Connector 2 Object Type`

        Args:
            value (str): value for IDD Field `Connector 2 Object Type`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Connector 2 Object Type"] = value

    @property
    def connector_2_name(self):
        """Get connector_2_name.

        Returns:
            str: the value of `connector_2_name` or None if not set

        """
        return self["Connector 2 Name"]

    @connector_2_name.setter
    def connector_2_name(self, value=None):
        """Corresponds to IDD field `Connector 2 Name`

        Args:
            value (str): value for IDD Field `Connector 2 Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Connector 2 Name"] = value




class NodeList(DataObject):

    """ Corresponds to IDD object `NodeList`
        This object is used in places where lists of nodes may be
        needed, e.g. ZoneHVAC:EquipmentConnections field Zone Air Inlet Node or NodeList Name
    """
    schema = {'min-fields': 2,
              'name': u'NodeList',
              'pyname': u'NodeList',
              'format': None,
              'fields': OrderedDict([(u'name',
                                      {'name': u'Name',
                                       'pyname': u'name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'node'})]),
              'extensible-fields': OrderedDict([(u'node name',
                                                 {'name': u'Node Name',
                                                  'pyname': u'node_name',
                                                  'required-field': False,
                                                  'autosizable': False,
                                                  'autocalculatable': False,
                                                  'type': u'node'})]),
              'unique-object': False,
              'required-object': False,
              'group': u'Node'}

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
                       node_name=None,
                       ):
        """Add values for extensible fields.

        Args:

            node_name (str): value for IDD Field `Node Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        """
        vals = []
        node_name = self.check_value("Node Name", node_name)
        vals.append(node_name)
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




class OutdoorAirNode(DataObject):

    """ Corresponds to IDD object `OutdoorAir:Node`
        This object sets the temperature and humidity conditions
        for an outdoor air node.  It allows the height above ground to be
        specified.  This object may be used more than once.
        The same node name may not appear in both an OutdoorAir:Node object and
        an OutdoorAir:NodeList object.
    """
    schema = {'min-fields': 0,
              'name': u'OutdoorAir:Node',
              'pyname': u'OutdoorAirNode',
              'format': None,
              'fields': OrderedDict([(u'name',
                                      {'name': u'Name',
                                       'pyname': u'name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'node'}),
                                     (u'height above ground',
                                      {'name': u'Height Above Ground',
                                       'pyname': u'height_above_ground',
                                       'default': -1.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'm'})]),
              'extensible-fields': OrderedDict(),
              'unique-object': False,
              'required-object': False,
              'group': u'Node'}

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
    def height_above_ground(self):
        """Get height_above_ground.

        Returns:
            float: the value of `height_above_ground` or None if not set

        """
        return self["Height Above Ground"]

    @height_above_ground.setter
    def height_above_ground(self, value=-1.0):
        """Corresponds to IDD field `Height Above Ground` A value less than
        zero indicates that the height will be ignored and the weather file
        conditions will be used.

        Args:
            value (float): value for IDD Field `Height Above Ground`
                Units: m
                Default value: -1.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Height Above Ground"] = value




class OutdoorAirNodeList(DataObject):

    """ Corresponds to IDD object `OutdoorAir:NodeList`
        This object sets the temperature and humidity conditions
        for an outdoor air node using the weather data values.
        to vary outdoor air node conditions with height above ground
        use OutdoorAir:Node instead of this object.
        This object may be used more than once.
        The same node name may not appear in both an OutdoorAir:Node object and
        an OutdoorAir:NodeList object.
    """
    schema = {'min-fields': 1,
              'name': u'OutdoorAir:NodeList',
              'pyname': u'OutdoorAirNodeList',
              'format': None,
              'fields': OrderedDict(),
              'extensible-fields': OrderedDict([(u'node or nodelist name 1',
                                                 {'name': u'Node or NodeList Name 1',
                                                  'pyname': u'node_or_nodelist_name_1',
                                                  'required-field': False,
                                                  'autosizable': False,
                                                  'autocalculatable': False,
                                                  'type': u'node'})]),
              'unique-object': False,
              'required-object': False,
              'group': u'Node'}

    def add_extensible(self,
                       node_or_nodelist_name_1=None,
                       ):
        """Add values for extensible fields.

        Args:

            node_or_nodelist_name_1 (str): value for IDD Field `Node or NodeList Name 1`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        """
        vals = []
        node_or_nodelist_name_1 = self.check_value(
            "Node or NodeList Name 1",
            node_or_nodelist_name_1)
        vals.append(node_or_nodelist_name_1)
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




class PipeAdiabatic(DataObject):

    """ Corresponds to IDD object `Pipe:Adiabatic`
        Passes Inlet Node state variables to Outlet Node state variables
    """
    schema = {'min-fields': 0,
              'name': u'Pipe:Adiabatic',
              'pyname': u'PipeAdiabatic',
              'format': None,
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
                                       'type': u'node'})]),
              'extensible-fields': OrderedDict(),
              'unique-object': False,
              'required-object': False,
              'group': u'Node'}

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




class PipeAdiabaticSteam(DataObject):

    """ Corresponds to IDD object `Pipe:Adiabatic:Steam`
        Passes Inlet Node state variables to Outlet Node state variables
    """
    schema = {'min-fields': 0,
              'name': u'Pipe:Adiabatic:Steam',
              'pyname': u'PipeAdiabaticSteam',
              'format': None,
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
                                       'type': u'node'})]),
              'extensible-fields': OrderedDict(),
              'unique-object': False,
              'required-object': False,
              'group': u'Node'}

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




class PipeIndoor(DataObject):

    """ Corresponds to IDD object `Pipe:Indoor`
        Pipe model with transport delay and heat transfer to the environment.
    """
    schema = {'min-fields': 0,
              'name': u'Pipe:Indoor',
              'pyname': u'PipeIndoor',
              'format': None,
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
                                     (u'environment type',
                                      {'name': u'Environment Type',
                                       'pyname': u'environment_type',
                                       'default': u'Zone',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'Zone',
                                                           u'Schedule'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'ambient temperature zone name',
                                      {'name': u'Ambient Temperature Zone Name',
                                       'pyname': u'ambient_temperature_zone_name',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'ambient temperature schedule name',
                                      {'name': u'Ambient Temperature Schedule Name',
                                       'pyname': u'ambient_temperature_schedule_name',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'ambient air velocity schedule name',
                                      {'name': u'Ambient Air Velocity Schedule Name',
                                       'pyname': u'ambient_air_velocity_schedule_name',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'pipe inside diameter',
                                      {'name': u'Pipe Inside Diameter',
                                       'pyname': u'pipe_inside_diameter',
                                       'minimum>': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'm'}),
                                     (u'pipe length',
                                      {'name': u'Pipe Length',
                                       'pyname': u'pipe_length',
                                       'minimum>': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'm'})]),
              'extensible-fields': OrderedDict(),
              'unique-object': False,
              'required-object': False,
              'group': u'Node'}

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
    def environment_type(self):
        """Get environment_type.

        Returns:
            str: the value of `environment_type` or None if not set

        """
        return self["Environment Type"]

    @environment_type.setter
    def environment_type(self, value="Zone"):
        """Corresponds to IDD field `Environment Type`

        Args:
            value (str): value for IDD Field `Environment Type`
                Default value: Zone
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Environment Type"] = value

    @property
    def ambient_temperature_zone_name(self):
        """Get ambient_temperature_zone_name.

        Returns:
            str: the value of `ambient_temperature_zone_name` or None if not set

        """
        return self["Ambient Temperature Zone Name"]

    @ambient_temperature_zone_name.setter
    def ambient_temperature_zone_name(self, value=None):
        """Corresponds to IDD field `Ambient Temperature Zone Name`

        Args:
            value (str): value for IDD Field `Ambient Temperature Zone Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Ambient Temperature Zone Name"] = value

    @property
    def ambient_temperature_schedule_name(self):
        """Get ambient_temperature_schedule_name.

        Returns:
            str: the value of `ambient_temperature_schedule_name` or None if not set

        """
        return self["Ambient Temperature Schedule Name"]

    @ambient_temperature_schedule_name.setter
    def ambient_temperature_schedule_name(self, value=None):
        """Corresponds to IDD field `Ambient Temperature Schedule Name`

        Args:
            value (str): value for IDD Field `Ambient Temperature Schedule Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Ambient Temperature Schedule Name"] = value

    @property
    def ambient_air_velocity_schedule_name(self):
        """Get ambient_air_velocity_schedule_name.

        Returns:
            str: the value of `ambient_air_velocity_schedule_name` or None if not set

        """
        return self["Ambient Air Velocity Schedule Name"]

    @ambient_air_velocity_schedule_name.setter
    def ambient_air_velocity_schedule_name(self, value=None):
        """Corresponds to IDD field `Ambient Air Velocity Schedule Name`

        Args:
            value (str): value for IDD Field `Ambient Air Velocity Schedule Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Ambient Air Velocity Schedule Name"] = value

    @property
    def pipe_inside_diameter(self):
        """Get pipe_inside_diameter.

        Returns:
            float: the value of `pipe_inside_diameter` or None if not set

        """
        return self["Pipe Inside Diameter"]

    @pipe_inside_diameter.setter
    def pipe_inside_diameter(self, value=None):
        """Corresponds to IDD field `Pipe Inside Diameter`

        Args:
            value (float): value for IDD Field `Pipe Inside Diameter`
                Units: m
                IP-Units: in
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Pipe Inside Diameter"] = value

    @property
    def pipe_length(self):
        """Get pipe_length.

        Returns:
            float: the value of `pipe_length` or None if not set

        """
        return self["Pipe Length"]

    @pipe_length.setter
    def pipe_length(self, value=None):
        """Corresponds to IDD field `Pipe Length`

        Args:
            value (float): value for IDD Field `Pipe Length`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Pipe Length"] = value




class PipeOutdoor(DataObject):

    """ Corresponds to IDD object `Pipe:Outdoor`
        Pipe model with transport delay and heat transfer to the environment.
    """
    schema = {'min-fields': 0,
              'name': u'Pipe:Outdoor',
              'pyname': u'PipeOutdoor',
              'format': None,
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
                                     (u'ambient temperature outdoor air node name',
                                      {'name': u'Ambient Temperature Outdoor Air Node Name',
                                       'pyname': u'ambient_temperature_outdoor_air_node_name',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'node'}),
                                     (u'pipe inside diameter',
                                      {'name': u'Pipe Inside Diameter',
                                       'pyname': u'pipe_inside_diameter',
                                       'minimum>': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'm'}),
                                     (u'pipe length',
                                      {'name': u'Pipe Length',
                                       'pyname': u'pipe_length',
                                       'minimum>': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'm'})]),
              'extensible-fields': OrderedDict(),
              'unique-object': False,
              'required-object': False,
              'group': u'Node'}

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
    def ambient_temperature_outdoor_air_node_name(self):
        """Get ambient_temperature_outdoor_air_node_name.

        Returns:
            str: the value of `ambient_temperature_outdoor_air_node_name` or None if not set

        """
        return self["Ambient Temperature Outdoor Air Node Name"]

    @ambient_temperature_outdoor_air_node_name.setter
    def ambient_temperature_outdoor_air_node_name(self, value=None):
        """Corresponds to IDD field `Ambient Temperature Outdoor Air Node Name`

        Args:
            value (str): value for IDD Field `Ambient Temperature Outdoor Air Node Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Ambient Temperature Outdoor Air Node Name"] = value

    @property
    def pipe_inside_diameter(self):
        """Get pipe_inside_diameter.

        Returns:
            float: the value of `pipe_inside_diameter` or None if not set

        """
        return self["Pipe Inside Diameter"]

    @pipe_inside_diameter.setter
    def pipe_inside_diameter(self, value=None):
        """Corresponds to IDD field `Pipe Inside Diameter`

        Args:
            value (float): value for IDD Field `Pipe Inside Diameter`
                Units: m
                IP-Units: in
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Pipe Inside Diameter"] = value

    @property
    def pipe_length(self):
        """Get pipe_length.

        Returns:
            float: the value of `pipe_length` or None if not set

        """
        return self["Pipe Length"]

    @pipe_length.setter
    def pipe_length(self, value=None):
        """Corresponds to IDD field `Pipe Length`

        Args:
            value (float): value for IDD Field `Pipe Length`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Pipe Length"] = value




class PipeUnderground(DataObject):

    """ Corresponds to IDD object `Pipe:Underground`
        Buried Pipe model: For pipes buried at a depth less
        than one meter, this is an alternative object to:
        HeatExchanger:Surface
    """
    schema = {'min-fields': 0,
              'name': u'Pipe:Underground',
              'pyname': u'PipeUnderground',
              'format': None,
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
                                     (u'sun exposure',
                                      {'name': u'Sun Exposure',
                                       'pyname': u'sun_exposure',
                                       'required-field': True,
                                       'autosizable': False,
                                       'accepted-values': [u'SunExposed',
                                                           u'NoSun'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'pipe inside diameter',
                                      {'name': u'Pipe Inside Diameter',
                                       'pyname': u'pipe_inside_diameter',
                                       'minimum>': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'm'}),
                                     (u'pipe length',
                                      {'name': u'Pipe Length',
                                       'pyname': u'pipe_length',
                                       'minimum>': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'm'}),
                                     (u'soil material name',
                                      {'name': u'Soil Material Name',
                                       'pyname': u'soil_material_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'alpha'}),
                                     (u'average soil surface temperature',
                                      {'name': u'Average Soil Surface Temperature',
                                       'pyname': u'average_soil_surface_temperature',
                                       'default': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'C'}),
                                     (u'amplitude of soil surface temperature',
                                      {'name': u'Amplitude of Soil Surface Temperature',
                                       'pyname': u'amplitude_of_soil_surface_temperature',
                                       'default': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'C'}),
                                     (u'phase constant of soil surface temperature',
                                      {'name': u'Phase Constant of Soil Surface Temperature',
                                       'pyname': u'phase_constant_of_soil_surface_temperature',
                                       'default': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'days'})]),
              'extensible-fields': OrderedDict(),
              'unique-object': False,
              'required-object': False,
              'group': u'Node'}

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
    def sun_exposure(self):
        """Get sun_exposure.

        Returns:
            str: the value of `sun_exposure` or None if not set

        """
        return self["Sun Exposure"]

    @sun_exposure.setter
    def sun_exposure(self, value=None):
        """Corresponds to IDD field `Sun Exposure`

        Args:
            value (str): value for IDD Field `Sun Exposure`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Sun Exposure"] = value

    @property
    def pipe_inside_diameter(self):
        """Get pipe_inside_diameter.

        Returns:
            float: the value of `pipe_inside_diameter` or None if not set

        """
        return self["Pipe Inside Diameter"]

    @pipe_inside_diameter.setter
    def pipe_inside_diameter(self, value=None):
        """Corresponds to IDD field `Pipe Inside Diameter` pipe thickness is
        defined in the Construction object.

        Args:
            value (float): value for IDD Field `Pipe Inside Diameter`
                Units: m
                IP-Units: in
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Pipe Inside Diameter"] = value

    @property
    def pipe_length(self):
        """Get pipe_length.

        Returns:
            float: the value of `pipe_length` or None if not set

        """
        return self["Pipe Length"]

    @pipe_length.setter
    def pipe_length(self, value=None):
        """Corresponds to IDD field `Pipe Length`

        Args:
            value (float): value for IDD Field `Pipe Length`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Pipe Length"] = value

    @property
    def soil_material_name(self):
        """Get soil_material_name.

        Returns:
            str: the value of `soil_material_name` or None if not set

        """
        return self["Soil Material Name"]

    @soil_material_name.setter
    def soil_material_name(self, value=None):
        """Corresponds to IDD field `Soil Material Name`

        Args:
            value (str): value for IDD Field `Soil Material Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Soil Material Name"] = value

    @property
    def average_soil_surface_temperature(self):
        """Get average_soil_surface_temperature.

        Returns:
            float: the value of `average_soil_surface_temperature` or None if not set

        """
        return self["Average Soil Surface Temperature"]

    @average_soil_surface_temperature.setter
    def average_soil_surface_temperature(self, value=None):
        """Corresponds to IDD field `Average Soil Surface Temperature`
        optional.

        Args:
            value (float): value for IDD Field `Average Soil Surface Temperature`
                Units: C
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Average Soil Surface Temperature"] = value

    @property
    def amplitude_of_soil_surface_temperature(self):
        """Get amplitude_of_soil_surface_temperature.

        Returns:
            float: the value of `amplitude_of_soil_surface_temperature` or None if not set

        """
        return self["Amplitude of Soil Surface Temperature"]

    @amplitude_of_soil_surface_temperature.setter
    def amplitude_of_soil_surface_temperature(self, value=None):
        """Corresponds to IDD field `Amplitude of Soil Surface Temperature`
        optional.

        Args:
            value (float): value for IDD Field `Amplitude of Soil Surface Temperature`
                Units: C
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Amplitude of Soil Surface Temperature"] = value

    @property
    def phase_constant_of_soil_surface_temperature(self):
        """Get phase_constant_of_soil_surface_temperature.

        Returns:
            float: the value of `phase_constant_of_soil_surface_temperature` or None if not set

        """
        return self["Phase Constant of Soil Surface Temperature"]

    @phase_constant_of_soil_surface_temperature.setter
    def phase_constant_of_soil_surface_temperature(self, value=None):
        """Corresponds to IDD field `Phase Constant of Soil Surface
        Temperature` optional.

        Args:
            value (float): value for IDD Field `Phase Constant of Soil Surface Temperature`
                Units: days
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Phase Constant of Soil Surface Temperature"] = value




class PipingSystemUndergroundDomain(DataObject):

    """ Corresponds to IDD object `PipingSystem:Underground:Domain`
        The ground domain object for underground piping system simulation.
    """
    schema = {'min-fields': 31,
              'name': u'PipingSystem:Underground:Domain',
              'pyname': u'PipingSystemUndergroundDomain',
              'format': None,
              'fields': OrderedDict([(u'name',
                                      {'name': u'Name',
                                       'pyname': u'name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'alpha'}),
                                     (u'xmax',
                                      {'name': u'Xmax',
                                       'pyname': u'xmax',
                                       'minimum>': 0.0,
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'm'}),
                                     (u'ymax',
                                      {'name': u'Ymax',
                                       'pyname': u'ymax',
                                       'minimum>': 0.0,
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'm'}),
                                     (u'zmax',
                                      {'name': u'Zmax',
                                       'pyname': u'zmax',
                                       'minimum>': 0.0,
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'm'}),
                                     (u'x-direction mesh density parameter',
                                      {'name': u'X-Direction Mesh Density Parameter',
                                       'pyname': u'xdirection_mesh_density_parameter',
                                       'default': 4,
                                       'minimum>': 0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'integer'}),
                                     (u'x-direction mesh type',
                                      {'name': u'X-Direction Mesh Type',
                                       'pyname': u'xdirection_mesh_type',
                                       'required-field': True,
                                       'autosizable': False,
                                       'accepted-values': [u'Uniform',
                                                           u'SymmetricGeometric'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'x-direction geometric coefficient',
                                      {'name': u'X-Direction Geometric Coefficient',
                                       'pyname': u'xdirection_geometric_coefficient',
                                       'default': 1.3,
                                       'maximum': 2.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 1.0,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'y-direction mesh density parameter',
                                      {'name': u'Y-Direction Mesh Density Parameter',
                                       'pyname': u'ydirection_mesh_density_parameter',
                                       'default': 4,
                                       'minimum>': 0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'integer'}),
                                     (u'y-direction mesh type',
                                      {'name': u'Y-Direction Mesh Type',
                                       'pyname': u'ydirection_mesh_type',
                                       'required-field': True,
                                       'autosizable': False,
                                       'accepted-values': [u'Uniform',
                                                           u'SymmetricGeometric'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'y-direction geometric coefficient',
                                      {'name': u'Y-Direction Geometric Coefficient',
                                       'pyname': u'ydirection_geometric_coefficient',
                                       'default': 1.3,
                                       'maximum': 2.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 1.0,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'z-direction mesh density parameter',
                                      {'name': u'Z-Direction Mesh Density Parameter',
                                       'pyname': u'zdirection_mesh_density_parameter',
                                       'default': 4,
                                       'minimum>': 0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'integer'}),
                                     (u'z-direction mesh type',
                                      {'name': u'Z-Direction Mesh Type',
                                       'pyname': u'zdirection_mesh_type',
                                       'required-field': True,
                                       'autosizable': False,
                                       'accepted-values': [u'Uniform',
                                                           u'SymmetricGeometric'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'z-direction geometric coefficient',
                                      {'name': u'Z-Direction Geometric Coefficient',
                                       'pyname': u'zdirection_geometric_coefficient',
                                       'default': 1.3,
                                       'maximum': 2.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 1.0,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'soil thermal conductivity',
                                      {'name': u'Soil Thermal Conductivity',
                                       'pyname': u'soil_thermal_conductivity',
                                       'minimum>': 0.0,
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'W/m-K'}),
                                     (u'soil density',
                                      {'name': u'Soil Density',
                                       'pyname': u'soil_density',
                                       'minimum>': 0.0,
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'kg/m3'}),
                                     (u'soil specific heat',
                                      {'name': u'Soil Specific Heat',
                                       'pyname': u'soil_specific_heat',
                                       'minimum>': 0.0,
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'J/kg-K'}),
                                     (u'soil moisture content volume fraction',
                                      {'name': u'Soil Moisture Content Volume Fraction',
                                       'pyname': u'soil_moisture_content_volume_fraction',
                                       'default': 30.0,
                                       'maximum': 100.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'percent'}),
                                     (u'soil moisture content volume fraction at saturation',
                                      {'name': u'Soil Moisture Content Volume Fraction at Saturation',
                                       'pyname': u'soil_moisture_content_volume_fraction_at_saturation',
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
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'C'}),
                                     (u'kusuda-achenbach average amplitude of surface temperature',
                                      {'name': u'Kusuda-Achenbach Average Amplitude of Surface Temperature',
                                       'pyname': u'kusudaachenbach_average_amplitude_of_surface_temperature',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'C'}),
                                     (u'kusuda-achenbach phase shift of minimum surface temperature',
                                      {'name': u'Kusuda-Achenbach Phase Shift of Minimum Surface Temperature',
                                       'pyname': u'kusudaachenbach_phase_shift_of_minimum_surface_temperature',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'days'}),
                                     (u'this domain includes basement surface interaction',
                                      {'name': u'This Domain Includes Basement Surface Interaction',
                                       'pyname': u'this_domain_includes_basement_surface_interaction',
                                       'default': u'No',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'Yes',
                                                           u'No'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'width of basement floor in ground domain',
                                      {'name': u'Width of Basement Floor in Ground Domain',
                                       'pyname': u'width_of_basement_floor_in_ground_domain',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'm'}),
                                     (u'depth of basement wall in ground domain',
                                      {'name': u'Depth of Basement Wall In Ground Domain',
                                       'pyname': u'depth_of_basement_wall_in_ground_domain',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'm'}),
                                     (u'shift pipe x coordinates by basement width',
                                      {'name': u'Shift Pipe X Coordinates By Basement Width',
                                       'pyname': u'shift_pipe_x_coordinates_by_basement_width',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'Yes',
                                                           u'No'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'name of basement wall boundary condition model',
                                      {'name': u'Name of Basement Wall Boundary Condition Model',
                                       'pyname': u'name_of_basement_wall_boundary_condition_model',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'name of basement floor boundary condition model',
                                      {'name': u'Name of Basement Floor Boundary Condition Model',
                                       'pyname': u'name_of_basement_floor_boundary_condition_model',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'convergence criterion for the outer cartesian domain iteration loop',
                                      {'name': u'Convergence Criterion for the Outer Cartesian Domain Iteration Loop',
                                       'pyname': u'convergence_criterion_for_the_outer_cartesian_domain_iteration_loop',
                                       'default': 0.001,
                                       'maximum': 0.5,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 1e-06,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'deltaC'}),
                                     (u'maximum iterations in the outer cartesian domain iteration loop',
                                      {'name': u'Maximum Iterations in the Outer Cartesian Domain Iteration Loop',
                                       'pyname': u'maximum_iterations_in_the_outer_cartesian_domain_iteration_loop',
                                       'default': 500,
                                       'maximum': 10000,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 3,
                                       'autocalculatable': False,
                                       'type': u'integer'}),
                                     (u'evapotranspiration ground cover parameter',
                                      {'name': u'Evapotranspiration Ground Cover Parameter',
                                       'pyname': u'evapotranspiration_ground_cover_parameter',
                                       'default': 0.4,
                                       'maximum': 1.5,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'number of pipe circuits entered for this domain',
                                      {'name': u'Number of Pipe Circuits Entered for this Domain',
                                       'pyname': u'number_of_pipe_circuits_entered_for_this_domain',
                                       'required-field': True,
                                       'autosizable': False,
                                       'minimum': 1,
                                       'autocalculatable': False,
                                       'type': u'integer'})]),
              'extensible-fields': OrderedDict([(u'pipe circuit 1',
                                                 {'name': u'Pipe Circuit 1',
                                                  'pyname': u'pipe_circuit_1',
                                                  'required-field': True,
                                                  'autosizable': False,
                                                  'autocalculatable': False,
                                                  'type': u'object-list'})]),
              'unique-object': False,
              'required-object': False,
              'group': u'Node'}

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
    def xmax(self):
        """Get xmax.

        Returns:
            float: the value of `xmax` or None if not set

        """
        return self["Xmax"]

    @xmax.setter
    def xmax(self, value=None):
        """Corresponds to IDD field `Xmax` Domain extent in the local 'X'
        direction.

        Args:
            value (float): value for IDD Field `Xmax`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Xmax"] = value

    @property
    def ymax(self):
        """Get ymax.

        Returns:
            float: the value of `ymax` or None if not set

        """
        return self["Ymax"]

    @ymax.setter
    def ymax(self, value=None):
        """Corresponds to IDD field `Ymax` Domain extent in the local 'Y'
        direction.

        Args:
            value (float): value for IDD Field `Ymax`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Ymax"] = value

    @property
    def zmax(self):
        """Get zmax.

        Returns:
            float: the value of `zmax` or None if not set

        """
        return self["Zmax"]

    @zmax.setter
    def zmax(self, value=None):
        """Corresponds to IDD field `Zmax` Domain extent in the local 'Y'
        direction.

        Args:
            value (float): value for IDD Field `Zmax`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Zmax"] = value

    @property
    def xdirection_mesh_density_parameter(self):
        """Get xdirection_mesh_density_parameter.

        Returns:
            int: the value of `xdirection_mesh_density_parameter` or None if not set

        """
        return self["X-Direction Mesh Density Parameter"]

    @xdirection_mesh_density_parameter.setter
    def xdirection_mesh_density_parameter(self, value=4):
        """  Corresponds to IDD field `X-Direction Mesh Density Parameter`
        If mesh type is symmetric geometric, this should be an even number.

        Args:
            value (int): value for IDD Field `X-Direction Mesh Density Parameter`
                Default value: 4
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["X-Direction Mesh Density Parameter"] = value

    @property
    def xdirection_mesh_type(self):
        """Get xdirection_mesh_type.

        Returns:
            str: the value of `xdirection_mesh_type` or None if not set

        """
        return self["X-Direction Mesh Type"]

    @xdirection_mesh_type.setter
    def xdirection_mesh_type(self, value=None):
        """  Corresponds to IDD field `X-Direction Mesh Type`

        Args:
            value (str): value for IDD Field `X-Direction Mesh Type`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["X-Direction Mesh Type"] = value

    @property
    def xdirection_geometric_coefficient(self):
        """Get xdirection_geometric_coefficient.

        Returns:
            float: the value of `xdirection_geometric_coefficient` or None if not set

        """
        return self["X-Direction Geometric Coefficient"]

    @xdirection_geometric_coefficient.setter
    def xdirection_geometric_coefficient(self, value=1.3):
        """  Corresponds to IDD field `X-Direction Geometric Coefficient`
        optional
        Only used if mesh type is symmetric geometric

        Args:
            value (float): value for IDD Field `X-Direction Geometric Coefficient`
                Default value: 1.3
                value >= 1.0
                value <= 2.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["X-Direction Geometric Coefficient"] = value

    @property
    def ydirection_mesh_density_parameter(self):
        """Get ydirection_mesh_density_parameter.

        Returns:
            int: the value of `ydirection_mesh_density_parameter` or None if not set

        """
        return self["Y-Direction Mesh Density Parameter"]

    @ydirection_mesh_density_parameter.setter
    def ydirection_mesh_density_parameter(self, value=4):
        """  Corresponds to IDD field `Y-Direction Mesh Density Parameter`
        If mesh type is symmetric geometric, this should be an even number.

        Args:
            value (int): value for IDD Field `Y-Direction Mesh Density Parameter`
                Default value: 4
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Y-Direction Mesh Density Parameter"] = value

    @property
    def ydirection_mesh_type(self):
        """Get ydirection_mesh_type.

        Returns:
            str: the value of `ydirection_mesh_type` or None if not set

        """
        return self["Y-Direction Mesh Type"]

    @ydirection_mesh_type.setter
    def ydirection_mesh_type(self, value=None):
        """  Corresponds to IDD field `Y-Direction Mesh Type`

        Args:
            value (str): value for IDD Field `Y-Direction Mesh Type`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Y-Direction Mesh Type"] = value

    @property
    def ydirection_geometric_coefficient(self):
        """Get ydirection_geometric_coefficient.

        Returns:
            float: the value of `ydirection_geometric_coefficient` or None if not set

        """
        return self["Y-Direction Geometric Coefficient"]

    @ydirection_geometric_coefficient.setter
    def ydirection_geometric_coefficient(self, value=1.3):
        """  Corresponds to IDD field `Y-Direction Geometric Coefficient`
        optional
        Only used if mesh type is symmetric geometric

        Args:
            value (float): value for IDD Field `Y-Direction Geometric Coefficient`
                Default value: 1.3
                value >= 1.0
                value <= 2.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Y-Direction Geometric Coefficient"] = value

    @property
    def zdirection_mesh_density_parameter(self):
        """Get zdirection_mesh_density_parameter.

        Returns:
            int: the value of `zdirection_mesh_density_parameter` or None if not set

        """
        return self["Z-Direction Mesh Density Parameter"]

    @zdirection_mesh_density_parameter.setter
    def zdirection_mesh_density_parameter(self, value=4):
        """  Corresponds to IDD field `Z-Direction Mesh Density Parameter`
        If mesh type is symmetric geometric, this should be an even number.

        Args:
            value (int): value for IDD Field `Z-Direction Mesh Density Parameter`
                Default value: 4
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Z-Direction Mesh Density Parameter"] = value

    @property
    def zdirection_mesh_type(self):
        """Get zdirection_mesh_type.

        Returns:
            str: the value of `zdirection_mesh_type` or None if not set

        """
        return self["Z-Direction Mesh Type"]

    @zdirection_mesh_type.setter
    def zdirection_mesh_type(self, value=None):
        """  Corresponds to IDD field `Z-Direction Mesh Type`

        Args:
            value (str): value for IDD Field `Z-Direction Mesh Type`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Z-Direction Mesh Type"] = value

    @property
    def zdirection_geometric_coefficient(self):
        """Get zdirection_geometric_coefficient.

        Returns:
            float: the value of `zdirection_geometric_coefficient` or None if not set

        """
        return self["Z-Direction Geometric Coefficient"]

    @zdirection_geometric_coefficient.setter
    def zdirection_geometric_coefficient(self, value=1.3):
        """  Corresponds to IDD field `Z-Direction Geometric Coefficient`
        optional
        Only used if mesh type is symmetric geometric

        Args:
            value (float): value for IDD Field `Z-Direction Geometric Coefficient`
                Default value: 1.3
                value >= 1.0
                value <= 2.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Z-Direction Geometric Coefficient"] = value

    @property
    def soil_thermal_conductivity(self):
        """Get soil_thermal_conductivity.

        Returns:
            float: the value of `soil_thermal_conductivity` or None if not set

        """
        return self["Soil Thermal Conductivity"]

    @soil_thermal_conductivity.setter
    def soil_thermal_conductivity(self, value=None):
        """Corresponds to IDD field `Soil Thermal Conductivity`

        Args:
            value (float): value for IDD Field `Soil Thermal Conductivity`
                Units: W/m-K
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
    def soil_density(self, value=None):
        """Corresponds to IDD field `Soil Density`

        Args:
            value (float): value for IDD Field `Soil Density`
                Units: kg/m3
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
    def soil_specific_heat(self, value=None):
        """Corresponds to IDD field `Soil Specific Heat` This is a dry soil
        property, which is adjusted for freezing effects by the simulation
        algorithm.

        Args:
            value (float): value for IDD Field `Soil Specific Heat`
                Units: J/kg-K
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Soil Specific Heat"] = value

    @property
    def soil_moisture_content_volume_fraction(self):
        """Get soil_moisture_content_volume_fraction.

        Returns:
            float: the value of `soil_moisture_content_volume_fraction` or None if not set

        """
        return self["Soil Moisture Content Volume Fraction"]

    @soil_moisture_content_volume_fraction.setter
    def soil_moisture_content_volume_fraction(self, value=30.0):
        """Corresponds to IDD field `Soil Moisture Content Volume Fraction`

        Args:
            value (float): value for IDD Field `Soil Moisture Content Volume Fraction`
                Units: percent
                Default value: 30.0
                value <= 100.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Soil Moisture Content Volume Fraction"] = value

    @property
    def soil_moisture_content_volume_fraction_at_saturation(self):
        """Get soil_moisture_content_volume_fraction_at_saturation.

        Returns:
            float: the value of `soil_moisture_content_volume_fraction_at_saturation` or None if not set

        """
        return self["Soil Moisture Content Volume Fraction at Saturation"]

    @soil_moisture_content_volume_fraction_at_saturation.setter
    def soil_moisture_content_volume_fraction_at_saturation(self, value=50.0):
        """Corresponds to IDD field `Soil Moisture Content Volume Fraction at
        Saturation`

        Args:
            value (float): value for IDD Field `Soil Moisture Content Volume Fraction at Saturation`
                Units: percent
                Default value: 50.0
                value <= 100.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Soil Moisture Content Volume Fraction at Saturation"] = value

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
    def this_domain_includes_basement_surface_interaction(self):
        """Get this_domain_includes_basement_surface_interaction.

        Returns:
            str: the value of `this_domain_includes_basement_surface_interaction` or None if not set

        """
        return self["This Domain Includes Basement Surface Interaction"]

    @this_domain_includes_basement_surface_interaction.setter
    def this_domain_includes_basement_surface_interaction(self, value="No"):
        """  Corresponds to IDD field `This Domain Includes Basement Surface Interaction`
        if Yes, then the following basement inputs are used
        if No, then the following basement inputs are *ignored*

        Args:
            value (str): value for IDD Field `This Domain Includes Basement Surface Interaction`
                Default value: No
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["This Domain Includes Basement Surface Interaction"] = value

    @property
    def width_of_basement_floor_in_ground_domain(self):
        """Get width_of_basement_floor_in_ground_domain.

        Returns:
            float: the value of `width_of_basement_floor_in_ground_domain` or None if not set

        """
        return self["Width of Basement Floor in Ground Domain"]

    @width_of_basement_floor_in_ground_domain.setter
    def width_of_basement_floor_in_ground_domain(self, value=None):
        """Corresponds to IDD field `Width of Basement Floor in Ground Domain`
        Required only if Domain Has Basement Interaction.

        Args:
            value (float): value for IDD Field `Width of Basement Floor in Ground Domain`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Width of Basement Floor in Ground Domain"] = value

    @property
    def depth_of_basement_wall_in_ground_domain(self):
        """Get depth_of_basement_wall_in_ground_domain.

        Returns:
            float: the value of `depth_of_basement_wall_in_ground_domain` or None if not set

        """
        return self["Depth of Basement Wall In Ground Domain"]

    @depth_of_basement_wall_in_ground_domain.setter
    def depth_of_basement_wall_in_ground_domain(self, value=None):
        """Corresponds to IDD field `Depth of Basement Wall In Ground Domain`
        Required only if Domain Has Basement Interaction.

        Args:
            value (float): value for IDD Field `Depth of Basement Wall In Ground Domain`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Depth of Basement Wall In Ground Domain"] = value

    @property
    def shift_pipe_x_coordinates_by_basement_width(self):
        """Get shift_pipe_x_coordinates_by_basement_width.

        Returns:
            str: the value of `shift_pipe_x_coordinates_by_basement_width` or None if not set

        """
        return self["Shift Pipe X Coordinates By Basement Width"]

    @shift_pipe_x_coordinates_by_basement_width.setter
    def shift_pipe_x_coordinates_by_basement_width(self, value=None):
        """Corresponds to IDD field `Shift Pipe X Coordinates By Basement
        Width` Required only if Domain Has Basement Interaction.

        Args:
            value (str): value for IDD Field `Shift Pipe X Coordinates By Basement Width`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Shift Pipe X Coordinates By Basement Width"] = value

    @property
    def name_of_basement_wall_boundary_condition_model(self):
        """Get name_of_basement_wall_boundary_condition_model.

        Returns:
            str: the value of `name_of_basement_wall_boundary_condition_model` or None if not set

        """
        return self["Name of Basement Wall Boundary Condition Model"]

    @name_of_basement_wall_boundary_condition_model.setter
    def name_of_basement_wall_boundary_condition_model(self, value=None):
        """Corresponds to IDD field `Name of Basement Wall Boundary Condition
        Model` Required only if Domain Has Basement Interaction.

        Args:
            value (str): value for IDD Field `Name of Basement Wall Boundary Condition Model`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Name of Basement Wall Boundary Condition Model"] = value

    @property
    def name_of_basement_floor_boundary_condition_model(self):
        """Get name_of_basement_floor_boundary_condition_model.

        Returns:
            str: the value of `name_of_basement_floor_boundary_condition_model` or None if not set

        """
        return self["Name of Basement Floor Boundary Condition Model"]

    @name_of_basement_floor_boundary_condition_model.setter
    def name_of_basement_floor_boundary_condition_model(self, value=None):
        """Corresponds to IDD field `Name of Basement Floor Boundary Condition
        Model` Required only if Domain Has Basement Interaction.

        Args:
            value (str): value for IDD Field `Name of Basement Floor Boundary Condition Model`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Name of Basement Floor Boundary Condition Model"] = value

    @property
    def convergence_criterion_for_the_outer_cartesian_domain_iteration_loop(
            self):
        """Get
        convergence_criterion_for_the_outer_cartesian_domain_iteration_loop.

        Returns:
            float: the value of `convergence_criterion_for_the_outer_cartesian_domain_iteration_loop` or None if not set

        """
        return self[
            "Convergence Criterion for the Outer Cartesian Domain Iteration Loop"]

    @convergence_criterion_for_the_outer_cartesian_domain_iteration_loop.setter
    def convergence_criterion_for_the_outer_cartesian_domain_iteration_loop(
            self,
            value=0.001):
        """Corresponds to IDD field `Convergence Criterion for the Outer
        Cartesian Domain Iteration Loop`

        Args:
            value (float): value for IDD Field `Convergence Criterion for the Outer Cartesian Domain Iteration Loop`
                Units: deltaC
                Default value: 0.001
                value >= 1e-06
                value <= 0.5
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self[
            "Convergence Criterion for the Outer Cartesian Domain Iteration Loop"] = value

    @property
    def maximum_iterations_in_the_outer_cartesian_domain_iteration_loop(self):
        """Get maximum_iterations_in_the_outer_cartesian_domain_iteration_loop.

        Returns:
            int: the value of `maximum_iterations_in_the_outer_cartesian_domain_iteration_loop` or None if not set

        """
        return self[
            "Maximum Iterations in the Outer Cartesian Domain Iteration Loop"]

    @maximum_iterations_in_the_outer_cartesian_domain_iteration_loop.setter
    def maximum_iterations_in_the_outer_cartesian_domain_iteration_loop(
            self,
            value=500):
        """Corresponds to IDD field `Maximum Iterations in the Outer Cartesian
        Domain Iteration Loop`

        Args:
            value (int): value for IDD Field `Maximum Iterations in the Outer Cartesian Domain Iteration Loop`
                Default value: 500
                value >= 3
                value <= 10000
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self[
            "Maximum Iterations in the Outer Cartesian Domain Iteration Loop"] = value

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

    @property
    def number_of_pipe_circuits_entered_for_this_domain(self):
        """Get number_of_pipe_circuits_entered_for_this_domain.

        Returns:
            int: the value of `number_of_pipe_circuits_entered_for_this_domain` or None if not set

        """
        return self["Number of Pipe Circuits Entered for this Domain"]

    @number_of_pipe_circuits_entered_for_this_domain.setter
    def number_of_pipe_circuits_entered_for_this_domain(self, value=None):
        """Corresponds to IDD field `Number of Pipe Circuits Entered for this
        Domain`

        Args:
            value (int): value for IDD Field `Number of Pipe Circuits Entered for this Domain`
                value >= 1
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Number of Pipe Circuits Entered for this Domain"] = value

    def add_extensible(self,
                       pipe_circuit_1=None,
                       ):
        """Add values for extensible fields.

        Args:

            pipe_circuit_1 (str): value for IDD Field `Pipe Circuit 1`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        """
        vals = []
        pipe_circuit_1 = self.check_value("Pipe Circuit 1", pipe_circuit_1)
        vals.append(pipe_circuit_1)
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




class PipingSystemUndergroundPipeCircuit(DataObject):

    """ Corresponds to IDD object `PipingSystem:Underground:PipeCircuit`
        The pipe circuit object in an underground piping system.
        This object is simulated within an underground piping domain object
        and connected on a branch on a plant loop.
    """
    schema = {'min-fields': 15,
              'name': u'PipingSystem:Underground:PipeCircuit',
              'pyname': u'PipingSystemUndergroundPipeCircuit',
              'format': None,
              'fields': OrderedDict([(u'name',
                                      {'name': u'Name',
                                       'pyname': u'name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'alpha'}),
                                     (u'pipe thermal conductivity',
                                      {'name': u'Pipe Thermal Conductivity',
                                       'pyname': u'pipe_thermal_conductivity',
                                       'minimum>': 0.0,
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'W/m-K'}),
                                     (u'pipe density',
                                      {'name': u'Pipe Density',
                                       'pyname': u'pipe_density',
                                       'minimum>': 0.0,
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'kg/m3'}),
                                     (u'pipe specific heat',
                                      {'name': u'Pipe Specific Heat',
                                       'pyname': u'pipe_specific_heat',
                                       'minimum>': 0.0,
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'J/kg-K'}),
                                     (u'pipe inner diameter',
                                      {'name': u'Pipe Inner Diameter',
                                       'pyname': u'pipe_inner_diameter',
                                       'minimum>': 0.0,
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'm'}),
                                     (u'pipe outer diameter',
                                      {'name': u'Pipe Outer Diameter',
                                       'pyname': u'pipe_outer_diameter',
                                       'minimum>': 0.0,
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'm'}),
                                     (u'design flow rate',
                                      {'name': u'Design Flow Rate',
                                       'pyname': u'design_flow_rate',
                                       'minimum>': 0.0,
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'm3/s'}),
                                     (u'circuit inlet node',
                                      {'name': u'Circuit Inlet Node',
                                       'pyname': u'circuit_inlet_node',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'node'}),
                                     (u'circuit outlet node',
                                      {'name': u'Circuit Outlet Node',
                                       'pyname': u'circuit_outlet_node',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'node'}),
                                     (u'convergence criterion for the inner radial iteration loop',
                                      {'name': u'Convergence Criterion for the Inner Radial Iteration Loop',
                                       'pyname': u'convergence_criterion_for_the_inner_radial_iteration_loop',
                                       'default': 0.001,
                                       'maximum': 0.5,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 1e-06,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'deltaC'}),
                                     (u'maximum iterations in the inner radial iteration loop',
                                      {'name': u'Maximum Iterations in the Inner Radial Iteration Loop',
                                       'pyname': u'maximum_iterations_in_the_inner_radial_iteration_loop',
                                       'default': 500,
                                       'maximum': 10000,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 3,
                                       'autocalculatable': False,
                                       'type': u'integer'}),
                                     (u'number of soil nodes in the inner radial near pipe mesh region',
                                      {'name': u'Number of Soil Nodes in the Inner Radial Near Pipe Mesh Region',
                                       'pyname': u'number_of_soil_nodes_in_the_inner_radial_near_pipe_mesh_region',
                                       'default': 3,
                                       'maximum': 15,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 1,
                                       'autocalculatable': False,
                                       'type': u'integer'}),
                                     (u'radial thickness of inner radial near pipe mesh region',
                                      {'name': u'Radial Thickness of Inner Radial Near Pipe Mesh Region',
                                       'pyname': u'radial_thickness_of_inner_radial_near_pipe_mesh_region',
                                       'minimum>': 0.0,
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'number of pipe segments entered for this pipe circuit',
                                      {'name': u'Number of Pipe Segments Entered for this Pipe Circuit',
                                       'pyname': u'number_of_pipe_segments_entered_for_this_pipe_circuit',
                                       'required-field': True,
                                       'autosizable': False,
                                       'minimum': 1,
                                       'autocalculatable': False,
                                       'type': u'integer'})]),
              'extensible-fields': OrderedDict([(u'pipe segment 1',
                                                 {'name': u'Pipe Segment 1',
                                                  'pyname': u'pipe_segment_1',
                                                  'required-field': True,
                                                  'autosizable': False,
                                                  'autocalculatable': False,
                                                  'type': u'object-list'})]),
              'unique-object': False,
              'required-object': False,
              'group': u'Node'}

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
    def pipe_density(self):
        """Get pipe_density.

        Returns:
            float: the value of `pipe_density` or None if not set

        """
        return self["Pipe Density"]

    @pipe_density.setter
    def pipe_density(self, value=None):
        """Corresponds to IDD field `Pipe Density`

        Args:
            value (float): value for IDD Field `Pipe Density`
                Units: kg/m3
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
    def pipe_specific_heat(self, value=None):
        """Corresponds to IDD field `Pipe Specific Heat`

        Args:
            value (float): value for IDD Field `Pipe Specific Heat`
                Units: J/kg-K
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Pipe Specific Heat"] = value

    @property
    def pipe_inner_diameter(self):
        """Get pipe_inner_diameter.

        Returns:
            float: the value of `pipe_inner_diameter` or None if not set

        """
        return self["Pipe Inner Diameter"]

    @pipe_inner_diameter.setter
    def pipe_inner_diameter(self, value=None):
        """Corresponds to IDD field `Pipe Inner Diameter`

        Args:
            value (float): value for IDD Field `Pipe Inner Diameter`
                Units: m
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
    def pipe_outer_diameter(self, value=None):
        """Corresponds to IDD field `Pipe Outer Diameter`

        Args:
            value (float): value for IDD Field `Pipe Outer Diameter`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Pipe Outer Diameter"] = value

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
    def circuit_inlet_node(self):
        """Get circuit_inlet_node.

        Returns:
            str: the value of `circuit_inlet_node` or None if not set

        """
        return self["Circuit Inlet Node"]

    @circuit_inlet_node.setter
    def circuit_inlet_node(self, value=None):
        """Corresponds to IDD field `Circuit Inlet Node`

        Args:
            value (str): value for IDD Field `Circuit Inlet Node`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Circuit Inlet Node"] = value

    @property
    def circuit_outlet_node(self):
        """Get circuit_outlet_node.

        Returns:
            str: the value of `circuit_outlet_node` or None if not set

        """
        return self["Circuit Outlet Node"]

    @circuit_outlet_node.setter
    def circuit_outlet_node(self, value=None):
        """Corresponds to IDD field `Circuit Outlet Node`

        Args:
            value (str): value for IDD Field `Circuit Outlet Node`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Circuit Outlet Node"] = value

    @property
    def convergence_criterion_for_the_inner_radial_iteration_loop(self):
        """Get convergence_criterion_for_the_inner_radial_iteration_loop.

        Returns:
            float: the value of `convergence_criterion_for_the_inner_radial_iteration_loop` or None if not set

        """
        return self[
            "Convergence Criterion for the Inner Radial Iteration Loop"]

    @convergence_criterion_for_the_inner_radial_iteration_loop.setter
    def convergence_criterion_for_the_inner_radial_iteration_loop(
            self,
            value=0.001):
        """Corresponds to IDD field `Convergence Criterion for the Inner Radial
        Iteration Loop`

        Args:
            value (float): value for IDD Field `Convergence Criterion for the Inner Radial Iteration Loop`
                Units: deltaC
                Default value: 0.001
                value >= 1e-06
                value <= 0.5
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self[
            "Convergence Criterion for the Inner Radial Iteration Loop"] = value

    @property
    def maximum_iterations_in_the_inner_radial_iteration_loop(self):
        """Get maximum_iterations_in_the_inner_radial_iteration_loop.

        Returns:
            int: the value of `maximum_iterations_in_the_inner_radial_iteration_loop` or None if not set

        """
        return self["Maximum Iterations in the Inner Radial Iteration Loop"]

    @maximum_iterations_in_the_inner_radial_iteration_loop.setter
    def maximum_iterations_in_the_inner_radial_iteration_loop(self, value=500):
        """Corresponds to IDD field `Maximum Iterations in the Inner Radial
        Iteration Loop`

        Args:
            value (int): value for IDD Field `Maximum Iterations in the Inner Radial Iteration Loop`
                Default value: 500
                value >= 3
                value <= 10000
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Maximum Iterations in the Inner Radial Iteration Loop"] = value

    @property
    def number_of_soil_nodes_in_the_inner_radial_near_pipe_mesh_region(self):
        """Get number_of_soil_nodes_in_the_inner_radial_near_pipe_mesh_region.

        Returns:
            int: the value of `number_of_soil_nodes_in_the_inner_radial_near_pipe_mesh_region` or None if not set

        """
        return self[
            "Number of Soil Nodes in the Inner Radial Near Pipe Mesh Region"]

    @number_of_soil_nodes_in_the_inner_radial_near_pipe_mesh_region.setter
    def number_of_soil_nodes_in_the_inner_radial_near_pipe_mesh_region(
            self,
            value=3):
        """Corresponds to IDD field `Number of Soil Nodes in the Inner Radial
        Near Pipe Mesh Region`

        Args:
            value (int): value for IDD Field `Number of Soil Nodes in the Inner Radial Near Pipe Mesh Region`
                Default value: 3
                value >= 1
                value <= 15
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self[
            "Number of Soil Nodes in the Inner Radial Near Pipe Mesh Region"] = value

    @property
    def radial_thickness_of_inner_radial_near_pipe_mesh_region(self):
        """Get radial_thickness_of_inner_radial_near_pipe_mesh_region.

        Returns:
            float: the value of `radial_thickness_of_inner_radial_near_pipe_mesh_region` or None if not set

        """
        return self["Radial Thickness of Inner Radial Near Pipe Mesh Region"]

    @radial_thickness_of_inner_radial_near_pipe_mesh_region.setter
    def radial_thickness_of_inner_radial_near_pipe_mesh_region(
            self,
            value=None):
        """Corresponds to IDD field `Radial Thickness of Inner Radial Near Pipe
        Mesh Region` Required because it must be selected by user instead of
        being inferred from circuit/domain object inputs.

        Args:
            value (float): value for IDD Field `Radial Thickness of Inner Radial Near Pipe Mesh Region`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Radial Thickness of Inner Radial Near Pipe Mesh Region"] = value

    @property
    def number_of_pipe_segments_entered_for_this_pipe_circuit(self):
        """Get number_of_pipe_segments_entered_for_this_pipe_circuit.

        Returns:
            int: the value of `number_of_pipe_segments_entered_for_this_pipe_circuit` or None if not set

        """
        return self["Number of Pipe Segments Entered for this Pipe Circuit"]

    @number_of_pipe_segments_entered_for_this_pipe_circuit.setter
    def number_of_pipe_segments_entered_for_this_pipe_circuit(
            self,
            value=None):
        """Corresponds to IDD field `Number of Pipe Segments Entered for this
        Pipe Circuit`

        Args:
            value (int): value for IDD Field `Number of Pipe Segments Entered for this Pipe Circuit`
                value >= 1
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Number of Pipe Segments Entered for this Pipe Circuit"] = value

    def add_extensible(self,
                       pipe_segment_1=None,
                       ):
        """Add values for extensible fields.

        Args:

            pipe_segment_1 (str): value for IDD Field `Pipe Segment 1`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        """
        vals = []
        pipe_segment_1 = self.check_value("Pipe Segment 1", pipe_segment_1)
        vals.append(pipe_segment_1)
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




class PipingSystemUndergroundPipeSegment(DataObject):

    """ Corresponds to IDD object `PipingSystem:Underground:PipeSegment`
        The pipe segment to be used in an underground piping system
        This object represents a single pipe leg positioned axially
        in the local z-direction, at a given x, y location in the domain
    """
    schema = {'min-fields': 4,
              'name': u'PipingSystem:Underground:PipeSegment',
              'pyname': u'PipingSystemUndergroundPipeSegment',
              'format': None,
              'fields': OrderedDict([(u'name',
                                      {'name': u'Name',
                                       'pyname': u'name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'alpha'}),
                                     (u'x position',
                                      {'name': u'X Position',
                                       'pyname': u'x_position',
                                       'minimum>': 0.0,
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'm'}),
                                     (u'y position',
                                      {'name': u'Y Position',
                                       'pyname': u'y_position',
                                       'minimum>': 0.0,
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'm'}),
                                     (u'flow direction',
                                      {'name': u'Flow Direction',
                                       'pyname': u'flow_direction',
                                       'required-field': True,
                                       'autosizable': False,
                                       'accepted-values': [u'IncreasingZ',
                                                           u'DecreasingZ'],
                                       'autocalculatable': False,
                                       'type': 'alpha'})]),
              'extensible-fields': OrderedDict(),
              'unique-object': False,
              'required-object': False,
              'group': u'Node'}

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
    def x_position(self):
        """Get x_position.

        Returns:
            float: the value of `x_position` or None if not set

        """
        return self["X Position"]

    @x_position.setter
    def x_position(self, value=None):
        """  Corresponds to IDD field `X Position`
        This segment will be centered at this distance from the x=0
        domain surface or the basement wall surface, based on whether
        a basement exists in this domain and the selection of the
        shift input field found in the domain object.

        Args:
            value (float): value for IDD Field `X Position`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["X Position"] = value

    @property
    def y_position(self):
        """Get y_position.

        Returns:
            float: the value of `y_position` or None if not set

        """
        return self["Y Position"]

    @y_position.setter
    def y_position(self, value=None):
        """Corresponds to IDD field `Y Position` This segment will be centered
        at this distance away from the ground surface; thus this value
        represents the burial depth of this pipe segment.

        Args:
            value (float): value for IDD Field `Y Position`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Y Position"] = value

    @property
    def flow_direction(self):
        """Get flow_direction.

        Returns:
            str: the value of `flow_direction` or None if not set

        """
        return self["Flow Direction"]

    @flow_direction.setter
    def flow_direction(self, value=None):
        """Corresponds to IDD field `Flow Direction` This segment will be
        simulated such that the flow is in the selected direction.  This can
        allow for detailed analysis of circuiting effects in a single domain.

        Args:
            value (str): value for IDD Field `Flow Direction`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Flow Direction"] = value




class Duct(DataObject):

    """Corresponds to IDD object `Duct` Passes inlet node state variables to
    outlet node state variables."""
    schema = {'min-fields': 0,
              'name': u'Duct',
              'pyname': u'Duct',
              'format': None,
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
                                       'type': u'node'})]),
              'extensible-fields': OrderedDict(),
              'unique-object': False,
              'required-object': False,
              'group': u'Node'}

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


