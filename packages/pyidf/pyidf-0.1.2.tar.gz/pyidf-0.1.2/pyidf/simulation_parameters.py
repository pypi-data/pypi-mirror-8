""" Data objects in group "Simulation Parameters"
"""

from collections import OrderedDict
import logging
from pyidf.helper import DataObject

logger = logging.getLogger("pyidf")
logger.addHandler(logging.NullHandler())



class Version(DataObject):

    """Corresponds to IDD object `Version` Specifies the EnergyPlus version of
    the IDF file."""
    schema = {'extensible-fields': OrderedDict(),
              'fields': OrderedDict([(u'version identifier',
                                      {'name': u'Version Identifier',
                                       'pyname': u'version_identifier',
                                       'default': u'7.0',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'alpha'})]),
              'format': u'singleline',
              'group': u'Simulation Parameters',
              'min-fields': 0,
              'name': u'Version',
              'pyname': u'Version',
              'required-object': False,
              'unique-object': True}

    @property
    def version_identifier(self):
        """Get version_identifier.

        Returns:
            str: the value of `version_identifier` or None if not set

        """
        return self["Version Identifier"]

    @version_identifier.setter
    def version_identifier(self, value="7.0"):
        """Corresponds to IDD field `Version Identifier`

        Args:
            value (str): value for IDD Field `Version Identifier`
                Default value: 7.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Version Identifier"] = value




class SimulationControl(DataObject):

    """ Corresponds to IDD object `SimulationControl`
        Note that the following 3 fields are related to the Sizing:Zone, Sizing:System,
        and Sizing:Plant objects.  Having these fields set to Yes but no corresponding
        Sizing object will not cause the sizing to be done. However, having any of these
        fields set to No, the corresponding Sizing object is ignored.
        Note also, if you want to do system sizing, you must also do zone sizing in the same
        run or an error will result.
    """
    schema = {'extensible-fields': OrderedDict(),
              'fields': OrderedDict([(u'do zone sizing calculation',
                                      {'name': u'Do Zone Sizing Calculation',
                                       'pyname': u'do_zone_sizing_calculation',
                                       'default': u'No',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'Yes',
                                                           u'No'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'do system sizing calculation',
                                      {'name': u'Do System Sizing Calculation',
                                       'pyname': u'do_system_sizing_calculation',
                                       'default': u'No',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'Yes',
                                                           u'No'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'do plant sizing calculation',
                                      {'name': u'Do Plant Sizing Calculation',
                                       'pyname': u'do_plant_sizing_calculation',
                                       'default': u'No',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'Yes',
                                                           u'No'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'run simulation for sizing periods',
                                      {'name': u'Run Simulation for Sizing Periods',
                                       'pyname': u'run_simulation_for_sizing_periods',
                                       'default': u'Yes',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'Yes',
                                                           u'No'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'run simulation for weather file run periods',
                                      {'name': u'Run Simulation for Weather File Run Periods',
                                       'pyname': u'run_simulation_for_weather_file_run_periods',
                                       'default': u'Yes',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'Yes',
                                                           u'No'],
                                       'autocalculatable': False,
                                       'type': 'alpha'})]),
              'format': None,
              'group': u'Simulation Parameters',
              'min-fields': 0,
              'name': u'SimulationControl',
              'pyname': u'SimulationControl',
              'required-object': False,
              'unique-object': True}

    @property
    def do_zone_sizing_calculation(self):
        """Get do_zone_sizing_calculation.

        Returns:
            str: the value of `do_zone_sizing_calculation` or None if not set

        """
        return self["Do Zone Sizing Calculation"]

    @do_zone_sizing_calculation.setter
    def do_zone_sizing_calculation(self, value="No"):
        """  Corresponds to IDD field `Do Zone Sizing Calculation`
        If Yes, Zone sizing is accomplished from corresponding Sizing:Zone objects
        and autosize fields.

        Args:
            value (str): value for IDD Field `Do Zone Sizing Calculation`
                Default value: No
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Do Zone Sizing Calculation"] = value

    @property
    def do_system_sizing_calculation(self):
        """Get do_system_sizing_calculation.

        Returns:
            str: the value of `do_system_sizing_calculation` or None if not set

        """
        return self["Do System Sizing Calculation"]

    @do_system_sizing_calculation.setter
    def do_system_sizing_calculation(self, value="No"):
        """  Corresponds to IDD field `Do System Sizing Calculation`
        If Yes, System sizing is accomplished from corresponding Sizing:System objects
        and autosize fields.
        If Yes, Zone sizing (previous field) must also be Yes.

        Args:
            value (str): value for IDD Field `Do System Sizing Calculation`
                Default value: No
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Do System Sizing Calculation"] = value

    @property
    def do_plant_sizing_calculation(self):
        """Get do_plant_sizing_calculation.

        Returns:
            str: the value of `do_plant_sizing_calculation` or None if not set

        """
        return self["Do Plant Sizing Calculation"]

    @do_plant_sizing_calculation.setter
    def do_plant_sizing_calculation(self, value="No"):
        """  Corresponds to IDD field `Do Plant Sizing Calculation`
        If Yes, Plant sizing is accomplished from corresponding Sizing:Plant objects
        and autosize fields.

        Args:
            value (str): value for IDD Field `Do Plant Sizing Calculation`
                Default value: No
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Do Plant Sizing Calculation"] = value

    @property
    def run_simulation_for_sizing_periods(self):
        """Get run_simulation_for_sizing_periods.

        Returns:
            str: the value of `run_simulation_for_sizing_periods` or None if not set

        """
        return self["Run Simulation for Sizing Periods"]

    @run_simulation_for_sizing_periods.setter
    def run_simulation_for_sizing_periods(self, value="Yes"):
        """  Corresponds to IDD field `Run Simulation for Sizing Periods`
        If Yes, SizingPeriod:* objects are executed and results from those may be displayed..

        Args:
            value (str): value for IDD Field `Run Simulation for Sizing Periods`
                Default value: Yes
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Run Simulation for Sizing Periods"] = value

    @property
    def run_simulation_for_weather_file_run_periods(self):
        """Get run_simulation_for_weather_file_run_periods.

        Returns:
            str: the value of `run_simulation_for_weather_file_run_periods` or None if not set

        """
        return self["Run Simulation for Weather File Run Periods"]

    @run_simulation_for_weather_file_run_periods.setter
    def run_simulation_for_weather_file_run_periods(self, value="Yes"):
        """  Corresponds to IDD field `Run Simulation for Weather File Run Periods`
        If Yes, RunPeriod:* objects are executed and results from those may be displayed..

        Args:
            value (str): value for IDD Field `Run Simulation for Weather File Run Periods`
                Default value: Yes
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Run Simulation for Weather File Run Periods"] = value




