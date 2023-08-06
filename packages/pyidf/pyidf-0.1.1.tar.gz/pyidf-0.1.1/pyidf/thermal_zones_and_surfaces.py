""" Data objects in group "Thermal Zones and Surfaces"
"""

from collections import OrderedDict
import logging
from pyidf.helper import DataObject

logger = logging.getLogger("pyidf")
logger.addHandler(logging.NullHandler())



class GlobalGeometryRules(DataObject):

    """Corresponds to IDD object `GlobalGeometryRules` Specifes the geometric
    rules used to describe the input of surface vertices and daylighting
    reference points."""
    schema = {'extensible-fields': OrderedDict(),
              'fields': OrderedDict([(u'starting vertex position',
                                      {'name': u'Starting Vertex Position',
                                       'pyname': u'starting_vertex_position',
                                       'required-field': True,
                                       'autosizable': False,
                                       'accepted-values': [u'UpperLeftCorner',
                                                           u'LowerLeftCorner',
                                                           u'UpperRightCorner',
                                                           u'LowerRightCorner'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'vertex entry direction',
                                      {'name': u'Vertex Entry Direction',
                                       'pyname': u'vertex_entry_direction',
                                       'required-field': True,
                                       'autosizable': False,
                                       'accepted-values': [u'Counterclockwise',
                                                           u'Clockwise'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'coordinate system',
                                      {'name': u'Coordinate System',
                                       'pyname': u'coordinate_system',
                                       'required-field': True,
                                       'autosizable': False,
                                       'accepted-values': [u'Relative',
                                                           u'World',
                                                           u'Absolute'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'daylighting reference point coordinate system',
                                      {'name': u'Daylighting Reference Point Coordinate System',
                                       'pyname': u'daylighting_reference_point_coordinate_system',
                                       'default': u'Relative',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'Relative',
                                                           u'World',
                                                           u'Absolute'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'rectangular surface coordinate system',
                                      {'name': u'Rectangular Surface Coordinate System',
                                       'pyname': u'rectangular_surface_coordinate_system',
                                       'default': u'Relative',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'Relative',
                                                           u'World',
                                                           u'Absolute'],
                                       'autocalculatable': False,
                                       'type': 'alpha'})]),
              'format': None,
              'group': u'Thermal Zones and Surfaces',
              'min-fields': 0,
              'name': u'GlobalGeometryRules',
              'pyname': u'GlobalGeometryRules',
              'required-object': True,
              'unique-object': True}

    @property
    def starting_vertex_position(self):
        """Get starting_vertex_position.

        Returns:
            str: the value of `starting_vertex_position` or None if not set

        """
        return self["Starting Vertex Position"]

    @starting_vertex_position.setter
    def starting_vertex_position(self, value=None):
        """Corresponds to IDD field `Starting Vertex Position` Specified as
        entry for a 4 sided surface/rectangle Surfaces are specified as viewed
        from outside the surface Shading surfaces as viewed from behind.
        (towards what they are shading)

        Args:
            value (str): value for IDD Field `Starting Vertex Position`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Starting Vertex Position"] = value

    @property
    def vertex_entry_direction(self):
        """Get vertex_entry_direction.

        Returns:
            str: the value of `vertex_entry_direction` or None if not set

        """
        return self["Vertex Entry Direction"]

    @vertex_entry_direction.setter
    def vertex_entry_direction(self, value=None):
        """Corresponds to IDD field `Vertex Entry Direction`

        Args:
            value (str): value for IDD Field `Vertex Entry Direction`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Vertex Entry Direction"] = value

    @property
    def coordinate_system(self):
        """Get coordinate_system.

        Returns:
            str: the value of `coordinate_system` or None if not set

        """
        return self["Coordinate System"]

    @coordinate_system.setter
    def coordinate_system(self, value=None):
        """  Corresponds to IDD field `Coordinate System`
        relative -- coordinates are entered relative to zone origin
        world -- all coordinates entered are "absolute" for this facility
        absolute -- same as world

        Args:
            value (str): value for IDD Field `Coordinate System`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Coordinate System"] = value

    @property
    def daylighting_reference_point_coordinate_system(self):
        """Get daylighting_reference_point_coordinate_system.

        Returns:
            str: the value of `daylighting_reference_point_coordinate_system` or None if not set

        """
        return self["Daylighting Reference Point Coordinate System"]

    @daylighting_reference_point_coordinate_system.setter
    def daylighting_reference_point_coordinate_system(self, value="Relative"):
        """  Corresponds to IDD field `Daylighting Reference Point Coordinate System`
        Relative -- coordinates are entered relative to zone origin
        World -- all coordinates entered are "absolute" for this facility
        absolute -- same as world

        Args:
            value (str): value for IDD Field `Daylighting Reference Point Coordinate System`
                Default value: Relative
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Daylighting Reference Point Coordinate System"] = value

    @property
    def rectangular_surface_coordinate_system(self):
        """Get rectangular_surface_coordinate_system.

        Returns:
            str: the value of `rectangular_surface_coordinate_system` or None if not set

        """
        return self["Rectangular Surface Coordinate System"]

    @rectangular_surface_coordinate_system.setter
    def rectangular_surface_coordinate_system(self, value="Relative"):
        """  Corresponds to IDD field `Rectangular Surface Coordinate System`
        Relative -- Starting corner is entered relative to zone origin
        World -- Starting corner is entered in "absolute"
        absolute -- same as world

        Args:
            value (str): value for IDD Field `Rectangular Surface Coordinate System`
                Default value: Relative
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Rectangular Surface Coordinate System"] = value




class GeometryTransform(DataObject):

    """Corresponds to IDD object `GeometryTransform` Provides a simple method
    of altering the footprint geometry of a model.

    The intent is to provide a single parameter that can be used to
    reshape the building description contained in the rest of the input
    file.

    """
    schema = {'extensible-fields': OrderedDict(),
              'fields': OrderedDict([(u'plane of transform',
                                      {'name': u'Plane of Transform',
                                       'pyname': u'plane_of_transform',
                                       'default': u'XY',
                                       'required-field': True,
                                       'autosizable': False,
                                       'accepted-values': [u'XY'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'current aspect ratio',
                                      {'name': u'Current Aspect Ratio',
                                       'pyname': u'current_aspect_ratio',
                                       'minimum>': 0.0,
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real'}),
                                     (u'new aspect ratio',
                                      {'name': u'New Aspect Ratio',
                                       'pyname': u'new_aspect_ratio',
                                       'minimum>': 0.0,
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real'})]),
              'format': None,
              'group': u'Thermal Zones and Surfaces',
              'min-fields': 0,
              'name': u'GeometryTransform',
              'pyname': u'GeometryTransform',
              'required-object': False,
              'unique-object': True}

    @property
    def plane_of_transform(self):
        """Get plane_of_transform.

        Returns:
            str: the value of `plane_of_transform` or None if not set

        """
        return self["Plane of Transform"]

    @plane_of_transform.setter
    def plane_of_transform(self, value="XY"):
        """Corresponds to IDD field `Plane of Transform` only current allowed
        value is "XY".

        Args:
            value (str): value for IDD Field `Plane of Transform`
                Default value: XY
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Plane of Transform"] = value

    @property
    def current_aspect_ratio(self):
        """Get current_aspect_ratio.

        Returns:
            float: the value of `current_aspect_ratio` or None if not set

        """
        return self["Current Aspect Ratio"]

    @current_aspect_ratio.setter
    def current_aspect_ratio(self, value=None):
        """Corresponds to IDD field `Current Aspect Ratio` Aspect ratio of
        building as described in idf.

        Args:
            value (float): value for IDD Field `Current Aspect Ratio`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Current Aspect Ratio"] = value

    @property
    def new_aspect_ratio(self):
        """Get new_aspect_ratio.

        Returns:
            float: the value of `new_aspect_ratio` or None if not set

        """
        return self["New Aspect Ratio"]

    @new_aspect_ratio.setter
    def new_aspect_ratio(self, value=None):
        """Corresponds to IDD field `New Aspect Ratio` Aspect ratio to
        transform to during run.

        Args:
            value (float): value for IDD Field `New Aspect Ratio`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["New Aspect Ratio"] = value




class Zone(DataObject):

    """Corresponds to IDD object `Zone` Defines a thermal zone of the
    building."""
    schema = {'extensible-fields': OrderedDict(),
              'fields': OrderedDict([(u'name',
                                      {'name': u'Name',
                                       'pyname': u'name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'alpha'}),
                                     (u'direction of relative north',
                                      {'name': u'Direction of Relative North',
                                       'pyname': u'direction_of_relative_north',
                                       'default': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'deg'}),
                                     (u'x origin',
                                      {'name': u'X Origin',
                                       'pyname': u'x_origin',
                                       'default': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'm'}),
                                     (u'y origin',
                                      {'name': u'Y Origin',
                                       'pyname': u'y_origin',
                                       'default': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'm'}),
                                     (u'z origin',
                                      {'name': u'Z Origin',
                                       'pyname': u'z_origin',
                                       'default': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'm'}),
                                     (u'type',
                                      {'name': u'Type',
                                       'pyname': u'type',
                                       'default': 1,
                                       'maximum': 1,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 1,
                                       'autocalculatable': False,
                                       'type': u'integer'}),
                                     (u'multiplier',
                                      {'name': u'Multiplier',
                                       'pyname': u'multiplier',
                                       'default': 1,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 1,
                                       'autocalculatable': False,
                                       'type': u'integer'}),
                                     (u'ceiling height',
                                      {'name': u'Ceiling Height',
                                       'pyname': u'ceiling_height',
                                       'default': 'autocalculate',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': True,
                                       'type': u'real',
                                       'unit': u'm'}),
                                     (u'volume',
                                      {'name': u'Volume',
                                       'pyname': u'volume',
                                       'default': 'autocalculate',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': True,
                                       'type': u'real',
                                       'unit': u'm3'}),
                                     (u'floor area',
                                      {'name': u'Floor Area',
                                       'pyname': u'floor_area',
                                       'default': 'autocalculate',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': True,
                                       'type': u'real',
                                       'unit': u'm2'}),
                                     (u'zone inside convection algorithm',
                                      {'name': u'Zone Inside Convection Algorithm',
                                       'pyname': u'zone_inside_convection_algorithm',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'Simple',
                                                           u'TARP',
                                                           u'CeilingDiffuser',
                                                           u'AdaptiveConvectionAlgorithm',
                                                           u'TrombeWall'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'zone outside convection algorithm',
                                      {'name': u'Zone Outside Convection Algorithm',
                                       'pyname': u'zone_outside_convection_algorithm',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'SimpleCombined',
                                                           u'TARP',
                                                           u'DOE-2',
                                                           u'MoWiTT',
                                                           u'AdaptiveConvectionAlgorithm'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'part of total floor area',
                                      {'name': u'Part of Total Floor Area',
                                       'pyname': u'part_of_total_floor_area',
                                       'default': u'Yes',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'Yes',
                                                           u'No'],
                                       'autocalculatable': False,
                                       'type': 'alpha'})]),
              'format': u'vertices',
              'group': u'Thermal Zones and Surfaces',
              'min-fields': 0,
              'name': u'Zone',
              'pyname': u'Zone',
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
    def direction_of_relative_north(self):
        """Get direction_of_relative_north.

        Returns:
            float: the value of `direction_of_relative_north` or None if not set

        """
        return self["Direction of Relative North"]

    @direction_of_relative_north.setter
    def direction_of_relative_north(self, value=None):
        """Corresponds to IDD field `Direction of Relative North`

        Args:
            value (float): value for IDD Field `Direction of Relative North`
                Units: deg
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Direction of Relative North"] = value

    @property
    def x_origin(self):
        """Get x_origin.

        Returns:
            float: the value of `x_origin` or None if not set

        """
        return self["X Origin"]

    @x_origin.setter
    def x_origin(self, value=None):
        """Corresponds to IDD field `X Origin`

        Args:
            value (float): value for IDD Field `X Origin`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["X Origin"] = value

    @property
    def y_origin(self):
        """Get y_origin.

        Returns:
            float: the value of `y_origin` or None if not set

        """
        return self["Y Origin"]

    @y_origin.setter
    def y_origin(self, value=None):
        """Corresponds to IDD field `Y Origin`

        Args:
            value (float): value for IDD Field `Y Origin`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Y Origin"] = value

    @property
    def z_origin(self):
        """Get z_origin.

        Returns:
            float: the value of `z_origin` or None if not set

        """
        return self["Z Origin"]

    @z_origin.setter
    def z_origin(self, value=None):
        """Corresponds to IDD field `Z Origin`

        Args:
            value (float): value for IDD Field `Z Origin`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Z Origin"] = value

    @property
    def type(self):
        """Get type.

        Returns:
            int: the value of `type` or None if not set

        """
        return self["Type"]

    @type.setter
    def type(self, value=1):
        """Corresponds to IDD field `Type`

        Args:
            value (int): value for IDD Field `Type`
                Default value: 1
                value >= 1
                value <= 1
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Type"] = value

    @property
    def multiplier(self):
        """Get multiplier.

        Returns:
            int: the value of `multiplier` or None if not set

        """
        return self["Multiplier"]

    @multiplier.setter
    def multiplier(self, value=1):
        """Corresponds to IDD field `Multiplier`

        Args:
            value (int): value for IDD Field `Multiplier`
                Default value: 1
                value >= 1
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Multiplier"] = value

    @property
    def ceiling_height(self):
        """Get ceiling_height.

        Returns:
            float: the value of `ceiling_height` or None if not set

        """
        return self["Ceiling Height"]

    @ceiling_height.setter
    def ceiling_height(self, value="autocalculate"):
        """  Corresponds to IDD field `Ceiling Height`
        If this field is 0.0, negative or autocalculate, then the average height
        of the zone is automatically calculated and used in subsequent calculations.
        If this field is positive, then the number entered here will be used.
        Note that the Zone Ceiling Height is the distance from the Floor to
        the Ceiling in the Zone, not an absolute height from the ground.

        Args:
            value (float or "Autocalculate"): value for IDD Field `Ceiling Height`
                Units: m
                Default value: "autocalculate"
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Ceiling Height"] = value

    @property
    def volume(self):
        """Get volume.

        Returns:
            float: the value of `volume` or None if not set

        """
        return self["Volume"]

    @volume.setter
    def volume(self, value="autocalculate"):
        """  Corresponds to IDD field `Volume`
        If this field is 0.0, negative or autocalculate, then the volume of the zone
        is automatically calculated and used in subsequent calculations.
        If this field is positive, then the number entered here will be used.

        Args:
            value (float or "Autocalculate"): value for IDD Field `Volume`
                Units: m3
                Default value: "autocalculate"
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Volume"] = value

    @property
    def floor_area(self):
        """Get floor_area.

        Returns:
            float: the value of `floor_area` or None if not set

        """
        return self["Floor Area"]

    @floor_area.setter
    def floor_area(self, value="autocalculate"):
        """  Corresponds to IDD field `Floor Area`
        If this field is 0.0, negative or autocalculate, then the floor area of the zone
        is automatically calculated and used in subsequent calculations.
        If this field is positive, then the number entered here will be used.

        Args:
            value (float or "Autocalculate"): value for IDD Field `Floor Area`
                Units: m2
                Default value: "autocalculate"
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Floor Area"] = value

    @property
    def zone_inside_convection_algorithm(self):
        """Get zone_inside_convection_algorithm.

        Returns:
            str: the value of `zone_inside_convection_algorithm` or None if not set

        """
        return self["Zone Inside Convection Algorithm"]

    @zone_inside_convection_algorithm.setter
    def zone_inside_convection_algorithm(self, value=None):
        """  Corresponds to IDD field `Zone Inside Convection Algorithm`
        Will default to same value as SurfaceConvectionAlgorithm:Inside object
        setting this field overrides the default SurfaceConvectionAlgorithm:Inside for this zone
        Simple = constant natural convection (ASHRAE)
        TARP = variable natural convection based on temperature difference (ASHRAE)
        CeilingDiffuser = ACH based forced and mixed convection correlations
        for ceiling diffuser configuration with simple natural convection limit
        AdaptiveConvectionAlgorithm = dynamic selection of convection models based on conditions
        TrombeWall = variable natural convection in an enclosed rectangular cavity

        Args:
            value (str): value for IDD Field `Zone Inside Convection Algorithm`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Zone Inside Convection Algorithm"] = value

    @property
    def zone_outside_convection_algorithm(self):
        """Get zone_outside_convection_algorithm.

        Returns:
            str: the value of `zone_outside_convection_algorithm` or None if not set

        """
        return self["Zone Outside Convection Algorithm"]

    @zone_outside_convection_algorithm.setter
    def zone_outside_convection_algorithm(self, value=None):
        """  Corresponds to IDD field `Zone Outside Convection Algorithm`
        Will default to same value as SurfaceConvectionAlgorithm:Outside object
        setting this field overrides the default SurfaceConvectionAlgorithm:Outside for this zone
        SimpleCombined = Combined radiation and convection coefficient using simple ASHRAE model
        TARP = correlation from models developed by ASHRAE, Walton, and Sparrow et. al.
        MoWiTT = correlation from measurements by Klems and Yazdanian for smooth surfaces
        DOE-2 = correlation from measurements by Klems and Yazdanian for rough surfaces
        AdaptiveConvectionAlgorithm = dynamic selection of correlations based on conditions

        Args:
            value (str): value for IDD Field `Zone Outside Convection Algorithm`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Zone Outside Convection Algorithm"] = value

    @property
    def part_of_total_floor_area(self):
        """Get part_of_total_floor_area.

        Returns:
            str: the value of `part_of_total_floor_area` or None if not set

        """
        return self["Part of Total Floor Area"]

    @part_of_total_floor_area.setter
    def part_of_total_floor_area(self, value="Yes"):
        """Corresponds to IDD field `Part of Total Floor Area`

        Args:
            value (str): value for IDD Field `Part of Total Floor Area`
                Default value: Yes
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Part of Total Floor Area"] = value




class ZoneList(DataObject):

    """Corresponds to IDD object `ZoneList` Defines a list of thermal zones
    which can be referenced as a group.

    The ZoneList name
    may be used elsewhere in the input to apply a parameter to all zones in the list.
    ZoneLists can be used effectively with the following objects: People, Lights,
    ElectricEquipment, GasEquipment, HotWaterEquipment, ZoneInfiltration:DesignFlowRate,
    ZoneVentilation:DesignFlowRate, Sizing:Zone, ZoneControl:Thermostat, and others.

    """
    schema = {'extensible-fields': OrderedDict([(u'zone 1 name',
                                                 {'name': u'Zone 1 Name',
                                                  'pyname': u'zone_1_name',
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
                                       'type': u'alpha'})]),
              'format': None,
              'group': u'Thermal Zones and Surfaces',
              'min-fields': 2,
              'name': u'ZoneList',
              'pyname': u'ZoneList',
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
        """Corresponds to IDD field `Name` Name of the Zone List.

        Args:
            value (str): value for IDD Field `Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Name"] = value

    def add_extensible(self,
                       zone_1_name=None,
                       ):
        """Add values for extensible fields.

        Args:

            zone_1_name (str): value for IDD Field `Zone 1 Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        """
        vals = []
        zone_1_name = self.check_value("Zone 1 Name", zone_1_name)
        vals.append(zone_1_name)
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




class ZoneGroup(DataObject):

    """Corresponds to IDD object `ZoneGroup` Adds a multiplier to a ZoneList.

    This can be used to reduce the amount of input
    necessary for simulating repetitive structures, such as the identical floors of a
    multi-story building.

    """
    schema = {'extensible-fields': OrderedDict(),
              'fields': OrderedDict([(u'name',
                                      {'name': u'Name',
                                       'pyname': u'name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'alpha'}),
                                     (u'zone list name',
                                      {'name': u'Zone List Name',
                                       'pyname': u'zone_list_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'zone list multiplier',
                                      {'name': u'Zone List Multiplier',
                                       'pyname': u'zone_list_multiplier',
                                       'default': 1,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 1,
                                       'autocalculatable': False,
                                       'type': u'integer'})]),
              'format': None,
              'group': u'Thermal Zones and Surfaces',
              'min-fields': 2,
              'name': u'ZoneGroup',
              'pyname': u'ZoneGroup',
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
        """Corresponds to IDD field `Name` Name of the Zone Group.

        Args:
            value (str): value for IDD Field `Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Name"] = value

    @property
    def zone_list_name(self):
        """Get zone_list_name.

        Returns:
            str: the value of `zone_list_name` or None if not set

        """
        return self["Zone List Name"]

    @zone_list_name.setter
    def zone_list_name(self, value=None):
        """Corresponds to IDD field `Zone List Name`

        Args:
            value (str): value for IDD Field `Zone List Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Zone List Name"] = value

    @property
    def zone_list_multiplier(self):
        """Get zone_list_multiplier.

        Returns:
            int: the value of `zone_list_multiplier` or None if not set

        """
        return self["Zone List Multiplier"]

    @zone_list_multiplier.setter
    def zone_list_multiplier(self, value=1):
        """Corresponds to IDD field `Zone List Multiplier`

        Args:
            value (int): value for IDD Field `Zone List Multiplier`
                Default value: 1
                value >= 1
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Zone List Multiplier"] = value




class BuildingSurfaceDetailed(DataObject):

    """ Corresponds to IDD object `BuildingSurface:Detailed`
        Allows for detailed entry of building heat transfer surfaces.  Does not include subsurfaces such as windows or doors.
    """
    schema = {'extensible-fields': OrderedDict([(u'vertex 1 x-coordinate',
                                                 {'name': u'Vertex 1 X-coordinate',
                                                  'pyname': u'vertex_1_xcoordinate',
                                                  'required-field': True,
                                                  'autosizable': False,
                                                  'autocalculatable': False,
                                                  'type': u'real',
                                                  'unit': u'm'}),
                                                (u'vertex 1 y-coordinate',
                                                 {'name': u'Vertex 1 Y-coordinate',
                                                  'pyname': u'vertex_1_ycoordinate',
                                                  'required-field': True,
                                                  'autosizable': False,
                                                  'autocalculatable': False,
                                                  'type': u'real',
                                                  'unit': u'm'}),
                                                (u'vertex 1 z-coordinate',
                                                 {'name': u'Vertex 1 Z-coordinate',
                                                  'pyname': u'vertex_1_zcoordinate',
                                                  'required-field': True,
                                                  'autosizable': False,
                                                  'autocalculatable': False,
                                                  'type': u'real',
                                                  'unit': u'm'})]),
              'fields': OrderedDict([(u'name',
                                      {'name': u'Name',
                                       'pyname': u'name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'alpha'}),
                                     (u'surface type',
                                      {'name': u'Surface Type',
                                       'pyname': u'surface_type',
                                       'required-field': True,
                                       'autosizable': False,
                                       'accepted-values': [u'Floor',
                                                           u'Wall',
                                                           u'Ceiling',
                                                           u'Roof'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'construction name',
                                      {'name': u'Construction Name',
                                       'pyname': u'construction_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'zone name',
                                      {'name': u'Zone Name',
                                       'pyname': u'zone_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'outside boundary condition',
                                      {'name': u'Outside Boundary Condition',
                                       'pyname': u'outside_boundary_condition',
                                       'required-field': True,
                                       'autosizable': False,
                                       'accepted-values': [u'Adiabatic',
                                                           u'Surface',
                                                           u'Zone',
                                                           u'Outdoors',
                                                           u'Ground',
                                                           u'GroundFCfactorMethod',
                                                           u'OtherSideCoefficients',
                                                           u'OtherSideConditionsModel',
                                                           u'GroundSlabPreprocessorAverage',
                                                           u'GroundSlabPreprocessorCore',
                                                           u'GroundSlabPreprocessorPerimeter',
                                                           u'GroundBasementPreprocessorAverageWall',
                                                           u'GroundBasementPreprocessorAverageFloor',
                                                           u'GroundBasementPreprocessorUpperWall',
                                                           u'GroundBasementPreprocessorLowerWall'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'outside boundary condition object',
                                      {'name': u'Outside Boundary Condition Object',
                                       'pyname': u'outside_boundary_condition_object',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'sun exposure',
                                      {'name': u'Sun Exposure',
                                       'pyname': u'sun_exposure',
                                       'default': u'SunExposed',
                                       'required-field': True,
                                       'autosizable': False,
                                       'accepted-values': [u'SunExposed',
                                                           u'NoSun'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'wind exposure',
                                      {'name': u'Wind Exposure',
                                       'pyname': u'wind_exposure',
                                       'default': u'WindExposed',
                                       'required-field': True,
                                       'autosizable': False,
                                       'accepted-values': [u'WindExposed',
                                                           u'NoWind'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'view factor to ground',
                                      {'name': u'View Factor to Ground',
                                       'pyname': u'view_factor_to_ground',
                                       'default': 'autocalculate',
                                       'maximum': 1.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': True,
                                       'type': u'real'}),
                                     (u'number of vertices',
                                      {'name': u'Number of Vertices',
                                       'pyname': u'number_of_vertices',
                                       'default': 'autocalculate',
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 3.0,
                                       'autocalculatable': True,
                                       'type': 'real'})]),
              'format': u'vertices',
              'group': u'Thermal Zones and Surfaces',
              'min-fields': 19,
              'name': u'BuildingSurface:Detailed',
              'pyname': u'BuildingSurfaceDetailed',
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
    def surface_type(self):
        """Get surface_type.

        Returns:
            str: the value of `surface_type` or None if not set

        """
        return self["Surface Type"]

    @surface_type.setter
    def surface_type(self, value=None):
        """Corresponds to IDD field `Surface Type`

        Args:
            value (str): value for IDD Field `Surface Type`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Surface Type"] = value

    @property
    def construction_name(self):
        """Get construction_name.

        Returns:
            str: the value of `construction_name` or None if not set

        """
        return self["Construction Name"]

    @construction_name.setter
    def construction_name(self, value=None):
        """Corresponds to IDD field `Construction Name` To be matched with a
        construction in this input file.

        Args:
            value (str): value for IDD Field `Construction Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Construction Name"] = value

    @property
    def zone_name(self):
        """Get zone_name.

        Returns:
            str: the value of `zone_name` or None if not set

        """
        return self["Zone Name"]

    @zone_name.setter
    def zone_name(self, value=None):
        """Corresponds to IDD field `Zone Name` Zone the surface is a part of.

        Args:
            value (str): value for IDD Field `Zone Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Zone Name"] = value

    @property
    def outside_boundary_condition(self):
        """Get outside_boundary_condition.

        Returns:
            str: the value of `outside_boundary_condition` or None if not set

        """
        return self["Outside Boundary Condition"]

    @outside_boundary_condition.setter
    def outside_boundary_condition(self, value=None):
        """Corresponds to IDD field `Outside Boundary Condition`

        Args:
            value (str): value for IDD Field `Outside Boundary Condition`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Outside Boundary Condition"] = value

    @property
    def outside_boundary_condition_object(self):
        """Get outside_boundary_condition_object.

        Returns:
            str: the value of `outside_boundary_condition_object` or None if not set

        """
        return self["Outside Boundary Condition Object"]

    @outside_boundary_condition_object.setter
    def outside_boundary_condition_object(self, value=None):
        """  Corresponds to IDD field `Outside Boundary Condition Object`
        Non-blank only if the field Outside Boundary Condition is Surface,
        Zone, OtherSideCoefficients or OtherSideConditionsModel
        If Surface, specify name of corresponding surface in adjacent zone or
        specify current surface name for internal partition separating like zones
        If Zone, specify the name of the corresponding zone and
        the program will generate the corresponding interzone surface
        If OtherSideCoefficients, specify name of SurfaceProperty:OtherSideCoefficients
        If OtherSideConditionsModel, specify name of SurfaceProperty:OtherSideConditionsModel

        Args:
            value (str): value for IDD Field `Outside Boundary Condition Object`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Outside Boundary Condition Object"] = value

    @property
    def sun_exposure(self):
        """Get sun_exposure.

        Returns:
            str: the value of `sun_exposure` or None if not set

        """
        return self["Sun Exposure"]

    @sun_exposure.setter
    def sun_exposure(self, value="SunExposed"):
        """Corresponds to IDD field `Sun Exposure`

        Args:
            value (str): value for IDD Field `Sun Exposure`
                Default value: SunExposed
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Sun Exposure"] = value

    @property
    def wind_exposure(self):
        """Get wind_exposure.

        Returns:
            str: the value of `wind_exposure` or None if not set

        """
        return self["Wind Exposure"]

    @wind_exposure.setter
    def wind_exposure(self, value="WindExposed"):
        """Corresponds to IDD field `Wind Exposure`

        Args:
            value (str): value for IDD Field `Wind Exposure`
                Default value: WindExposed
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Wind Exposure"] = value

    @property
    def view_factor_to_ground(self):
        """Get view_factor_to_ground.

        Returns:
            float: the value of `view_factor_to_ground` or None if not set

        """
        return self["View Factor to Ground"]

    @view_factor_to_ground.setter
    def view_factor_to_ground(self, value="autocalculate"):
        """  Corresponds to IDD field `View Factor to Ground`
        From the exterior of the surface
        Unused if one uses the "reflections" options in Solar Distribution in Building input
        unless a DaylightingDevice:Shelf or DaylightingDevice:Tubular object has been specified.
        autocalculate will automatically calculate this value from the tilt of the surface

        Args:
            value (float or "Autocalculate"): value for IDD Field `View Factor to Ground`
                Default value: "autocalculate"
                value <= 1.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["View Factor to Ground"] = value

    @property
    def number_of_vertices(self):
        """Get number_of_vertices.

        Returns:
            float: the value of `number_of_vertices` or None if not set

        """
        return self["Number of Vertices"]

    @number_of_vertices.setter
    def number_of_vertices(self, value="autocalculate"):
        """  Corresponds to IDD field `Number of Vertices`
        shown with 120 vertex coordinates -- extensible object
        "extensible" -- duplicate last set of x,y,z coordinates (last 3 fields),
        remembering to remove ; from "inner" fields.
        for clarity in any error messages, renumber the fields as well.
        (and changing z terminator to a comma "," for all but last one which needs a semi-colon ";")
        vertices are given in GlobalGeometryRules coordinates -- if relative, all surface coordinates
        are "relative" to the Zone Origin.  If world, then building and zone origins are used
        for some internal calculations, but all coordinates are given in an "absolute" system.

        Args:
            value (float or "Autocalculate"): value for IDD Field `Number of Vertices`
                Default value: "autocalculate"
                value >= 3.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Number of Vertices"] = value

    def add_extensible(self,
                       vertex_1_xcoordinate=None,
                       vertex_1_ycoordinate=None,
                       vertex_1_zcoordinate=None,
                       ):
        """Add values for extensible fields.

        Args:

            vertex_1_xcoordinate (float): value for IDD Field `Vertex 1 X-coordinate`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

            vertex_1_ycoordinate (float): value for IDD Field `Vertex 1 Y-coordinate`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

            vertex_1_zcoordinate (float): value for IDD Field `Vertex 1 Z-coordinate`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        """
        vals = []
        vertex_1_xcoordinate = self.check_value(
            "Vertex 1 X-coordinate",
            vertex_1_xcoordinate)
        vals.append(vertex_1_xcoordinate)
        vertex_1_ycoordinate = self.check_value(
            "Vertex 1 Y-coordinate",
            vertex_1_ycoordinate)
        vals.append(vertex_1_ycoordinate)
        vertex_1_zcoordinate = self.check_value(
            "Vertex 1 Z-coordinate",
            vertex_1_zcoordinate)
        vals.append(vertex_1_zcoordinate)
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




class WallDetailed(DataObject):

    """ Corresponds to IDD object `Wall:Detailed`
        Allows for detailed entry of wall heat transfer surfaces.
    """
    schema = {'extensible-fields': OrderedDict([(u'vertex 1 x-coordinate',
                                                 {'name': u'Vertex 1 X-coordinate',
                                                  'pyname': u'vertex_1_xcoordinate',
                                                  'required-field': True,
                                                  'autosizable': False,
                                                  'autocalculatable': False,
                                                  'type': u'real',
                                                  'unit': u'm'}),
                                                (u'vertex 1 y-coordinate',
                                                 {'name': u'Vertex 1 Y-coordinate',
                                                  'pyname': u'vertex_1_ycoordinate',
                                                  'required-field': True,
                                                  'autosizable': False,
                                                  'autocalculatable': False,
                                                  'type': u'real',
                                                  'unit': u'm'}),
                                                (u'vertex 1 z-coordinate',
                                                 {'name': u'Vertex 1 Z-coordinate',
                                                  'pyname': u'vertex_1_zcoordinate',
                                                  'required-field': True,
                                                  'autosizable': False,
                                                  'autocalculatable': False,
                                                  'type': u'real',
                                                  'unit': u'm'})]),
              'fields': OrderedDict([(u'name',
                                      {'name': u'Name',
                                       'pyname': u'name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'alpha'}),
                                     (u'construction name',
                                      {'name': u'Construction Name',
                                       'pyname': u'construction_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'zone name',
                                      {'name': u'Zone Name',
                                       'pyname': u'zone_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'outside boundary condition',
                                      {'name': u'Outside Boundary Condition',
                                       'pyname': u'outside_boundary_condition',
                                       'required-field': True,
                                       'autosizable': False,
                                       'accepted-values': [u'Adiabatic',
                                                           u'Surface',
                                                           u'Zone',
                                                           u'Outdoors',
                                                           u'Ground',
                                                           u'GroundFCfactorMethod',
                                                           u'OtherSideCoefficients',
                                                           u'OtherSideConditionsModel',
                                                           u'GroundSlabPreprocessorAverage',
                                                           u'GroundSlabPreprocessorCore',
                                                           u'GroundSlabPreprocessorPerimeter',
                                                           u'GroundBasementPreprocessorAverageWall',
                                                           u'GroundBasementPreprocessorAverageFloor',
                                                           u'GroundBasementPreprocessorUpperWall',
                                                           u'GroundBasementPreprocessorLowerWall'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'outside boundary condition object',
                                      {'name': u'Outside Boundary Condition Object',
                                       'pyname': u'outside_boundary_condition_object',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'sun exposure',
                                      {'name': u'Sun Exposure',
                                       'pyname': u'sun_exposure',
                                       'default': u'SunExposed',
                                       'required-field': True,
                                       'autosizable': False,
                                       'accepted-values': [u'SunExposed',
                                                           u'NoSun'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'wind exposure',
                                      {'name': u'Wind Exposure',
                                       'pyname': u'wind_exposure',
                                       'default': u'WindExposed',
                                       'required-field': True,
                                       'autosizable': False,
                                       'accepted-values': [u'WindExposed',
                                                           u'NoWind'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'view factor to ground',
                                      {'name': u'View Factor to Ground',
                                       'pyname': u'view_factor_to_ground',
                                       'default': 'autocalculate',
                                       'maximum': 1.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': True,
                                       'type': u'real'}),
                                     (u'number of vertices',
                                      {'name': u'Number of Vertices',
                                       'pyname': u'number_of_vertices',
                                       'default': 'autocalculate',
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 3.0,
                                       'autocalculatable': True,
                                       'type': 'real'})]),
              'format': u'vertices',
              'group': u'Thermal Zones and Surfaces',
              'min-fields': 18,
              'name': u'Wall:Detailed',
              'pyname': u'WallDetailed',
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
        """Corresponds to IDD field `Construction Name` To be matched with a
        construction in this input file.

        Args:
            value (str): value for IDD Field `Construction Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Construction Name"] = value

    @property
    def zone_name(self):
        """Get zone_name.

        Returns:
            str: the value of `zone_name` or None if not set

        """
        return self["Zone Name"]

    @zone_name.setter
    def zone_name(self, value=None):
        """Corresponds to IDD field `Zone Name` Zone the surface is a part of.

        Args:
            value (str): value for IDD Field `Zone Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Zone Name"] = value

    @property
    def outside_boundary_condition(self):
        """Get outside_boundary_condition.

        Returns:
            str: the value of `outside_boundary_condition` or None if not set

        """
        return self["Outside Boundary Condition"]

    @outside_boundary_condition.setter
    def outside_boundary_condition(self, value=None):
        """Corresponds to IDD field `Outside Boundary Condition`

        Args:
            value (str): value for IDD Field `Outside Boundary Condition`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Outside Boundary Condition"] = value

    @property
    def outside_boundary_condition_object(self):
        """Get outside_boundary_condition_object.

        Returns:
            str: the value of `outside_boundary_condition_object` or None if not set

        """
        return self["Outside Boundary Condition Object"]

    @outside_boundary_condition_object.setter
    def outside_boundary_condition_object(self, value=None):
        """  Corresponds to IDD field `Outside Boundary Condition Object`
        Non-blank only if the field Outside Boundary Condition is Surface,
        Zone, OtherSideCoefficients or OtherSideConditionsModel
        If Surface, specify name of corresponding surface in adjacent zone or
        specify current surface name for internal partition separating like zones
        If Zone, specify the name of the corresponding zone and
        the program will generate the corresponding interzone surface
        If OtherSideCoefficients, specify name of SurfaceProperty:OtherSideCoefficients
        If OtherSideConditionsModel, specify name of SurfaceProperty:OtherSideConditionsModel

        Args:
            value (str): value for IDD Field `Outside Boundary Condition Object`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Outside Boundary Condition Object"] = value

    @property
    def sun_exposure(self):
        """Get sun_exposure.

        Returns:
            str: the value of `sun_exposure` or None if not set

        """
        return self["Sun Exposure"]

    @sun_exposure.setter
    def sun_exposure(self, value="SunExposed"):
        """Corresponds to IDD field `Sun Exposure`

        Args:
            value (str): value for IDD Field `Sun Exposure`
                Default value: SunExposed
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Sun Exposure"] = value

    @property
    def wind_exposure(self):
        """Get wind_exposure.

        Returns:
            str: the value of `wind_exposure` or None if not set

        """
        return self["Wind Exposure"]

    @wind_exposure.setter
    def wind_exposure(self, value="WindExposed"):
        """Corresponds to IDD field `Wind Exposure`

        Args:
            value (str): value for IDD Field `Wind Exposure`
                Default value: WindExposed
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Wind Exposure"] = value

    @property
    def view_factor_to_ground(self):
        """Get view_factor_to_ground.

        Returns:
            float: the value of `view_factor_to_ground` or None if not set

        """
        return self["View Factor to Ground"]

    @view_factor_to_ground.setter
    def view_factor_to_ground(self, value="autocalculate"):
        """  Corresponds to IDD field `View Factor to Ground`
        From the exterior of the surface
        Unused if one uses the "reflections" options in Solar Distribution in Building input
        unless a DaylightingDevice:Shelf or DaylightingDevice:Tubular object has been specified.
        autocalculate will automatically calculate this value from the tilt of the surface

        Args:
            value (float or "Autocalculate"): value for IDD Field `View Factor to Ground`
                Default value: "autocalculate"
                value <= 1.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["View Factor to Ground"] = value

    @property
    def number_of_vertices(self):
        """Get number_of_vertices.

        Returns:
            float: the value of `number_of_vertices` or None if not set

        """
        return self["Number of Vertices"]

    @number_of_vertices.setter
    def number_of_vertices(self, value="autocalculate"):
        """  Corresponds to IDD field `Number of Vertices`
        shown with 10 vertex coordinates -- extensible object
        "extensible" -- duplicate last set of x,y,z coordinates, renumbering please
        (and changing z terminator to a comma "," for all but last one which needs a semi-colon ";")
        vertices are given in GlobalGeometryRules coordinates -- if relative, all surface coordinates
        are "relative" to the Zone Origin.  If world, then building and zone origins are used
        for some internal calculations, but all coordinates are given in an "absolute" system.

        Args:
            value (float or "Autocalculate"): value for IDD Field `Number of Vertices`
                Default value: "autocalculate"
                value >= 3.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Number of Vertices"] = value

    def add_extensible(self,
                       vertex_1_xcoordinate=None,
                       vertex_1_ycoordinate=None,
                       vertex_1_zcoordinate=None,
                       ):
        """Add values for extensible fields.

        Args:

            vertex_1_xcoordinate (float): value for IDD Field `Vertex 1 X-coordinate`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

            vertex_1_ycoordinate (float): value for IDD Field `Vertex 1 Y-coordinate`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

            vertex_1_zcoordinate (float): value for IDD Field `Vertex 1 Z-coordinate`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        """
        vals = []
        vertex_1_xcoordinate = self.check_value(
            "Vertex 1 X-coordinate",
            vertex_1_xcoordinate)
        vals.append(vertex_1_xcoordinate)
        vertex_1_ycoordinate = self.check_value(
            "Vertex 1 Y-coordinate",
            vertex_1_ycoordinate)
        vals.append(vertex_1_ycoordinate)
        vertex_1_zcoordinate = self.check_value(
            "Vertex 1 Z-coordinate",
            vertex_1_zcoordinate)
        vals.append(vertex_1_zcoordinate)
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




class RoofCeilingDetailed(DataObject):

    """ Corresponds to IDD object `RoofCeiling:Detailed`
        Allows for detailed entry of roof/ceiling heat transfer surfaces.
    """
    schema = {'extensible-fields': OrderedDict([(u'vertex 1 x-coordinate',
                                                 {'name': u'Vertex 1 X-coordinate',
                                                  'pyname': u'vertex_1_xcoordinate',
                                                  'required-field': True,
                                                  'autosizable': False,
                                                  'autocalculatable': False,
                                                  'type': u'real',
                                                  'unit': u'm'}),
                                                (u'vertex 1 y-coordinate',
                                                 {'name': u'Vertex 1 Y-coordinate',
                                                  'pyname': u'vertex_1_ycoordinate',
                                                  'required-field': True,
                                                  'autosizable': False,
                                                  'autocalculatable': False,
                                                  'type': u'real',
                                                  'unit': u'm'}),
                                                (u'vertex 1 z-coordinate',
                                                 {'name': u'Vertex 1 Z-coordinate',
                                                  'pyname': u'vertex_1_zcoordinate',
                                                  'required-field': True,
                                                  'autosizable': False,
                                                  'autocalculatable': False,
                                                  'type': u'real',
                                                  'unit': u'm'})]),
              'fields': OrderedDict([(u'name',
                                      {'name': u'Name',
                                       'pyname': u'name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'alpha'}),
                                     (u'construction name',
                                      {'name': u'Construction Name',
                                       'pyname': u'construction_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'zone name',
                                      {'name': u'Zone Name',
                                       'pyname': u'zone_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'outside boundary condition',
                                      {'name': u'Outside Boundary Condition',
                                       'pyname': u'outside_boundary_condition',
                                       'required-field': True,
                                       'autosizable': False,
                                       'accepted-values': [u'Adiabatic',
                                                           u'Surface',
                                                           u'Zone',
                                                           u'Outdoors',
                                                           u'Ground',
                                                           u'OtherSideCoefficients',
                                                           u'OtherSideConditionsModel',
                                                           u'GroundSlabPreprocessorAverage',
                                                           u'GroundSlabPreprocessorCore',
                                                           u'GroundSlabPreprocessorPerimeter',
                                                           u'GroundBasementPreprocessorAverageWall',
                                                           u'GroundBasementPreprocessorAverageFloor',
                                                           u'GroundBasementPreprocessorUpperWall',
                                                           u'GroundBasementPreprocessorLowerWall'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'outside boundary condition object',
                                      {'name': u'Outside Boundary Condition Object',
                                       'pyname': u'outside_boundary_condition_object',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'sun exposure',
                                      {'name': u'Sun Exposure',
                                       'pyname': u'sun_exposure',
                                       'default': u'SunExposed',
                                       'required-field': True,
                                       'autosizable': False,
                                       'accepted-values': [u'SunExposed',
                                                           u'NoSun'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'wind exposure',
                                      {'name': u'Wind Exposure',
                                       'pyname': u'wind_exposure',
                                       'default': u'WindExposed',
                                       'required-field': True,
                                       'autosizable': False,
                                       'accepted-values': [u'WindExposed',
                                                           u'NoWind'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'view factor to ground',
                                      {'name': u'View Factor to Ground',
                                       'pyname': u'view_factor_to_ground',
                                       'default': 'autocalculate',
                                       'maximum': 1.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': True,
                                       'type': u'real'}),
                                     (u'number of vertices',
                                      {'name': u'Number of Vertices',
                                       'pyname': u'number_of_vertices',
                                       'default': 'autocalculate',
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 3.0,
                                       'autocalculatable': True,
                                       'type': 'real'})]),
              'format': u'vertices',
              'group': u'Thermal Zones and Surfaces',
              'min-fields': 18,
              'name': u'RoofCeiling:Detailed',
              'pyname': u'RoofCeilingDetailed',
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
        """Corresponds to IDD field `Construction Name` To be matched with a
        construction in this input file.

        Args:
            value (str): value for IDD Field `Construction Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Construction Name"] = value

    @property
    def zone_name(self):
        """Get zone_name.

        Returns:
            str: the value of `zone_name` or None if not set

        """
        return self["Zone Name"]

    @zone_name.setter
    def zone_name(self, value=None):
        """Corresponds to IDD field `Zone Name` Zone the surface is a part of.

        Args:
            value (str): value for IDD Field `Zone Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Zone Name"] = value

    @property
    def outside_boundary_condition(self):
        """Get outside_boundary_condition.

        Returns:
            str: the value of `outside_boundary_condition` or None if not set

        """
        return self["Outside Boundary Condition"]

    @outside_boundary_condition.setter
    def outside_boundary_condition(self, value=None):
        """Corresponds to IDD field `Outside Boundary Condition`

        Args:
            value (str): value for IDD Field `Outside Boundary Condition`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Outside Boundary Condition"] = value

    @property
    def outside_boundary_condition_object(self):
        """Get outside_boundary_condition_object.

        Returns:
            str: the value of `outside_boundary_condition_object` or None if not set

        """
        return self["Outside Boundary Condition Object"]

    @outside_boundary_condition_object.setter
    def outside_boundary_condition_object(self, value=None):
        """  Corresponds to IDD field `Outside Boundary Condition Object`
        Non-blank only if the field Outside Boundary Condition is Surface,
        Zone, OtherSideCoefficients or OtherSideConditionsModel
        If Surface, specify name of corresponding surface in adjacent zone or
        specify current surface name for internal partition separating like zones
        If Zone, specify the name of the corresponding zone and
        the program will generate the corresponding interzone surface
        If OtherSideCoefficients, specify name of SurfaceProperty:OtherSideCoefficients
        If OtherSideConditionsModel, specify name of SurfaceProperty:OtherSideConditionsModel

        Args:
            value (str): value for IDD Field `Outside Boundary Condition Object`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Outside Boundary Condition Object"] = value

    @property
    def sun_exposure(self):
        """Get sun_exposure.

        Returns:
            str: the value of `sun_exposure` or None if not set

        """
        return self["Sun Exposure"]

    @sun_exposure.setter
    def sun_exposure(self, value="SunExposed"):
        """Corresponds to IDD field `Sun Exposure`

        Args:
            value (str): value for IDD Field `Sun Exposure`
                Default value: SunExposed
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Sun Exposure"] = value

    @property
    def wind_exposure(self):
        """Get wind_exposure.

        Returns:
            str: the value of `wind_exposure` or None if not set

        """
        return self["Wind Exposure"]

    @wind_exposure.setter
    def wind_exposure(self, value="WindExposed"):
        """Corresponds to IDD field `Wind Exposure`

        Args:
            value (str): value for IDD Field `Wind Exposure`
                Default value: WindExposed
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Wind Exposure"] = value

    @property
    def view_factor_to_ground(self):
        """Get view_factor_to_ground.

        Returns:
            float: the value of `view_factor_to_ground` or None if not set

        """
        return self["View Factor to Ground"]

    @view_factor_to_ground.setter
    def view_factor_to_ground(self, value="autocalculate"):
        """  Corresponds to IDD field `View Factor to Ground`
        From the exterior of the surface
        Unused if one uses the "reflections" options in Solar Distribution in Building input
        unless a DaylightingDevice:Shelf or DaylightingDevice:Tubular object has been specified.
        autocalculate will automatically calculate this value from the tilt of the surface

        Args:
            value (float or "Autocalculate"): value for IDD Field `View Factor to Ground`
                Default value: "autocalculate"
                value <= 1.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["View Factor to Ground"] = value

    @property
    def number_of_vertices(self):
        """Get number_of_vertices.

        Returns:
            float: the value of `number_of_vertices` or None if not set

        """
        return self["Number of Vertices"]

    @number_of_vertices.setter
    def number_of_vertices(self, value="autocalculate"):
        """  Corresponds to IDD field `Number of Vertices`
        shown with 10 vertex coordinates -- extensible object
        "extensible" -- duplicate last set of x,y,z coordinates, renumbering please
        (and changing z terminator to a comma "," for all but last one which needs a semi-colon ";")
        vertices are given in GlobalGeometryRules coordinates -- if relative, all surface coordinates
        are "relative" to the Zone Origin.  If world, then building and zone origins are used
        for some internal calculations, but all coordinates are given in an "absolute" system.

        Args:
            value (float or "Autocalculate"): value for IDD Field `Number of Vertices`
                Default value: "autocalculate"
                value >= 3.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Number of Vertices"] = value

    def add_extensible(self,
                       vertex_1_xcoordinate=None,
                       vertex_1_ycoordinate=None,
                       vertex_1_zcoordinate=None,
                       ):
        """Add values for extensible fields.

        Args:

            vertex_1_xcoordinate (float): value for IDD Field `Vertex 1 X-coordinate`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

            vertex_1_ycoordinate (float): value for IDD Field `Vertex 1 Y-coordinate`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

            vertex_1_zcoordinate (float): value for IDD Field `Vertex 1 Z-coordinate`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        """
        vals = []
        vertex_1_xcoordinate = self.check_value(
            "Vertex 1 X-coordinate",
            vertex_1_xcoordinate)
        vals.append(vertex_1_xcoordinate)
        vertex_1_ycoordinate = self.check_value(
            "Vertex 1 Y-coordinate",
            vertex_1_ycoordinate)
        vals.append(vertex_1_ycoordinate)
        vertex_1_zcoordinate = self.check_value(
            "Vertex 1 Z-coordinate",
            vertex_1_zcoordinate)
        vals.append(vertex_1_zcoordinate)
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




class FloorDetailed(DataObject):

    """ Corresponds to IDD object `Floor:Detailed`
        Allows for detailed entry of floor heat transfer surfaces.
    """
    schema = {'extensible-fields': OrderedDict([(u'vertex 1 x-coordinate',
                                                 {'name': u'Vertex 1 X-coordinate',
                                                  'pyname': u'vertex_1_xcoordinate',
                                                  'required-field': True,
                                                  'autosizable': False,
                                                  'autocalculatable': False,
                                                  'type': u'real',
                                                  'unit': u'm'}),
                                                (u'vertex 1 y-coordinate',
                                                 {'name': u'Vertex 1 Y-coordinate',
                                                  'pyname': u'vertex_1_ycoordinate',
                                                  'required-field': True,
                                                  'autosizable': False,
                                                  'autocalculatable': False,
                                                  'type': u'real',
                                                  'unit': u'm'}),
                                                (u'vertex 1 z-coordinate',
                                                 {'name': u'Vertex 1 Z-coordinate',
                                                  'pyname': u'vertex_1_zcoordinate',
                                                  'required-field': True,
                                                  'autosizable': False,
                                                  'autocalculatable': False,
                                                  'type': u'real',
                                                  'unit': u'm'})]),
              'fields': OrderedDict([(u'name',
                                      {'name': u'Name',
                                       'pyname': u'name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'alpha'}),
                                     (u'construction name',
                                      {'name': u'Construction Name',
                                       'pyname': u'construction_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'zone name',
                                      {'name': u'Zone Name',
                                       'pyname': u'zone_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'outside boundary condition',
                                      {'name': u'Outside Boundary Condition',
                                       'pyname': u'outside_boundary_condition',
                                       'required-field': True,
                                       'autosizable': False,
                                       'accepted-values': [u'Adiabatic',
                                                           u'Surface',
                                                           u'Zone',
                                                           u'Outdoors',
                                                           u'Ground',
                                                           u'GroundFCfactorMethod',
                                                           u'OtherSideCoefficients',
                                                           u'OtherSideConditionsModel',
                                                           u'GroundSlabPreprocessorAverage',
                                                           u'GroundSlabPreprocessorCore',
                                                           u'GroundSlabPreprocessorPerimeter',
                                                           u'GroundBasementPreprocessorAverageWall',
                                                           u'GroundBasementPreprocessorAverageFloor',
                                                           u'GroundBasementPreprocessorUpperWall',
                                                           u'GroundBasementPreprocessorLowerWall'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'outside boundary condition object',
                                      {'name': u'Outside Boundary Condition Object',
                                       'pyname': u'outside_boundary_condition_object',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'sun exposure',
                                      {'name': u'Sun Exposure',
                                       'pyname': u'sun_exposure',
                                       'default': u'SunExposed',
                                       'required-field': True,
                                       'autosizable': False,
                                       'accepted-values': [u'SunExposed',
                                                           u'NoSun'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'wind exposure',
                                      {'name': u'Wind Exposure',
                                       'pyname': u'wind_exposure',
                                       'default': u'WindExposed',
                                       'required-field': True,
                                       'autosizable': False,
                                       'accepted-values': [u'WindExposed',
                                                           u'NoWind'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'view factor to ground',
                                      {'name': u'View Factor to Ground',
                                       'pyname': u'view_factor_to_ground',
                                       'default': 'autocalculate',
                                       'maximum': 1.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': True,
                                       'type': u'real'}),
                                     (u'number of vertices',
                                      {'name': u'Number of Vertices',
                                       'pyname': u'number_of_vertices',
                                       'default': 'autocalculate',
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 3.0,
                                       'autocalculatable': True,
                                       'type': 'real'})]),
              'format': u'vertices',
              'group': u'Thermal Zones and Surfaces',
              'min-fields': 18,
              'name': u'Floor:Detailed',
              'pyname': u'FloorDetailed',
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
        """Corresponds to IDD field `Construction Name` To be matched with a
        construction in this input file.

        Args:
            value (str): value for IDD Field `Construction Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Construction Name"] = value

    @property
    def zone_name(self):
        """Get zone_name.

        Returns:
            str: the value of `zone_name` or None if not set

        """
        return self["Zone Name"]

    @zone_name.setter
    def zone_name(self, value=None):
        """Corresponds to IDD field `Zone Name` Zone the surface is a part of.

        Args:
            value (str): value for IDD Field `Zone Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Zone Name"] = value

    @property
    def outside_boundary_condition(self):
        """Get outside_boundary_condition.

        Returns:
            str: the value of `outside_boundary_condition` or None if not set

        """
        return self["Outside Boundary Condition"]

    @outside_boundary_condition.setter
    def outside_boundary_condition(self, value=None):
        """Corresponds to IDD field `Outside Boundary Condition`

        Args:
            value (str): value for IDD Field `Outside Boundary Condition`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Outside Boundary Condition"] = value

    @property
    def outside_boundary_condition_object(self):
        """Get outside_boundary_condition_object.

        Returns:
            str: the value of `outside_boundary_condition_object` or None if not set

        """
        return self["Outside Boundary Condition Object"]

    @outside_boundary_condition_object.setter
    def outside_boundary_condition_object(self, value=None):
        """  Corresponds to IDD field `Outside Boundary Condition Object`
        Non-blank only if the field Outside Boundary Condition is Surface,
        Zone, OtherSideCoefficients or OtherSideConditionsModel
        If Surface, specify name of corresponding surface in adjacent zone or
        specify current surface name for internal partition separating like zones
        If Zone, specify the name of the corresponding zone and
        the program will generate the corresponding interzone surface
        If OtherSideCoefficients, specify name of SurfaceProperty:OtherSideCoefficients
        If OtherSideConditionsModel, specify name of SurfaceProperty:OtherSideConditionsModel

        Args:
            value (str): value for IDD Field `Outside Boundary Condition Object`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Outside Boundary Condition Object"] = value

    @property
    def sun_exposure(self):
        """Get sun_exposure.

        Returns:
            str: the value of `sun_exposure` or None if not set

        """
        return self["Sun Exposure"]

    @sun_exposure.setter
    def sun_exposure(self, value="SunExposed"):
        """Corresponds to IDD field `Sun Exposure`

        Args:
            value (str): value for IDD Field `Sun Exposure`
                Default value: SunExposed
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Sun Exposure"] = value

    @property
    def wind_exposure(self):
        """Get wind_exposure.

        Returns:
            str: the value of `wind_exposure` or None if not set

        """
        return self["Wind Exposure"]

    @wind_exposure.setter
    def wind_exposure(self, value="WindExposed"):
        """Corresponds to IDD field `Wind Exposure`

        Args:
            value (str): value for IDD Field `Wind Exposure`
                Default value: WindExposed
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Wind Exposure"] = value

    @property
    def view_factor_to_ground(self):
        """Get view_factor_to_ground.

        Returns:
            float: the value of `view_factor_to_ground` or None if not set

        """
        return self["View Factor to Ground"]

    @view_factor_to_ground.setter
    def view_factor_to_ground(self, value="autocalculate"):
        """  Corresponds to IDD field `View Factor to Ground`
        From the exterior of the surface
        Unused if one uses the "reflections" options in Solar Distribution in Building input
        unless a DaylightingDevice:Shelf or DaylightingDevice:Tubular object has been specified.
        autocalculate will automatically calculate this value from the tilt of the surface

        Args:
            value (float or "Autocalculate"): value for IDD Field `View Factor to Ground`
                Default value: "autocalculate"
                value <= 1.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["View Factor to Ground"] = value

    @property
    def number_of_vertices(self):
        """Get number_of_vertices.

        Returns:
            float: the value of `number_of_vertices` or None if not set

        """
        return self["Number of Vertices"]

    @number_of_vertices.setter
    def number_of_vertices(self, value="autocalculate"):
        """  Corresponds to IDD field `Number of Vertices`
        shown with 10 vertex coordinates -- extensible object
        "extensible" -- duplicate last set of x,y,z coordinates, renumbering please
        (and changing z terminator to a comma "," for all but last one which needs a semi-colon ";")
        vertices are given in GlobalGeometryRules coordinates -- if relative, all surface coordinates
        are "relative" to the Zone Origin.  If world, then building and zone origins are used
        for some internal calculations, but all coordinates are given in an "absolute" system.

        Args:
            value (float or "Autocalculate"): value for IDD Field `Number of Vertices`
                Default value: "autocalculate"
                value >= 3.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Number of Vertices"] = value

    def add_extensible(self,
                       vertex_1_xcoordinate=None,
                       vertex_1_ycoordinate=None,
                       vertex_1_zcoordinate=None,
                       ):
        """Add values for extensible fields.

        Args:

            vertex_1_xcoordinate (float): value for IDD Field `Vertex 1 X-coordinate`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

            vertex_1_ycoordinate (float): value for IDD Field `Vertex 1 Y-coordinate`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

            vertex_1_zcoordinate (float): value for IDD Field `Vertex 1 Z-coordinate`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        """
        vals = []
        vertex_1_xcoordinate = self.check_value(
            "Vertex 1 X-coordinate",
            vertex_1_xcoordinate)
        vals.append(vertex_1_xcoordinate)
        vertex_1_ycoordinate = self.check_value(
            "Vertex 1 Y-coordinate",
            vertex_1_ycoordinate)
        vals.append(vertex_1_ycoordinate)
        vertex_1_zcoordinate = self.check_value(
            "Vertex 1 Z-coordinate",
            vertex_1_zcoordinate)
        vals.append(vertex_1_zcoordinate)
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




class WallExterior(DataObject):

    """ Corresponds to IDD object `Wall:Exterior`
        Allows for simplified entry of exterior walls.
        View Factor to Ground is automatically calculated.
    """
    schema = {'extensible-fields': OrderedDict(),
              'fields': OrderedDict([(u'name',
                                      {'name': u'Name',
                                       'pyname': u'name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'alpha'}),
                                     (u'construction name',
                                      {'name': u'Construction Name',
                                       'pyname': u'construction_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'zone name',
                                      {'name': u'Zone Name',
                                       'pyname': u'zone_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'azimuth angle',
                                      {'name': u'Azimuth Angle',
                                       'pyname': u'azimuth_angle',
                                       'maximum': 360.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'deg'}),
                                     (u'tilt angle',
                                      {'name': u'Tilt Angle',
                                       'pyname': u'tilt_angle',
                                       'default': 90.0,
                                       'maximum': 180.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'deg'}),
                                     (u'starting x coordinate',
                                      {'name': u'Starting X Coordinate',
                                       'pyname': u'starting_x_coordinate',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'starting y coordinate',
                                      {'name': u'Starting Y Coordinate',
                                       'pyname': u'starting_y_coordinate',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'starting z coordinate',
                                      {'name': u'Starting Z Coordinate',
                                       'pyname': u'starting_z_coordinate',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'length',
                                      {'name': u'Length',
                                       'pyname': u'length',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'height',
                                      {'name': u'Height',
                                       'pyname': u'height',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'})]),
              'format': None,
              'group': u'Thermal Zones and Surfaces',
              'min-fields': 0,
              'name': u'Wall:Exterior',
              'pyname': u'WallExterior',
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
        """Corresponds to IDD field `Construction Name` To be matched with a
        construction in this input file.

        Args:
            value (str): value for IDD Field `Construction Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Construction Name"] = value

    @property
    def zone_name(self):
        """Get zone_name.

        Returns:
            str: the value of `zone_name` or None if not set

        """
        return self["Zone Name"]

    @zone_name.setter
    def zone_name(self, value=None):
        """Corresponds to IDD field `Zone Name` Zone the surface is a part of.

        Args:
            value (str): value for IDD Field `Zone Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Zone Name"] = value

    @property
    def azimuth_angle(self):
        """Get azimuth_angle.

        Returns:
            float: the value of `azimuth_angle` or None if not set

        """
        return self["Azimuth Angle"]

    @azimuth_angle.setter
    def azimuth_angle(self, value=None):
        """  Corresponds to IDD field `Azimuth Angle`
        Facing direction of outside of wall (S=180,N=0,E=90,W=270)

        Args:
            value (float): value for IDD Field `Azimuth Angle`
                Units: deg
                value <= 360.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Azimuth Angle"] = value

    @property
    def tilt_angle(self):
        """Get tilt_angle.

        Returns:
            float: the value of `tilt_angle` or None if not set

        """
        return self["Tilt Angle"]

    @tilt_angle.setter
    def tilt_angle(self, value=90.0):
        """Corresponds to IDD field `Tilt Angle` Walls are usually tilted 90
        degrees.

        Args:
            value (float): value for IDD Field `Tilt Angle`
                Units: deg
                Default value: 90.0
                value <= 180.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Tilt Angle"] = value

    @property
    def starting_x_coordinate(self):
        """Get starting_x_coordinate.

        Returns:
            float: the value of `starting_x_coordinate` or None if not set

        """
        return self["Starting X Coordinate"]

    @starting_x_coordinate.setter
    def starting_x_coordinate(self, value=None):
        """Corresponds to IDD field `Starting X Coordinate` Starting (x,y,z)
        coordinate is the Lower Left Corner of the Wall.

        Args:
            value (float): value for IDD Field `Starting X Coordinate`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Starting X Coordinate"] = value

    @property
    def starting_y_coordinate(self):
        """Get starting_y_coordinate.

        Returns:
            float: the value of `starting_y_coordinate` or None if not set

        """
        return self["Starting Y Coordinate"]

    @starting_y_coordinate.setter
    def starting_y_coordinate(self, value=None):
        """Corresponds to IDD field `Starting Y Coordinate`

        Args:
            value (float): value for IDD Field `Starting Y Coordinate`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Starting Y Coordinate"] = value

    @property
    def starting_z_coordinate(self):
        """Get starting_z_coordinate.

        Returns:
            float: the value of `starting_z_coordinate` or None if not set

        """
        return self["Starting Z Coordinate"]

    @starting_z_coordinate.setter
    def starting_z_coordinate(self, value=None):
        """Corresponds to IDD field `Starting Z Coordinate`

        Args:
            value (float): value for IDD Field `Starting Z Coordinate`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Starting Z Coordinate"] = value

    @property
    def length(self):
        """Get length.

        Returns:
            float: the value of `length` or None if not set

        """
        return self["Length"]

    @length.setter
    def length(self, value=None):
        """Corresponds to IDD field `Length`

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
    def height(self):
        """Get height.

        Returns:
            float: the value of `height` or None if not set

        """
        return self["Height"]

    @height.setter
    def height(self, value=None):
        """Corresponds to IDD field `Height`

        Args:
            value (float): value for IDD Field `Height`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Height"] = value




class WallAdiabatic(DataObject):

    """ Corresponds to IDD object `Wall:Adiabatic`
        Allows for simplified entry of interior walls.
    """
    schema = {'extensible-fields': OrderedDict(),
              'fields': OrderedDict([(u'name',
                                      {'name': u'Name',
                                       'pyname': u'name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'alpha'}),
                                     (u'construction name',
                                      {'name': u'Construction Name',
                                       'pyname': u'construction_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'zone name',
                                      {'name': u'Zone Name',
                                       'pyname': u'zone_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'azimuth angle',
                                      {'name': u'Azimuth Angle',
                                       'pyname': u'azimuth_angle',
                                       'maximum': 360.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'deg'}),
                                     (u'tilt angle',
                                      {'name': u'Tilt Angle',
                                       'pyname': u'tilt_angle',
                                       'default': 90.0,
                                       'maximum': 180.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'deg'}),
                                     (u'starting x coordinate',
                                      {'name': u'Starting X Coordinate',
                                       'pyname': u'starting_x_coordinate',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'starting y coordinate',
                                      {'name': u'Starting Y Coordinate',
                                       'pyname': u'starting_y_coordinate',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'starting z coordinate',
                                      {'name': u'Starting Z Coordinate',
                                       'pyname': u'starting_z_coordinate',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'length',
                                      {'name': u'Length',
                                       'pyname': u'length',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'height',
                                      {'name': u'Height',
                                       'pyname': u'height',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'})]),
              'format': None,
              'group': u'Thermal Zones and Surfaces',
              'min-fields': 0,
              'name': u'Wall:Adiabatic',
              'pyname': u'WallAdiabatic',
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
        """Corresponds to IDD field `Construction Name` To be matched with a
        construction in this input file.

        Args:
            value (str): value for IDD Field `Construction Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Construction Name"] = value

    @property
    def zone_name(self):
        """Get zone_name.

        Returns:
            str: the value of `zone_name` or None if not set

        """
        return self["Zone Name"]

    @zone_name.setter
    def zone_name(self, value=None):
        """Corresponds to IDD field `Zone Name` Zone the surface is a part of.

        Args:
            value (str): value for IDD Field `Zone Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Zone Name"] = value

    @property
    def azimuth_angle(self):
        """Get azimuth_angle.

        Returns:
            float: the value of `azimuth_angle` or None if not set

        """
        return self["Azimuth Angle"]

    @azimuth_angle.setter
    def azimuth_angle(self, value=None):
        """  Corresponds to IDD field `Azimuth Angle`
        Facing direction of outside of wall (S=180,N=0,E=90,W=270)

        Args:
            value (float): value for IDD Field `Azimuth Angle`
                Units: deg
                value <= 360.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Azimuth Angle"] = value

    @property
    def tilt_angle(self):
        """Get tilt_angle.

        Returns:
            float: the value of `tilt_angle` or None if not set

        """
        return self["Tilt Angle"]

    @tilt_angle.setter
    def tilt_angle(self, value=90.0):
        """Corresponds to IDD field `Tilt Angle` Walls are usually tilted 90
        degrees.

        Args:
            value (float): value for IDD Field `Tilt Angle`
                Units: deg
                Default value: 90.0
                value <= 180.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Tilt Angle"] = value

    @property
    def starting_x_coordinate(self):
        """Get starting_x_coordinate.

        Returns:
            float: the value of `starting_x_coordinate` or None if not set

        """
        return self["Starting X Coordinate"]

    @starting_x_coordinate.setter
    def starting_x_coordinate(self, value=None):
        """Corresponds to IDD field `Starting X Coordinate` Starting (x,y,z)
        coordinate is the Lower Left Corner of the Wall.

        Args:
            value (float): value for IDD Field `Starting X Coordinate`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Starting X Coordinate"] = value

    @property
    def starting_y_coordinate(self):
        """Get starting_y_coordinate.

        Returns:
            float: the value of `starting_y_coordinate` or None if not set

        """
        return self["Starting Y Coordinate"]

    @starting_y_coordinate.setter
    def starting_y_coordinate(self, value=None):
        """Corresponds to IDD field `Starting Y Coordinate`

        Args:
            value (float): value for IDD Field `Starting Y Coordinate`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Starting Y Coordinate"] = value

    @property
    def starting_z_coordinate(self):
        """Get starting_z_coordinate.

        Returns:
            float: the value of `starting_z_coordinate` or None if not set

        """
        return self["Starting Z Coordinate"]

    @starting_z_coordinate.setter
    def starting_z_coordinate(self, value=None):
        """Corresponds to IDD field `Starting Z Coordinate`

        Args:
            value (float): value for IDD Field `Starting Z Coordinate`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Starting Z Coordinate"] = value

    @property
    def length(self):
        """Get length.

        Returns:
            float: the value of `length` or None if not set

        """
        return self["Length"]

    @length.setter
    def length(self, value=None):
        """Corresponds to IDD field `Length`

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
    def height(self):
        """Get height.

        Returns:
            float: the value of `height` or None if not set

        """
        return self["Height"]

    @height.setter
    def height(self, value=None):
        """Corresponds to IDD field `Height`

        Args:
            value (float): value for IDD Field `Height`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Height"] = value




class WallUnderground(DataObject):

    """ Corresponds to IDD object `Wall:Underground`
        Allows for simplified entry of underground walls.
    """
    schema = {'extensible-fields': OrderedDict(),
              'fields': OrderedDict([(u'name',
                                      {'name': u'Name',
                                       'pyname': u'name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'alpha'}),
                                     (u'construction name',
                                      {'name': u'Construction Name',
                                       'pyname': u'construction_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'zone name',
                                      {'name': u'Zone Name',
                                       'pyname': u'zone_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'azimuth angle',
                                      {'name': u'Azimuth Angle',
                                       'pyname': u'azimuth_angle',
                                       'maximum': 360.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'deg'}),
                                     (u'tilt angle',
                                      {'name': u'Tilt Angle',
                                       'pyname': u'tilt_angle',
                                       'default': 90.0,
                                       'maximum': 180.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'deg'}),
                                     (u'starting x coordinate',
                                      {'name': u'Starting X Coordinate',
                                       'pyname': u'starting_x_coordinate',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'starting y coordinate',
                                      {'name': u'Starting Y Coordinate',
                                       'pyname': u'starting_y_coordinate',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'starting z coordinate',
                                      {'name': u'Starting Z Coordinate',
                                       'pyname': u'starting_z_coordinate',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'length',
                                      {'name': u'Length',
                                       'pyname': u'length',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'height',
                                      {'name': u'Height',
                                       'pyname': u'height',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'})]),
              'format': None,
              'group': u'Thermal Zones and Surfaces',
              'min-fields': 0,
              'name': u'Wall:Underground',
              'pyname': u'WallUnderground',
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
        """  Corresponds to IDD field `Construction Name`
        To be matched with a construction in this input file.
        If the construction is type "Construction:CfactorUndergroundWall",
        then the GroundFCfactorMethod will be used.

        Args:
            value (str): value for IDD Field `Construction Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Construction Name"] = value

    @property
    def zone_name(self):
        """Get zone_name.

        Returns:
            str: the value of `zone_name` or None if not set

        """
        return self["Zone Name"]

    @zone_name.setter
    def zone_name(self, value=None):
        """Corresponds to IDD field `Zone Name` Zone the surface is a part of.

        Args:
            value (str): value for IDD Field `Zone Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Zone Name"] = value

    @property
    def azimuth_angle(self):
        """Get azimuth_angle.

        Returns:
            float: the value of `azimuth_angle` or None if not set

        """
        return self["Azimuth Angle"]

    @azimuth_angle.setter
    def azimuth_angle(self, value=None):
        """  Corresponds to IDD field `Azimuth Angle`
        Facing direction of outside of wall (S=180,N=0,E=90,W=270)

        Args:
            value (float): value for IDD Field `Azimuth Angle`
                Units: deg
                value <= 360.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Azimuth Angle"] = value

    @property
    def tilt_angle(self):
        """Get tilt_angle.

        Returns:
            float: the value of `tilt_angle` or None if not set

        """
        return self["Tilt Angle"]

    @tilt_angle.setter
    def tilt_angle(self, value=90.0):
        """Corresponds to IDD field `Tilt Angle` Walls are usually tilted 90
        degrees.

        Args:
            value (float): value for IDD Field `Tilt Angle`
                Units: deg
                Default value: 90.0
                value <= 180.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Tilt Angle"] = value

    @property
    def starting_x_coordinate(self):
        """Get starting_x_coordinate.

        Returns:
            float: the value of `starting_x_coordinate` or None if not set

        """
        return self["Starting X Coordinate"]

    @starting_x_coordinate.setter
    def starting_x_coordinate(self, value=None):
        """Corresponds to IDD field `Starting X Coordinate` Starting (x,y,z)
        coordinate is the Lower Left Corner of the Wall.

        Args:
            value (float): value for IDD Field `Starting X Coordinate`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Starting X Coordinate"] = value

    @property
    def starting_y_coordinate(self):
        """Get starting_y_coordinate.

        Returns:
            float: the value of `starting_y_coordinate` or None if not set

        """
        return self["Starting Y Coordinate"]

    @starting_y_coordinate.setter
    def starting_y_coordinate(self, value=None):
        """Corresponds to IDD field `Starting Y Coordinate`

        Args:
            value (float): value for IDD Field `Starting Y Coordinate`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Starting Y Coordinate"] = value

    @property
    def starting_z_coordinate(self):
        """Get starting_z_coordinate.

        Returns:
            float: the value of `starting_z_coordinate` or None if not set

        """
        return self["Starting Z Coordinate"]

    @starting_z_coordinate.setter
    def starting_z_coordinate(self, value=None):
        """Corresponds to IDD field `Starting Z Coordinate`

        Args:
            value (float): value for IDD Field `Starting Z Coordinate`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Starting Z Coordinate"] = value

    @property
    def length(self):
        """Get length.

        Returns:
            float: the value of `length` or None if not set

        """
        return self["Length"]

    @length.setter
    def length(self, value=None):
        """Corresponds to IDD field `Length`

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
    def height(self):
        """Get height.

        Returns:
            float: the value of `height` or None if not set

        """
        return self["Height"]

    @height.setter
    def height(self, value=None):
        """Corresponds to IDD field `Height`

        Args:
            value (float): value for IDD Field `Height`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Height"] = value




class WallInterzone(DataObject):

    """ Corresponds to IDD object `Wall:Interzone`
        Allows for simplified entry of interzone walls (walls between zones).
    """
    schema = {'extensible-fields': OrderedDict(),
              'fields': OrderedDict([(u'name',
                                      {'name': u'Name',
                                       'pyname': u'name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'alpha'}),
                                     (u'construction name',
                                      {'name': u'Construction Name',
                                       'pyname': u'construction_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'zone name',
                                      {'name': u'Zone Name',
                                       'pyname': u'zone_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'outside boundary condition object',
                                      {'name': u'Outside Boundary Condition Object',
                                       'pyname': u'outside_boundary_condition_object',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'azimuth angle',
                                      {'name': u'Azimuth Angle',
                                       'pyname': u'azimuth_angle',
                                       'maximum': 360.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'deg'}),
                                     (u'tilt angle',
                                      {'name': u'Tilt Angle',
                                       'pyname': u'tilt_angle',
                                       'default': 90.0,
                                       'maximum': 180.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'deg'}),
                                     (u'starting x coordinate',
                                      {'name': u'Starting X Coordinate',
                                       'pyname': u'starting_x_coordinate',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'starting y coordinate',
                                      {'name': u'Starting Y Coordinate',
                                       'pyname': u'starting_y_coordinate',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'starting z coordinate',
                                      {'name': u'Starting Z Coordinate',
                                       'pyname': u'starting_z_coordinate',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'length',
                                      {'name': u'Length',
                                       'pyname': u'length',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'height',
                                      {'name': u'Height',
                                       'pyname': u'height',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'})]),
              'format': None,
              'group': u'Thermal Zones and Surfaces',
              'min-fields': 0,
              'name': u'Wall:Interzone',
              'pyname': u'WallInterzone',
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
        """Corresponds to IDD field `Construction Name` To be matched with a
        construction in this input file.

        Args:
            value (str): value for IDD Field `Construction Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Construction Name"] = value

    @property
    def zone_name(self):
        """Get zone_name.

        Returns:
            str: the value of `zone_name` or None if not set

        """
        return self["Zone Name"]

    @zone_name.setter
    def zone_name(self, value=None):
        """Corresponds to IDD field `Zone Name` Zone for the inside of the
        surface.

        Args:
            value (str): value for IDD Field `Zone Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Zone Name"] = value

    @property
    def outside_boundary_condition_object(self):
        """Get outside_boundary_condition_object.

        Returns:
            str: the value of `outside_boundary_condition_object` or None if not set

        """
        return self["Outside Boundary Condition Object"]

    @outside_boundary_condition_object.setter
    def outside_boundary_condition_object(self, value=None):
        """Corresponds to IDD field `Outside Boundary Condition Object` Specify
        a surface name in an adjacent zone for known interior walls. Specify a
        zone name of an adjacent zone to automatically generate the interior
        wall in the adjacent zone.

        Args:
            value (str): value for IDD Field `Outside Boundary Condition Object`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Outside Boundary Condition Object"] = value

    @property
    def azimuth_angle(self):
        """Get azimuth_angle.

        Returns:
            float: the value of `azimuth_angle` or None if not set

        """
        return self["Azimuth Angle"]

    @azimuth_angle.setter
    def azimuth_angle(self, value=None):
        """  Corresponds to IDD field `Azimuth Angle`
        Facing direction of outside of wall (S=180,N=0,E=90,W=270)

        Args:
            value (float): value for IDD Field `Azimuth Angle`
                Units: deg
                value <= 360.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Azimuth Angle"] = value

    @property
    def tilt_angle(self):
        """Get tilt_angle.

        Returns:
            float: the value of `tilt_angle` or None if not set

        """
        return self["Tilt Angle"]

    @tilt_angle.setter
    def tilt_angle(self, value=90.0):
        """Corresponds to IDD field `Tilt Angle` Walls are usually tilted 90
        degrees.

        Args:
            value (float): value for IDD Field `Tilt Angle`
                Units: deg
                Default value: 90.0
                value <= 180.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Tilt Angle"] = value

    @property
    def starting_x_coordinate(self):
        """Get starting_x_coordinate.

        Returns:
            float: the value of `starting_x_coordinate` or None if not set

        """
        return self["Starting X Coordinate"]

    @starting_x_coordinate.setter
    def starting_x_coordinate(self, value=None):
        """Corresponds to IDD field `Starting X Coordinate` Starting (x,y,z)
        coordinate is the Lower Left Corner of the Wall.

        Args:
            value (float): value for IDD Field `Starting X Coordinate`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Starting X Coordinate"] = value

    @property
    def starting_y_coordinate(self):
        """Get starting_y_coordinate.

        Returns:
            float: the value of `starting_y_coordinate` or None if not set

        """
        return self["Starting Y Coordinate"]

    @starting_y_coordinate.setter
    def starting_y_coordinate(self, value=None):
        """Corresponds to IDD field `Starting Y Coordinate`

        Args:
            value (float): value for IDD Field `Starting Y Coordinate`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Starting Y Coordinate"] = value

    @property
    def starting_z_coordinate(self):
        """Get starting_z_coordinate.

        Returns:
            float: the value of `starting_z_coordinate` or None if not set

        """
        return self["Starting Z Coordinate"]

    @starting_z_coordinate.setter
    def starting_z_coordinate(self, value=None):
        """Corresponds to IDD field `Starting Z Coordinate`

        Args:
            value (float): value for IDD Field `Starting Z Coordinate`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Starting Z Coordinate"] = value

    @property
    def length(self):
        """Get length.

        Returns:
            float: the value of `length` or None if not set

        """
        return self["Length"]

    @length.setter
    def length(self, value=None):
        """Corresponds to IDD field `Length`

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
    def height(self):
        """Get height.

        Returns:
            float: the value of `height` or None if not set

        """
        return self["Height"]

    @height.setter
    def height(self, value=None):
        """Corresponds to IDD field `Height`

        Args:
            value (float): value for IDD Field `Height`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Height"] = value




class Roof(DataObject):

    """Corresponds to IDD object `Roof` Allows for simplified entry of roofs
    (exterior).

    View Factor to Ground is automatically calculated.

    """
    schema = {'extensible-fields': OrderedDict(),
              'fields': OrderedDict([(u'name',
                                      {'name': u'Name',
                                       'pyname': u'name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'alpha'}),
                                     (u'construction name',
                                      {'name': u'Construction Name',
                                       'pyname': u'construction_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'zone name',
                                      {'name': u'Zone Name',
                                       'pyname': u'zone_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'azimuth angle',
                                      {'name': u'Azimuth Angle',
                                       'pyname': u'azimuth_angle',
                                       'maximum': 360.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'deg'}),
                                     (u'tilt angle',
                                      {'name': u'Tilt Angle',
                                       'pyname': u'tilt_angle',
                                       'default': 0.0,
                                       'maximum': 180.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'deg'}),
                                     (u'starting x coordinate',
                                      {'name': u'Starting X Coordinate',
                                       'pyname': u'starting_x_coordinate',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'starting y coordinate',
                                      {'name': u'Starting Y Coordinate',
                                       'pyname': u'starting_y_coordinate',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'starting z coordinate',
                                      {'name': u'Starting Z Coordinate',
                                       'pyname': u'starting_z_coordinate',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'length',
                                      {'name': u'Length',
                                       'pyname': u'length',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'width',
                                      {'name': u'Width',
                                       'pyname': u'width',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'})]),
              'format': None,
              'group': u'Thermal Zones and Surfaces',
              'min-fields': 0,
              'name': u'Roof',
              'pyname': u'Roof',
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
        """Corresponds to IDD field `Construction Name` To be matched with a
        construction in this input file.

        Args:
            value (str): value for IDD Field `Construction Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Construction Name"] = value

    @property
    def zone_name(self):
        """Get zone_name.

        Returns:
            str: the value of `zone_name` or None if not set

        """
        return self["Zone Name"]

    @zone_name.setter
    def zone_name(self, value=None):
        """Corresponds to IDD field `Zone Name` Zone the surface is a part of.

        Args:
            value (str): value for IDD Field `Zone Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Zone Name"] = value

    @property
    def azimuth_angle(self):
        """Get azimuth_angle.

        Returns:
            float: the value of `azimuth_angle` or None if not set

        """
        return self["Azimuth Angle"]

    @azimuth_angle.setter
    def azimuth_angle(self, value=None):
        """Corresponds to IDD field `Azimuth Angle` Facing direction of outside
        of Roof.

        Args:
            value (float): value for IDD Field `Azimuth Angle`
                Units: deg
                value <= 360.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Azimuth Angle"] = value

    @property
    def tilt_angle(self):
        """Get tilt_angle.

        Returns:
            float: the value of `tilt_angle` or None if not set

        """
        return self["Tilt Angle"]

    @tilt_angle.setter
    def tilt_angle(self, value=None):
        """Corresponds to IDD field `Tilt Angle` Flat Roofs are tilted 0
        degrees.

        Args:
            value (float): value for IDD Field `Tilt Angle`
                Units: deg
                value <= 180.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Tilt Angle"] = value

    @property
    def starting_x_coordinate(self):
        """Get starting_x_coordinate.

        Returns:
            float: the value of `starting_x_coordinate` or None if not set

        """
        return self["Starting X Coordinate"]

    @starting_x_coordinate.setter
    def starting_x_coordinate(self, value=None):
        """Corresponds to IDD field `Starting X Coordinate` If not Flat,
        Starting coordinate is the Lower Left Corner of the Roof.

        Args:
            value (float): value for IDD Field `Starting X Coordinate`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Starting X Coordinate"] = value

    @property
    def starting_y_coordinate(self):
        """Get starting_y_coordinate.

        Returns:
            float: the value of `starting_y_coordinate` or None if not set

        """
        return self["Starting Y Coordinate"]

    @starting_y_coordinate.setter
    def starting_y_coordinate(self, value=None):
        """Corresponds to IDD field `Starting Y Coordinate`

        Args:
            value (float): value for IDD Field `Starting Y Coordinate`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Starting Y Coordinate"] = value

    @property
    def starting_z_coordinate(self):
        """Get starting_z_coordinate.

        Returns:
            float: the value of `starting_z_coordinate` or None if not set

        """
        return self["Starting Z Coordinate"]

    @starting_z_coordinate.setter
    def starting_z_coordinate(self, value=None):
        """Corresponds to IDD field `Starting Z Coordinate`

        Args:
            value (float): value for IDD Field `Starting Z Coordinate`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Starting Z Coordinate"] = value

    @property
    def length(self):
        """Get length.

        Returns:
            float: the value of `length` or None if not set

        """
        return self["Length"]

    @length.setter
    def length(self, value=None):
        """Corresponds to IDD field `Length` Along X Axis.

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
    def width(self):
        """Get width.

        Returns:
            float: the value of `width` or None if not set

        """
        return self["Width"]

    @width.setter
    def width(self, value=None):
        """Corresponds to IDD field `Width` Along Y Axis.

        Args:
            value (float): value for IDD Field `Width`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Width"] = value




class CeilingAdiabatic(DataObject):

    """ Corresponds to IDD object `Ceiling:Adiabatic`
        Allows for simplified entry of interior ceilings.
    """
    schema = {'extensible-fields': OrderedDict(),
              'fields': OrderedDict([(u'name',
                                      {'name': u'Name',
                                       'pyname': u'name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'alpha'}),
                                     (u'construction name',
                                      {'name': u'Construction Name',
                                       'pyname': u'construction_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'zone name',
                                      {'name': u'Zone Name',
                                       'pyname': u'zone_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'azimuth angle',
                                      {'name': u'Azimuth Angle',
                                       'pyname': u'azimuth_angle',
                                       'maximum': 360.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'deg'}),
                                     (u'tilt angle',
                                      {'name': u'Tilt Angle',
                                       'pyname': u'tilt_angle',
                                       'default': 0.0,
                                       'maximum': 180.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'deg'}),
                                     (u'starting x coordinate',
                                      {'name': u'Starting X Coordinate',
                                       'pyname': u'starting_x_coordinate',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'starting y coordinate',
                                      {'name': u'Starting Y Coordinate',
                                       'pyname': u'starting_y_coordinate',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'starting z coordinate',
                                      {'name': u'Starting Z Coordinate',
                                       'pyname': u'starting_z_coordinate',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'length',
                                      {'name': u'Length',
                                       'pyname': u'length',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'width',
                                      {'name': u'Width',
                                       'pyname': u'width',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'})]),
              'format': None,
              'group': u'Thermal Zones and Surfaces',
              'min-fields': 0,
              'name': u'Ceiling:Adiabatic',
              'pyname': u'CeilingAdiabatic',
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
        """Corresponds to IDD field `Construction Name` To be matched with a
        construction in this input file.

        Args:
            value (str): value for IDD Field `Construction Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Construction Name"] = value

    @property
    def zone_name(self):
        """Get zone_name.

        Returns:
            str: the value of `zone_name` or None if not set

        """
        return self["Zone Name"]

    @zone_name.setter
    def zone_name(self, value=None):
        """Corresponds to IDD field `Zone Name` Zone the surface is a part of.

        Args:
            value (str): value for IDD Field `Zone Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Zone Name"] = value

    @property
    def azimuth_angle(self):
        """Get azimuth_angle.

        Returns:
            float: the value of `azimuth_angle` or None if not set

        """
        return self["Azimuth Angle"]

    @azimuth_angle.setter
    def azimuth_angle(self, value=None):
        """Corresponds to IDD field `Azimuth Angle` Facing direction of outside
        of Ceiling.

        Args:
            value (float): value for IDD Field `Azimuth Angle`
                Units: deg
                value <= 360.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Azimuth Angle"] = value

    @property
    def tilt_angle(self):
        """Get tilt_angle.

        Returns:
            float: the value of `tilt_angle` or None if not set

        """
        return self["Tilt Angle"]

    @tilt_angle.setter
    def tilt_angle(self, value=None):
        """Corresponds to IDD field `Tilt Angle` Ceilings are usually tilted 0
        degrees.

        Args:
            value (float): value for IDD Field `Tilt Angle`
                Units: deg
                value <= 180.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Tilt Angle"] = value

    @property
    def starting_x_coordinate(self):
        """Get starting_x_coordinate.

        Returns:
            float: the value of `starting_x_coordinate` or None if not set

        """
        return self["Starting X Coordinate"]

    @starting_x_coordinate.setter
    def starting_x_coordinate(self, value=None):
        """Corresponds to IDD field `Starting X Coordinate` If not Flat,
        Starting coordinate is the Lower Left Corner of the Ceiling.

        Args:
            value (float): value for IDD Field `Starting X Coordinate`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Starting X Coordinate"] = value

    @property
    def starting_y_coordinate(self):
        """Get starting_y_coordinate.

        Returns:
            float: the value of `starting_y_coordinate` or None if not set

        """
        return self["Starting Y Coordinate"]

    @starting_y_coordinate.setter
    def starting_y_coordinate(self, value=None):
        """Corresponds to IDD field `Starting Y Coordinate`

        Args:
            value (float): value for IDD Field `Starting Y Coordinate`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Starting Y Coordinate"] = value

    @property
    def starting_z_coordinate(self):
        """Get starting_z_coordinate.

        Returns:
            float: the value of `starting_z_coordinate` or None if not set

        """
        return self["Starting Z Coordinate"]

    @starting_z_coordinate.setter
    def starting_z_coordinate(self, value=None):
        """Corresponds to IDD field `Starting Z Coordinate`

        Args:
            value (float): value for IDD Field `Starting Z Coordinate`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Starting Z Coordinate"] = value

    @property
    def length(self):
        """Get length.

        Returns:
            float: the value of `length` or None if not set

        """
        return self["Length"]

    @length.setter
    def length(self, value=None):
        """Corresponds to IDD field `Length` Along X Axis.

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
    def width(self):
        """Get width.

        Returns:
            float: the value of `width` or None if not set

        """
        return self["Width"]

    @width.setter
    def width(self, value=None):
        """Corresponds to IDD field `Width` Along Y Axis.

        Args:
            value (float): value for IDD Field `Width`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Width"] = value




class CeilingInterzone(DataObject):

    """ Corresponds to IDD object `Ceiling:Interzone`
        Allows for simplified entry of ceilings using adjacent zone
        (interzone) heat transfer - adjacent surface should be a floor
    """
    schema = {'extensible-fields': OrderedDict(),
              'fields': OrderedDict([(u'name',
                                      {'name': u'Name',
                                       'pyname': u'name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'alpha'}),
                                     (u'construction name',
                                      {'name': u'Construction Name',
                                       'pyname': u'construction_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'zone name',
                                      {'name': u'Zone Name',
                                       'pyname': u'zone_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'outside boundary condition object',
                                      {'name': u'Outside Boundary Condition Object',
                                       'pyname': u'outside_boundary_condition_object',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'azimuth angle',
                                      {'name': u'Azimuth Angle',
                                       'pyname': u'azimuth_angle',
                                       'maximum': 360.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'deg'}),
                                     (u'tilt angle',
                                      {'name': u'Tilt Angle',
                                       'pyname': u'tilt_angle',
                                       'default': 0.0,
                                       'maximum': 180.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'deg'}),
                                     (u'starting x coordinate',
                                      {'name': u'Starting X Coordinate',
                                       'pyname': u'starting_x_coordinate',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'starting y coordinate',
                                      {'name': u'Starting Y Coordinate',
                                       'pyname': u'starting_y_coordinate',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'starting z coordinate',
                                      {'name': u'Starting Z Coordinate',
                                       'pyname': u'starting_z_coordinate',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'length',
                                      {'name': u'Length',
                                       'pyname': u'length',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'width',
                                      {'name': u'Width',
                                       'pyname': u'width',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'})]),
              'format': None,
              'group': u'Thermal Zones and Surfaces',
              'min-fields': 0,
              'name': u'Ceiling:Interzone',
              'pyname': u'CeilingInterzone',
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
        """Corresponds to IDD field `Construction Name` To be matched with a
        construction in this input file.

        Args:
            value (str): value for IDD Field `Construction Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Construction Name"] = value

    @property
    def zone_name(self):
        """Get zone_name.

        Returns:
            str: the value of `zone_name` or None if not set

        """
        return self["Zone Name"]

    @zone_name.setter
    def zone_name(self, value=None):
        """Corresponds to IDD field `Zone Name` Zone for the inside of the
        surface.

        Args:
            value (str): value for IDD Field `Zone Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Zone Name"] = value

    @property
    def outside_boundary_condition_object(self):
        """Get outside_boundary_condition_object.

        Returns:
            str: the value of `outside_boundary_condition_object` or None if not set

        """
        return self["Outside Boundary Condition Object"]

    @outside_boundary_condition_object.setter
    def outside_boundary_condition_object(self, value=None):
        """Corresponds to IDD field `Outside Boundary Condition Object` Specify
        a surface name in an adjacent zone for known interior floors Specify a
        zone name of an adjacent zone to automatically generate the interior
        floor in the adjacent zone.

        Args:
            value (str): value for IDD Field `Outside Boundary Condition Object`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Outside Boundary Condition Object"] = value

    @property
    def azimuth_angle(self):
        """Get azimuth_angle.

        Returns:
            float: the value of `azimuth_angle` or None if not set

        """
        return self["Azimuth Angle"]

    @azimuth_angle.setter
    def azimuth_angle(self, value=None):
        """  Corresponds to IDD field `Azimuth Angle`
        Facing direction of outside of wall (S=180,N=0,E=90,W=270)

        Args:
            value (float): value for IDD Field `Azimuth Angle`
                Units: deg
                value <= 360.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Azimuth Angle"] = value

    @property
    def tilt_angle(self):
        """Get tilt_angle.

        Returns:
            float: the value of `tilt_angle` or None if not set

        """
        return self["Tilt Angle"]

    @tilt_angle.setter
    def tilt_angle(self, value=None):
        """Corresponds to IDD field `Tilt Angle` Ceilings are usually tilted 0
        degrees.

        Args:
            value (float): value for IDD Field `Tilt Angle`
                Units: deg
                value <= 180.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Tilt Angle"] = value

    @property
    def starting_x_coordinate(self):
        """Get starting_x_coordinate.

        Returns:
            float: the value of `starting_x_coordinate` or None if not set

        """
        return self["Starting X Coordinate"]

    @starting_x_coordinate.setter
    def starting_x_coordinate(self, value=None):
        """Corresponds to IDD field `Starting X Coordinate` If not Flat, should
        be Lower Left Corner (from outside)

        Args:
            value (float): value for IDD Field `Starting X Coordinate`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Starting X Coordinate"] = value

    @property
    def starting_y_coordinate(self):
        """Get starting_y_coordinate.

        Returns:
            float: the value of `starting_y_coordinate` or None if not set

        """
        return self["Starting Y Coordinate"]

    @starting_y_coordinate.setter
    def starting_y_coordinate(self, value=None):
        """Corresponds to IDD field `Starting Y Coordinate`

        Args:
            value (float): value for IDD Field `Starting Y Coordinate`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Starting Y Coordinate"] = value

    @property
    def starting_z_coordinate(self):
        """Get starting_z_coordinate.

        Returns:
            float: the value of `starting_z_coordinate` or None if not set

        """
        return self["Starting Z Coordinate"]

    @starting_z_coordinate.setter
    def starting_z_coordinate(self, value=None):
        """Corresponds to IDD field `Starting Z Coordinate`

        Args:
            value (float): value for IDD Field `Starting Z Coordinate`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Starting Z Coordinate"] = value

    @property
    def length(self):
        """Get length.

        Returns:
            float: the value of `length` or None if not set

        """
        return self["Length"]

    @length.setter
    def length(self, value=None):
        """Corresponds to IDD field `Length` Along X Axis.

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
    def width(self):
        """Get width.

        Returns:
            float: the value of `width` or None if not set

        """
        return self["Width"]

    @width.setter
    def width(self, value=None):
        """Corresponds to IDD field `Width` Along Y Axis.

        Args:
            value (float): value for IDD Field `Width`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Width"] = value




class FloorGroundContact(DataObject):

    """ Corresponds to IDD object `Floor:GroundContact`
        Allows for simplified entry of exterior floors with ground contact.
        View Factors to Ground is automatically calculated.
    """
    schema = {'extensible-fields': OrderedDict(),
              'fields': OrderedDict([(u'name',
                                      {'name': u'Name',
                                       'pyname': u'name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'alpha'}),
                                     (u'construction name',
                                      {'name': u'Construction Name',
                                       'pyname': u'construction_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'zone name',
                                      {'name': u'Zone Name',
                                       'pyname': u'zone_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'azimuth angle',
                                      {'name': u'Azimuth Angle',
                                       'pyname': u'azimuth_angle',
                                       'maximum': 360.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'deg'}),
                                     (u'tilt angle',
                                      {'name': u'Tilt Angle',
                                       'pyname': u'tilt_angle',
                                       'default': 180.0,
                                       'maximum': 180.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'deg'}),
                                     (u'starting x coordinate',
                                      {'name': u'Starting X Coordinate',
                                       'pyname': u'starting_x_coordinate',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'starting y coordinate',
                                      {'name': u'Starting Y Coordinate',
                                       'pyname': u'starting_y_coordinate',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'starting z coordinate',
                                      {'name': u'Starting Z Coordinate',
                                       'pyname': u'starting_z_coordinate',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'length',
                                      {'name': u'Length',
                                       'pyname': u'length',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'width',
                                      {'name': u'Width',
                                       'pyname': u'width',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'})]),
              'format': None,
              'group': u'Thermal Zones and Surfaces',
              'min-fields': 0,
              'name': u'Floor:GroundContact',
              'pyname': u'FloorGroundContact',
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
        """  Corresponds to IDD field `Construction Name`
        To be matched with a construction in this input file
        If the construction is type "Construction:FfactorGroundFloor",
        then the GroundFCfactorMethod will be used.

        Args:
            value (str): value for IDD Field `Construction Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Construction Name"] = value

    @property
    def zone_name(self):
        """Get zone_name.

        Returns:
            str: the value of `zone_name` or None if not set

        """
        return self["Zone Name"]

    @zone_name.setter
    def zone_name(self, value=None):
        """Corresponds to IDD field `Zone Name` Zone the surface is a part of.

        Args:
            value (str): value for IDD Field `Zone Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Zone Name"] = value

    @property
    def azimuth_angle(self):
        """Get azimuth_angle.

        Returns:
            float: the value of `azimuth_angle` or None if not set

        """
        return self["Azimuth Angle"]

    @azimuth_angle.setter
    def azimuth_angle(self, value=None):
        """Corresponds to IDD field `Azimuth Angle`

        Args:
            value (float): value for IDD Field `Azimuth Angle`
                Units: deg
                value <= 360.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Azimuth Angle"] = value

    @property
    def tilt_angle(self):
        """Get tilt_angle.

        Returns:
            float: the value of `tilt_angle` or None if not set

        """
        return self["Tilt Angle"]

    @tilt_angle.setter
    def tilt_angle(self, value=180.0):
        """Corresponds to IDD field `Tilt Angle` Floors are usually tilted 180
        degrees.

        Args:
            value (float): value for IDD Field `Tilt Angle`
                Units: deg
                Default value: 180.0
                value <= 180.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Tilt Angle"] = value

    @property
    def starting_x_coordinate(self):
        """Get starting_x_coordinate.

        Returns:
            float: the value of `starting_x_coordinate` or None if not set

        """
        return self["Starting X Coordinate"]

    @starting_x_coordinate.setter
    def starting_x_coordinate(self, value=None):
        """Corresponds to IDD field `Starting X Coordinate` if not flat, should
        be lower left corner (from outside)

        Args:
            value (float): value for IDD Field `Starting X Coordinate`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Starting X Coordinate"] = value

    @property
    def starting_y_coordinate(self):
        """Get starting_y_coordinate.

        Returns:
            float: the value of `starting_y_coordinate` or None if not set

        """
        return self["Starting Y Coordinate"]

    @starting_y_coordinate.setter
    def starting_y_coordinate(self, value=None):
        """Corresponds to IDD field `Starting Y Coordinate`

        Args:
            value (float): value for IDD Field `Starting Y Coordinate`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Starting Y Coordinate"] = value

    @property
    def starting_z_coordinate(self):
        """Get starting_z_coordinate.

        Returns:
            float: the value of `starting_z_coordinate` or None if not set

        """
        return self["Starting Z Coordinate"]

    @starting_z_coordinate.setter
    def starting_z_coordinate(self, value=None):
        """Corresponds to IDD field `Starting Z Coordinate`

        Args:
            value (float): value for IDD Field `Starting Z Coordinate`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Starting Z Coordinate"] = value

    @property
    def length(self):
        """Get length.

        Returns:
            float: the value of `length` or None if not set

        """
        return self["Length"]

    @length.setter
    def length(self, value=None):
        """Corresponds to IDD field `Length` Along X Axis.

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
    def width(self):
        """Get width.

        Returns:
            float: the value of `width` or None if not set

        """
        return self["Width"]

    @width.setter
    def width(self, value=None):
        """Corresponds to IDD field `Width` Along Y Axis.

        Args:
            value (float): value for IDD Field `Width`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Width"] = value




class FloorAdiabatic(DataObject):

    """ Corresponds to IDD object `Floor:Adiabatic`
        Allows for simplified entry of exterior floors
        ignoring ground contact or interior floors.
        View Factor to Ground is automatically calculated.
    """
    schema = {'extensible-fields': OrderedDict(),
              'fields': OrderedDict([(u'name',
                                      {'name': u'Name',
                                       'pyname': u'name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'alpha'}),
                                     (u'construction name',
                                      {'name': u'Construction Name',
                                       'pyname': u'construction_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'zone name',
                                      {'name': u'Zone Name',
                                       'pyname': u'zone_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'azimuth angle',
                                      {'name': u'Azimuth Angle',
                                       'pyname': u'azimuth_angle',
                                       'maximum': 360.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'deg'}),
                                     (u'tilt angle',
                                      {'name': u'Tilt Angle',
                                       'pyname': u'tilt_angle',
                                       'default': 180.0,
                                       'maximum': 180.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'deg'}),
                                     (u'starting x coordinate',
                                      {'name': u'Starting X Coordinate',
                                       'pyname': u'starting_x_coordinate',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'starting y coordinate',
                                      {'name': u'Starting Y Coordinate',
                                       'pyname': u'starting_y_coordinate',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'starting z coordinate',
                                      {'name': u'Starting Z Coordinate',
                                       'pyname': u'starting_z_coordinate',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'length',
                                      {'name': u'Length',
                                       'pyname': u'length',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'width',
                                      {'name': u'Width',
                                       'pyname': u'width',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'})]),
              'format': None,
              'group': u'Thermal Zones and Surfaces',
              'min-fields': 0,
              'name': u'Floor:Adiabatic',
              'pyname': u'FloorAdiabatic',
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
        """Corresponds to IDD field `Construction Name` To be matched with a
        construction in this input file.

        Args:
            value (str): value for IDD Field `Construction Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Construction Name"] = value

    @property
    def zone_name(self):
        """Get zone_name.

        Returns:
            str: the value of `zone_name` or None if not set

        """
        return self["Zone Name"]

    @zone_name.setter
    def zone_name(self, value=None):
        """Corresponds to IDD field `Zone Name` Zone the surface is a part of.

        Args:
            value (str): value for IDD Field `Zone Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Zone Name"] = value

    @property
    def azimuth_angle(self):
        """Get azimuth_angle.

        Returns:
            float: the value of `azimuth_angle` or None if not set

        """
        return self["Azimuth Angle"]

    @azimuth_angle.setter
    def azimuth_angle(self, value=None):
        """Corresponds to IDD field `Azimuth Angle`

        Args:
            value (float): value for IDD Field `Azimuth Angle`
                Units: deg
                value <= 360.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Azimuth Angle"] = value

    @property
    def tilt_angle(self):
        """Get tilt_angle.

        Returns:
            float: the value of `tilt_angle` or None if not set

        """
        return self["Tilt Angle"]

    @tilt_angle.setter
    def tilt_angle(self, value=180.0):
        """Corresponds to IDD field `Tilt Angle` Floors are usually tilted 180
        degrees.

        Args:
            value (float): value for IDD Field `Tilt Angle`
                Units: deg
                Default value: 180.0
                value <= 180.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Tilt Angle"] = value

    @property
    def starting_x_coordinate(self):
        """Get starting_x_coordinate.

        Returns:
            float: the value of `starting_x_coordinate` or None if not set

        """
        return self["Starting X Coordinate"]

    @starting_x_coordinate.setter
    def starting_x_coordinate(self, value=None):
        """Corresponds to IDD field `Starting X Coordinate` if not flat, should
        be lower left corner (from outside)

        Args:
            value (float): value for IDD Field `Starting X Coordinate`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Starting X Coordinate"] = value

    @property
    def starting_y_coordinate(self):
        """Get starting_y_coordinate.

        Returns:
            float: the value of `starting_y_coordinate` or None if not set

        """
        return self["Starting Y Coordinate"]

    @starting_y_coordinate.setter
    def starting_y_coordinate(self, value=None):
        """Corresponds to IDD field `Starting Y Coordinate`

        Args:
            value (float): value for IDD Field `Starting Y Coordinate`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Starting Y Coordinate"] = value

    @property
    def starting_z_coordinate(self):
        """Get starting_z_coordinate.

        Returns:
            float: the value of `starting_z_coordinate` or None if not set

        """
        return self["Starting Z Coordinate"]

    @starting_z_coordinate.setter
    def starting_z_coordinate(self, value=None):
        """Corresponds to IDD field `Starting Z Coordinate`

        Args:
            value (float): value for IDD Field `Starting Z Coordinate`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Starting Z Coordinate"] = value

    @property
    def length(self):
        """Get length.

        Returns:
            float: the value of `length` or None if not set

        """
        return self["Length"]

    @length.setter
    def length(self, value=None):
        """Corresponds to IDD field `Length` Along X Axis.

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
    def width(self):
        """Get width.

        Returns:
            float: the value of `width` or None if not set

        """
        return self["Width"]

    @width.setter
    def width(self, value=None):
        """Corresponds to IDD field `Width` Along Y Axis.

        Args:
            value (float): value for IDD Field `Width`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Width"] = value




class FloorInterzone(DataObject):

    """ Corresponds to IDD object `Floor:Interzone`
        Allows for simplified entry of floors using adjacent zone
        (interzone) heat transfer - adjacent surface should be a ceiling.
    """
    schema = {'extensible-fields': OrderedDict(),
              'fields': OrderedDict([(u'name',
                                      {'name': u'Name',
                                       'pyname': u'name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'alpha'}),
                                     (u'construction name',
                                      {'name': u'Construction Name',
                                       'pyname': u'construction_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'zone name',
                                      {'name': u'Zone Name',
                                       'pyname': u'zone_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'outside boundary condition object',
                                      {'name': u'Outside Boundary Condition Object',
                                       'pyname': u'outside_boundary_condition_object',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'azimuth angle',
                                      {'name': u'Azimuth Angle',
                                       'pyname': u'azimuth_angle',
                                       'maximum': 360.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'deg'}),
                                     (u'tilt angle',
                                      {'name': u'Tilt Angle',
                                       'pyname': u'tilt_angle',
                                       'default': 180.0,
                                       'maximum': 180.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'deg'}),
                                     (u'starting x coordinate',
                                      {'name': u'Starting X Coordinate',
                                       'pyname': u'starting_x_coordinate',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'starting y coordinate',
                                      {'name': u'Starting Y Coordinate',
                                       'pyname': u'starting_y_coordinate',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'starting z coordinate',
                                      {'name': u'Starting Z Coordinate',
                                       'pyname': u'starting_z_coordinate',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'length',
                                      {'name': u'Length',
                                       'pyname': u'length',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'width',
                                      {'name': u'Width',
                                       'pyname': u'width',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'})]),
              'format': None,
              'group': u'Thermal Zones and Surfaces',
              'min-fields': 0,
              'name': u'Floor:Interzone',
              'pyname': u'FloorInterzone',
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
        """Corresponds to IDD field `Construction Name` To be matched with a
        construction in this input file.

        Args:
            value (str): value for IDD Field `Construction Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Construction Name"] = value

    @property
    def zone_name(self):
        """Get zone_name.

        Returns:
            str: the value of `zone_name` or None if not set

        """
        return self["Zone Name"]

    @zone_name.setter
    def zone_name(self, value=None):
        """Corresponds to IDD field `Zone Name` Zone for the inside of the
        surface.

        Args:
            value (str): value for IDD Field `Zone Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Zone Name"] = value

    @property
    def outside_boundary_condition_object(self):
        """Get outside_boundary_condition_object.

        Returns:
            str: the value of `outside_boundary_condition_object` or None if not set

        """
        return self["Outside Boundary Condition Object"]

    @outside_boundary_condition_object.setter
    def outside_boundary_condition_object(self, value=None):
        """Corresponds to IDD field `Outside Boundary Condition Object` Specify
        a surface name in an adjacent zone for known interior ceilings. Specify
        a zone name of an adjacent zone to automatically generate the interior
        ceiling in the adjacent zone.

        Args:
            value (str): value for IDD Field `Outside Boundary Condition Object`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Outside Boundary Condition Object"] = value

    @property
    def azimuth_angle(self):
        """Get azimuth_angle.

        Returns:
            float: the value of `azimuth_angle` or None if not set

        """
        return self["Azimuth Angle"]

    @azimuth_angle.setter
    def azimuth_angle(self, value=None):
        """Corresponds to IDD field `Azimuth Angle`

        Args:
            value (float): value for IDD Field `Azimuth Angle`
                Units: deg
                value <= 360.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Azimuth Angle"] = value

    @property
    def tilt_angle(self):
        """Get tilt_angle.

        Returns:
            float: the value of `tilt_angle` or None if not set

        """
        return self["Tilt Angle"]

    @tilt_angle.setter
    def tilt_angle(self, value=180.0):
        """Corresponds to IDD field `Tilt Angle` Floors are usually tilted 180
        degrees.

        Args:
            value (float): value for IDD Field `Tilt Angle`
                Units: deg
                Default value: 180.0
                value <= 180.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Tilt Angle"] = value

    @property
    def starting_x_coordinate(self):
        """Get starting_x_coordinate.

        Returns:
            float: the value of `starting_x_coordinate` or None if not set

        """
        return self["Starting X Coordinate"]

    @starting_x_coordinate.setter
    def starting_x_coordinate(self, value=None):
        """Corresponds to IDD field `Starting X Coordinate` If not Flat, should
        be Lower Left Corner (from outside)

        Args:
            value (float): value for IDD Field `Starting X Coordinate`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Starting X Coordinate"] = value

    @property
    def starting_y_coordinate(self):
        """Get starting_y_coordinate.

        Returns:
            float: the value of `starting_y_coordinate` or None if not set

        """
        return self["Starting Y Coordinate"]

    @starting_y_coordinate.setter
    def starting_y_coordinate(self, value=None):
        """Corresponds to IDD field `Starting Y Coordinate`

        Args:
            value (float): value for IDD Field `Starting Y Coordinate`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Starting Y Coordinate"] = value

    @property
    def starting_z_coordinate(self):
        """Get starting_z_coordinate.

        Returns:
            float: the value of `starting_z_coordinate` or None if not set

        """
        return self["Starting Z Coordinate"]

    @starting_z_coordinate.setter
    def starting_z_coordinate(self, value=None):
        """Corresponds to IDD field `Starting Z Coordinate`

        Args:
            value (float): value for IDD Field `Starting Z Coordinate`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Starting Z Coordinate"] = value

    @property
    def length(self):
        """Get length.

        Returns:
            float: the value of `length` or None if not set

        """
        return self["Length"]

    @length.setter
    def length(self, value=None):
        """Corresponds to IDD field `Length` Along X Axis.

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
    def width(self):
        """Get width.

        Returns:
            float: the value of `width` or None if not set

        """
        return self["Width"]

    @width.setter
    def width(self, value=None):
        """Corresponds to IDD field `Width` Along Y Axis.

        Args:
            value (float): value for IDD Field `Width`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Width"] = value




class FenestrationSurfaceDetailed(DataObject):

    """ Corresponds to IDD object `FenestrationSurface:Detailed`
        Allows for detailed entry of subsurfaces
        (windows, doors, glass doors, tubular daylighting devices).
    """
    schema = {'extensible-fields': OrderedDict(),
              'fields': OrderedDict([(u'name',
                                      {'name': u'Name',
                                       'pyname': u'name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'alpha'}),
                                     (u'surface type',
                                      {'name': u'Surface Type',
                                       'pyname': u'surface_type',
                                       'required-field': True,
                                       'autosizable': False,
                                       'accepted-values': [u'Window',
                                                           u'Door',
                                                           u'GlassDoor',
                                                           u'TubularDaylightDome',
                                                           u'TubularDaylightDiffuser'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'construction name',
                                      {'name': u'Construction Name',
                                       'pyname': u'construction_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'building surface name',
                                      {'name': u'Building Surface Name',
                                       'pyname': u'building_surface_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'outside boundary condition object',
                                      {'name': u'Outside Boundary Condition Object',
                                       'pyname': u'outside_boundary_condition_object',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'view factor to ground',
                                      {'name': u'View Factor to Ground',
                                       'pyname': u'view_factor_to_ground',
                                       'default': 'autocalculate',
                                       'maximum': 1.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': True,
                                       'type': u'real'}),
                                     (u'shading control name',
                                      {'name': u'Shading Control Name',
                                       'pyname': u'shading_control_name',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'frame and divider name',
                                      {'name': u'Frame and Divider Name',
                                       'pyname': u'frame_and_divider_name',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'multiplier',
                                      {'name': u'Multiplier',
                                       'pyname': u'multiplier',
                                       'default': 1.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 1.0,
                                       'autocalculatable': False,
                                       'type': 'real'}),
                                     (u'number of vertices',
                                      {'name': u'Number of Vertices',
                                       'pyname': u'number_of_vertices',
                                       'default': 'autocalculate',
                                       'maximum': 4.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 3.0,
                                       'autocalculatable': True,
                                       'type': 'real'}),
                                     (u'vertex 1 x-coordinate',
                                      {'name': u'Vertex 1 X-coordinate',
                                       'pyname': u'vertex_1_xcoordinate',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'm'}),
                                     (u'vertex 1 y-coordinate',
                                      {'name': u'Vertex 1 Y-coordinate',
                                       'pyname': u'vertex_1_ycoordinate',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'm'}),
                                     (u'vertex 1 z-coordinate',
                                      {'name': u'Vertex 1 Z-coordinate',
                                       'pyname': u'vertex_1_zcoordinate',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'm'}),
                                     (u'vertex 2 x-coordinate',
                                      {'name': u'Vertex 2 X-coordinate',
                                       'pyname': u'vertex_2_xcoordinate',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'm'}),
                                     (u'vertex 2 y-coordinate',
                                      {'name': u'Vertex 2 Y-coordinate',
                                       'pyname': u'vertex_2_ycoordinate',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'm'}),
                                     (u'vertex 2 z-coordinate',
                                      {'name': u'Vertex 2 Z-coordinate',
                                       'pyname': u'vertex_2_zcoordinate',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'm'}),
                                     (u'vertex 3 x-coordinate',
                                      {'name': u'Vertex 3 X-coordinate',
                                       'pyname': u'vertex_3_xcoordinate',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'm'}),
                                     (u'vertex 3 y-coordinate',
                                      {'name': u'Vertex 3 Y-coordinate',
                                       'pyname': u'vertex_3_ycoordinate',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'm'}),
                                     (u'vertex 3 z-coordinate',
                                      {'name': u'Vertex 3 Z-coordinate',
                                       'pyname': u'vertex_3_zcoordinate',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'm'}),
                                     (u'vertex 4 x-coordinate',
                                      {'name': u'Vertex 4 X-coordinate',
                                       'pyname': u'vertex_4_xcoordinate',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'm'}),
                                     (u'vertex 4 y-coordinate',
                                      {'name': u'Vertex 4 Y-coordinate',
                                       'pyname': u'vertex_4_ycoordinate',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'm'}),
                                     (u'vertex 4 z-coordinate',
                                      {'name': u'Vertex 4 Z-coordinate',
                                       'pyname': u'vertex_4_zcoordinate',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'm'})]),
              'format': u'vertices',
              'group': u'Thermal Zones and Surfaces',
              'min-fields': 19,
              'name': u'FenestrationSurface:Detailed',
              'pyname': u'FenestrationSurfaceDetailed',
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
    def surface_type(self):
        """Get surface_type.

        Returns:
            str: the value of `surface_type` or None if not set

        """
        return self["Surface Type"]

    @surface_type.setter
    def surface_type(self, value=None):
        """Corresponds to IDD field `Surface Type`

        Args:
            value (str): value for IDD Field `Surface Type`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Surface Type"] = value

    @property
    def construction_name(self):
        """Get construction_name.

        Returns:
            str: the value of `construction_name` or None if not set

        """
        return self["Construction Name"]

    @construction_name.setter
    def construction_name(self, value=None):
        """Corresponds to IDD field `Construction Name` To be matched with a
        construction in this input file.

        Args:
            value (str): value for IDD Field `Construction Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Construction Name"] = value

    @property
    def building_surface_name(self):
        """Get building_surface_name.

        Returns:
            str: the value of `building_surface_name` or None if not set

        """
        return self["Building Surface Name"]

    @building_surface_name.setter
    def building_surface_name(self, value=None):
        """Corresponds to IDD field `Building Surface Name`

        Args:
            value (str): value for IDD Field `Building Surface Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Building Surface Name"] = value

    @property
    def outside_boundary_condition_object(self):
        """Get outside_boundary_condition_object.

        Returns:
            str: the value of `outside_boundary_condition_object` or None if not set

        """
        return self["Outside Boundary Condition Object"]

    @outside_boundary_condition_object.setter
    def outside_boundary_condition_object(self, value=None):
        """  Corresponds to IDD field `Outside Boundary Condition Object`
        Non-blank only if base surface field Outside Boundary Condition is
        Surface or OtherSideCoefficients
        If Base Surface's Surface, specify name of corresponding subsurface in adjacent zone or
        specify current subsurface name for internal partition separating like zones
        If OtherSideCoefficients, specify name of SurfaceProperty:OtherSideCoefficients
        or leave blank to inherit Base Surface's OtherSide Coefficients

        Args:
            value (str): value for IDD Field `Outside Boundary Condition Object`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Outside Boundary Condition Object"] = value

    @property
    def view_factor_to_ground(self):
        """Get view_factor_to_ground.

        Returns:
            float: the value of `view_factor_to_ground` or None if not set

        """
        return self["View Factor to Ground"]

    @view_factor_to_ground.setter
    def view_factor_to_ground(self, value="autocalculate"):
        """  Corresponds to IDD field `View Factor to Ground`
        From the exterior of the surface
        Unused if one uses the "reflections" options in Solar Distribution in Building input
        unless a DaylightingDevice:Shelf or DaylightingDevice:Tubular object has been specified.
        autocalculate will automatically calculate this value from the tilt of the surface

        Args:
            value (float or "Autocalculate"): value for IDD Field `View Factor to Ground`
                Default value: "autocalculate"
                value <= 1.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["View Factor to Ground"] = value

    @property
    def shading_control_name(self):
        """Get shading_control_name.

        Returns:
            str: the value of `shading_control_name` or None if not set

        """
        return self["Shading Control Name"]

    @shading_control_name.setter
    def shading_control_name(self, value=None):
        """  Corresponds to IDD field `Shading Control Name`
        enter the name of a WindowProperty:ShadingControl object
        used for windows and glass doors only
        If not specified, window or glass door has no shading (blind, roller shade, etc.)

        Args:
            value (str): value for IDD Field `Shading Control Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Shading Control Name"] = value

    @property
    def frame_and_divider_name(self):
        """Get frame_and_divider_name.

        Returns:
            str: the value of `frame_and_divider_name` or None if not set

        """
        return self["Frame and Divider Name"]

    @frame_and_divider_name.setter
    def frame_and_divider_name(self, value=None):
        """  Corresponds to IDD field `Frame and Divider Name`
        Enter the name of a WindowProperty:FrameAndDivider object
        Used only for exterior windows (rectangular) and glass doors.
        Unused for triangular windows.
        If not specified (blank), window or glass door has no frame or divider
        and no beam solar reflection from reveal surfaces.

        Args:
            value (str): value for IDD Field `Frame and Divider Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Frame and Divider Name"] = value

    @property
    def multiplier(self):
        """Get multiplier.

        Returns:
            float: the value of `multiplier` or None if not set

        """
        return self["Multiplier"]

    @multiplier.setter
    def multiplier(self, value=1.0):
        """  Corresponds to IDD field `Multiplier`
        Used only for Surface Type = WINDOW, GLASSDOOR or DOOR
        Non-integer values will be truncated to integer

        Args:
            value (float): value for IDD Field `Multiplier`
                Default value: 1.0
                value >= 1.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Multiplier"] = value

    @property
    def number_of_vertices(self):
        """Get number_of_vertices.

        Returns:
            float: the value of `number_of_vertices` or None if not set

        """
        return self["Number of Vertices"]

    @number_of_vertices.setter
    def number_of_vertices(self, value="autocalculate"):
        """  Corresponds to IDD field `Number of Vertices`
        vertices are given in GlobalGeometryRules coordinates -- if relative, all surface coordinates
        are "relative" to the Zone Origin.  If world, then building and zone origins are used
        for some internal calculations, but all coordinates are given in an "absolute" system.

        Args:
            value (float or "Autocalculate"): value for IDD Field `Number of Vertices`
                Default value: "autocalculate"
                value >= 3.0
                value <= 4.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Number of Vertices"] = value

    @property
    def vertex_1_xcoordinate(self):
        """Get vertex_1_xcoordinate.

        Returns:
            float: the value of `vertex_1_xcoordinate` or None if not set

        """
        return self["Vertex 1 X-coordinate"]

    @vertex_1_xcoordinate.setter
    def vertex_1_xcoordinate(self, value=None):
        """  Corresponds to IDD field `Vertex 1 X-coordinate`

        Args:
            value (float): value for IDD Field `Vertex 1 X-coordinate`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Vertex 1 X-coordinate"] = value

    @property
    def vertex_1_ycoordinate(self):
        """Get vertex_1_ycoordinate.

        Returns:
            float: the value of `vertex_1_ycoordinate` or None if not set

        """
        return self["Vertex 1 Y-coordinate"]

    @vertex_1_ycoordinate.setter
    def vertex_1_ycoordinate(self, value=None):
        """  Corresponds to IDD field `Vertex 1 Y-coordinate`

        Args:
            value (float): value for IDD Field `Vertex 1 Y-coordinate`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Vertex 1 Y-coordinate"] = value

    @property
    def vertex_1_zcoordinate(self):
        """Get vertex_1_zcoordinate.

        Returns:
            float: the value of `vertex_1_zcoordinate` or None if not set

        """
        return self["Vertex 1 Z-coordinate"]

    @vertex_1_zcoordinate.setter
    def vertex_1_zcoordinate(self, value=None):
        """  Corresponds to IDD field `Vertex 1 Z-coordinate`

        Args:
            value (float): value for IDD Field `Vertex 1 Z-coordinate`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Vertex 1 Z-coordinate"] = value

    @property
    def vertex_2_xcoordinate(self):
        """Get vertex_2_xcoordinate.

        Returns:
            float: the value of `vertex_2_xcoordinate` or None if not set

        """
        return self["Vertex 2 X-coordinate"]

    @vertex_2_xcoordinate.setter
    def vertex_2_xcoordinate(self, value=None):
        """  Corresponds to IDD field `Vertex 2 X-coordinate`

        Args:
            value (float): value for IDD Field `Vertex 2 X-coordinate`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Vertex 2 X-coordinate"] = value

    @property
    def vertex_2_ycoordinate(self):
        """Get vertex_2_ycoordinate.

        Returns:
            float: the value of `vertex_2_ycoordinate` or None if not set

        """
        return self["Vertex 2 Y-coordinate"]

    @vertex_2_ycoordinate.setter
    def vertex_2_ycoordinate(self, value=None):
        """  Corresponds to IDD field `Vertex 2 Y-coordinate`

        Args:
            value (float): value for IDD Field `Vertex 2 Y-coordinate`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Vertex 2 Y-coordinate"] = value

    @property
    def vertex_2_zcoordinate(self):
        """Get vertex_2_zcoordinate.

        Returns:
            float: the value of `vertex_2_zcoordinate` or None if not set

        """
        return self["Vertex 2 Z-coordinate"]

    @vertex_2_zcoordinate.setter
    def vertex_2_zcoordinate(self, value=None):
        """  Corresponds to IDD field `Vertex 2 Z-coordinate`

        Args:
            value (float): value for IDD Field `Vertex 2 Z-coordinate`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Vertex 2 Z-coordinate"] = value

    @property
    def vertex_3_xcoordinate(self):
        """Get vertex_3_xcoordinate.

        Returns:
            float: the value of `vertex_3_xcoordinate` or None if not set

        """
        return self["Vertex 3 X-coordinate"]

    @vertex_3_xcoordinate.setter
    def vertex_3_xcoordinate(self, value=None):
        """  Corresponds to IDD field `Vertex 3 X-coordinate`

        Args:
            value (float): value for IDD Field `Vertex 3 X-coordinate`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Vertex 3 X-coordinate"] = value

    @property
    def vertex_3_ycoordinate(self):
        """Get vertex_3_ycoordinate.

        Returns:
            float: the value of `vertex_3_ycoordinate` or None if not set

        """
        return self["Vertex 3 Y-coordinate"]

    @vertex_3_ycoordinate.setter
    def vertex_3_ycoordinate(self, value=None):
        """  Corresponds to IDD field `Vertex 3 Y-coordinate`

        Args:
            value (float): value for IDD Field `Vertex 3 Y-coordinate`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Vertex 3 Y-coordinate"] = value

    @property
    def vertex_3_zcoordinate(self):
        """Get vertex_3_zcoordinate.

        Returns:
            float: the value of `vertex_3_zcoordinate` or None if not set

        """
        return self["Vertex 3 Z-coordinate"]

    @vertex_3_zcoordinate.setter
    def vertex_3_zcoordinate(self, value=None):
        """  Corresponds to IDD field `Vertex 3 Z-coordinate`

        Args:
            value (float): value for IDD Field `Vertex 3 Z-coordinate`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Vertex 3 Z-coordinate"] = value

    @property
    def vertex_4_xcoordinate(self):
        """Get vertex_4_xcoordinate.

        Returns:
            float: the value of `vertex_4_xcoordinate` or None if not set

        """
        return self["Vertex 4 X-coordinate"]

    @vertex_4_xcoordinate.setter
    def vertex_4_xcoordinate(self, value=None):
        """  Corresponds to IDD field `Vertex 4 X-coordinate`
        Not used for triangles

        Args:
            value (float): value for IDD Field `Vertex 4 X-coordinate`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Vertex 4 X-coordinate"] = value

    @property
    def vertex_4_ycoordinate(self):
        """Get vertex_4_ycoordinate.

        Returns:
            float: the value of `vertex_4_ycoordinate` or None if not set

        """
        return self["Vertex 4 Y-coordinate"]

    @vertex_4_ycoordinate.setter
    def vertex_4_ycoordinate(self, value=None):
        """  Corresponds to IDD field `Vertex 4 Y-coordinate`
        Not used for triangles

        Args:
            value (float): value for IDD Field `Vertex 4 Y-coordinate`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Vertex 4 Y-coordinate"] = value

    @property
    def vertex_4_zcoordinate(self):
        """Get vertex_4_zcoordinate.

        Returns:
            float: the value of `vertex_4_zcoordinate` or None if not set

        """
        return self["Vertex 4 Z-coordinate"]

    @vertex_4_zcoordinate.setter
    def vertex_4_zcoordinate(self, value=None):
        """  Corresponds to IDD field `Vertex 4 Z-coordinate`
        Not used for triangles

        Args:
            value (float): value for IDD Field `Vertex 4 Z-coordinate`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Vertex 4 Z-coordinate"] = value




class Window(DataObject):

    """Corresponds to IDD object `Window` Allows for simplified entry of
    Windows."""
    schema = {'extensible-fields': OrderedDict(),
              'fields': OrderedDict([(u'name',
                                      {'name': u'Name',
                                       'pyname': u'name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'alpha'}),
                                     (u'construction name',
                                      {'name': u'Construction Name',
                                       'pyname': u'construction_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'building surface name',
                                      {'name': u'Building Surface Name',
                                       'pyname': u'building_surface_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'shading control name',
                                      {'name': u'Shading Control Name',
                                       'pyname': u'shading_control_name',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'frame and divider name',
                                      {'name': u'Frame and Divider Name',
                                       'pyname': u'frame_and_divider_name',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'multiplier',
                                      {'name': u'Multiplier',
                                       'pyname': u'multiplier',
                                       'default': 1.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 1.0,
                                       'autocalculatable': False,
                                       'type': 'real'}),
                                     (u'starting x coordinate',
                                      {'name': u'Starting X Coordinate',
                                       'pyname': u'starting_x_coordinate',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'starting z coordinate',
                                      {'name': u'Starting Z Coordinate',
                                       'pyname': u'starting_z_coordinate',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'length',
                                      {'name': u'Length',
                                       'pyname': u'length',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'height',
                                      {'name': u'Height',
                                       'pyname': u'height',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'})]),
              'format': None,
              'group': u'Thermal Zones and Surfaces',
              'min-fields': 0,
              'name': u'Window',
              'pyname': u'Window',
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
        """Corresponds to IDD field `Construction Name` To be matched with a
        construction in this input file.

        Args:
            value (str): value for IDD Field `Construction Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Construction Name"] = value

    @property
    def building_surface_name(self):
        """Get building_surface_name.

        Returns:
            str: the value of `building_surface_name` or None if not set

        """
        return self["Building Surface Name"]

    @building_surface_name.setter
    def building_surface_name(self, value=None):
        """Corresponds to IDD field `Building Surface Name` Name of Surface
        (Wall, usually) the Window is on (i.e., Base Surface) Window assumes
        the azimuth and tilt angles of the surface it is on.

        Args:
            value (str): value for IDD Field `Building Surface Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Building Surface Name"] = value

    @property
    def shading_control_name(self):
        """Get shading_control_name.

        Returns:
            str: the value of `shading_control_name` or None if not set

        """
        return self["Shading Control Name"]

    @shading_control_name.setter
    def shading_control_name(self, value=None):
        """  Corresponds to IDD field `Shading Control Name`
        enter the name of a WindowProperty:ShadingControl object
        used for windows and glass doors only
        If not specified, window or glass door has no shading (blind, roller shade, etc.)

        Args:
            value (str): value for IDD Field `Shading Control Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Shading Control Name"] = value

    @property
    def frame_and_divider_name(self):
        """Get frame_and_divider_name.

        Returns:
            str: the value of `frame_and_divider_name` or None if not set

        """
        return self["Frame and Divider Name"]

    @frame_and_divider_name.setter
    def frame_and_divider_name(self, value=None):
        """  Corresponds to IDD field `Frame and Divider Name`
        Enter the name of a WindowProperty:FrameAndDivider object
        Used only for exterior windows (rectangular) and glass doors.
        Unused for triangular windows.
        If not specified (blank), window or glass door has no frame or divider
        and no beam solar reflection from reveal surfaces.

        Args:
            value (str): value for IDD Field `Frame and Divider Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Frame and Divider Name"] = value

    @property
    def multiplier(self):
        """Get multiplier.

        Returns:
            float: the value of `multiplier` or None if not set

        """
        return self["Multiplier"]

    @multiplier.setter
    def multiplier(self, value=1.0):
        """  Corresponds to IDD field `Multiplier`
        Used only for Surface Type = WINDOW, GLASSDOOR or DOOR
        Non-integer values will be truncated to integer

        Args:
            value (float): value for IDD Field `Multiplier`
                Default value: 1.0
                value >= 1.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Multiplier"] = value

    @property
    def starting_x_coordinate(self):
        """Get starting_x_coordinate.

        Returns:
            float: the value of `starting_x_coordinate` or None if not set

        """
        return self["Starting X Coordinate"]

    @starting_x_coordinate.setter
    def starting_x_coordinate(self, value=None):
        """Corresponds to IDD field `Starting X Coordinate` Window starting
        coordinate is specified relative to the Base Surface origin.

        Args:
            value (float): value for IDD Field `Starting X Coordinate`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Starting X Coordinate"] = value

    @property
    def starting_z_coordinate(self):
        """Get starting_z_coordinate.

        Returns:
            float: the value of `starting_z_coordinate` or None if not set

        """
        return self["Starting Z Coordinate"]

    @starting_z_coordinate.setter
    def starting_z_coordinate(self, value=None):
        """  Corresponds to IDD field `Starting Z Coordinate`
        How far up the wall the Window starts. (in 2-d, this would be a Y Coordinate)

        Args:
            value (float): value for IDD Field `Starting Z Coordinate`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Starting Z Coordinate"] = value

    @property
    def length(self):
        """Get length.

        Returns:
            float: the value of `length` or None if not set

        """
        return self["Length"]

    @length.setter
    def length(self, value=None):
        """Corresponds to IDD field `Length`

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
    def height(self):
        """Get height.

        Returns:
            float: the value of `height` or None if not set

        """
        return self["Height"]

    @height.setter
    def height(self, value=None):
        """Corresponds to IDD field `Height`

        Args:
            value (float): value for IDD Field `Height`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Height"] = value




class Door(DataObject):

    """Corresponds to IDD object `Door` Allows for simplified entry of opaque
    Doors."""
    schema = {'extensible-fields': OrderedDict(),
              'fields': OrderedDict([(u'name',
                                      {'name': u'Name',
                                       'pyname': u'name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'alpha'}),
                                     (u'construction name',
                                      {'name': u'Construction Name',
                                       'pyname': u'construction_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'building surface name',
                                      {'name': u'Building Surface Name',
                                       'pyname': u'building_surface_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'multiplier',
                                      {'name': u'Multiplier',
                                       'pyname': u'multiplier',
                                       'default': 1.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 1.0,
                                       'autocalculatable': False,
                                       'type': 'real'}),
                                     (u'starting x coordinate',
                                      {'name': u'Starting X Coordinate',
                                       'pyname': u'starting_x_coordinate',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'starting z coordinate',
                                      {'name': u'Starting Z Coordinate',
                                       'pyname': u'starting_z_coordinate',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'length',
                                      {'name': u'Length',
                                       'pyname': u'length',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'height',
                                      {'name': u'Height',
                                       'pyname': u'height',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'})]),
              'format': None,
              'group': u'Thermal Zones and Surfaces',
              'min-fields': 0,
              'name': u'Door',
              'pyname': u'Door',
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
        """Corresponds to IDD field `Construction Name` To be matched with a
        construction in this input file.

        Args:
            value (str): value for IDD Field `Construction Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Construction Name"] = value

    @property
    def building_surface_name(self):
        """Get building_surface_name.

        Returns:
            str: the value of `building_surface_name` or None if not set

        """
        return self["Building Surface Name"]

    @building_surface_name.setter
    def building_surface_name(self, value=None):
        """Corresponds to IDD field `Building Surface Name` Name of Surface
        (Wall, usually) the Door is on (i.e., Base Surface) Door assumes the
        azimuth and tilt angles of the surface it is on.

        Args:
            value (str): value for IDD Field `Building Surface Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Building Surface Name"] = value

    @property
    def multiplier(self):
        """Get multiplier.

        Returns:
            float: the value of `multiplier` or None if not set

        """
        return self["Multiplier"]

    @multiplier.setter
    def multiplier(self, value=1.0):
        """  Corresponds to IDD field `Multiplier`
        Used only for Surface Type = WINDOW, GLASSDOOR or DOOR
        Non-integer values will be truncated to integer

        Args:
            value (float): value for IDD Field `Multiplier`
                Default value: 1.0
                value >= 1.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Multiplier"] = value

    @property
    def starting_x_coordinate(self):
        """Get starting_x_coordinate.

        Returns:
            float: the value of `starting_x_coordinate` or None if not set

        """
        return self["Starting X Coordinate"]

    @starting_x_coordinate.setter
    def starting_x_coordinate(self, value=None):
        """Corresponds to IDD field `Starting X Coordinate` Door starting
        coordinate is specified relative to the Base Surface origin.

        Args:
            value (float): value for IDD Field `Starting X Coordinate`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Starting X Coordinate"] = value

    @property
    def starting_z_coordinate(self):
        """Get starting_z_coordinate.

        Returns:
            float: the value of `starting_z_coordinate` or None if not set

        """
        return self["Starting Z Coordinate"]

    @starting_z_coordinate.setter
    def starting_z_coordinate(self, value=None):
        """  Corresponds to IDD field `Starting Z Coordinate`
        How far up the wall the Door starts. (in 2-d, this would be a Y Coordinate)

        Args:
            value (float): value for IDD Field `Starting Z Coordinate`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Starting Z Coordinate"] = value

    @property
    def length(self):
        """Get length.

        Returns:
            float: the value of `length` or None if not set

        """
        return self["Length"]

    @length.setter
    def length(self, value=None):
        """Corresponds to IDD field `Length`

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
    def height(self):
        """Get height.

        Returns:
            float: the value of `height` or None if not set

        """
        return self["Height"]

    @height.setter
    def height(self, value=None):
        """Corresponds to IDD field `Height`

        Args:
            value (float): value for IDD Field `Height`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Height"] = value




class GlazedDoor(DataObject):

    """Corresponds to IDD object `GlazedDoor` Allows for simplified entry of
    glass Doors."""
    schema = {'extensible-fields': OrderedDict(),
              'fields': OrderedDict([(u'name',
                                      {'name': u'Name',
                                       'pyname': u'name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'alpha'}),
                                     (u'construction name',
                                      {'name': u'Construction Name',
                                       'pyname': u'construction_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'building surface name',
                                      {'name': u'Building Surface Name',
                                       'pyname': u'building_surface_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'shading control name',
                                      {'name': u'Shading Control Name',
                                       'pyname': u'shading_control_name',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'frame and divider name',
                                      {'name': u'Frame and Divider Name',
                                       'pyname': u'frame_and_divider_name',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'multiplier',
                                      {'name': u'Multiplier',
                                       'pyname': u'multiplier',
                                       'default': 1.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 1.0,
                                       'autocalculatable': False,
                                       'type': 'real'}),
                                     (u'starting x coordinate',
                                      {'name': u'Starting X Coordinate',
                                       'pyname': u'starting_x_coordinate',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'starting z coordinate',
                                      {'name': u'Starting Z Coordinate',
                                       'pyname': u'starting_z_coordinate',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'length',
                                      {'name': u'Length',
                                       'pyname': u'length',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'height',
                                      {'name': u'Height',
                                       'pyname': u'height',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'})]),
              'format': None,
              'group': u'Thermal Zones and Surfaces',
              'min-fields': 0,
              'name': u'GlazedDoor',
              'pyname': u'GlazedDoor',
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
        """Corresponds to IDD field `Construction Name` To be matched with a
        construction in this input file.

        Args:
            value (str): value for IDD Field `Construction Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Construction Name"] = value

    @property
    def building_surface_name(self):
        """Get building_surface_name.

        Returns:
            str: the value of `building_surface_name` or None if not set

        """
        return self["Building Surface Name"]

    @building_surface_name.setter
    def building_surface_name(self, value=None):
        """Corresponds to IDD field `Building Surface Name` Name of Surface
        (Wall, usually) the Door is on (i.e., Base Surface) Door assumes the
        azimuth and tilt angles of the surface it is on.

        Args:
            value (str): value for IDD Field `Building Surface Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Building Surface Name"] = value

    @property
    def shading_control_name(self):
        """Get shading_control_name.

        Returns:
            str: the value of `shading_control_name` or None if not set

        """
        return self["Shading Control Name"]

    @shading_control_name.setter
    def shading_control_name(self, value=None):
        """  Corresponds to IDD field `Shading Control Name`
        enter the name of a WindowProperty:ShadingControl object
        used for windows and glass doors only
        If not specified, window or glass door has no shading (blind, roller shade, etc.)

        Args:
            value (str): value for IDD Field `Shading Control Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Shading Control Name"] = value

    @property
    def frame_and_divider_name(self):
        """Get frame_and_divider_name.

        Returns:
            str: the value of `frame_and_divider_name` or None if not set

        """
        return self["Frame and Divider Name"]

    @frame_and_divider_name.setter
    def frame_and_divider_name(self, value=None):
        """  Corresponds to IDD field `Frame and Divider Name`
        Enter the name of a WindowProperty:FrameAndDivider object
        Used only for exterior windows (rectangular) and glass doors.
        Unused for triangular windows.
        If not specified (blank), window or glass door has no frame or divider
        and no beam solar reflection from reveal surfaces.

        Args:
            value (str): value for IDD Field `Frame and Divider Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Frame and Divider Name"] = value

    @property
    def multiplier(self):
        """Get multiplier.

        Returns:
            float: the value of `multiplier` or None if not set

        """
        return self["Multiplier"]

    @multiplier.setter
    def multiplier(self, value=1.0):
        """  Corresponds to IDD field `Multiplier`
        Used only for Surface Type = WINDOW, GLASSDOOR or DOOR
        Non-integer values will be truncated to integer

        Args:
            value (float): value for IDD Field `Multiplier`
                Default value: 1.0
                value >= 1.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Multiplier"] = value

    @property
    def starting_x_coordinate(self):
        """Get starting_x_coordinate.

        Returns:
            float: the value of `starting_x_coordinate` or None if not set

        """
        return self["Starting X Coordinate"]

    @starting_x_coordinate.setter
    def starting_x_coordinate(self, value=None):
        """Corresponds to IDD field `Starting X Coordinate` Door starting
        coordinate is specified relative to the Base Surface origin.

        Args:
            value (float): value for IDD Field `Starting X Coordinate`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Starting X Coordinate"] = value

    @property
    def starting_z_coordinate(self):
        """Get starting_z_coordinate.

        Returns:
            float: the value of `starting_z_coordinate` or None if not set

        """
        return self["Starting Z Coordinate"]

    @starting_z_coordinate.setter
    def starting_z_coordinate(self, value=None):
        """  Corresponds to IDD field `Starting Z Coordinate`
        How far up the wall the Door starts. (in 2-d, this would be a Y Coordinate)

        Args:
            value (float): value for IDD Field `Starting Z Coordinate`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Starting Z Coordinate"] = value

    @property
    def length(self):
        """Get length.

        Returns:
            float: the value of `length` or None if not set

        """
        return self["Length"]

    @length.setter
    def length(self, value=None):
        """Corresponds to IDD field `Length`

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
    def height(self):
        """Get height.

        Returns:
            float: the value of `height` or None if not set

        """
        return self["Height"]

    @height.setter
    def height(self, value=None):
        """Corresponds to IDD field `Height`

        Args:
            value (float): value for IDD Field `Height`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Height"] = value




class WindowInterzone(DataObject):

    """ Corresponds to IDD object `Window:Interzone`
        Allows for simplified entry of interzone windows (adjacent to
        other zones).
    """
    schema = {'extensible-fields': OrderedDict(),
              'fields': OrderedDict([(u'name',
                                      {'name': u'Name',
                                       'pyname': u'name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'alpha'}),
                                     (u'construction name',
                                      {'name': u'Construction Name',
                                       'pyname': u'construction_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'building surface name',
                                      {'name': u'Building Surface Name',
                                       'pyname': u'building_surface_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'outside boundary condition object',
                                      {'name': u'Outside Boundary Condition Object',
                                       'pyname': u'outside_boundary_condition_object',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'multiplier',
                                      {'name': u'Multiplier',
                                       'pyname': u'multiplier',
                                       'default': 1.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 1.0,
                                       'autocalculatable': False,
                                       'type': 'real'}),
                                     (u'starting x coordinate',
                                      {'name': u'Starting X Coordinate',
                                       'pyname': u'starting_x_coordinate',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'starting z coordinate',
                                      {'name': u'Starting Z Coordinate',
                                       'pyname': u'starting_z_coordinate',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'length',
                                      {'name': u'Length',
                                       'pyname': u'length',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'height',
                                      {'name': u'Height',
                                       'pyname': u'height',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'})]),
              'format': None,
              'group': u'Thermal Zones and Surfaces',
              'min-fields': 0,
              'name': u'Window:Interzone',
              'pyname': u'WindowInterzone',
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
        """Corresponds to IDD field `Construction Name` To be matched with a
        construction in this input file.

        Args:
            value (str): value for IDD Field `Construction Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Construction Name"] = value

    @property
    def building_surface_name(self):
        """Get building_surface_name.

        Returns:
            str: the value of `building_surface_name` or None if not set

        """
        return self["Building Surface Name"]

    @building_surface_name.setter
    def building_surface_name(self, value=None):
        """Corresponds to IDD field `Building Surface Name` Name of Surface
        (Wall, usually) the Window is on (i.e., Base Surface) Window assumes
        the azimuth and tilt angles of the surface it is on.

        Args:
            value (str): value for IDD Field `Building Surface Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Building Surface Name"] = value

    @property
    def outside_boundary_condition_object(self):
        """Get outside_boundary_condition_object.

        Returns:
            str: the value of `outside_boundary_condition_object` or None if not set

        """
        return self["Outside Boundary Condition Object"]

    @outside_boundary_condition_object.setter
    def outside_boundary_condition_object(self, value=None):
        """Corresponds to IDD field `Outside Boundary Condition Object` Specify
        a surface name in an adjacent zone for known interior windows. Specify
        a zone name of an adjacent zone to automatically generate the interior
        window in the adjacent zone. a blank field will set up a Window in an
        adjacent zone (same zone as adjacent to base surface)

        Args:
            value (str): value for IDD Field `Outside Boundary Condition Object`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Outside Boundary Condition Object"] = value

    @property
    def multiplier(self):
        """Get multiplier.

        Returns:
            float: the value of `multiplier` or None if not set

        """
        return self["Multiplier"]

    @multiplier.setter
    def multiplier(self, value=1.0):
        """  Corresponds to IDD field `Multiplier`
        Used only for Surface Type = WINDOW, GLASSDOOR or DOOR
        Non-integer values will be truncated to integer

        Args:
            value (float): value for IDD Field `Multiplier`
                Default value: 1.0
                value >= 1.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Multiplier"] = value

    @property
    def starting_x_coordinate(self):
        """Get starting_x_coordinate.

        Returns:
            float: the value of `starting_x_coordinate` or None if not set

        """
        return self["Starting X Coordinate"]

    @starting_x_coordinate.setter
    def starting_x_coordinate(self, value=None):
        """Corresponds to IDD field `Starting X Coordinate` Window starting
        coordinate is specified relative to the Base Surface origin.

        Args:
            value (float): value for IDD Field `Starting X Coordinate`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Starting X Coordinate"] = value

    @property
    def starting_z_coordinate(self):
        """Get starting_z_coordinate.

        Returns:
            float: the value of `starting_z_coordinate` or None if not set

        """
        return self["Starting Z Coordinate"]

    @starting_z_coordinate.setter
    def starting_z_coordinate(self, value=None):
        """  Corresponds to IDD field `Starting Z Coordinate`
        How far up the wall the Window starts. (in 2-d, this would be a Y Coordinate)

        Args:
            value (float): value for IDD Field `Starting Z Coordinate`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Starting Z Coordinate"] = value

    @property
    def length(self):
        """Get length.

        Returns:
            float: the value of `length` or None if not set

        """
        return self["Length"]

    @length.setter
    def length(self, value=None):
        """Corresponds to IDD field `Length`

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
    def height(self):
        """Get height.

        Returns:
            float: the value of `height` or None if not set

        """
        return self["Height"]

    @height.setter
    def height(self, value=None):
        """Corresponds to IDD field `Height`

        Args:
            value (float): value for IDD Field `Height`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Height"] = value




class DoorInterzone(DataObject):

    """ Corresponds to IDD object `Door:Interzone`
        Allows for simplified entry of interzone (opaque interior) doors (adjacent to
        other zones).
    """
    schema = {'extensible-fields': OrderedDict(),
              'fields': OrderedDict([(u'name',
                                      {'name': u'Name',
                                       'pyname': u'name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'alpha'}),
                                     (u'construction name',
                                      {'name': u'Construction Name',
                                       'pyname': u'construction_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'building surface name',
                                      {'name': u'Building Surface Name',
                                       'pyname': u'building_surface_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'outside boundary condition object',
                                      {'name': u'Outside Boundary Condition Object',
                                       'pyname': u'outside_boundary_condition_object',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'multiplier',
                                      {'name': u'Multiplier',
                                       'pyname': u'multiplier',
                                       'default': 1.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 1.0,
                                       'autocalculatable': False,
                                       'type': 'real'}),
                                     (u'starting x coordinate',
                                      {'name': u'Starting X Coordinate',
                                       'pyname': u'starting_x_coordinate',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'starting z coordinate',
                                      {'name': u'Starting Z Coordinate',
                                       'pyname': u'starting_z_coordinate',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'length',
                                      {'name': u'Length',
                                       'pyname': u'length',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'height',
                                      {'name': u'Height',
                                       'pyname': u'height',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'})]),
              'format': None,
              'group': u'Thermal Zones and Surfaces',
              'min-fields': 0,
              'name': u'Door:Interzone',
              'pyname': u'DoorInterzone',
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
        """Corresponds to IDD field `Construction Name` To be matched with a
        construction in this input file.

        Args:
            value (str): value for IDD Field `Construction Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Construction Name"] = value

    @property
    def building_surface_name(self):
        """Get building_surface_name.

        Returns:
            str: the value of `building_surface_name` or None if not set

        """
        return self["Building Surface Name"]

    @building_surface_name.setter
    def building_surface_name(self, value=None):
        """Corresponds to IDD field `Building Surface Name` Name of Surface
        (Wall, usually) the Door is on (i.e., Base Surface) Door assumes the
        azimuth and tilt angles of the surface it is on.

        Args:
            value (str): value for IDD Field `Building Surface Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Building Surface Name"] = value

    @property
    def outside_boundary_condition_object(self):
        """Get outside_boundary_condition_object.

        Returns:
            str: the value of `outside_boundary_condition_object` or None if not set

        """
        return self["Outside Boundary Condition Object"]

    @outside_boundary_condition_object.setter
    def outside_boundary_condition_object(self, value=None):
        """Corresponds to IDD field `Outside Boundary Condition Object` Specify
        a surface name in an adjacent zone for known interior doors. Specify a
        zone name of an adjacent zone to automatically generate the interior
        door in the adjacent zone. a blank field will set up a Window in an
        adjacent zone (same zone as adjacent to base surface)

        Args:
            value (str): value for IDD Field `Outside Boundary Condition Object`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Outside Boundary Condition Object"] = value

    @property
    def multiplier(self):
        """Get multiplier.

        Returns:
            float: the value of `multiplier` or None if not set

        """
        return self["Multiplier"]

    @multiplier.setter
    def multiplier(self, value=1.0):
        """  Corresponds to IDD field `Multiplier`
        Used only for Surface Type = WINDOW, GLASSDOOR or DOOR
        Non-integer values will be truncated to integer

        Args:
            value (float): value for IDD Field `Multiplier`
                Default value: 1.0
                value >= 1.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Multiplier"] = value

    @property
    def starting_x_coordinate(self):
        """Get starting_x_coordinate.

        Returns:
            float: the value of `starting_x_coordinate` or None if not set

        """
        return self["Starting X Coordinate"]

    @starting_x_coordinate.setter
    def starting_x_coordinate(self, value=None):
        """Corresponds to IDD field `Starting X Coordinate` Door starting
        coordinate is specified relative to the Base Surface origin.

        Args:
            value (float): value for IDD Field `Starting X Coordinate`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Starting X Coordinate"] = value

    @property
    def starting_z_coordinate(self):
        """Get starting_z_coordinate.

        Returns:
            float: the value of `starting_z_coordinate` or None if not set

        """
        return self["Starting Z Coordinate"]

    @starting_z_coordinate.setter
    def starting_z_coordinate(self, value=None):
        """  Corresponds to IDD field `Starting Z Coordinate`
        How far up the wall the Door starts. (in 2-d, this would be a Y Coordinate)

        Args:
            value (float): value for IDD Field `Starting Z Coordinate`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Starting Z Coordinate"] = value

    @property
    def length(self):
        """Get length.

        Returns:
            float: the value of `length` or None if not set

        """
        return self["Length"]

    @length.setter
    def length(self, value=None):
        """Corresponds to IDD field `Length`

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
    def height(self):
        """Get height.

        Returns:
            float: the value of `height` or None if not set

        """
        return self["Height"]

    @height.setter
    def height(self, value=None):
        """Corresponds to IDD field `Height`

        Args:
            value (float): value for IDD Field `Height`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Height"] = value




class GlazedDoorInterzone(DataObject):

    """ Corresponds to IDD object `GlazedDoor:Interzone`
        Allows for simplified entry of interzone (glass interior) doors (adjacent to
        other zones).
    """
    schema = {'extensible-fields': OrderedDict(),
              'fields': OrderedDict([(u'name',
                                      {'name': u'Name',
                                       'pyname': u'name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'alpha'}),
                                     (u'construction name',
                                      {'name': u'Construction Name',
                                       'pyname': u'construction_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'building surface name',
                                      {'name': u'Building Surface Name',
                                       'pyname': u'building_surface_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'outside boundary condition object',
                                      {'name': u'Outside Boundary Condition Object',
                                       'pyname': u'outside_boundary_condition_object',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'multiplier',
                                      {'name': u'Multiplier',
                                       'pyname': u'multiplier',
                                       'default': 1.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 1.0,
                                       'autocalculatable': False,
                                       'type': 'real'}),
                                     (u'starting x coordinate',
                                      {'name': u'Starting X Coordinate',
                                       'pyname': u'starting_x_coordinate',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'starting z coordinate',
                                      {'name': u'Starting Z Coordinate',
                                       'pyname': u'starting_z_coordinate',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'length',
                                      {'name': u'Length',
                                       'pyname': u'length',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'height',
                                      {'name': u'Height',
                                       'pyname': u'height',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'})]),
              'format': None,
              'group': u'Thermal Zones and Surfaces',
              'min-fields': 0,
              'name': u'GlazedDoor:Interzone',
              'pyname': u'GlazedDoorInterzone',
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
        """Corresponds to IDD field `Construction Name` To be matched with a
        construction in this input file.

        Args:
            value (str): value for IDD Field `Construction Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Construction Name"] = value

    @property
    def building_surface_name(self):
        """Get building_surface_name.

        Returns:
            str: the value of `building_surface_name` or None if not set

        """
        return self["Building Surface Name"]

    @building_surface_name.setter
    def building_surface_name(self, value=None):
        """Corresponds to IDD field `Building Surface Name` Name of Surface
        (Wall, usually) the Door is on (i.e., Base Surface) Door assumes the
        azimuth and tilt angles of the surface it is on.

        Args:
            value (str): value for IDD Field `Building Surface Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Building Surface Name"] = value

    @property
    def outside_boundary_condition_object(self):
        """Get outside_boundary_condition_object.

        Returns:
            str: the value of `outside_boundary_condition_object` or None if not set

        """
        return self["Outside Boundary Condition Object"]

    @outside_boundary_condition_object.setter
    def outside_boundary_condition_object(self, value=None):
        """Corresponds to IDD field `Outside Boundary Condition Object` Specify
        a surface name in an adjacent zone for known interior doors. Specify a
        zone name of an adjacent zone to automatically generate the interior
        door in the adjacent zone. a blank field will set up a Window in an
        adjacent zone (same zone as adjacent to base surface)

        Args:
            value (str): value for IDD Field `Outside Boundary Condition Object`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Outside Boundary Condition Object"] = value

    @property
    def multiplier(self):
        """Get multiplier.

        Returns:
            float: the value of `multiplier` or None if not set

        """
        return self["Multiplier"]

    @multiplier.setter
    def multiplier(self, value=1.0):
        """  Corresponds to IDD field `Multiplier`
        Used only for Surface Type = WINDOW, GLASSDOOR or DOOR
        Non-integer values will be truncated to integer

        Args:
            value (float): value for IDD Field `Multiplier`
                Default value: 1.0
                value >= 1.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Multiplier"] = value

    @property
    def starting_x_coordinate(self):
        """Get starting_x_coordinate.

        Returns:
            float: the value of `starting_x_coordinate` or None if not set

        """
        return self["Starting X Coordinate"]

    @starting_x_coordinate.setter
    def starting_x_coordinate(self, value=None):
        """Corresponds to IDD field `Starting X Coordinate` Door starting
        coordinate is specified relative to the Base Surface origin.

        Args:
            value (float): value for IDD Field `Starting X Coordinate`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Starting X Coordinate"] = value

    @property
    def starting_z_coordinate(self):
        """Get starting_z_coordinate.

        Returns:
            float: the value of `starting_z_coordinate` or None if not set

        """
        return self["Starting Z Coordinate"]

    @starting_z_coordinate.setter
    def starting_z_coordinate(self, value=None):
        """  Corresponds to IDD field `Starting Z Coordinate`
        How far up the wall the Door starts. (in 2-d, this would be a Y Coordinate)

        Args:
            value (float): value for IDD Field `Starting Z Coordinate`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Starting Z Coordinate"] = value

    @property
    def length(self):
        """Get length.

        Returns:
            float: the value of `length` or None if not set

        """
        return self["Length"]

    @length.setter
    def length(self, value=None):
        """Corresponds to IDD field `Length`

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
    def height(self):
        """Get height.

        Returns:
            float: the value of `height` or None if not set

        """
        return self["Height"]

    @height.setter
    def height(self, value=None):
        """Corresponds to IDD field `Height`

        Args:
            value (float): value for IDD Field `Height`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Height"] = value




class WindowPropertyShadingControl(DataObject):

    """ Corresponds to IDD object `WindowProperty:ShadingControl`
        Specifies the type, location, and controls for window shades, window blinds, and
        switchable glazing. Referenced by the surface objects for exterior windows and glass
        doors (ref: FenestrationSurface:Detailed, Window, and GlazedDoor).
    """
    schema = {'extensible-fields': OrderedDict(),
              'fields': OrderedDict([(u'name',
                                      {'name': u'Name',
                                       'pyname': u'name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'alpha'}),
                                     (u'shading type',
                                      {'name': u'Shading Type',
                                       'pyname': u'shading_type',
                                       'required-field': True,
                                       'autosizable': False,
                                       'accepted-values': [u'InteriorShade',
                                                           u'ExteriorShade',
                                                           u'ExteriorScreen',
                                                           u'InteriorBlind',
                                                           u'ExteriorBlind',
                                                           u'BetweenGlassShade',
                                                           u'BetweenGlassBlind',
                                                           u'SwitchableGlazing'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'construction with shading name',
                                      {'name': u'Construction with Shading Name',
                                       'pyname': u'construction_with_shading_name',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'shading control type',
                                      {'name': u'Shading Control Type',
                                       'pyname': u'shading_control_type',
                                       'required-field': True,
                                       'autosizable': False,
                                       'accepted-values': [u'AlwaysOn',
                                                           u'AlwaysOff',
                                                           u'OnIfScheduleAllows',
                                                           u'OnIfHighSolarOnWindow',
                                                           u'OnIfHighHorizontalSolar',
                                                           u'OnIfHighOutdoorAirTemperature',
                                                           u'OnIfHighZoneAirTemperature',
                                                           u'OnIfHighZoneCooling',
                                                           u'OnIfHighGlare',
                                                           u'MeetDaylightIlluminanceSetpoint',
                                                           u'OnNightIfLowOutdoorTempAndOffDay',
                                                           u'OnNightIfLowInsideTempAndOffDay',
                                                           u'OnNightIfHeatingAndOffDay',
                                                           u'OnNightIfLowOutdoorTempAndOnDayIfCooling',
                                                           u'OnNightIfHeatingAndOnDayIfCooling',
                                                           u'OffNightAndOnDayIfCoolingAndHighSolarOnWindow',
                                                           u'OnNightAndOnDayIfCoolingAndHighSolarOnWindow',
                                                           u'OnIfHighOutdoorAirTempAndHighSolarOnWindow',
                                                           u'OnIfHighOutdoorAirTempAndHighHorizontalSolar',
                                                           u'OnIfHighZoneAirTempAndHighSolarOnWindow',
                                                           u'OnIfHighZoneAirTempAndHighHorizontalSolar'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'schedule name',
                                      {'name': u'Schedule Name',
                                       'pyname': u'schedule_name',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'setpoint',
                                      {'name': u'Setpoint',
                                       'pyname': u'setpoint',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'W/m2, W or deg C'}),
                                     (u'shading control is scheduled',
                                      {'name': u'Shading Control Is Scheduled',
                                       'pyname': u'shading_control_is_scheduled',
                                       'default': u'No',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'No',
                                                           u'Yes'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'glare control is active',
                                      {'name': u'Glare Control Is Active',
                                       'pyname': u'glare_control_is_active',
                                       'default': u'No',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'No',
                                                           u'Yes'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'shading device material name',
                                      {'name': u'Shading Device Material Name',
                                       'pyname': u'shading_device_material_name',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'type of slat angle control for blinds',
                                      {'name': u'Type of Slat Angle Control for Blinds',
                                       'pyname': u'type_of_slat_angle_control_for_blinds',
                                       'default': u'FixedSlatAngle',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'FixedSlatAngle',
                                                           u'ScheduledSlatAngle',
                                                           u'BlockBeamSolar'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'slat angle schedule name',
                                      {'name': u'Slat Angle Schedule Name',
                                       'pyname': u'slat_angle_schedule_name',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'setpoint 2',
                                      {'name': u'Setpoint 2',
                                       'pyname': u'setpoint_2',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'W/m2 or deg C'})]),
              'format': None,
              'group': u'Thermal Zones and Surfaces',
              'min-fields': 11,
              'name': u'WindowProperty:ShadingControl',
              'pyname': u'WindowPropertyShadingControl',
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
        """Corresponds to IDD field `Name` Referenced by surfaces that are
        exterior windows Not used by interzone windows.

        Args:
            value (str): value for IDD Field `Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Name"] = value

    @property
    def shading_type(self):
        """Get shading_type.

        Returns:
            str: the value of `shading_type` or None if not set

        """
        return self["Shading Type"]

    @shading_type.setter
    def shading_type(self, value=None):
        """Corresponds to IDD field `Shading Type`

        Args:
            value (str): value for IDD Field `Shading Type`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Shading Type"] = value

    @property
    def construction_with_shading_name(self):
        """Get construction_with_shading_name.

        Returns:
            str: the value of `construction_with_shading_name` or None if not set

        """
        return self["Construction with Shading Name"]

    @construction_with_shading_name.setter
    def construction_with_shading_name(self, value=None):
        """  Corresponds to IDD field `Construction with Shading Name`
        Required if Shading Type = SwitchableGlazing
        Required if Shading Type = interior or exterior shade or blind, or exterior screen, and
        "Shading Device Material Name" is not specified.
        If both "Construction with Shading Name" and "Shading Device Material Name" are entered,
        the former takes precedence.

        Args:
            value (str): value for IDD Field `Construction with Shading Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Construction with Shading Name"] = value

    @property
    def shading_control_type(self):
        """Get shading_control_type.

        Returns:
            str: the value of `shading_control_type` or None if not set

        """
        return self["Shading Control Type"]

    @shading_control_type.setter
    def shading_control_type(self, value=None):
        """  Corresponds to IDD field `Shading Control Type`
        OnIfScheduleAllows requires that Schedule Name be specified and
        Shading Control Is Scheduled = Yes.
        AlwaysOn, AlwaysOff and OnIfScheduleAllows are the only valid control types for ExteriorScreen.
        The following six control types are used primarily to reduce
        zone cooling load due to window solar gain
        Following entry should be used only if Shading Type = SwitchableGlazing
        and window is in a daylit zone
        The following three control types are used to reduce zone Heating load. They can be
        used with any Shading Type but are most appropriate for opaque interior or exterior
        shades with high insulating value ("opaque movable insulation")
        The following two control types are used to reduce zone heating and cooling load.
        They can be used with any Shading Type but are most appropriate for translucent interior
        or exterior shades with high insulating value ("translucent movable insulation")
        The following two control types are used to reduce zone Cooling load.
        They can be used with any Shading Type but are most appropriate for interior
        or exterior blinds,interior or exterior shades with low insulating value, or
        switchable glazing
        The following four control types require that both Setpoint and Setpoint2 be specified
        Setpoint will correspond to outdoor air temp or zone air temp (deg C)
        Setpoint2 will correspond to solar on window or horizontal solar (W/m2)

        Args:
            value (str): value for IDD Field `Shading Control Type`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Shading Control Type"] = value

    @property
    def schedule_name(self):
        """Get schedule_name.

        Returns:
            str: the value of `schedule_name` or None if not set

        """
        return self["Schedule Name"]

    @schedule_name.setter
    def schedule_name(self, value=None):
        """  Corresponds to IDD field `Schedule Name`
        Required if Shading Control Is Scheduled = Yes.
        If schedule value = 1, shading control is active, i.e., shading can take place only
        if the control test passes. If schedule value = 0, shading is off whether or not
        the control test passes. Schedule Name is required if Shading Control Is Scheduled = Yes.
        If Schedule Name is not specified, shading control is assumed to be active at all times.

        Args:
            value (str): value for IDD Field `Schedule Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Schedule Name"] = value

    @property
    def setpoint(self):
        """Get setpoint.

        Returns:
            float: the value of `setpoint` or None if not set

        """
        return self["Setpoint"]

    @setpoint.setter
    def setpoint(self, value=None):
        """  Corresponds to IDD field `Setpoint`
        W/m2 for solar-based controls, W for cooling- or heating-based controls,
        deg C for temperature-based controls.
        Unused for Shading Control Type = AlwaysOn, AlwaysOff, OnIfScheduleAllows,
        OnIfHighGlare, Glare, and DaylightIlluminance

        Args:
            value (float): value for IDD Field `Setpoint`
                Units: W/m2, W or deg C
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Setpoint"] = value

    @property
    def shading_control_is_scheduled(self):
        """Get shading_control_is_scheduled.

        Returns:
            str: the value of `shading_control_is_scheduled` or None if not set

        """
        return self["Shading Control Is Scheduled"]

    @shading_control_is_scheduled.setter
    def shading_control_is_scheduled(self, value="No"):
        """  Corresponds to IDD field `Shading Control Is Scheduled`
        If Yes, Schedule Name is required; if No, Schedule Name is not used.
        Shading Control Is Scheduled = Yes is required if Shading Control Type = OnIfScheduleAllows.

        Args:
            value (str): value for IDD Field `Shading Control Is Scheduled`
                Default value: No
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Shading Control Is Scheduled"] = value

    @property
    def glare_control_is_active(self):
        """Get glare_control_is_active.

        Returns:
            str: the value of `glare_control_is_active` or None if not set

        """
        return self["Glare Control Is Active"]

    @glare_control_is_active.setter
    def glare_control_is_active(self, value="No"):
        """  Corresponds to IDD field `Glare Control Is Active`
        If Yes and window is in a daylit zone, shading is on if zone's discomfort glare index exceeds
        the maximum discomfort glare index specified in the Daylighting object referenced by the zone.
        The glare test is OR'ed with the test specified by Shading Control Type.
        Glare Control Is Active = Yes is required if Shading Control Type = OnIfHighGlare.

        Args:
            value (str): value for IDD Field `Glare Control Is Active`
                Default value: No
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Glare Control Is Active"] = value

    @property
    def shading_device_material_name(self):
        """Get shading_device_material_name.

        Returns:
            str: the value of `shading_device_material_name` or None if not set

        """
        return self["Shading Device Material Name"]

    @shading_device_material_name.setter
    def shading_device_material_name(self, value=None):
        """  Corresponds to IDD field `Shading Device Material Name`
        Enter the name of a WindowMaterial:Shade, WindowMaterial:Screen or WindowMaterial:Blind object.
        Required if "Construction with Shading Name" is not specified.
        Not used if Shading Control Type = SwitchableGlazing, BetweenGlassShade, or BetweenGlassBlind.
        If both "Construction with Shading Name" and "Shading Device Material Name" are entered,
        the former takes precedence.

        Args:
            value (str): value for IDD Field `Shading Device Material Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Shading Device Material Name"] = value

    @property
    def type_of_slat_angle_control_for_blinds(self):
        """Get type_of_slat_angle_control_for_blinds.

        Returns:
            str: the value of `type_of_slat_angle_control_for_blinds` or None if not set

        """
        return self["Type of Slat Angle Control for Blinds"]

    @type_of_slat_angle_control_for_blinds.setter
    def type_of_slat_angle_control_for_blinds(self, value="FixedSlatAngle"):
        """  Corresponds to IDD field `Type of Slat Angle Control for Blinds`
        Used only if Shading Type = InteriorBlind, ExteriorBlind or BetweenGlassBlind.
        If choice is ScheduledSlatAngle then Slat Angle Schedule Name is required.

        Args:
            value (str): value for IDD Field `Type of Slat Angle Control for Blinds`
                Default value: FixedSlatAngle
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Type of Slat Angle Control for Blinds"] = value

    @property
    def slat_angle_schedule_name(self):
        """Get slat_angle_schedule_name.

        Returns:
            str: the value of `slat_angle_schedule_name` or None if not set

        """
        return self["Slat Angle Schedule Name"]

    @slat_angle_schedule_name.setter
    def slat_angle_schedule_name(self, value=None):
        """  Corresponds to IDD field `Slat Angle Schedule Name`
        Used only if Shading Type = InteriorBlind, ExteriorBlind or BetweenGlassBlind.
        Required if Type of Slat Angle Control for Blinds = ScheduledSlatAngle
        Schedule values should be degrees (0 minimum, 180 maximum)

        Args:
            value (str): value for IDD Field `Slat Angle Schedule Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Slat Angle Schedule Name"] = value

    @property
    def setpoint_2(self):
        """Get setpoint_2.

        Returns:
            float: the value of `setpoint_2` or None if not set

        """
        return self["Setpoint 2"]

    @setpoint_2.setter
    def setpoint_2(self, value=None):
        """  Corresponds to IDD field `Setpoint 2`
        W/m2 for solar-based controls, deg C for temperature-based controls.
        Used only as the second setpoint for the following two-setpoint control types:
        OnIfHighOutdoorAirTempAndHighSolarOnWindow, OnIfHighOutdoorAirTempAndHighHorizontalSolar,
        OnIfHighZoneAirTempAndHighSolarOnWindow, and OnIfHighZoneAirTempAndHighHorizontalSolar

        Args:
            value (float): value for IDD Field `Setpoint 2`
                Units: W/m2 or deg C
                IP-Units: unknown
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Setpoint 2"] = value




class WindowPropertyFrameAndDivider(DataObject):

    """ Corresponds to IDD object `WindowProperty:FrameAndDivider`
        Specifies the dimensions of a window frame, dividers, and inside reveal surfaces.
        Referenced by the surface objects for exterior windows and glass doors
        (ref: FenestrationSurface:Detailed, Window, and GlazedDoor).
    """
    schema = {'extensible-fields': OrderedDict(),
              'fields': OrderedDict([(u'name',
                                      {'name': u'Name',
                                       'pyname': u'name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'alpha'}),
                                     (u'frame width',
                                      {'name': u'Frame Width',
                                       'pyname': u'frame_width',
                                       'default': 0.0,
                                       'maximum': 1.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'm'}),
                                     (u'frame outside projection',
                                      {'name': u'Frame Outside Projection',
                                       'pyname': u'frame_outside_projection',
                                       'default': 0.0,
                                       'maximum': 0.5,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'm'}),
                                     (u'frame inside projection',
                                      {'name': u'Frame Inside Projection',
                                       'pyname': u'frame_inside_projection',
                                       'default': 0.0,
                                       'maximum': 0.5,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'm'}),
                                     (u'frame conductance',
                                      {'name': u'Frame Conductance',
                                       'pyname': u'frame_conductance',
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'W/m2-K'}),
                                     (u'ratio of frame-edge glass conductance to center-of-glass conductance',
                                      {'name': u'Ratio of Frame-Edge Glass Conductance to Center-Of-Glass Conductance',
                                       'pyname': u'ratio_of_frameedge_glass_conductance_to_centerofglass_conductance',
                                       'default': 1.0,
                                       'minimum>': 0.0,
                                       'maximum': 4.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'frame solar absorptance',
                                      {'name': u'Frame Solar Absorptance',
                                       'pyname': u'frame_solar_absorptance',
                                       'default': 0.7,
                                       'maximum': 1.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'frame visible absorptance',
                                      {'name': u'Frame Visible Absorptance',
                                       'pyname': u'frame_visible_absorptance',
                                       'default': 0.7,
                                       'maximum': 1.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'frame thermal hemispherical emissivity',
                                      {'name': u'Frame Thermal Hemispherical Emissivity',
                                       'pyname': u'frame_thermal_hemispherical_emissivity',
                                       'default': 0.9,
                                       'minimum>': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'divider type',
                                      {'name': u'Divider Type',
                                       'pyname': u'divider_type',
                                       'default': u'DividedLite',
                                       'required-field': True,
                                       'autosizable': False,
                                       'accepted-values': [u'DividedLite',
                                                           u'Suspended'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'divider width',
                                      {'name': u'Divider Width',
                                       'pyname': u'divider_width',
                                       'default': 0.0,
                                       'maximum': 0.5,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'm'}),
                                     (u'number of horizontal dividers',
                                      {'name': u'Number of Horizontal Dividers',
                                       'pyname': u'number_of_horizontal_dividers',
                                       'default': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'number of vertical dividers',
                                      {'name': u'Number of Vertical Dividers',
                                       'pyname': u'number_of_vertical_dividers',
                                       'default': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'divider outside projection',
                                      {'name': u'Divider Outside Projection',
                                       'pyname': u'divider_outside_projection',
                                       'default': 0.0,
                                       'maximum': 0.5,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'm'}),
                                     (u'divider inside projection',
                                      {'name': u'Divider Inside Projection',
                                       'pyname': u'divider_inside_projection',
                                       'default': 0.0,
                                       'maximum': 0.5,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'm'}),
                                     (u'divider conductance',
                                      {'name': u'Divider Conductance',
                                       'pyname': u'divider_conductance',
                                       'default': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'W/m2-K'}),
                                     (u'ratio of divider-edge glass conductance to center-of-glass conductance',
                                      {'name': u'Ratio of Divider-Edge Glass Conductance to Center-Of-Glass Conductance',
                                       'pyname': u'ratio_of_divideredge_glass_conductance_to_centerofglass_conductance',
                                       'default': 1.0,
                                       'minimum>': 0.0,
                                       'maximum': 4.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'divider solar absorptance',
                                      {'name': u'Divider Solar Absorptance',
                                       'pyname': u'divider_solar_absorptance',
                                       'default': 0.0,
                                       'maximum': 1.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'divider visible absorptance',
                                      {'name': u'Divider Visible Absorptance',
                                       'pyname': u'divider_visible_absorptance',
                                       'default': 0.0,
                                       'maximum': 1.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'divider thermal hemispherical emissivity',
                                      {'name': u'Divider Thermal Hemispherical Emissivity',
                                       'pyname': u'divider_thermal_hemispherical_emissivity',
                                       'default': 0.9,
                                       'minimum>': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'maximum<': 1.0}),
                                     (u'outside reveal solar absorptance',
                                      {'name': u'Outside Reveal Solar Absorptance',
                                       'pyname': u'outside_reveal_solar_absorptance',
                                       'default': 0.0,
                                       'maximum': 1.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'inside sill depth',
                                      {'name': u'Inside Sill Depth',
                                       'pyname': u'inside_sill_depth',
                                       'default': 0.0,
                                       'maximum': 2.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'm'}),
                                     (u'inside sill solar absorptance',
                                      {'name': u'Inside Sill Solar Absorptance',
                                       'pyname': u'inside_sill_solar_absorptance',
                                       'default': 0.0,
                                       'maximum': 1.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'inside reveal depth',
                                      {'name': u'Inside Reveal Depth',
                                       'pyname': u'inside_reveal_depth',
                                       'default': 0.0,
                                       'maximum': 2.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'inside reveal solar absorptance',
                                      {'name': u'Inside Reveal Solar Absorptance',
                                       'pyname': u'inside_reveal_solar_absorptance',
                                       'default': 0.0,
                                       'maximum': 1.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': u'real'})]),
              'format': None,
              'group': u'Thermal Zones and Surfaces',
              'min-fields': 20,
              'name': u'WindowProperty:FrameAndDivider',
              'pyname': u'WindowPropertyFrameAndDivider',
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
        """Corresponds to IDD field `Name` Referenced by surfaces that are
        exterior windows Not used by interzone windows.

        Args:
            value (str): value for IDD Field `Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Name"] = value

    @property
    def frame_width(self):
        """Get frame_width.

        Returns:
            float: the value of `frame_width` or None if not set

        """
        return self["Frame Width"]

    @frame_width.setter
    def frame_width(self, value=None):
        """Corresponds to IDD field `Frame Width` Width of frame in plane of
        window Frame width assumed the same on all sides of window.

        Args:
            value (float): value for IDD Field `Frame Width`
                Units: m
                value <= 1.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Frame Width"] = value

    @property
    def frame_outside_projection(self):
        """Get frame_outside_projection.

        Returns:
            float: the value of `frame_outside_projection` or None if not set

        """
        return self["Frame Outside Projection"]

    @frame_outside_projection.setter
    def frame_outside_projection(self, value=None):
        """Corresponds to IDD field `Frame Outside Projection` Amount that
        frame projects outward from the outside face of the glazing.

        Args:
            value (float): value for IDD Field `Frame Outside Projection`
                Units: m
                value <= 0.5
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Frame Outside Projection"] = value

    @property
    def frame_inside_projection(self):
        """Get frame_inside_projection.

        Returns:
            float: the value of `frame_inside_projection` or None if not set

        """
        return self["Frame Inside Projection"]

    @frame_inside_projection.setter
    def frame_inside_projection(self, value=None):
        """Corresponds to IDD field `Frame Inside Projection` Amount that frame
        projects inward from the inside face of the glazing.

        Args:
            value (float): value for IDD Field `Frame Inside Projection`
                Units: m
                value <= 0.5
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Frame Inside Projection"] = value

    @property
    def frame_conductance(self):
        """Get frame_conductance.

        Returns:
            float: the value of `frame_conductance` or None if not set

        """
        return self["Frame Conductance"]

    @frame_conductance.setter
    def frame_conductance(self, value=None):
        """  Corresponds to IDD field `Frame Conductance`
        Effective conductance of frame
        Excludes air films
        Obtained from WINDOW 5 or other 2-D calculation

        Args:
            value (float): value for IDD Field `Frame Conductance`
                Units: W/m2-K
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Frame Conductance"] = value

    @property
    def ratio_of_frameedge_glass_conductance_to_centerofglass_conductance(
            self):
        """Get
        ratio_of_frameedge_glass_conductance_to_centerofglass_conductance.

        Returns:
            float: the value of `ratio_of_frameedge_glass_conductance_to_centerofglass_conductance` or None if not set

        """
        return self[
            "Ratio of Frame-Edge Glass Conductance to Center-Of-Glass Conductance"]

    @ratio_of_frameedge_glass_conductance_to_centerofglass_conductance.setter
    def ratio_of_frameedge_glass_conductance_to_centerofglass_conductance(
            self,
            value=1.0):
        """  Corresponds to IDD field `Ratio of Frame-Edge Glass Conductance to Center-Of-Glass Conductance`
        Excludes air films; applies only to multipane windows
        Obtained from WINDOW 5 or other 2-D calculation

        Args:
            value (float): value for IDD Field `Ratio of Frame-Edge Glass Conductance to Center-Of-Glass Conductance`
                Default value: 1.0
                value <= 4.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self[
            "Ratio of Frame-Edge Glass Conductance to Center-Of-Glass Conductance"] = value

    @property
    def frame_solar_absorptance(self):
        """Get frame_solar_absorptance.

        Returns:
            float: the value of `frame_solar_absorptance` or None if not set

        """
        return self["Frame Solar Absorptance"]

    @frame_solar_absorptance.setter
    def frame_solar_absorptance(self, value=0.7):
        """Corresponds to IDD field `Frame Solar Absorptance` Assumed same on
        outside and inside of frame.

        Args:
            value (float): value for IDD Field `Frame Solar Absorptance`
                Default value: 0.7
                value <= 1.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Frame Solar Absorptance"] = value

    @property
    def frame_visible_absorptance(self):
        """Get frame_visible_absorptance.

        Returns:
            float: the value of `frame_visible_absorptance` or None if not set

        """
        return self["Frame Visible Absorptance"]

    @frame_visible_absorptance.setter
    def frame_visible_absorptance(self, value=0.7):
        """Corresponds to IDD field `Frame Visible Absorptance` Assumed same on
        outside and inside of frame.

        Args:
            value (float): value for IDD Field `Frame Visible Absorptance`
                Default value: 0.7
                value <= 1.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Frame Visible Absorptance"] = value

    @property
    def frame_thermal_hemispherical_emissivity(self):
        """Get frame_thermal_hemispherical_emissivity.

        Returns:
            float: the value of `frame_thermal_hemispherical_emissivity` or None if not set

        """
        return self["Frame Thermal Hemispherical Emissivity"]

    @frame_thermal_hemispherical_emissivity.setter
    def frame_thermal_hemispherical_emissivity(self, value=0.9):
        """Corresponds to IDD field `Frame Thermal Hemispherical Emissivity`
        Assumed same on outside and inside of frame.

        Args:
            value (float): value for IDD Field `Frame Thermal Hemispherical Emissivity`
                Default value: 0.9
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Frame Thermal Hemispherical Emissivity"] = value

    @property
    def divider_type(self):
        """Get divider_type.

        Returns:
            str: the value of `divider_type` or None if not set

        """
        return self["Divider Type"]

    @divider_type.setter
    def divider_type(self, value="DividedLite"):
        """Corresponds to IDD field `Divider Type`

        Args:
            value (str): value for IDD Field `Divider Type`
                Default value: DividedLite
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Divider Type"] = value

    @property
    def divider_width(self):
        """Get divider_width.

        Returns:
            float: the value of `divider_width` or None if not set

        """
        return self["Divider Width"]

    @divider_width.setter
    def divider_width(self, value=None):
        """Corresponds to IDD field `Divider Width` Width of dividers in plane
        of window Width assumed the same for all dividers.

        Args:
            value (float): value for IDD Field `Divider Width`
                Units: m
                value <= 0.5
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Divider Width"] = value

    @property
    def number_of_horizontal_dividers(self):
        """Get number_of_horizontal_dividers.

        Returns:
            float: the value of `number_of_horizontal_dividers` or None if not set

        """
        return self["Number of Horizontal Dividers"]

    @number_of_horizontal_dividers.setter
    def number_of_horizontal_dividers(self, value=None):
        """  Corresponds to IDD field `Number of Horizontal Dividers`
        "Horizontal" means parallel to local window X-axis

        Args:
            value (float): value for IDD Field `Number of Horizontal Dividers`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Number of Horizontal Dividers"] = value

    @property
    def number_of_vertical_dividers(self):
        """Get number_of_vertical_dividers.

        Returns:
            float: the value of `number_of_vertical_dividers` or None if not set

        """
        return self["Number of Vertical Dividers"]

    @number_of_vertical_dividers.setter
    def number_of_vertical_dividers(self, value=None):
        """  Corresponds to IDD field `Number of Vertical Dividers`
        "Vertical" means parallel to local window Y-axis

        Args:
            value (float): value for IDD Field `Number of Vertical Dividers`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Number of Vertical Dividers"] = value

    @property
    def divider_outside_projection(self):
        """Get divider_outside_projection.

        Returns:
            float: the value of `divider_outside_projection` or None if not set

        """
        return self["Divider Outside Projection"]

    @divider_outside_projection.setter
    def divider_outside_projection(self, value=None):
        """Corresponds to IDD field `Divider Outside Projection` Amount that
        divider projects outward from the outside face of the glazing Outside
        projection assumed the same for all divider elements.

        Args:
            value (float): value for IDD Field `Divider Outside Projection`
                Units: m
                value <= 0.5
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Divider Outside Projection"] = value

    @property
    def divider_inside_projection(self):
        """Get divider_inside_projection.

        Returns:
            float: the value of `divider_inside_projection` or None if not set

        """
        return self["Divider Inside Projection"]

    @divider_inside_projection.setter
    def divider_inside_projection(self, value=None):
        """Corresponds to IDD field `Divider Inside Projection` Amount that
        divider projects inward from the inside face of the glazing Inside
        projection assumed the same for all divider elements.

        Args:
            value (float): value for IDD Field `Divider Inside Projection`
                Units: m
                value <= 0.5
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Divider Inside Projection"] = value

    @property
    def divider_conductance(self):
        """Get divider_conductance.

        Returns:
            float: the value of `divider_conductance` or None if not set

        """
        return self["Divider Conductance"]

    @divider_conductance.setter
    def divider_conductance(self, value=None):
        """  Corresponds to IDD field `Divider Conductance`
        Effective conductance of divider
        Excludes air films
        Obtained from WINDOW 5 or other 2-D calculation

        Args:
            value (float): value for IDD Field `Divider Conductance`
                Units: W/m2-K
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Divider Conductance"] = value

    @property
    def ratio_of_divideredge_glass_conductance_to_centerofglass_conductance(
            self):
        """Get
        ratio_of_divideredge_glass_conductance_to_centerofglass_conductance.

        Returns:
            float: the value of `ratio_of_divideredge_glass_conductance_to_centerofglass_conductance` or None if not set

        """
        return self[
            "Ratio of Divider-Edge Glass Conductance to Center-Of-Glass Conductance"]

    @ratio_of_divideredge_glass_conductance_to_centerofglass_conductance.setter
    def ratio_of_divideredge_glass_conductance_to_centerofglass_conductance(
            self,
            value=1.0):
        """  Corresponds to IDD field `Ratio of Divider-Edge Glass Conductance to Center-Of-Glass Conductance`
        Excludes air films
        Obtained from WINDOW 5 or other 2-D calculation

        Args:
            value (float): value for IDD Field `Ratio of Divider-Edge Glass Conductance to Center-Of-Glass Conductance`
                Default value: 1.0
                value <= 4.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self[
            "Ratio of Divider-Edge Glass Conductance to Center-Of-Glass Conductance"] = value

    @property
    def divider_solar_absorptance(self):
        """Get divider_solar_absorptance.

        Returns:
            float: the value of `divider_solar_absorptance` or None if not set

        """
        return self["Divider Solar Absorptance"]

    @divider_solar_absorptance.setter
    def divider_solar_absorptance(self, value=None):
        """Corresponds to IDD field `Divider Solar Absorptance` Assumed same on
        outside and inside of divider.

        Args:
            value (float): value for IDD Field `Divider Solar Absorptance`
                value <= 1.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Divider Solar Absorptance"] = value

    @property
    def divider_visible_absorptance(self):
        """Get divider_visible_absorptance.

        Returns:
            float: the value of `divider_visible_absorptance` or None if not set

        """
        return self["Divider Visible Absorptance"]

    @divider_visible_absorptance.setter
    def divider_visible_absorptance(self, value=None):
        """Corresponds to IDD field `Divider Visible Absorptance` Assumed same
        on outside and inside of divider.

        Args:
            value (float): value for IDD Field `Divider Visible Absorptance`
                value <= 1.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Divider Visible Absorptance"] = value

    @property
    def divider_thermal_hemispherical_emissivity(self):
        """Get divider_thermal_hemispherical_emissivity.

        Returns:
            float: the value of `divider_thermal_hemispherical_emissivity` or None if not set

        """
        return self["Divider Thermal Hemispherical Emissivity"]

    @divider_thermal_hemispherical_emissivity.setter
    def divider_thermal_hemispherical_emissivity(self, value=0.9):
        """Corresponds to IDD field `Divider Thermal Hemispherical Emissivity`
        Assumed same on outside and inside of divider.

        Args:
            value (float): value for IDD Field `Divider Thermal Hemispherical Emissivity`
                Default value: 0.9
                value < 1.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Divider Thermal Hemispherical Emissivity"] = value

    @property
    def outside_reveal_solar_absorptance(self):
        """Get outside_reveal_solar_absorptance.

        Returns:
            float: the value of `outside_reveal_solar_absorptance` or None if not set

        """
        return self["Outside Reveal Solar Absorptance"]

    @outside_reveal_solar_absorptance.setter
    def outside_reveal_solar_absorptance(self, value=None):
        """Corresponds to IDD field `Outside Reveal Solar Absorptance`

        Args:
            value (float): value for IDD Field `Outside Reveal Solar Absorptance`
                value <= 1.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Outside Reveal Solar Absorptance"] = value

    @property
    def inside_sill_depth(self):
        """Get inside_sill_depth.

        Returns:
            float: the value of `inside_sill_depth` or None if not set

        """
        return self["Inside Sill Depth"]

    @inside_sill_depth.setter
    def inside_sill_depth(self, value=None):
        """Corresponds to IDD field `Inside Sill Depth`

        Args:
            value (float): value for IDD Field `Inside Sill Depth`
                Units: m
                value <= 2.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Inside Sill Depth"] = value

    @property
    def inside_sill_solar_absorptance(self):
        """Get inside_sill_solar_absorptance.

        Returns:
            float: the value of `inside_sill_solar_absorptance` or None if not set

        """
        return self["Inside Sill Solar Absorptance"]

    @inside_sill_solar_absorptance.setter
    def inside_sill_solar_absorptance(self, value=None):
        """Corresponds to IDD field `Inside Sill Solar Absorptance`

        Args:
            value (float): value for IDD Field `Inside Sill Solar Absorptance`
                value <= 1.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Inside Sill Solar Absorptance"] = value

    @property
    def inside_reveal_depth(self):
        """Get inside_reveal_depth.

        Returns:
            float: the value of `inside_reveal_depth` or None if not set

        """
        return self["Inside Reveal Depth"]

    @inside_reveal_depth.setter
    def inside_reveal_depth(self, value=None):
        """  Corresponds to IDD field `Inside Reveal Depth`
        Distance from plane of inside surface of glazing
        to plane of inside surface of wall.
        Outside reveal depth is determined from the geometry
        of the window and the wall it is on; it is non-zero if the plane of
        the outside surface of the glazing is set back from the plane of the
        outside surface of the wall.

        Args:
            value (float): value for IDD Field `Inside Reveal Depth`
                Units: m
                value <= 2.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Inside Reveal Depth"] = value

    @property
    def inside_reveal_solar_absorptance(self):
        """Get inside_reveal_solar_absorptance.

        Returns:
            float: the value of `inside_reveal_solar_absorptance` or None if not set

        """
        return self["Inside Reveal Solar Absorptance"]

    @inside_reveal_solar_absorptance.setter
    def inside_reveal_solar_absorptance(self, value=None):
        """Corresponds to IDD field `Inside Reveal Solar Absorptance`

        Args:
            value (float): value for IDD Field `Inside Reveal Solar Absorptance`
                value <= 1.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Inside Reveal Solar Absorptance"] = value




class WindowPropertyAirflowControl(DataObject):

    """ Corresponds to IDD object `WindowProperty:AirflowControl`
        Used to control forced airflow through a gap between glass layers
    """
    schema = {'extensible-fields': OrderedDict(),
              'fields': OrderedDict([(u'name',
                                      {'name': u'Name',
                                       'pyname': u'name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'airflow source',
                                      {'name': u'Airflow Source',
                                       'pyname': u'airflow_source',
                                       'default': u'IndoorAir',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'IndoorAir',
                                                           u'OutdoorAir'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'airflow destination',
                                      {'name': u'Airflow Destination',
                                       'pyname': u'airflow_destination',
                                       'default': u'OutdoorAir',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'IndoorAir',
                                                           u'OutdoorAir',
                                                           u'ReturnAir'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'maximum flow rate',
                                      {'name': u'Maximum Flow Rate',
                                       'pyname': u'maximum_flow_rate',
                                       'default': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm3/s-m'}),
                                     (u'airflow control type',
                                      {'name': u'Airflow Control Type',
                                       'pyname': u'airflow_control_type',
                                       'default': u'AlwaysOnAtMaximumFlow',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'AlwaysOnAtMaximumFlow',
                                                           u'AlwaysOff',
                                                           u'ScheduledOnly'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'airflow is scheduled',
                                      {'name': u'Airflow Is Scheduled',
                                       'pyname': u'airflow_is_scheduled',
                                       'default': u'No',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'Yes',
                                                           u'No'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'airflow multiplier schedule name',
                                      {'name': u'Airflow Multiplier Schedule Name',
                                       'pyname': u'airflow_multiplier_schedule_name',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'})]),
              'format': None,
              'group': u'Thermal Zones and Surfaces',
              'min-fields': 7,
              'name': u'WindowProperty:AirflowControl',
              'pyname': u'WindowPropertyAirflowControl',
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
        """Corresponds to IDD field `Name` Name must be that of an exterior
        window with two or three glass layers.

        Args:
            value (str): value for IDD Field `Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Name"] = value

    @property
    def airflow_source(self):
        """Get airflow_source.

        Returns:
            str: the value of `airflow_source` or None if not set

        """
        return self["Airflow Source"]

    @airflow_source.setter
    def airflow_source(self, value="IndoorAir"):
        """Corresponds to IDD field `Airflow Source`

        Args:
            value (str): value for IDD Field `Airflow Source`
                Default value: IndoorAir
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Airflow Source"] = value

    @property
    def airflow_destination(self):
        """Get airflow_destination.

        Returns:
            str: the value of `airflow_destination` or None if not set

        """
        return self["Airflow Destination"]

    @airflow_destination.setter
    def airflow_destination(self, value="OutdoorAir"):
        """Corresponds to IDD field `Airflow Destination`

        Args:
            value (str): value for IDD Field `Airflow Destination`
                Default value: OutdoorAir
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Airflow Destination"] = value

    @property
    def maximum_flow_rate(self):
        """Get maximum_flow_rate.

        Returns:
            float: the value of `maximum_flow_rate` or None if not set

        """
        return self["Maximum Flow Rate"]

    @maximum_flow_rate.setter
    def maximum_flow_rate(self, value=None):
        """Corresponds to IDD field `Maximum Flow Rate` Above is m3/s per m of
        glazing width.

        Args:
            value (float): value for IDD Field `Maximum Flow Rate`
                Units: m3/s-m
                IP-Units: ft3/min-ft
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Maximum Flow Rate"] = value

    @property
    def airflow_control_type(self):
        """Get airflow_control_type.

        Returns:
            str: the value of `airflow_control_type` or None if not set

        """
        return self["Airflow Control Type"]

    @airflow_control_type.setter
    def airflow_control_type(self, value="AlwaysOnAtMaximumFlow"):
        """  Corresponds to IDD field `Airflow Control Type`
        ScheduledOnly requires that Airflow Has Multiplier Schedule Name = Yes
        and that Airflow Multiplier Schedule Name is specified.

        Args:
            value (str): value for IDD Field `Airflow Control Type`
                Default value: AlwaysOnAtMaximumFlow
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Airflow Control Type"] = value

    @property
    def airflow_is_scheduled(self):
        """Get airflow_is_scheduled.

        Returns:
            str: the value of `airflow_is_scheduled` or None if not set

        """
        return self["Airflow Is Scheduled"]

    @airflow_is_scheduled.setter
    def airflow_is_scheduled(self, value="No"):
        """Corresponds to IDD field `Airflow Is Scheduled` If Yes, then Airflow
        Multiplier Schedule Name must be specified.

        Args:
            value (str): value for IDD Field `Airflow Is Scheduled`
                Default value: No
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Airflow Is Scheduled"] = value

    @property
    def airflow_multiplier_schedule_name(self):
        """Get airflow_multiplier_schedule_name.

        Returns:
            str: the value of `airflow_multiplier_schedule_name` or None if not set

        """
        return self["Airflow Multiplier Schedule Name"]

    @airflow_multiplier_schedule_name.setter
    def airflow_multiplier_schedule_name(self, value=None):
        """  Corresponds to IDD field `Airflow Multiplier Schedule Name`
        Required if Airflow Is Scheduled = Yes.
        Schedule values are 0.0 or 1.0 and multiply Maximum Air Flow.

        Args:
            value (str): value for IDD Field `Airflow Multiplier Schedule Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Airflow Multiplier Schedule Name"] = value




class WindowPropertyStormWindow(DataObject):

    """ Corresponds to IDD object `WindowProperty:StormWindow`
        This is a movable exterior glass layer that is usually applied in the winter
        and removed in the summer.
    """
    schema = {'extensible-fields': OrderedDict(),
              'fields': OrderedDict([(u'window name',
                                      {'name': u'Window Name',
                                       'pyname': u'window_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'alpha'}),
                                     (u'storm glass layer name',
                                      {'name': u'Storm Glass Layer Name',
                                       'pyname': u'storm_glass_layer_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'distance between storm glass layer and adjacent glass',
                                      {'name': u'Distance Between Storm Glass Layer and Adjacent Glass',
                                       'pyname': u'distance_between_storm_glass_layer_and_adjacent_glass',
                                       'default': 0.05,
                                       'minimum>': 0.0,
                                       'maximum': 0.5,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'm'}),
                                     (u'month that storm glass layer is put on',
                                      {'name': u'Month that Storm Glass Layer is Put On',
                                       'pyname': u'month_that_storm_glass_layer_is_put_on',
                                       'maximum': 12,
                                       'required-field': True,
                                       'autosizable': False,
                                       'minimum': 1,
                                       'autocalculatable': False,
                                       'type': u'integer'}),
                                     (u'day of month that storm glass layer is put on',
                                      {'name': u'Day of Month that Storm Glass Layer is Put On',
                                       'pyname': u'day_of_month_that_storm_glass_layer_is_put_on',
                                       'maximum': 31,
                                       'required-field': True,
                                       'autosizable': False,
                                       'minimum': 1,
                                       'autocalculatable': False,
                                       'type': u'integer'}),
                                     (u'month that storm glass layer is taken off',
                                      {'name': u'Month that Storm Glass Layer is Taken Off',
                                       'pyname': u'month_that_storm_glass_layer_is_taken_off',
                                       'maximum': 12,
                                       'required-field': True,
                                       'autosizable': False,
                                       'minimum': 1,
                                       'autocalculatable': False,
                                       'type': u'integer'}),
                                     (u'day of month that storm glass layer is taken off',
                                      {'name': u'Day of Month that Storm Glass Layer is Taken Off',
                                       'pyname': u'day_of_month_that_storm_glass_layer_is_taken_off',
                                       'maximum': 31,
                                       'required-field': True,
                                       'autosizable': False,
                                       'minimum': 1,
                                       'autocalculatable': False,
                                       'type': u'integer'})]),
              'format': None,
              'group': u'Thermal Zones and Surfaces',
              'min-fields': 7,
              'name': u'WindowProperty:StormWindow',
              'pyname': u'WindowPropertyStormWindow',
              'required-object': False,
              'unique-object': False}

    @property
    def window_name(self):
        """Get window_name.

        Returns:
            str: the value of `window_name` or None if not set

        """
        return self["Window Name"]

    @window_name.setter
    def window_name(self, value=None):
        """  Corresponds to IDD field `Window Name`
        Must be the name of a FenestrationSurface:Detailed object with Surface Type = WINDOW.
        The WindowProperty:StormWindow object can only be used with exterior windows.

        Args:
            value (str): value for IDD Field `Window Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Window Name"] = value

    @property
    def storm_glass_layer_name(self):
        """Get storm_glass_layer_name.

        Returns:
            str: the value of `storm_glass_layer_name` or None if not set

        """
        return self["Storm Glass Layer Name"]

    @storm_glass_layer_name.setter
    def storm_glass_layer_name(self, value=None):
        """  Corresponds to IDD field `Storm Glass Layer Name`
        Must be a WindowMaterial:Glazing or WindowMaterial:Glazing:RefractionExtinctionMethod
        Gap between storm glass layer and adjacent glass layer is assumed to be filled
        with Air

        Args:
            value (str): value for IDD Field `Storm Glass Layer Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Storm Glass Layer Name"] = value

    @property
    def distance_between_storm_glass_layer_and_adjacent_glass(self):
        """Get distance_between_storm_glass_layer_and_adjacent_glass.

        Returns:
            float: the value of `distance_between_storm_glass_layer_and_adjacent_glass` or None if not set

        """
        return self["Distance Between Storm Glass Layer and Adjacent Glass"]

    @distance_between_storm_glass_layer_and_adjacent_glass.setter
    def distance_between_storm_glass_layer_and_adjacent_glass(
            self,
            value=0.05):
        """Corresponds to IDD field `Distance Between Storm Glass Layer and
        Adjacent Glass`

        Args:
            value (float): value for IDD Field `Distance Between Storm Glass Layer and Adjacent Glass`
                Units: m
                Default value: 0.05
                value <= 0.5
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Distance Between Storm Glass Layer and Adjacent Glass"] = value

    @property
    def month_that_storm_glass_layer_is_put_on(self):
        """Get month_that_storm_glass_layer_is_put_on.

        Returns:
            int: the value of `month_that_storm_glass_layer_is_put_on` or None if not set

        """
        return self["Month that Storm Glass Layer is Put On"]

    @month_that_storm_glass_layer_is_put_on.setter
    def month_that_storm_glass_layer_is_put_on(self, value=None):
        """Corresponds to IDD field `Month that Storm Glass Layer is Put On`

        Args:
            value (int): value for IDD Field `Month that Storm Glass Layer is Put On`
                value >= 1
                value <= 12
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Month that Storm Glass Layer is Put On"] = value

    @property
    def day_of_month_that_storm_glass_layer_is_put_on(self):
        """Get day_of_month_that_storm_glass_layer_is_put_on.

        Returns:
            int: the value of `day_of_month_that_storm_glass_layer_is_put_on` or None if not set

        """
        return self["Day of Month that Storm Glass Layer is Put On"]

    @day_of_month_that_storm_glass_layer_is_put_on.setter
    def day_of_month_that_storm_glass_layer_is_put_on(self, value=None):
        """Corresponds to IDD field `Day of Month that Storm Glass Layer is Put
        On`

        Args:
            value (int): value for IDD Field `Day of Month that Storm Glass Layer is Put On`
                value >= 1
                value <= 31
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Day of Month that Storm Glass Layer is Put On"] = value

    @property
    def month_that_storm_glass_layer_is_taken_off(self):
        """Get month_that_storm_glass_layer_is_taken_off.

        Returns:
            int: the value of `month_that_storm_glass_layer_is_taken_off` or None if not set

        """
        return self["Month that Storm Glass Layer is Taken Off"]

    @month_that_storm_glass_layer_is_taken_off.setter
    def month_that_storm_glass_layer_is_taken_off(self, value=None):
        """Corresponds to IDD field `Month that Storm Glass Layer is Taken Off`

        Args:
            value (int): value for IDD Field `Month that Storm Glass Layer is Taken Off`
                value >= 1
                value <= 12
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Month that Storm Glass Layer is Taken Off"] = value

    @property
    def day_of_month_that_storm_glass_layer_is_taken_off(self):
        """Get day_of_month_that_storm_glass_layer_is_taken_off.

        Returns:
            int: the value of `day_of_month_that_storm_glass_layer_is_taken_off` or None if not set

        """
        return self["Day of Month that Storm Glass Layer is Taken Off"]

    @day_of_month_that_storm_glass_layer_is_taken_off.setter
    def day_of_month_that_storm_glass_layer_is_taken_off(self, value=None):
        """Corresponds to IDD field `Day of Month that Storm Glass Layer is
        Taken Off`

        Args:
            value (int): value for IDD Field `Day of Month that Storm Glass Layer is Taken Off`
                value >= 1
                value <= 31
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Day of Month that Storm Glass Layer is Taken Off"] = value




class InternalMass(DataObject):

    """Corresponds to IDD object `InternalMass` Used to describe internal zone
    surface area that does not need to be part of geometric representation.

    This should be the total surface area exposed to the zone air.

    """
    schema = {'extensible-fields': OrderedDict(),
              'fields': OrderedDict([(u'name',
                                      {'name': u'Name',
                                       'pyname': u'name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'alpha'}),
                                     (u'construction name',
                                      {'name': u'Construction Name',
                                       'pyname': u'construction_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'zone name',
                                      {'name': u'Zone Name',
                                       'pyname': u'zone_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'surface area',
                                      {'name': u'Surface Area',
                                       'pyname': u'surface_area',
                                       'minimum>': 0.0,
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm2'})]),
              'format': None,
              'group': u'Thermal Zones and Surfaces',
              'min-fields': 0,
              'name': u'InternalMass',
              'pyname': u'InternalMass',
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
        """Corresponds to IDD field `Construction Name` To be matched with a
        construction in this input file.

        Args:
            value (str): value for IDD Field `Construction Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Construction Name"] = value

    @property
    def zone_name(self):
        """Get zone_name.

        Returns:
            str: the value of `zone_name` or None if not set

        """
        return self["Zone Name"]

    @zone_name.setter
    def zone_name(self, value=None):
        """Corresponds to IDD field `Zone Name` Zone the surface is a part of
        used to be Interior Environment.

        Args:
            value (str): value for IDD Field `Zone Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Zone Name"] = value

    @property
    def surface_area(self):
        """Get surface_area.

        Returns:
            float: the value of `surface_area` or None if not set

        """
        return self["Surface Area"]

    @surface_area.setter
    def surface_area(self, value=None):
        """Corresponds to IDD field `Surface Area`

        Args:
            value (float): value for IDD Field `Surface Area`
                Units: m2
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Surface Area"] = value




class ShadingSite(DataObject):

    """ Corresponds to IDD object `Shading:Site`
        used for shading elements such as trees
        these items are fixed in space and would not move with relative geometry
    """
    schema = {'extensible-fields': OrderedDict(),
              'fields': OrderedDict([(u'name',
                                      {'name': u'Name',
                                       'pyname': u'name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'alpha'}),
                                     (u'azimuth angle',
                                      {'name': u'Azimuth Angle',
                                       'pyname': u'azimuth_angle',
                                       'maximum': 360.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'deg'}),
                                     (u'tilt angle',
                                      {'name': u'Tilt Angle',
                                       'pyname': u'tilt_angle',
                                       'default': 90.0,
                                       'maximum': 180.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'deg'}),
                                     (u'starting x coordinate',
                                      {'name': u'Starting X Coordinate',
                                       'pyname': u'starting_x_coordinate',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'starting y coordinate',
                                      {'name': u'Starting Y Coordinate',
                                       'pyname': u'starting_y_coordinate',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'starting z coordinate',
                                      {'name': u'Starting Z Coordinate',
                                       'pyname': u'starting_z_coordinate',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'length',
                                      {'name': u'Length',
                                       'pyname': u'length',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'height',
                                      {'name': u'Height',
                                       'pyname': u'height',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'})]),
              'format': None,
              'group': u'Thermal Zones and Surfaces',
              'min-fields': 0,
              'name': u'Shading:Site',
              'pyname': u'ShadingSite',
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
    def azimuth_angle(self):
        """Get azimuth_angle.

        Returns:
            float: the value of `azimuth_angle` or None if not set

        """
        return self["Azimuth Angle"]

    @azimuth_angle.setter
    def azimuth_angle(self, value=None):
        """  Corresponds to IDD field `Azimuth Angle`
        Facing direction of outside of shading device (S=180,N=0,E=90,W=270)

        Args:
            value (float): value for IDD Field `Azimuth Angle`
                Units: deg
                value <= 360.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Azimuth Angle"] = value

    @property
    def tilt_angle(self):
        """Get tilt_angle.

        Returns:
            float: the value of `tilt_angle` or None if not set

        """
        return self["Tilt Angle"]

    @tilt_angle.setter
    def tilt_angle(self, value=90.0):
        """Corresponds to IDD field `Tilt Angle`

        Args:
            value (float): value for IDD Field `Tilt Angle`
                Units: deg
                Default value: 90.0
                value <= 180.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Tilt Angle"] = value

    @property
    def starting_x_coordinate(self):
        """Get starting_x_coordinate.

        Returns:
            float: the value of `starting_x_coordinate` or None if not set

        """
        return self["Starting X Coordinate"]

    @starting_x_coordinate.setter
    def starting_x_coordinate(self, value=None):
        """Corresponds to IDD field `Starting X Coordinate` Starting coordinate
        is the Lower Left Corner of the Shade.

        Args:
            value (float): value for IDD Field `Starting X Coordinate`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Starting X Coordinate"] = value

    @property
    def starting_y_coordinate(self):
        """Get starting_y_coordinate.

        Returns:
            float: the value of `starting_y_coordinate` or None if not set

        """
        return self["Starting Y Coordinate"]

    @starting_y_coordinate.setter
    def starting_y_coordinate(self, value=None):
        """Corresponds to IDD field `Starting Y Coordinate`

        Args:
            value (float): value for IDD Field `Starting Y Coordinate`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Starting Y Coordinate"] = value

    @property
    def starting_z_coordinate(self):
        """Get starting_z_coordinate.

        Returns:
            float: the value of `starting_z_coordinate` or None if not set

        """
        return self["Starting Z Coordinate"]

    @starting_z_coordinate.setter
    def starting_z_coordinate(self, value=None):
        """Corresponds to IDD field `Starting Z Coordinate`

        Args:
            value (float): value for IDD Field `Starting Z Coordinate`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Starting Z Coordinate"] = value

    @property
    def length(self):
        """Get length.

        Returns:
            float: the value of `length` or None if not set

        """
        return self["Length"]

    @length.setter
    def length(self, value=None):
        """Corresponds to IDD field `Length`

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
    def height(self):
        """Get height.

        Returns:
            float: the value of `height` or None if not set

        """
        return self["Height"]

    @height.setter
    def height(self, value=None):
        """Corresponds to IDD field `Height`

        Args:
            value (float): value for IDD Field `Height`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Height"] = value




class ShadingBuilding(DataObject):

    """ Corresponds to IDD object `Shading:Building`
        used for shading elements such as trees, other buildings, parts of this building not being modeled
        these items are relative to the current building and would move with relative geometry
    """
    schema = {'extensible-fields': OrderedDict(),
              'fields': OrderedDict([(u'name',
                                      {'name': u'Name',
                                       'pyname': u'name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'alpha'}),
                                     (u'azimuth angle',
                                      {'name': u'Azimuth Angle',
                                       'pyname': u'azimuth_angle',
                                       'maximum': 360.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'deg'}),
                                     (u'tilt angle',
                                      {'name': u'Tilt Angle',
                                       'pyname': u'tilt_angle',
                                       'default': 90.0,
                                       'maximum': 180.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'deg'}),
                                     (u'starting x coordinate',
                                      {'name': u'Starting X Coordinate',
                                       'pyname': u'starting_x_coordinate',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'starting y coordinate',
                                      {'name': u'Starting Y Coordinate',
                                       'pyname': u'starting_y_coordinate',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'starting z coordinate',
                                      {'name': u'Starting Z Coordinate',
                                       'pyname': u'starting_z_coordinate',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'length',
                                      {'name': u'Length',
                                       'pyname': u'length',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'height',
                                      {'name': u'Height',
                                       'pyname': u'height',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'})]),
              'format': None,
              'group': u'Thermal Zones and Surfaces',
              'min-fields': 0,
              'name': u'Shading:Building',
              'pyname': u'ShadingBuilding',
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
    def azimuth_angle(self):
        """Get azimuth_angle.

        Returns:
            float: the value of `azimuth_angle` or None if not set

        """
        return self["Azimuth Angle"]

    @azimuth_angle.setter
    def azimuth_angle(self, value=None):
        """  Corresponds to IDD field `Azimuth Angle`
        Facing direction of outside of shading device (S=180,N=0,E=90,W=270)

        Args:
            value (float): value for IDD Field `Azimuth Angle`
                Units: deg
                value <= 360.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Azimuth Angle"] = value

    @property
    def tilt_angle(self):
        """Get tilt_angle.

        Returns:
            float: the value of `tilt_angle` or None if not set

        """
        return self["Tilt Angle"]

    @tilt_angle.setter
    def tilt_angle(self, value=90.0):
        """Corresponds to IDD field `Tilt Angle`

        Args:
            value (float): value for IDD Field `Tilt Angle`
                Units: deg
                Default value: 90.0
                value <= 180.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Tilt Angle"] = value

    @property
    def starting_x_coordinate(self):
        """Get starting_x_coordinate.

        Returns:
            float: the value of `starting_x_coordinate` or None if not set

        """
        return self["Starting X Coordinate"]

    @starting_x_coordinate.setter
    def starting_x_coordinate(self, value=None):
        """Corresponds to IDD field `Starting X Coordinate` Starting coordinate
        is the Lower Left Corner of the Shade.

        Args:
            value (float): value for IDD Field `Starting X Coordinate`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Starting X Coordinate"] = value

    @property
    def starting_y_coordinate(self):
        """Get starting_y_coordinate.

        Returns:
            float: the value of `starting_y_coordinate` or None if not set

        """
        return self["Starting Y Coordinate"]

    @starting_y_coordinate.setter
    def starting_y_coordinate(self, value=None):
        """Corresponds to IDD field `Starting Y Coordinate`

        Args:
            value (float): value for IDD Field `Starting Y Coordinate`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Starting Y Coordinate"] = value

    @property
    def starting_z_coordinate(self):
        """Get starting_z_coordinate.

        Returns:
            float: the value of `starting_z_coordinate` or None if not set

        """
        return self["Starting Z Coordinate"]

    @starting_z_coordinate.setter
    def starting_z_coordinate(self, value=None):
        """Corresponds to IDD field `Starting Z Coordinate`

        Args:
            value (float): value for IDD Field `Starting Z Coordinate`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Starting Z Coordinate"] = value

    @property
    def length(self):
        """Get length.

        Returns:
            float: the value of `length` or None if not set

        """
        return self["Length"]

    @length.setter
    def length(self, value=None):
        """Corresponds to IDD field `Length`

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
    def height(self):
        """Get height.

        Returns:
            float: the value of `height` or None if not set

        """
        return self["Height"]

    @height.setter
    def height(self, value=None):
        """Corresponds to IDD field `Height`

        Args:
            value (float): value for IDD Field `Height`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Height"] = value




class ShadingSiteDetailed(DataObject):

    """ Corresponds to IDD object `Shading:Site:Detailed`
        used for shading elements such as trees
        these items are fixed in space and would not move with relative geometry
    """
    schema = {'extensible-fields': OrderedDict([(u'vertex 1 x-coordinate',
                                                 {'name': u'Vertex 1 X-coordinate',
                                                  'pyname': u'vertex_1_xcoordinate',
                                                  'required-field': True,
                                                  'autosizable': False,
                                                  'autocalculatable': False,
                                                  'type': u'real',
                                                  'unit': u'm'}),
                                                (u'vertex 1 y-coordinate',
                                                 {'name': u'Vertex 1 Y-coordinate',
                                                  'pyname': u'vertex_1_ycoordinate',
                                                  'required-field': True,
                                                  'autosizable': False,
                                                  'autocalculatable': False,
                                                  'type': u'real',
                                                  'unit': u'm'}),
                                                (u'vertex 1 z-coordinate',
                                                 {'name': u'Vertex 1 Z-coordinate',
                                                  'pyname': u'vertex_1_zcoordinate',
                                                  'required-field': True,
                                                  'autosizable': False,
                                                  'autocalculatable': False,
                                                  'type': u'real',
                                                  'unit': u'm'})]),
              'fields': OrderedDict([(u'name',
                                      {'name': u'Name',
                                       'pyname': u'name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'alpha'}),
                                     (u'transmittance schedule name',
                                      {'name': u'Transmittance Schedule Name',
                                       'pyname': u'transmittance_schedule_name',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'number of vertices',
                                      {'name': u'Number of Vertices',
                                       'pyname': u'number_of_vertices',
                                       'default': 'autocalculate',
                                       'required-field': True,
                                       'autosizable': False,
                                       'minimum': 3.0,
                                       'autocalculatable': True,
                                       'type': 'real'})]),
              'format': u'vertices',
              'group': u'Thermal Zones and Surfaces',
              'min-fields': 12,
              'name': u'Shading:Site:Detailed',
              'pyname': u'ShadingSiteDetailed',
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
    def transmittance_schedule_name(self):
        """Get transmittance_schedule_name.

        Returns:
            str: the value of `transmittance_schedule_name` or None if not set

        """
        return self["Transmittance Schedule Name"]

    @transmittance_schedule_name.setter
    def transmittance_schedule_name(self, value=None):
        """Corresponds to IDD field `Transmittance Schedule Name` Transmittance
        schedule for the shading device, defaults to zero (always opaque)

        Args:
            value (str): value for IDD Field `Transmittance Schedule Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Transmittance Schedule Name"] = value

    @property
    def number_of_vertices(self):
        """Get number_of_vertices.

        Returns:
            float: the value of `number_of_vertices` or None if not set

        """
        return self["Number of Vertices"]

    @number_of_vertices.setter
    def number_of_vertices(self, value="autocalculate"):
        """  Corresponds to IDD field `Number of Vertices`
        shown with 6 vertex coordinates -- extensible object
        Rules for vertices are given in GlobalGeometryRules coordinates --
        For this object all surface coordinates are in world coordinates.

        Args:
            value (float or "Autocalculate"): value for IDD Field `Number of Vertices`
                Default value: "autocalculate"
                value >= 3.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Number of Vertices"] = value

    def add_extensible(self,
                       vertex_1_xcoordinate=None,
                       vertex_1_ycoordinate=None,
                       vertex_1_zcoordinate=None,
                       ):
        """Add values for extensible fields.

        Args:

            vertex_1_xcoordinate (float): value for IDD Field `Vertex 1 X-coordinate`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

            vertex_1_ycoordinate (float): value for IDD Field `Vertex 1 Y-coordinate`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

            vertex_1_zcoordinate (float): value for IDD Field `Vertex 1 Z-coordinate`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        """
        vals = []
        vertex_1_xcoordinate = self.check_value(
            "Vertex 1 X-coordinate",
            vertex_1_xcoordinate)
        vals.append(vertex_1_xcoordinate)
        vertex_1_ycoordinate = self.check_value(
            "Vertex 1 Y-coordinate",
            vertex_1_ycoordinate)
        vals.append(vertex_1_ycoordinate)
        vertex_1_zcoordinate = self.check_value(
            "Vertex 1 Z-coordinate",
            vertex_1_zcoordinate)
        vals.append(vertex_1_zcoordinate)
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




class ShadingBuildingDetailed(DataObject):

    """ Corresponds to IDD object `Shading:Building:Detailed`
        used for shading elements such as trees, other buildings, parts of this building not being modeled
        these items are relative to the current building and would move with relative geometry
    """
    schema = {'extensible-fields': OrderedDict([(u'vertex 1 x-coordinate',
                                                 {'name': u'Vertex 1 X-coordinate',
                                                  'pyname': u'vertex_1_xcoordinate',
                                                  'required-field': True,
                                                  'autosizable': False,
                                                  'autocalculatable': False,
                                                  'type': u'real',
                                                  'unit': u'm'}),
                                                (u'vertex 1 y-coordinate',
                                                 {'name': u'Vertex 1 Y-coordinate',
                                                  'pyname': u'vertex_1_ycoordinate',
                                                  'required-field': True,
                                                  'autosizable': False,
                                                  'autocalculatable': False,
                                                  'type': u'real',
                                                  'unit': u'm'}),
                                                (u'vertex 1 z-coordinate',
                                                 {'name': u'Vertex 1 Z-coordinate',
                                                  'pyname': u'vertex_1_zcoordinate',
                                                  'required-field': True,
                                                  'autosizable': False,
                                                  'autocalculatable': False,
                                                  'type': u'real',
                                                  'unit': u'm'})]),
              'fields': OrderedDict([(u'name',
                                      {'name': u'Name',
                                       'pyname': u'name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'alpha'}),
                                     (u'transmittance schedule name',
                                      {'name': u'Transmittance Schedule Name',
                                       'pyname': u'transmittance_schedule_name',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'number of vertices',
                                      {'name': u'Number of Vertices',
                                       'pyname': u'number_of_vertices',
                                       'default': 'autocalculate',
                                       'required-field': True,
                                       'autosizable': False,
                                       'minimum': 3.0,
                                       'autocalculatable': True,
                                       'type': 'real'})]),
              'format': u'vertices',
              'group': u'Thermal Zones and Surfaces',
              'min-fields': 12,
              'name': u'Shading:Building:Detailed',
              'pyname': u'ShadingBuildingDetailed',
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
    def transmittance_schedule_name(self):
        """Get transmittance_schedule_name.

        Returns:
            str: the value of `transmittance_schedule_name` or None if not set

        """
        return self["Transmittance Schedule Name"]

    @transmittance_schedule_name.setter
    def transmittance_schedule_name(self, value=None):
        """Corresponds to IDD field `Transmittance Schedule Name` Transmittance
        schedule for the shading device, defaults to zero (always opaque)

        Args:
            value (str): value for IDD Field `Transmittance Schedule Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Transmittance Schedule Name"] = value

    @property
    def number_of_vertices(self):
        """Get number_of_vertices.

        Returns:
            float: the value of `number_of_vertices` or None if not set

        """
        return self["Number of Vertices"]

    @number_of_vertices.setter
    def number_of_vertices(self, value="autocalculate"):
        """  Corresponds to IDD field `Number of Vertices`
        shown with 6 vertex coordinates -- extensible object
        Rules for vertices are given in GlobalGeometryRules coordinates --
        For this object all surface coordinates are relative to the building origin (0,0,0)
        and will rotate with the BUILDING north axis.

        Args:
            value (float or "Autocalculate"): value for IDD Field `Number of Vertices`
                Default value: "autocalculate"
                value >= 3.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Number of Vertices"] = value

    def add_extensible(self,
                       vertex_1_xcoordinate=None,
                       vertex_1_ycoordinate=None,
                       vertex_1_zcoordinate=None,
                       ):
        """Add values for extensible fields.

        Args:

            vertex_1_xcoordinate (float): value for IDD Field `Vertex 1 X-coordinate`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

            vertex_1_ycoordinate (float): value for IDD Field `Vertex 1 Y-coordinate`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

            vertex_1_zcoordinate (float): value for IDD Field `Vertex 1 Z-coordinate`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        """
        vals = []
        vertex_1_xcoordinate = self.check_value(
            "Vertex 1 X-coordinate",
            vertex_1_xcoordinate)
        vals.append(vertex_1_xcoordinate)
        vertex_1_ycoordinate = self.check_value(
            "Vertex 1 Y-coordinate",
            vertex_1_ycoordinate)
        vals.append(vertex_1_ycoordinate)
        vertex_1_zcoordinate = self.check_value(
            "Vertex 1 Z-coordinate",
            vertex_1_zcoordinate)
        vals.append(vertex_1_zcoordinate)
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




class ShadingOverhang(DataObject):

    """ Corresponds to IDD object `Shading:Overhang`
        Overhangs are usually flat shading surfaces that reference a window or door.
    """
    schema = {'extensible-fields': OrderedDict(),
              'fields': OrderedDict([(u'name',
                                      {'name': u'Name',
                                       'pyname': u'name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'alpha'}),
                                     (u'window or door name',
                                      {'name': u'Window or Door Name',
                                       'pyname': u'window_or_door_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'height above window or door',
                                      {'name': u'Height above Window or Door',
                                       'pyname': u'height_above_window_or_door',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'tilt angle from window/door',
                                      {'name': u'Tilt Angle from Window/Door',
                                       'pyname': u'tilt_angle_from_window_or_door',
                                       'default': 90.0,
                                       'maximum': 180.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'deg'}),
                                     (u'left extension from window/door width',
                                      {'name': u'Left extension from Window/Door Width',
                                       'pyname': u'left_extension_from_window_or_door_width',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'right extension from window/door width',
                                      {'name': u'Right extension from Window/Door Width',
                                       'pyname': u'right_extension_from_window_or_door_width',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'depth',
                                      {'name': u'Depth',
                                       'pyname': u'depth',
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'})]),
              'format': None,
              'group': u'Thermal Zones and Surfaces',
              'min-fields': 0,
              'name': u'Shading:Overhang',
              'pyname': u'ShadingOverhang',
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
    def window_or_door_name(self):
        """Get window_or_door_name.

        Returns:
            str: the value of `window_or_door_name` or None if not set

        """
        return self["Window or Door Name"]

    @window_or_door_name.setter
    def window_or_door_name(self, value=None):
        """Corresponds to IDD field `Window or Door Name`

        Args:
            value (str): value for IDD Field `Window or Door Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Window or Door Name"] = value

    @property
    def height_above_window_or_door(self):
        """Get height_above_window_or_door.

        Returns:
            float: the value of `height_above_window_or_door` or None if not set

        """
        return self["Height above Window or Door"]

    @height_above_window_or_door.setter
    def height_above_window_or_door(self, value=None):
        """Corresponds to IDD field `Height above Window or Door`

        Args:
            value (float): value for IDD Field `Height above Window or Door`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Height above Window or Door"] = value

    @property
    def tilt_angle_from_window_or_door(self):
        """Get tilt_angle_from_window_or_door.

        Returns:
            float: the value of `tilt_angle_from_window_or_door` or None if not set

        """
        return self["Tilt Angle from Window/Door"]

    @tilt_angle_from_window_or_door.setter
    def tilt_angle_from_window_or_door(self, value=90.0):
        """Corresponds to IDD field `Tilt Angle from Window/Door`

        Args:
            value (float): value for IDD Field `Tilt Angle from Window/Door`
                Units: deg
                Default value: 90.0
                value <= 180.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Tilt Angle from Window/Door"] = value

    @property
    def left_extension_from_window_or_door_width(self):
        """Get left_extension_from_window_or_door_width.

        Returns:
            float: the value of `left_extension_from_window_or_door_width` or None if not set

        """
        return self["Left extension from Window/Door Width"]

    @left_extension_from_window_or_door_width.setter
    def left_extension_from_window_or_door_width(self, value=None):
        """Corresponds to IDD field `Left extension from Window/Door Width`

        Args:
            value (float): value for IDD Field `Left extension from Window/Door Width`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Left extension from Window/Door Width"] = value

    @property
    def right_extension_from_window_or_door_width(self):
        """Get right_extension_from_window_or_door_width.

        Returns:
            float: the value of `right_extension_from_window_or_door_width` or None if not set

        """
        return self["Right extension from Window/Door Width"]

    @right_extension_from_window_or_door_width.setter
    def right_extension_from_window_or_door_width(self, value=None):
        """Corresponds to IDD field `Right extension from Window/Door Width` N3
        + N4 + Window/Door Width is Overhang Length.

        Args:
            value (float): value for IDD Field `Right extension from Window/Door Width`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Right extension from Window/Door Width"] = value

    @property
    def depth(self):
        """Get depth.

        Returns:
            float: the value of `depth` or None if not set

        """
        return self["Depth"]

    @depth.setter
    def depth(self, value=None):
        """Corresponds to IDD field `Depth`

        Args:
            value (float): value for IDD Field `Depth`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Depth"] = value




class ShadingOverhangProjection(DataObject):

    """ Corresponds to IDD object `Shading:Overhang:Projection`
        Overhangs are typically flat shading surfaces that reference a window or door.
    """
    schema = {'extensible-fields': OrderedDict(),
              'fields': OrderedDict([(u'name',
                                      {'name': u'Name',
                                       'pyname': u'name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'alpha'}),
                                     (u'window or door name',
                                      {'name': u'Window or Door Name',
                                       'pyname': u'window_or_door_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'height above window or door',
                                      {'name': u'Height above Window or Door',
                                       'pyname': u'height_above_window_or_door',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'tilt angle from window/door',
                                      {'name': u'Tilt Angle from Window/Door',
                                       'pyname': u'tilt_angle_from_window_or_door',
                                       'default': 90.0,
                                       'maximum': 180.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'deg'}),
                                     (u'left extension from window/door width',
                                      {'name': u'Left extension from Window/Door Width',
                                       'pyname': u'left_extension_from_window_or_door_width',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'right extension from window/door width',
                                      {'name': u'Right extension from Window/Door Width',
                                       'pyname': u'right_extension_from_window_or_door_width',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'depth as fraction of window/door height',
                                      {'name': u'Depth as Fraction of Window/Door Height',
                                       'pyname': u'depth_as_fraction_of_window_or_door_height',
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'dimensionless'})]),
              'format': None,
              'group': u'Thermal Zones and Surfaces',
              'min-fields': 0,
              'name': u'Shading:Overhang:Projection',
              'pyname': u'ShadingOverhangProjection',
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
    def window_or_door_name(self):
        """Get window_or_door_name.

        Returns:
            str: the value of `window_or_door_name` or None if not set

        """
        return self["Window or Door Name"]

    @window_or_door_name.setter
    def window_or_door_name(self, value=None):
        """Corresponds to IDD field `Window or Door Name`

        Args:
            value (str): value for IDD Field `Window or Door Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Window or Door Name"] = value

    @property
    def height_above_window_or_door(self):
        """Get height_above_window_or_door.

        Returns:
            float: the value of `height_above_window_or_door` or None if not set

        """
        return self["Height above Window or Door"]

    @height_above_window_or_door.setter
    def height_above_window_or_door(self, value=None):
        """Corresponds to IDD field `Height above Window or Door`

        Args:
            value (float): value for IDD Field `Height above Window or Door`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Height above Window or Door"] = value

    @property
    def tilt_angle_from_window_or_door(self):
        """Get tilt_angle_from_window_or_door.

        Returns:
            float: the value of `tilt_angle_from_window_or_door` or None if not set

        """
        return self["Tilt Angle from Window/Door"]

    @tilt_angle_from_window_or_door.setter
    def tilt_angle_from_window_or_door(self, value=90.0):
        """Corresponds to IDD field `Tilt Angle from Window/Door`

        Args:
            value (float): value for IDD Field `Tilt Angle from Window/Door`
                Units: deg
                Default value: 90.0
                value <= 180.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Tilt Angle from Window/Door"] = value

    @property
    def left_extension_from_window_or_door_width(self):
        """Get left_extension_from_window_or_door_width.

        Returns:
            float: the value of `left_extension_from_window_or_door_width` or None if not set

        """
        return self["Left extension from Window/Door Width"]

    @left_extension_from_window_or_door_width.setter
    def left_extension_from_window_or_door_width(self, value=None):
        """Corresponds to IDD field `Left extension from Window/Door Width`

        Args:
            value (float): value for IDD Field `Left extension from Window/Door Width`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Left extension from Window/Door Width"] = value

    @property
    def right_extension_from_window_or_door_width(self):
        """Get right_extension_from_window_or_door_width.

        Returns:
            float: the value of `right_extension_from_window_or_door_width` or None if not set

        """
        return self["Right extension from Window/Door Width"]

    @right_extension_from_window_or_door_width.setter
    def right_extension_from_window_or_door_width(self, value=None):
        """Corresponds to IDD field `Right extension from Window/Door Width` N3
        + N4 + Window/Door Width is Overhang Length.

        Args:
            value (float): value for IDD Field `Right extension from Window/Door Width`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Right extension from Window/Door Width"] = value

    @property
    def depth_as_fraction_of_window_or_door_height(self):
        """Get depth_as_fraction_of_window_or_door_height.

        Returns:
            float: the value of `depth_as_fraction_of_window_or_door_height` or None if not set

        """
        return self["Depth as Fraction of Window/Door Height"]

    @depth_as_fraction_of_window_or_door_height.setter
    def depth_as_fraction_of_window_or_door_height(self, value=None):
        """Corresponds to IDD field `Depth as Fraction of Window/Door Height`

        Args:
            value (float): value for IDD Field `Depth as Fraction of Window/Door Height`
                Units: dimensionless
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Depth as Fraction of Window/Door Height"] = value




class ShadingFin(DataObject):

    """ Corresponds to IDD object `Shading:Fin`
        Fins are usually shading surfaces that are perpendicular to a window or door.
    """
    schema = {'extensible-fields': OrderedDict(),
              'fields': OrderedDict([(u'name',
                                      {'name': u'Name',
                                       'pyname': u'name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'alpha'}),
                                     (u'window or door name',
                                      {'name': u'Window or Door Name',
                                       'pyname': u'window_or_door_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'left extension from window/door',
                                      {'name': u'Left Extension from Window/Door',
                                       'pyname': u'left_extension_from_window_or_door',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'left distance above top of window',
                                      {'name': u'Left Distance Above Top of Window',
                                       'pyname': u'left_distance_above_top_of_window',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'left distance below bottom of window',
                                      {'name': u'Left Distance Below Bottom of Window',
                                       'pyname': u'left_distance_below_bottom_of_window',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'left tilt angle from window/door',
                                      {'name': u'Left Tilt Angle from Window/Door',
                                       'pyname': u'left_tilt_angle_from_window_or_door',
                                       'default': 90.0,
                                       'maximum': 180.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'deg'}),
                                     (u'left depth',
                                      {'name': u'Left Depth',
                                       'pyname': u'left_depth',
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'right extension from window/door',
                                      {'name': u'Right Extension from Window/Door',
                                       'pyname': u'right_extension_from_window_or_door',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'right distance above top of window',
                                      {'name': u'Right Distance Above Top of Window',
                                       'pyname': u'right_distance_above_top_of_window',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'right distance below bottom of window',
                                      {'name': u'Right Distance Below Bottom of Window',
                                       'pyname': u'right_distance_below_bottom_of_window',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'right tilt angle from window/door',
                                      {'name': u'Right Tilt Angle from Window/Door',
                                       'pyname': u'right_tilt_angle_from_window_or_door',
                                       'default': 90.0,
                                       'maximum': 180.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'deg'}),
                                     (u'right depth',
                                      {'name': u'Right Depth',
                                       'pyname': u'right_depth',
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'})]),
              'format': None,
              'group': u'Thermal Zones and Surfaces',
              'min-fields': 0,
              'name': u'Shading:Fin',
              'pyname': u'ShadingFin',
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
    def window_or_door_name(self):
        """Get window_or_door_name.

        Returns:
            str: the value of `window_or_door_name` or None if not set

        """
        return self["Window or Door Name"]

    @window_or_door_name.setter
    def window_or_door_name(self, value=None):
        """Corresponds to IDD field `Window or Door Name`

        Args:
            value (str): value for IDD Field `Window or Door Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Window or Door Name"] = value

    @property
    def left_extension_from_window_or_door(self):
        """Get left_extension_from_window_or_door.

        Returns:
            float: the value of `left_extension_from_window_or_door` or None if not set

        """
        return self["Left Extension from Window/Door"]

    @left_extension_from_window_or_door.setter
    def left_extension_from_window_or_door(self, value=None):
        """Corresponds to IDD field `Left Extension from Window/Door`

        Args:
            value (float): value for IDD Field `Left Extension from Window/Door`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Left Extension from Window/Door"] = value

    @property
    def left_distance_above_top_of_window(self):
        """Get left_distance_above_top_of_window.

        Returns:
            float: the value of `left_distance_above_top_of_window` or None if not set

        """
        return self["Left Distance Above Top of Window"]

    @left_distance_above_top_of_window.setter
    def left_distance_above_top_of_window(self, value=None):
        """Corresponds to IDD field `Left Distance Above Top of Window`

        Args:
            value (float): value for IDD Field `Left Distance Above Top of Window`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Left Distance Above Top of Window"] = value

    @property
    def left_distance_below_bottom_of_window(self):
        """Get left_distance_below_bottom_of_window.

        Returns:
            float: the value of `left_distance_below_bottom_of_window` or None if not set

        """
        return self["Left Distance Below Bottom of Window"]

    @left_distance_below_bottom_of_window.setter
    def left_distance_below_bottom_of_window(self, value=None):
        """Corresponds to IDD field `Left Distance Below Bottom of Window` N2 +
        N3 + height of Window/Door is height of Fin.

        Args:
            value (float): value for IDD Field `Left Distance Below Bottom of Window`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Left Distance Below Bottom of Window"] = value

    @property
    def left_tilt_angle_from_window_or_door(self):
        """Get left_tilt_angle_from_window_or_door.

        Returns:
            float: the value of `left_tilt_angle_from_window_or_door` or None if not set

        """
        return self["Left Tilt Angle from Window/Door"]

    @left_tilt_angle_from_window_or_door.setter
    def left_tilt_angle_from_window_or_door(self, value=90.0):
        """Corresponds to IDD field `Left Tilt Angle from Window/Door`

        Args:
            value (float): value for IDD Field `Left Tilt Angle from Window/Door`
                Units: deg
                Default value: 90.0
                value <= 180.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Left Tilt Angle from Window/Door"] = value

    @property
    def left_depth(self):
        """Get left_depth.

        Returns:
            float: the value of `left_depth` or None if not set

        """
        return self["Left Depth"]

    @left_depth.setter
    def left_depth(self, value=None):
        """Corresponds to IDD field `Left Depth`

        Args:
            value (float): value for IDD Field `Left Depth`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Left Depth"] = value

    @property
    def right_extension_from_window_or_door(self):
        """Get right_extension_from_window_or_door.

        Returns:
            float: the value of `right_extension_from_window_or_door` or None if not set

        """
        return self["Right Extension from Window/Door"]

    @right_extension_from_window_or_door.setter
    def right_extension_from_window_or_door(self, value=None):
        """Corresponds to IDD field `Right Extension from Window/Door`

        Args:
            value (float): value for IDD Field `Right Extension from Window/Door`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Right Extension from Window/Door"] = value

    @property
    def right_distance_above_top_of_window(self):
        """Get right_distance_above_top_of_window.

        Returns:
            float: the value of `right_distance_above_top_of_window` or None if not set

        """
        return self["Right Distance Above Top of Window"]

    @right_distance_above_top_of_window.setter
    def right_distance_above_top_of_window(self, value=None):
        """Corresponds to IDD field `Right Distance Above Top of Window`

        Args:
            value (float): value for IDD Field `Right Distance Above Top of Window`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Right Distance Above Top of Window"] = value

    @property
    def right_distance_below_bottom_of_window(self):
        """Get right_distance_below_bottom_of_window.

        Returns:
            float: the value of `right_distance_below_bottom_of_window` or None if not set

        """
        return self["Right Distance Below Bottom of Window"]

    @right_distance_below_bottom_of_window.setter
    def right_distance_below_bottom_of_window(self, value=None):
        """Corresponds to IDD field `Right Distance Below Bottom of Window` N7
        + N8 + height of Window/Door is height of Fin.

        Args:
            value (float): value for IDD Field `Right Distance Below Bottom of Window`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Right Distance Below Bottom of Window"] = value

    @property
    def right_tilt_angle_from_window_or_door(self):
        """Get right_tilt_angle_from_window_or_door.

        Returns:
            float: the value of `right_tilt_angle_from_window_or_door` or None if not set

        """
        return self["Right Tilt Angle from Window/Door"]

    @right_tilt_angle_from_window_or_door.setter
    def right_tilt_angle_from_window_or_door(self, value=90.0):
        """Corresponds to IDD field `Right Tilt Angle from Window/Door`

        Args:
            value (float): value for IDD Field `Right Tilt Angle from Window/Door`
                Units: deg
                Default value: 90.0
                value <= 180.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Right Tilt Angle from Window/Door"] = value

    @property
    def right_depth(self):
        """Get right_depth.

        Returns:
            float: the value of `right_depth` or None if not set

        """
        return self["Right Depth"]

    @right_depth.setter
    def right_depth(self, value=None):
        """Corresponds to IDD field `Right Depth`

        Args:
            value (float): value for IDD Field `Right Depth`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Right Depth"] = value




class ShadingFinProjection(DataObject):

    """ Corresponds to IDD object `Shading:Fin:Projection`
        Fins are usually shading surfaces that are perpendicular to a window or door.
    """
    schema = {'extensible-fields': OrderedDict(),
              'fields': OrderedDict([(u'name',
                                      {'name': u'Name',
                                       'pyname': u'name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'alpha'}),
                                     (u'window or door name',
                                      {'name': u'Window or Door Name',
                                       'pyname': u'window_or_door_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'left extension from window/door',
                                      {'name': u'Left Extension from Window/Door',
                                       'pyname': u'left_extension_from_window_or_door',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'left distance above top of window',
                                      {'name': u'Left Distance Above Top of Window',
                                       'pyname': u'left_distance_above_top_of_window',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'left distance below bottom of window',
                                      {'name': u'Left Distance Below Bottom of Window',
                                       'pyname': u'left_distance_below_bottom_of_window',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'left tilt angle from window/door',
                                      {'name': u'Left Tilt Angle from Window/Door',
                                       'pyname': u'left_tilt_angle_from_window_or_door',
                                       'default': 90.0,
                                       'maximum': 180.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'deg'}),
                                     (u'left depth as fraction of window/door width',
                                      {'name': u'Left Depth as Fraction of Window/Door Width',
                                       'pyname': u'left_depth_as_fraction_of_window_or_door_width',
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'dimensionless'}),
                                     (u'right extension from window/door',
                                      {'name': u'Right Extension from Window/Door',
                                       'pyname': u'right_extension_from_window_or_door',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'right distance above top of window',
                                      {'name': u'Right Distance Above Top of Window',
                                       'pyname': u'right_distance_above_top_of_window',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'right distance below bottom of window',
                                      {'name': u'Right Distance Below Bottom of Window',
                                       'pyname': u'right_distance_below_bottom_of_window',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'm'}),
                                     (u'right tilt angle from window/door',
                                      {'name': u'Right Tilt Angle from Window/Door',
                                       'pyname': u'right_tilt_angle_from_window_or_door',
                                       'default': 90.0,
                                       'maximum': 180.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'deg'}),
                                     (u'right depth as fraction of window/door width',
                                      {'name': u'Right Depth as Fraction of Window/Door Width',
                                       'pyname': u'right_depth_as_fraction_of_window_or_door_width',
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'dimensionless'})]),
              'format': None,
              'group': u'Thermal Zones and Surfaces',
              'min-fields': 0,
              'name': u'Shading:Fin:Projection',
              'pyname': u'ShadingFinProjection',
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
    def window_or_door_name(self):
        """Get window_or_door_name.

        Returns:
            str: the value of `window_or_door_name` or None if not set

        """
        return self["Window or Door Name"]

    @window_or_door_name.setter
    def window_or_door_name(self, value=None):
        """Corresponds to IDD field `Window or Door Name`

        Args:
            value (str): value for IDD Field `Window or Door Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Window or Door Name"] = value

    @property
    def left_extension_from_window_or_door(self):
        """Get left_extension_from_window_or_door.

        Returns:
            float: the value of `left_extension_from_window_or_door` or None if not set

        """
        return self["Left Extension from Window/Door"]

    @left_extension_from_window_or_door.setter
    def left_extension_from_window_or_door(self, value=None):
        """Corresponds to IDD field `Left Extension from Window/Door`

        Args:
            value (float): value for IDD Field `Left Extension from Window/Door`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Left Extension from Window/Door"] = value

    @property
    def left_distance_above_top_of_window(self):
        """Get left_distance_above_top_of_window.

        Returns:
            float: the value of `left_distance_above_top_of_window` or None if not set

        """
        return self["Left Distance Above Top of Window"]

    @left_distance_above_top_of_window.setter
    def left_distance_above_top_of_window(self, value=None):
        """Corresponds to IDD field `Left Distance Above Top of Window`

        Args:
            value (float): value for IDD Field `Left Distance Above Top of Window`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Left Distance Above Top of Window"] = value

    @property
    def left_distance_below_bottom_of_window(self):
        """Get left_distance_below_bottom_of_window.

        Returns:
            float: the value of `left_distance_below_bottom_of_window` or None if not set

        """
        return self["Left Distance Below Bottom of Window"]

    @left_distance_below_bottom_of_window.setter
    def left_distance_below_bottom_of_window(self, value=None):
        """Corresponds to IDD field `Left Distance Below Bottom of Window` N2 +
        N3 + height of Window/Door is height of Fin.

        Args:
            value (float): value for IDD Field `Left Distance Below Bottom of Window`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Left Distance Below Bottom of Window"] = value

    @property
    def left_tilt_angle_from_window_or_door(self):
        """Get left_tilt_angle_from_window_or_door.

        Returns:
            float: the value of `left_tilt_angle_from_window_or_door` or None if not set

        """
        return self["Left Tilt Angle from Window/Door"]

    @left_tilt_angle_from_window_or_door.setter
    def left_tilt_angle_from_window_or_door(self, value=90.0):
        """Corresponds to IDD field `Left Tilt Angle from Window/Door`

        Args:
            value (float): value for IDD Field `Left Tilt Angle from Window/Door`
                Units: deg
                Default value: 90.0
                value <= 180.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Left Tilt Angle from Window/Door"] = value

    @property
    def left_depth_as_fraction_of_window_or_door_width(self):
        """Get left_depth_as_fraction_of_window_or_door_width.

        Returns:
            float: the value of `left_depth_as_fraction_of_window_or_door_width` or None if not set

        """
        return self["Left Depth as Fraction of Window/Door Width"]

    @left_depth_as_fraction_of_window_or_door_width.setter
    def left_depth_as_fraction_of_window_or_door_width(self, value=None):
        """Corresponds to IDD field `Left Depth as Fraction of Window/Door
        Width`

        Args:
            value (float): value for IDD Field `Left Depth as Fraction of Window/Door Width`
                Units: dimensionless
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Left Depth as Fraction of Window/Door Width"] = value

    @property
    def right_extension_from_window_or_door(self):
        """Get right_extension_from_window_or_door.

        Returns:
            float: the value of `right_extension_from_window_or_door` or None if not set

        """
        return self["Right Extension from Window/Door"]

    @right_extension_from_window_or_door.setter
    def right_extension_from_window_or_door(self, value=None):
        """Corresponds to IDD field `Right Extension from Window/Door`

        Args:
            value (float): value for IDD Field `Right Extension from Window/Door`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Right Extension from Window/Door"] = value

    @property
    def right_distance_above_top_of_window(self):
        """Get right_distance_above_top_of_window.

        Returns:
            float: the value of `right_distance_above_top_of_window` or None if not set

        """
        return self["Right Distance Above Top of Window"]

    @right_distance_above_top_of_window.setter
    def right_distance_above_top_of_window(self, value=None):
        """Corresponds to IDD field `Right Distance Above Top of Window`

        Args:
            value (float): value for IDD Field `Right Distance Above Top of Window`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Right Distance Above Top of Window"] = value

    @property
    def right_distance_below_bottom_of_window(self):
        """Get right_distance_below_bottom_of_window.

        Returns:
            float: the value of `right_distance_below_bottom_of_window` or None if not set

        """
        return self["Right Distance Below Bottom of Window"]

    @right_distance_below_bottom_of_window.setter
    def right_distance_below_bottom_of_window(self, value=None):
        """Corresponds to IDD field `Right Distance Below Bottom of Window` N7
        + N8 + height of Window/Door is height of Fin.

        Args:
            value (float): value for IDD Field `Right Distance Below Bottom of Window`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Right Distance Below Bottom of Window"] = value

    @property
    def right_tilt_angle_from_window_or_door(self):
        """Get right_tilt_angle_from_window_or_door.

        Returns:
            float: the value of `right_tilt_angle_from_window_or_door` or None if not set

        """
        return self["Right Tilt Angle from Window/Door"]

    @right_tilt_angle_from_window_or_door.setter
    def right_tilt_angle_from_window_or_door(self, value=90.0):
        """Corresponds to IDD field `Right Tilt Angle from Window/Door`

        Args:
            value (float): value for IDD Field `Right Tilt Angle from Window/Door`
                Units: deg
                Default value: 90.0
                value <= 180.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Right Tilt Angle from Window/Door"] = value

    @property
    def right_depth_as_fraction_of_window_or_door_width(self):
        """Get right_depth_as_fraction_of_window_or_door_width.

        Returns:
            float: the value of `right_depth_as_fraction_of_window_or_door_width` or None if not set

        """
        return self["Right Depth as Fraction of Window/Door Width"]

    @right_depth_as_fraction_of_window_or_door_width.setter
    def right_depth_as_fraction_of_window_or_door_width(self, value=None):
        """Corresponds to IDD field `Right Depth as Fraction of Window/Door
        Width`

        Args:
            value (float): value for IDD Field `Right Depth as Fraction of Window/Door Width`
                Units: dimensionless
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Right Depth as Fraction of Window/Door Width"] = value




class ShadingZoneDetailed(DataObject):

    """ Corresponds to IDD object `Shading:Zone:Detailed`
        used For fins, overhangs, elements that shade the building, are attached to the building
        but are not part of the heat transfer calculations
    """
    schema = {'extensible-fields': OrderedDict([(u'vertex 1 x-coordinate',
                                                 {'name': u'Vertex 1 X-coordinate',
                                                  'pyname': u'vertex_1_xcoordinate',
                                                  'required-field': True,
                                                  'autosizable': False,
                                                  'autocalculatable': False,
                                                  'type': u'real',
                                                  'unit': u'm'}),
                                                (u'vertex 1 y-coordinate',
                                                 {'name': u'Vertex 1 Y-coordinate',
                                                  'pyname': u'vertex_1_ycoordinate',
                                                  'required-field': True,
                                                  'autosizable': False,
                                                  'autocalculatable': False,
                                                  'type': u'real',
                                                  'unit': u'm'}),
                                                (u'vertex 1 z-coordinate',
                                                 {'name': u'Vertex 1 Z-coordinate',
                                                  'pyname': u'vertex_1_zcoordinate',
                                                  'required-field': True,
                                                  'autosizable': False,
                                                  'autocalculatable': False,
                                                  'type': u'real',
                                                  'unit': u'm'})]),
              'fields': OrderedDict([(u'name',
                                      {'name': u'Name',
                                       'pyname': u'name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'alpha'}),
                                     (u'base surface name',
                                      {'name': u'Base Surface Name',
                                       'pyname': u'base_surface_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'transmittance schedule name',
                                      {'name': u'Transmittance Schedule Name',
                                       'pyname': u'transmittance_schedule_name',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'number of vertices',
                                      {'name': u'Number of Vertices',
                                       'pyname': u'number_of_vertices',
                                       'default': 'autocalculate',
                                       'required-field': True,
                                       'autosizable': False,
                                       'minimum': 3.0,
                                       'autocalculatable': True,
                                       'type': 'real'})]),
              'format': u'vertices',
              'group': u'Thermal Zones and Surfaces',
              'min-fields': 13,
              'name': u'Shading:Zone:Detailed',
              'pyname': u'ShadingZoneDetailed',
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
    def base_surface_name(self):
        """Get base_surface_name.

        Returns:
            str: the value of `base_surface_name` or None if not set

        """
        return self["Base Surface Name"]

    @base_surface_name.setter
    def base_surface_name(self, value=None):
        """Corresponds to IDD field `Base Surface Name`

        Args:
            value (str): value for IDD Field `Base Surface Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Base Surface Name"] = value

    @property
    def transmittance_schedule_name(self):
        """Get transmittance_schedule_name.

        Returns:
            str: the value of `transmittance_schedule_name` or None if not set

        """
        return self["Transmittance Schedule Name"]

    @transmittance_schedule_name.setter
    def transmittance_schedule_name(self, value=None):
        """Corresponds to IDD field `Transmittance Schedule Name` Transmittance
        schedule for the shading device, defaults to zero (always opaque)

        Args:
            value (str): value for IDD Field `Transmittance Schedule Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Transmittance Schedule Name"] = value

    @property
    def number_of_vertices(self):
        """Get number_of_vertices.

        Returns:
            float: the value of `number_of_vertices` or None if not set

        """
        return self["Number of Vertices"]

    @number_of_vertices.setter
    def number_of_vertices(self, value="autocalculate"):
        """  Corresponds to IDD field `Number of Vertices`
        shown with 6 vertex coordinates -- extensible object
        vertices are given in GlobalGeometryRules coordinates -- if relative, all surface coordinates
        are "relative" to the Zone Origin.  if world, then building and zone origins are used
        for some internal calculations, but all coordinates are given in an "absolute" system.

        Args:
            value (float or "Autocalculate"): value for IDD Field `Number of Vertices`
                Default value: "autocalculate"
                value >= 3.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Number of Vertices"] = value

    def add_extensible(self,
                       vertex_1_xcoordinate=None,
                       vertex_1_ycoordinate=None,
                       vertex_1_zcoordinate=None,
                       ):
        """Add values for extensible fields.

        Args:

            vertex_1_xcoordinate (float): value for IDD Field `Vertex 1 X-coordinate`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

            vertex_1_ycoordinate (float): value for IDD Field `Vertex 1 Y-coordinate`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

            vertex_1_zcoordinate (float): value for IDD Field `Vertex 1 Z-coordinate`
                Units: m
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        """
        vals = []
        vertex_1_xcoordinate = self.check_value(
            "Vertex 1 X-coordinate",
            vertex_1_xcoordinate)
        vals.append(vertex_1_xcoordinate)
        vertex_1_ycoordinate = self.check_value(
            "Vertex 1 Y-coordinate",
            vertex_1_ycoordinate)
        vals.append(vertex_1_ycoordinate)
        vertex_1_zcoordinate = self.check_value(
            "Vertex 1 Z-coordinate",
            vertex_1_zcoordinate)
        vals.append(vertex_1_zcoordinate)
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




class ShadingPropertyReflectance(DataObject):

    """ Corresponds to IDD object `ShadingProperty:Reflectance`
        If this object is not defined for a shading surface the default values
        listed in following fields will be used in the solar reflection calculation.
    """
    schema = {'extensible-fields': OrderedDict(),
              'fields': OrderedDict([(u'shading surface name',
                                      {'name': u'Shading Surface Name',
                                       'pyname': u'shading_surface_name',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'diffuse solar reflectance of unglazed part of shading surface',
                                      {'name': u'Diffuse Solar Reflectance of Unglazed Part of Shading Surface',
                                       'pyname': u'diffuse_solar_reflectance_of_unglazed_part_of_shading_surface',
                                       'default': 0.2,
                                       'maximum': 1.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': 'real'}),
                                     (u'diffuse visible reflectance of unglazed part of shading surface',
                                      {'name': u'Diffuse Visible Reflectance of Unglazed Part of Shading Surface',
                                       'pyname': u'diffuse_visible_reflectance_of_unglazed_part_of_shading_surface',
                                       'default': 0.2,
                                       'maximum': 1.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': 'real'}),
                                     (u'fraction of shading surface that is glazed',
                                      {'name': u'Fraction of Shading Surface That Is Glazed',
                                       'pyname': u'fraction_of_shading_surface_that_is_glazed',
                                       'default': 0.0,
                                       'maximum': 1.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.0,
                                       'autocalculatable': False,
                                       'type': 'real'}),
                                     (u'glazing construction name',
                                      {'name': u'Glazing Construction Name',
                                       'pyname': u'glazing_construction_name',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'alpha'})]),
              'format': None,
              'group': u'Thermal Zones and Surfaces',
              'min-fields': 3,
              'name': u'ShadingProperty:Reflectance',
              'pyname': u'ShadingPropertyReflectance',
              'required-object': False,
              'unique-object': False}

    @property
    def shading_surface_name(self):
        """Get shading_surface_name.

        Returns:
            str: the value of `shading_surface_name` or None if not set

        """
        return self["Shading Surface Name"]

    @shading_surface_name.setter
    def shading_surface_name(self, value=None):
        """Corresponds to IDD field `Shading Surface Name`

        Args:
            value (str): value for IDD Field `Shading Surface Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Shading Surface Name"] = value

    @property
    def diffuse_solar_reflectance_of_unglazed_part_of_shading_surface(self):
        """Get diffuse_solar_reflectance_of_unglazed_part_of_shading_surface.

        Returns:
            float: the value of `diffuse_solar_reflectance_of_unglazed_part_of_shading_surface` or None if not set

        """
        return self[
            "Diffuse Solar Reflectance of Unglazed Part of Shading Surface"]

    @diffuse_solar_reflectance_of_unglazed_part_of_shading_surface.setter
    def diffuse_solar_reflectance_of_unglazed_part_of_shading_surface(
            self,
            value=0.2):
        """Corresponds to IDD field `Diffuse Solar Reflectance of Unglazed Part
        of Shading Surface`

        Args:
            value (float): value for IDD Field `Diffuse Solar Reflectance of Unglazed Part of Shading Surface`
                Default value: 0.2
                value <= 1.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self[
            "Diffuse Solar Reflectance of Unglazed Part of Shading Surface"] = value

    @property
    def diffuse_visible_reflectance_of_unglazed_part_of_shading_surface(self):
        """Get diffuse_visible_reflectance_of_unglazed_part_of_shading_surface.

        Returns:
            float: the value of `diffuse_visible_reflectance_of_unglazed_part_of_shading_surface` or None if not set

        """
        return self[
            "Diffuse Visible Reflectance of Unglazed Part of Shading Surface"]

    @diffuse_visible_reflectance_of_unglazed_part_of_shading_surface.setter
    def diffuse_visible_reflectance_of_unglazed_part_of_shading_surface(
            self,
            value=0.2):
        """Corresponds to IDD field `Diffuse Visible Reflectance of Unglazed
        Part of Shading Surface`

        Args:
            value (float): value for IDD Field `Diffuse Visible Reflectance of Unglazed Part of Shading Surface`
                Default value: 0.2
                value <= 1.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self[
            "Diffuse Visible Reflectance of Unglazed Part of Shading Surface"] = value

    @property
    def fraction_of_shading_surface_that_is_glazed(self):
        """Get fraction_of_shading_surface_that_is_glazed.

        Returns:
            float: the value of `fraction_of_shading_surface_that_is_glazed` or None if not set

        """
        return self["Fraction of Shading Surface That Is Glazed"]

    @fraction_of_shading_surface_that_is_glazed.setter
    def fraction_of_shading_surface_that_is_glazed(self, value=None):
        """Corresponds to IDD field `Fraction of Shading Surface That Is
        Glazed`

        Args:
            value (float): value for IDD Field `Fraction of Shading Surface That Is Glazed`
                value <= 1.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Fraction of Shading Surface That Is Glazed"] = value

    @property
    def glazing_construction_name(self):
        """Get glazing_construction_name.

        Returns:
            str: the value of `glazing_construction_name` or None if not set

        """
        return self["Glazing Construction Name"]

    @glazing_construction_name.setter
    def glazing_construction_name(self, value=None):
        """  Corresponds to IDD field `Glazing Construction Name`
        Required if Fraction of Shading Surface That Is Glazed > 0.0

        Args:
            value (str): value for IDD Field `Glazing Construction Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Glazing Construction Name"] = value