class Building(DataObject):

    """Corresponds to IDD object `Building` Describes parameters that are used
    during the simulation of the building.

    There are necessary correlations between the entries for
    this object and some entries in the Site:WeatherStation and
    Site:HeightVariation objects, specifically the Terrain field.

    """
    schema = {'extensible-fields': OrderedDict(),
              'fields': OrderedDict([(u'name',
                                      {'name': u'Name',
                                       'pyname': u'name',
                                       'default': u'NONE',
                                       'required-field': True,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'north axis',
                                      {'name': u'North Axis',
                                       'pyname': u'north_axis',
                                       'default': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'deg'}),
                                     (u'terrain',
                                      {'name': u'Terrain',
                                       'pyname': u'terrain',
                                       'default': u'Suburbs',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'Country',
                                                           u'Suburbs',
                                                           u'City',
                                                           u'Ocean',
                                                           u'Urban'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'loads convergence tolerance value',
                                      {'name': u'Loads Convergence Tolerance Value',
                                       'pyname': u'loads_convergence_tolerance_value',
                                       'default': 0.04,
                                       'minimum>': 0.0,
                                       'maximum': 0.5,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'temperature convergence tolerance value',
                                      {'name': u'Temperature Convergence Tolerance Value',
                                       'pyname': u'temperature_convergence_tolerance_value',
                                       'default': 0.4,
                                       'minimum>': 0.0,
                                       'maximum': 0.5,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'deltaC'}),
                                     (u'solar distribution',
                                      {'name': u'Solar Distribution',
                                       'pyname': u'solar_distribution',
                                       'default': u'FullExterior',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'MinimalShadowing',
                                                           u'FullExterior',
                                                           u'FullInteriorAndExterior',
                                                           u'FullExteriorWithReflections',
                                                           u'FullInteriorAndExteriorWithReflections'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'maximum number of warmup days',
                                      {'name': u'Maximum Number of Warmup Days',
                                       'pyname': u'maximum_number_of_warmup_days',
                                       'default': 25,
                                       'minimum>': 0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'integer'}),
                                     (u'minimum number of warmup days',
                                      {'name': u'Minimum Number of Warmup Days',
                                       'pyname': u'minimum_number_of_warmup_days',
                                       'default': 6,
                                       'minimum>': 0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'integer'})]),
              'format': None,
              'group': u'Simulation Parameters',
              'min-fields': 8,
              'name': u'Building',
              'pyname': u'Building',
              'required-object': True,
              'unique-object': True}

    @property
    def name(self):
        """Get name.

        Returns:
            str: the value of `name` or None if not set

        """
        return self["Name"]

    @name.setter
    def name(self, value="NONE"):
        """Corresponds to IDD field `Name`

        Args:
            value (str): value for IDD Field `Name`
                Default value: NONE
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Name"] = value

    @property
    def north_axis(self):
        """Get north_axis.

        Returns:
            float: the value of `north_axis` or None if not set

        """
        return self["North Axis"]

    @north_axis.setter
    def north_axis(self, value=None):
        """Corresponds to IDD field `North Axis` degrees from true North.

        Args:
            value (float): value for IDD Field `North Axis`
                Units: deg
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["North Axis"] = value

    @property
    def terrain(self):
        """Get terrain.

        Returns:
            str: the value of `terrain` or None if not set

        """
        return self["Terrain"]

    @terrain.setter
    def terrain(self, value="Suburbs"):
        """  Corresponds to IDD field `Terrain`
        Country=FlatOpenCountry | Suburbs=CountryTownsSuburbs | City=CityCenter | Ocean=body of water (5km) | Urban=Urban-Industrial-Forest

        Args:
            value (str): value for IDD Field `Terrain`
                Default value: Suburbs
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Terrain"] = value

    @property
    def loads_convergence_tolerance_value(self):
        """Get loads_convergence_tolerance_value.

        Returns:
            float: the value of `loads_convergence_tolerance_value` or None if not set

        """
        return self["Loads Convergence Tolerance Value"]

    @loads_convergence_tolerance_value.setter
    def loads_convergence_tolerance_value(self, value=0.04):
        """Corresponds to IDD field `Loads Convergence Tolerance Value` Loads
        Convergence Tolerance Value is a fraction of load.

        Args:
            value (float): value for IDD Field `Loads Convergence Tolerance Value`
                Default value: 0.04
                value <= 0.5
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Loads Convergence Tolerance Value"] = value

    @property
    def temperature_convergence_tolerance_value(self):
        """Get temperature_convergence_tolerance_value.

        Returns:
            float: the value of `temperature_convergence_tolerance_value` or None if not set

        """
        return self["Temperature Convergence Tolerance Value"]

    @temperature_convergence_tolerance_value.setter
    def temperature_convergence_tolerance_value(self, value=0.4):
        """Corresponds to IDD field `Temperature Convergence Tolerance Value`

        Args:
            value (float): value for IDD Field `Temperature Convergence Tolerance Value`
                Units: deltaC
                Default value: 0.4
                value <= 0.5
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Temperature Convergence Tolerance Value"] = value

    @property
    def solar_distribution(self):
        """Get solar_distribution.

        Returns:
            str: the value of `solar_distribution` or None if not set

        """
        return self["Solar Distribution"]

    @solar_distribution.setter
    def solar_distribution(self, value="FullExterior"):
        """Corresponds to IDD field `Solar Distribution` MinimalShadowing |
        FullExterior | FullInteriorAndExterior | FullExteriorWithReflections |
        FullInteriorAndExteriorWithReflections.

        Args:
            value (str): value for IDD Field `Solar Distribution`
                Default value: FullExterior
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Solar Distribution"] = value

    @property
    def maximum_number_of_warmup_days(self):
        """Get maximum_number_of_warmup_days.

        Returns:
            int: the value of `maximum_number_of_warmup_days` or None if not set

        """
        return self["Maximum Number of Warmup Days"]

    @maximum_number_of_warmup_days.setter
    def maximum_number_of_warmup_days(self, value=25):
        """  Corresponds to IDD field `Maximum Number of Warmup Days`
        EnergyPlus will only use as many warmup days as needed to reach convergence tolerance.
        This field's value should NOT be set less than 25.

        Args:
            value (int): value for IDD Field `Maximum Number of Warmup Days`
                Default value: 25
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Maximum Number of Warmup Days"] = value

    @property
    def minimum_number_of_warmup_days(self):
        """Get minimum_number_of_warmup_days.

        Returns:
            int: the value of `minimum_number_of_warmup_days` or None if not set

        """
        return self["Minimum Number of Warmup Days"]

    @minimum_number_of_warmup_days.setter
    def minimum_number_of_warmup_days(self, value=6):
        """  Corresponds to IDD field `Minimum Number of Warmup Days`
        The minimum number of warmup days that produce enough temperature and flux history
        to start EnergyPlus simulation for all reference buildings was suggested to be 6.
        When this field is greater than the maximum warmup days defined previous field
        the maximum number of warmup days will be reset to the minimum value entered here.
        Warmup days will be set to be the value you entered when it is less than the default 6.

        Args:
            value (int): value for IDD Field `Minimum Number of Warmup Days`
                Default value: 6
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Minimum Number of Warmup Days"] = value




class ShadowCalculation(DataObject):

    """Corresponds to IDD object `ShadowCalculation` This object is used to
    control details of the solar, shading, and daylighting models."""
    schema = {'extensible-fields': OrderedDict(),
              'fields': OrderedDict([(u'calculation method',
                                      {'name': u'Calculation Method',
                                       'pyname': u'calculation_method',
                                       'default': u'AverageOverDaysInFrequency',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'AverageOverDaysInFrequency',
                                                           u'TimestepFrequency'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'calculation frequency',
                                      {'name': u'Calculation Frequency',
                                       'pyname': u'calculation_frequency',
                                       'default': 20,
                                       'required-field': True,
                                       'autosizable': False,
                                       'minimum': 1,
                                       'autocalculatable': False,
                                       'type': u'integer'}),
                                     (u'maximum figures in shadow overlap calculations',
                                      {'name': u'Maximum Figures in Shadow Overlap Calculations',
                                       'pyname': u'maximum_figures_in_shadow_overlap_calculations',
                                       'default': 15000,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 200,
                                       'autocalculatable': False,
                                       'type': u'integer'}),
                                     (u'polygon clipping algorithm',
                                      {'name': u'Polygon Clipping Algorithm',
                                       'pyname': u'polygon_clipping_algorithm',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'ConvexWeilerAtherton',
                                                           u'SutherlandHodgman'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'sky diffuse modeling algorithm',
                                      {'name': u'Sky Diffuse Modeling Algorithm',
                                       'pyname': u'sky_diffuse_modeling_algorithm',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'SimpleSkyDiffuseModeling',
                                                           u'DetailedSkyDiffuseModeling'],
                                       'autocalculatable': False,
                                       'type': 'alpha'})]),
              'format': None,
              'group': u'Simulation Parameters',
              'min-fields': 0,
              'name': u'ShadowCalculation',
              'pyname': u'ShadowCalculation',
              'required-object': False,
              'unique-object': True}

    @property
    def calculation_method(self):
        """Get calculation_method.

        Returns:
            str: the value of `calculation_method` or None if not set

        """
        return self["Calculation Method"]

    @calculation_method.setter
    def calculation_method(self, value="AverageOverDaysInFrequency"):
        """Corresponds to IDD field `Calculation Method` choose calculation
        method. note that TimestepFrequency is only needed for certain cases
        and can increase execution time significantly.

        Args:
            value (str): value for IDD Field `Calculation Method`
                Default value: AverageOverDaysInFrequency
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Calculation Method"] = value

    @property
    def calculation_frequency(self):
        """Get calculation_frequency.

        Returns:
            int: the value of `calculation_frequency` or None if not set

        """
        return self["Calculation Frequency"]

    @calculation_frequency.setter
    def calculation_frequency(self, value=20):
        """  Corresponds to IDD field `Calculation Frequency`
        enter number of days
        this field is only used if the previous field is set to AverageOverDaysInFrequency
        0=Use Default Periodic Calculation|<else> calculate every <value> day
        only really applicable to RunPeriods
        warning issued if >31

        Args:
            value (int): value for IDD Field `Calculation Frequency`
                Default value: 20
                value >= 1
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Calculation Frequency"] = value

    @property
    def maximum_figures_in_shadow_overlap_calculations(self):
        """Get maximum_figures_in_shadow_overlap_calculations.

        Returns:
            int: the value of `maximum_figures_in_shadow_overlap_calculations` or None if not set

        """
        return self["Maximum Figures in Shadow Overlap Calculations"]

    @maximum_figures_in_shadow_overlap_calculations.setter
    def maximum_figures_in_shadow_overlap_calculations(self, value=15000):
        """Corresponds to IDD field `Maximum Figures in Shadow Overlap
        Calculations` Number of allowable figures in shadow overlap
        calculations.

        Args:
            value (int): value for IDD Field `Maximum Figures in Shadow Overlap Calculations`
                Default value: 15000
                value >= 200
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Maximum Figures in Shadow Overlap Calculations"] = value

    @property
    def polygon_clipping_algorithm(self):
        """Get polygon_clipping_algorithm.

        Returns:
            str: the value of `polygon_clipping_algorithm` or None if not set

        """
        return self["Polygon Clipping Algorithm"]

    @polygon_clipping_algorithm.setter
    def polygon_clipping_algorithm(self, value=None):
        """Corresponds to IDD field `Polygon Clipping Algorithm` Advanced
        Feature.  Internal default is SutherlandHodgman Refer to InputOutput
        Reference and Engineering Reference for more information.

        Args:
            value (str): value for IDD Field `Polygon Clipping Algorithm`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Polygon Clipping Algorithm"] = value

    @property
    def sky_diffuse_modeling_algorithm(self):
        """Get sky_diffuse_modeling_algorithm.

        Returns:
            str: the value of `sky_diffuse_modeling_algorithm` or None if not set

        """
        return self["Sky Diffuse Modeling Algorithm"]

    @sky_diffuse_modeling_algorithm.setter
    def sky_diffuse_modeling_algorithm(self, value=None):
        """Corresponds to IDD field `Sky Diffuse Modeling Algorithm` Advanced
        Feature.  Internal default is SimpleSkyDiffuseModeling If you have
        shading elements that change transmittance over the year, you may wish
        to choose the detailed method. Refer to InputOutput Reference and
        Engineering Reference for more information.

        Args:
            value (str): value for IDD Field `Sky Diffuse Modeling Algorithm`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Sky Diffuse Modeling Algorithm"] = value




class SurfaceConvectionAlgorithmInside(DataObject):

    """ Corresponds to IDD object `SurfaceConvectionAlgorithm:Inside`
        Default indoor surface heat transfer convection algorithm to be used for all zones
    """
    schema = {'extensible-fields': OrderedDict(),
              'fields': OrderedDict([(u'algorithm',
                                      {'name': u'Algorithm',
                                       'pyname': u'algorithm',
                                       'default': u'TARP',
                                       'required-field': True,
                                       'autosizable': False,
                                       'accepted-values': [u'Simple',
                                                           u'TARP',
                                                           u'CeilingDiffuser',
                                                           u'AdaptiveConvectionAlgorithm'],
                                       'autocalculatable': False,
                                       'type': 'alpha'})]),
              'format': u'singleline',
              'group': u'Simulation Parameters',
              'min-fields': 0,
              'name': u'SurfaceConvectionAlgorithm:Inside',
              'pyname': u'SurfaceConvectionAlgorithmInside',
              'required-object': False,
              'unique-object': True}

    @property
    def algorithm(self):
        """Get algorithm.

        Returns:
            str: the value of `algorithm` or None if not set

        """
        return self["Algorithm"]

    @algorithm.setter
    def algorithm(self, value="TARP"):
        """  Corresponds to IDD field `Algorithm`
        Simple = constant value natural convection (ASHRAE)
        TARP = variable natural convection based on temperature difference (ASHRAE, Walton)
        CeilingDiffuser = ACH-based forced and mixed convection correlations
        for ceiling diffuser configuration with simple natural convection limit
        AdaptiveConvectionAlgorithm = dynamic selection of convection models based on conditions

        Args:
            value (str): value for IDD Field `Algorithm`
                Default value: TARP
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Algorithm"] = value




class SurfaceConvectionAlgorithmOutside(DataObject):

    """ Corresponds to IDD object `SurfaceConvectionAlgorithm:Outside`
        Default outside surface heat transfer convection algorithm to be used for all zones
    """
    schema = {'extensible-fields': OrderedDict(),
              'fields': OrderedDict([(u'algorithm',
                                      {'name': u'Algorithm',
                                       'pyname': u'algorithm',
                                       'default': u'DOE-2',
                                       'required-field': True,
                                       'autosizable': False,
                                       'accepted-values': [u'SimpleCombined',
                                                           u'TARP',
                                                           u'MoWiTT',
                                                           u'DOE-2',
                                                           u'AdaptiveConvectionAlgorithm'],
                                       'autocalculatable': False,
                                       'type': 'alpha'})]),
              'format': u'singleline',
              'group': u'Simulation Parameters',
              'min-fields': 0,
              'name': u'SurfaceConvectionAlgorithm:Outside',
              'pyname': u'SurfaceConvectionAlgorithmOutside',
              'required-object': False,
              'unique-object': True}

    @property
    def algorithm(self):
        """Get algorithm.

        Returns:
            str: the value of `algorithm` or None if not set

        """
        return self["Algorithm"]

    @algorithm.setter
    def algorithm(self, value="DOE-2"):
        """  Corresponds to IDD field `Algorithm`
        SimpleCombined = Combined radiation and convection coefficient using simple ASHRAE model
        TARP = correlation from models developed by ASHRAE, Walton, and Sparrow et. al.
        MoWiTT = correlation from measurements by Klems and Yazdanian for smooth surfaces
        DOE-2 = correlation from measurements by Klems and Yazdanian for rough surfaces
        AdaptiveConvectionAlgorithm = dynamic selection of correlations based on conditions

        Args:
            value (str): value for IDD Field `Algorithm`
                Default value: DOE-2
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Algorithm"] = value




class HeatBalanceAlgorithm(DataObject):

    """Corresponds to IDD object `HeatBalanceAlgorithm` Determines which Heat
    Balance Algorithm will be used ie.

    CTF (Conduction Transfer Functions),
    EMPD (Effective Moisture Penetration Depth with Conduction Transfer Functions).
    Advanced/Research Usage: CondFD (Conduction Finite Difference)
    Advanced/Research Usage: ConductionFiniteDifferenceSimplified
    Advanced/Research Usage: HAMT (Combined Heat And Moisture Finite Element)

    """
    schema = {'extensible-fields': OrderedDict(),
              'fields': OrderedDict([(u'algorithm',
                                      {'name': u'Algorithm',
                                       'pyname': u'algorithm',
                                       'default': u'ConductionTransferFunction',
                                       'required-field': True,
                                       'autosizable': False,
                                       'accepted-values': [u'ConductionTransferFunction',
                                                           u'MoisturePenetrationDepthConductionTransferFunction',
                                                           u'ConductionFiniteDifference',
                                                           u'CombinedHeatAndMoistureFiniteElement'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'surface temperature upper limit',
                                      {'name': u'Surface Temperature Upper Limit',
                                       'pyname': u'surface_temperature_upper_limit',
                                       'default': 200.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 200.0,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'C'}),
                                     (u'minimum surface convection heat transfer coefficient value',
                                      {'name': u'Minimum Surface Convection Heat Transfer Coefficient Value',
                                       'pyname': u'minimum_surface_convection_heat_transfer_coefficient_value',
                                       'default': 0.1,
                                       'minimum>': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'W/m2-K'}),
                                     (u'maximum surface convection heat transfer coefficient value',
                                      {'name': u'Maximum Surface Convection Heat Transfer Coefficient Value',
                                       'pyname': u'maximum_surface_convection_heat_transfer_coefficient_value',
                                       'default': 1000.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 1.0,
                                       'autocalculatable': False,
                                       'type': 'real',
                                       'unit': u'W/m2-K'})]),
              'format': u'singleline',
              'group': u'Simulation Parameters',
              'min-fields': 0,
              'name': u'HeatBalanceAlgorithm',
              'pyname': u'HeatBalanceAlgorithm',
              'required-object': False,
              'unique-object': True}

    @property
    def algorithm(self):
        """Get algorithm.

        Returns:
            str: the value of `algorithm` or None if not set

        """
        return self["Algorithm"]

    @algorithm.setter
    def algorithm(self, value="ConductionTransferFunction"):
        """Corresponds to IDD field `Algorithm`

        Args:
            value (str): value for IDD Field `Algorithm`
                Default value: ConductionTransferFunction
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Algorithm"] = value

    @property
    def surface_temperature_upper_limit(self):
        """Get surface_temperature_upper_limit.

        Returns:
            float: the value of `surface_temperature_upper_limit` or None if not set

        """
        return self["Surface Temperature Upper Limit"]

    @surface_temperature_upper_limit.setter
    def surface_temperature_upper_limit(self, value=200.0):
        """Corresponds to IDD field `Surface Temperature Upper Limit`

        Args:
            value (float): value for IDD Field `Surface Temperature Upper Limit`
                Units: C
                Default value: 200.0
                value >= 200.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Surface Temperature Upper Limit"] = value

    @property
    def minimum_surface_convection_heat_transfer_coefficient_value(self):
        """Get minimum_surface_convection_heat_transfer_coefficient_value.

        Returns:
            float: the value of `minimum_surface_convection_heat_transfer_coefficient_value` or None if not set

        """
        return self[
            "Minimum Surface Convection Heat Transfer Coefficient Value"]

    @minimum_surface_convection_heat_transfer_coefficient_value.setter
    def minimum_surface_convection_heat_transfer_coefficient_value(
            self,
            value=0.1):
        """Corresponds to IDD field `Minimum Surface Convection Heat Transfer
        Coefficient Value`

        Args:
            value (float): value for IDD Field `Minimum Surface Convection Heat Transfer Coefficient Value`
                Units: W/m2-K
                Default value: 0.1
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self[
            "Minimum Surface Convection Heat Transfer Coefficient Value"] = value

    @property
    def maximum_surface_convection_heat_transfer_coefficient_value(self):
        """Get maximum_surface_convection_heat_transfer_coefficient_value.

        Returns:
            float: the value of `maximum_surface_convection_heat_transfer_coefficient_value` or None if not set

        """
        return self[
            "Maximum Surface Convection Heat Transfer Coefficient Value"]

    @maximum_surface_convection_heat_transfer_coefficient_value.setter
    def maximum_surface_convection_heat_transfer_coefficient_value(
            self,
            value=1000.0):
        """Corresponds to IDD field `Maximum Surface Convection Heat Transfer
        Coefficient Value`

        Args:
            value (float): value for IDD Field `Maximum Surface Convection Heat Transfer Coefficient Value`
                Units: W/m2-K
                Default value: 1000.0
                value >= 1.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self[
            "Maximum Surface Convection Heat Transfer Coefficient Value"] = value




class HeatBalanceSettingsConductionFiniteDifference(DataObject):

    """ Corresponds to IDD object `HeatBalanceSettings:ConductionFiniteDifference`
        Determines settings for the Conduction Finite Difference
        algorithm for surface heat transfer modeling.
    """
    schema = {'extensible-fields': OrderedDict(),
              'fields': OrderedDict([(u'difference scheme',
                                      {'name': u'Difference Scheme',
                                       'pyname': u'difference_scheme',
                                       'default': u'FullyImplicitFirstOrder',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'CrankNicholsonSecondOrder',
                                                           u'FullyImplicitFirstOrder'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'space discretization constant',
                                      {'name': u'Space Discretization Constant',
                                       'pyname': u'space_discretization_constant',
                                       'default': 3.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'relaxation factor',
                                      {'name': u'Relaxation Factor',
                                       'pyname': u'relaxation_factor',
                                       'default': 1.0,
                                       'maximum': 1.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0.01,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'inside face surface temperature convergence criteria',
                                      {'name': u'Inside Face Surface Temperature Convergence Criteria',
                                       'pyname': u'inside_face_surface_temperature_convergence_criteria',
                                       'default': 0.002,
                                       'maximum': 0.01,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 1e-07,
                                       'autocalculatable': False,
                                       'type': u'real'})]),
              'format': None,
              'group': u'Simulation Parameters',
              'min-fields': 0,
              'name': u'HeatBalanceSettings:ConductionFiniteDifference',
              'pyname': u'HeatBalanceSettingsConductionFiniteDifference',
              'required-object': False,
              'unique-object': True}

    @property
    def difference_scheme(self):
        """Get difference_scheme.

        Returns:
            str: the value of `difference_scheme` or None if not set

        """
        return self["Difference Scheme"]

    @difference_scheme.setter
    def difference_scheme(self, value="FullyImplicitFirstOrder"):
        """Corresponds to IDD field `Difference Scheme`

        Args:
            value (str): value for IDD Field `Difference Scheme`
                Default value: FullyImplicitFirstOrder
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Difference Scheme"] = value

    @property
    def space_discretization_constant(self):
        """Get space_discretization_constant.

        Returns:
            float: the value of `space_discretization_constant` or None if not set

        """
        return self["Space Discretization Constant"]

    @space_discretization_constant.setter
    def space_discretization_constant(self, value=3.0):
        """Corresponds to IDD field `Space Discretization Constant` increase or
        decrease number of nodes.

        Args:
            value (float): value for IDD Field `Space Discretization Constant`
                Default value: 3.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Space Discretization Constant"] = value

    @property
    def relaxation_factor(self):
        """Get relaxation_factor.

        Returns:
            float: the value of `relaxation_factor` or None if not set

        """
        return self["Relaxation Factor"]

    @relaxation_factor.setter
    def relaxation_factor(self, value=1.0):
        """Corresponds to IDD field `Relaxation Factor`

        Args:
            value (float): value for IDD Field `Relaxation Factor`
                Default value: 1.0
                value >= 0.01
                value <= 1.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Relaxation Factor"] = value

    @property
    def inside_face_surface_temperature_convergence_criteria(self):
        """Get inside_face_surface_temperature_convergence_criteria.

        Returns:
            float: the value of `inside_face_surface_temperature_convergence_criteria` or None if not set

        """
        return self["Inside Face Surface Temperature Convergence Criteria"]

    @inside_face_surface_temperature_convergence_criteria.setter
    def inside_face_surface_temperature_convergence_criteria(
            self,
            value=0.002):
        """Corresponds to IDD field `Inside Face Surface Temperature
        Convergence Criteria`

        Args:
            value (float): value for IDD Field `Inside Face Surface Temperature Convergence Criteria`
                Default value: 0.002
                value >= 1e-07
                value <= 0.01
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Inside Face Surface Temperature Convergence Criteria"] = value




class ZoneAirHeatBalanceAlgorithm(DataObject):

    """Corresponds to IDD object `ZoneAirHeatBalanceAlgorithm` Determines which
    algorithm will be used to solve the zone air heat balance."""
    schema = {'extensible-fields': OrderedDict(),
              'fields': OrderedDict([(u'algorithm',
                                      {'name': u'Algorithm',
                                       'pyname': u'algorithm',
                                       'default': u'ThirdOrderBackwardDifference',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'ThirdOrderBackwardDifference',
                                                           u'AnalyticalSolution',
                                                           u'EulerMethod'],
                                       'autocalculatable': False,
                                       'type': 'alpha'})]),
              'format': u'singleline',
              'group': u'Simulation Parameters',
              'min-fields': 0,
              'name': u'ZoneAirHeatBalanceAlgorithm',
              'pyname': u'ZoneAirHeatBalanceAlgorithm',
              'required-object': False,
              'unique-object': True}

    @property
    def algorithm(self):
        """Get algorithm.

        Returns:
            str: the value of `algorithm` or None if not set

        """
        return self["Algorithm"]

    @algorithm.setter
    def algorithm(self, value="ThirdOrderBackwardDifference"):
        """Corresponds to IDD field `Algorithm`

        Args:
            value (str): value for IDD Field `Algorithm`
                Default value: ThirdOrderBackwardDifference
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Algorithm"] = value




class ZoneAirContaminantBalance(DataObject):

    """Corresponds to IDD object `ZoneAirContaminantBalance` Determines which
    contaminant concentration will be simulates."""
    schema = {'extensible-fields': OrderedDict(),
              'fields': OrderedDict([(u'carbon dioxide concentration',
                                      {'name': u'Carbon Dioxide Concentration',
                                       'pyname': u'carbon_dioxide_concentration',
                                       'default': u'No',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'Yes',
                                                           u'No'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'outdoor carbon dioxide schedule name',
                                      {'name': u'Outdoor Carbon Dioxide Schedule Name',
                                       'pyname': u'outdoor_carbon_dioxide_schedule_name',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'}),
                                     (u'generic contaminant concentration',
                                      {'name': u'Generic Contaminant Concentration',
                                       'pyname': u'generic_contaminant_concentration',
                                       'default': u'No',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'Yes',
                                                           u'No'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'outdoor generic contaminant schedule name',
                                      {'name': u'Outdoor Generic Contaminant Schedule Name',
                                       'pyname': u'outdoor_generic_contaminant_schedule_name',
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'object-list'})]),
              'format': u'singleline',
              'group': u'Simulation Parameters',
              'min-fields': 0,
              'name': u'ZoneAirContaminantBalance',
              'pyname': u'ZoneAirContaminantBalance',
              'required-object': False,
              'unique-object': True}

    @property
    def carbon_dioxide_concentration(self):
        """Get carbon_dioxide_concentration.

        Returns:
            str: the value of `carbon_dioxide_concentration` or None if not set

        """
        return self["Carbon Dioxide Concentration"]

    @carbon_dioxide_concentration.setter
    def carbon_dioxide_concentration(self, value="No"):
        """Corresponds to IDD field `Carbon Dioxide Concentration` If Yes, CO2
        simulation will be performed.

        Args:
            value (str): value for IDD Field `Carbon Dioxide Concentration`
                Default value: No
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Carbon Dioxide Concentration"] = value

    @property
    def outdoor_carbon_dioxide_schedule_name(self):
        """Get outdoor_carbon_dioxide_schedule_name.

        Returns:
            str: the value of `outdoor_carbon_dioxide_schedule_name` or None if not set

        """
        return self["Outdoor Carbon Dioxide Schedule Name"]

    @outdoor_carbon_dioxide_schedule_name.setter
    def outdoor_carbon_dioxide_schedule_name(self, value=None):
        """Corresponds to IDD field `Outdoor Carbon Dioxide Schedule Name`
        Schedule values should be in parts per million (ppm)

        Args:
            value (str): value for IDD Field `Outdoor Carbon Dioxide Schedule Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Outdoor Carbon Dioxide Schedule Name"] = value

    @property
    def generic_contaminant_concentration(self):
        """Get generic_contaminant_concentration.

        Returns:
            str: the value of `generic_contaminant_concentration` or None if not set

        """
        return self["Generic Contaminant Concentration"]

    @generic_contaminant_concentration.setter
    def generic_contaminant_concentration(self, value="No"):
        """Corresponds to IDD field `Generic Contaminant Concentration` If Yes,
        generic contaminant simulation will be performed.

        Args:
            value (str): value for IDD Field `Generic Contaminant Concentration`
                Default value: No
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Generic Contaminant Concentration"] = value

    @property
    def outdoor_generic_contaminant_schedule_name(self):
        """Get outdoor_generic_contaminant_schedule_name.

        Returns:
            str: the value of `outdoor_generic_contaminant_schedule_name` or None if not set

        """
        return self["Outdoor Generic Contaminant Schedule Name"]

    @outdoor_generic_contaminant_schedule_name.setter
    def outdoor_generic_contaminant_schedule_name(self, value=None):
        """Corresponds to IDD field `Outdoor Generic Contaminant Schedule Name`
        Schedule values should be generic contaminant concentration in parts
        per million (ppm)

        Args:
            value (str): value for IDD Field `Outdoor Generic Contaminant Schedule Name`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Outdoor Generic Contaminant Schedule Name"] = value




class ZoneAirMassFlowConservation(DataObject):

    """Corresponds to IDD object `ZoneAirMassFlowConservation` Enforces the
    zone air mass flow balance by adjusting zone mixing object flow rates.

    The infiltration object mass flow rate may also be adjusted or may
    add infiltration air flow to the base infiltration air flow for
    source zones only.

    """
    schema = {'extensible-fields': OrderedDict(),
              'fields': OrderedDict([(u'adjust zone mixing for zone air mass flow balance',
                                      {'name': u'Adjust Zone Mixing For Zone Air Mass Flow Balance',
                                       'pyname': u'adjust_zone_mixing_for_zone_air_mass_flow_balance',
                                       'default': u'No',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'Yes',
                                                           u'No'],
                                       'autocalculatable': False,
                                       'type': 'alpha'}),
                                     (u'source zone infiltration treatment',
                                      {'name': u'Source Zone Infiltration Treatment',
                                       'pyname': u'source_zone_infiltration_treatment',
                                       'default': u'AddInfiltrationFlow',
                                       'required-field': False,
                                       'autosizable': False,
                                       'accepted-values': [u'AddInfiltrationFlow',
                                                           u'AdjustInfiltrationFlow'],
                                       'autocalculatable': False,
                                       'type': 'alpha'})]),
              'format': None,
              'group': u'Simulation Parameters',
              'min-fields': 0,
              'name': u'ZoneAirMassFlowConservation',
              'pyname': u'ZoneAirMassFlowConservation',
              'required-object': False,
              'unique-object': True}

    @property
    def adjust_zone_mixing_for_zone_air_mass_flow_balance(self):
        """Get adjust_zone_mixing_for_zone_air_mass_flow_balance.

        Returns:
            str: the value of `adjust_zone_mixing_for_zone_air_mass_flow_balance` or None if not set

        """
        return self["Adjust Zone Mixing For Zone Air Mass Flow Balance"]

    @adjust_zone_mixing_for_zone_air_mass_flow_balance.setter
    def adjust_zone_mixing_for_zone_air_mass_flow_balance(self, value="No"):
        """  Corresponds to IDD field `Adjust Zone Mixing For Zone Air Mass Flow Balance`
        If Yes, Zone mixing object flow rates are adjusted to balance the zone air mass flow
        and additional infiltration air flow may be added if required in order to balance the
        zone air mass flow.
        This optional choice input field allows users triggering the zone air mass flow
        balance calculation when desired. This global object has two choice KEYs: Yes and
        No. If this input field is specified as Yes, then EnergyPlus attempts to enforce
        the zone air mass flow conservation, or else if it is specified as No, then EnergyPlus
        calculation defaults to zone air mass flow balance that does not include zone mixing
        objects and that assumes self-balanced simple flow objects per the default procedure,
        which may not necessarily enforce zone mass conservation unless the user specified
        a balanced flow to begin with. Mass conservation is enforced both for the receiving
        and source zones if there is at least one mixing object defined. The default input
        is No. (Note that No input may also results in balanced flow depending on the
        system specified).

        Args:
            value (str): value for IDD Field `Adjust Zone Mixing For Zone Air Mass Flow Balance`
                Default value: No
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Adjust Zone Mixing For Zone Air Mass Flow Balance"] = value

    @property
    def source_zone_infiltration_treatment(self):
        """Get source_zone_infiltration_treatment.

        Returns:
            str: the value of `source_zone_infiltration_treatment` or None if not set

        """
        return self["Source Zone Infiltration Treatment"]

    @source_zone_infiltration_treatment.setter
    def source_zone_infiltration_treatment(self, value="AddInfiltrationFlow"):
        """  Corresponds to IDD field `Source Zone Infiltration Treatment`
        This input field allows user to choose how zone infiltration flow is treated during
        the zone air mass flow balance calculation.
        It has two choice KEYs: AddInfiltrationFlow and AdjustInfiltrationFlow.  If this
        input is specified as AddInfiltrationFlow, then energy plus adds infiltration air
        mass flow on top of the base flow, which is calculated using the infiltration object
        user inputs, in order to balance the zone air mass flow.  The additional infiltration
        air mass flow is not self-balanced.  If this input is specified as
        AdjustInfiltrationFlow, then energy plus may adjust the base flow calculated using
        the infiltration object user inputs in order to balance the zone air mass flow. If it
        is not required to adjust the base infiltration air flow calculated from the user
        specified infiltration object inputs, then the base infiltration air mass flow
        is assumed self-balanced. If the above input field specified as "No", then this input
        field has no impact on the simulation.

        Args:
            value (str): value for IDD Field `Source Zone Infiltration Treatment`
                Default value: AddInfiltrationFlow
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Source Zone Infiltration Treatment"] = value




class ZoneCapacitanceMultiplierResearchSpecial(DataObject):

    """ Corresponds to IDD object `ZoneCapacitanceMultiplier:ResearchSpecial`
        Multiplier altering the relative capacitance of the air compared to an empty zone
    """
    schema = {'extensible-fields': OrderedDict(),
              'fields': OrderedDict([(u'temperature capacity multiplier',
                                      {'name': u'Temperature Capacity Multiplier',
                                       'pyname': u'temperature_capacity_multiplier',
                                       'default': 1.0,
                                       'minimum>': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'humidity capacity multiplier',
                                      {'name': u'Humidity Capacity Multiplier',
                                       'pyname': u'humidity_capacity_multiplier',
                                       'default': 1.0,
                                       'minimum>': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'carbon dioxide capacity multiplier',
                                      {'name': u'Carbon Dioxide Capacity Multiplier',
                                       'pyname': u'carbon_dioxide_capacity_multiplier',
                                       'default': 1.0,
                                       'minimum>': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'}),
                                     (u'generic contaminant capacity multiplier',
                                      {'name': u'Generic Contaminant Capacity Multiplier',
                                       'pyname': u'generic_contaminant_capacity_multiplier',
                                       'default': 1.0,
                                       'minimum>': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real'})]),
              'format': u'singleline',
              'group': u'Simulation Parameters',
              'min-fields': 4,
              'name': u'ZoneCapacitanceMultiplier:ResearchSpecial',
              'pyname': u'ZoneCapacitanceMultiplierResearchSpecial',
              'required-object': False,
              'unique-object': True}

    @property
    def temperature_capacity_multiplier(self):
        """Get temperature_capacity_multiplier.

        Returns:
            float: the value of `temperature_capacity_multiplier` or None if not set

        """
        return self["Temperature Capacity Multiplier"]

    @temperature_capacity_multiplier.setter
    def temperature_capacity_multiplier(self, value=1.0):
        """Corresponds to IDD field `Temperature Capacity Multiplier` Used to
        alter the capacitance of zone air with respect to heat or temperature.

        Args:
            value (float): value for IDD Field `Temperature Capacity Multiplier`
                Default value: 1.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Temperature Capacity Multiplier"] = value

    @property
    def humidity_capacity_multiplier(self):
        """Get humidity_capacity_multiplier.

        Returns:
            float: the value of `humidity_capacity_multiplier` or None if not set

        """
        return self["Humidity Capacity Multiplier"]

    @humidity_capacity_multiplier.setter
    def humidity_capacity_multiplier(self, value=1.0):
        """Corresponds to IDD field `Humidity Capacity Multiplier` Used to
        alter the capacitance of zone air with respect to moisture or humidity
        ratio.

        Args:
            value (float): value for IDD Field `Humidity Capacity Multiplier`
                Default value: 1.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Humidity Capacity Multiplier"] = value

    @property
    def carbon_dioxide_capacity_multiplier(self):
        """Get carbon_dioxide_capacity_multiplier.

        Returns:
            float: the value of `carbon_dioxide_capacity_multiplier` or None if not set

        """
        return self["Carbon Dioxide Capacity Multiplier"]

    @carbon_dioxide_capacity_multiplier.setter
    def carbon_dioxide_capacity_multiplier(self, value=1.0):
        """Corresponds to IDD field `Carbon Dioxide Capacity Multiplier` Used
        to alter the capacitance of zone air with respect to zone air carbob
        dioxide concentration.

        Args:
            value (float): value for IDD Field `Carbon Dioxide Capacity Multiplier`
                Default value: 1.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Carbon Dioxide Capacity Multiplier"] = value

    @property
    def generic_contaminant_capacity_multiplier(self):
        """Get generic_contaminant_capacity_multiplier.

        Returns:
            float: the value of `generic_contaminant_capacity_multiplier` or None if not set

        """
        return self["Generic Contaminant Capacity Multiplier"]

    @generic_contaminant_capacity_multiplier.setter
    def generic_contaminant_capacity_multiplier(self, value=1.0):
        """Corresponds to IDD field `Generic Contaminant Capacity Multiplier`
        Used to alter the capacitance of zone air with respect to zone air
        generic contaminant concentration.

        Args:
            value (float): value for IDD Field `Generic Contaminant Capacity Multiplier`
                Default value: 1.0
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Generic Contaminant Capacity Multiplier"] = value




class Timestep(DataObject):

    """Corresponds to IDD object `Timestep` Specifies the "basic" timestep for
    the simulation.

    The value entered here is also known as the Zone Timestep.  This is
    used in the Zone Heat Balance Model calculation as the driving
    timestep for heat transfer and load calculations.

    """
    schema = {'extensible-fields': OrderedDict(),
              'fields': OrderedDict([(u'number of timesteps per hour',
                                      {'name': u'Number of Timesteps per Hour',
                                       'pyname': u'number_of_timesteps_per_hour',
                                       'default': 6,
                                       'maximum': 60,
                                       'required-field': True,
                                       'autosizable': False,
                                       'minimum': 1,
                                       'autocalculatable': False,
                                       'type': u'integer'})]),
              'format': u'singleline',
              'group': u'Simulation Parameters',
              'min-fields': 0,
              'name': u'Timestep',
              'pyname': u'Timestep',
              'required-object': False,
              'unique-object': True}

    @property
    def number_of_timesteps_per_hour(self):
        """Get number_of_timesteps_per_hour.

        Returns:
            int: the value of `number_of_timesteps_per_hour` or None if not set

        """
        return self["Number of Timesteps per Hour"]

    @number_of_timesteps_per_hour.setter
    def number_of_timesteps_per_hour(self, value=6):
        """  Corresponds to IDD field `Number of Timesteps per Hour`
        Number in hour: normal validity 4 to 60: 6 suggested
        Must be evenly divisible into 60
        Allowable values include 1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 30, and 60
        Normal 6 is mimimum as lower values may cause inaccuracies
        A minimum value of 20 is suggested for both ConductionFiniteDifference
        and CombinedHeatAndMoistureFiniteElement surface heat balance alogorithms
        A minimum of 12 is suggested for simulations involving a Vegetated Roof (Material:RoofVegetation).

        Args:
            value (int): value for IDD Field `Number of Timesteps per Hour`
                Default value: 6
                value >= 1
                value <= 60
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Number of Timesteps per Hour"] = value




class ConvergenceLimits(DataObject):

    """Corresponds to IDD object `ConvergenceLimits` Specifies limits on HVAC
    system simulation timesteps and iterations.

    This item is an advanced feature that should be used only with
    caution.

    """
    schema = {'extensible-fields': OrderedDict(),
              'fields': OrderedDict([(u'minimum system timestep',
                                      {'name': u'Minimum System Timestep',
                                       'pyname': u'minimum_system_timestep',
                                       'maximum': 60,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0,
                                       'autocalculatable': False,
                                       'type': u'integer',
                                       'unit': u'minutes'}),
                                     (u'maximum hvac iterations',
                                      {'name': u'Maximum HVAC Iterations',
                                       'pyname': u'maximum_hvac_iterations',
                                       'default': 20,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 1,
                                       'autocalculatable': False,
                                       'type': u'integer'}),
                                     (u'minimum plant iterations',
                                      {'name': u'Minimum Plant Iterations',
                                       'pyname': u'minimum_plant_iterations',
                                       'default': 2,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 1,
                                       'autocalculatable': False,
                                       'type': u'integer'}),
                                     (u'maximum plant iterations',
                                      {'name': u'Maximum Plant Iterations',
                                       'pyname': u'maximum_plant_iterations',
                                       'default': 8,
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 2,
                                       'autocalculatable': False,
                                       'type': u'integer'})]),
              'format': None,
              'group': u'Simulation Parameters',
              'min-fields': 0,
              'name': u'ConvergenceLimits',
              'pyname': u'ConvergenceLimits',
              'required-object': False,
              'unique-object': True}

    @property
    def minimum_system_timestep(self):
        """Get minimum_system_timestep.

        Returns:
            int: the value of `minimum_system_timestep` or None if not set

        """
        return self["Minimum System Timestep"]

    @minimum_system_timestep.setter
    def minimum_system_timestep(self, value=None):
        """  Corresponds to IDD field `Minimum System Timestep`
        0 sets the minimum to the zone timestep (ref: Timestep)
        1 is normal (ratchet down to 1 minute)
        setting greater than zone timestep (in minutes) will effectively set to zone timestep

        Args:
            value (int): value for IDD Field `Minimum System Timestep`
                Units: minutes
                value <= 60
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Minimum System Timestep"] = value

    @property
    def maximum_hvac_iterations(self):
        """Get maximum_hvac_iterations.

        Returns:
            int: the value of `maximum_hvac_iterations` or None if not set

        """
        return self["Maximum HVAC Iterations"]

    @maximum_hvac_iterations.setter
    def maximum_hvac_iterations(self, value=20):
        """Corresponds to IDD field `Maximum HVAC Iterations`

        Args:
            value (int): value for IDD Field `Maximum HVAC Iterations`
                Default value: 20
                value >= 1
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Maximum HVAC Iterations"] = value

    @property
    def minimum_plant_iterations(self):
        """Get minimum_plant_iterations.

        Returns:
            int: the value of `minimum_plant_iterations` or None if not set

        """
        return self["Minimum Plant Iterations"]

    @minimum_plant_iterations.setter
    def minimum_plant_iterations(self, value=2):
        """  Corresponds to IDD field `Minimum Plant Iterations`
        Controls the minimum number of plant system solver iterations within a single HVAC iteration
        Larger values will increase runtime but might improve solution accuracy for complicated plant systems
        Complex plants include: several interconnected loops, heat recovery, thermal load following generators, etc.

        Args:
            value (int): value for IDD Field `Minimum Plant Iterations`
                Default value: 2
                value >= 1
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Minimum Plant Iterations"] = value

    @property
    def maximum_plant_iterations(self):
        """Get maximum_plant_iterations.

        Returns:
            int: the value of `maximum_plant_iterations` or None if not set

        """
        return self["Maximum Plant Iterations"]

    @maximum_plant_iterations.setter
    def maximum_plant_iterations(self, value=8):
        """Corresponds to IDD field `Maximum Plant Iterations` Controls the
        maximum number of plant system solver iterations within a single HVAC
        iteration Smaller values might decrease runtime but could decrease
        solution accuracy for complicated plant systems.

        Args:
            value (int): value for IDD Field `Maximum Plant Iterations`
                Default value: 8
                value >= 2
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value

        """
        self["Maximum Plant Iterations"] = value




class ProgramControl(DataObject):

    """Corresponds to IDD object `ProgramControl` used to support various
    efforts in time reduction for simulation including threading."""
    schema = {'extensible-fields': OrderedDict(),
              'fields': OrderedDict([(u'number of threads allowed',
                                      {'name': u'Number of Threads Allowed',
                                       'pyname': u'number_of_threads_allowed',
                                       'required-field': False,
                                       'autosizable': False,
                                       'minimum': 0,
                                       'autocalculatable': False,
                                       'type': u'integer'})]),
              'format': None,
              'group': u'Simulation Parameters',
              'min-fields': 0,
              'name': u'ProgramControl',
              'pyname': u'ProgramControl',
              'required-object': False,
              'unique-object': False}

    @property
    def number_of_threads_allowed(self):
        """Get number_of_threads_allowed.

        Returns:
            int: the value of `number_of_threads_allowed` or None if not set

        """
        return self["Number of Threads Allowed"]

    @number_of_threads_allowed.setter
    def number_of_threads_allowed(self, value=None):
        """  Corresponds to IDD field `Number of Threads Allowed`
        This is currently used only in the Interior Radiant Exchange module -- view factors on # surfaces
        if value is 0, then maximum number allowed will be used.

        Args:
            value (int): value for IDD Field `Number of Threads Allowed`
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Number of Threads Allowed"] = value


