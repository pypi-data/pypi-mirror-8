#!/usr/bin/python
"""
WARNING: This is an automatically generated file.
It is based on a modified Energy+.idd specification file.

Do not expect (yet) that it actually works!

Generation date: 2014-12-08

"""
import six
import re
import logging
import pyidf
import datetime
from collections import OrderedDict
from pyidf.internal_gains import *
from pyidf.water_heaters_and_thermal_storage import *
from pyidf.demand_limiting_controls import *
from pyidf.variable_refrigerant_flow_equipment import *
from pyidf.condenser_equipment_and_heat_exchangers import *
from pyidf.exterior_equipment import *
from pyidf.energy_management_system import *
from pyidf.schedules import *
from pyidf.non import *
from pyidf.location_and_climate import *
from pyidf.unitary_equipment import *
from pyidf.economics import *
from pyidf.zone_hvac_radiative import *
from pyidf.parametrics import *
from pyidf.external_interface import *
from pyidf.performance_tables import *
from pyidf.water_systems import *
from pyidf.fluid_properties import *
from pyidf.coils import *
from pyidf.evaporative_coolers import *
from pyidf.humidifiers_and_dehumidifiers import *
from pyidf.zone_hvac_controls_and_thermostats import *
from pyidf.simulation_parameters import *
from pyidf.operational_faults import *
from pyidf.performance_curves import *
from pyidf.output_reporting import *
from pyidf.fans import *
from pyidf.compliance_objects import *
from pyidf.refrigeration import *
from pyidf.advanced_construction import *
from pyidf.heat_recovery import *
from pyidf.daylighting import *
from pyidf.node import *
from pyidf.plant import *
from pyidf.zone_hvac_forced_air_units import *
from pyidf.plant_heating_and_cooling_equipment import *
from pyidf.solar_collectors import *
from pyidf.zone_hvac_air_loop_terminal_units import *
from pyidf.surface_construction_elements import *
from pyidf.pumps import *
from pyidf.zone_hvac_equipment_connections import *
from pyidf.setpoint_managers import *
from pyidf.hvac_design_objects import *
from pyidf.zone_airflow import *
from pyidf.room_air_models import *
from pyidf.user_defined_hvac_and_plant_component_models import *
from pyidf.thermal_zones_and_surfaces import *
from pyidf.system_availability_managers import *
from pyidf.natural_ventilation_and_duct_leakage import *
from pyidf.detailed_ground_heat_transfer import *
from pyidf.air_distribution import *
from pyidf.controllers import *
from pyidf.hvac_templates import *
from pyidf.energyplus import *
from pyidf.electric_load_center import *


logger = logging.getLogger("pyidf")
logger.addHandler(logging.NullHandler())


class IDF(object):

    """Represents an EnergyPlus IDF input file."""

    required_objects = ["building", "globalgeometryrules"]
    unique_objects = [
        "zoneairheatbalancealgorithm",
        "surfaceconvectionalgorithm:outside:adaptivemodelselections",
        "outputcontrol:sizing:style",
        "runperiodcontrol:daylightsavingtime",
        "building",
        "zoneairmassflowconservation",
        "zoneaircontaminantbalance",
        "site:groundtemperature:shallow",
        "site:solarandvisiblespectrum",
        "output:debuggingdata",
        "outputcontrol:illuminancemap:style",
        "site:heightvariation",
        "lifecyclecost:parameters",
        "timestep",
        "convergencelimits",
        "heatbalancesettings:conductionfinitedifference",
        "version",
        "airflownetwork:simulationcontrol",
        "site:weatherstation",
        "globalgeometryrules",
        "output:energymanagementsystem",
        "shadowcalculation",
        "site:groundreflectance",
        "site:groundtemperature:buildingsurface",
        "surfaceconvectionalgorithm:inside",
        "hvactemplate:plant:chilledwaterloop",
        "site:location",
        "parametric:logic",
        "parametric:runcontrol",
        "surfaceconvectionalgorithm:inside:adaptivemodelselections",
        "zonecapacitancemultiplier:researchspecial",
        "compliance:building",
        "sizing:parameters",
        "hvactemplate:plant:hotwaterloop",
        "site:groundtemperature:deep",
        "hvactemplate:plant:mixedwaterloop",
        "outputcontrol:reportingtolerances",
        "simulationcontrol",
        "output:sqlite",
        "site:groundtemperature:fcfactormethod",
        "heatbalancealgorithm",
        "parametric:filenamesuffix",
        "geometrytransform",
        "outputcontrol:table:style",
        "surfaceconvectionalgorithm:outside",
        "output:table:summaryreports",
        "currencytype"]

    def __init__(self, path=None):
        """Inits IDF object."""
        self._data = OrderedDict()
        self.comment_headers = []

        if path is not None:
            self.read(path)

    def add(self, dataobject):
        """Adds a data object to the IDF. If data object is unique, it replaces
        an eventual existing data object.

        Args:
            dataobject: the data object

        """
        group = dataobject.schema['group']
        if group not in self._data:
            self._data[group] = OrderedDict()

        lower_name = dataobject.schema['name'].lower()
        if lower_name not in self._data[group]:
            self._data[group][lower_name] = []
        if lower_name in self.unique_objects:
            self._data[group][lower_name] = [dataobject]
        else:
            self._data[group][lower_name].append(dataobject)

    def save(self, path, check=True):
        """Save data to path.

        Args:
            path (str): path where data should be save

        Raises:
            ValueError: if required objects are not present or
                unique objects are not unique

        """
        with open(path, 'w') as f:
            if check:
                for group in self._data:
                    for key in self._data[group]:
                        if len(
                                self._data[group][key]) == 0 and key in self.required_objects:
                            raise ValueError('{} is not valid.'.format(key))
                        if key in self.unique_objects and len(
                                self._data[group][key]) > 1:
                            raise ValueError(
                                '{} is not unique: {}'.format(
                                    key, len(
                                        self._data[group][key])))
                        for obj in self._data[group][key]:
                            obj.check(strict=True)

            f.write(
                "!- Generated with pyidf version {}, "
                "generation date: {}\n".format(
                    pyidf.__version__, str(
                        datetime.datetime.now())))
            f.write("!- Validation level: {}\n".format(pyidf.validation_level))

            if len(self.comment_headers) > 0:
                f.write("\n!- Previous comments:\n\n")
                for comment in self.comment_headers:
                    f.write("{}\n".format(comment))

            for group in self._data:
                f.write(
                    "\n!-   ===========  ALL OBJECTS OF GROUP: {}  ===========\n".format(group))
                for key in self._data[group]:
                    if len(self._data[group][key]) > 0:
                        for dobj in self._data[group][key]:
                            if dobj.schema['format'] == "singleline":
                                vals = [dobj.schema['name']]
                                vals += [v[1] for v in dobj.export()]
                                f.write("\n  {};\n".format(",".join(vals)))
                            elif dobj.schema['format'] == "vertices":
                                f.write(
                                    "\n  {},\n".format(
                                        dobj.schema['name']))
                                vals = dobj.export()
                                cval = len(vals)
                                i = 0
                                while i < cval:

                                    if ((i +
                                         2) < cval and "x" in vals[i][0].lower() and "y" in vals[i +
                                                                                                 1][0].lower() and "z" in vals[i +
                                                                                                                               2][0].lower()):
                                        val = ",".join(
                                            [vals[i][1], vals[i + 1][1], vals[i + 2][1]])
                                        comment = ",".join(
                                            [vals[i][0], vals[i + 1][0], vals[i + 2][0]])
                                        i += 3
                                    else:
                                        val = vals[i][1]
                                        comment = vals[i][0]
                                        i += 1

                                    sep = ','
                                    if i >= cval:
                                        sep = ';'
                                    blanks = ' ' * \
                                        max(30 - 4 - len(val) - 2, 2)

                                    f.write(
                                        "    {val}{sep}{blanks}!- {comment}\n".format(
                                            val=val,
                                            sep=sep,
                                            blanks=blanks,
                                            comment=comment))
                            elif dobj.schema['format'] == "compactschedule":
                                f.write(
                                    "\n  {},\n".format(
                                        dobj.schema['name']))
                                vals = dobj.export()
                                cval = len(vals)
                                i = 0
                                while i < cval:

                                    if "until" in vals[i][1].lower():
                                        j = i + 1
                                        while j < cval:
                                            jval = vals[j][1].lower()
                                            if "for" in jval or "until" in jval:
                                                break
                                            j += 1
                                        val = ",".join(
                                            [vals[i][1]] + [vals[t][1] for t in range(i + 1, j)])
                                        comment = "Fields {} - {}".format(
                                            i +
                                            1,
                                            j +
                                            1)
                                        i += (j - i)
                                    else:
                                        val = vals[i][1]
                                        comment = vals[i][0]
                                        i += 1

                                    sep = ','
                                    if i >= cval:
                                        sep = ';'
                                    blanks = ' ' * \
                                        max(30 - 4 - len(val) - 2, 2)

                                    f.write(
                                        "    {val}{sep}{blanks}!- {comment}\n".format(
                                            val=val,
                                            sep=sep,
                                            blanks=blanks,
                                            comment=comment))
                            elif dobj.schema['format'] == "fluidproperty":

                                f.write(
                                    "\n  {},\n".format(
                                        dobj.schema['name']))
                                vals = dobj.export()
                                cval = len(vals)
                                i = 0
                                while i < cval:

                                    is_fluidprops = True
                                    for j in range(min(7, cval - i)):

                                        # Test the next values
                                        fluidprops_match = re.search(
                                            r"([0-9]|value|property)",
                                            vals[
                                                i +
                                                j][0])
                                        if fluidprops_match is None:
                                            is_fluidprops = False
                                            break

                                    if is_fluidprops:
                                        val = ",".join(
                                            [vals[i + j][1] for j in range(min(7, cval - i))])
                                        comment = ""
                                        i += min(7, cval - i)
                                    else:
                                        val = vals[i][1]
                                        comment = vals[i][0]
                                        i += 1

                                    sep = ','
                                    if i >= cval:
                                        sep = ';'
                                    blanks = ' ' * \
                                        max(30 - 4 - len(val) - 2, 2)

                                    f.write(
                                        "    {val}{sep}{blanks}!- {comment}\n".format(
                                            val=val,
                                            sep=sep,
                                            blanks=blanks,
                                            comment=comment))
                            elif dobj.schema['format'] == "spectral":
                                f.write(
                                    "\n  {},\n".format(
                                        dobj.schema['name']))
                                vals = dobj.export()
                                cval = len(vals)
                                i = 0
                                while i < cval:

                                    start = i
                                    end = min(i + 4, cval)

                                    if False not in [
                                        "name" not in jval[0].lower() for jval in vals[
                                            start:end]]:
                                        val = ",".join(
                                            [vals[j][1] for j in range(start, end)])
                                        i += (end - start)
                                        comment = ""
                                    else:
                                        val = vals[i][1]
                                        comment = vals[i][0]
                                        i += 1

                                    sep = ','
                                    if i >= cval:
                                        sep = ';'
                                    blanks = ' ' * \
                                        max(30 - 4 - len(val) - 2, 2)

                                    f.write(
                                        "    {val}{sep}{blanks}!- {comment}\n".format(
                                            val=val,
                                            sep=sep,
                                            blanks=blanks,
                                            comment=comment))

                            else:
                                f.write(
                                    "\n  {},\n".format(
                                        dobj.schema['name']))
                                vals = dobj.export()
                                cval = len(vals)
                                for i, val in enumerate(vals):

                                    sep = ','
                                    if i == (cval - 1):
                                        sep = ';'
                                    blanks = ' ' * \
                                        max(30 - 4 - len(val[1]) - 2, 2)
                                    comment = val[0]

                                    f.write(
                                        "    {val}{sep}{blanks}!- {comment}\n".format(
                                            val=val[1],
                                            sep=sep,
                                            blanks=blanks,
                                            comment=comment))

    def read(self, path):
        """Read IDF data from path.

        Args:
            path (str): path to read data from

        """
        with open(path, "r") as f:
            current_object = None
            current_vals = []

            # First lines are header comments
            header = True

            for line in f:

                line = line.strip()
                if re.search(r"^\s*!", line) is not None:
                    if header:
                        self.comment_headers.append(line)
                    continue
                if len(line) == 0:
                    continue

                header = False

                line_comments = line.split("!")
                line_match = re.search(r"\s*([\S ]*[,;])\s*", line_comments[0])
                if line_match is None:
                    logger.warn("Not matched: {}".format(line))
                    continue
                else:
                    line = line_match.group(1)

                splits = line.split(";")

                for i, split in enumerate(splits):

                    split = split.strip()
                    if len(split) > 0 and split[-1] == ',':
                        split = split[:-1]

                    splitvals = split.split(",")

                    if i > 1 and len(split) == 0:
                        continue

                    for j, val in enumerate(splitvals):

                        val = val.strip()

                        if j == len(splitvals) and len(val) == 0:
                            continue

                        if val == '' and current_object is None:
                            continue

                        if current_object is None:
                            current_object = val.lower()
                        else:
                            current_vals.append(val)

                    if len(splits) > 1 and current_object is not None:

                        data_object = self._create_datadict(current_object)
                        data_object.read(current_vals)
                        self.add(data_object)

                        current_object = None
                        current_vals = []

    @property
    def lead_inputs(self):
        """Get list of all `LeadInput` objects.

        Raises:
            ValueError: if no objects of type `LeadInput` are present

        """
        return self._data["energyplus"]["lead input"]

    @property
    def simulation_datas(self):
        """Get list of all `SimulationData` objects.

        Raises:
            ValueError: if no objects of type `SimulationData` are present

        """
        return self._data["energyplus"]["simulation data"]

    @property
    def versions(self):
        """Get list of all `Version` objects.

        Raises:
            ValueError: if no objects of type `Version` are present

        """
        return self._data["Simulation Parameters"]["version"]

    @property
    def simulationcontrols(self):
        """Get list of all `SimulationControl` objects.

        Raises:
            ValueError: if no objects of type `SimulationControl` are present

        """
        return self._data["Simulation Parameters"]["simulationcontrol"]

    @property
    def buildings(self):
        """Get list of all `Building` objects.

        Raises:
            ValueError: if no objects of type `Building` are present

        """
        return self._data["Simulation Parameters"]["building"]

    @property
    def shadowcalculations(self):
        """Get list of all `ShadowCalculation` objects.

        Raises:
            ValueError: if no objects of type `ShadowCalculation` are present

        """
        return self._data["Simulation Parameters"]["shadowcalculation"]

    @property
    def surfaceconvectionalgorithminsides(self):
        """Get list of all `SurfaceConvectionAlgorithmInside` objects.

        Raises:
            ValueError: if no objects of type `SurfaceConvectionAlgorithmInside` are present

        """
        return self._data["Simulation Parameters"][
            "surfaceconvectionalgorithm:inside"]

    @property
    def surfaceconvectionalgorithmoutsides(self):
        """Get list of all `SurfaceConvectionAlgorithmOutside` objects.

        Raises:
            ValueError: if no objects of type `SurfaceConvectionAlgorithmOutside` are present

        """
        return self._data["Simulation Parameters"][
            "surfaceconvectionalgorithm:outside"]

    @property
    def heatbalancealgorithms(self):
        """Get list of all `HeatBalanceAlgorithm` objects.

        Raises:
            ValueError: if no objects of type `HeatBalanceAlgorithm` are present

        """
        return self._data["Simulation Parameters"]["heatbalancealgorithm"]

    @property
    def heatbalancesettingsconductionfinitedifferences(self):
        """Get list of all `HeatBalanceSettingsConductionFiniteDifference`
        objects.

        Raises:
            ValueError: if no objects of type `HeatBalanceSettingsConductionFiniteDifference` are present

        """
        return self._data["Simulation Parameters"][
            "heatbalancesettings:conductionfinitedifference"]

    @property
    def zoneairheatbalancealgorithms(self):
        """Get list of all `ZoneAirHeatBalanceAlgorithm` objects.

        Raises:
            ValueError: if no objects of type `ZoneAirHeatBalanceAlgorithm` are present

        """
        return self._data["Simulation Parameters"][
            "zoneairheatbalancealgorithm"]

    @property
    def zoneaircontaminantbalances(self):
        """Get list of all `ZoneAirContaminantBalance` objects.

        Raises:
            ValueError: if no objects of type `ZoneAirContaminantBalance` are present

        """
        return self._data["Simulation Parameters"]["zoneaircontaminantbalance"]

    @property
    def zoneairmassflowconservations(self):
        """Get list of all `ZoneAirMassFlowConservation` objects.

        Raises:
            ValueError: if no objects of type `ZoneAirMassFlowConservation` are present

        """
        return self._data["Simulation Parameters"][
            "zoneairmassflowconservation"]

    @property
    def zonecapacitancemultiplierresearchspecials(self):
        """Get list of all `ZoneCapacitanceMultiplierResearchSpecial` objects.

        Raises:
            ValueError: if no objects of type `ZoneCapacitanceMultiplierResearchSpecial` are present

        """
        return self._data["Simulation Parameters"][
            "zonecapacitancemultiplier:researchspecial"]

    @property
    def timesteps(self):
        """Get list of all `Timestep` objects.

        Raises:
            ValueError: if no objects of type `Timestep` are present

        """
        return self._data["Simulation Parameters"]["timestep"]

    @property
    def convergencelimitss(self):
        """Get list of all `ConvergenceLimits` objects.

        Raises:
            ValueError: if no objects of type `ConvergenceLimits` are present

        """
        return self._data["Simulation Parameters"]["convergencelimits"]

    @property
    def programcontrols(self):
        """Get list of all `ProgramControl` objects.

        Raises:
            ValueError: if no objects of type `ProgramControl` are present

        """
        return self._data["Simulation Parameters"]["programcontrol"]

    @property
    def compliancebuildings(self):
        """Get list of all `ComplianceBuilding` objects.

        Raises:
            ValueError: if no objects of type `ComplianceBuilding` are present

        """
        return self._data["Compliance Objects"]["compliance:building"]

    @property
    def sitelocations(self):
        """Get list of all `SiteLocation` objects.

        Raises:
            ValueError: if no objects of type `SiteLocation` are present

        """
        return self._data["Location and Climate"]["site:location"]

    @property
    def sizingperioddesigndays(self):
        """Get list of all `SizingPeriodDesignDay` objects.

        Raises:
            ValueError: if no objects of type `SizingPeriodDesignDay` are present

        """
        return self._data["Location and Climate"]["sizingperiod:designday"]

    @property
    def sizingperiodweatherfiledayss(self):
        """Get list of all `SizingPeriodWeatherFileDays` objects.

        Raises:
            ValueError: if no objects of type `SizingPeriodWeatherFileDays` are present

        """
        return self._data["Location and Climate"][
            "sizingperiod:weatherfiledays"]

    @property
    def sizingperiodweatherfileconditiontypes(self):
        """Get list of all `SizingPeriodWeatherFileConditionType` objects.

        Raises:
            ValueError: if no objects of type `SizingPeriodWeatherFileConditionType` are present

        """
        return self._data["Location and Climate"][
            "sizingperiod:weatherfileconditiontype"]

    @property
    def runperiods(self):
        """Get list of all `RunPeriod` objects.

        Raises:
            ValueError: if no objects of type `RunPeriod` are present

        """
        return self._data["Location and Climate"]["runperiod"]

    @property
    def runperiodcustomranges(self):
        """Get list of all `RunPeriodCustomRange` objects.

        Raises:
            ValueError: if no objects of type `RunPeriodCustomRange` are present

        """
        return self._data["Location and Climate"]["runperiod:customrange"]

    @property
    def runperiodcontrolspecialdayss(self):
        """Get list of all `RunPeriodControlSpecialDays` objects.

        Raises:
            ValueError: if no objects of type `RunPeriodControlSpecialDays` are present

        """
        return self._data["Location and Climate"][
            "runperiodcontrol:specialdays"]

    @property
    def runperiodcontroldaylightsavingtimes(self):
        """Get list of all `RunPeriodControlDaylightSavingTime` objects.

        Raises:
            ValueError: if no objects of type `RunPeriodControlDaylightSavingTime` are present

        """
        return self._data["Location and Climate"][
            "runperiodcontrol:daylightsavingtime"]

    @property
    def weatherpropertyskytemperatures(self):
        """Get list of all `WeatherPropertySkyTemperature` objects.

        Raises:
            ValueError: if no objects of type `WeatherPropertySkyTemperature` are present

        """
        return self._data["Location and Climate"][
            "weatherproperty:skytemperature"]

    @property
    def siteweatherstations(self):
        """Get list of all `SiteWeatherStation` objects.

        Raises:
            ValueError: if no objects of type `SiteWeatherStation` are present

        """
        return self._data["Location and Climate"]["site:weatherstation"]

    @property
    def siteheightvariations(self):
        """Get list of all `SiteHeightVariation` objects.

        Raises:
            ValueError: if no objects of type `SiteHeightVariation` are present

        """
        return self._data["Location and Climate"]["site:heightvariation"]

    @property
    def sitegroundtemperaturebuildingsurfaces(self):
        """Get list of all `SiteGroundTemperatureBuildingSurface` objects.

        Raises:
            ValueError: if no objects of type `SiteGroundTemperatureBuildingSurface` are present

        """
        return self._data["Location and Climate"][
            "site:groundtemperature:buildingsurface"]

    @property
    def sitegroundtemperaturefcfactormethods(self):
        """Get list of all `SiteGroundTemperatureFcfactorMethod` objects.

        Raises:
            ValueError: if no objects of type `SiteGroundTemperatureFcfactorMethod` are present

        """
        return self._data["Location and Climate"][
            "site:groundtemperature:fcfactormethod"]

    @property
    def sitegroundtemperatureshallows(self):
        """Get list of all `SiteGroundTemperatureShallow` objects.

        Raises:
            ValueError: if no objects of type `SiteGroundTemperatureShallow` are present

        """
        return self._data["Location and Climate"][
            "site:groundtemperature:shallow"]

    @property
    def sitegroundtemperaturedeeps(self):
        """Get list of all `SiteGroundTemperatureDeep` objects.

        Raises:
            ValueError: if no objects of type `SiteGroundTemperatureDeep` are present

        """
        return self._data["Location and Climate"][
            "site:groundtemperature:deep"]

    @property
    def sitegrounddomains(self):
        """Get list of all `SiteGroundDomain` objects.

        Raises:
            ValueError: if no objects of type `SiteGroundDomain` are present

        """
        return self._data["Location and Climate"]["site:grounddomain"]

    @property
    def sitegroundreflectances(self):
        """Get list of all `SiteGroundReflectance` objects.

        Raises:
            ValueError: if no objects of type `SiteGroundReflectance` are present

        """
        return self._data["Location and Climate"]["site:groundreflectance"]

    @property
    def sitegroundreflectancesnowmodifiers(self):
        """Get list of all `SiteGroundReflectanceSnowModifier` objects.

        Raises:
            ValueError: if no objects of type `SiteGroundReflectanceSnowModifier` are present

        """
        return self._data["Location and Climate"][
            "site:groundreflectance:snowmodifier"]

    @property
    def sitewatermainstemperatures(self):
        """Get list of all `SiteWaterMainsTemperature` objects.

        Raises:
            ValueError: if no objects of type `SiteWaterMainsTemperature` are present

        """
        return self._data["Location and Climate"]["site:watermainstemperature"]

    @property
    def siteprecipitations(self):
        """Get list of all `SitePrecipitation` objects.

        Raises:
            ValueError: if no objects of type `SitePrecipitation` are present

        """
        return self._data["Location and Climate"]["site:precipitation"]

    @property
    def roofirrigations(self):
        """Get list of all `RoofIrrigation` objects.

        Raises:
            ValueError: if no objects of type `RoofIrrigation` are present

        """
        return self._data["Location and Climate"]["roofirrigation"]

    @property
    def sitesolarandvisiblespectrums(self):
        """Get list of all `SiteSolarAndVisibleSpectrum` objects.

        Raises:
            ValueError: if no objects of type `SiteSolarAndVisibleSpectrum` are present

        """
        return self._data["Location and Climate"][
            "site:solarandvisiblespectrum"]

    @property
    def sitespectrumdatas(self):
        """Get list of all `SiteSpectrumData` objects.

        Raises:
            ValueError: if no objects of type `SiteSpectrumData` are present

        """
        return self._data["Location and Climate"]["site:spectrumdata"]

    @property
    def scheduletypelimitss(self):
        """Get list of all `ScheduleTypeLimits` objects.

        Raises:
            ValueError: if no objects of type `ScheduleTypeLimits` are present

        """
        return self._data["Schedules"]["scheduletypelimits"]

    @property
    def scheduledayhourlys(self):
        """Get list of all `ScheduleDayHourly` objects.

        Raises:
            ValueError: if no objects of type `ScheduleDayHourly` are present

        """
        return self._data["Schedules"]["schedule:day:hourly"]

    @property
    def scheduledayintervals(self):
        """Get list of all `ScheduleDayInterval` objects.

        Raises:
            ValueError: if no objects of type `ScheduleDayInterval` are present

        """
        return self._data["Schedules"]["schedule:day:interval"]

    @property
    def scheduledaylists(self):
        """Get list of all `ScheduleDayList` objects.

        Raises:
            ValueError: if no objects of type `ScheduleDayList` are present

        """
        return self._data["Schedules"]["schedule:day:list"]

    @property
    def scheduleweekdailys(self):
        """Get list of all `ScheduleWeekDaily` objects.

        Raises:
            ValueError: if no objects of type `ScheduleWeekDaily` are present

        """
        return self._data["Schedules"]["schedule:week:daily"]

    @property
    def scheduleweekcompacts(self):
        """Get list of all `ScheduleWeekCompact` objects.

        Raises:
            ValueError: if no objects of type `ScheduleWeekCompact` are present

        """
        return self._data["Schedules"]["schedule:week:compact"]

    @property
    def scheduleyears(self):
        """Get list of all `ScheduleYear` objects.

        Raises:
            ValueError: if no objects of type `ScheduleYear` are present

        """
        return self._data["Schedules"]["schedule:year"]

    @property
    def schedulecompacts(self):
        """Get list of all `ScheduleCompact` objects.

        Raises:
            ValueError: if no objects of type `ScheduleCompact` are present

        """
        return self._data["Schedules"]["schedule:compact"]

    @property
    def scheduleconstants(self):
        """Get list of all `ScheduleConstant` objects.

        Raises:
            ValueError: if no objects of type `ScheduleConstant` are present

        """
        return self._data["Schedules"]["schedule:constant"]

    @property
    def schedulefiles(self):
        """Get list of all `ScheduleFile` objects.

        Raises:
            ValueError: if no objects of type `ScheduleFile` are present

        """
        return self._data["Schedules"]["schedule:file"]

    @property
    def materials(self):
        """Get list of all `Material` objects.

        Raises:
            ValueError: if no objects of type `Material` are present

        """
        return self._data["Surface Construction Elements"]["material"]

    @property
    def materialnomasss(self):
        """Get list of all `MaterialNoMass` objects.

        Raises:
            ValueError: if no objects of type `MaterialNoMass` are present

        """
        return self._data["Surface Construction Elements"]["material:nomass"]

    @property
    def materialinfraredtransparents(self):
        """Get list of all `MaterialInfraredTransparent` objects.

        Raises:
            ValueError: if no objects of type `MaterialInfraredTransparent` are present

        """
        return self._data["Surface Construction Elements"][
            "material:infraredtransparent"]

    @property
    def materialairgaps(self):
        """Get list of all `MaterialAirGap` objects.

        Raises:
            ValueError: if no objects of type `MaterialAirGap` are present

        """
        return self._data["Surface Construction Elements"]["material:airgap"]

    @property
    def materialroofvegetations(self):
        """Get list of all `MaterialRoofVegetation` objects.

        Raises:
            ValueError: if no objects of type `MaterialRoofVegetation` are present

        """
        return self._data["Surface Construction Elements"][
            "material:roofvegetation"]

    @property
    def windowmaterialsimpleglazingsystems(self):
        """Get list of all `WindowMaterialSimpleGlazingSystem` objects.

        Raises:
            ValueError: if no objects of type `WindowMaterialSimpleGlazingSystem` are present

        """
        return self._data["Surface Construction Elements"][
            "windowmaterial:simpleglazingsystem"]

    @property
    def windowmaterialglazings(self):
        """Get list of all `WindowMaterialGlazing` objects.

        Raises:
            ValueError: if no objects of type `WindowMaterialGlazing` are present

        """
        return self._data["Surface Construction Elements"][
            "windowmaterial:glazing"]

    @property
    def windowmaterialglazinggroupthermochromics(self):
        """Get list of all `WindowMaterialGlazingGroupThermochromic` objects.

        Raises:
            ValueError: if no objects of type `WindowMaterialGlazingGroupThermochromic` are present

        """
        return self._data["Surface Construction Elements"][
            "windowmaterial:glazinggroup:thermochromic"]

    @property
    def windowmaterialglazingrefractionextinctionmethods(self):
        """Get list of all `WindowMaterialGlazingRefractionExtinctionMethod`
        objects.

        Raises:
            ValueError: if no objects of type `WindowMaterialGlazingRefractionExtinctionMethod` are present

        """
        return self._data["Surface Construction Elements"][
            "windowmaterial:glazing:refractionextinctionmethod"]

    @property
    def windowmaterialgass(self):
        """Get list of all `WindowMaterialGas` objects.

        Raises:
            ValueError: if no objects of type `WindowMaterialGas` are present

        """
        return self._data["Surface Construction Elements"][
            "windowmaterial:gas"]

    @property
    def windowgapsupportpillars(self):
        """Get list of all `WindowGapSupportPillar` objects.

        Raises:
            ValueError: if no objects of type `WindowGapSupportPillar` are present

        """
        return self._data["Surface Construction Elements"][
            "windowgap:supportpillar"]

    @property
    def windowgapdeflectionstates(self):
        """Get list of all `WindowGapDeflectionState` objects.

        Raises:
            ValueError: if no objects of type `WindowGapDeflectionState` are present

        """
        return self._data["Surface Construction Elements"][
            "windowgap:deflectionstate"]

    @property
    def windowmaterialgasmixtures(self):
        """Get list of all `WindowMaterialGasMixture` objects.

        Raises:
            ValueError: if no objects of type `WindowMaterialGasMixture` are present

        """
        return self._data["Surface Construction Elements"][
            "windowmaterial:gasmixture"]

    @property
    def windowmaterialgaps(self):
        """Get list of all `WindowMaterialGap` objects.

        Raises:
            ValueError: if no objects of type `WindowMaterialGap` are present

        """
        return self._data["Surface Construction Elements"][
            "windowmaterial:gap"]

    @property
    def windowmaterialshades(self):
        """Get list of all `WindowMaterialShade` objects.

        Raises:
            ValueError: if no objects of type `WindowMaterialShade` are present

        """
        return self._data["Surface Construction Elements"][
            "windowmaterial:shade"]

    @property
    def windowmaterialcomplexshades(self):
        """Get list of all `WindowMaterialComplexShade` objects.

        Raises:
            ValueError: if no objects of type `WindowMaterialComplexShade` are present

        """
        return self._data["Surface Construction Elements"][
            "windowmaterial:complexshade"]

    @property
    def windowmaterialblinds(self):
        """Get list of all `WindowMaterialBlind` objects.

        Raises:
            ValueError: if no objects of type `WindowMaterialBlind` are present

        """
        return self._data["Surface Construction Elements"][
            "windowmaterial:blind"]

    @property
    def windowmaterialscreens(self):
        """Get list of all `WindowMaterialScreen` objects.

        Raises:
            ValueError: if no objects of type `WindowMaterialScreen` are present

        """
        return self._data["Surface Construction Elements"][
            "windowmaterial:screen"]

    @property
    def windowmaterialshadeequivalentlayers(self):
        """Get list of all `WindowMaterialShadeEquivalentLayer` objects.

        Raises:
            ValueError: if no objects of type `WindowMaterialShadeEquivalentLayer` are present

        """
        return self._data["Surface Construction Elements"][
            "windowmaterial:shade:equivalentlayer"]

    @property
    def windowmaterialdrapeequivalentlayers(self):
        """Get list of all `WindowMaterialDrapeEquivalentLayer` objects.

        Raises:
            ValueError: if no objects of type `WindowMaterialDrapeEquivalentLayer` are present

        """
        return self._data["Surface Construction Elements"][
            "windowmaterial:drape:equivalentlayer"]

    @property
    def windowmaterialblindequivalentlayers(self):
        """Get list of all `WindowMaterialBlindEquivalentLayer` objects.

        Raises:
            ValueError: if no objects of type `WindowMaterialBlindEquivalentLayer` are present

        """
        return self._data["Surface Construction Elements"][
            "windowmaterial:blind:equivalentlayer"]

    @property
    def windowmaterialscreenequivalentlayers(self):
        """Get list of all `WindowMaterialScreenEquivalentLayer` objects.

        Raises:
            ValueError: if no objects of type `WindowMaterialScreenEquivalentLayer` are present

        """
        return self._data["Surface Construction Elements"][
            "windowmaterial:screen:equivalentlayer"]

    @property
    def windowmaterialglazingequivalentlayers(self):
        """Get list of all `WindowMaterialGlazingEquivalentLayer` objects.

        Raises:
            ValueError: if no objects of type `WindowMaterialGlazingEquivalentLayer` are present

        """
        return self._data["Surface Construction Elements"][
            "windowmaterial:glazing:equivalentlayer"]

    @property
    def constructionwindowequivalentlayers(self):
        """Get list of all `ConstructionWindowEquivalentLayer` objects.

        Raises:
            ValueError: if no objects of type `ConstructionWindowEquivalentLayer` are present

        """
        return self._data["Surface Construction Elements"][
            "construction:windowequivalentlayer"]

    @property
    def windowmaterialgapequivalentlayers(self):
        """Get list of all `WindowMaterialGapEquivalentLayer` objects.

        Raises:
            ValueError: if no objects of type `WindowMaterialGapEquivalentLayer` are present

        """
        return self._data["Surface Construction Elements"][
            "windowmaterial:gap:equivalentlayer"]

    @property
    def materialpropertymoisturepenetrationdepthsettingss(self):
        """Get list of all `MaterialPropertyMoisturePenetrationDepthSettings`
        objects.

        Raises:
            ValueError: if no objects of type `MaterialPropertyMoisturePenetrationDepthSettings` are present

        """
        return self._data["Surface Construction Elements"][
            "materialproperty:moisturepenetrationdepth:settings"]

    @property
    def materialpropertyphasechanges(self):
        """Get list of all `MaterialPropertyPhaseChange` objects.

        Raises:
            ValueError: if no objects of type `MaterialPropertyPhaseChange` are present

        """
        return self._data["Surface Construction Elements"][
            "materialproperty:phasechange"]

    @property
    def materialpropertyvariablethermalconductivitys(self):
        """Get list of all `MaterialPropertyVariableThermalConductivity`
        objects.

        Raises:
            ValueError: if no objects of type `MaterialPropertyVariableThermalConductivity` are present

        """
        return self._data["Surface Construction Elements"][
            "materialproperty:variablethermalconductivity"]

    @property
    def materialpropertyheatandmoisturetransfersettingss(self):
        """Get list of all `MaterialPropertyHeatAndMoistureTransferSettings`
        objects.

        Raises:
            ValueError: if no objects of type `MaterialPropertyHeatAndMoistureTransferSettings` are present

        """
        return self._data["Surface Construction Elements"][
            "materialproperty:heatandmoisturetransfer:settings"]

    @property
    def materialpropertyheatandmoisturetransfersorptionisotherms(self):
        """Get list of all
        `MaterialPropertyHeatAndMoistureTransferSorptionIsotherm` objects.

        Raises:
            ValueError: if no objects of type `MaterialPropertyHeatAndMoistureTransferSorptionIsotherm` are present

        """
        return self._data["Surface Construction Elements"][
            "materialproperty:heatandmoisturetransfer:sorptionisotherm"]

    @property
    def materialpropertyheatandmoisturetransfersuctions(self):
        """Get list of all `MaterialPropertyHeatAndMoistureTransferSuction`
        objects.

        Raises:
            ValueError: if no objects of type `MaterialPropertyHeatAndMoistureTransferSuction` are present

        """
        return self._data["Surface Construction Elements"][
            "materialproperty:heatandmoisturetransfer:suction"]

    @property
    def materialpropertyheatandmoisturetransferredistributions(self):
        """Get list of all
        `MaterialPropertyHeatAndMoistureTransferRedistribution` objects.

        Raises:
            ValueError: if no objects of type `MaterialPropertyHeatAndMoistureTransferRedistribution` are present

        """
        return self._data["Surface Construction Elements"][
            "materialproperty:heatandmoisturetransfer:redistribution"]

    @property
    def materialpropertyheatandmoisturetransferdiffusions(self):
        """Get list of all `MaterialPropertyHeatAndMoistureTransferDiffusion`
        objects.

        Raises:
            ValueError: if no objects of type `MaterialPropertyHeatAndMoistureTransferDiffusion` are present

        """
        return self._data["Surface Construction Elements"][
            "materialproperty:heatandmoisturetransfer:diffusion"]

    @property
    def materialpropertyheatandmoisturetransferthermalconductivitys(self):
        """Get list of all
        `MaterialPropertyHeatAndMoistureTransferThermalConductivity` objects.

        Raises:
            ValueError: if no objects of type `MaterialPropertyHeatAndMoistureTransferThermalConductivity` are present

        """
        return self._data["Surface Construction Elements"][
            "materialproperty:heatandmoisturetransfer:thermalconductivity"]

    @property
    def materialpropertyglazingspectraldatas(self):
        """Get list of all `MaterialPropertyGlazingSpectralData` objects.

        Raises:
            ValueError: if no objects of type `MaterialPropertyGlazingSpectralData` are present

        """
        return self._data["Surface Construction Elements"][
            "materialproperty:glazingspectraldata"]

    @property
    def constructions(self):
        """Get list of all `Construction` objects.

        Raises:
            ValueError: if no objects of type `Construction` are present

        """
        return self._data["Surface Construction Elements"]["construction"]

    @property
    def constructioncfactorundergroundwalls(self):
        """Get list of all `ConstructionCfactorUndergroundWall` objects.

        Raises:
            ValueError: if no objects of type `ConstructionCfactorUndergroundWall` are present

        """
        return self._data["Surface Construction Elements"][
            "construction:cfactorundergroundwall"]

    @property
    def constructionffactorgroundfloors(self):
        """Get list of all `ConstructionFfactorGroundFloor` objects.

        Raises:
            ValueError: if no objects of type `ConstructionFfactorGroundFloor` are present

        """
        return self._data["Surface Construction Elements"][
            "construction:ffactorgroundfloor"]

    @property
    def constructioninternalsources(self):
        """Get list of all `ConstructionInternalSource` objects.

        Raises:
            ValueError: if no objects of type `ConstructionInternalSource` are present

        """
        return self._data["Surface Construction Elements"][
            "construction:internalsource"]

    @property
    def windowthermalmodelparamss(self):
        """Get list of all `WindowThermalModelParams` objects.

        Raises:
            ValueError: if no objects of type `WindowThermalModelParams` are present

        """
        return self._data["Surface Construction Elements"][
            "windowthermalmodel:params"]

    @property
    def constructioncomplexfenestrationstates(self):
        """Get list of all `ConstructionComplexFenestrationState` objects.

        Raises:
            ValueError: if no objects of type `ConstructionComplexFenestrationState` are present

        """
        return self._data["Surface Construction Elements"][
            "construction:complexfenestrationstate"]

    @property
    def constructionwindowdatafiles(self):
        """Get list of all `ConstructionWindowDataFile` objects.

        Raises:
            ValueError: if no objects of type `ConstructionWindowDataFile` are present

        """
        return self._data["Surface Construction Elements"][
            "construction:windowdatafile"]

    @property
    def globalgeometryruless(self):
        """Get list of all `GlobalGeometryRules` objects.

        Raises:
            ValueError: if no objects of type `GlobalGeometryRules` are present

        """
        return self._data["Thermal Zones and Surfaces"]["globalgeometryrules"]

    @property
    def geometrytransforms(self):
        """Get list of all `GeometryTransform` objects.

        Raises:
            ValueError: if no objects of type `GeometryTransform` are present

        """
        return self._data["Thermal Zones and Surfaces"]["geometrytransform"]

    @property
    def zones(self):
        """Get list of all `Zone` objects.

        Raises:
            ValueError: if no objects of type `Zone` are present

        """
        return self._data["Thermal Zones and Surfaces"]["zone"]

    @property
    def zonelists(self):
        """Get list of all `ZoneList` objects.

        Raises:
            ValueError: if no objects of type `ZoneList` are present

        """
        return self._data["Thermal Zones and Surfaces"]["zonelist"]

    @property
    def zonegroups(self):
        """Get list of all `ZoneGroup` objects.

        Raises:
            ValueError: if no objects of type `ZoneGroup` are present

        """
        return self._data["Thermal Zones and Surfaces"]["zonegroup"]

    @property
    def buildingsurfacedetaileds(self):
        """Get list of all `BuildingSurfaceDetailed` objects.

        Raises:
            ValueError: if no objects of type `BuildingSurfaceDetailed` are present

        """
        return self._data["Thermal Zones and Surfaces"][
            "buildingsurface:detailed"]

    @property
    def walldetaileds(self):
        """Get list of all `WallDetailed` objects.

        Raises:
            ValueError: if no objects of type `WallDetailed` are present

        """
        return self._data["Thermal Zones and Surfaces"]["wall:detailed"]

    @property
    def roofceilingdetaileds(self):
        """Get list of all `RoofCeilingDetailed` objects.

        Raises:
            ValueError: if no objects of type `RoofCeilingDetailed` are present

        """
        return self._data["Thermal Zones and Surfaces"]["roofceiling:detailed"]

    @property
    def floordetaileds(self):
        """Get list of all `FloorDetailed` objects.

        Raises:
            ValueError: if no objects of type `FloorDetailed` are present

        """
        return self._data["Thermal Zones and Surfaces"]["floor:detailed"]

    @property
    def wallexteriors(self):
        """Get list of all `WallExterior` objects.

        Raises:
            ValueError: if no objects of type `WallExterior` are present

        """
        return self._data["Thermal Zones and Surfaces"]["wall:exterior"]

    @property
    def walladiabatics(self):
        """Get list of all `WallAdiabatic` objects.

        Raises:
            ValueError: if no objects of type `WallAdiabatic` are present

        """
        return self._data["Thermal Zones and Surfaces"]["wall:adiabatic"]

    @property
    def wallundergrounds(self):
        """Get list of all `WallUnderground` objects.

        Raises:
            ValueError: if no objects of type `WallUnderground` are present

        """
        return self._data["Thermal Zones and Surfaces"]["wall:underground"]

    @property
    def wallinterzones(self):
        """Get list of all `WallInterzone` objects.

        Raises:
            ValueError: if no objects of type `WallInterzone` are present

        """
        return self._data["Thermal Zones and Surfaces"]["wall:interzone"]

    @property
    def roofs(self):
        """Get list of all `Roof` objects.

        Raises:
            ValueError: if no objects of type `Roof` are present

        """
        return self._data["Thermal Zones and Surfaces"]["roof"]

    @property
    def ceilingadiabatics(self):
        """Get list of all `CeilingAdiabatic` objects.

        Raises:
            ValueError: if no objects of type `CeilingAdiabatic` are present

        """
        return self._data["Thermal Zones and Surfaces"]["ceiling:adiabatic"]

    @property
    def ceilinginterzones(self):
        """Get list of all `CeilingInterzone` objects.

        Raises:
            ValueError: if no objects of type `CeilingInterzone` are present

        """
        return self._data["Thermal Zones and Surfaces"]["ceiling:interzone"]

    @property
    def floorgroundcontacts(self):
        """Get list of all `FloorGroundContact` objects.

        Raises:
            ValueError: if no objects of type `FloorGroundContact` are present

        """
        return self._data["Thermal Zones and Surfaces"]["floor:groundcontact"]

    @property
    def flooradiabatics(self):
        """Get list of all `FloorAdiabatic` objects.

        Raises:
            ValueError: if no objects of type `FloorAdiabatic` are present

        """
        return self._data["Thermal Zones and Surfaces"]["floor:adiabatic"]

    @property
    def floorinterzones(self):
        """Get list of all `FloorInterzone` objects.

        Raises:
            ValueError: if no objects of type `FloorInterzone` are present

        """
        return self._data["Thermal Zones and Surfaces"]["floor:interzone"]

    @property
    def fenestrationsurfacedetaileds(self):
        """Get list of all `FenestrationSurfaceDetailed` objects.

        Raises:
            ValueError: if no objects of type `FenestrationSurfaceDetailed` are present

        """
        return self._data["Thermal Zones and Surfaces"][
            "fenestrationsurface:detailed"]

    @property
    def windows(self):
        """Get list of all `Window` objects.

        Raises:
            ValueError: if no objects of type `Window` are present

        """
        return self._data["Thermal Zones and Surfaces"]["window"]

    @property
    def doors(self):
        """Get list of all `Door` objects.

        Raises:
            ValueError: if no objects of type `Door` are present

        """
        return self._data["Thermal Zones and Surfaces"]["door"]

    @property
    def glazeddoors(self):
        """Get list of all `GlazedDoor` objects.

        Raises:
            ValueError: if no objects of type `GlazedDoor` are present

        """
        return self._data["Thermal Zones and Surfaces"]["glazeddoor"]

    @property
    def windowinterzones(self):
        """Get list of all `WindowInterzone` objects.

        Raises:
            ValueError: if no objects of type `WindowInterzone` are present

        """
        return self._data["Thermal Zones and Surfaces"]["window:interzone"]

    @property
    def doorinterzones(self):
        """Get list of all `DoorInterzone` objects.

        Raises:
            ValueError: if no objects of type `DoorInterzone` are present

        """
        return self._data["Thermal Zones and Surfaces"]["door:interzone"]

    @property
    def glazeddoorinterzones(self):
        """Get list of all `GlazedDoorInterzone` objects.

        Raises:
            ValueError: if no objects of type `GlazedDoorInterzone` are present

        """
        return self._data["Thermal Zones and Surfaces"]["glazeddoor:interzone"]

    @property
    def windowpropertyshadingcontrols(self):
        """Get list of all `WindowPropertyShadingControl` objects.

        Raises:
            ValueError: if no objects of type `WindowPropertyShadingControl` are present

        """
        return self._data["Thermal Zones and Surfaces"][
            "windowproperty:shadingcontrol"]

    @property
    def windowpropertyframeanddividers(self):
        """Get list of all `WindowPropertyFrameAndDivider` objects.

        Raises:
            ValueError: if no objects of type `WindowPropertyFrameAndDivider` are present

        """
        return self._data["Thermal Zones and Surfaces"][
            "windowproperty:frameanddivider"]

    @property
    def windowpropertyairflowcontrols(self):
        """Get list of all `WindowPropertyAirflowControl` objects.

        Raises:
            ValueError: if no objects of type `WindowPropertyAirflowControl` are present

        """
        return self._data["Thermal Zones and Surfaces"][
            "windowproperty:airflowcontrol"]

    @property
    def windowpropertystormwindows(self):
        """Get list of all `WindowPropertyStormWindow` objects.

        Raises:
            ValueError: if no objects of type `WindowPropertyStormWindow` are present

        """
        return self._data["Thermal Zones and Surfaces"][
            "windowproperty:stormwindow"]

    @property
    def internalmasss(self):
        """Get list of all `InternalMass` objects.

        Raises:
            ValueError: if no objects of type `InternalMass` are present

        """
        return self._data["Thermal Zones and Surfaces"]["internalmass"]

    @property
    def shadingsites(self):
        """Get list of all `ShadingSite` objects.

        Raises:
            ValueError: if no objects of type `ShadingSite` are present

        """
        return self._data["Thermal Zones and Surfaces"]["shading:site"]

    @property
    def shadingbuildings(self):
        """Get list of all `ShadingBuilding` objects.

        Raises:
            ValueError: if no objects of type `ShadingBuilding` are present

        """
        return self._data["Thermal Zones and Surfaces"]["shading:building"]

    @property
    def shadingsitedetaileds(self):
        """Get list of all `ShadingSiteDetailed` objects.

        Raises:
            ValueError: if no objects of type `ShadingSiteDetailed` are present

        """
        return self._data["Thermal Zones and Surfaces"][
            "shading:site:detailed"]

    @property
    def shadingbuildingdetaileds(self):
        """Get list of all `ShadingBuildingDetailed` objects.

        Raises:
            ValueError: if no objects of type `ShadingBuildingDetailed` are present

        """
        return self._data["Thermal Zones and Surfaces"][
            "shading:building:detailed"]

    @property
    def shadingoverhangs(self):
        """Get list of all `ShadingOverhang` objects.

        Raises:
            ValueError: if no objects of type `ShadingOverhang` are present

        """
        return self._data["Thermal Zones and Surfaces"]["shading:overhang"]

    @property
    def shadingoverhangprojections(self):
        """Get list of all `ShadingOverhangProjection` objects.

        Raises:
            ValueError: if no objects of type `ShadingOverhangProjection` are present

        """
        return self._data["Thermal Zones and Surfaces"][
            "shading:overhang:projection"]

    @property
    def shadingfins(self):
        """Get list of all `ShadingFin` objects.

        Raises:
            ValueError: if no objects of type `ShadingFin` are present

        """
        return self._data["Thermal Zones and Surfaces"]["shading:fin"]

    @property
    def shadingfinprojections(self):
        """Get list of all `ShadingFinProjection` objects.

        Raises:
            ValueError: if no objects of type `ShadingFinProjection` are present

        """
        return self._data["Thermal Zones and Surfaces"][
            "shading:fin:projection"]

    @property
    def shadingzonedetaileds(self):
        """Get list of all `ShadingZoneDetailed` objects.

        Raises:
            ValueError: if no objects of type `ShadingZoneDetailed` are present

        """
        return self._data["Thermal Zones and Surfaces"][
            "shading:zone:detailed"]

    @property
    def shadingpropertyreflectances(self):
        """Get list of all `ShadingPropertyReflectance` objects.

        Raises:
            ValueError: if no objects of type `ShadingPropertyReflectance` are present

        """
        return self._data["Thermal Zones and Surfaces"][
            "shadingproperty:reflectance"]

    @property
    def surfacepropertyheattransferalgorithms(self):
        """Get list of all `SurfacePropertyHeatTransferAlgorithm` objects.

        Raises:
            ValueError: if no objects of type `SurfacePropertyHeatTransferAlgorithm` are present

        """
        return self._data["Advanced Construction"][
            "surfaceproperty:heattransferalgorithm"]

    @property
    def surfacepropertyheattransferalgorithmmultiplesurfaces(self):
        """Get list of all
        `SurfacePropertyHeatTransferAlgorithmMultipleSurface` objects.

        Raises:
            ValueError: if no objects of type `SurfacePropertyHeatTransferAlgorithmMultipleSurface` are present

        """
        return self._data["Advanced Construction"][
            "surfaceproperty:heattransferalgorithm:multiplesurface"]

    @property
    def surfacepropertyheattransferalgorithmsurfacelists(self):
        """Get list of all `SurfacePropertyHeatTransferAlgorithmSurfaceList`
        objects.

        Raises:
            ValueError: if no objects of type `SurfacePropertyHeatTransferAlgorithmSurfaceList` are present

        """
        return self._data["Advanced Construction"][
            "surfaceproperty:heattransferalgorithm:surfacelist"]

    @property
    def surfacepropertyheattransferalgorithmconstructions(self):
        """Get list of all `SurfacePropertyHeatTransferAlgorithmConstruction`
        objects.

        Raises:
            ValueError: if no objects of type `SurfacePropertyHeatTransferAlgorithmConstruction` are present

        """
        return self._data["Advanced Construction"][
            "surfaceproperty:heattransferalgorithm:construction"]

    @property
    def surfacecontrolmovableinsulations(self):
        """Get list of all `SurfaceControlMovableInsulation` objects.

        Raises:
            ValueError: if no objects of type `SurfaceControlMovableInsulation` are present

        """
        return self._data["Advanced Construction"][
            "surfacecontrol:movableinsulation"]

    @property
    def surfacepropertyothersidecoefficientss(self):
        """Get list of all `SurfacePropertyOtherSideCoefficients` objects.

        Raises:
            ValueError: if no objects of type `SurfacePropertyOtherSideCoefficients` are present

        """
        return self._data["Advanced Construction"][
            "surfaceproperty:othersidecoefficients"]

    @property
    def surfacepropertyothersideconditionsmodels(self):
        """Get list of all `SurfacePropertyOtherSideConditionsModel` objects.

        Raises:
            ValueError: if no objects of type `SurfacePropertyOtherSideConditionsModel` are present

        """
        return self._data["Advanced Construction"][
            "surfaceproperty:othersideconditionsmodel"]

    @property
    def surfaceconvectionalgorithminsideadaptivemodelselectionss(self):
        """Get list of all
        `SurfaceConvectionAlgorithmInsideAdaptiveModelSelections` objects.

        Raises:
            ValueError: if no objects of type `SurfaceConvectionAlgorithmInsideAdaptiveModelSelections` are present

        """
        return self._data["Advanced Construction"][
            "surfaceconvectionalgorithm:inside:adaptivemodelselections"]

    @property
    def surfaceconvectionalgorithmoutsideadaptivemodelselectionss(self):
        """Get list of all
        `SurfaceConvectionAlgorithmOutsideAdaptiveModelSelections` objects.

        Raises:
            ValueError: if no objects of type `SurfaceConvectionAlgorithmOutsideAdaptiveModelSelections` are present

        """
        return self._data["Advanced Construction"][
            "surfaceconvectionalgorithm:outside:adaptivemodelselections"]

    @property
    def surfaceconvectionalgorithminsideusercurves(self):
        """Get list of all `SurfaceConvectionAlgorithmInsideUserCurve` objects.

        Raises:
            ValueError: if no objects of type `SurfaceConvectionAlgorithmInsideUserCurve` are present

        """
        return self._data["Advanced Construction"][
            "surfaceconvectionalgorithm:inside:usercurve"]

    @property
    def surfaceconvectionalgorithmoutsideusercurves(self):
        """Get list of all `SurfaceConvectionAlgorithmOutsideUserCurve`
        objects.

        Raises:
            ValueError: if no objects of type `SurfaceConvectionAlgorithmOutsideUserCurve` are present

        """
        return self._data["Advanced Construction"][
            "surfaceconvectionalgorithm:outside:usercurve"]

    @property
    def surfacepropertyconvectioncoefficientss(self):
        """Get list of all `SurfacePropertyConvectionCoefficients` objects.

        Raises:
            ValueError: if no objects of type `SurfacePropertyConvectionCoefficients` are present

        """
        return self._data["Advanced Construction"][
            "surfaceproperty:convectioncoefficients"]

    @property
    def surfacepropertyconvectioncoefficientsmultiplesurfaces(self):
        """Get list of all
        `SurfacePropertyConvectionCoefficientsMultipleSurface` objects.

        Raises:
            ValueError: if no objects of type `SurfacePropertyConvectionCoefficientsMultipleSurface` are present

        """
        return self._data["Advanced Construction"][
            "surfaceproperty:convectioncoefficients:multiplesurface"]

    @property
    def surfacepropertiesvaporcoefficientss(self):
        """Get list of all `SurfacePropertiesVaporCoefficients` objects.

        Raises:
            ValueError: if no objects of type `SurfacePropertiesVaporCoefficients` are present

        """
        return self._data["Advanced Construction"][
            "surfaceproperties:vaporcoefficients"]

    @property
    def surfacepropertyexteriornaturalventedcavitys(self):
        """Get list of all `SurfacePropertyExteriorNaturalVentedCavity`
        objects.

        Raises:
            ValueError: if no objects of type `SurfacePropertyExteriorNaturalVentedCavity` are present

        """
        return self._data["Advanced Construction"][
            "surfaceproperty:exteriornaturalventedcavity"]

    @property
    def surfacepropertysolarincidentinsides(self):
        """Get list of all `SurfacePropertySolarIncidentInside` objects.

        Raises:
            ValueError: if no objects of type `SurfacePropertySolarIncidentInside` are present

        """
        return self._data["Advanced Construction"][
            "surfaceproperty:solarincidentinside"]

    @property
    def complexfenestrationpropertysolarabsorbedlayerss(self):
        """Get list of all `ComplexFenestrationPropertySolarAbsorbedLayers`
        objects.

        Raises:
            ValueError: if no objects of type `ComplexFenestrationPropertySolarAbsorbedLayers` are present

        """
        return self._data["Advanced Construction"][
            "complexfenestrationproperty:solarabsorbedlayers"]

    @property
    def zonepropertyuserviewfactorsbysurfacenames(self):
        """Get list of all `ZonePropertyUserViewFactorsBySurfaceName` objects.

        Raises:
            ValueError: if no objects of type `ZonePropertyUserViewFactorsBySurfaceName` are present

        """
        return self._data["Advanced Construction"][
            "zoneproperty:userviewfactors:bysurfacename"]

    @property
    def groundheattransfercontrols(self):
        """Get list of all `GroundHeatTransferControl` objects.

        Raises:
            ValueError: if no objects of type `GroundHeatTransferControl` are present

        """
        return self._data["Detailed Ground Heat Transfer"][
            "groundheattransfer:control"]

    @property
    def groundheattransferslabmaterialss(self):
        """Get list of all `GroundHeatTransferSlabMaterials` objects.

        Raises:
            ValueError: if no objects of type `GroundHeatTransferSlabMaterials` are present

        """
        return self._data["Detailed Ground Heat Transfer"][
            "groundheattransfer:slab:materials"]

    @property
    def groundheattransferslabmatlpropss(self):
        """Get list of all `GroundHeatTransferSlabMatlProps` objects.

        Raises:
            ValueError: if no objects of type `GroundHeatTransferSlabMatlProps` are present

        """
        return self._data["Detailed Ground Heat Transfer"][
            "groundheattransfer:slab:matlprops"]

    @property
    def groundheattransferslabboundcondss(self):
        """Get list of all `GroundHeatTransferSlabBoundConds` objects.

        Raises:
            ValueError: if no objects of type `GroundHeatTransferSlabBoundConds` are present

        """
        return self._data["Detailed Ground Heat Transfer"][
            "groundheattransfer:slab:boundconds"]

    @property
    def groundheattransferslabbldgpropss(self):
        """Get list of all `GroundHeatTransferSlabBldgProps` objects.

        Raises:
            ValueError: if no objects of type `GroundHeatTransferSlabBldgProps` are present

        """
        return self._data["Detailed Ground Heat Transfer"][
            "groundheattransfer:slab:bldgprops"]

    @property
    def groundheattransferslabinsulations(self):
        """Get list of all `GroundHeatTransferSlabInsulation` objects.

        Raises:
            ValueError: if no objects of type `GroundHeatTransferSlabInsulation` are present

        """
        return self._data["Detailed Ground Heat Transfer"][
            "groundheattransfer:slab:insulation"]

    @property
    def groundheattransferslabequivalentslabs(self):
        """Get list of all `GroundHeatTransferSlabEquivalentSlab` objects.

        Raises:
            ValueError: if no objects of type `GroundHeatTransferSlabEquivalentSlab` are present

        """
        return self._data["Detailed Ground Heat Transfer"][
            "groundheattransfer:slab:equivalentslab"]

    @property
    def groundheattransferslabautogrids(self):
        """Get list of all `GroundHeatTransferSlabAutoGrid` objects.

        Raises:
            ValueError: if no objects of type `GroundHeatTransferSlabAutoGrid` are present

        """
        return self._data["Detailed Ground Heat Transfer"][
            "groundheattransfer:slab:autogrid"]

    @property
    def groundheattransferslabmanualgrids(self):
        """Get list of all `GroundHeatTransferSlabManualGrid` objects.

        Raises:
            ValueError: if no objects of type `GroundHeatTransferSlabManualGrid` are present

        """
        return self._data["Detailed Ground Heat Transfer"][
            "groundheattransfer:slab:manualgrid"]

    @property
    def groundheattransferslabxfaces(self):
        """Get list of all `GroundHeatTransferSlabXface` objects.

        Raises:
            ValueError: if no objects of type `GroundHeatTransferSlabXface` are present

        """
        return self._data["Room Air Models"]["groundheattransfer:slab:xface"]

    @property
    def groundheattransferslabyfaces(self):
        """Get list of all `GroundHeatTransferSlabYface` objects.

        Raises:
            ValueError: if no objects of type `GroundHeatTransferSlabYface` are present

        """
        return self._data["Room Air Models"]["groundheattransfer:slab:yface"]

    @property
    def groundheattransferslabzfaces(self):
        """Get list of all `GroundHeatTransferSlabZface` objects.

        Raises:
            ValueError: if no objects of type `GroundHeatTransferSlabZface` are present

        """
        return self._data["Room Air Models"]["groundheattransfer:slab:zface"]

    @property
    def groundheattransferbasementsimparameterss(self):
        """Get list of all `GroundHeatTransferBasementSimParameters` objects.

        Raises:
            ValueError: if no objects of type `GroundHeatTransferBasementSimParameters` are present

        """
        return self._data["Detailed Ground Heat Transfer"][
            "groundheattransfer:basement:simparameters"]

    @property
    def groundheattransferbasementmatlpropss(self):
        """Get list of all `GroundHeatTransferBasementMatlProps` objects.

        Raises:
            ValueError: if no objects of type `GroundHeatTransferBasementMatlProps` are present

        """
        return self._data["Detailed Ground Heat Transfer"][
            "groundheattransfer:basement:matlprops"]

    @property
    def groundheattransferbasementinsulations(self):
        """Get list of all `GroundHeatTransferBasementInsulation` objects.

        Raises:
            ValueError: if no objects of type `GroundHeatTransferBasementInsulation` are present

        """
        return self._data["Detailed Ground Heat Transfer"][
            "groundheattransfer:basement:insulation"]

    @property
    def groundheattransferbasementsurfacepropss(self):
        """Get list of all `GroundHeatTransferBasementSurfaceProps` objects.

        Raises:
            ValueError: if no objects of type `GroundHeatTransferBasementSurfaceProps` are present

        """
        return self._data["Detailed Ground Heat Transfer"][
            "groundheattransfer:basement:surfaceprops"]

    @property
    def groundheattransferbasementbldgdatas(self):
        """Get list of all `GroundHeatTransferBasementBldgData` objects.

        Raises:
            ValueError: if no objects of type `GroundHeatTransferBasementBldgData` are present

        """
        return self._data["Detailed Ground Heat Transfer"][
            "groundheattransfer:basement:bldgdata"]

    @property
    def groundheattransferbasementinteriors(self):
        """Get list of all `GroundHeatTransferBasementInterior` objects.

        Raises:
            ValueError: if no objects of type `GroundHeatTransferBasementInterior` are present

        """
        return self._data["Detailed Ground Heat Transfer"][
            "groundheattransfer:basement:interior"]

    @property
    def groundheattransferbasementcombldgs(self):
        """Get list of all `GroundHeatTransferBasementComBldg` objects.

        Raises:
            ValueError: if no objects of type `GroundHeatTransferBasementComBldg` are present

        """
        return self._data["Detailed Ground Heat Transfer"][
            "groundheattransfer:basement:combldg"]

    @property
    def groundheattransferbasementequivslabs(self):
        """Get list of all `GroundHeatTransferBasementEquivSlab` objects.

        Raises:
            ValueError: if no objects of type `GroundHeatTransferBasementEquivSlab` are present

        """
        return self._data["Detailed Ground Heat Transfer"][
            "groundheattransfer:basement:equivslab"]

    @property
    def groundheattransferbasementequivautogrids(self):
        """Get list of all `GroundHeatTransferBasementEquivAutoGrid` objects.

        Raises:
            ValueError: if no objects of type `GroundHeatTransferBasementEquivAutoGrid` are present

        """
        return self._data["Detailed Ground Heat Transfer"][
            "groundheattransfer:basement:equivautogrid"]

    @property
    def groundheattransferbasementautogrids(self):
        """Get list of all `GroundHeatTransferBasementAutoGrid` objects.

        Raises:
            ValueError: if no objects of type `GroundHeatTransferBasementAutoGrid` are present

        """
        return self._data["Detailed Ground Heat Transfer"][
            "groundheattransfer:basement:autogrid"]

    @property
    def groundheattransferbasementmanualgrids(self):
        """Get list of all `GroundHeatTransferBasementManualGrid` objects.

        Raises:
            ValueError: if no objects of type `GroundHeatTransferBasementManualGrid` are present

        """
        return self._data["Detailed Ground Heat Transfer"][
            "groundheattransfer:basement:manualgrid"]

    @property
    def groundheattransferbasementxfaces(self):
        """Get list of all `GroundHeatTransferBasementXface` objects.

        Raises:
            ValueError: if no objects of type `GroundHeatTransferBasementXface` are present

        """
        return self._data["Room Air Models"][
            "groundheattransfer:basement:xface"]

    @property
    def groundheattransferbasementyfaces(self):
        """Get list of all `GroundHeatTransferBasementYface` objects.

        Raises:
            ValueError: if no objects of type `GroundHeatTransferBasementYface` are present

        """
        return self._data["Room Air Models"][
            "groundheattransfer:basement:yface"]

    @property
    def groundheattransferbasementzfaces(self):
        """Get list of all `GroundHeatTransferBasementZface` objects.

        Raises:
            ValueError: if no objects of type `GroundHeatTransferBasementZface` are present

        """
        return self._data["Room Air Models"][
            "groundheattransfer:basement:zface"]

    @property
    def roomairmodeltypes(self):
        """Get list of all `RoomAirModelType` objects.

        Raises:
            ValueError: if no objects of type `RoomAirModelType` are present

        """
        return self._data["Room Air Models"]["roomairmodeltype"]

    @property
    def roomairtemperaturepatternuserdefineds(self):
        """Get list of all `RoomAirTemperaturePatternUserDefined` objects.

        Raises:
            ValueError: if no objects of type `RoomAirTemperaturePatternUserDefined` are present

        """
        return self._data["Room Air Models"][
            "roomair:temperaturepattern:userdefined"]

    @property
    def roomairtemperaturepatternconstantgradients(self):
        """Get list of all `RoomAirTemperaturePatternConstantGradient` objects.

        Raises:
            ValueError: if no objects of type `RoomAirTemperaturePatternConstantGradient` are present

        """
        return self._data["Room Air Models"][
            "roomair:temperaturepattern:constantgradient"]

    @property
    def roomairtemperaturepatterntwogradients(self):
        """Get list of all `RoomAirTemperaturePatternTwoGradient` objects.

        Raises:
            ValueError: if no objects of type `RoomAirTemperaturePatternTwoGradient` are present

        """
        return self._data["Room Air Models"][
            "roomair:temperaturepattern:twogradient"]

    @property
    def roomairtemperaturepatternnondimensionalheights(self):
        """Get list of all `RoomAirTemperaturePatternNondimensionalHeight`
        objects.

        Raises:
            ValueError: if no objects of type `RoomAirTemperaturePatternNondimensionalHeight` are present

        """
        return self._data["Room Air Models"][
            "roomair:temperaturepattern:nondimensionalheight"]

    @property
    def roomairtemperaturepatternsurfacemappings(self):
        """Get list of all `RoomAirTemperaturePatternSurfaceMapping` objects.

        Raises:
            ValueError: if no objects of type `RoomAirTemperaturePatternSurfaceMapping` are present

        """
        return self._data["Room Air Models"][
            "roomair:temperaturepattern:surfacemapping"]

    @property
    def roomairnodes(self):
        """Get list of all `RoomAirNode` objects.

        Raises:
            ValueError: if no objects of type `RoomAirNode` are present

        """
        return self._data["Room Air Models"]["roomair:node"]

    @property
    def roomairsettingsonenodedisplacementventilations(self):
        """Get list of all `RoomAirSettingsOneNodeDisplacementVentilation`
        objects.

        Raises:
            ValueError: if no objects of type `RoomAirSettingsOneNodeDisplacementVentilation` are present

        """
        return self._data["Room Air Models"][
            "roomairsettings:onenodedisplacementventilation"]

    @property
    def roomairsettingsthreenodedisplacementventilations(self):
        """Get list of all `RoomAirSettingsThreeNodeDisplacementVentilation`
        objects.

        Raises:
            ValueError: if no objects of type `RoomAirSettingsThreeNodeDisplacementVentilation` are present

        """
        return self._data["Room Air Models"][
            "roomairsettings:threenodedisplacementventilation"]

    @property
    def roomairsettingscrossventilations(self):
        """Get list of all `RoomAirSettingsCrossVentilation` objects.

        Raises:
            ValueError: if no objects of type `RoomAirSettingsCrossVentilation` are present

        """
        return self._data["Room Air Models"][
            "roomairsettings:crossventilation"]

    @property
    def roomairsettingsunderfloorairdistributioninteriors(self):
        """Get list of all `RoomAirSettingsUnderFloorAirDistributionInterior`
        objects.

        Raises:
            ValueError: if no objects of type `RoomAirSettingsUnderFloorAirDistributionInterior` are present

        """
        return self._data["Room Air Models"][
            "roomairsettings:underfloorairdistributioninterior"]

    @property
    def roomairsettingsunderfloorairdistributionexteriors(self):
        """Get list of all `RoomAirSettingsUnderFloorAirDistributionExterior`
        objects.

        Raises:
            ValueError: if no objects of type `RoomAirSettingsUnderFloorAirDistributionExterior` are present

        """
        return self._data["Room Air Models"][
            "roomairsettings:underfloorairdistributionexterior"]

    @property
    def peoples(self):
        """Get list of all `People` objects.

        Raises:
            ValueError: if no objects of type `People` are present

        """
        return self._data["Internal Gains"]["people"]

    @property
    def comfortviewfactorangless(self):
        """Get list of all `ComfortViewFactorAngles` objects.

        Raises:
            ValueError: if no objects of type `ComfortViewFactorAngles` are present

        """
        return self._data["Internal Gains"]["comfortviewfactorangles"]

    @property
    def lightss(self):
        """Get list of all `Lights` objects.

        Raises:
            ValueError: if no objects of type `Lights` are present

        """
        return self._data["Internal Gains"]["lights"]

    @property
    def electricequipments(self):
        """Get list of all `ElectricEquipment` objects.

        Raises:
            ValueError: if no objects of type `ElectricEquipment` are present

        """
        return self._data["Internal Gains"]["electricequipment"]

    @property
    def gasequipments(self):
        """Get list of all `GasEquipment` objects.

        Raises:
            ValueError: if no objects of type `GasEquipment` are present

        """
        return self._data["Internal Gains"]["gasequipment"]

    @property
    def hotwaterequipments(self):
        """Get list of all `HotWaterEquipment` objects.

        Raises:
            ValueError: if no objects of type `HotWaterEquipment` are present

        """
        return self._data["Internal Gains"]["hotwaterequipment"]

    @property
    def steamequipments(self):
        """Get list of all `SteamEquipment` objects.

        Raises:
            ValueError: if no objects of type `SteamEquipment` are present

        """
        return self._data["Internal Gains"]["steamequipment"]

    @property
    def otherequipments(self):
        """Get list of all `OtherEquipment` objects.

        Raises:
            ValueError: if no objects of type `OtherEquipment` are present

        """
        return self._data["Internal Gains"]["otherequipment"]

    @property
    def zonebaseboardoutdoortemperaturecontrolleds(self):
        """Get list of all `ZoneBaseboardOutdoorTemperatureControlled` objects.

        Raises:
            ValueError: if no objects of type `ZoneBaseboardOutdoorTemperatureControlled` are present

        """
        return self._data["Internal Gains"][
            "zonebaseboard:outdoortemperaturecontrolled"]

    @property
    def zonecontaminantsourceandsinkcarbondioxides(self):
        """Get list of all `ZoneContaminantSourceAndSinkCarbonDioxide` objects.

        Raises:
            ValueError: if no objects of type `ZoneContaminantSourceAndSinkCarbonDioxide` are present

        """
        return self._data["Internal Gains"][
            "zonecontaminantsourceandsink:carbondioxide"]

    @property
    def zonecontaminantsourceandsinkgenericconstants(self):
        """Get list of all `ZoneContaminantSourceAndSinkGenericConstant`
        objects.

        Raises:
            ValueError: if no objects of type `ZoneContaminantSourceAndSinkGenericConstant` are present

        """
        return self._data["Internal Gains"][
            "zonecontaminantsourceandsink:generic:constant"]

    @property
    def surfacecontaminantsourceandsinkgenericpressuredrivens(self):
        """Get list of all
        `SurfaceContaminantSourceAndSinkGenericPressureDriven` objects.

        Raises:
            ValueError: if no objects of type `SurfaceContaminantSourceAndSinkGenericPressureDriven` are present

        """
        return self._data["Internal Gains"][
            "surfacecontaminantsourceandsink:generic:pressuredriven"]

    @property
    def zonecontaminantsourceandsinkgenericcutoffmodels(self):
        """Get list of all `ZoneContaminantSourceAndSinkGenericCutoffModel`
        objects.

        Raises:
            ValueError: if no objects of type `ZoneContaminantSourceAndSinkGenericCutoffModel` are present

        """
        return self._data["Internal Gains"][
            "zonecontaminantsourceandsink:generic:cutoffmodel"]

    @property
    def zonecontaminantsourceandsinkgenericdecaysources(self):
        """Get list of all `ZoneContaminantSourceAndSinkGenericDecaySource`
        objects.

        Raises:
            ValueError: if no objects of type `ZoneContaminantSourceAndSinkGenericDecaySource` are present

        """
        return self._data["Internal Gains"][
            "zonecontaminantsourceandsink:generic:decaysource"]

    @property
    def surfacecontaminantsourceandsinkgenericboundarylayerdiffusions(self):
        """Get list of all
        `SurfaceContaminantSourceAndSinkGenericBoundaryLayerDiffusion` objects.

        Raises:
            ValueError: if no objects of type `SurfaceContaminantSourceAndSinkGenericBoundaryLayerDiffusion` are present

        """
        return self._data["Internal Gains"][
            "surfacecontaminantsourceandsink:generic:boundarylayerdiffusion"]

    @property
    def surfacecontaminantsourceandsinkgenericdepositionvelocitysinks(self):
        """Get list of all
        `SurfaceContaminantSourceAndSinkGenericDepositionVelocitySink` objects.

        Raises:
            ValueError: if no objects of type `SurfaceContaminantSourceAndSinkGenericDepositionVelocitySink` are present

        """
        return self._data["Internal Gains"][
            "surfacecontaminantsourceandsink:generic:depositionvelocitysink"]

    @property
    def zonecontaminantsourceandsinkgenericdepositionratesinks(self):
        """Get list of all
        `ZoneContaminantSourceAndSinkGenericDepositionRateSink` objects.

        Raises:
            ValueError: if no objects of type `ZoneContaminantSourceAndSinkGenericDepositionRateSink` are present

        """
        return self._data["Internal Gains"][
            "zonecontaminantsourceandsink:generic:depositionratesink"]

    @property
    def daylightingcontrolss(self):
        """Get list of all `DaylightingControls` objects.

        Raises:
            ValueError: if no objects of type `DaylightingControls` are present

        """
        return self._data["Daylighting"]["daylighting:controls"]

    @property
    def daylightingdelightcontrolss(self):
        """Get list of all `DaylightingDelightControls` objects.

        Raises:
            ValueError: if no objects of type `DaylightingDelightControls` are present

        """
        return self._data["Daylighting"]["daylighting:delight:controls"]

    @property
    def daylightingdelightreferencepoints(self):
        """Get list of all `DaylightingDelightReferencePoint` objects.

        Raises:
            ValueError: if no objects of type `DaylightingDelightReferencePoint` are present

        """
        return self._data["Daylighting"]["daylighting:delight:referencepoint"]

    @property
    def daylightingdelightcomplexfenestrations(self):
        """Get list of all `DaylightingDelightComplexFenestration` objects.

        Raises:
            ValueError: if no objects of type `DaylightingDelightComplexFenestration` are present

        """
        return self._data["Daylighting"][
            "daylighting:delight:complexfenestration"]

    @property
    def daylightingdevicetubulars(self):
        """Get list of all `DaylightingDeviceTubular` objects.

        Raises:
            ValueError: if no objects of type `DaylightingDeviceTubular` are present

        """
        return self._data["Daylighting"]["daylightingdevice:tubular"]

    @property
    def daylightingdeviceshelfs(self):
        """Get list of all `DaylightingDeviceShelf` objects.

        Raises:
            ValueError: if no objects of type `DaylightingDeviceShelf` are present

        """
        return self._data["Daylighting"]["daylightingdevice:shelf"]

    @property
    def daylightingdevicelightwells(self):
        """Get list of all `DaylightingDeviceLightWell` objects.

        Raises:
            ValueError: if no objects of type `DaylightingDeviceLightWell` are present

        """
        return self._data["Daylighting"]["daylightingdevice:lightwell"]

    @property
    def outputdaylightfactorss(self):
        """Get list of all `OutputDaylightFactors` objects.

        Raises:
            ValueError: if no objects of type `OutputDaylightFactors` are present

        """
        return self._data["Daylighting"]["output:daylightfactors"]

    @property
    def outputilluminancemaps(self):
        """Get list of all `OutputIlluminanceMap` objects.

        Raises:
            ValueError: if no objects of type `OutputIlluminanceMap` are present

        """
        return self._data["Daylighting"]["output:illuminancemap"]

    @property
    def outputcontrolilluminancemapstyles(self):
        """Get list of all `OutputControlIlluminanceMapStyle` objects.

        Raises:
            ValueError: if no objects of type `OutputControlIlluminanceMapStyle` are present

        """
        return self._data["Daylighting"]["outputcontrol:illuminancemap:style"]

    @property
    def zoneinfiltrationdesignflowrates(self):
        """Get list of all `ZoneInfiltrationDesignFlowRate` objects.

        Raises:
            ValueError: if no objects of type `ZoneInfiltrationDesignFlowRate` are present

        """
        return self._data["Zone Airflow"]["zoneinfiltration:designflowrate"]

    @property
    def zoneinfiltrationeffectiveleakageareas(self):
        """Get list of all `ZoneInfiltrationEffectiveLeakageArea` objects.

        Raises:
            ValueError: if no objects of type `ZoneInfiltrationEffectiveLeakageArea` are present

        """
        return self._data["Zone Airflow"][
            "zoneinfiltration:effectiveleakagearea"]

    @property
    def zoneinfiltrationflowcoefficients(self):
        """Get list of all `ZoneInfiltrationFlowCoefficient` objects.

        Raises:
            ValueError: if no objects of type `ZoneInfiltrationFlowCoefficient` are present

        """
        return self._data["Zone Airflow"]["zoneinfiltration:flowcoefficient"]

    @property
    def zoneventilationdesignflowrates(self):
        """Get list of all `ZoneVentilationDesignFlowRate` objects.

        Raises:
            ValueError: if no objects of type `ZoneVentilationDesignFlowRate` are present

        """
        return self._data["Zone Airflow"]["zoneventilation:designflowrate"]

    @property
    def zoneventilationwindandstackopenareas(self):
        """Get list of all `ZoneVentilationWindandStackOpenArea` objects.

        Raises:
            ValueError: if no objects of type `ZoneVentilationWindandStackOpenArea` are present

        """
        return self._data["Zone Airflow"][
            "zoneventilation:windandstackopenarea"]

    @property
    def zoneairbalanceoutdoorairs(self):
        """Get list of all `ZoneAirBalanceOutdoorAir` objects.

        Raises:
            ValueError: if no objects of type `ZoneAirBalanceOutdoorAir` are present

        """
        return self._data["Zone Airflow"]["zoneairbalance:outdoorair"]

    @property
    def zonemixings(self):
        """Get list of all `ZoneMixing` objects.

        Raises:
            ValueError: if no objects of type `ZoneMixing` are present

        """
        return self._data["Zone Airflow"]["zonemixing"]

    @property
    def zonecrossmixings(self):
        """Get list of all `ZoneCrossMixing` objects.

        Raises:
            ValueError: if no objects of type `ZoneCrossMixing` are present

        """
        return self._data["Zone Airflow"]["zonecrossmixing"]

    @property
    def zonerefrigerationdoormixings(self):
        """Get list of all `ZoneRefrigerationDoorMixing` objects.

        Raises:
            ValueError: if no objects of type `ZoneRefrigerationDoorMixing` are present

        """
        return self._data["Zone Airflow"]["zonerefrigerationdoormixing"]

    @property
    def zoneearthtubes(self):
        """Get list of all `ZoneEarthtube` objects.

        Raises:
            ValueError: if no objects of type `ZoneEarthtube` are present

        """
        return self._data["Zone Airflow"]["zoneearthtube"]

    @property
    def zonecooltowershowers(self):
        """Get list of all `ZoneCoolTowerShower` objects.

        Raises:
            ValueError: if no objects of type `ZoneCoolTowerShower` are present

        """
        return self._data["Zone Airflow"]["zonecooltower:shower"]

    @property
    def zonethermalchimneys(self):
        """Get list of all `ZoneThermalChimney` objects.

        Raises:
            ValueError: if no objects of type `ZoneThermalChimney` are present

        """
        return self._data["Zone Airflow"]["zonethermalchimney"]

    @property
    def airflownetworksimulationcontrols(self):
        """Get list of all `AirflowNetworkSimulationControl` objects.

        Raises:
            ValueError: if no objects of type `AirflowNetworkSimulationControl` are present

        """
        return self._data["Natural Ventilation and Duct Leakage"][
            "airflownetwork:simulationcontrol"]

    @property
    def airflownetworkmultizonezones(self):
        """Get list of all `AirflowNetworkMultiZoneZone` objects.

        Raises:
            ValueError: if no objects of type `AirflowNetworkMultiZoneZone` are present

        """
        return self._data["Natural Ventilation and Duct Leakage"][
            "airflownetwork:multizone:zone"]

    @property
    def airflownetworkmultizonesurfaces(self):
        """Get list of all `AirflowNetworkMultiZoneSurface` objects.

        Raises:
            ValueError: if no objects of type `AirflowNetworkMultiZoneSurface` are present

        """
        return self._data["Natural Ventilation and Duct Leakage"][
            "airflownetwork:multizone:surface"]

    @property
    def airflownetworkmultizonereferencecrackconditionss(self):
        """Get list of all `AirflowNetworkMultiZoneReferenceCrackConditions`
        objects.

        Raises:
            ValueError: if no objects of type `AirflowNetworkMultiZoneReferenceCrackConditions` are present

        """
        return self._data["Natural Ventilation and Duct Leakage"][
            "airflownetwork:multizone:referencecrackconditions"]

    @property
    def airflownetworkmultizonesurfacecracks(self):
        """Get list of all `AirflowNetworkMultiZoneSurfaceCrack` objects.

        Raises:
            ValueError: if no objects of type `AirflowNetworkMultiZoneSurfaceCrack` are present

        """
        return self._data["Natural Ventilation and Duct Leakage"][
            "airflownetwork:multizone:surface:crack"]

    @property
    def airflownetworkmultizonesurfaceeffectiveleakageareas(self):
        """Get list of all `AirflowNetworkMultiZoneSurfaceEffectiveLeakageArea`
        objects.

        Raises:
            ValueError: if no objects of type `AirflowNetworkMultiZoneSurfaceEffectiveLeakageArea` are present

        """
        return self._data["Natural Ventilation and Duct Leakage"][
            "airflownetwork:multizone:surface:effectiveleakagearea"]

    @property
    def airflownetworkmultizonecomponentdetailedopenings(self):
        """Get list of all `AirflowNetworkMultiZoneComponentDetailedOpening`
        objects.

        Raises:
            ValueError: if no objects of type `AirflowNetworkMultiZoneComponentDetailedOpening` are present

        """
        return self._data["Natural Ventilation and Duct Leakage"][
            "airflownetwork:multizone:component:detailedopening"]

    @property
    def airflownetworkmultizonecomponentsimpleopenings(self):
        """Get list of all `AirflowNetworkMultiZoneComponentSimpleOpening`
        objects.

        Raises:
            ValueError: if no objects of type `AirflowNetworkMultiZoneComponentSimpleOpening` are present

        """
        return self._data["Natural Ventilation and Duct Leakage"][
            "airflownetwork:multizone:component:simpleopening"]

    @property
    def airflownetworkmultizonecomponenthorizontalopenings(self):
        """Get list of all `AirflowNetworkMultiZoneComponentHorizontalOpening`
        objects.

        Raises:
            ValueError: if no objects of type `AirflowNetworkMultiZoneComponentHorizontalOpening` are present

        """
        return self._data["Natural Ventilation and Duct Leakage"][
            "airflownetwork:multizone:component:horizontalopening"]

    @property
    def airflownetworkmultizonecomponentzoneexhaustfans(self):
        """Get list of all `AirflowNetworkMultiZoneComponentZoneExhaustFan`
        objects.

        Raises:
            ValueError: if no objects of type `AirflowNetworkMultiZoneComponentZoneExhaustFan` are present

        """
        return self._data["Natural Ventilation and Duct Leakage"][
            "airflownetwork:multizone:component:zoneexhaustfan"]

    @property
    def airflownetworkmultizoneexternalnodes(self):
        """Get list of all `AirflowNetworkMultiZoneExternalNode` objects.

        Raises:
            ValueError: if no objects of type `AirflowNetworkMultiZoneExternalNode` are present

        """
        return self._data["Natural Ventilation and Duct Leakage"][
            "airflownetwork:multizone:externalnode"]

    @property
    def airflownetworkmultizonewindpressurecoefficientarrays(self):
        """Get list of all
        `AirflowNetworkMultiZoneWindPressureCoefficientArray` objects.

        Raises:
            ValueError: if no objects of type `AirflowNetworkMultiZoneWindPressureCoefficientArray` are present

        """
        return self._data["Natural Ventilation and Duct Leakage"][
            "airflownetwork:multizone:windpressurecoefficientarray"]

    @property
    def airflownetworkmultizonewindpressurecoefficientvaluess(self):
        """Get list of all
        `AirflowNetworkMultiZoneWindPressureCoefficientValues` objects.

        Raises:
            ValueError: if no objects of type `AirflowNetworkMultiZoneWindPressureCoefficientValues` are present

        """
        return self._data["Natural Ventilation and Duct Leakage"][
            "airflownetwork:multizone:windpressurecoefficientvalues"]

    @property
    def airflownetworkdistributionnodes(self):
        """Get list of all `AirflowNetworkDistributionNode` objects.

        Raises:
            ValueError: if no objects of type `AirflowNetworkDistributionNode` are present

        """
        return self._data["Natural Ventilation and Duct Leakage"][
            "airflownetwork:distribution:node"]

    @property
    def airflownetworkdistributioncomponentleaks(self):
        """Get list of all `AirflowNetworkDistributionComponentLeak` objects.

        Raises:
            ValueError: if no objects of type `AirflowNetworkDistributionComponentLeak` are present

        """
        return self._data["Natural Ventilation and Duct Leakage"][
            "airflownetwork:distribution:component:leak"]

    @property
    def airflownetworkdistributioncomponentleakageratios(self):
        """Get list of all `AirflowNetworkDistributionComponentLeakageRatio`
        objects.

        Raises:
            ValueError: if no objects of type `AirflowNetworkDistributionComponentLeakageRatio` are present

        """
        return self._data["Natural Ventilation and Duct Leakage"][
            "airflownetwork:distribution:component:leakageratio"]

    @property
    def airflownetworkdistributioncomponentducts(self):
        """Get list of all `AirflowNetworkDistributionComponentDuct` objects.

        Raises:
            ValueError: if no objects of type `AirflowNetworkDistributionComponentDuct` are present

        """
        return self._data["Natural Ventilation and Duct Leakage"][
            "airflownetwork:distribution:component:duct"]

    @property
    def airflownetworkdistributioncomponentfans(self):
        """Get list of all `AirflowNetworkDistributionComponentFan` objects.

        Raises:
            ValueError: if no objects of type `AirflowNetworkDistributionComponentFan` are present

        """
        return self._data["Natural Ventilation and Duct Leakage"][
            "airflownetwork:distribution:component:fan"]

    @property
    def airflownetworkdistributioncomponentcoils(self):
        """Get list of all `AirflowNetworkDistributionComponentCoil` objects.

        Raises:
            ValueError: if no objects of type `AirflowNetworkDistributionComponentCoil` are present

        """
        return self._data["Natural Ventilation and Duct Leakage"][
            "airflownetwork:distribution:component:coil"]

    @property
    def airflownetworkdistributioncomponentheatexchangers(self):
        """Get list of all `AirflowNetworkDistributionComponentHeatExchanger`
        objects.

        Raises:
            ValueError: if no objects of type `AirflowNetworkDistributionComponentHeatExchanger` are present

        """
        return self._data["Natural Ventilation and Duct Leakage"][
            "airflownetwork:distribution:component:heatexchanger"]

    @property
    def airflownetworkdistributioncomponentterminalunits(self):
        """Get list of all `AirflowNetworkDistributionComponentTerminalUnit`
        objects.

        Raises:
            ValueError: if no objects of type `AirflowNetworkDistributionComponentTerminalUnit` are present

        """
        return self._data["Natural Ventilation and Duct Leakage"][
            "airflownetwork:distribution:component:terminalunit"]

    @property
    def airflownetworkdistributioncomponentconstantpressuredrops(self):
        """Get list of all
        `AirflowNetworkDistributionComponentConstantPressureDrop` objects.

        Raises:
            ValueError: if no objects of type `AirflowNetworkDistributionComponentConstantPressureDrop` are present

        """
        return self._data["Natural Ventilation and Duct Leakage"][
            "airflownetwork:distribution:component:constantpressuredrop"]

    @property
    def airflownetworkdistributionlinkages(self):
        """Get list of all `AirflowNetworkDistributionLinkage` objects.

        Raises:
            ValueError: if no objects of type `AirflowNetworkDistributionLinkage` are present

        """
        return self._data["Natural Ventilation and Duct Leakage"][
            "airflownetwork:distribution:linkage"]

    @property
    def exteriorlightss(self):
        """Get list of all `ExteriorLights` objects.

        Raises:
            ValueError: if no objects of type `ExteriorLights` are present

        """
        return self._data["Exterior Equipment"]["exterior:lights"]

    @property
    def exteriorfuelequipments(self):
        """Get list of all `ExteriorFuelEquipment` objects.

        Raises:
            ValueError: if no objects of type `ExteriorFuelEquipment` are present

        """
        return self._data["Exterior Equipment"]["exterior:fuelequipment"]

    @property
    def exteriorwaterequipments(self):
        """Get list of all `ExteriorWaterEquipment` objects.

        Raises:
            ValueError: if no objects of type `ExteriorWaterEquipment` are present

        """
        return self._data["Exterior Equipment"]["exterior:waterequipment"]

    @property
    def hvactemplatethermostats(self):
        """Get list of all `HvactemplateThermostat` objects.

        Raises:
            ValueError: if no objects of type `HvactemplateThermostat` are present

        """
        return self._data["HVAC Templates"]["hvactemplate:thermostat"]

    @property
    def hvactemplatezoneidealloadsairsystems(self):
        """Get list of all `HvactemplateZoneIdealLoadsAirSystem` objects.

        Raises:
            ValueError: if no objects of type `HvactemplateZoneIdealLoadsAirSystem` are present

        """
        return self._data["HVAC Templates"][
            "hvactemplate:zone:idealloadsairsystem"]

    @property
    def hvactemplatezonebaseboardheats(self):
        """Get list of all `HvactemplateZoneBaseboardHeat` objects.

        Raises:
            ValueError: if no objects of type `HvactemplateZoneBaseboardHeat` are present

        """
        return self._data["HVAC Templates"]["hvactemplate:zone:baseboardheat"]

    @property
    def hvactemplatezonefancoils(self):
        """Get list of all `HvactemplateZoneFanCoil` objects.

        Raises:
            ValueError: if no objects of type `HvactemplateZoneFanCoil` are present

        """
        return self._data["HVAC Templates"]["hvactemplate:zone:fancoil"]

    @property
    def hvactemplatezoneptacs(self):
        """Get list of all `HvactemplateZonePtac` objects.

        Raises:
            ValueError: if no objects of type `HvactemplateZonePtac` are present

        """
        return self._data["HVAC Templates"]["hvactemplate:zone:ptac"]

    @property
    def hvactemplatezonepthps(self):
        """Get list of all `HvactemplateZonePthp` objects.

        Raises:
            ValueError: if no objects of type `HvactemplateZonePthp` are present

        """
        return self._data["HVAC Templates"]["hvactemplate:zone:pthp"]

    @property
    def hvactemplatezonewatertoairheatpumps(self):
        """Get list of all `HvactemplateZoneWaterToAirHeatPump` objects.

        Raises:
            ValueError: if no objects of type `HvactemplateZoneWaterToAirHeatPump` are present

        """
        return self._data["HVAC Templates"][
            "hvactemplate:zone:watertoairheatpump"]

    @property
    def hvactemplatezonevrfs(self):
        """Get list of all `HvactemplateZoneVrf` objects.

        Raises:
            ValueError: if no objects of type `HvactemplateZoneVrf` are present

        """
        return self._data["HVAC Templates"]["hvactemplate:zone:vrf"]

    @property
    def hvactemplatezoneunitarys(self):
        """Get list of all `HvactemplateZoneUnitary` objects.

        Raises:
            ValueError: if no objects of type `HvactemplateZoneUnitary` are present

        """
        return self._data["HVAC Templates"]["hvactemplate:zone:unitary"]

    @property
    def hvactemplatezonevavs(self):
        """Get list of all `HvactemplateZoneVav` objects.

        Raises:
            ValueError: if no objects of type `HvactemplateZoneVav` are present

        """
        return self._data["HVAC Templates"]["hvactemplate:zone:vav"]

    @property
    def hvactemplatezonevavfanpowereds(self):
        """Get list of all `HvactemplateZoneVavFanPowered` objects.

        Raises:
            ValueError: if no objects of type `HvactemplateZoneVavFanPowered` are present

        """
        return self._data["HVAC Templates"]["hvactemplate:zone:vav:fanpowered"]

    @property
    def hvactemplatezonevavheatandcools(self):
        """Get list of all `HvactemplateZoneVavHeatAndCool` objects.

        Raises:
            ValueError: if no objects of type `HvactemplateZoneVavHeatAndCool` are present

        """
        return self._data["HVAC Templates"][
            "hvactemplate:zone:vav:heatandcool"]

    @property
    def hvactemplatezoneconstantvolumes(self):
        """Get list of all `HvactemplateZoneConstantVolume` objects.

        Raises:
            ValueError: if no objects of type `HvactemplateZoneConstantVolume` are present

        """
        return self._data["HVAC Templates"]["hvactemplate:zone:constantvolume"]

    @property
    def hvactemplatezonedualducts(self):
        """Get list of all `HvactemplateZoneDualDuct` objects.

        Raises:
            ValueError: if no objects of type `HvactemplateZoneDualDuct` are present

        """
        return self._data["HVAC Templates"]["hvactemplate:zone:dualduct"]

    @property
    def hvactemplatesystemvrfs(self):
        """Get list of all `HvactemplateSystemVrf` objects.

        Raises:
            ValueError: if no objects of type `HvactemplateSystemVrf` are present

        """
        return self._data["HVAC Templates"]["hvactemplate:system:vrf"]

    @property
    def hvactemplatesystemunitarys(self):
        """Get list of all `HvactemplateSystemUnitary` objects.

        Raises:
            ValueError: if no objects of type `HvactemplateSystemUnitary` are present

        """
        return self._data["HVAC Templates"]["hvactemplate:system:unitary"]

    @property
    def hvactemplatesystemunitaryheatpumpairtoairs(self):
        """Get list of all `HvactemplateSystemUnitaryHeatPumpAirToAir` objects.

        Raises:
            ValueError: if no objects of type `HvactemplateSystemUnitaryHeatPumpAirToAir` are present

        """
        return self._data["HVAC Templates"][
            "hvactemplate:system:unitaryheatpump:airtoair"]

    @property
    def hvactemplatesystemunitarysystems(self):
        """Get list of all `HvactemplateSystemUnitarySystem` objects.

        Raises:
            ValueError: if no objects of type `HvactemplateSystemUnitarySystem` are present

        """
        return self._data["HVAC Templates"][
            "hvactemplate:system:unitarysystem"]

    @property
    def hvactemplatesystemvavs(self):
        """Get list of all `HvactemplateSystemVav` objects.

        Raises:
            ValueError: if no objects of type `HvactemplateSystemVav` are present

        """
        return self._data["HVAC Templates"]["hvactemplate:system:vav"]

    @property
    def hvactemplatesystempackagedvavs(self):
        """Get list of all `HvactemplateSystemPackagedVav` objects.

        Raises:
            ValueError: if no objects of type `HvactemplateSystemPackagedVav` are present

        """
        return self._data["HVAC Templates"]["hvactemplate:system:packagedvav"]

    @property
    def hvactemplatesystemconstantvolumes(self):
        """Get list of all `HvactemplateSystemConstantVolume` objects.

        Raises:
            ValueError: if no objects of type `HvactemplateSystemConstantVolume` are present

        """
        return self._data["HVAC Templates"][
            "hvactemplate:system:constantvolume"]

    @property
    def hvactemplatesystemdualducts(self):
        """Get list of all `HvactemplateSystemDualDuct` objects.

        Raises:
            ValueError: if no objects of type `HvactemplateSystemDualDuct` are present

        """
        return self._data["HVAC Templates"]["hvactemplate:system:dualduct"]

    @property
    def hvactemplatesystemdedicatedoutdoorairs(self):
        """Get list of all `HvactemplateSystemDedicatedOutdoorAir` objects.

        Raises:
            ValueError: if no objects of type `HvactemplateSystemDedicatedOutdoorAir` are present

        """
        return self._data["HVAC Templates"][
            "hvactemplate:system:dedicatedoutdoorair"]

    @property
    def hvactemplateplantchilledwaterloops(self):
        """Get list of all `HvactemplatePlantChilledWaterLoop` objects.

        Raises:
            ValueError: if no objects of type `HvactemplatePlantChilledWaterLoop` are present

        """
        return self._data["HVAC Templates"][
            "hvactemplate:plant:chilledwaterloop"]

    @property
    def hvactemplateplantchillers(self):
        """Get list of all `HvactemplatePlantChiller` objects.

        Raises:
            ValueError: if no objects of type `HvactemplatePlantChiller` are present

        """
        return self._data["HVAC Templates"]["hvactemplate:plant:chiller"]

    @property
    def hvactemplateplantchillerobjectreferences(self):
        """Get list of all `HvactemplatePlantChillerObjectReference` objects.

        Raises:
            ValueError: if no objects of type `HvactemplatePlantChillerObjectReference` are present

        """
        return self._data["HVAC Templates"][
            "hvactemplate:plant:chiller:objectreference"]

    @property
    def hvactemplateplanttowers(self):
        """Get list of all `HvactemplatePlantTower` objects.

        Raises:
            ValueError: if no objects of type `HvactemplatePlantTower` are present

        """
        return self._data["HVAC Templates"]["hvactemplate:plant:tower"]

    @property
    def hvactemplateplanttowerobjectreferences(self):
        """Get list of all `HvactemplatePlantTowerObjectReference` objects.

        Raises:
            ValueError: if no objects of type `HvactemplatePlantTowerObjectReference` are present

        """
        return self._data["HVAC Templates"][
            "hvactemplate:plant:tower:objectreference"]

    @property
    def hvactemplateplanthotwaterloops(self):
        """Get list of all `HvactemplatePlantHotWaterLoop` objects.

        Raises:
            ValueError: if no objects of type `HvactemplatePlantHotWaterLoop` are present

        """
        return self._data["HVAC Templates"]["hvactemplate:plant:hotwaterloop"]

    @property
    def hvactemplateplantboilers(self):
        """Get list of all `HvactemplatePlantBoiler` objects.

        Raises:
            ValueError: if no objects of type `HvactemplatePlantBoiler` are present

        """
        return self._data["HVAC Templates"]["hvactemplate:plant:boiler"]

    @property
    def hvactemplateplantboilerobjectreferences(self):
        """Get list of all `HvactemplatePlantBoilerObjectReference` objects.

        Raises:
            ValueError: if no objects of type `HvactemplatePlantBoilerObjectReference` are present

        """
        return self._data["HVAC Templates"][
            "hvactemplate:plant:boiler:objectreference"]

    @property
    def hvactemplateplantmixedwaterloops(self):
        """Get list of all `HvactemplatePlantMixedWaterLoop` objects.

        Raises:
            ValueError: if no objects of type `HvactemplatePlantMixedWaterLoop` are present

        """
        return self._data["HVAC Templates"][
            "hvactemplate:plant:mixedwaterloop"]

    @property
    def designspecificationoutdoorairs(self):
        """Get list of all `DesignSpecificationOutdoorAir` objects.

        Raises:
            ValueError: if no objects of type `DesignSpecificationOutdoorAir` are present

        """
        return self._data["HVAC Design Objects"][
            "designspecification:outdoorair"]

    @property
    def designspecificationzoneairdistributions(self):
        """Get list of all `DesignSpecificationZoneAirDistribution` objects.

        Raises:
            ValueError: if no objects of type `DesignSpecificationZoneAirDistribution` are present

        """
        return self._data["HVAC Design Objects"][
            "designspecification:zoneairdistribution"]

    @property
    def sizingparameterss(self):
        """Get list of all `SizingParameters` objects.

        Raises:
            ValueError: if no objects of type `SizingParameters` are present

        """
        return self._data["HVAC Design Objects"]["sizing:parameters"]

    @property
    def sizingzones(self):
        """Get list of all `SizingZone` objects.

        Raises:
            ValueError: if no objects of type `SizingZone` are present

        """
        return self._data["HVAC Design Objects"]["sizing:zone"]

    @property
    def designspecificationzonehvacsizings(self):
        """Get list of all `DesignSpecificationZoneHvacSizing` objects.

        Raises:
            ValueError: if no objects of type `DesignSpecificationZoneHvacSizing` are present

        """
        return self._data["HVAC Design Objects"][
            "designspecification:zonehvac:sizing"]

    @property
    def sizingsystems(self):
        """Get list of all `SizingSystem` objects.

        Raises:
            ValueError: if no objects of type `SizingSystem` are present

        """
        return self._data["HVAC Design Objects"]["sizing:system"]

    @property
    def sizingplants(self):
        """Get list of all `SizingPlant` objects.

        Raises:
            ValueError: if no objects of type `SizingPlant` are present

        """
        return self._data["HVAC Design Objects"]["sizing:plant"]

    @property
    def outputcontrolsizingstyles(self):
        """Get list of all `OutputControlSizingStyle` objects.

        Raises:
            ValueError: if no objects of type `OutputControlSizingStyle` are present

        """
        return self._data["HVAC Design Objects"]["outputcontrol:sizing:style"]

    @property
    def zonecontrolhumidistats(self):
        """Get list of all `ZoneControlHumidistat` objects.

        Raises:
            ValueError: if no objects of type `ZoneControlHumidistat` are present

        """
        return self._data["Zone HVAC Controls and Thermostats"][
            "zonecontrol:humidistat"]

    @property
    def zonecontrolthermostats(self):
        """Get list of all `ZoneControlThermostat` objects.

        Raises:
            ValueError: if no objects of type `ZoneControlThermostat` are present

        """
        return self._data["Zone HVAC Controls and Thermostats"][
            "zonecontrol:thermostat"]

    @property
    def zonecontrolthermostatoperativetemperatures(self):
        """Get list of all `ZoneControlThermostatOperativeTemperature` objects.

        Raises:
            ValueError: if no objects of type `ZoneControlThermostatOperativeTemperature` are present

        """
        return self._data["Zone HVAC Controls and Thermostats"][
            "zonecontrol:thermostat:operativetemperature"]

    @property
    def zonecontrolthermostatthermalcomforts(self):
        """Get list of all `ZoneControlThermostatThermalComfort` objects.

        Raises:
            ValueError: if no objects of type `ZoneControlThermostatThermalComfort` are present

        """
        return self._data["Zone HVAC Controls and Thermostats"][
            "zonecontrol:thermostat:thermalcomfort"]

    @property
    def zonecontrolthermostattemperatureandhumiditys(self):
        """Get list of all `ZoneControlThermostatTemperatureAndHumidity`
        objects.

        Raises:
            ValueError: if no objects of type `ZoneControlThermostatTemperatureAndHumidity` are present

        """
        return self._data["Zone HVAC Controls and Thermostats"][
            "zonecontrol:thermostat:temperatureandhumidity"]

    @property
    def thermostatsetpointsingleheatings(self):
        """Get list of all `ThermostatSetpointSingleHeating` objects.

        Raises:
            ValueError: if no objects of type `ThermostatSetpointSingleHeating` are present

        """
        return self._data["Zone HVAC Controls and Thermostats"][
            "thermostatsetpoint:singleheating"]

    @property
    def thermostatsetpointsinglecoolings(self):
        """Get list of all `ThermostatSetpointSingleCooling` objects.

        Raises:
            ValueError: if no objects of type `ThermostatSetpointSingleCooling` are present

        """
        return self._data["Zone HVAC Controls and Thermostats"][
            "thermostatsetpoint:singlecooling"]

    @property
    def thermostatsetpointsingleheatingorcoolings(self):
        """Get list of all `ThermostatSetpointSingleHeatingOrCooling` objects.

        Raises:
            ValueError: if no objects of type `ThermostatSetpointSingleHeatingOrCooling` are present

        """
        return self._data["Zone HVAC Controls and Thermostats"][
            "thermostatsetpoint:singleheatingorcooling"]

    @property
    def thermostatsetpointdualsetpoints(self):
        """Get list of all `ThermostatSetpointDualSetpoint` objects.

        Raises:
            ValueError: if no objects of type `ThermostatSetpointDualSetpoint` are present

        """
        return self._data["Zone HVAC Controls and Thermostats"][
            "thermostatsetpoint:dualsetpoint"]

    @property
    def thermostatsetpointthermalcomfortfangersingleheatings(self):
        """Get list of all
        `ThermostatSetpointThermalComfortFangerSingleHeating` objects.

        Raises:
            ValueError: if no objects of type `ThermostatSetpointThermalComfortFangerSingleHeating` are present

        """
        return self._data["Zone HVAC Controls and Thermostats"][
            "thermostatsetpoint:thermalcomfort:fanger:singleheating"]

    @property
    def thermostatsetpointthermalcomfortfangersinglecoolings(self):
        """Get list of all
        `ThermostatSetpointThermalComfortFangerSingleCooling` objects.

        Raises:
            ValueError: if no objects of type `ThermostatSetpointThermalComfortFangerSingleCooling` are present

        """
        return self._data["Zone HVAC Controls and Thermostats"][
            "thermostatsetpoint:thermalcomfort:fanger:singlecooling"]

    @property
    def thermostatsetpointthermalcomfortfangersingleheatingorcoolings(self):
        """Get list of all
        `ThermostatSetpointThermalComfortFangerSingleHeatingOrCooling` objects.

        Raises:
            ValueError: if no objects of type `ThermostatSetpointThermalComfortFangerSingleHeatingOrCooling` are present

        """
        return self._data["Zone HVAC Controls and Thermostats"][
            "thermostatsetpoint:thermalcomfort:fanger:singleheatingorcooling"]

    @property
    def thermostatsetpointthermalcomfortfangerdualsetpoints(self):
        """Get list of all `ThermostatSetpointThermalComfortFangerDualSetpoint`
        objects.

        Raises:
            ValueError: if no objects of type `ThermostatSetpointThermalComfortFangerDualSetpoint` are present

        """
        return self._data["Zone HVAC Controls and Thermostats"][
            "thermostatsetpoint:thermalcomfort:fanger:dualsetpoint"]

    @property
    def zonecontrolthermostatstageddualsetpoints(self):
        """Get list of all `ZoneControlThermostatStagedDualSetpoint` objects.

        Raises:
            ValueError: if no objects of type `ZoneControlThermostatStagedDualSetpoint` are present

        """
        return self._data["Zone HVAC Controls and Thermostats"][
            "zonecontrol:thermostat:stageddualsetpoint"]

    @property
    def zonecontrolcontaminantcontrollers(self):
        """Get list of all `ZoneControlContaminantController` objects.

        Raises:
            ValueError: if no objects of type `ZoneControlContaminantController` are present

        """
        return self._data["Zone HVAC Controls and Thermostats"][
            "zonecontrol:contaminantcontroller"]

    @property
    def zonehvacidealloadsairsystems(self):
        """Get list of all `ZoneHvacIdealLoadsAirSystem` objects.

        Raises:
            ValueError: if no objects of type `ZoneHvacIdealLoadsAirSystem` are present

        """
        return self._data["Zone HVAC Forced Air Units"][
            "zonehvac:idealloadsairsystem"]

    @property
    def zonehvacfourpipefancoils(self):
        """Get list of all `ZoneHvacFourPipeFanCoil` objects.

        Raises:
            ValueError: if no objects of type `ZoneHvacFourPipeFanCoil` are present

        """
        return self._data["Zone HVAC Forced Air Units"][
            "zonehvac:fourpipefancoil"]

    @property
    def zonehvacwindowairconditioners(self):
        """Get list of all `ZoneHvacWindowAirConditioner` objects.

        Raises:
            ValueError: if no objects of type `ZoneHvacWindowAirConditioner` are present

        """
        return self._data["Zone HVAC Forced Air Units"][
            "zonehvac:windowairconditioner"]

    @property
    def zonehvacpackagedterminalairconditioners(self):
        """Get list of all `ZoneHvacPackagedTerminalAirConditioner` objects.

        Raises:
            ValueError: if no objects of type `ZoneHvacPackagedTerminalAirConditioner` are present

        """
        return self._data["Zone HVAC Forced Air Units"][
            "zonehvac:packagedterminalairconditioner"]

    @property
    def zonehvacpackagedterminalheatpumps(self):
        """Get list of all `ZoneHvacPackagedTerminalHeatPump` objects.

        Raises:
            ValueError: if no objects of type `ZoneHvacPackagedTerminalHeatPump` are present

        """
        return self._data["Zone HVAC Forced Air Units"][
            "zonehvac:packagedterminalheatpump"]

    @property
    def zonehvacwatertoairheatpumps(self):
        """Get list of all `ZoneHvacWaterToAirHeatPump` objects.

        Raises:
            ValueError: if no objects of type `ZoneHvacWaterToAirHeatPump` are present

        """
        return self._data["Zone HVAC Forced Air Units"][
            "zonehvac:watertoairheatpump"]

    @property
    def zonehvacdehumidifierdxs(self):
        """Get list of all `ZoneHvacDehumidifierDx` objects.

        Raises:
            ValueError: if no objects of type `ZoneHvacDehumidifierDx` are present

        """
        return self._data["Zone HVAC Forced Air Units"][
            "zonehvac:dehumidifier:dx"]

    @property
    def zonehvacenergyrecoveryventilators(self):
        """Get list of all `ZoneHvacEnergyRecoveryVentilator` objects.

        Raises:
            ValueError: if no objects of type `ZoneHvacEnergyRecoveryVentilator` are present

        """
        return self._data["Zone HVAC Forced Air Units"][
            "zonehvac:energyrecoveryventilator"]

    @property
    def zonehvacenergyrecoveryventilatorcontrollers(self):
        """Get list of all `ZoneHvacEnergyRecoveryVentilatorController`
        objects.

        Raises:
            ValueError: if no objects of type `ZoneHvacEnergyRecoveryVentilatorController` are present

        """
        return self._data["Zone HVAC Forced Air Units"][
            "zonehvac:energyrecoveryventilator:controller"]

    @property
    def zonehvacunitventilators(self):
        """Get list of all `ZoneHvacUnitVentilator` objects.

        Raises:
            ValueError: if no objects of type `ZoneHvacUnitVentilator` are present

        """
        return self._data["Zone HVAC Forced Air Units"][
            "zonehvac:unitventilator"]

    @property
    def zonehvacunitheaters(self):
        """Get list of all `ZoneHvacUnitHeater` objects.

        Raises:
            ValueError: if no objects of type `ZoneHvacUnitHeater` are present

        """
        return self._data["Zone HVAC Forced Air Units"]["zonehvac:unitheater"]

    @property
    def zonehvacevaporativecoolerunits(self):
        """Get list of all `ZoneHvacEvaporativeCoolerUnit` objects.

        Raises:
            ValueError: if no objects of type `ZoneHvacEvaporativeCoolerUnit` are present

        """
        return self._data["Zone HVAC Forced Air Units"][
            "zonehvac:evaporativecoolerunit"]

    @property
    def zonehvacoutdoorairunits(self):
        """Get list of all `ZoneHvacOutdoorAirUnit` objects.

        Raises:
            ValueError: if no objects of type `ZoneHvacOutdoorAirUnit` are present

        """
        return self._data["Zone HVAC Forced Air Units"][
            "zonehvac:outdoorairunit"]

    @property
    def zonehvacoutdoorairunitequipmentlists(self):
        """Get list of all `ZoneHvacOutdoorAirUnitEquipmentList` objects.

        Raises:
            ValueError: if no objects of type `ZoneHvacOutdoorAirUnitEquipmentList` are present

        """
        return self._data["Zone HVAC Forced Air Units"][
            "zonehvac:outdoorairunit:equipmentlist"]

    @property
    def zonehvacterminalunitvariablerefrigerantflows(self):
        """Get list of all `ZoneHvacTerminalUnitVariableRefrigerantFlow`
        objects.

        Raises:
            ValueError: if no objects of type `ZoneHvacTerminalUnitVariableRefrigerantFlow` are present

        """
        return self._data["Zone HVAC Forced Air Units"][
            "zonehvac:terminalunit:variablerefrigerantflow"]

    @property
    def zonehvacbaseboardradiantconvectivewaters(self):
        """Get list of all `ZoneHvacBaseboardRadiantConvectiveWater` objects.

        Raises:
            ValueError: if no objects of type `ZoneHvacBaseboardRadiantConvectiveWater` are present

        """
        return self._data["Zone HVAC Radiative"][
            "zonehvac:baseboard:radiantconvective:water"]

    @property
    def zonehvacbaseboardradiantconvectivesteams(self):
        """Get list of all `ZoneHvacBaseboardRadiantConvectiveSteam` objects.

        Raises:
            ValueError: if no objects of type `ZoneHvacBaseboardRadiantConvectiveSteam` are present

        """
        return self._data["Zone HVAC Radiative"][
            "zonehvac:baseboard:radiantconvective:steam"]

    @property
    def zonehvacbaseboardradiantconvectiveelectrics(self):
        """Get list of all `ZoneHvacBaseboardRadiantConvectiveElectric`
        objects.

        Raises:
            ValueError: if no objects of type `ZoneHvacBaseboardRadiantConvectiveElectric` are present

        """
        return self._data["Zone HVAC Radiative"][
            "zonehvac:baseboard:radiantconvective:electric"]

    @property
    def zonehvacbaseboardconvectivewaters(self):
        """Get list of all `ZoneHvacBaseboardConvectiveWater` objects.

        Raises:
            ValueError: if no objects of type `ZoneHvacBaseboardConvectiveWater` are present

        """
        return self._data["Zone HVAC Radiative"][
            "zonehvac:baseboard:convective:water"]

    @property
    def zonehvacbaseboardconvectiveelectrics(self):
        """Get list of all `ZoneHvacBaseboardConvectiveElectric` objects.

        Raises:
            ValueError: if no objects of type `ZoneHvacBaseboardConvectiveElectric` are present

        """
        return self._data["Zone HVAC Radiative"][
            "zonehvac:baseboard:convective:electric"]

    @property
    def zonehvaclowtemperatureradiantvariableflows(self):
        """Get list of all `ZoneHvacLowTemperatureRadiantVariableFlow` objects.

        Raises:
            ValueError: if no objects of type `ZoneHvacLowTemperatureRadiantVariableFlow` are present

        """
        return self._data["Zone HVAC Radiative"][
            "zonehvac:lowtemperatureradiant:variableflow"]

    @property
    def zonehvaclowtemperatureradiantconstantflows(self):
        """Get list of all `ZoneHvacLowTemperatureRadiantConstantFlow` objects.

        Raises:
            ValueError: if no objects of type `ZoneHvacLowTemperatureRadiantConstantFlow` are present

        """
        return self._data["Zone HVAC Radiative"][
            "zonehvac:lowtemperatureradiant:constantflow"]

    @property
    def zonehvaclowtemperatureradiantelectrics(self):
        """Get list of all `ZoneHvacLowTemperatureRadiantElectric` objects.

        Raises:
            ValueError: if no objects of type `ZoneHvacLowTemperatureRadiantElectric` are present

        """
        return self._data["Zone HVAC Radiative"][
            "zonehvac:lowtemperatureradiant:electric"]

    @property
    def zonehvaclowtemperatureradiantsurfacegroups(self):
        """Get list of all `ZoneHvacLowTemperatureRadiantSurfaceGroup` objects.

        Raises:
            ValueError: if no objects of type `ZoneHvacLowTemperatureRadiantSurfaceGroup` are present

        """
        return self._data["Zone HVAC Radiative"][
            "zonehvac:lowtemperatureradiant:surfacegroup"]

    @property
    def zonehvachightemperatureradiants(self):
        """Get list of all `ZoneHvacHighTemperatureRadiant` objects.

        Raises:
            ValueError: if no objects of type `ZoneHvacHighTemperatureRadiant` are present

        """
        return self._data["Zone HVAC Radiative"][
            "zonehvac:hightemperatureradiant"]

    @property
    def zonehvacventilatedslabs(self):
        """Get list of all `ZoneHvacVentilatedSlab` objects.

        Raises:
            ValueError: if no objects of type `ZoneHvacVentilatedSlab` are present

        """
        return self._data["Zone HVAC Radiative"]["zonehvac:ventilatedslab"]

    @property
    def zonehvacventilatedslabslabgroups(self):
        """Get list of all `ZoneHvacVentilatedSlabSlabGroup` objects.

        Raises:
            ValueError: if no objects of type `ZoneHvacVentilatedSlabSlabGroup` are present

        """
        return self._data["Zone HVAC Radiative"][
            "zonehvac:ventilatedslab:slabgroup"]

    @property
    def airterminalsingleductuncontrolleds(self):
        """Get list of all `AirTerminalSingleDuctUncontrolled` objects.

        Raises:
            ValueError: if no objects of type `AirTerminalSingleDuctUncontrolled` are present

        """
        return self._data["Zone HVAC Air Loop Terminal Units"][
            "airterminal:singleduct:uncontrolled"]

    @property
    def airterminalsingleductconstantvolumereheats(self):
        """Get list of all `AirTerminalSingleDuctConstantVolumeReheat` objects.

        Raises:
            ValueError: if no objects of type `AirTerminalSingleDuctConstantVolumeReheat` are present

        """
        return self._data["Zone HVAC Air Loop Terminal Units"][
            "airterminal:singleduct:constantvolume:reheat"]

    @property
    def airterminalsingleductvavnoreheats(self):
        """Get list of all `AirTerminalSingleDuctVavNoReheat` objects.

        Raises:
            ValueError: if no objects of type `AirTerminalSingleDuctVavNoReheat` are present

        """
        return self._data["Zone HVAC Air Loop Terminal Units"][
            "airterminal:singleduct:vav:noreheat"]

    @property
    def airterminalsingleductvavreheats(self):
        """Get list of all `AirTerminalSingleDuctVavReheat` objects.

        Raises:
            ValueError: if no objects of type `AirTerminalSingleDuctVavReheat` are present

        """
        return self._data["Zone HVAC Air Loop Terminal Units"][
            "airterminal:singleduct:vav:reheat"]

    @property
    def airterminalsingleductvavreheatvariablespeedfans(self):
        """Get list of all `AirTerminalSingleDuctVavReheatVariableSpeedFan`
        objects.

        Raises:
            ValueError: if no objects of type `AirTerminalSingleDuctVavReheatVariableSpeedFan` are present

        """
        return self._data["Zone HVAC Air Loop Terminal Units"][
            "airterminal:singleduct:vav:reheat:variablespeedfan"]

    @property
    def airterminalsingleductvavheatandcoolnoreheats(self):
        """Get list of all `AirTerminalSingleDuctVavHeatAndCoolNoReheat`
        objects.

        Raises:
            ValueError: if no objects of type `AirTerminalSingleDuctVavHeatAndCoolNoReheat` are present

        """
        return self._data["Zone HVAC Air Loop Terminal Units"][
            "airterminal:singleduct:vav:heatandcool:noreheat"]

    @property
    def airterminalsingleductvavheatandcoolreheats(self):
        """Get list of all `AirTerminalSingleDuctVavHeatAndCoolReheat` objects.

        Raises:
            ValueError: if no objects of type `AirTerminalSingleDuctVavHeatAndCoolReheat` are present

        """
        return self._data["Zone HVAC Air Loop Terminal Units"][
            "airterminal:singleduct:vav:heatandcool:reheat"]

    @property
    def airterminalsingleductseriespiureheats(self):
        """Get list of all `AirTerminalSingleDuctSeriesPiuReheat` objects.

        Raises:
            ValueError: if no objects of type `AirTerminalSingleDuctSeriesPiuReheat` are present

        """
        return self._data["Zone HVAC Air Loop Terminal Units"][
            "airterminal:singleduct:seriespiu:reheat"]

    @property
    def airterminalsingleductparallelpiureheats(self):
        """Get list of all `AirTerminalSingleDuctParallelPiuReheat` objects.

        Raises:
            ValueError: if no objects of type `AirTerminalSingleDuctParallelPiuReheat` are present

        """
        return self._data["Zone HVAC Air Loop Terminal Units"][
            "airterminal:singleduct:parallelpiu:reheat"]

    @property
    def airterminalsingleductconstantvolumefourpipeinductions(self):
        """Get list of all
        `AirTerminalSingleDuctConstantVolumeFourPipeInduction` objects.

        Raises:
            ValueError: if no objects of type `AirTerminalSingleDuctConstantVolumeFourPipeInduction` are present

        """
        return self._data["Zone HVAC Air Loop Terminal Units"][
            "airterminal:singleduct:constantvolume:fourpipeinduction"]

    @property
    def airterminalsingleductconstantvolumecooledbeams(self):
        """Get list of all `AirTerminalSingleDuctConstantVolumeCooledBeam`
        objects.

        Raises:
            ValueError: if no objects of type `AirTerminalSingleDuctConstantVolumeCooledBeam` are present

        """
        return self._data["Zone HVAC Air Loop Terminal Units"][
            "airterminal:singleduct:constantvolume:cooledbeam"]

    @property
    def airterminalsingleductinletsidemixers(self):
        """Get list of all `AirTerminalSingleDuctInletSideMixer` objects.

        Raises:
            ValueError: if no objects of type `AirTerminalSingleDuctInletSideMixer` are present

        """
        return self._data["Zone HVAC Air Loop Terminal Units"][
            "airterminal:singleduct:inletsidemixer"]

    @property
    def airterminalsingleductsupplysidemixers(self):
        """Get list of all `AirTerminalSingleDuctSupplySideMixer` objects.

        Raises:
            ValueError: if no objects of type `AirTerminalSingleDuctSupplySideMixer` are present

        """
        return self._data["Zone HVAC Air Loop Terminal Units"][
            "airterminal:singleduct:supplysidemixer"]

    @property
    def airterminaldualductconstantvolumes(self):
        """Get list of all `AirTerminalDualDuctConstantVolume` objects.

        Raises:
            ValueError: if no objects of type `AirTerminalDualDuctConstantVolume` are present

        """
        return self._data["Zone HVAC Air Loop Terminal Units"][
            "airterminal:dualduct:constantvolume"]

    @property
    def airterminaldualductvavs(self):
        """Get list of all `AirTerminalDualDuctVav` objects.

        Raises:
            ValueError: if no objects of type `AirTerminalDualDuctVav` are present

        """
        return self._data["Zone HVAC Air Loop Terminal Units"][
            "airterminal:dualduct:vav"]

    @property
    def airterminaldualductvavoutdoorairs(self):
        """Get list of all `AirTerminalDualDuctVavOutdoorAir` objects.

        Raises:
            ValueError: if no objects of type `AirTerminalDualDuctVavOutdoorAir` are present

        """
        return self._data["Zone HVAC Air Loop Terminal Units"][
            "airterminal:dualduct:vav:outdoorair"]

    @property
    def zonehvacairdistributionunits(self):
        """Get list of all `ZoneHvacAirDistributionUnit` objects.

        Raises:
            ValueError: if no objects of type `ZoneHvacAirDistributionUnit` are present

        """
        return self._data["Zone HVAC Air Loop Terminal Units"][
            "zonehvac:airdistributionunit"]

    @property
    def zonehvacequipmentlists(self):
        """Get list of all `ZoneHvacEquipmentList` objects.

        Raises:
            ValueError: if no objects of type `ZoneHvacEquipmentList` are present

        """
        return self._data["Zone HVAC Equipment Connections"][
            "zonehvac:equipmentlist"]

    @property
    def zonehvacequipmentconnectionss(self):
        """Get list of all `ZoneHvacEquipmentConnections` objects.

        Raises:
            ValueError: if no objects of type `ZoneHvacEquipmentConnections` are present

        """
        return self._data["Zone HVAC Equipment Connections"][
            "zonehvac:equipmentconnections"]

    @property
    def fanconstantvolumes(self):
        """Get list of all `FanConstantVolume` objects.

        Raises:
            ValueError: if no objects of type `FanConstantVolume` are present

        """
        return self._data["Fans"]["fan:constantvolume"]

    @property
    def fanvariablevolumes(self):
        """Get list of all `FanVariableVolume` objects.

        Raises:
            ValueError: if no objects of type `FanVariableVolume` are present

        """
        return self._data["Fans"]["fan:variablevolume"]

    @property
    def fanonoffs(self):
        """Get list of all `FanOnOff` objects.

        Raises:
            ValueError: if no objects of type `FanOnOff` are present

        """
        return self._data["Fans"]["fan:onoff"]

    @property
    def fanzoneexhausts(self):
        """Get list of all `FanZoneExhaust` objects.

        Raises:
            ValueError: if no objects of type `FanZoneExhaust` are present

        """
        return self._data["Fans"]["fan:zoneexhaust"]

    @property
    def fanperformancenightventilations(self):
        """Get list of all `FanPerformanceNightVentilation` objects.

        Raises:
            ValueError: if no objects of type `FanPerformanceNightVentilation` are present

        """
        return self._data["Fans"]["fanperformance:nightventilation"]

    @property
    def fancomponentmodels(self):
        """Get list of all `FanComponentModel` objects.

        Raises:
            ValueError: if no objects of type `FanComponentModel` are present

        """
        return self._data["Fans"]["fan:componentmodel"]

    @property
    def coilcoolingwaters(self):
        """Get list of all `CoilCoolingWater` objects.

        Raises:
            ValueError: if no objects of type `CoilCoolingWater` are present

        """
        return self._data["Coils"]["coil:cooling:water"]

    @property
    def coilcoolingwaterdetailedgeometrys(self):
        """Get list of all `CoilCoolingWaterDetailedGeometry` objects.

        Raises:
            ValueError: if no objects of type `CoilCoolingWaterDetailedGeometry` are present

        """
        return self._data["Coils"]["coil:cooling:water:detailedgeometry"]

    @property
    def coilcoolingdxsinglespeeds(self):
        """Get list of all `CoilCoolingDxSingleSpeed` objects.

        Raises:
            ValueError: if no objects of type `CoilCoolingDxSingleSpeed` are present

        """
        return self._data["Coils"]["coil:cooling:dx:singlespeed"]

    @property
    def coilcoolingdxtwospeeds(self):
        """Get list of all `CoilCoolingDxTwoSpeed` objects.

        Raises:
            ValueError: if no objects of type `CoilCoolingDxTwoSpeed` are present

        """
        return self._data["Coils"]["coil:cooling:dx:twospeed"]

    @property
    def coilcoolingdxmultispeeds(self):
        """Get list of all `CoilCoolingDxMultiSpeed` objects.

        Raises:
            ValueError: if no objects of type `CoilCoolingDxMultiSpeed` are present

        """
        return self._data["Coils"]["coil:cooling:dx:multispeed"]

    @property
    def coilcoolingdxvariablespeeds(self):
        """Get list of all `CoilCoolingDxVariableSpeed` objects.

        Raises:
            ValueError: if no objects of type `CoilCoolingDxVariableSpeed` are present

        """
        return self._data["Coils"]["coil:cooling:dx:variablespeed"]

    @property
    def coilcoolingdxtwostagewithhumiditycontrolmodes(self):
        """Get list of all `CoilCoolingDxTwoStageWithHumidityControlMode`
        objects.

        Raises:
            ValueError: if no objects of type `CoilCoolingDxTwoStageWithHumidityControlMode` are present

        """
        return self._data["Coils"][
            "coil:cooling:dx:twostagewithhumiditycontrolmode"]

    @property
    def coilperformancedxcoolings(self):
        """Get list of all `CoilPerformanceDxCooling` objects.

        Raises:
            ValueError: if no objects of type `CoilPerformanceDxCooling` are present

        """
        return self._data["Coils"]["coilperformance:dx:cooling"]

    @property
    def coilcoolingdxvariablerefrigerantflows(self):
        """Get list of all `CoilCoolingDxVariableRefrigerantFlow` objects.

        Raises:
            ValueError: if no objects of type `CoilCoolingDxVariableRefrigerantFlow` are present

        """
        return self._data["Coils"]["coil:cooling:dx:variablerefrigerantflow"]

    @property
    def coilheatingdxvariablerefrigerantflows(self):
        """Get list of all `CoilHeatingDxVariableRefrigerantFlow` objects.

        Raises:
            ValueError: if no objects of type `CoilHeatingDxVariableRefrigerantFlow` are present

        """
        return self._data["Coils"]["coil:heating:dx:variablerefrigerantflow"]

    @property
    def coilheatingwaters(self):
        """Get list of all `CoilHeatingWater` objects.

        Raises:
            ValueError: if no objects of type `CoilHeatingWater` are present

        """
        return self._data["Coils"]["coil:heating:water"]

    @property
    def coilheatingsteams(self):
        """Get list of all `CoilHeatingSteam` objects.

        Raises:
            ValueError: if no objects of type `CoilHeatingSteam` are present

        """
        return self._data["Coils"]["coil:heating:steam"]

    @property
    def coilheatingelectrics(self):
        """Get list of all `CoilHeatingElectric` objects.

        Raises:
            ValueError: if no objects of type `CoilHeatingElectric` are present

        """
        return self._data["Coils"]["coil:heating:electric"]

    @property
    def coilheatingelectricmultistages(self):
        """Get list of all `CoilHeatingElectricMultiStage` objects.

        Raises:
            ValueError: if no objects of type `CoilHeatingElectricMultiStage` are present

        """
        return self._data["Coils"]["coil:heating:electric:multistage"]

    @property
    def coilheatinggass(self):
        """Get list of all `CoilHeatingGas` objects.

        Raises:
            ValueError: if no objects of type `CoilHeatingGas` are present

        """
        return self._data["Coils"]["coil:heating:gas"]

    @property
    def coilheatinggasmultistages(self):
        """Get list of all `CoilHeatingGasMultiStage` objects.

        Raises:
            ValueError: if no objects of type `CoilHeatingGasMultiStage` are present

        """
        return self._data["Coils"]["coil:heating:gas:multistage"]

    @property
    def coilheatingdesuperheaters(self):
        """Get list of all `CoilHeatingDesuperheater` objects.

        Raises:
            ValueError: if no objects of type `CoilHeatingDesuperheater` are present

        """
        return self._data["Coils"]["coil:heating:desuperheater"]

    @property
    def coilheatingdxsinglespeeds(self):
        """Get list of all `CoilHeatingDxSingleSpeed` objects.

        Raises:
            ValueError: if no objects of type `CoilHeatingDxSingleSpeed` are present

        """
        return self._data["Coils"]["coil:heating:dx:singlespeed"]

    @property
    def coilheatingdxmultispeeds(self):
        """Get list of all `CoilHeatingDxMultiSpeed` objects.

        Raises:
            ValueError: if no objects of type `CoilHeatingDxMultiSpeed` are present

        """
        return self._data["Coils"]["coil:heating:dx:multispeed"]

    @property
    def coilheatingdxvariablespeeds(self):
        """Get list of all `CoilHeatingDxVariableSpeed` objects.

        Raises:
            ValueError: if no objects of type `CoilHeatingDxVariableSpeed` are present

        """
        return self._data["Coils"]["coil:heating:dx:variablespeed"]

    @property
    def coilcoolingwatertoairheatpumpparameterestimations(self):
        """Get list of all `CoilCoolingWaterToAirHeatPumpParameterEstimation`
        objects.

        Raises:
            ValueError: if no objects of type `CoilCoolingWaterToAirHeatPumpParameterEstimation` are present

        """
        return self._data["Coils"][
            "coil:cooling:watertoairheatpump:parameterestimation"]

    @property
    def coilheatingwatertoairheatpumpparameterestimations(self):
        """Get list of all `CoilHeatingWaterToAirHeatPumpParameterEstimation`
        objects.

        Raises:
            ValueError: if no objects of type `CoilHeatingWaterToAirHeatPumpParameterEstimation` are present

        """
        return self._data["Coils"][
            "coil:heating:watertoairheatpump:parameterestimation"]

    @property
    def coilcoolingwatertoairheatpumpequationfits(self):
        """Get list of all `CoilCoolingWaterToAirHeatPumpEquationFit` objects.

        Raises:
            ValueError: if no objects of type `CoilCoolingWaterToAirHeatPumpEquationFit` are present

        """
        return self._data["Coils"][
            "coil:cooling:watertoairheatpump:equationfit"]

    @property
    def coilcoolingwatertoairheatpumpvariablespeedequationfits(self):
        """Get list of all
        `CoilCoolingWaterToAirHeatPumpVariableSpeedEquationFit` objects.

        Raises:
            ValueError: if no objects of type `CoilCoolingWaterToAirHeatPumpVariableSpeedEquationFit` are present

        """
        return self._data["Coils"][
            "coil:cooling:watertoairheatpump:variablespeedequationfit"]

    @property
    def coilheatingwatertoairheatpumpequationfits(self):
        """Get list of all `CoilHeatingWaterToAirHeatPumpEquationFit` objects.

        Raises:
            ValueError: if no objects of type `CoilHeatingWaterToAirHeatPumpEquationFit` are present

        """
        return self._data["Coils"][
            "coil:heating:watertoairheatpump:equationfit"]

    @property
    def coilheatingwatertoairheatpumpvariablespeedequationfits(self):
        """Get list of all
        `CoilHeatingWaterToAirHeatPumpVariableSpeedEquationFit` objects.

        Raises:
            ValueError: if no objects of type `CoilHeatingWaterToAirHeatPumpVariableSpeedEquationFit` are present

        """
        return self._data["Coils"][
            "coil:heating:watertoairheatpump:variablespeedequationfit"]

    @property
    def coilwaterheatingairtowaterheatpumps(self):
        """Get list of all `CoilWaterHeatingAirToWaterHeatPump` objects.

        Raises:
            ValueError: if no objects of type `CoilWaterHeatingAirToWaterHeatPump` are present

        """
        return self._data["Coils"]["coil:waterheating:airtowaterheatpump"]

    @property
    def coilwaterheatingdesuperheaters(self):
        """Get list of all `CoilWaterHeatingDesuperheater` objects.

        Raises:
            ValueError: if no objects of type `CoilWaterHeatingDesuperheater` are present

        """
        return self._data["Coils"]["coil:waterheating:desuperheater"]

    @property
    def coilsystemcoolingdxs(self):
        """Get list of all `CoilSystemCoolingDx` objects.

        Raises:
            ValueError: if no objects of type `CoilSystemCoolingDx` are present

        """
        return self._data["Coils"]["coilsystem:cooling:dx"]

    @property
    def coilsystemheatingdxs(self):
        """Get list of all `CoilSystemHeatingDx` objects.

        Raises:
            ValueError: if no objects of type `CoilSystemHeatingDx` are present

        """
        return self._data["Coils"]["coilsystem:heating:dx"]

    @property
    def coilsystemcoolingwaterheatexchangerassisteds(self):
        """Get list of all `CoilSystemCoolingWaterHeatExchangerAssisted`
        objects.

        Raises:
            ValueError: if no objects of type `CoilSystemCoolingWaterHeatExchangerAssisted` are present

        """
        return self._data["Coils"][
            "coilsystem:cooling:water:heatexchangerassisted"]

    @property
    def coilsystemcoolingdxheatexchangerassisteds(self):
        """Get list of all `CoilSystemCoolingDxHeatExchangerAssisted` objects.

        Raises:
            ValueError: if no objects of type `CoilSystemCoolingDxHeatExchangerAssisted` are present

        """
        return self._data["Coils"][
            "coilsystem:cooling:dx:heatexchangerassisted"]

    @property
    def coilcoolingdxsinglespeedthermalstorages(self):
        """Get list of all `CoilCoolingDxSingleSpeedThermalStorage` objects.

        Raises:
            ValueError: if no objects of type `CoilCoolingDxSingleSpeedThermalStorage` are present

        """
        return self._data["Coils"][
            "coil:cooling:dx:singlespeed:thermalstorage"]

    @property
    def evaporativecoolerdirectceldekpads(self):
        """Get list of all `EvaporativeCoolerDirectCelDekPad` objects.

        Raises:
            ValueError: if no objects of type `EvaporativeCoolerDirectCelDekPad` are present

        """
        return self._data["Evaporative Coolers"][
            "evaporativecooler:direct:celdekpad"]

    @property
    def evaporativecoolerindirectceldekpads(self):
        """Get list of all `EvaporativeCoolerIndirectCelDekPad` objects.

        Raises:
            ValueError: if no objects of type `EvaporativeCoolerIndirectCelDekPad` are present

        """
        return self._data["Evaporative Coolers"][
            "evaporativecooler:indirect:celdekpad"]

    @property
    def evaporativecoolerindirectwetcoils(self):
        """Get list of all `EvaporativeCoolerIndirectWetCoil` objects.

        Raises:
            ValueError: if no objects of type `EvaporativeCoolerIndirectWetCoil` are present

        """
        return self._data["Evaporative Coolers"][
            "evaporativecooler:indirect:wetcoil"]

    @property
    def evaporativecoolerindirectresearchspecials(self):
        """Get list of all `EvaporativeCoolerIndirectResearchSpecial` objects.

        Raises:
            ValueError: if no objects of type `EvaporativeCoolerIndirectResearchSpecial` are present

        """
        return self._data["Evaporative Coolers"][
            "evaporativecooler:indirect:researchspecial"]

    @property
    def evaporativecoolerdirectresearchspecials(self):
        """Get list of all `EvaporativeCoolerDirectResearchSpecial` objects.

        Raises:
            ValueError: if no objects of type `EvaporativeCoolerDirectResearchSpecial` are present

        """
        return self._data["Evaporative Coolers"][
            "evaporativecooler:direct:researchspecial"]

    @property
    def humidifiersteamelectrics(self):
        """Get list of all `HumidifierSteamElectric` objects.

        Raises:
            ValueError: if no objects of type `HumidifierSteamElectric` are present

        """
        return self._data["Humidifiers and Dehumidifiers"][
            "humidifier:steam:electric"]

    @property
    def dehumidifierdesiccantnofanss(self):
        """Get list of all `DehumidifierDesiccantNoFans` objects.

        Raises:
            ValueError: if no objects of type `DehumidifierDesiccantNoFans` are present

        """
        return self._data["Humidifiers and Dehumidifiers"][
            "dehumidifier:desiccant:nofans"]

    @property
    def dehumidifierdesiccantsystems(self):
        """Get list of all `DehumidifierDesiccantSystem` objects.

        Raises:
            ValueError: if no objects of type `DehumidifierDesiccantSystem` are present

        """
        return self._data["Humidifiers and Dehumidifiers"][
            "dehumidifier:desiccant:system"]

    @property
    def heatexchangerairtoairflatplates(self):
        """Get list of all `HeatExchangerAirToAirFlatPlate` objects.

        Raises:
            ValueError: if no objects of type `HeatExchangerAirToAirFlatPlate` are present

        """
        return self._data["Heat Recovery"]["heatexchanger:airtoair:flatplate"]

    @property
    def heatexchangerairtoairsensibleandlatents(self):
        """Get list of all `HeatExchangerAirToAirSensibleAndLatent` objects.

        Raises:
            ValueError: if no objects of type `HeatExchangerAirToAirSensibleAndLatent` are present

        """
        return self._data["Heat Recovery"][
            "heatexchanger:airtoair:sensibleandlatent"]

    @property
    def heatexchangerdesiccantbalancedflows(self):
        """Get list of all `HeatExchangerDesiccantBalancedFlow` objects.

        Raises:
            ValueError: if no objects of type `HeatExchangerDesiccantBalancedFlow` are present

        """
        return self._data["Heat Recovery"][
            "heatexchanger:desiccant:balancedflow"]

    @property
    def heatexchangerdesiccantbalancedflowperformancedatatype1s(self):
        """Get list of all
        `HeatExchangerDesiccantBalancedFlowPerformanceDataType1` objects.

        Raises:
            ValueError: if no objects of type `HeatExchangerDesiccantBalancedFlowPerformanceDataType1` are present

        """
        return self._data["Heat Recovery"][
            "heatexchanger:desiccant:balancedflow:performancedatatype1"]

    @property
    def airloophvacunitarysystems(self):
        """Get list of all `AirLoopHvacUnitarySystem` objects.

        Raises:
            ValueError: if no objects of type `AirLoopHvacUnitarySystem` are present

        """
        return self._data["Unitary Equipment"]["airloophvac:unitarysystem"]

    @property
    def unitarysystemperformanceheatpumpmultispeeds(self):
        """Get list of all `UnitarySystemPerformanceHeatPumpMultispeed`
        objects.

        Raises:
            ValueError: if no objects of type `UnitarySystemPerformanceHeatPumpMultispeed` are present

        """
        return self._data["Unitary Equipment"][
            "unitarysystemperformance:heatpump:multispeed"]

    @property
    def airloophvacunitaryfurnaceheatonlys(self):
        """Get list of all `AirLoopHvacUnitaryFurnaceHeatOnly` objects.

        Raises:
            ValueError: if no objects of type `AirLoopHvacUnitaryFurnaceHeatOnly` are present

        """
        return self._data["Unitary Equipment"][
            "airloophvac:unitary:furnace:heatonly"]

    @property
    def airloophvacunitaryfurnaceheatcools(self):
        """Get list of all `AirLoopHvacUnitaryFurnaceHeatCool` objects.

        Raises:
            ValueError: if no objects of type `AirLoopHvacUnitaryFurnaceHeatCool` are present

        """
        return self._data["Unitary Equipment"][
            "airloophvac:unitary:furnace:heatcool"]

    @property
    def airloophvacunitaryheatonlys(self):
        """Get list of all `AirLoopHvacUnitaryHeatOnly` objects.

        Raises:
            ValueError: if no objects of type `AirLoopHvacUnitaryHeatOnly` are present

        """
        return self._data["Unitary Equipment"]["airloophvac:unitaryheatonly"]

    @property
    def airloophvacunitaryheatcools(self):
        """Get list of all `AirLoopHvacUnitaryHeatCool` objects.

        Raises:
            ValueError: if no objects of type `AirLoopHvacUnitaryHeatCool` are present

        """
        return self._data["Unitary Equipment"]["airloophvac:unitaryheatcool"]

    @property
    def airloophvacunitaryheatpumpairtoairs(self):
        """Get list of all `AirLoopHvacUnitaryHeatPumpAirToAir` objects.

        Raises:
            ValueError: if no objects of type `AirLoopHvacUnitaryHeatPumpAirToAir` are present

        """
        return self._data["Unitary Equipment"][
            "airloophvac:unitaryheatpump:airtoair"]

    @property
    def airloophvacunitaryheatpumpwatertoairs(self):
        """Get list of all `AirLoopHvacUnitaryHeatPumpWaterToAir` objects.

        Raises:
            ValueError: if no objects of type `AirLoopHvacUnitaryHeatPumpWaterToAir` are present

        """
        return self._data["Unitary Equipment"][
            "airloophvac:unitaryheatpump:watertoair"]

    @property
    def airloophvacunitaryheatcoolvavchangeoverbypasss(self):
        """Get list of all `AirLoopHvacUnitaryHeatCoolVavchangeoverBypass`
        objects.

        Raises:
            ValueError: if no objects of type `AirLoopHvacUnitaryHeatCoolVavchangeoverBypass` are present

        """
        return self._data["Unitary Equipment"][
            "airloophvac:unitaryheatcool:vavchangeoverbypass"]

    @property
    def airloophvacunitaryheatpumpairtoairmultispeeds(self):
        """Get list of all `AirLoopHvacUnitaryHeatPumpAirToAirMultiSpeed`
        objects.

        Raises:
            ValueError: if no objects of type `AirLoopHvacUnitaryHeatPumpAirToAirMultiSpeed` are present

        """
        return self._data["Unitary Equipment"][
            "airloophvac:unitaryheatpump:airtoair:multispeed"]

    @property
    def airconditionervariablerefrigerantflows(self):
        """Get list of all `AirConditionerVariableRefrigerantFlow` objects.

        Raises:
            ValueError: if no objects of type `AirConditionerVariableRefrigerantFlow` are present

        """
        return self._data["Variable Refrigerant Flow Equipment"][
            "airconditioner:variablerefrigerantflow"]

    @property
    def zoneterminalunitlists(self):
        """Get list of all `ZoneTerminalUnitList` objects.

        Raises:
            ValueError: if no objects of type `ZoneTerminalUnitList` are present

        """
        return self._data["Variable Refrigerant Flow Equipment"][
            "zoneterminalunitlist"]

    @property
    def controllerwatercoils(self):
        """Get list of all `ControllerWaterCoil` objects.

        Raises:
            ValueError: if no objects of type `ControllerWaterCoil` are present

        """
        return self._data["Controllers"]["controller:watercoil"]

    @property
    def controlleroutdoorairs(self):
        """Get list of all `ControllerOutdoorAir` objects.

        Raises:
            ValueError: if no objects of type `ControllerOutdoorAir` are present

        """
        return self._data["Controllers"]["controller:outdoorair"]

    @property
    def controllermechanicalventilations(self):
        """Get list of all `ControllerMechanicalVentilation` objects.

        Raises:
            ValueError: if no objects of type `ControllerMechanicalVentilation` are present

        """
        return self._data["Controllers"]["controller:mechanicalventilation"]

    @property
    def airloophvaccontrollerlists(self):
        """Get list of all `AirLoopHvacControllerList` objects.

        Raises:
            ValueError: if no objects of type `AirLoopHvacControllerList` are present

        """
        return self._data["Controllers"]["airloophvac:controllerlist"]

    @property
    def airloophvacs(self):
        """Get list of all `AirLoopHvac` objects.

        Raises:
            ValueError: if no objects of type `AirLoopHvac` are present

        """
        return self._data["Air Distribution"]["airloophvac"]

    @property
    def airloophvacoutdoorairsystemequipmentlists(self):
        """Get list of all `AirLoopHvacOutdoorAirSystemEquipmentList` objects.

        Raises:
            ValueError: if no objects of type `AirLoopHvacOutdoorAirSystemEquipmentList` are present

        """
        return self._data["Air Distribution"][
            "airloophvac:outdoorairsystem:equipmentlist"]

    @property
    def airloophvacoutdoorairsystems(self):
        """Get list of all `AirLoopHvacOutdoorAirSystem` objects.

        Raises:
            ValueError: if no objects of type `AirLoopHvacOutdoorAirSystem` are present

        """
        return self._data["Air Distribution"]["airloophvac:outdoorairsystem"]

    @property
    def outdoorairmixers(self):
        """Get list of all `OutdoorAirMixer` objects.

        Raises:
            ValueError: if no objects of type `OutdoorAirMixer` are present

        """
        return self._data["Air Distribution"]["outdoorair:mixer"]

    @property
    def airloophvaczonesplitters(self):
        """Get list of all `AirLoopHvacZoneSplitter` objects.

        Raises:
            ValueError: if no objects of type `AirLoopHvacZoneSplitter` are present

        """
        return self._data["Air Distribution"]["airloophvac:zonesplitter"]

    @property
    def airloophvacsupplyplenums(self):
        """Get list of all `AirLoopHvacSupplyPlenum` objects.

        Raises:
            ValueError: if no objects of type `AirLoopHvacSupplyPlenum` are present

        """
        return self._data["Air Distribution"]["airloophvac:supplyplenum"]

    @property
    def airloophvacsupplypaths(self):
        """Get list of all `AirLoopHvacSupplyPath` objects.

        Raises:
            ValueError: if no objects of type `AirLoopHvacSupplyPath` are present

        """
        return self._data["Air Distribution"]["airloophvac:supplypath"]

    @property
    def airloophvaczonemixers(self):
        """Get list of all `AirLoopHvacZoneMixer` objects.

        Raises:
            ValueError: if no objects of type `AirLoopHvacZoneMixer` are present

        """
        return self._data["Air Distribution"]["airloophvac:zonemixer"]

    @property
    def airloophvacreturnplenums(self):
        """Get list of all `AirLoopHvacReturnPlenum` objects.

        Raises:
            ValueError: if no objects of type `AirLoopHvacReturnPlenum` are present

        """
        return self._data["Air Distribution"]["airloophvac:returnplenum"]

    @property
    def airloophvacreturnpaths(self):
        """Get list of all `AirLoopHvacReturnPath` objects.

        Raises:
            ValueError: if no objects of type `AirLoopHvacReturnPath` are present

        """
        return self._data["Air Distribution"]["airloophvac:returnpath"]

    @property
    def branchs(self):
        """Get list of all `Branch` objects.

        Raises:
            ValueError: if no objects of type `Branch` are present

        """
        return self._data["Node"]["branch"]

    @property
    def branchlists(self):
        """Get list of all `BranchList` objects.

        Raises:
            ValueError: if no objects of type `BranchList` are present

        """
        return self._data["Pumps"]["branchlist"]

    @property
    def connectorsplitters(self):
        """Get list of all `ConnectorSplitter` objects.

        Raises:
            ValueError: if no objects of type `ConnectorSplitter` are present

        """
        return self._data["Node"]["connector:splitter"]

    @property
    def connectormixers(self):
        """Get list of all `ConnectorMixer` objects.

        Raises:
            ValueError: if no objects of type `ConnectorMixer` are present

        """
        return self._data["Node"]["connector:mixer"]

    @property
    def connectorlists(self):
        """Get list of all `ConnectorList` objects.

        Raises:
            ValueError: if no objects of type `ConnectorList` are present

        """
        return self._data["Node"]["connectorlist"]

    @property
    def nodelists(self):
        """Get list of all `NodeList` objects.

        Raises:
            ValueError: if no objects of type `NodeList` are present

        """
        return self._data["Node"]["nodelist"]

    @property
    def outdoorairnodes(self):
        """Get list of all `OutdoorAirNode` objects.

        Raises:
            ValueError: if no objects of type `OutdoorAirNode` are present

        """
        return self._data["Node"]["outdoorair:node"]

    @property
    def outdoorairnodelists(self):
        """Get list of all `OutdoorAirNodeList` objects.

        Raises:
            ValueError: if no objects of type `OutdoorAirNodeList` are present

        """
        return self._data["Node"]["outdoorair:nodelist"]

    @property
    def pipeadiabatics(self):
        """Get list of all `PipeAdiabatic` objects.

        Raises:
            ValueError: if no objects of type `PipeAdiabatic` are present

        """
        return self._data["Node"]["pipe:adiabatic"]

    @property
    def pipeadiabaticsteams(self):
        """Get list of all `PipeAdiabaticSteam` objects.

        Raises:
            ValueError: if no objects of type `PipeAdiabaticSteam` are present

        """
        return self._data["Node"]["pipe:adiabatic:steam"]

    @property
    def pipeindoors(self):
        """Get list of all `PipeIndoor` objects.

        Raises:
            ValueError: if no objects of type `PipeIndoor` are present

        """
        return self._data["Node"]["pipe:indoor"]

    @property
    def pipeoutdoors(self):
        """Get list of all `PipeOutdoor` objects.

        Raises:
            ValueError: if no objects of type `PipeOutdoor` are present

        """
        return self._data["Node"]["pipe:outdoor"]

    @property
    def pipeundergrounds(self):
        """Get list of all `PipeUnderground` objects.

        Raises:
            ValueError: if no objects of type `PipeUnderground` are present

        """
        return self._data["Node"]["pipe:underground"]

    @property
    def pipingsystemundergrounddomains(self):
        """Get list of all `PipingSystemUndergroundDomain` objects.

        Raises:
            ValueError: if no objects of type `PipingSystemUndergroundDomain` are present

        """
        return self._data["Node"]["pipingsystem:underground:domain"]

    @property
    def pipingsystemundergroundpipecircuits(self):
        """Get list of all `PipingSystemUndergroundPipeCircuit` objects.

        Raises:
            ValueError: if no objects of type `PipingSystemUndergroundPipeCircuit` are present

        """
        return self._data["Node"]["pipingsystem:underground:pipecircuit"]

    @property
    def pipingsystemundergroundpipesegments(self):
        """Get list of all `PipingSystemUndergroundPipeSegment` objects.

        Raises:
            ValueError: if no objects of type `PipingSystemUndergroundPipeSegment` are present

        """
        return self._data["Node"]["pipingsystem:underground:pipesegment"]

    @property
    def ducts(self):
        """Get list of all `Duct` objects.

        Raises:
            ValueError: if no objects of type `Duct` are present

        """
        return self._data["Node"]["duct"]

    @property
    def pumpvariablespeeds(self):
        """Get list of all `PumpVariableSpeed` objects.

        Raises:
            ValueError: if no objects of type `PumpVariableSpeed` are present

        """
        return self._data["Pumps"]["pump:variablespeed"]

    @property
    def pumpconstantspeeds(self):
        """Get list of all `PumpConstantSpeed` objects.

        Raises:
            ValueError: if no objects of type `PumpConstantSpeed` are present

        """
        return self._data["Pumps"]["pump:constantspeed"]

    @property
    def pumpvariablespeedcondensates(self):
        """Get list of all `PumpVariableSpeedCondensate` objects.

        Raises:
            ValueError: if no objects of type `PumpVariableSpeedCondensate` are present

        """
        return self._data["Pumps"]["pump:variablespeed:condensate"]

    @property
    def headeredpumpsconstantspeeds(self):
        """Get list of all `HeaderedPumpsConstantSpeed` objects.

        Raises:
            ValueError: if no objects of type `HeaderedPumpsConstantSpeed` are present

        """
        return self._data["Pumps"]["headeredpumps:constantspeed"]

    @property
    def headeredpumpsvariablespeeds(self):
        """Get list of all `HeaderedPumpsVariableSpeed` objects.

        Raises:
            ValueError: if no objects of type `HeaderedPumpsVariableSpeed` are present

        """
        return self._data["Pumps"]["headeredpumps:variablespeed"]

    @property
    def temperingvalves(self):
        """Get list of all `TemperingValve` objects.

        Raises:
            ValueError: if no objects of type `TemperingValve` are present

        """
        return self._data["Plant"]["temperingvalve"]

    @property
    def loadprofileplants(self):
        """Get list of all `LoadProfilePlant` objects.

        Raises:
            ValueError: if no objects of type `LoadProfilePlant` are present

        """
        return self._data["Non"]["loadprofile:plant"]

    @property
    def solarcollectorperformanceflatplates(self):
        """Get list of all `SolarCollectorPerformanceFlatPlate` objects.

        Raises:
            ValueError: if no objects of type `SolarCollectorPerformanceFlatPlate` are present

        """
        return self._data["Solar Collectors"][
            "solarcollectorperformance:flatplate"]

    @property
    def solarcollectorflatplatewaters(self):
        """Get list of all `SolarCollectorFlatPlateWater` objects.

        Raises:
            ValueError: if no objects of type `SolarCollectorFlatPlateWater` are present

        """
        return self._data["Solar Collectors"]["solarcollector:flatplate:water"]

    @property
    def solarcollectorflatplatephotovoltaicthermals(self):
        """Get list of all `SolarCollectorFlatPlatePhotovoltaicThermal`
        objects.

        Raises:
            ValueError: if no objects of type `SolarCollectorFlatPlatePhotovoltaicThermal` are present

        """
        return self._data["Solar Collectors"][
            "solarcollector:flatplate:photovoltaicthermal"]

    @property
    def solarcollectorperformancephotovoltaicthermalsimples(self):
        """Get list of all `SolarCollectorPerformancePhotovoltaicThermalSimple`
        objects.

        Raises:
            ValueError: if no objects of type `SolarCollectorPerformancePhotovoltaicThermalSimple` are present

        """
        return self._data["Solar Collectors"][
            "solarcollectorperformance:photovoltaicthermal:simple"]

    @property
    def solarcollectorintegralcollectorstorages(self):
        """Get list of all `SolarCollectorIntegralCollectorStorage` objects.

        Raises:
            ValueError: if no objects of type `SolarCollectorIntegralCollectorStorage` are present

        """
        return self._data["Solar Collectors"][
            "solarcollector:integralcollectorstorage"]

    @property
    def solarcollectorperformanceintegralcollectorstorages(self):
        """Get list of all `SolarCollectorPerformanceIntegralCollectorStorage`
        objects.

        Raises:
            ValueError: if no objects of type `SolarCollectorPerformanceIntegralCollectorStorage` are present

        """
        return self._data["Solar Collectors"][
            "solarcollectorperformance:integralcollectorstorage"]

    @property
    def solarcollectorunglazedtranspireds(self):
        """Get list of all `SolarCollectorUnglazedTranspired` objects.

        Raises:
            ValueError: if no objects of type `SolarCollectorUnglazedTranspired` are present

        """
        return self._data["Solar Collectors"][
            "solarcollector:unglazedtranspired"]

    @property
    def solarcollectorunglazedtranspiredmultisystems(self):
        """Get list of all `SolarCollectorUnglazedTranspiredMultisystem`
        objects.

        Raises:
            ValueError: if no objects of type `SolarCollectorUnglazedTranspiredMultisystem` are present

        """
        return self._data["Solar Collectors"][
            "solarcollector:unglazedtranspired:multisystem"]

    @property
    def boilerhotwaters(self):
        """Get list of all `BoilerHotWater` objects.

        Raises:
            ValueError: if no objects of type `BoilerHotWater` are present

        """
        return self._data["Plant Heating and Cooling Equipment"][
            "boiler:hotwater"]

    @property
    def boilersteams(self):
        """Get list of all `BoilerSteam` objects.

        Raises:
            ValueError: if no objects of type `BoilerSteam` are present

        """
        return self._data["Plant Heating and Cooling Equipment"][
            "boiler:steam"]

    @property
    def chillerelectriceirs(self):
        """Get list of all `ChillerElectricEir` objects.

        Raises:
            ValueError: if no objects of type `ChillerElectricEir` are present

        """
        return self._data["Plant Heating and Cooling Equipment"][
            "chiller:electric:eir"]

    @property
    def chillerelectricreformulatedeirs(self):
        """Get list of all `ChillerElectricReformulatedEir` objects.

        Raises:
            ValueError: if no objects of type `ChillerElectricReformulatedEir` are present

        """
        return self._data["Plant Heating and Cooling Equipment"][
            "chiller:electric:reformulatedeir"]

    @property
    def chillerelectrics(self):
        """Get list of all `ChillerElectric` objects.

        Raises:
            ValueError: if no objects of type `ChillerElectric` are present

        """
        return self._data["Plant Heating and Cooling Equipment"][
            "chiller:electric"]

    @property
    def chillerabsorptionindirects(self):
        """Get list of all `ChillerAbsorptionIndirect` objects.

        Raises:
            ValueError: if no objects of type `ChillerAbsorptionIndirect` are present

        """
        return self._data["Plant Heating and Cooling Equipment"][
            "chiller:absorption:indirect"]

    @property
    def chillerabsorptions(self):
        """Get list of all `ChillerAbsorption` objects.

        Raises:
            ValueError: if no objects of type `ChillerAbsorption` are present

        """
        return self._data["Plant Heating and Cooling Equipment"][
            "chiller:absorption"]

    @property
    def chillerconstantcops(self):
        """Get list of all `ChillerConstantCop` objects.

        Raises:
            ValueError: if no objects of type `ChillerConstantCop` are present

        """
        return self._data["Plant Heating and Cooling Equipment"][
            "chiller:constantcop"]

    @property
    def chillerenginedrivens(self):
        """Get list of all `ChillerEngineDriven` objects.

        Raises:
            ValueError: if no objects of type `ChillerEngineDriven` are present

        """
        return self._data["Plant Heating and Cooling Equipment"][
            "chiller:enginedriven"]

    @property
    def chillercombustionturbines(self):
        """Get list of all `ChillerCombustionTurbine` objects.

        Raises:
            ValueError: if no objects of type `ChillerCombustionTurbine` are present

        """
        return self._data["Plant Heating and Cooling Equipment"][
            "chiller:combustionturbine"]

    @property
    def chillerheaterabsorptiondirectfireds(self):
        """Get list of all `ChillerHeaterAbsorptionDirectFired` objects.

        Raises:
            ValueError: if no objects of type `ChillerHeaterAbsorptionDirectFired` are present

        """
        return self._data["Plant Heating and Cooling Equipment"][
            "chillerheater:absorption:directfired"]

    @property
    def chillerheaterabsorptiondoubleeffects(self):
        """Get list of all `ChillerHeaterAbsorptionDoubleEffect` objects.

        Raises:
            ValueError: if no objects of type `ChillerHeaterAbsorptionDoubleEffect` are present

        """
        return self._data["Plant Heating and Cooling Equipment"][
            "chillerheater:absorption:doubleeffect"]

    @property
    def heatpumpwatertowaterequationfitheatings(self):
        """Get list of all `HeatPumpWaterToWaterEquationFitHeating` objects.

        Raises:
            ValueError: if no objects of type `HeatPumpWaterToWaterEquationFitHeating` are present

        """
        return self._data["Plant Heating and Cooling Equipment"][
            "heatpump:watertowater:equationfit:heating"]

    @property
    def heatpumpwatertowaterequationfitcoolings(self):
        """Get list of all `HeatPumpWaterToWaterEquationFitCooling` objects.

        Raises:
            ValueError: if no objects of type `HeatPumpWaterToWaterEquationFitCooling` are present

        """
        return self._data["Plant Heating and Cooling Equipment"][
            "heatpump:watertowater:equationfit:cooling"]

    @property
    def heatpumpwatertowaterparameterestimationcoolings(self):
        """Get list of all `HeatPumpWaterToWaterParameterEstimationCooling`
        objects.

        Raises:
            ValueError: if no objects of type `HeatPumpWaterToWaterParameterEstimationCooling` are present

        """
        return self._data["Plant Heating and Cooling Equipment"][
            "heatpump:watertowater:parameterestimation:cooling"]

    @property
    def heatpumpwatertowaterparameterestimationheatings(self):
        """Get list of all `HeatPumpWaterToWaterParameterEstimationHeating`
        objects.

        Raises:
            ValueError: if no objects of type `HeatPumpWaterToWaterParameterEstimationHeating` are present

        """
        return self._data["Plant Heating and Cooling Equipment"][
            "heatpump:watertowater:parameterestimation:heating"]

    @property
    def districtcoolings(self):
        """Get list of all `DistrictCooling` objects.

        Raises:
            ValueError: if no objects of type `DistrictCooling` are present

        """
        return self._data["Plant Heating and Cooling Equipment"][
            "districtcooling"]

    @property
    def districtheatings(self):
        """Get list of all `DistrictHeating` objects.

        Raises:
            ValueError: if no objects of type `DistrictHeating` are present

        """
        return self._data["Plant Heating and Cooling Equipment"][
            "districtheating"]

    @property
    def plantcomponenttemperaturesources(self):
        """Get list of all `PlantComponentTemperatureSource` objects.

        Raises:
            ValueError: if no objects of type `PlantComponentTemperatureSource` are present

        """
        return self._data["Plant Heating and Cooling Equipment"][
            "plantcomponent:temperaturesource"]

    @property
    def centralheatpumpsystems(self):
        """Get list of all `CentralHeatPumpSystem` objects.

        Raises:
            ValueError: if no objects of type `CentralHeatPumpSystem` are present

        """
        return self._data["Plant Heating and Cooling Equipment"][
            "centralheatpumpsystem"]

    @property
    def chillerheaterperformanceelectriceirs(self):
        """Get list of all `ChillerHeaterPerformanceElectricEir` objects.

        Raises:
            ValueError: if no objects of type `ChillerHeaterPerformanceElectricEir` are present

        """
        return self._data["Plant Heating and Cooling Equipment"][
            "chillerheaterperformance:electric:eir"]

    @property
    def coolingtowersinglespeeds(self):
        """Get list of all `CoolingTowerSingleSpeed` objects.

        Raises:
            ValueError: if no objects of type `CoolingTowerSingleSpeed` are present

        """
        return self._data["Condenser Equipment and Heat Exchangers"][
            "coolingtower:singlespeed"]

    @property
    def coolingtowertwospeeds(self):
        """Get list of all `CoolingTowerTwoSpeed` objects.

        Raises:
            ValueError: if no objects of type `CoolingTowerTwoSpeed` are present

        """
        return self._data["Condenser Equipment and Heat Exchangers"][
            "coolingtower:twospeed"]

    @property
    def coolingtowervariablespeedmerkels(self):
        """Get list of all `CoolingTowerVariableSpeedMerkel` objects.

        Raises:
            ValueError: if no objects of type `CoolingTowerVariableSpeedMerkel` are present

        """
        return self._data["Condenser Equipment and Heat Exchangers"][
            "coolingtower:variablespeed:merkel"]

    @property
    def coolingtowervariablespeeds(self):
        """Get list of all `CoolingTowerVariableSpeed` objects.

        Raises:
            ValueError: if no objects of type `CoolingTowerVariableSpeed` are present

        """
        return self._data["Condenser Equipment and Heat Exchangers"][
            "coolingtower:variablespeed"]

    @property
    def coolingtowerperformancecooltoolss(self):
        """Get list of all `CoolingTowerPerformanceCoolTools` objects.

        Raises:
            ValueError: if no objects of type `CoolingTowerPerformanceCoolTools` are present

        """
        return self._data["Condenser Equipment and Heat Exchangers"][
            "coolingtowerperformance:cooltools"]

    @property
    def coolingtowerperformanceyorkcalcs(self):
        """Get list of all `CoolingTowerPerformanceYorkCalc` objects.

        Raises:
            ValueError: if no objects of type `CoolingTowerPerformanceYorkCalc` are present

        """
        return self._data["Condenser Equipment and Heat Exchangers"][
            "coolingtowerperformance:yorkcalc"]

    @property
    def evaporativefluidcoolersinglespeeds(self):
        """Get list of all `EvaporativeFluidCoolerSingleSpeed` objects.

        Raises:
            ValueError: if no objects of type `EvaporativeFluidCoolerSingleSpeed` are present

        """
        return self._data["Condenser Equipment and Heat Exchangers"][
            "evaporativefluidcooler:singlespeed"]

    @property
    def evaporativefluidcoolertwospeeds(self):
        """Get list of all `EvaporativeFluidCoolerTwoSpeed` objects.

        Raises:
            ValueError: if no objects of type `EvaporativeFluidCoolerTwoSpeed` are present

        """
        return self._data["Condenser Equipment and Heat Exchangers"][
            "evaporativefluidcooler:twospeed"]

    @property
    def fluidcoolersinglespeeds(self):
        """Get list of all `FluidCoolerSingleSpeed` objects.

        Raises:
            ValueError: if no objects of type `FluidCoolerSingleSpeed` are present

        """
        return self._data["Condenser Equipment and Heat Exchangers"][
            "fluidcooler:singlespeed"]

    @property
    def fluidcoolertwospeeds(self):
        """Get list of all `FluidCoolerTwoSpeed` objects.

        Raises:
            ValueError: if no objects of type `FluidCoolerTwoSpeed` are present

        """
        return self._data["Condenser Equipment and Heat Exchangers"][
            "fluidcooler:twospeed"]

    @property
    def groundheatexchangerverticals(self):
        """Get list of all `GroundHeatExchangerVertical` objects.

        Raises:
            ValueError: if no objects of type `GroundHeatExchangerVertical` are present

        """
        return self._data["Condenser Equipment and Heat Exchangers"][
            "groundheatexchanger:vertical"]

    @property
    def groundheatexchangerponds(self):
        """Get list of all `GroundHeatExchangerPond` objects.

        Raises:
            ValueError: if no objects of type `GroundHeatExchangerPond` are present

        """
        return self._data["Condenser Equipment and Heat Exchangers"][
            "groundheatexchanger:pond"]

    @property
    def groundheatexchangersurfaces(self):
        """Get list of all `GroundHeatExchangerSurface` objects.

        Raises:
            ValueError: if no objects of type `GroundHeatExchangerSurface` are present

        """
        return self._data["Condenser Equipment and Heat Exchangers"][
            "groundheatexchanger:surface"]

    @property
    def groundheatexchangerhorizontaltrenchs(self):
        """Get list of all `GroundHeatExchangerHorizontalTrench` objects.

        Raises:
            ValueError: if no objects of type `GroundHeatExchangerHorizontalTrench` are present

        """
        return self._data["Condenser Equipment and Heat Exchangers"][
            "groundheatexchanger:horizontaltrench"]

    @property
    def heatexchangerfluidtofluids(self):
        """Get list of all `HeatExchangerFluidToFluid` objects.

        Raises:
            ValueError: if no objects of type `HeatExchangerFluidToFluid` are present

        """
        return self._data["Condenser Equipment and Heat Exchangers"][
            "heatexchanger:fluidtofluid"]

    @property
    def waterheatermixeds(self):
        """Get list of all `WaterHeaterMixed` objects.

        Raises:
            ValueError: if no objects of type `WaterHeaterMixed` are present

        """
        return self._data["Water Heaters and Thermal Storage"][
            "waterheater:mixed"]

    @property
    def waterheaterstratifieds(self):
        """Get list of all `WaterHeaterStratified` objects.

        Raises:
            ValueError: if no objects of type `WaterHeaterStratified` are present

        """
        return self._data["Water Heaters and Thermal Storage"][
            "waterheater:stratified"]

    @property
    def waterheatersizings(self):
        """Get list of all `WaterHeaterSizing` objects.

        Raises:
            ValueError: if no objects of type `WaterHeaterSizing` are present

        """
        return self._data["Water Heaters and Thermal Storage"][
            "waterheater:sizing"]

    @property
    def waterheaterheatpumps(self):
        """Get list of all `WaterHeaterHeatPump` objects.

        Raises:
            ValueError: if no objects of type `WaterHeaterHeatPump` are present

        """
        return self._data["Water Heaters and Thermal Storage"][
            "waterheater:heatpump"]

    @property
    def thermalstorageicesimples(self):
        """Get list of all `ThermalStorageIceSimple` objects.

        Raises:
            ValueError: if no objects of type `ThermalStorageIceSimple` are present

        """
        return self._data["Water Heaters and Thermal Storage"][
            "thermalstorage:ice:simple"]

    @property
    def thermalstorageicedetaileds(self):
        """Get list of all `ThermalStorageIceDetailed` objects.

        Raises:
            ValueError: if no objects of type `ThermalStorageIceDetailed` are present

        """
        return self._data["Water Heaters and Thermal Storage"][
            "thermalstorage:ice:detailed"]

    @property
    def thermalstoragechilledwatermixeds(self):
        """Get list of all `ThermalStorageChilledWaterMixed` objects.

        Raises:
            ValueError: if no objects of type `ThermalStorageChilledWaterMixed` are present

        """
        return self._data["Water Heaters and Thermal Storage"][
            "thermalstorage:chilledwater:mixed"]

    @property
    def thermalstoragechilledwaterstratifieds(self):
        """Get list of all `ThermalStorageChilledWaterStratified` objects.

        Raises:
            ValueError: if no objects of type `ThermalStorageChilledWaterStratified` are present

        """
        return self._data["Water Heaters and Thermal Storage"][
            "thermalstorage:chilledwater:stratified"]

    @property
    def plantloops(self):
        """Get list of all `PlantLoop` objects.

        Raises:
            ValueError: if no objects of type `PlantLoop` are present

        """
        return self._data["Plant"]["plantloop"]

    @property
    def condenserloops(self):
        """Get list of all `CondenserLoop` objects.

        Raises:
            ValueError: if no objects of type `CondenserLoop` are present

        """
        return self._data["Plant"]["condenserloop"]

    @property
    def plantequipmentlists(self):
        """Get list of all `PlantEquipmentList` objects.

        Raises:
            ValueError: if no objects of type `PlantEquipmentList` are present

        """
        return self._data["Plant"]["plantequipmentlist"]

    @property
    def condenserequipmentlists(self):
        """Get list of all `CondenserEquipmentList` objects.

        Raises:
            ValueError: if no objects of type `CondenserEquipmentList` are present

        """
        return self._data["Plant"]["condenserequipmentlist"]

    @property
    def plantequipmentoperationuncontrolleds(self):
        """Get list of all `PlantEquipmentOperationUncontrolled` objects.

        Raises:
            ValueError: if no objects of type `PlantEquipmentOperationUncontrolled` are present

        """
        return self._data["Plant"]["plantequipmentoperation:uncontrolled"]

    @property
    def plantequipmentoperationcoolingloads(self):
        """Get list of all `PlantEquipmentOperationCoolingLoad` objects.

        Raises:
            ValueError: if no objects of type `PlantEquipmentOperationCoolingLoad` are present

        """
        return self._data["Plant"]["plantequipmentoperation:coolingload"]

    @property
    def plantequipmentoperationheatingloads(self):
        """Get list of all `PlantEquipmentOperationHeatingLoad` objects.

        Raises:
            ValueError: if no objects of type `PlantEquipmentOperationHeatingLoad` are present

        """
        return self._data["Plant"]["plantequipmentoperation:heatingload"]

    @property
    def plantequipmentoperationoutdoordrybulbs(self):
        """Get list of all `PlantEquipmentOperationOutdoorDryBulb` objects.

        Raises:
            ValueError: if no objects of type `PlantEquipmentOperationOutdoorDryBulb` are present

        """
        return self._data["Plant"]["plantequipmentoperation:outdoordrybulb"]

    @property
    def plantequipmentoperationoutdoorwetbulbs(self):
        """Get list of all `PlantEquipmentOperationOutdoorWetBulb` objects.

        Raises:
            ValueError: if no objects of type `PlantEquipmentOperationOutdoorWetBulb` are present

        """
        return self._data["Plant"]["plantequipmentoperation:outdoorwetbulb"]

    @property
    def plantequipmentoperationoutdoorrelativehumiditys(self):
        """Get list of all `PlantEquipmentOperationOutdoorRelativeHumidity`
        objects.

        Raises:
            ValueError: if no objects of type `PlantEquipmentOperationOutdoorRelativeHumidity` are present

        """
        return self._data["Plant"][
            "plantequipmentoperation:outdoorrelativehumidity"]

    @property
    def plantequipmentoperationoutdoordewpoints(self):
        """Get list of all `PlantEquipmentOperationOutdoorDewpoint` objects.

        Raises:
            ValueError: if no objects of type `PlantEquipmentOperationOutdoorDewpoint` are present

        """
        return self._data["Plant"]["plantequipmentoperation:outdoordewpoint"]

    @property
    def plantequipmentoperationcomponentsetpoints(self):
        """Get list of all `PlantEquipmentOperationComponentSetpoint` objects.

        Raises:
            ValueError: if no objects of type `PlantEquipmentOperationComponentSetpoint` are present

        """
        return self._data["Plant"]["plantequipmentoperation:componentsetpoint"]

    @property
    def plantequipmentoperationoutdoordrybulbdifferences(self):
        """Get list of all `PlantEquipmentOperationOutdoorDryBulbDifference`
        objects.

        Raises:
            ValueError: if no objects of type `PlantEquipmentOperationOutdoorDryBulbDifference` are present

        """
        return self._data["Plant"][
            "plantequipmentoperation:outdoordrybulbdifference"]

    @property
    def plantequipmentoperationoutdoorwetbulbdifferences(self):
        """Get list of all `PlantEquipmentOperationOutdoorWetBulbDifference`
        objects.

        Raises:
            ValueError: if no objects of type `PlantEquipmentOperationOutdoorWetBulbDifference` are present

        """
        return self._data["Plant"][
            "plantequipmentoperation:outdoorwetbulbdifference"]

    @property
    def plantequipmentoperationoutdoordewpointdifferences(self):
        """Get list of all `PlantEquipmentOperationOutdoorDewpointDifference`
        objects.

        Raises:
            ValueError: if no objects of type `PlantEquipmentOperationOutdoorDewpointDifference` are present

        """
        return self._data["Plant"][
            "plantequipmentoperation:outdoordewpointdifference"]

    @property
    def plantequipmentoperationschemess(self):
        """Get list of all `PlantEquipmentOperationSchemes` objects.

        Raises:
            ValueError: if no objects of type `PlantEquipmentOperationSchemes` are present

        """
        return self._data["Plant"]["plantequipmentoperationschemes"]

    @property
    def condenserequipmentoperationschemess(self):
        """Get list of all `CondenserEquipmentOperationSchemes` objects.

        Raises:
            ValueError: if no objects of type `CondenserEquipmentOperationSchemes` are present

        """
        return self._data["Plant"]["condenserequipmentoperationschemes"]

    @property
    def energymanagementsystemsensors(self):
        """Get list of all `EnergyManagementSystemSensor` objects.

        Raises:
            ValueError: if no objects of type `EnergyManagementSystemSensor` are present

        """
        return self._data["Energy Management System"][
            "energymanagementsystem:sensor"]

    @property
    def energymanagementsystemactuators(self):
        """Get list of all `EnergyManagementSystemActuator` objects.

        Raises:
            ValueError: if no objects of type `EnergyManagementSystemActuator` are present

        """
        return self._data["Energy Management System"][
            "energymanagementsystem:actuator"]

    @property
    def energymanagementsystemprogramcallingmanagers(self):
        """Get list of all `EnergyManagementSystemProgramCallingManager`
        objects.

        Raises:
            ValueError: if no objects of type `EnergyManagementSystemProgramCallingManager` are present

        """
        return self._data["Energy Management System"][
            "energymanagementsystem:programcallingmanager"]

    @property
    def energymanagementsystemprograms(self):
        """Get list of all `EnergyManagementSystemProgram` objects.

        Raises:
            ValueError: if no objects of type `EnergyManagementSystemProgram` are present

        """
        return self._data["Energy Management System"][
            "energymanagementsystem:program"]

    @property
    def energymanagementsystemsubroutines(self):
        """Get list of all `EnergyManagementSystemSubroutine` objects.

        Raises:
            ValueError: if no objects of type `EnergyManagementSystemSubroutine` are present

        """
        return self._data["Energy Management System"][
            "energymanagementsystem:subroutine"]

    @property
    def energymanagementsystemglobalvariables(self):
        """Get list of all `EnergyManagementSystemGlobalVariable` objects.

        Raises:
            ValueError: if no objects of type `EnergyManagementSystemGlobalVariable` are present

        """
        return self._data["Energy Management System"][
            "energymanagementsystem:globalvariable"]

    @property
    def energymanagementsystemoutputvariables(self):
        """Get list of all `EnergyManagementSystemOutputVariable` objects.

        Raises:
            ValueError: if no objects of type `EnergyManagementSystemOutputVariable` are present

        """
        return self._data["Energy Management System"][
            "energymanagementsystem:outputvariable"]

    @property
    def energymanagementsystemmeteredoutputvariables(self):
        """Get list of all `EnergyManagementSystemMeteredOutputVariable`
        objects.

        Raises:
            ValueError: if no objects of type `EnergyManagementSystemMeteredOutputVariable` are present

        """
        return self._data["Energy Management System"][
            "energymanagementsystem:meteredoutputvariable"]

    @property
    def energymanagementsystemtrendvariables(self):
        """Get list of all `EnergyManagementSystemTrendVariable` objects.

        Raises:
            ValueError: if no objects of type `EnergyManagementSystemTrendVariable` are present

        """
        return self._data["Energy Management System"][
            "energymanagementsystem:trendvariable"]

    @property
    def energymanagementsysteminternalvariables(self):
        """Get list of all `EnergyManagementSystemInternalVariable` objects.

        Raises:
            ValueError: if no objects of type `EnergyManagementSystemInternalVariable` are present

        """
        return self._data["Energy Management System"][
            "energymanagementsystem:internalvariable"]

    @property
    def energymanagementsystemcurveortableindexvariables(self):
        """Get list of all `EnergyManagementSystemCurveOrTableIndexVariable`
        objects.

        Raises:
            ValueError: if no objects of type `EnergyManagementSystemCurveOrTableIndexVariable` are present

        """
        return self._data["Energy Management System"][
            "energymanagementsystem:curveortableindexvariable"]

    @property
    def energymanagementsystemconstructionindexvariables(self):
        """Get list of all `EnergyManagementSystemConstructionIndexVariable`
        objects.

        Raises:
            ValueError: if no objects of type `EnergyManagementSystemConstructionIndexVariable` are present

        """
        return self._data["Energy Management System"][
            "energymanagementsystem:constructionindexvariable"]

    @property
    def externalinterfaces(self):
        """Get list of all `ExternalInterface` objects.

        Raises:
            ValueError: if no objects of type `ExternalInterface` are present

        """
        return self._data["External Interface"]["externalinterface"]

    @property
    def externalinterfaceschedules(self):
        """Get list of all `ExternalInterfaceSchedule` objects.

        Raises:
            ValueError: if no objects of type `ExternalInterfaceSchedule` are present

        """
        return self._data["External Interface"]["externalinterface:schedule"]

    @property
    def externalinterfacevariables(self):
        """Get list of all `ExternalInterfaceVariable` objects.

        Raises:
            ValueError: if no objects of type `ExternalInterfaceVariable` are present

        """
        return self._data["External Interface"]["externalinterface:variable"]

    @property
    def externalinterfaceactuators(self):
        """Get list of all `ExternalInterfaceActuator` objects.

        Raises:
            ValueError: if no objects of type `ExternalInterfaceActuator` are present

        """
        return self._data["External Interface"]["externalinterface:actuator"]

    @property
    def externalinterfacefunctionalmockupunitimports(self):
        """Get list of all `ExternalInterfaceFunctionalMockupUnitImport`
        objects.

        Raises:
            ValueError: if no objects of type `ExternalInterfaceFunctionalMockupUnitImport` are present

        """
        return self._data["External Interface"][
            "externalinterface:functionalmockupunitimport"]

    @property
    def externalinterfacefunctionalmockupunitimportfromvariables(self):
        """Get list of all
        `ExternalInterfaceFunctionalMockupUnitImportFromVariable` objects.

        Raises:
            ValueError: if no objects of type `ExternalInterfaceFunctionalMockupUnitImportFromVariable` are present

        """
        return self._data["External Interface"][
            "externalinterface:functionalmockupunitimport:from:variable"]

    @property
    def externalinterfacefunctionalmockupunitimporttoschedules(self):
        """Get list of all
        `ExternalInterfaceFunctionalMockupUnitImportToSchedule` objects.

        Raises:
            ValueError: if no objects of type `ExternalInterfaceFunctionalMockupUnitImportToSchedule` are present

        """
        return self._data["External Interface"][
            "externalinterface:functionalmockupunitimport:to:schedule"]

    @property
    def externalinterfacefunctionalmockupunitimporttoactuators(self):
        """Get list of all
        `ExternalInterfaceFunctionalMockupUnitImportToActuator` objects.

        Raises:
            ValueError: if no objects of type `ExternalInterfaceFunctionalMockupUnitImportToActuator` are present

        """
        return self._data["External Interface"][
            "externalinterface:functionalmockupunitimport:to:actuator"]

    @property
    def externalinterfacefunctionalmockupunitimporttovariables(self):
        """Get list of all
        `ExternalInterfaceFunctionalMockupUnitImportToVariable` objects.

        Raises:
            ValueError: if no objects of type `ExternalInterfaceFunctionalMockupUnitImportToVariable` are present

        """
        return self._data["External Interface"][
            "externalinterface:functionalmockupunitimport:to:variable"]

    @property
    def externalinterfacefunctionalmockupunitexportfromvariables(self):
        """Get list of all
        `ExternalInterfaceFunctionalMockupUnitExportFromVariable` objects.

        Raises:
            ValueError: if no objects of type `ExternalInterfaceFunctionalMockupUnitExportFromVariable` are present

        """
        return self._data["External Interface"][
            "externalinterface:functionalmockupunitexport:from:variable"]

    @property
    def externalinterfacefunctionalmockupunitexporttoschedules(self):
        """Get list of all
        `ExternalInterfaceFunctionalMockupUnitExportToSchedule` objects.

        Raises:
            ValueError: if no objects of type `ExternalInterfaceFunctionalMockupUnitExportToSchedule` are present

        """
        return self._data["External Interface"][
            "externalinterface:functionalmockupunitexport:to:schedule"]

    @property
    def externalinterfacefunctionalmockupunitexporttoactuators(self):
        """Get list of all
        `ExternalInterfaceFunctionalMockupUnitExportToActuator` objects.

        Raises:
            ValueError: if no objects of type `ExternalInterfaceFunctionalMockupUnitExportToActuator` are present

        """
        return self._data["External Interface"][
            "externalinterface:functionalmockupunitexport:to:actuator"]

    @property
    def externalinterfacefunctionalmockupunitexporttovariables(self):
        """Get list of all
        `ExternalInterfaceFunctionalMockupUnitExportToVariable` objects.

        Raises:
            ValueError: if no objects of type `ExternalInterfaceFunctionalMockupUnitExportToVariable` are present

        """
        return self._data["External Interface"][
            "externalinterface:functionalmockupunitexport:to:variable"]

    @property
    def zonehvacforcedairuserdefineds(self):
        """Get list of all `ZoneHvacForcedAirUserDefined` objects.

        Raises:
            ValueError: if no objects of type `ZoneHvacForcedAirUserDefined` are present

        """
        return self._data["User Defined HVAC and Plant Component Models"][
            "zonehvac:forcedair:userdefined"]

    @property
    def airterminalsingleductuserdefineds(self):
        """Get list of all `AirTerminalSingleDuctUserDefined` objects.

        Raises:
            ValueError: if no objects of type `AirTerminalSingleDuctUserDefined` are present

        """
        return self._data["User Defined HVAC and Plant Component Models"][
            "airterminal:singleduct:userdefined"]

    @property
    def coiluserdefineds(self):
        """Get list of all `CoilUserDefined` objects.

        Raises:
            ValueError: if no objects of type `CoilUserDefined` are present

        """
        return self._data["User Defined HVAC and Plant Component Models"][
            "coil:userdefined"]

    @property
    def plantcomponentuserdefineds(self):
        """Get list of all `PlantComponentUserDefined` objects.

        Raises:
            ValueError: if no objects of type `PlantComponentUserDefined` are present

        """
        return self._data["User Defined HVAC and Plant Component Models"][
            "plantcomponent:userdefined"]

    @property
    def plantequipmentoperationuserdefineds(self):
        """Get list of all `PlantEquipmentOperationUserDefined` objects.

        Raises:
            ValueError: if no objects of type `PlantEquipmentOperationUserDefined` are present

        """
        return self._data["User Defined HVAC and Plant Component Models"][
            "plantequipmentoperation:userdefined"]

    @property
    def availabilitymanagerscheduleds(self):
        """Get list of all `AvailabilityManagerScheduled` objects.

        Raises:
            ValueError: if no objects of type `AvailabilityManagerScheduled` are present

        """
        return self._data["System Availability Managers"][
            "availabilitymanager:scheduled"]

    @property
    def availabilitymanagerscheduledons(self):
        """Get list of all `AvailabilityManagerScheduledOn` objects.

        Raises:
            ValueError: if no objects of type `AvailabilityManagerScheduledOn` are present

        """
        return self._data["System Availability Managers"][
            "availabilitymanager:scheduledon"]

    @property
    def availabilitymanagerscheduledoffs(self):
        """Get list of all `AvailabilityManagerScheduledOff` objects.

        Raises:
            ValueError: if no objects of type `AvailabilityManagerScheduledOff` are present

        """
        return self._data["System Availability Managers"][
            "availabilitymanager:scheduledoff"]

    @property
    def availabilitymanageroptimumstarts(self):
        """Get list of all `AvailabilityManagerOptimumStart` objects.

        Raises:
            ValueError: if no objects of type `AvailabilityManagerOptimumStart` are present

        """
        return self._data["System Availability Managers"][
            "availabilitymanager:optimumstart"]

    @property
    def availabilitymanagernightcycles(self):
        """Get list of all `AvailabilityManagerNightCycle` objects.

        Raises:
            ValueError: if no objects of type `AvailabilityManagerNightCycle` are present

        """
        return self._data["System Availability Managers"][
            "availabilitymanager:nightcycle"]

    @property
    def availabilitymanagerdifferentialthermostats(self):
        """Get list of all `AvailabilityManagerDifferentialThermostat` objects.

        Raises:
            ValueError: if no objects of type `AvailabilityManagerDifferentialThermostat` are present

        """
        return self._data["System Availability Managers"][
            "availabilitymanager:differentialthermostat"]

    @property
    def availabilitymanagerhightemperatureturnoffs(self):
        """Get list of all `AvailabilityManagerHighTemperatureTurnOff` objects.

        Raises:
            ValueError: if no objects of type `AvailabilityManagerHighTemperatureTurnOff` are present

        """
        return self._data["System Availability Managers"][
            "availabilitymanager:hightemperatureturnoff"]

    @property
    def availabilitymanagerhightemperatureturnons(self):
        """Get list of all `AvailabilityManagerHighTemperatureTurnOn` objects.

        Raises:
            ValueError: if no objects of type `AvailabilityManagerHighTemperatureTurnOn` are present

        """
        return self._data["System Availability Managers"][
            "availabilitymanager:hightemperatureturnon"]

    @property
    def availabilitymanagerlowtemperatureturnoffs(self):
        """Get list of all `AvailabilityManagerLowTemperatureTurnOff` objects.

        Raises:
            ValueError: if no objects of type `AvailabilityManagerLowTemperatureTurnOff` are present

        """
        return self._data["System Availability Managers"][
            "availabilitymanager:lowtemperatureturnoff"]

    @property
    def availabilitymanagerlowtemperatureturnons(self):
        """Get list of all `AvailabilityManagerLowTemperatureTurnOn` objects.

        Raises:
            ValueError: if no objects of type `AvailabilityManagerLowTemperatureTurnOn` are present

        """
        return self._data["System Availability Managers"][
            "availabilitymanager:lowtemperatureturnon"]

    @property
    def availabilitymanagernightventilations(self):
        """Get list of all `AvailabilityManagerNightVentilation` objects.

        Raises:
            ValueError: if no objects of type `AvailabilityManagerNightVentilation` are present

        """
        return self._data["System Availability Managers"][
            "availabilitymanager:nightventilation"]

    @property
    def availabilitymanagerhybridventilations(self):
        """Get list of all `AvailabilityManagerHybridVentilation` objects.

        Raises:
            ValueError: if no objects of type `AvailabilityManagerHybridVentilation` are present

        """
        return self._data["System Availability Managers"][
            "availabilitymanager:hybridventilation"]

    @property
    def availabilitymanagerassignmentlists(self):
        """Get list of all `AvailabilityManagerAssignmentList` objects.

        Raises:
            ValueError: if no objects of type `AvailabilityManagerAssignmentList` are present

        """
        return self._data["System Availability Managers"][
            "availabilitymanagerassignmentlist"]

    @property
    def setpointmanagerscheduleds(self):
        """Get list of all `SetpointManagerScheduled` objects.

        Raises:
            ValueError: if no objects of type `SetpointManagerScheduled` are present

        """
        return self._data["Setpoint Managers"]["setpointmanager:scheduled"]

    @property
    def setpointmanagerscheduleddualsetpoints(self):
        """Get list of all `SetpointManagerScheduledDualSetpoint` objects.

        Raises:
            ValueError: if no objects of type `SetpointManagerScheduledDualSetpoint` are present

        """
        return self._data["Setpoint Managers"][
            "setpointmanager:scheduled:dualsetpoint"]

    @property
    def setpointmanageroutdoorairresets(self):
        """Get list of all `SetpointManagerOutdoorAirReset` objects.

        Raises:
            ValueError: if no objects of type `SetpointManagerOutdoorAirReset` are present

        """
        return self._data["Setpoint Managers"][
            "setpointmanager:outdoorairreset"]

    @property
    def setpointmanagersinglezonereheats(self):
        """Get list of all `SetpointManagerSingleZoneReheat` objects.

        Raises:
            ValueError: if no objects of type `SetpointManagerSingleZoneReheat` are present

        """
        return self._data["Setpoint Managers"][
            "setpointmanager:singlezone:reheat"]

    @property
    def setpointmanagersinglezoneheatings(self):
        """Get list of all `SetpointManagerSingleZoneHeating` objects.

        Raises:
            ValueError: if no objects of type `SetpointManagerSingleZoneHeating` are present

        """
        return self._data["Setpoint Managers"][
            "setpointmanager:singlezone:heating"]

    @property
    def setpointmanagersinglezonecoolings(self):
        """Get list of all `SetpointManagerSingleZoneCooling` objects.

        Raises:
            ValueError: if no objects of type `SetpointManagerSingleZoneCooling` are present

        """
        return self._data["Setpoint Managers"][
            "setpointmanager:singlezone:cooling"]

    @property
    def setpointmanagersinglezonehumidityminimums(self):
        """Get list of all `SetpointManagerSingleZoneHumidityMinimum` objects.

        Raises:
            ValueError: if no objects of type `SetpointManagerSingleZoneHumidityMinimum` are present

        """
        return self._data["Setpoint Managers"][
            "setpointmanager:singlezone:humidity:minimum"]

    @property
    def setpointmanagersinglezonehumiditymaximums(self):
        """Get list of all `SetpointManagerSingleZoneHumidityMaximum` objects.

        Raises:
            ValueError: if no objects of type `SetpointManagerSingleZoneHumidityMaximum` are present

        """
        return self._data["Setpoint Managers"][
            "setpointmanager:singlezone:humidity:maximum"]

    @property
    def setpointmanagermixedairs(self):
        """Get list of all `SetpointManagerMixedAir` objects.

        Raises:
            ValueError: if no objects of type `SetpointManagerMixedAir` are present

        """
        return self._data["Setpoint Managers"]["setpointmanager:mixedair"]

    @property
    def setpointmanageroutdoorairpretreats(self):
        """Get list of all `SetpointManagerOutdoorAirPretreat` objects.

        Raises:
            ValueError: if no objects of type `SetpointManagerOutdoorAirPretreat` are present

        """
        return self._data["Setpoint Managers"][
            "setpointmanager:outdoorairpretreat"]

    @property
    def setpointmanagerwarmests(self):
        """Get list of all `SetpointManagerWarmest` objects.

        Raises:
            ValueError: if no objects of type `SetpointManagerWarmest` are present

        """
        return self._data["Setpoint Managers"]["setpointmanager:warmest"]

    @property
    def setpointmanagercoldests(self):
        """Get list of all `SetpointManagerColdest` objects.

        Raises:
            ValueError: if no objects of type `SetpointManagerColdest` are present

        """
        return self._data["Setpoint Managers"]["setpointmanager:coldest"]

    @property
    def setpointmanagerreturnairbypassflows(self):
        """Get list of all `SetpointManagerReturnAirBypassFlow` objects.

        Raises:
            ValueError: if no objects of type `SetpointManagerReturnAirBypassFlow` are present

        """
        return self._data["Setpoint Managers"][
            "setpointmanager:returnairbypassflow"]

    @property
    def setpointmanagerwarmesttemperatureflows(self):
        """Get list of all `SetpointManagerWarmestTemperatureFlow` objects.

        Raises:
            ValueError: if no objects of type `SetpointManagerWarmestTemperatureFlow` are present

        """
        return self._data["Setpoint Managers"][
            "setpointmanager:warmesttemperatureflow"]

    @property
    def setpointmanagermultizoneheatingaverages(self):
        """Get list of all `SetpointManagerMultiZoneHeatingAverage` objects.

        Raises:
            ValueError: if no objects of type `SetpointManagerMultiZoneHeatingAverage` are present

        """
        return self._data["Setpoint Managers"][
            "setpointmanager:multizone:heating:average"]

    @property
    def setpointmanagermultizonecoolingaverages(self):
        """Get list of all `SetpointManagerMultiZoneCoolingAverage` objects.

        Raises:
            ValueError: if no objects of type `SetpointManagerMultiZoneCoolingAverage` are present

        """
        return self._data["Setpoint Managers"][
            "setpointmanager:multizone:cooling:average"]

    @property
    def setpointmanagermultizoneminimumhumidityaverages(self):
        """Get list of all `SetpointManagerMultiZoneMinimumHumidityAverage`
        objects.

        Raises:
            ValueError: if no objects of type `SetpointManagerMultiZoneMinimumHumidityAverage` are present

        """
        return self._data["Setpoint Managers"][
            "setpointmanager:multizone:minimumhumidity:average"]

    @property
    def setpointmanagermultizonemaximumhumidityaverages(self):
        """Get list of all `SetpointManagerMultiZoneMaximumHumidityAverage`
        objects.

        Raises:
            ValueError: if no objects of type `SetpointManagerMultiZoneMaximumHumidityAverage` are present

        """
        return self._data["Setpoint Managers"][
            "setpointmanager:multizone:maximumhumidity:average"]

    @property
    def setpointmanagermultizonehumidityminimums(self):
        """Get list of all `SetpointManagerMultiZoneHumidityMinimum` objects.

        Raises:
            ValueError: if no objects of type `SetpointManagerMultiZoneHumidityMinimum` are present

        """
        return self._data["Setpoint Managers"][
            "setpointmanager:multizone:humidity:minimum"]

    @property
    def setpointmanagermultizonehumiditymaximums(self):
        """Get list of all `SetpointManagerMultiZoneHumidityMaximum` objects.

        Raises:
            ValueError: if no objects of type `SetpointManagerMultiZoneHumidityMaximum` are present

        """
        return self._data["Setpoint Managers"][
            "setpointmanager:multizone:humidity:maximum"]

    @property
    def setpointmanagerfollowoutdoorairtemperatures(self):
        """Get list of all `SetpointManagerFollowOutdoorAirTemperature`
        objects.

        Raises:
            ValueError: if no objects of type `SetpointManagerFollowOutdoorAirTemperature` are present

        """
        return self._data["Setpoint Managers"][
            "setpointmanager:followoutdoorairtemperature"]

    @property
    def setpointmanagerfollowsystemnodetemperatures(self):
        """Get list of all `SetpointManagerFollowSystemNodeTemperature`
        objects.

        Raises:
            ValueError: if no objects of type `SetpointManagerFollowSystemNodeTemperature` are present

        """
        return self._data["Setpoint Managers"][
            "setpointmanager:followsystemnodetemperature"]

    @property
    def setpointmanagerfollowgroundtemperatures(self):
        """Get list of all `SetpointManagerFollowGroundTemperature` objects.

        Raises:
            ValueError: if no objects of type `SetpointManagerFollowGroundTemperature` are present

        """
        return self._data["Setpoint Managers"][
            "setpointmanager:followgroundtemperature"]

    @property
    def setpointmanagercondenserenteringresets(self):
        """Get list of all `SetpointManagerCondenserEnteringReset` objects.

        Raises:
            ValueError: if no objects of type `SetpointManagerCondenserEnteringReset` are present

        """
        return self._data["Setpoint Managers"][
            "setpointmanager:condenserenteringreset"]

    @property
    def setpointmanagercondenserenteringresetideals(self):
        """Get list of all `SetpointManagerCondenserEnteringResetIdeal`
        objects.

        Raises:
            ValueError: if no objects of type `SetpointManagerCondenserEnteringResetIdeal` are present

        """
        return self._data["Setpoint Managers"][
            "setpointmanager:condenserenteringreset:ideal"]

    @property
    def setpointmanagersinglezoneonestagecoolings(self):
        """Get list of all `SetpointManagerSingleZoneOneStageCooling` objects.

        Raises:
            ValueError: if no objects of type `SetpointManagerSingleZoneOneStageCooling` are present

        """
        return self._data["Setpoint Managers"][
            "setpointmanager:singlezone:onestagecooling"]

    @property
    def setpointmanagersinglezoneonestageheatings(self):
        """Get list of all `SetpointManagerSingleZoneOneStageHeating` objects.

        Raises:
            ValueError: if no objects of type `SetpointManagerSingleZoneOneStageHeating` are present

        """
        return self._data["Setpoint Managers"][
            "setpointmanager:singlezone:onestageheating"]

    @property
    def refrigerationcases(self):
        """Get list of all `RefrigerationCase` objects.

        Raises:
            ValueError: if no objects of type `RefrigerationCase` are present

        """
        return self._data["Refrigeration"]["refrigeration:case"]

    @property
    def refrigerationcompressorracks(self):
        """Get list of all `RefrigerationCompressorRack` objects.

        Raises:
            ValueError: if no objects of type `RefrigerationCompressorRack` are present

        """
        return self._data["Refrigeration"]["refrigeration:compressorrack"]

    @property
    def refrigerationcaseandwalkinlists(self):
        """Get list of all `RefrigerationCaseAndWalkInList` objects.

        Raises:
            ValueError: if no objects of type `RefrigerationCaseAndWalkInList` are present

        """
        return self._data["Refrigeration"]["refrigeration:caseandwalkinlist"]

    @property
    def refrigerationcondenseraircooleds(self):
        """Get list of all `RefrigerationCondenserAirCooled` objects.

        Raises:
            ValueError: if no objects of type `RefrigerationCondenserAirCooled` are present

        """
        return self._data["Refrigeration"]["refrigeration:condenser:aircooled"]

    @property
    def refrigerationcondenserevaporativecooleds(self):
        """Get list of all `RefrigerationCondenserEvaporativeCooled` objects.

        Raises:
            ValueError: if no objects of type `RefrigerationCondenserEvaporativeCooled` are present

        """
        return self._data["Refrigeration"][
            "refrigeration:condenser:evaporativecooled"]

    @property
    def refrigerationcondenserwatercooleds(self):
        """Get list of all `RefrigerationCondenserWaterCooled` objects.

        Raises:
            ValueError: if no objects of type `RefrigerationCondenserWaterCooled` are present

        """
        return self._data["Refrigeration"][
            "refrigeration:condenser:watercooled"]

    @property
    def refrigerationcondensercascades(self):
        """Get list of all `RefrigerationCondenserCascade` objects.

        Raises:
            ValueError: if no objects of type `RefrigerationCondenserCascade` are present

        """
        return self._data["Refrigeration"]["refrigeration:condenser:cascade"]

    @property
    def refrigerationgascooleraircooleds(self):
        """Get list of all `RefrigerationGasCoolerAirCooled` objects.

        Raises:
            ValueError: if no objects of type `RefrigerationGasCoolerAirCooled` are present

        """
        return self._data["Refrigeration"]["refrigeration:gascooler:aircooled"]

    @property
    def refrigerationtransferloadlists(self):
        """Get list of all `RefrigerationTransferLoadList` objects.

        Raises:
            ValueError: if no objects of type `RefrigerationTransferLoadList` are present

        """
        return self._data["Refrigeration"]["refrigeration:transferloadlist"]

    @property
    def refrigerationsubcoolers(self):
        """Get list of all `RefrigerationSubcooler` objects.

        Raises:
            ValueError: if no objects of type `RefrigerationSubcooler` are present

        """
        return self._data["Refrigeration"]["refrigeration:subcooler"]

    @property
    def refrigerationcompressors(self):
        """Get list of all `RefrigerationCompressor` objects.

        Raises:
            ValueError: if no objects of type `RefrigerationCompressor` are present

        """
        return self._data["Refrigeration"]["refrigeration:compressor"]

    @property
    def refrigerationcompressorlists(self):
        """Get list of all `RefrigerationCompressorList` objects.

        Raises:
            ValueError: if no objects of type `RefrigerationCompressorList` are present

        """
        return self._data["Refrigeration"]["refrigeration:compressorlist"]

    @property
    def refrigerationsystems(self):
        """Get list of all `RefrigerationSystem` objects.

        Raises:
            ValueError: if no objects of type `RefrigerationSystem` are present

        """
        return self._data["Refrigeration"]["refrigeration:system"]

    @property
    def refrigerationtranscriticalsystems(self):
        """Get list of all `RefrigerationTranscriticalSystem` objects.

        Raises:
            ValueError: if no objects of type `RefrigerationTranscriticalSystem` are present

        """
        return self._data["Refrigeration"]["refrigeration:transcriticalsystem"]

    @property
    def refrigerationsecondarysystems(self):
        """Get list of all `RefrigerationSecondarySystem` objects.

        Raises:
            ValueError: if no objects of type `RefrigerationSecondarySystem` are present

        """
        return self._data["Refrigeration"]["refrigeration:secondarysystem"]

    @property
    def refrigerationwalkins(self):
        """Get list of all `RefrigerationWalkIn` objects.

        Raises:
            ValueError: if no objects of type `RefrigerationWalkIn` are present

        """
        return self._data["Refrigeration"]["refrigeration:walkin"]

    @property
    def refrigerationairchillers(self):
        """Get list of all `RefrigerationAirChiller` objects.

        Raises:
            ValueError: if no objects of type `RefrigerationAirChiller` are present

        """
        return self._data["Refrigeration"]["refrigeration:airchiller"]

    @property
    def zonehvacrefrigerationchillersets(self):
        """Get list of all `ZoneHvacRefrigerationChillerSet` objects.

        Raises:
            ValueError: if no objects of type `ZoneHvacRefrigerationChillerSet` are present

        """
        return self._data["Refrigeration"]["zonehvac:refrigerationchillerset"]

    @property
    def demandmanagerassignmentlists(self):
        """Get list of all `DemandManagerAssignmentList` objects.

        Raises:
            ValueError: if no objects of type `DemandManagerAssignmentList` are present

        """
        return self._data["Demand Limiting Controls"][
            "demandmanagerassignmentlist"]

    @property
    def demandmanagerexteriorlightss(self):
        """Get list of all `DemandManagerExteriorLights` objects.

        Raises:
            ValueError: if no objects of type `DemandManagerExteriorLights` are present

        """
        return self._data["Demand Limiting Controls"][
            "demandmanager:exteriorlights"]

    @property
    def demandmanagerlightss(self):
        """Get list of all `DemandManagerLights` objects.

        Raises:
            ValueError: if no objects of type `DemandManagerLights` are present

        """
        return self._data["Demand Limiting Controls"]["demandmanager:lights"]

    @property
    def demandmanagerelectricequipments(self):
        """Get list of all `DemandManagerElectricEquipment` objects.

        Raises:
            ValueError: if no objects of type `DemandManagerElectricEquipment` are present

        """
        return self._data["Demand Limiting Controls"][
            "demandmanager:electricequipment"]

    @property
    def demandmanagerthermostatss(self):
        """Get list of all `DemandManagerThermostats` objects.

        Raises:
            ValueError: if no objects of type `DemandManagerThermostats` are present

        """
        return self._data["Demand Limiting Controls"][
            "demandmanager:thermostats"]

    @property
    def generatorinternalcombustionengines(self):
        """Get list of all `GeneratorInternalCombustionEngine` objects.

        Raises:
            ValueError: if no objects of type `GeneratorInternalCombustionEngine` are present

        """
        return self._data["Electric Load Center"][
            "generator:internalcombustionengine"]

    @property
    def generatorcombustionturbines(self):
        """Get list of all `GeneratorCombustionTurbine` objects.

        Raises:
            ValueError: if no objects of type `GeneratorCombustionTurbine` are present

        """
        return self._data["Electric Load Center"][
            "generator:combustionturbine"]

    @property
    def generatormicroturbines(self):
        """Get list of all `GeneratorMicroTurbine` objects.

        Raises:
            ValueError: if no objects of type `GeneratorMicroTurbine` are present

        """
        return self._data["Electric Load Center"]["generator:microturbine"]

    @property
    def generatorphotovoltaics(self):
        """Get list of all `GeneratorPhotovoltaic` objects.

        Raises:
            ValueError: if no objects of type `GeneratorPhotovoltaic` are present

        """
        return self._data["Electric Load Center"]["generator:photovoltaic"]

    @property
    def photovoltaicperformancesimples(self):
        """Get list of all `PhotovoltaicPerformanceSimple` objects.

        Raises:
            ValueError: if no objects of type `PhotovoltaicPerformanceSimple` are present

        """
        return self._data["Electric Load Center"][
            "photovoltaicperformance:simple"]

    @property
    def photovoltaicperformanceequivalentonediodes(self):
        """Get list of all `PhotovoltaicPerformanceEquivalentOneDiode` objects.

        Raises:
            ValueError: if no objects of type `PhotovoltaicPerformanceEquivalentOneDiode` are present

        """
        return self._data["Electric Load Center"][
            "photovoltaicperformance:equivalentone-diode"]

    @property
    def photovoltaicperformancesandias(self):
        """Get list of all `PhotovoltaicPerformanceSandia` objects.

        Raises:
            ValueError: if no objects of type `PhotovoltaicPerformanceSandia` are present

        """
        return self._data["Electric Load Center"][
            "photovoltaicperformance:sandia"]

    @property
    def generatorfuelcells(self):
        """Get list of all `GeneratorFuelCell` objects.

        Raises:
            ValueError: if no objects of type `GeneratorFuelCell` are present

        """
        return self._data["Electric Load Center"]["generator:fuelcell"]

    @property
    def generatorfuelcellpowermodules(self):
        """Get list of all `GeneratorFuelCellPowerModule` objects.

        Raises:
            ValueError: if no objects of type `GeneratorFuelCellPowerModule` are present

        """
        return self._data["Electric Load Center"][
            "generator:fuelcell:powermodule"]

    @property
    def generatorfuelcellairsupplys(self):
        """Get list of all `GeneratorFuelCellAirSupply` objects.

        Raises:
            ValueError: if no objects of type `GeneratorFuelCellAirSupply` are present

        """
        return self._data["Electric Load Center"][
            "generator:fuelcell:airsupply"]

    @property
    def generatorfuelcellwatersupplys(self):
        """Get list of all `GeneratorFuelCellWaterSupply` objects.

        Raises:
            ValueError: if no objects of type `GeneratorFuelCellWaterSupply` are present

        """
        return self._data["Electric Load Center"][
            "generator:fuelcell:watersupply"]

    @property
    def generatorfuelcellauxiliaryheaters(self):
        """Get list of all `GeneratorFuelCellAuxiliaryHeater` objects.

        Raises:
            ValueError: if no objects of type `GeneratorFuelCellAuxiliaryHeater` are present

        """
        return self._data["Electric Load Center"][
            "generator:fuelcell:auxiliaryheater"]

    @property
    def generatorfuelcellexhaustgastowaterheatexchangers(self):
        """Get list of all `GeneratorFuelCellExhaustGasToWaterHeatExchanger`
        objects.

        Raises:
            ValueError: if no objects of type `GeneratorFuelCellExhaustGasToWaterHeatExchanger` are present

        """
        return self._data["Electric Load Center"][
            "generator:fuelcell:exhaustgastowaterheatexchanger"]

    @property
    def generatorfuelcellelectricalstorages(self):
        """Get list of all `GeneratorFuelCellElectricalStorage` objects.

        Raises:
            ValueError: if no objects of type `GeneratorFuelCellElectricalStorage` are present

        """
        return self._data["Electric Load Center"][
            "generator:fuelcell:electricalstorage"]

    @property
    def generatorfuelcellinverters(self):
        """Get list of all `GeneratorFuelCellInverter` objects.

        Raises:
            ValueError: if no objects of type `GeneratorFuelCellInverter` are present

        """
        return self._data["Electric Load Center"][
            "generator:fuelcell:inverter"]

    @property
    def generatorfuelcellstackcoolers(self):
        """Get list of all `GeneratorFuelCellStackCooler` objects.

        Raises:
            ValueError: if no objects of type `GeneratorFuelCellStackCooler` are present

        """
        return self._data["Electric Load Center"][
            "generator:fuelcell:stackcooler"]

    @property
    def generatormicrochps(self):
        """Get list of all `GeneratorMicroChp` objects.

        Raises:
            ValueError: if no objects of type `GeneratorMicroChp` are present

        """
        return self._data["Electric Load Center"]["generator:microchp"]

    @property
    def generatormicrochpnonnormalizedparameterss(self):
        """Get list of all `GeneratorMicroChpNonNormalizedParameters` objects.

        Raises:
            ValueError: if no objects of type `GeneratorMicroChpNonNormalizedParameters` are present

        """
        return self._data["Electric Load Center"][
            "generator:microchp:nonnormalizedparameters"]

    @property
    def generatorfuelsupplys(self):
        """Get list of all `GeneratorFuelSupply` objects.

        Raises:
            ValueError: if no objects of type `GeneratorFuelSupply` are present

        """
        return self._data["Electric Load Center"]["generator:fuelsupply"]

    @property
    def generatorwindturbines(self):
        """Get list of all `GeneratorWindTurbine` objects.

        Raises:
            ValueError: if no objects of type `GeneratorWindTurbine` are present

        """
        return self._data["Electric Load Center"]["generator:windturbine"]

    @property
    def electricloadcentergeneratorss(self):
        """Get list of all `ElectricLoadCenterGenerators` objects.

        Raises:
            ValueError: if no objects of type `ElectricLoadCenterGenerators` are present

        """
        return self._data["Electric Load Center"][
            "electricloadcenter:generators"]

    @property
    def electricloadcenterinvertersimples(self):
        """Get list of all `ElectricLoadCenterInverterSimple` objects.

        Raises:
            ValueError: if no objects of type `ElectricLoadCenterInverterSimple` are present

        """
        return self._data["Electric Load Center"][
            "electricloadcenter:inverter:simple"]

    @property
    def electricloadcenterinverterfunctionofpowers(self):
        """Get list of all `ElectricLoadCenterInverterFunctionOfPower` objects.

        Raises:
            ValueError: if no objects of type `ElectricLoadCenterInverterFunctionOfPower` are present

        """
        return self._data["Electric Load Center"][
            "electricloadcenter:inverter:functionofpower"]

    @property
    def electricloadcenterinverterlookuptables(self):
        """Get list of all `ElectricLoadCenterInverterLookUpTable` objects.

        Raises:
            ValueError: if no objects of type `ElectricLoadCenterInverterLookUpTable` are present

        """
        return self._data["Electric Load Center"][
            "electricloadcenter:inverter:lookuptable"]

    @property
    def electricloadcenterstoragesimples(self):
        """Get list of all `ElectricLoadCenterStorageSimple` objects.

        Raises:
            ValueError: if no objects of type `ElectricLoadCenterStorageSimple` are present

        """
        return self._data["Electric Load Center"][
            "electricloadcenter:storage:simple"]

    @property
    def electricloadcenterstoragebatterys(self):
        """Get list of all `ElectricLoadCenterStorageBattery` objects.

        Raises:
            ValueError: if no objects of type `ElectricLoadCenterStorageBattery` are present

        """
        return self._data["Electric Load Center"][
            "electricloadcenter:storage:battery"]

    @property
    def electricloadcentertransformers(self):
        """Get list of all `ElectricLoadCenterTransformer` objects.

        Raises:
            ValueError: if no objects of type `ElectricLoadCenterTransformer` are present

        """
        return self._data["Electric Load Center"][
            "electricloadcenter:transformer"]

    @property
    def electricloadcenterdistributions(self):
        """Get list of all `ElectricLoadCenterDistribution` objects.

        Raises:
            ValueError: if no objects of type `ElectricLoadCenterDistribution` are present

        """
        return self._data["Electric Load Center"][
            "electricloadcenter:distribution"]

    @property
    def wateruseequipments(self):
        """Get list of all `WaterUseEquipment` objects.

        Raises:
            ValueError: if no objects of type `WaterUseEquipment` are present

        """
        return self._data["Water Systems"]["wateruse:equipment"]

    @property
    def wateruseconnectionss(self):
        """Get list of all `WaterUseConnections` objects.

        Raises:
            ValueError: if no objects of type `WaterUseConnections` are present

        """
        return self._data["Water Systems"]["wateruse:connections"]

    @property
    def waterusestorages(self):
        """Get list of all `WaterUseStorage` objects.

        Raises:
            ValueError: if no objects of type `WaterUseStorage` are present

        """
        return self._data["Water Systems"]["wateruse:storage"]

    @property
    def waterusewells(self):
        """Get list of all `WaterUseWell` objects.

        Raises:
            ValueError: if no objects of type `WaterUseWell` are present

        """
        return self._data["Water Systems"]["wateruse:well"]

    @property
    def wateruseraincollectors(self):
        """Get list of all `WaterUseRainCollector` objects.

        Raises:
            ValueError: if no objects of type `WaterUseRainCollector` are present

        """
        return self._data["Water Systems"]["wateruse:raincollector"]

    @property
    def faultmodeltemperaturesensoroffsetoutdoorairs(self):
        """Get list of all `FaultModelTemperatureSensorOffsetOutdoorAir`
        objects.

        Raises:
            ValueError: if no objects of type `FaultModelTemperatureSensorOffsetOutdoorAir` are present

        """
        return self._data["Operational Faults"][
            "faultmodel:temperaturesensoroffset:outdoorair"]

    @property
    def faultmodelhumiditysensoroffsetoutdoorairs(self):
        """Get list of all `FaultModelHumiditySensorOffsetOutdoorAir` objects.

        Raises:
            ValueError: if no objects of type `FaultModelHumiditySensorOffsetOutdoorAir` are present

        """
        return self._data["Operational Faults"][
            "faultmodel:humiditysensoroffset:outdoorair"]

    @property
    def faultmodelenthalpysensoroffsetoutdoorairs(self):
        """Get list of all `FaultModelEnthalpySensorOffsetOutdoorAir` objects.

        Raises:
            ValueError: if no objects of type `FaultModelEnthalpySensorOffsetOutdoorAir` are present

        """
        return self._data["Operational Faults"][
            "faultmodel:enthalpysensoroffset:outdoorair"]

    @property
    def faultmodelpressuresensoroffsetoutdoorairs(self):
        """Get list of all `FaultModelPressureSensorOffsetOutdoorAir` objects.

        Raises:
            ValueError: if no objects of type `FaultModelPressureSensorOffsetOutdoorAir` are present

        """
        return self._data["Operational Faults"][
            "faultmodel:pressuresensoroffset:outdoorair"]

    @property
    def faultmodeltemperaturesensoroffsetreturnairs(self):
        """Get list of all `FaultModelTemperatureSensorOffsetReturnAir`
        objects.

        Raises:
            ValueError: if no objects of type `FaultModelTemperatureSensorOffsetReturnAir` are present

        """
        return self._data["Operational Faults"][
            "faultmodel:temperaturesensoroffset:returnair"]

    @property
    def faultmodelenthalpysensoroffsetreturnairs(self):
        """Get list of all `FaultModelEnthalpySensorOffsetReturnAir` objects.

        Raises:
            ValueError: if no objects of type `FaultModelEnthalpySensorOffsetReturnAir` are present

        """
        return self._data["Operational Faults"][
            "faultmodel:enthalpysensoroffset:returnair"]

    @property
    def faultmodelfoulingcoils(self):
        """Get list of all `FaultModelFoulingCoil` objects.

        Raises:
            ValueError: if no objects of type `FaultModelFoulingCoil` are present

        """
        return self._data["Operational Faults"]["faultmodel:fouling:coil"]

    @property
    def matrixtwodimensions(self):
        """Get list of all `MatrixTwoDimension` objects.

        Raises:
            ValueError: if no objects of type `MatrixTwoDimension` are present

        """
        return self._data["Refrigeration"]["matrix:twodimension"]

    @property
    def curvelinears(self):
        """Get list of all `CurveLinear` objects.

        Raises:
            ValueError: if no objects of type `CurveLinear` are present

        """
        return self._data["Performance Curves"]["curve:linear"]

    @property
    def curvequadlinears(self):
        """Get list of all `CurveQuadLinear` objects.

        Raises:
            ValueError: if no objects of type `CurveQuadLinear` are present

        """
        return self._data["Performance Curves"]["curve:quadlinear"]

    @property
    def curvequadratics(self):
        """Get list of all `CurveQuadratic` objects.

        Raises:
            ValueError: if no objects of type `CurveQuadratic` are present

        """
        return self._data["Performance Curves"]["curve:quadratic"]

    @property
    def curvecubics(self):
        """Get list of all `CurveCubic` objects.

        Raises:
            ValueError: if no objects of type `CurveCubic` are present

        """
        return self._data["Performance Curves"]["curve:cubic"]

    @property
    def curvequartics(self):
        """Get list of all `CurveQuartic` objects.

        Raises:
            ValueError: if no objects of type `CurveQuartic` are present

        """
        return self._data["Performance Curves"]["curve:quartic"]

    @property
    def curveexponents(self):
        """Get list of all `CurveExponent` objects.

        Raises:
            ValueError: if no objects of type `CurveExponent` are present

        """
        return self._data["Performance Curves"]["curve:exponent"]

    @property
    def curvebicubics(self):
        """Get list of all `CurveBicubic` objects.

        Raises:
            ValueError: if no objects of type `CurveBicubic` are present

        """
        return self._data["Performance Curves"]["curve:bicubic"]

    @property
    def curvebiquadratics(self):
        """Get list of all `CurveBiquadratic` objects.

        Raises:
            ValueError: if no objects of type `CurveBiquadratic` are present

        """
        return self._data["Performance Curves"]["curve:biquadratic"]

    @property
    def curvequadraticlinears(self):
        """Get list of all `CurveQuadraticLinear` objects.

        Raises:
            ValueError: if no objects of type `CurveQuadraticLinear` are present

        """
        return self._data["Performance Curves"]["curve:quadraticlinear"]

    @property
    def curvetriquadratics(self):
        """Get list of all `CurveTriquadratic` objects.

        Raises:
            ValueError: if no objects of type `CurveTriquadratic` are present

        """
        return self._data["Performance Curves"]["curve:triquadratic"]

    @property
    def curvefunctionalpressuredrops(self):
        """Get list of all `CurveFunctionalPressureDrop` objects.

        Raises:
            ValueError: if no objects of type `CurveFunctionalPressureDrop` are present

        """
        return self._data["Performance Curves"][
            "curve:functional:pressuredrop"]

    @property
    def curvefanpressurerises(self):
        """Get list of all `CurveFanPressureRise` objects.

        Raises:
            ValueError: if no objects of type `CurveFanPressureRise` are present

        """
        return self._data["Performance Curves"]["curve:fanpressurerise"]

    @property
    def curveexponentialskewnormals(self):
        """Get list of all `CurveExponentialSkewNormal` objects.

        Raises:
            ValueError: if no objects of type `CurveExponentialSkewNormal` are present

        """
        return self._data["Performance Curves"]["curve:exponentialskewnormal"]

    @property
    def curvesigmoids(self):
        """Get list of all `CurveSigmoid` objects.

        Raises:
            ValueError: if no objects of type `CurveSigmoid` are present

        """
        return self._data["Performance Curves"]["curve:sigmoid"]

    @property
    def curverectangularhyperbola1s(self):
        """Get list of all `CurveRectangularHyperbola1` objects.

        Raises:
            ValueError: if no objects of type `CurveRectangularHyperbola1` are present

        """
        return self._data["Performance Curves"]["curve:rectangularhyperbola1"]

    @property
    def curverectangularhyperbola2s(self):
        """Get list of all `CurveRectangularHyperbola2` objects.

        Raises:
            ValueError: if no objects of type `CurveRectangularHyperbola2` are present

        """
        return self._data["Performance Curves"]["curve:rectangularhyperbola2"]

    @property
    def curveexponentialdecays(self):
        """Get list of all `CurveExponentialDecay` objects.

        Raises:
            ValueError: if no objects of type `CurveExponentialDecay` are present

        """
        return self._data["Performance Curves"]["curve:exponentialdecay"]

    @property
    def curvedoubleexponentialdecays(self):
        """Get list of all `CurveDoubleExponentialDecay` objects.

        Raises:
            ValueError: if no objects of type `CurveDoubleExponentialDecay` are present

        """
        return self._data["Performance Curves"]["curve:doubleexponentialdecay"]

    @property
    def tableoneindependentvariables(self):
        """Get list of all `TableOneIndependentVariable` objects.

        Raises:
            ValueError: if no objects of type `TableOneIndependentVariable` are present

        """
        return self._data["Performance Tables"]["table:oneindependentvariable"]

    @property
    def tabletwoindependentvariabless(self):
        """Get list of all `TableTwoIndependentVariables` objects.

        Raises:
            ValueError: if no objects of type `TableTwoIndependentVariables` are present

        """
        return self._data["Performance Tables"][
            "table:twoindependentvariables"]

    @property
    def tablemultivariablelookups(self):
        """Get list of all `TableMultiVariableLookup` objects.

        Raises:
            ValueError: if no objects of type `TableMultiVariableLookup` are present

        """
        return self._data["Performance Tables"]["table:multivariablelookup"]

    @property
    def fluidpropertiesnames(self):
        """Get list of all `FluidPropertiesName` objects.

        Raises:
            ValueError: if no objects of type `FluidPropertiesName` are present

        """
        return self._data["Fluid Properties"]["fluidproperties:name"]

    @property
    def fluidpropertiesglycolconcentrations(self):
        """Get list of all `FluidPropertiesGlycolConcentration` objects.

        Raises:
            ValueError: if no objects of type `FluidPropertiesGlycolConcentration` are present

        """
        return self._data["Fluid Properties"][
            "fluidproperties:glycolconcentration"]

    @property
    def fluidpropertiestemperaturess(self):
        """Get list of all `FluidPropertiesTemperatures` objects.

        Raises:
            ValueError: if no objects of type `FluidPropertiesTemperatures` are present

        """
        return self._data["Fluid Properties"]["fluidproperties:temperatures"]

    @property
    def fluidpropertiessaturateds(self):
        """Get list of all `FluidPropertiesSaturated` objects.

        Raises:
            ValueError: if no objects of type `FluidPropertiesSaturated` are present

        """
        return self._data["Fluid Properties"]["fluidproperties:saturated"]

    @property
    def fluidpropertiessuperheateds(self):
        """Get list of all `FluidPropertiesSuperheated` objects.

        Raises:
            ValueError: if no objects of type `FluidPropertiesSuperheated` are present

        """
        return self._data["Fluid Properties"]["fluidproperties:superheated"]

    @property
    def fluidpropertiesconcentrations(self):
        """Get list of all `FluidPropertiesConcentration` objects.

        Raises:
            ValueError: if no objects of type `FluidPropertiesConcentration` are present

        """
        return self._data["Fluid Properties"]["fluidproperties:concentration"]

    @property
    def currencytypes(self):
        """Get list of all `CurrencyType` objects.

        Raises:
            ValueError: if no objects of type `CurrencyType` are present

        """
        return self._data["Economics"]["currencytype"]

    @property
    def componentcostadjustmentss(self):
        """Get list of all `ComponentCostAdjustments` objects.

        Raises:
            ValueError: if no objects of type `ComponentCostAdjustments` are present

        """
        return self._data["Economics"]["componentcost:adjustments"]

    @property
    def componentcostreferences(self):
        """Get list of all `ComponentCostReference` objects.

        Raises:
            ValueError: if no objects of type `ComponentCostReference` are present

        """
        return self._data["Economics"]["componentcost:reference"]

    @property
    def componentcostlineitems(self):
        """Get list of all `ComponentCostLineItem` objects.

        Raises:
            ValueError: if no objects of type `ComponentCostLineItem` are present

        """
        return self._data["Economics"]["componentcost:lineitem"]

    @property
    def utilitycosttariffs(self):
        """Get list of all `UtilityCostTariff` objects.

        Raises:
            ValueError: if no objects of type `UtilityCostTariff` are present

        """
        return self._data["Economics"]["utilitycost:tariff"]

    @property
    def utilitycostqualifys(self):
        """Get list of all `UtilityCostQualify` objects.

        Raises:
            ValueError: if no objects of type `UtilityCostQualify` are present

        """
        return self._data["Economics"]["utilitycost:qualify"]

    @property
    def utilitycostchargesimples(self):
        """Get list of all `UtilityCostChargeSimple` objects.

        Raises:
            ValueError: if no objects of type `UtilityCostChargeSimple` are present

        """
        return self._data["Economics"]["utilitycost:charge:simple"]

    @property
    def utilitycostchargeblocks(self):
        """Get list of all `UtilityCostChargeBlock` objects.

        Raises:
            ValueError: if no objects of type `UtilityCostChargeBlock` are present

        """
        return self._data["Economics"]["utilitycost:charge:block"]

    @property
    def utilitycostratchets(self):
        """Get list of all `UtilityCostRatchet` objects.

        Raises:
            ValueError: if no objects of type `UtilityCostRatchet` are present

        """
        return self._data["Economics"]["utilitycost:ratchet"]

    @property
    def utilitycostvariables(self):
        """Get list of all `UtilityCostVariable` objects.

        Raises:
            ValueError: if no objects of type `UtilityCostVariable` are present

        """
        return self._data["Economics"]["utilitycost:variable"]

    @property
    def utilitycostcomputations(self):
        """Get list of all `UtilityCostComputation` objects.

        Raises:
            ValueError: if no objects of type `UtilityCostComputation` are present

        """
        return self._data["Economics"]["utilitycost:computation"]

    @property
    def lifecyclecostparameterss(self):
        """Get list of all `LifeCycleCostParameters` objects.

        Raises:
            ValueError: if no objects of type `LifeCycleCostParameters` are present

        """
        return self._data["Economics"]["lifecyclecost:parameters"]

    @property
    def lifecyclecostrecurringcostss(self):
        """Get list of all `LifeCycleCostRecurringCosts` objects.

        Raises:
            ValueError: if no objects of type `LifeCycleCostRecurringCosts` are present

        """
        return self._data["Economics"]["lifecyclecost:recurringcosts"]

    @property
    def lifecyclecostnonrecurringcosts(self):
        """Get list of all `LifeCycleCostNonrecurringCost` objects.

        Raises:
            ValueError: if no objects of type `LifeCycleCostNonrecurringCost` are present

        """
        return self._data["Economics"]["lifecyclecost:nonrecurringcost"]

    @property
    def lifecyclecostusepriceescalations(self):
        """Get list of all `LifeCycleCostUsePriceEscalation` objects.

        Raises:
            ValueError: if no objects of type `LifeCycleCostUsePriceEscalation` are present

        """
        return self._data["Economics"]["lifecyclecost:usepriceescalation"]

    @property
    def lifecyclecostuseadjustments(self):
        """Get list of all `LifeCycleCostUseAdjustment` objects.

        Raises:
            ValueError: if no objects of type `LifeCycleCostUseAdjustment` are present

        """
        return self._data["Economics"]["lifecyclecost:useadjustment"]

    @property
    def parametricsetvalueforruns(self):
        """Get list of all `ParametricSetValueForRun` objects.

        Raises:
            ValueError: if no objects of type `ParametricSetValueForRun` are present

        """
        return self._data["Parametrics"]["parametric:setvalueforrun"]

    @property
    def parametriclogics(self):
        """Get list of all `ParametricLogic` objects.

        Raises:
            ValueError: if no objects of type `ParametricLogic` are present

        """
        return self._data["Parametrics"]["parametric:logic"]

    @property
    def parametricruncontrols(self):
        """Get list of all `ParametricRunControl` objects.

        Raises:
            ValueError: if no objects of type `ParametricRunControl` are present

        """
        return self._data["Parametrics"]["parametric:runcontrol"]

    @property
    def parametricfilenamesuffixs(self):
        """Get list of all `ParametricFileNameSuffix` objects.

        Raises:
            ValueError: if no objects of type `ParametricFileNameSuffix` are present

        """
        return self._data["Parametrics"]["parametric:filenamesuffix"]

    @property
    def outputvariabledictionarys(self):
        """Get list of all `OutputVariableDictionary` objects.

        Raises:
            ValueError: if no objects of type `OutputVariableDictionary` are present

        """
        return self._data["Output Reporting"]["output:variabledictionary"]

    @property
    def outputsurfaceslists(self):
        """Get list of all `OutputSurfacesList` objects.

        Raises:
            ValueError: if no objects of type `OutputSurfacesList` are present

        """
        return self._data["Output Reporting"]["output:surfaces:list"]

    @property
    def outputsurfacesdrawings(self):
        """Get list of all `OutputSurfacesDrawing` objects.

        Raises:
            ValueError: if no objects of type `OutputSurfacesDrawing` are present

        """
        return self._data["Output Reporting"]["output:surfaces:drawing"]

    @property
    def outputscheduless(self):
        """Get list of all `OutputSchedules` objects.

        Raises:
            ValueError: if no objects of type `OutputSchedules` are present

        """
        return self._data["Output Reporting"]["output:schedules"]

    @property
    def outputconstructionss(self):
        """Get list of all `OutputConstructions` objects.

        Raises:
            ValueError: if no objects of type `OutputConstructions` are present

        """
        return self._data["Output Reporting"]["output:constructions"]

    @property
    def outputenergymanagementsystems(self):
        """Get list of all `OutputEnergyManagementSystem` objects.

        Raises:
            ValueError: if no objects of type `OutputEnergyManagementSystem` are present

        """
        return self._data["Output Reporting"]["output:energymanagementsystem"]

    @property
    def outputcontrolsurfacecolorschemes(self):
        """Get list of all `OutputControlSurfaceColorScheme` objects.

        Raises:
            ValueError: if no objects of type `OutputControlSurfaceColorScheme` are present

        """
        return self._data["Output Reporting"][
            "outputcontrol:surfacecolorscheme"]

    @property
    def outputtablesummaryreportss(self):
        """Get list of all `OutputTableSummaryReports` objects.

        Raises:
            ValueError: if no objects of type `OutputTableSummaryReports` are present

        """
        return self._data["Output Reporting"]["output:table:summaryreports"]

    @property
    def outputtabletimebinss(self):
        """Get list of all `OutputTableTimeBins` objects.

        Raises:
            ValueError: if no objects of type `OutputTableTimeBins` are present

        """
        return self._data["Output Reporting"]["output:table:timebins"]

    @property
    def outputtablemonthlys(self):
        """Get list of all `OutputTableMonthly` objects.

        Raises:
            ValueError: if no objects of type `OutputTableMonthly` are present

        """
        return self._data["Output Reporting"]["output:table:monthly"]

    @property
    def outputcontroltablestyles(self):
        """Get list of all `OutputControlTableStyle` objects.

        Raises:
            ValueError: if no objects of type `OutputControlTableStyle` are present

        """
        return self._data["Output Reporting"]["outputcontrol:table:style"]

    @property
    def outputcontrolreportingtolerancess(self):
        """Get list of all `OutputControlReportingTolerances` objects.

        Raises:
            ValueError: if no objects of type `OutputControlReportingTolerances` are present

        """
        return self._data["Output Reporting"][
            "outputcontrol:reportingtolerances"]

    @property
    def outputvariables(self):
        """Get list of all `OutputVariable` objects.

        Raises:
            ValueError: if no objects of type `OutputVariable` are present

        """
        return self._data["Output Reporting"]["output:variable"]

    @property
    def outputmeters(self):
        """Get list of all `OutputMeter` objects.

        Raises:
            ValueError: if no objects of type `OutputMeter` are present

        """
        return self._data["Output Reporting"]["output:meter"]

    @property
    def outputmetermeterfileonlys(self):
        """Get list of all `OutputMeterMeterFileOnly` objects.

        Raises:
            ValueError: if no objects of type `OutputMeterMeterFileOnly` are present

        """
        return self._data["Output Reporting"]["output:meter:meterfileonly"]

    @property
    def outputmetercumulatives(self):
        """Get list of all `OutputMeterCumulative` objects.

        Raises:
            ValueError: if no objects of type `OutputMeterCumulative` are present

        """
        return self._data["Output Reporting"]["output:meter:cumulative"]

    @property
    def outputmetercumulativemeterfileonlys(self):
        """Get list of all `OutputMeterCumulativeMeterFileOnly` objects.

        Raises:
            ValueError: if no objects of type `OutputMeterCumulativeMeterFileOnly` are present

        """
        return self._data["Output Reporting"][
            "output:meter:cumulative:meterfileonly"]

    @property
    def metercustoms(self):
        """Get list of all `MeterCustom` objects.

        Raises:
            ValueError: if no objects of type `MeterCustom` are present

        """
        return self._data["Output Reporting"]["meter:custom"]

    @property
    def metercustomdecrements(self):
        """Get list of all `MeterCustomDecrement` objects.

        Raises:
            ValueError: if no objects of type `MeterCustomDecrement` are present

        """
        return self._data["Output Reporting"]["meter:customdecrement"]

    @property
    def outputsqlites(self):
        """Get list of all `OutputSqlite` objects.

        Raises:
            ValueError: if no objects of type `OutputSqlite` are present

        """
        return self._data["Output Reporting"]["output:sqlite"]

    @property
    def outputenvironmentalimpactfactorss(self):
        """Get list of all `OutputEnvironmentalImpactFactors` objects.

        Raises:
            ValueError: if no objects of type `OutputEnvironmentalImpactFactors` are present

        """
        return self._data["Output Reporting"][
            "output:environmentalimpactfactors"]

    @property
    def environmentalimpactfactorss(self):
        """Get list of all `EnvironmentalImpactFactors` objects.

        Raises:
            ValueError: if no objects of type `EnvironmentalImpactFactors` are present

        """
        return self._data["Output Reporting"]["environmentalimpactfactors"]

    @property
    def fuelfactorss(self):
        """Get list of all `FuelFactors` objects.

        Raises:
            ValueError: if no objects of type `FuelFactors` are present

        """
        return self._data["Output Reporting"]["fuelfactors"]

    @property
    def outputdiagnosticss(self):
        """Get list of all `OutputDiagnostics` objects.

        Raises:
            ValueError: if no objects of type `OutputDiagnostics` are present

        """
        return self._data["Output Reporting"]["output:diagnostics"]

    @property
    def outputdebuggingdatas(self):
        """Get list of all `OutputDebuggingData` objects.

        Raises:
            ValueError: if no objects of type `OutputDebuggingData` are present

        """
        return self._data["Output Reporting"]["output:debuggingdata"]

    @property
    def outputpreprocessormessages(self):
        """Get list of all `OutputPreprocessorMessage` objects.

        Raises:
            ValueError: if no objects of type `OutputPreprocessorMessage` are present

        """
        return self._data["Output Reporting"]["output:preprocessormessage"]

    @classmethod
    def _create_datadict(cls, internal_name):
        """Creates an object depending on `internal_name`

        Args:
            internal_name (str): IDD name

        Raises:
            ValueError: if `internal_name` cannot be matched to a data dictionary object

        """
        if internal_name.lower() == "lead input":
            return LeadInput()
        if internal_name.lower() == "simulation data":
            return SimulationData()
        if internal_name.lower() == "version":
            return Version()
        if internal_name.lower() == "simulationcontrol":
            return SimulationControl()
        if internal_name.lower() == "building":
            return Building()
        if internal_name.lower() == "shadowcalculation":
            return ShadowCalculation()
        if internal_name.lower() == "surfaceconvectionalgorithm:inside":
            return SurfaceConvectionAlgorithmInside()
        if internal_name.lower() == "surfaceconvectionalgorithm:outside":
            return SurfaceConvectionAlgorithmOutside()
        if internal_name.lower() == "heatbalancealgorithm":
            return HeatBalanceAlgorithm()
        if internal_name.lower(
        ) == "heatbalancesettings:conductionfinitedifference":
            return HeatBalanceSettingsConductionFiniteDifference()
        if internal_name.lower() == "zoneairheatbalancealgorithm":
            return ZoneAirHeatBalanceAlgorithm()
        if internal_name.lower() == "zoneaircontaminantbalance":
            return ZoneAirContaminantBalance()
        if internal_name.lower() == "zoneairmassflowconservation":
            return ZoneAirMassFlowConservation()
        if internal_name.lower(
        ) == "zonecapacitancemultiplier:researchspecial":
            return ZoneCapacitanceMultiplierResearchSpecial()
        if internal_name.lower() == "timestep":
            return Timestep()
        if internal_name.lower() == "convergencelimits":
            return ConvergenceLimits()
        if internal_name.lower() == "programcontrol":
            return ProgramControl()
        if internal_name.lower() == "compliance:building":
            return ComplianceBuilding()
        if internal_name.lower() == "site:location":
            return SiteLocation()
        if internal_name.lower() == "sizingperiod:designday":
            return SizingPeriodDesignDay()
        if internal_name.lower() == "sizingperiod:weatherfiledays":
            return SizingPeriodWeatherFileDays()
        if internal_name.lower() == "sizingperiod:weatherfileconditiontype":
            return SizingPeriodWeatherFileConditionType()
        if internal_name.lower() == "runperiod":
            return RunPeriod()
        if internal_name.lower() == "runperiod:customrange":
            return RunPeriodCustomRange()
        if internal_name.lower() == "runperiodcontrol:specialdays":
            return RunPeriodControlSpecialDays()
        if internal_name.lower() == "runperiodcontrol:daylightsavingtime":
            return RunPeriodControlDaylightSavingTime()
        if internal_name.lower() == "weatherproperty:skytemperature":
            return WeatherPropertySkyTemperature()
        if internal_name.lower() == "site:weatherstation":
            return SiteWeatherStation()
        if internal_name.lower() == "site:heightvariation":
            return SiteHeightVariation()
        if internal_name.lower() == "site:groundtemperature:buildingsurface":
            return SiteGroundTemperatureBuildingSurface()
        if internal_name.lower() == "site:groundtemperature:fcfactormethod":
            return SiteGroundTemperatureFcfactorMethod()
        if internal_name.lower() == "site:groundtemperature:shallow":
            return SiteGroundTemperatureShallow()
        if internal_name.lower() == "site:groundtemperature:deep":
            return SiteGroundTemperatureDeep()
        if internal_name.lower() == "site:grounddomain":
            return SiteGroundDomain()
        if internal_name.lower() == "site:groundreflectance":
            return SiteGroundReflectance()
        if internal_name.lower() == "site:groundreflectance:snowmodifier":
            return SiteGroundReflectanceSnowModifier()
        if internal_name.lower() == "site:watermainstemperature":
            return SiteWaterMainsTemperature()
        if internal_name.lower() == "site:precipitation":
            return SitePrecipitation()
        if internal_name.lower() == "roofirrigation":
            return RoofIrrigation()
        if internal_name.lower() == "site:solarandvisiblespectrum":
            return SiteSolarAndVisibleSpectrum()
        if internal_name.lower() == "site:spectrumdata":
            return SiteSpectrumData()
        if internal_name.lower() == "scheduletypelimits":
            return ScheduleTypeLimits()
        if internal_name.lower() == "schedule:day:hourly":
            return ScheduleDayHourly()
        if internal_name.lower() == "schedule:day:interval":
            return ScheduleDayInterval()
        if internal_name.lower() == "schedule:day:list":
            return ScheduleDayList()
        if internal_name.lower() == "schedule:week:daily":
            return ScheduleWeekDaily()
        if internal_name.lower() == "schedule:week:compact":
            return ScheduleWeekCompact()
        if internal_name.lower() == "schedule:year":
            return ScheduleYear()
        if internal_name.lower() == "schedule:compact":
            return ScheduleCompact()
        if internal_name.lower() == "schedule:constant":
            return ScheduleConstant()
        if internal_name.lower() == "schedule:file":
            return ScheduleFile()
        if internal_name.lower() == "material":
            return Material()
        if internal_name.lower() == "material:nomass":
            return MaterialNoMass()
        if internal_name.lower() == "material:infraredtransparent":
            return MaterialInfraredTransparent()
        if internal_name.lower() == "material:airgap":
            return MaterialAirGap()
        if internal_name.lower() == "material:roofvegetation":
            return MaterialRoofVegetation()
        if internal_name.lower() == "windowmaterial:simpleglazingsystem":
            return WindowMaterialSimpleGlazingSystem()
        if internal_name.lower() == "windowmaterial:glazing":
            return WindowMaterialGlazing()
        if internal_name.lower(
        ) == "windowmaterial:glazinggroup:thermochromic":
            return WindowMaterialGlazingGroupThermochromic()
        if internal_name.lower(
        ) == "windowmaterial:glazing:refractionextinctionmethod":
            return WindowMaterialGlazingRefractionExtinctionMethod()
        if internal_name.lower() == "windowmaterial:gas":
            return WindowMaterialGas()
        if internal_name.lower() == "windowgap:supportpillar":
            return WindowGapSupportPillar()
        if internal_name.lower() == "windowgap:deflectionstate":
            return WindowGapDeflectionState()
        if internal_name.lower() == "windowmaterial:gasmixture":
            return WindowMaterialGasMixture()
        if internal_name.lower() == "windowmaterial:gap":
            return WindowMaterialGap()
        if internal_name.lower() == "windowmaterial:shade":
            return WindowMaterialShade()
        if internal_name.lower() == "windowmaterial:complexshade":
            return WindowMaterialComplexShade()
        if internal_name.lower() == "windowmaterial:blind":
            return WindowMaterialBlind()
        if internal_name.lower() == "windowmaterial:screen":
            return WindowMaterialScreen()
        if internal_name.lower() == "windowmaterial:shade:equivalentlayer":
            return WindowMaterialShadeEquivalentLayer()
        if internal_name.lower() == "windowmaterial:drape:equivalentlayer":
            return WindowMaterialDrapeEquivalentLayer()
        if internal_name.lower() == "windowmaterial:blind:equivalentlayer":
            return WindowMaterialBlindEquivalentLayer()
        if internal_name.lower() == "windowmaterial:screen:equivalentlayer":
            return WindowMaterialScreenEquivalentLayer()
        if internal_name.lower() == "windowmaterial:glazing:equivalentlayer":
            return WindowMaterialGlazingEquivalentLayer()
        if internal_name.lower() == "construction:windowequivalentlayer":
            return ConstructionWindowEquivalentLayer()
        if internal_name.lower() == "windowmaterial:gap:equivalentlayer":
            return WindowMaterialGapEquivalentLayer()
        if internal_name.lower(
        ) == "materialproperty:moisturepenetrationdepth:settings":
            return MaterialPropertyMoisturePenetrationDepthSettings()
        if internal_name.lower() == "materialproperty:phasechange":
            return MaterialPropertyPhaseChange()
        if internal_name.lower(
        ) == "materialproperty:variablethermalconductivity":
            return MaterialPropertyVariableThermalConductivity()
        if internal_name.lower(
        ) == "materialproperty:heatandmoisturetransfer:settings":
            return MaterialPropertyHeatAndMoistureTransferSettings()
        if internal_name.lower(
        ) == "materialproperty:heatandmoisturetransfer:sorptionisotherm":
            return MaterialPropertyHeatAndMoistureTransferSorptionIsotherm()
        if internal_name.lower(
        ) == "materialproperty:heatandmoisturetransfer:suction":
            return MaterialPropertyHeatAndMoistureTransferSuction()
        if internal_name.lower(
        ) == "materialproperty:heatandmoisturetransfer:redistribution":
            return MaterialPropertyHeatAndMoistureTransferRedistribution()
        if internal_name.lower(
        ) == "materialproperty:heatandmoisturetransfer:diffusion":
            return MaterialPropertyHeatAndMoistureTransferDiffusion()
        if internal_name.lower(
        ) == "materialproperty:heatandmoisturetransfer:thermalconductivity":
            return MaterialPropertyHeatAndMoistureTransferThermalConductivity()
        if internal_name.lower() == "materialproperty:glazingspectraldata":
            return MaterialPropertyGlazingSpectralData()
        if internal_name.lower() == "construction":
            return Construction()
        if internal_name.lower() == "construction:cfactorundergroundwall":
            return ConstructionCfactorUndergroundWall()
        if internal_name.lower() == "construction:ffactorgroundfloor":
            return ConstructionFfactorGroundFloor()
        if internal_name.lower() == "construction:internalsource":
            return ConstructionInternalSource()
        if internal_name.lower() == "windowthermalmodel:params":
            return WindowThermalModelParams()
        if internal_name.lower() == "construction:complexfenestrationstate":
            return ConstructionComplexFenestrationState()
        if internal_name.lower() == "construction:windowdatafile":
            return ConstructionWindowDataFile()
        if internal_name.lower() == "globalgeometryrules":
            return GlobalGeometryRules()
        if internal_name.lower() == "geometrytransform":
            return GeometryTransform()
        if internal_name.lower() == "zone":
            return Zone()
        if internal_name.lower() == "zonelist":
            return ZoneList()
        if internal_name.lower() == "zonegroup":
            return ZoneGroup()
        if internal_name.lower() == "buildingsurface:detailed":
            return BuildingSurfaceDetailed()
        if internal_name.lower() == "wall:detailed":
            return WallDetailed()
        if internal_name.lower() == "roofceiling:detailed":
            return RoofCeilingDetailed()
        if internal_name.lower() == "floor:detailed":
            return FloorDetailed()
        if internal_name.lower() == "wall:exterior":
            return WallExterior()
        if internal_name.lower() == "wall:adiabatic":
            return WallAdiabatic()
        if internal_name.lower() == "wall:underground":
            return WallUnderground()
        if internal_name.lower() == "wall:interzone":
            return WallInterzone()
        if internal_name.lower() == "roof":
            return Roof()
        if internal_name.lower() == "ceiling:adiabatic":
            return CeilingAdiabatic()
        if internal_name.lower() == "ceiling:interzone":
            return CeilingInterzone()
        if internal_name.lower() == "floor:groundcontact":
            return FloorGroundContact()
        if internal_name.lower() == "floor:adiabatic":
            return FloorAdiabatic()
        if internal_name.lower() == "floor:interzone":
            return FloorInterzone()
        if internal_name.lower() == "fenestrationsurface:detailed":
            return FenestrationSurfaceDetailed()
        if internal_name.lower() == "window":
            return Window()
        if internal_name.lower() == "door":
            return Door()
        if internal_name.lower() == "glazeddoor":
            return GlazedDoor()
        if internal_name.lower() == "window:interzone":
            return WindowInterzone()
        if internal_name.lower() == "door:interzone":
            return DoorInterzone()
        if internal_name.lower() == "glazeddoor:interzone":
            return GlazedDoorInterzone()
        if internal_name.lower() == "windowproperty:shadingcontrol":
            return WindowPropertyShadingControl()
        if internal_name.lower() == "windowproperty:frameanddivider":
            return WindowPropertyFrameAndDivider()
        if internal_name.lower() == "windowproperty:airflowcontrol":
            return WindowPropertyAirflowControl()
        if internal_name.lower() == "windowproperty:stormwindow":
            return WindowPropertyStormWindow()
        if internal_name.lower() == "internalmass":
            return InternalMass()
        if internal_name.lower() == "shading:site":
            return ShadingSite()
        if internal_name.lower() == "shading:building":
            return ShadingBuilding()
        if internal_name.lower() == "shading:site:detailed":
            return ShadingSiteDetailed()
        if internal_name.lower() == "shading:building:detailed":
            return ShadingBuildingDetailed()
        if internal_name.lower() == "shading:overhang":
            return ShadingOverhang()
        if internal_name.lower() == "shading:overhang:projection":
            return ShadingOverhangProjection()
        if internal_name.lower() == "shading:fin":
            return ShadingFin()
        if internal_name.lower() == "shading:fin:projection":
            return ShadingFinProjection()
        if internal_name.lower() == "shading:zone:detailed":
            return ShadingZoneDetailed()
        if internal_name.lower() == "shadingproperty:reflectance":
            return ShadingPropertyReflectance()
        if internal_name.lower() == "surfaceproperty:heattransferalgorithm":
            return SurfacePropertyHeatTransferAlgorithm()
        if internal_name.lower(
        ) == "surfaceproperty:heattransferalgorithm:multiplesurface":
            return SurfacePropertyHeatTransferAlgorithmMultipleSurface()
        if internal_name.lower(
        ) == "surfaceproperty:heattransferalgorithm:surfacelist":
            return SurfacePropertyHeatTransferAlgorithmSurfaceList()
        if internal_name.lower(
        ) == "surfaceproperty:heattransferalgorithm:construction":
            return SurfacePropertyHeatTransferAlgorithmConstruction()
        if internal_name.lower() == "surfacecontrol:movableinsulation":
            return SurfaceControlMovableInsulation()
        if internal_name.lower() == "surfaceproperty:othersidecoefficients":
            return SurfacePropertyOtherSideCoefficients()
        if internal_name.lower() == "surfaceproperty:othersideconditionsmodel":
            return SurfacePropertyOtherSideConditionsModel()
        if internal_name.lower(
        ) == "surfaceconvectionalgorithm:inside:adaptivemodelselections":
            return SurfaceConvectionAlgorithmInsideAdaptiveModelSelections()
        if internal_name.lower(
        ) == "surfaceconvectionalgorithm:outside:adaptivemodelselections":
            return SurfaceConvectionAlgorithmOutsideAdaptiveModelSelections()
        if internal_name.lower(
        ) == "surfaceconvectionalgorithm:inside:usercurve":
            return SurfaceConvectionAlgorithmInsideUserCurve()
        if internal_name.lower(
        ) == "surfaceconvectionalgorithm:outside:usercurve":
            return SurfaceConvectionAlgorithmOutsideUserCurve()
        if internal_name.lower() == "surfaceproperty:convectioncoefficients":
            return SurfacePropertyConvectionCoefficients()
        if internal_name.lower(
        ) == "surfaceproperty:convectioncoefficients:multiplesurface":
            return SurfacePropertyConvectionCoefficientsMultipleSurface()
        if internal_name.lower() == "surfaceproperties:vaporcoefficients":
            return SurfacePropertiesVaporCoefficients()
        if internal_name.lower(
        ) == "surfaceproperty:exteriornaturalventedcavity":
            return SurfacePropertyExteriorNaturalVentedCavity()
        if internal_name.lower() == "surfaceproperty:solarincidentinside":
            return SurfacePropertySolarIncidentInside()
        if internal_name.lower(
        ) == "complexfenestrationproperty:solarabsorbedlayers":
            return ComplexFenestrationPropertySolarAbsorbedLayers()
        if internal_name.lower(
        ) == "zoneproperty:userviewfactors:bysurfacename":
            return ZonePropertyUserViewFactorsBySurfaceName()
        if internal_name.lower() == "groundheattransfer:control":
            return GroundHeatTransferControl()
        if internal_name.lower() == "groundheattransfer:slab:materials":
            return GroundHeatTransferSlabMaterials()
        if internal_name.lower() == "groundheattransfer:slab:matlprops":
            return GroundHeatTransferSlabMatlProps()
        if internal_name.lower() == "groundheattransfer:slab:boundconds":
            return GroundHeatTransferSlabBoundConds()
        if internal_name.lower() == "groundheattransfer:slab:bldgprops":
            return GroundHeatTransferSlabBldgProps()
        if internal_name.lower() == "groundheattransfer:slab:insulation":
            return GroundHeatTransferSlabInsulation()
        if internal_name.lower() == "groundheattransfer:slab:equivalentslab":
            return GroundHeatTransferSlabEquivalentSlab()
        if internal_name.lower() == "groundheattransfer:slab:autogrid":
            return GroundHeatTransferSlabAutoGrid()
        if internal_name.lower() == "groundheattransfer:slab:manualgrid":
            return GroundHeatTransferSlabManualGrid()
        if internal_name.lower() == "groundheattransfer:slab:xface":
            return GroundHeatTransferSlabXface()
        if internal_name.lower() == "groundheattransfer:slab:yface":
            return GroundHeatTransferSlabYface()
        if internal_name.lower() == "groundheattransfer:slab:zface":
            return GroundHeatTransferSlabZface()
        if internal_name.lower(
        ) == "groundheattransfer:basement:simparameters":
            return GroundHeatTransferBasementSimParameters()
        if internal_name.lower() == "groundheattransfer:basement:matlprops":
            return GroundHeatTransferBasementMatlProps()
        if internal_name.lower() == "groundheattransfer:basement:insulation":
            return GroundHeatTransferBasementInsulation()
        if internal_name.lower() == "groundheattransfer:basement:surfaceprops":
            return GroundHeatTransferBasementSurfaceProps()
        if internal_name.lower() == "groundheattransfer:basement:bldgdata":
            return GroundHeatTransferBasementBldgData()
        if internal_name.lower() == "groundheattransfer:basement:interior":
            return GroundHeatTransferBasementInterior()
        if internal_name.lower() == "groundheattransfer:basement:combldg":
            return GroundHeatTransferBasementComBldg()
        if internal_name.lower() == "groundheattransfer:basement:equivslab":
            return GroundHeatTransferBasementEquivSlab()
        if internal_name.lower(
        ) == "groundheattransfer:basement:equivautogrid":
            return GroundHeatTransferBasementEquivAutoGrid()
        if internal_name.lower() == "groundheattransfer:basement:autogrid":
            return GroundHeatTransferBasementAutoGrid()
        if internal_name.lower() == "groundheattransfer:basement:manualgrid":
            return GroundHeatTransferBasementManualGrid()
        if internal_name.lower() == "groundheattransfer:basement:xface":
            return GroundHeatTransferBasementXface()
        if internal_name.lower() == "groundheattransfer:basement:yface":
            return GroundHeatTransferBasementYface()
        if internal_name.lower() == "groundheattransfer:basement:zface":
            return GroundHeatTransferBasementZface()
        if internal_name.lower() == "roomairmodeltype":
            return RoomAirModelType()
        if internal_name.lower() == "roomair:temperaturepattern:userdefined":
            return RoomAirTemperaturePatternUserDefined()
        if internal_name.lower(
        ) == "roomair:temperaturepattern:constantgradient":
            return RoomAirTemperaturePatternConstantGradient()
        if internal_name.lower() == "roomair:temperaturepattern:twogradient":
            return RoomAirTemperaturePatternTwoGradient()
        if internal_name.lower(
        ) == "roomair:temperaturepattern:nondimensionalheight":
            return RoomAirTemperaturePatternNondimensionalHeight()
        if internal_name.lower(
        ) == "roomair:temperaturepattern:surfacemapping":
            return RoomAirTemperaturePatternSurfaceMapping()
        if internal_name.lower() == "roomair:node":
            return RoomAirNode()
        if internal_name.lower(
        ) == "roomairsettings:onenodedisplacementventilation":
            return RoomAirSettingsOneNodeDisplacementVentilation()
        if internal_name.lower(
        ) == "roomairsettings:threenodedisplacementventilation":
            return RoomAirSettingsThreeNodeDisplacementVentilation()
        if internal_name.lower() == "roomairsettings:crossventilation":
            return RoomAirSettingsCrossVentilation()
        if internal_name.lower(
        ) == "roomairsettings:underfloorairdistributioninterior":
            return RoomAirSettingsUnderFloorAirDistributionInterior()
        if internal_name.lower(
        ) == "roomairsettings:underfloorairdistributionexterior":
            return RoomAirSettingsUnderFloorAirDistributionExterior()
        if internal_name.lower() == "people":
            return People()
        if internal_name.lower() == "comfortviewfactorangles":
            return ComfortViewFactorAngles()
        if internal_name.lower() == "lights":
            return Lights()
        if internal_name.lower() == "electricequipment":
            return ElectricEquipment()
        if internal_name.lower() == "gasequipment":
            return GasEquipment()
        if internal_name.lower() == "hotwaterequipment":
            return HotWaterEquipment()
        if internal_name.lower() == "steamequipment":
            return SteamEquipment()
        if internal_name.lower() == "otherequipment":
            return OtherEquipment()
        if internal_name.lower(
        ) == "zonebaseboard:outdoortemperaturecontrolled":
            return ZoneBaseboardOutdoorTemperatureControlled()
        if internal_name.lower(
        ) == "zonecontaminantsourceandsink:carbondioxide":
            return ZoneContaminantSourceAndSinkCarbonDioxide()
        if internal_name.lower(
        ) == "zonecontaminantsourceandsink:generic:constant":
            return ZoneContaminantSourceAndSinkGenericConstant()
        if internal_name.lower(
        ) == "surfacecontaminantsourceandsink:generic:pressuredriven":
            return SurfaceContaminantSourceAndSinkGenericPressureDriven()
        if internal_name.lower(
        ) == "zonecontaminantsourceandsink:generic:cutoffmodel":
            return ZoneContaminantSourceAndSinkGenericCutoffModel()
        if internal_name.lower(
        ) == "zonecontaminantsourceandsink:generic:decaysource":
            return ZoneContaminantSourceAndSinkGenericDecaySource()
        if internal_name.lower(
        ) == "surfacecontaminantsourceandsink:generic:boundarylayerdiffusion":
            return SurfaceContaminantSourceAndSinkGenericBoundaryLayerDiffusion()
        if internal_name.lower(
        ) == "surfacecontaminantsourceandsink:generic:depositionvelocitysink":
            return SurfaceContaminantSourceAndSinkGenericDepositionVelocitySink()
        if internal_name.lower(
        ) == "zonecontaminantsourceandsink:generic:depositionratesink":
            return ZoneContaminantSourceAndSinkGenericDepositionRateSink()
        if internal_name.lower() == "daylighting:controls":
            return DaylightingControls()
        if internal_name.lower() == "daylighting:delight:controls":
            return DaylightingDelightControls()
        if internal_name.lower() == "daylighting:delight:referencepoint":
            return DaylightingDelightReferencePoint()
        if internal_name.lower() == "daylighting:delight:complexfenestration":
            return DaylightingDelightComplexFenestration()
        if internal_name.lower() == "daylightingdevice:tubular":
            return DaylightingDeviceTubular()
        if internal_name.lower() == "daylightingdevice:shelf":
            return DaylightingDeviceShelf()
        if internal_name.lower() == "daylightingdevice:lightwell":
            return DaylightingDeviceLightWell()
        if internal_name.lower() == "output:daylightfactors":
            return OutputDaylightFactors()
        if internal_name.lower() == "output:illuminancemap":
            return OutputIlluminanceMap()
        if internal_name.lower() == "outputcontrol:illuminancemap:style":
            return OutputControlIlluminanceMapStyle()
        if internal_name.lower() == "zoneinfiltration:designflowrate":
            return ZoneInfiltrationDesignFlowRate()
        if internal_name.lower() == "zoneinfiltration:effectiveleakagearea":
            return ZoneInfiltrationEffectiveLeakageArea()
        if internal_name.lower() == "zoneinfiltration:flowcoefficient":
            return ZoneInfiltrationFlowCoefficient()
        if internal_name.lower() == "zoneventilation:designflowrate":
            return ZoneVentilationDesignFlowRate()
        if internal_name.lower() == "zoneventilation:windandstackopenarea":
            return ZoneVentilationWindandStackOpenArea()
        if internal_name.lower() == "zoneairbalance:outdoorair":
            return ZoneAirBalanceOutdoorAir()
        if internal_name.lower() == "zonemixing":
            return ZoneMixing()
        if internal_name.lower() == "zonecrossmixing":
            return ZoneCrossMixing()
        if internal_name.lower() == "zonerefrigerationdoormixing":
            return ZoneRefrigerationDoorMixing()
        if internal_name.lower() == "zoneearthtube":
            return ZoneEarthtube()
        if internal_name.lower() == "zonecooltower:shower":
            return ZoneCoolTowerShower()
        if internal_name.lower() == "zonethermalchimney":
            return ZoneThermalChimney()
        if internal_name.lower() == "airflownetwork:simulationcontrol":
            return AirflowNetworkSimulationControl()
        if internal_name.lower() == "airflownetwork:multizone:zone":
            return AirflowNetworkMultiZoneZone()
        if internal_name.lower() == "airflownetwork:multizone:surface":
            return AirflowNetworkMultiZoneSurface()
        if internal_name.lower(
        ) == "airflownetwork:multizone:referencecrackconditions":
            return AirflowNetworkMultiZoneReferenceCrackConditions()
        if internal_name.lower() == "airflownetwork:multizone:surface:crack":
            return AirflowNetworkMultiZoneSurfaceCrack()
        if internal_name.lower(
        ) == "airflownetwork:multizone:surface:effectiveleakagearea":
            return AirflowNetworkMultiZoneSurfaceEffectiveLeakageArea()
        if internal_name.lower(
        ) == "airflownetwork:multizone:component:detailedopening":
            return AirflowNetworkMultiZoneComponentDetailedOpening()
        if internal_name.lower(
        ) == "airflownetwork:multizone:component:simpleopening":
            return AirflowNetworkMultiZoneComponentSimpleOpening()
        if internal_name.lower(
        ) == "airflownetwork:multizone:component:horizontalopening":
            return AirflowNetworkMultiZoneComponentHorizontalOpening()
        if internal_name.lower(
        ) == "airflownetwork:multizone:component:zoneexhaustfan":
            return AirflowNetworkMultiZoneComponentZoneExhaustFan()
        if internal_name.lower() == "airflownetwork:multizone:externalnode":
            return AirflowNetworkMultiZoneExternalNode()
        if internal_name.lower(
        ) == "airflownetwork:multizone:windpressurecoefficientarray":
            return AirflowNetworkMultiZoneWindPressureCoefficientArray()
        if internal_name.lower(
        ) == "airflownetwork:multizone:windpressurecoefficientvalues":
            return AirflowNetworkMultiZoneWindPressureCoefficientValues()
        if internal_name.lower() == "airflownetwork:distribution:node":
            return AirflowNetworkDistributionNode()
        if internal_name.lower(
        ) == "airflownetwork:distribution:component:leak":
            return AirflowNetworkDistributionComponentLeak()
        if internal_name.lower(
        ) == "airflownetwork:distribution:component:leakageratio":
            return AirflowNetworkDistributionComponentLeakageRatio()
        if internal_name.lower(
        ) == "airflownetwork:distribution:component:duct":
            return AirflowNetworkDistributionComponentDuct()
        if internal_name.lower(
        ) == "airflownetwork:distribution:component:fan":
            return AirflowNetworkDistributionComponentFan()
        if internal_name.lower(
        ) == "airflownetwork:distribution:component:coil":
            return AirflowNetworkDistributionComponentCoil()
        if internal_name.lower(
        ) == "airflownetwork:distribution:component:heatexchanger":
            return AirflowNetworkDistributionComponentHeatExchanger()
        if internal_name.lower(
        ) == "airflownetwork:distribution:component:terminalunit":
            return AirflowNetworkDistributionComponentTerminalUnit()
        if internal_name.lower(
        ) == "airflownetwork:distribution:component:constantpressuredrop":
            return AirflowNetworkDistributionComponentConstantPressureDrop()
        if internal_name.lower() == "airflownetwork:distribution:linkage":
            return AirflowNetworkDistributionLinkage()
        if internal_name.lower() == "exterior:lights":
            return ExteriorLights()
        if internal_name.lower() == "exterior:fuelequipment":
            return ExteriorFuelEquipment()
        if internal_name.lower() == "exterior:waterequipment":
            return ExteriorWaterEquipment()
        if internal_name.lower() == "hvactemplate:thermostat":
            return HvactemplateThermostat()
        if internal_name.lower() == "hvactemplate:zone:idealloadsairsystem":
            return HvactemplateZoneIdealLoadsAirSystem()
        if internal_name.lower() == "hvactemplate:zone:baseboardheat":
            return HvactemplateZoneBaseboardHeat()
        if internal_name.lower() == "hvactemplate:zone:fancoil":
            return HvactemplateZoneFanCoil()
        if internal_name.lower() == "hvactemplate:zone:ptac":
            return HvactemplateZonePtac()
        if internal_name.lower() == "hvactemplate:zone:pthp":
            return HvactemplateZonePthp()
        if internal_name.lower() == "hvactemplate:zone:watertoairheatpump":
            return HvactemplateZoneWaterToAirHeatPump()
        if internal_name.lower() == "hvactemplate:zone:vrf":
            return HvactemplateZoneVrf()
        if internal_name.lower() == "hvactemplate:zone:unitary":
            return HvactemplateZoneUnitary()
        if internal_name.lower() == "hvactemplate:zone:vav":
            return HvactemplateZoneVav()
        if internal_name.lower() == "hvactemplate:zone:vav:fanpowered":
            return HvactemplateZoneVavFanPowered()
        if internal_name.lower() == "hvactemplate:zone:vav:heatandcool":
            return HvactemplateZoneVavHeatAndCool()
        if internal_name.lower() == "hvactemplate:zone:constantvolume":
            return HvactemplateZoneConstantVolume()
        if internal_name.lower() == "hvactemplate:zone:dualduct":
            return HvactemplateZoneDualDuct()
        if internal_name.lower() == "hvactemplate:system:vrf":
            return HvactemplateSystemVrf()
        if internal_name.lower() == "hvactemplate:system:unitary":
            return HvactemplateSystemUnitary()
        if internal_name.lower(
        ) == "hvactemplate:system:unitaryheatpump:airtoair":
            return HvactemplateSystemUnitaryHeatPumpAirToAir()
        if internal_name.lower() == "hvactemplate:system:unitarysystem":
            return HvactemplateSystemUnitarySystem()
        if internal_name.lower() == "hvactemplate:system:vav":
            return HvactemplateSystemVav()
        if internal_name.lower() == "hvactemplate:system:packagedvav":
            return HvactemplateSystemPackagedVav()
        if internal_name.lower() == "hvactemplate:system:constantvolume":
            return HvactemplateSystemConstantVolume()
        if internal_name.lower() == "hvactemplate:system:dualduct":
            return HvactemplateSystemDualDuct()
        if internal_name.lower() == "hvactemplate:system:dedicatedoutdoorair":
            return HvactemplateSystemDedicatedOutdoorAir()
        if internal_name.lower() == "hvactemplate:plant:chilledwaterloop":
            return HvactemplatePlantChilledWaterLoop()
        if internal_name.lower() == "hvactemplate:plant:chiller":
            return HvactemplatePlantChiller()
        if internal_name.lower(
        ) == "hvactemplate:plant:chiller:objectreference":
            return HvactemplatePlantChillerObjectReference()
        if internal_name.lower() == "hvactemplate:plant:tower":
            return HvactemplatePlantTower()
        if internal_name.lower() == "hvactemplate:plant:tower:objectreference":
            return HvactemplatePlantTowerObjectReference()
        if internal_name.lower() == "hvactemplate:plant:hotwaterloop":
            return HvactemplatePlantHotWaterLoop()
        if internal_name.lower() == "hvactemplate:plant:boiler":
            return HvactemplatePlantBoiler()
        if internal_name.lower(
        ) == "hvactemplate:plant:boiler:objectreference":
            return HvactemplatePlantBoilerObjectReference()
        if internal_name.lower() == "hvactemplate:plant:mixedwaterloop":
            return HvactemplatePlantMixedWaterLoop()
        if internal_name.lower() == "designspecification:outdoorair":
            return DesignSpecificationOutdoorAir()
        if internal_name.lower() == "designspecification:zoneairdistribution":
            return DesignSpecificationZoneAirDistribution()
        if internal_name.lower() == "sizing:parameters":
            return SizingParameters()
        if internal_name.lower() == "sizing:zone":
            return SizingZone()
        if internal_name.lower() == "designspecification:zonehvac:sizing":
            return DesignSpecificationZoneHvacSizing()
        if internal_name.lower() == "sizing:system":
            return SizingSystem()
        if internal_name.lower() == "sizing:plant":
            return SizingPlant()
        if internal_name.lower() == "outputcontrol:sizing:style":
            return OutputControlSizingStyle()
        if internal_name.lower() == "zonecontrol:humidistat":
            return ZoneControlHumidistat()
        if internal_name.lower() == "zonecontrol:thermostat":
            return ZoneControlThermostat()
        if internal_name.lower(
        ) == "zonecontrol:thermostat:operativetemperature":
            return ZoneControlThermostatOperativeTemperature()
        if internal_name.lower() == "zonecontrol:thermostat:thermalcomfort":
            return ZoneControlThermostatThermalComfort()
        if internal_name.lower(
        ) == "zonecontrol:thermostat:temperatureandhumidity":
            return ZoneControlThermostatTemperatureAndHumidity()
        if internal_name.lower() == "thermostatsetpoint:singleheating":
            return ThermostatSetpointSingleHeating()
        if internal_name.lower() == "thermostatsetpoint:singlecooling":
            return ThermostatSetpointSingleCooling()
        if internal_name.lower(
        ) == "thermostatsetpoint:singleheatingorcooling":
            return ThermostatSetpointSingleHeatingOrCooling()
        if internal_name.lower() == "thermostatsetpoint:dualsetpoint":
            return ThermostatSetpointDualSetpoint()
        if internal_name.lower(
        ) == "thermostatsetpoint:thermalcomfort:fanger:singleheating":
            return ThermostatSetpointThermalComfortFangerSingleHeating()
        if internal_name.lower(
        ) == "thermostatsetpoint:thermalcomfort:fanger:singlecooling":
            return ThermostatSetpointThermalComfortFangerSingleCooling()
        if internal_name.lower(
        ) == "thermostatsetpoint:thermalcomfort:fanger:singleheatingorcooling":
            return ThermostatSetpointThermalComfortFangerSingleHeatingOrCooling()
        if internal_name.lower(
        ) == "thermostatsetpoint:thermalcomfort:fanger:dualsetpoint":
            return ThermostatSetpointThermalComfortFangerDualSetpoint()
        if internal_name.lower(
        ) == "zonecontrol:thermostat:stageddualsetpoint":
            return ZoneControlThermostatStagedDualSetpoint()
        if internal_name.lower() == "zonecontrol:contaminantcontroller":
            return ZoneControlContaminantController()
        if internal_name.lower() == "zonehvac:idealloadsairsystem":
            return ZoneHvacIdealLoadsAirSystem()
        if internal_name.lower() == "zonehvac:fourpipefancoil":
            return ZoneHvacFourPipeFanCoil()
        if internal_name.lower() == "zonehvac:windowairconditioner":
            return ZoneHvacWindowAirConditioner()
        if internal_name.lower() == "zonehvac:packagedterminalairconditioner":
            return ZoneHvacPackagedTerminalAirConditioner()
        if internal_name.lower() == "zonehvac:packagedterminalheatpump":
            return ZoneHvacPackagedTerminalHeatPump()
        if internal_name.lower() == "zonehvac:watertoairheatpump":
            return ZoneHvacWaterToAirHeatPump()
        if internal_name.lower() == "zonehvac:dehumidifier:dx":
            return ZoneHvacDehumidifierDx()
        if internal_name.lower() == "zonehvac:energyrecoveryventilator":
            return ZoneHvacEnergyRecoveryVentilator()
        if internal_name.lower(
        ) == "zonehvac:energyrecoveryventilator:controller":
            return ZoneHvacEnergyRecoveryVentilatorController()
        if internal_name.lower() == "zonehvac:unitventilator":
            return ZoneHvacUnitVentilator()
        if internal_name.lower() == "zonehvac:unitheater":
            return ZoneHvacUnitHeater()
        if internal_name.lower() == "zonehvac:evaporativecoolerunit":
            return ZoneHvacEvaporativeCoolerUnit()
        if internal_name.lower() == "zonehvac:outdoorairunit":
            return ZoneHvacOutdoorAirUnit()
        if internal_name.lower() == "zonehvac:outdoorairunit:equipmentlist":
            return ZoneHvacOutdoorAirUnitEquipmentList()
        if internal_name.lower(
        ) == "zonehvac:terminalunit:variablerefrigerantflow":
            return ZoneHvacTerminalUnitVariableRefrigerantFlow()
        if internal_name.lower(
        ) == "zonehvac:baseboard:radiantconvective:water":
            return ZoneHvacBaseboardRadiantConvectiveWater()
        if internal_name.lower(
        ) == "zonehvac:baseboard:radiantconvective:steam":
            return ZoneHvacBaseboardRadiantConvectiveSteam()
        if internal_name.lower(
        ) == "zonehvac:baseboard:radiantconvective:electric":
            return ZoneHvacBaseboardRadiantConvectiveElectric()
        if internal_name.lower() == "zonehvac:baseboard:convective:water":
            return ZoneHvacBaseboardConvectiveWater()
        if internal_name.lower() == "zonehvac:baseboard:convective:electric":
            return ZoneHvacBaseboardConvectiveElectric()
        if internal_name.lower(
        ) == "zonehvac:lowtemperatureradiant:variableflow":
            return ZoneHvacLowTemperatureRadiantVariableFlow()
        if internal_name.lower(
        ) == "zonehvac:lowtemperatureradiant:constantflow":
            return ZoneHvacLowTemperatureRadiantConstantFlow()
        if internal_name.lower() == "zonehvac:lowtemperatureradiant:electric":
            return ZoneHvacLowTemperatureRadiantElectric()
        if internal_name.lower(
        ) == "zonehvac:lowtemperatureradiant:surfacegroup":
            return ZoneHvacLowTemperatureRadiantSurfaceGroup()
        if internal_name.lower() == "zonehvac:hightemperatureradiant":
            return ZoneHvacHighTemperatureRadiant()
        if internal_name.lower() == "zonehvac:ventilatedslab":
            return ZoneHvacVentilatedSlab()
        if internal_name.lower() == "zonehvac:ventilatedslab:slabgroup":
            return ZoneHvacVentilatedSlabSlabGroup()
        if internal_name.lower() == "airterminal:singleduct:uncontrolled":
            return AirTerminalSingleDuctUncontrolled()
        if internal_name.lower(
        ) == "airterminal:singleduct:constantvolume:reheat":
            return AirTerminalSingleDuctConstantVolumeReheat()
        if internal_name.lower() == "airterminal:singleduct:vav:noreheat":
            return AirTerminalSingleDuctVavNoReheat()
        if internal_name.lower() == "airterminal:singleduct:vav:reheat":
            return AirTerminalSingleDuctVavReheat()
        if internal_name.lower(
        ) == "airterminal:singleduct:vav:reheat:variablespeedfan":
            return AirTerminalSingleDuctVavReheatVariableSpeedFan()
        if internal_name.lower(
        ) == "airterminal:singleduct:vav:heatandcool:noreheat":
            return AirTerminalSingleDuctVavHeatAndCoolNoReheat()
        if internal_name.lower(
        ) == "airterminal:singleduct:vav:heatandcool:reheat":
            return AirTerminalSingleDuctVavHeatAndCoolReheat()
        if internal_name.lower() == "airterminal:singleduct:seriespiu:reheat":
            return AirTerminalSingleDuctSeriesPiuReheat()
        if internal_name.lower(
        ) == "airterminal:singleduct:parallelpiu:reheat":
            return AirTerminalSingleDuctParallelPiuReheat()
        if internal_name.lower(
        ) == "airterminal:singleduct:constantvolume:fourpipeinduction":
            return AirTerminalSingleDuctConstantVolumeFourPipeInduction()
        if internal_name.lower(
        ) == "airterminal:singleduct:constantvolume:cooledbeam":
            return AirTerminalSingleDuctConstantVolumeCooledBeam()
        if internal_name.lower() == "airterminal:singleduct:inletsidemixer":
            return AirTerminalSingleDuctInletSideMixer()
        if internal_name.lower() == "airterminal:singleduct:supplysidemixer":
            return AirTerminalSingleDuctSupplySideMixer()
        if internal_name.lower() == "airterminal:dualduct:constantvolume":
            return AirTerminalDualDuctConstantVolume()
        if internal_name.lower() == "airterminal:dualduct:vav":
            return AirTerminalDualDuctVav()
        if internal_name.lower() == "airterminal:dualduct:vav:outdoorair":
            return AirTerminalDualDuctVavOutdoorAir()
        if internal_name.lower() == "zonehvac:airdistributionunit":
            return ZoneHvacAirDistributionUnit()
        if internal_name.lower() == "zonehvac:equipmentlist":
            return ZoneHvacEquipmentList()
        if internal_name.lower() == "zonehvac:equipmentconnections":
            return ZoneHvacEquipmentConnections()
        if internal_name.lower() == "fan:constantvolume":
            return FanConstantVolume()
        if internal_name.lower() == "fan:variablevolume":
            return FanVariableVolume()
        if internal_name.lower() == "fan:onoff":
            return FanOnOff()
        if internal_name.lower() == "fan:zoneexhaust":
            return FanZoneExhaust()
        if internal_name.lower() == "fanperformance:nightventilation":
            return FanPerformanceNightVentilation()
        if internal_name.lower() == "fan:componentmodel":
            return FanComponentModel()
        if internal_name.lower() == "coil:cooling:water":
            return CoilCoolingWater()
        if internal_name.lower() == "coil:cooling:water:detailedgeometry":
            return CoilCoolingWaterDetailedGeometry()
        if internal_name.lower() == "coil:cooling:dx:singlespeed":
            return CoilCoolingDxSingleSpeed()
        if internal_name.lower() == "coil:cooling:dx:twospeed":
            return CoilCoolingDxTwoSpeed()
        if internal_name.lower() == "coil:cooling:dx:multispeed":
            return CoilCoolingDxMultiSpeed()
        if internal_name.lower() == "coil:cooling:dx:variablespeed":
            return CoilCoolingDxVariableSpeed()
        if internal_name.lower(
        ) == "coil:cooling:dx:twostagewithhumiditycontrolmode":
            return CoilCoolingDxTwoStageWithHumidityControlMode()
        if internal_name.lower() == "coilperformance:dx:cooling":
            return CoilPerformanceDxCooling()
        if internal_name.lower() == "coil:cooling:dx:variablerefrigerantflow":
            return CoilCoolingDxVariableRefrigerantFlow()
        if internal_name.lower() == "coil:heating:dx:variablerefrigerantflow":
            return CoilHeatingDxVariableRefrigerantFlow()
        if internal_name.lower() == "coil:heating:water":
            return CoilHeatingWater()
        if internal_name.lower() == "coil:heating:steam":
            return CoilHeatingSteam()
        if internal_name.lower() == "coil:heating:electric":
            return CoilHeatingElectric()
        if internal_name.lower() == "coil:heating:electric:multistage":
            return CoilHeatingElectricMultiStage()
        if internal_name.lower() == "coil:heating:gas":
            return CoilHeatingGas()
        if internal_name.lower() == "coil:heating:gas:multistage":
            return CoilHeatingGasMultiStage()
        if internal_name.lower() == "coil:heating:desuperheater":
            return CoilHeatingDesuperheater()
        if internal_name.lower() == "coil:heating:dx:singlespeed":
            return CoilHeatingDxSingleSpeed()
        if internal_name.lower() == "coil:heating:dx:multispeed":
            return CoilHeatingDxMultiSpeed()
        if internal_name.lower() == "coil:heating:dx:variablespeed":
            return CoilHeatingDxVariableSpeed()
        if internal_name.lower(
        ) == "coil:cooling:watertoairheatpump:parameterestimation":
            return CoilCoolingWaterToAirHeatPumpParameterEstimation()
        if internal_name.lower(
        ) == "coil:heating:watertoairheatpump:parameterestimation":
            return CoilHeatingWaterToAirHeatPumpParameterEstimation()
        if internal_name.lower(
        ) == "coil:cooling:watertoairheatpump:equationfit":
            return CoilCoolingWaterToAirHeatPumpEquationFit()
        if internal_name.lower(
        ) == "coil:cooling:watertoairheatpump:variablespeedequationfit":
            return CoilCoolingWaterToAirHeatPumpVariableSpeedEquationFit()
        if internal_name.lower(
        ) == "coil:heating:watertoairheatpump:equationfit":
            return CoilHeatingWaterToAirHeatPumpEquationFit()
        if internal_name.lower(
        ) == "coil:heating:watertoairheatpump:variablespeedequationfit":
            return CoilHeatingWaterToAirHeatPumpVariableSpeedEquationFit()
        if internal_name.lower() == "coil:waterheating:airtowaterheatpump":
            return CoilWaterHeatingAirToWaterHeatPump()
        if internal_name.lower() == "coil:waterheating:desuperheater":
            return CoilWaterHeatingDesuperheater()
        if internal_name.lower() == "coilsystem:cooling:dx":
            return CoilSystemCoolingDx()
        if internal_name.lower() == "coilsystem:heating:dx":
            return CoilSystemHeatingDx()
        if internal_name.lower(
        ) == "coilsystem:cooling:water:heatexchangerassisted":
            return CoilSystemCoolingWaterHeatExchangerAssisted()
        if internal_name.lower(
        ) == "coilsystem:cooling:dx:heatexchangerassisted":
            return CoilSystemCoolingDxHeatExchangerAssisted()
        if internal_name.lower(
        ) == "coil:cooling:dx:singlespeed:thermalstorage":
            return CoilCoolingDxSingleSpeedThermalStorage()
        if internal_name.lower() == "evaporativecooler:direct:celdekpad":
            return EvaporativeCoolerDirectCelDekPad()
        if internal_name.lower() == "evaporativecooler:indirect:celdekpad":
            return EvaporativeCoolerIndirectCelDekPad()
        if internal_name.lower() == "evaporativecooler:indirect:wetcoil":
            return EvaporativeCoolerIndirectWetCoil()
        if internal_name.lower(
        ) == "evaporativecooler:indirect:researchspecial":
            return EvaporativeCoolerIndirectResearchSpecial()
        if internal_name.lower() == "evaporativecooler:direct:researchspecial":
            return EvaporativeCoolerDirectResearchSpecial()
        if internal_name.lower() == "humidifier:steam:electric":
            return HumidifierSteamElectric()
        if internal_name.lower() == "dehumidifier:desiccant:nofans":
            return DehumidifierDesiccantNoFans()
        if internal_name.lower() == "dehumidifier:desiccant:system":
            return DehumidifierDesiccantSystem()
        if internal_name.lower() == "heatexchanger:airtoair:flatplate":
            return HeatExchangerAirToAirFlatPlate()
        if internal_name.lower() == "heatexchanger:airtoair:sensibleandlatent":
            return HeatExchangerAirToAirSensibleAndLatent()
        if internal_name.lower() == "heatexchanger:desiccant:balancedflow":
            return HeatExchangerDesiccantBalancedFlow()
        if internal_name.lower(
        ) == "heatexchanger:desiccant:balancedflow:performancedatatype1":
            return HeatExchangerDesiccantBalancedFlowPerformanceDataType1()
        if internal_name.lower() == "airloophvac:unitarysystem":
            return AirLoopHvacUnitarySystem()
        if internal_name.lower(
        ) == "unitarysystemperformance:heatpump:multispeed":
            return UnitarySystemPerformanceHeatPumpMultispeed()
        if internal_name.lower() == "airloophvac:unitary:furnace:heatonly":
            return AirLoopHvacUnitaryFurnaceHeatOnly()
        if internal_name.lower() == "airloophvac:unitary:furnace:heatcool":
            return AirLoopHvacUnitaryFurnaceHeatCool()
        if internal_name.lower() == "airloophvac:unitaryheatonly":
            return AirLoopHvacUnitaryHeatOnly()
        if internal_name.lower() == "airloophvac:unitaryheatcool":
            return AirLoopHvacUnitaryHeatCool()
        if internal_name.lower() == "airloophvac:unitaryheatpump:airtoair":
            return AirLoopHvacUnitaryHeatPumpAirToAir()
        if internal_name.lower() == "airloophvac:unitaryheatpump:watertoair":
            return AirLoopHvacUnitaryHeatPumpWaterToAir()
        if internal_name.lower(
        ) == "airloophvac:unitaryheatcool:vavchangeoverbypass":
            return AirLoopHvacUnitaryHeatCoolVavchangeoverBypass()
        if internal_name.lower(
        ) == "airloophvac:unitaryheatpump:airtoair:multispeed":
            return AirLoopHvacUnitaryHeatPumpAirToAirMultiSpeed()
        if internal_name.lower() == "airconditioner:variablerefrigerantflow":
            return AirConditionerVariableRefrigerantFlow()
        if internal_name.lower() == "zoneterminalunitlist":
            return ZoneTerminalUnitList()
        if internal_name.lower() == "controller:watercoil":
            return ControllerWaterCoil()
        if internal_name.lower() == "controller:outdoorair":
            return ControllerOutdoorAir()
        if internal_name.lower() == "controller:mechanicalventilation":
            return ControllerMechanicalVentilation()
        if internal_name.lower() == "airloophvac:controllerlist":
            return AirLoopHvacControllerList()
        if internal_name.lower() == "airloophvac":
            return AirLoopHvac()
        if internal_name.lower(
        ) == "airloophvac:outdoorairsystem:equipmentlist":
            return AirLoopHvacOutdoorAirSystemEquipmentList()
        if internal_name.lower() == "airloophvac:outdoorairsystem":
            return AirLoopHvacOutdoorAirSystem()
        if internal_name.lower() == "outdoorair:mixer":
            return OutdoorAirMixer()
        if internal_name.lower() == "airloophvac:zonesplitter":
            return AirLoopHvacZoneSplitter()
        if internal_name.lower() == "airloophvac:supplyplenum":
            return AirLoopHvacSupplyPlenum()
        if internal_name.lower() == "airloophvac:supplypath":
            return AirLoopHvacSupplyPath()
        if internal_name.lower() == "airloophvac:zonemixer":
            return AirLoopHvacZoneMixer()
        if internal_name.lower() == "airloophvac:returnplenum":
            return AirLoopHvacReturnPlenum()
        if internal_name.lower() == "airloophvac:returnpath":
            return AirLoopHvacReturnPath()
        if internal_name.lower() == "branch":
            return Branch()
        if internal_name.lower() == "branchlist":
            return BranchList()
        if internal_name.lower() == "connector:splitter":
            return ConnectorSplitter()
        if internal_name.lower() == "connector:mixer":
            return ConnectorMixer()
        if internal_name.lower() == "connectorlist":
            return ConnectorList()
        if internal_name.lower() == "nodelist":
            return NodeList()
        if internal_name.lower() == "outdoorair:node":
            return OutdoorAirNode()
        if internal_name.lower() == "outdoorair:nodelist":
            return OutdoorAirNodeList()
        if internal_name.lower() == "pipe:adiabatic":
            return PipeAdiabatic()
        if internal_name.lower() == "pipe:adiabatic:steam":
            return PipeAdiabaticSteam()
        if internal_name.lower() == "pipe:indoor":
            return PipeIndoor()
        if internal_name.lower() == "pipe:outdoor":
            return PipeOutdoor()
        if internal_name.lower() == "pipe:underground":
            return PipeUnderground()
        if internal_name.lower() == "pipingsystem:underground:domain":
            return PipingSystemUndergroundDomain()
        if internal_name.lower() == "pipingsystem:underground:pipecircuit":
            return PipingSystemUndergroundPipeCircuit()
        if internal_name.lower() == "pipingsystem:underground:pipesegment":
            return PipingSystemUndergroundPipeSegment()
        if internal_name.lower() == "duct":
            return Duct()
        if internal_name.lower() == "pump:variablespeed":
            return PumpVariableSpeed()
        if internal_name.lower() == "pump:constantspeed":
            return PumpConstantSpeed()
        if internal_name.lower() == "pump:variablespeed:condensate":
            return PumpVariableSpeedCondensate()
        if internal_name.lower() == "headeredpumps:constantspeed":
            return HeaderedPumpsConstantSpeed()
        if internal_name.lower() == "headeredpumps:variablespeed":
            return HeaderedPumpsVariableSpeed()
        if internal_name.lower() == "temperingvalve":
            return TemperingValve()
        if internal_name.lower() == "loadprofile:plant":
            return LoadProfilePlant()
        if internal_name.lower() == "solarcollectorperformance:flatplate":
            return SolarCollectorPerformanceFlatPlate()
        if internal_name.lower() == "solarcollector:flatplate:water":
            return SolarCollectorFlatPlateWater()
        if internal_name.lower(
        ) == "solarcollector:flatplate:photovoltaicthermal":
            return SolarCollectorFlatPlatePhotovoltaicThermal()
        if internal_name.lower(
        ) == "solarcollectorperformance:photovoltaicthermal:simple":
            return SolarCollectorPerformancePhotovoltaicThermalSimple()
        if internal_name.lower() == "solarcollector:integralcollectorstorage":
            return SolarCollectorIntegralCollectorStorage()
        if internal_name.lower(
        ) == "solarcollectorperformance:integralcollectorstorage":
            return SolarCollectorPerformanceIntegralCollectorStorage()
        if internal_name.lower() == "solarcollector:unglazedtranspired":
            return SolarCollectorUnglazedTranspired()
        if internal_name.lower(
        ) == "solarcollector:unglazedtranspired:multisystem":
            return SolarCollectorUnglazedTranspiredMultisystem()
        if internal_name.lower() == "boiler:hotwater":
            return BoilerHotWater()
        if internal_name.lower() == "boiler:steam":
            return BoilerSteam()
        if internal_name.lower() == "chiller:electric:eir":
            return ChillerElectricEir()
        if internal_name.lower() == "chiller:electric:reformulatedeir":
            return ChillerElectricReformulatedEir()
        if internal_name.lower() == "chiller:electric":
            return ChillerElectric()
        if internal_name.lower() == "chiller:absorption:indirect":
            return ChillerAbsorptionIndirect()
        if internal_name.lower() == "chiller:absorption":
            return ChillerAbsorption()
        if internal_name.lower() == "chiller:constantcop":
            return ChillerConstantCop()
        if internal_name.lower() == "chiller:enginedriven":
            return ChillerEngineDriven()
        if internal_name.lower() == "chiller:combustionturbine":
            return ChillerCombustionTurbine()
        if internal_name.lower() == "chillerheater:absorption:directfired":
            return ChillerHeaterAbsorptionDirectFired()
        if internal_name.lower() == "chillerheater:absorption:doubleeffect":
            return ChillerHeaterAbsorptionDoubleEffect()
        if internal_name.lower(
        ) == "heatpump:watertowater:equationfit:heating":
            return HeatPumpWaterToWaterEquationFitHeating()
        if internal_name.lower(
        ) == "heatpump:watertowater:equationfit:cooling":
            return HeatPumpWaterToWaterEquationFitCooling()
        if internal_name.lower(
        ) == "heatpump:watertowater:parameterestimation:cooling":
            return HeatPumpWaterToWaterParameterEstimationCooling()
        if internal_name.lower(
        ) == "heatpump:watertowater:parameterestimation:heating":
            return HeatPumpWaterToWaterParameterEstimationHeating()
        if internal_name.lower() == "districtcooling":
            return DistrictCooling()
        if internal_name.lower() == "districtheating":
            return DistrictHeating()
        if internal_name.lower() == "plantcomponent:temperaturesource":
            return PlantComponentTemperatureSource()
        if internal_name.lower() == "centralheatpumpsystem":
            return CentralHeatPumpSystem()
        if internal_name.lower() == "chillerheaterperformance:electric:eir":
            return ChillerHeaterPerformanceElectricEir()
        if internal_name.lower() == "coolingtower:singlespeed":
            return CoolingTowerSingleSpeed()
        if internal_name.lower() == "coolingtower:twospeed":
            return CoolingTowerTwoSpeed()
        if internal_name.lower() == "coolingtower:variablespeed:merkel":
            return CoolingTowerVariableSpeedMerkel()
        if internal_name.lower() == "coolingtower:variablespeed":
            return CoolingTowerVariableSpeed()
        if internal_name.lower() == "coolingtowerperformance:cooltools":
            return CoolingTowerPerformanceCoolTools()
        if internal_name.lower() == "coolingtowerperformance:yorkcalc":
            return CoolingTowerPerformanceYorkCalc()
        if internal_name.lower() == "evaporativefluidcooler:singlespeed":
            return EvaporativeFluidCoolerSingleSpeed()
        if internal_name.lower() == "evaporativefluidcooler:twospeed":
            return EvaporativeFluidCoolerTwoSpeed()
        if internal_name.lower() == "fluidcooler:singlespeed":
            return FluidCoolerSingleSpeed()
        if internal_name.lower() == "fluidcooler:twospeed":
            return FluidCoolerTwoSpeed()
        if internal_name.lower() == "groundheatexchanger:vertical":
            return GroundHeatExchangerVertical()
        if internal_name.lower() == "groundheatexchanger:pond":
            return GroundHeatExchangerPond()
        if internal_name.lower() == "groundheatexchanger:surface":
            return GroundHeatExchangerSurface()
        if internal_name.lower() == "groundheatexchanger:horizontaltrench":
            return GroundHeatExchangerHorizontalTrench()
        if internal_name.lower() == "heatexchanger:fluidtofluid":
            return HeatExchangerFluidToFluid()
        if internal_name.lower() == "waterheater:mixed":
            return WaterHeaterMixed()
        if internal_name.lower() == "waterheater:stratified":
            return WaterHeaterStratified()
        if internal_name.lower() == "waterheater:sizing":
            return WaterHeaterSizing()
        if internal_name.lower() == "waterheater:heatpump":
            return WaterHeaterHeatPump()
        if internal_name.lower() == "thermalstorage:ice:simple":
            return ThermalStorageIceSimple()
        if internal_name.lower() == "thermalstorage:ice:detailed":
            return ThermalStorageIceDetailed()
        if internal_name.lower() == "thermalstorage:chilledwater:mixed":
            return ThermalStorageChilledWaterMixed()
        if internal_name.lower() == "thermalstorage:chilledwater:stratified":
            return ThermalStorageChilledWaterStratified()
        if internal_name.lower() == "plantloop":
            return PlantLoop()
        if internal_name.lower() == "condenserloop":
            return CondenserLoop()
        if internal_name.lower() == "plantequipmentlist":
            return PlantEquipmentList()
        if internal_name.lower() == "condenserequipmentlist":
            return CondenserEquipmentList()
        if internal_name.lower() == "plantequipmentoperation:uncontrolled":
            return PlantEquipmentOperationUncontrolled()
        if internal_name.lower() == "plantequipmentoperation:coolingload":
            return PlantEquipmentOperationCoolingLoad()
        if internal_name.lower() == "plantequipmentoperation:heatingload":
            return PlantEquipmentOperationHeatingLoad()
        if internal_name.lower() == "plantequipmentoperation:outdoordrybulb":
            return PlantEquipmentOperationOutdoorDryBulb()
        if internal_name.lower() == "plantequipmentoperation:outdoorwetbulb":
            return PlantEquipmentOperationOutdoorWetBulb()
        if internal_name.lower(
        ) == "plantequipmentoperation:outdoorrelativehumidity":
            return PlantEquipmentOperationOutdoorRelativeHumidity()
        if internal_name.lower() == "plantequipmentoperation:outdoordewpoint":
            return PlantEquipmentOperationOutdoorDewpoint()
        if internal_name.lower(
        ) == "plantequipmentoperation:componentsetpoint":
            return PlantEquipmentOperationComponentSetpoint()
        if internal_name.lower(
        ) == "plantequipmentoperation:outdoordrybulbdifference":
            return PlantEquipmentOperationOutdoorDryBulbDifference()
        if internal_name.lower(
        ) == "plantequipmentoperation:outdoorwetbulbdifference":
            return PlantEquipmentOperationOutdoorWetBulbDifference()
        if internal_name.lower(
        ) == "plantequipmentoperation:outdoordewpointdifference":
            return PlantEquipmentOperationOutdoorDewpointDifference()
        if internal_name.lower() == "plantequipmentoperationschemes":
            return PlantEquipmentOperationSchemes()
        if internal_name.lower() == "condenserequipmentoperationschemes":
            return CondenserEquipmentOperationSchemes()
        if internal_name.lower() == "energymanagementsystem:sensor":
            return EnergyManagementSystemSensor()
        if internal_name.lower() == "energymanagementsystem:actuator":
            return EnergyManagementSystemActuator()
        if internal_name.lower(
        ) == "energymanagementsystem:programcallingmanager":
            return EnergyManagementSystemProgramCallingManager()
        if internal_name.lower() == "energymanagementsystem:program":
            return EnergyManagementSystemProgram()
        if internal_name.lower() == "energymanagementsystem:subroutine":
            return EnergyManagementSystemSubroutine()
        if internal_name.lower() == "energymanagementsystem:globalvariable":
            return EnergyManagementSystemGlobalVariable()
        if internal_name.lower() == "energymanagementsystem:outputvariable":
            return EnergyManagementSystemOutputVariable()
        if internal_name.lower(
        ) == "energymanagementsystem:meteredoutputvariable":
            return EnergyManagementSystemMeteredOutputVariable()
        if internal_name.lower() == "energymanagementsystem:trendvariable":
            return EnergyManagementSystemTrendVariable()
        if internal_name.lower() == "energymanagementsystem:internalvariable":
            return EnergyManagementSystemInternalVariable()
        if internal_name.lower(
        ) == "energymanagementsystem:curveortableindexvariable":
            return EnergyManagementSystemCurveOrTableIndexVariable()
        if internal_name.lower(
        ) == "energymanagementsystem:constructionindexvariable":
            return EnergyManagementSystemConstructionIndexVariable()
        if internal_name.lower() == "externalinterface":
            return ExternalInterface()
        if internal_name.lower() == "externalinterface:schedule":
            return ExternalInterfaceSchedule()
        if internal_name.lower() == "externalinterface:variable":
            return ExternalInterfaceVariable()
        if internal_name.lower() == "externalinterface:actuator":
            return ExternalInterfaceActuator()
        if internal_name.lower(
        ) == "externalinterface:functionalmockupunitimport":
            return ExternalInterfaceFunctionalMockupUnitImport()
        if internal_name.lower(
        ) == "externalinterface:functionalmockupunitimport:from:variable":
            return ExternalInterfaceFunctionalMockupUnitImportFromVariable()
        if internal_name.lower(
        ) == "externalinterface:functionalmockupunitimport:to:schedule":
            return ExternalInterfaceFunctionalMockupUnitImportToSchedule()
        if internal_name.lower(
        ) == "externalinterface:functionalmockupunitimport:to:actuator":
            return ExternalInterfaceFunctionalMockupUnitImportToActuator()
        if internal_name.lower(
        ) == "externalinterface:functionalmockupunitimport:to:variable":
            return ExternalInterfaceFunctionalMockupUnitImportToVariable()
        if internal_name.lower(
        ) == "externalinterface:functionalmockupunitexport:from:variable":
            return ExternalInterfaceFunctionalMockupUnitExportFromVariable()
        if internal_name.lower(
        ) == "externalinterface:functionalmockupunitexport:to:schedule":
            return ExternalInterfaceFunctionalMockupUnitExportToSchedule()
        if internal_name.lower(
        ) == "externalinterface:functionalmockupunitexport:to:actuator":
            return ExternalInterfaceFunctionalMockupUnitExportToActuator()
        if internal_name.lower(
        ) == "externalinterface:functionalmockupunitexport:to:variable":
            return ExternalInterfaceFunctionalMockupUnitExportToVariable()
        if internal_name.lower() == "zonehvac:forcedair:userdefined":
            return ZoneHvacForcedAirUserDefined()
        if internal_name.lower() == "airterminal:singleduct:userdefined":
            return AirTerminalSingleDuctUserDefined()
        if internal_name.lower() == "coil:userdefined":
            return CoilUserDefined()
        if internal_name.lower() == "plantcomponent:userdefined":
            return PlantComponentUserDefined()
        if internal_name.lower() == "plantequipmentoperation:userdefined":
            return PlantEquipmentOperationUserDefined()
        if internal_name.lower() == "availabilitymanager:scheduled":
            return AvailabilityManagerScheduled()
        if internal_name.lower() == "availabilitymanager:scheduledon":
            return AvailabilityManagerScheduledOn()
        if internal_name.lower() == "availabilitymanager:scheduledoff":
            return AvailabilityManagerScheduledOff()
        if internal_name.lower() == "availabilitymanager:optimumstart":
            return AvailabilityManagerOptimumStart()
        if internal_name.lower() == "availabilitymanager:nightcycle":
            return AvailabilityManagerNightCycle()
        if internal_name.lower(
        ) == "availabilitymanager:differentialthermostat":
            return AvailabilityManagerDifferentialThermostat()
        if internal_name.lower(
        ) == "availabilitymanager:hightemperatureturnoff":
            return AvailabilityManagerHighTemperatureTurnOff()
        if internal_name.lower(
        ) == "availabilitymanager:hightemperatureturnon":
            return AvailabilityManagerHighTemperatureTurnOn()
        if internal_name.lower(
        ) == "availabilitymanager:lowtemperatureturnoff":
            return AvailabilityManagerLowTemperatureTurnOff()
        if internal_name.lower() == "availabilitymanager:lowtemperatureturnon":
            return AvailabilityManagerLowTemperatureTurnOn()
        if internal_name.lower() == "availabilitymanager:nightventilation":
            return AvailabilityManagerNightVentilation()
        if internal_name.lower() == "availabilitymanager:hybridventilation":
            return AvailabilityManagerHybridVentilation()
        if internal_name.lower() == "availabilitymanagerassignmentlist":
            return AvailabilityManagerAssignmentList()
        if internal_name.lower() == "setpointmanager:scheduled":
            return SetpointManagerScheduled()
        if internal_name.lower() == "setpointmanager:scheduled:dualsetpoint":
            return SetpointManagerScheduledDualSetpoint()
        if internal_name.lower() == "setpointmanager:outdoorairreset":
            return SetpointManagerOutdoorAirReset()
        if internal_name.lower() == "setpointmanager:singlezone:reheat":
            return SetpointManagerSingleZoneReheat()
        if internal_name.lower() == "setpointmanager:singlezone:heating":
            return SetpointManagerSingleZoneHeating()
        if internal_name.lower() == "setpointmanager:singlezone:cooling":
            return SetpointManagerSingleZoneCooling()
        if internal_name.lower(
        ) == "setpointmanager:singlezone:humidity:minimum":
            return SetpointManagerSingleZoneHumidityMinimum()
        if internal_name.lower(
        ) == "setpointmanager:singlezone:humidity:maximum":
            return SetpointManagerSingleZoneHumidityMaximum()
        if internal_name.lower() == "setpointmanager:mixedair":
            return SetpointManagerMixedAir()
        if internal_name.lower() == "setpointmanager:outdoorairpretreat":
            return SetpointManagerOutdoorAirPretreat()
        if internal_name.lower() == "setpointmanager:warmest":
            return SetpointManagerWarmest()
        if internal_name.lower() == "setpointmanager:coldest":
            return SetpointManagerColdest()
        if internal_name.lower() == "setpointmanager:returnairbypassflow":
            return SetpointManagerReturnAirBypassFlow()
        if internal_name.lower() == "setpointmanager:warmesttemperatureflow":
            return SetpointManagerWarmestTemperatureFlow()
        if internal_name.lower(
        ) == "setpointmanager:multizone:heating:average":
            return SetpointManagerMultiZoneHeatingAverage()
        if internal_name.lower(
        ) == "setpointmanager:multizone:cooling:average":
            return SetpointManagerMultiZoneCoolingAverage()
        if internal_name.lower(
        ) == "setpointmanager:multizone:minimumhumidity:average":
            return SetpointManagerMultiZoneMinimumHumidityAverage()
        if internal_name.lower(
        ) == "setpointmanager:multizone:maximumhumidity:average":
            return SetpointManagerMultiZoneMaximumHumidityAverage()
        if internal_name.lower(
        ) == "setpointmanager:multizone:humidity:minimum":
            return SetpointManagerMultiZoneHumidityMinimum()
        if internal_name.lower(
        ) == "setpointmanager:multizone:humidity:maximum":
            return SetpointManagerMultiZoneHumidityMaximum()
        if internal_name.lower(
        ) == "setpointmanager:followoutdoorairtemperature":
            return SetpointManagerFollowOutdoorAirTemperature()
        if internal_name.lower(
        ) == "setpointmanager:followsystemnodetemperature":
            return SetpointManagerFollowSystemNodeTemperature()
        if internal_name.lower() == "setpointmanager:followgroundtemperature":
            return SetpointManagerFollowGroundTemperature()
        if internal_name.lower() == "setpointmanager:condenserenteringreset":
            return SetpointManagerCondenserEnteringReset()
        if internal_name.lower(
        ) == "setpointmanager:condenserenteringreset:ideal":
            return SetpointManagerCondenserEnteringResetIdeal()
        if internal_name.lower(
        ) == "setpointmanager:singlezone:onestagecooling":
            return SetpointManagerSingleZoneOneStageCooling()
        if internal_name.lower(
        ) == "setpointmanager:singlezone:onestageheating":
            return SetpointManagerSingleZoneOneStageHeating()
        if internal_name.lower() == "refrigeration:case":
            return RefrigerationCase()
        if internal_name.lower() == "refrigeration:compressorrack":
            return RefrigerationCompressorRack()
        if internal_name.lower() == "refrigeration:caseandwalkinlist":
            return RefrigerationCaseAndWalkInList()
        if internal_name.lower() == "refrigeration:condenser:aircooled":
            return RefrigerationCondenserAirCooled()
        if internal_name.lower(
        ) == "refrigeration:condenser:evaporativecooled":
            return RefrigerationCondenserEvaporativeCooled()
        if internal_name.lower() == "refrigeration:condenser:watercooled":
            return RefrigerationCondenserWaterCooled()
        if internal_name.lower() == "refrigeration:condenser:cascade":
            return RefrigerationCondenserCascade()
        if internal_name.lower() == "refrigeration:gascooler:aircooled":
            return RefrigerationGasCoolerAirCooled()
        if internal_name.lower() == "refrigeration:transferloadlist":
            return RefrigerationTransferLoadList()
        if internal_name.lower() == "refrigeration:subcooler":
            return RefrigerationSubcooler()
        if internal_name.lower() == "refrigeration:compressor":
            return RefrigerationCompressor()
        if internal_name.lower() == "refrigeration:compressorlist":
            return RefrigerationCompressorList()
        if internal_name.lower() == "refrigeration:system":
            return RefrigerationSystem()
        if internal_name.lower() == "refrigeration:transcriticalsystem":
            return RefrigerationTranscriticalSystem()
        if internal_name.lower() == "refrigeration:secondarysystem":
            return RefrigerationSecondarySystem()
        if internal_name.lower() == "refrigeration:walkin":
            return RefrigerationWalkIn()
        if internal_name.lower() == "refrigeration:airchiller":
            return RefrigerationAirChiller()
        if internal_name.lower() == "zonehvac:refrigerationchillerset":
            return ZoneHvacRefrigerationChillerSet()
        if internal_name.lower() == "demandmanagerassignmentlist":
            return DemandManagerAssignmentList()
        if internal_name.lower() == "demandmanager:exteriorlights":
            return DemandManagerExteriorLights()
        if internal_name.lower() == "demandmanager:lights":
            return DemandManagerLights()
        if internal_name.lower() == "demandmanager:electricequipment":
            return DemandManagerElectricEquipment()
        if internal_name.lower() == "demandmanager:thermostats":
            return DemandManagerThermostats()
        if internal_name.lower() == "generator:internalcombustionengine":
            return GeneratorInternalCombustionEngine()
        if internal_name.lower() == "generator:combustionturbine":
            return GeneratorCombustionTurbine()
        if internal_name.lower() == "generator:microturbine":
            return GeneratorMicroTurbine()
        if internal_name.lower() == "generator:photovoltaic":
            return GeneratorPhotovoltaic()
        if internal_name.lower() == "photovoltaicperformance:simple":
            return PhotovoltaicPerformanceSimple()
        if internal_name.lower(
        ) == "photovoltaicperformance:equivalentone-diode":
            return PhotovoltaicPerformanceEquivalentOneDiode()
        if internal_name.lower() == "photovoltaicperformance:sandia":
            return PhotovoltaicPerformanceSandia()
        if internal_name.lower() == "generator:fuelcell":
            return GeneratorFuelCell()
        if internal_name.lower() == "generator:fuelcell:powermodule":
            return GeneratorFuelCellPowerModule()
        if internal_name.lower() == "generator:fuelcell:airsupply":
            return GeneratorFuelCellAirSupply()
        if internal_name.lower() == "generator:fuelcell:watersupply":
            return GeneratorFuelCellWaterSupply()
        if internal_name.lower() == "generator:fuelcell:auxiliaryheater":
            return GeneratorFuelCellAuxiliaryHeater()
        if internal_name.lower(
        ) == "generator:fuelcell:exhaustgastowaterheatexchanger":
            return GeneratorFuelCellExhaustGasToWaterHeatExchanger()
        if internal_name.lower() == "generator:fuelcell:electricalstorage":
            return GeneratorFuelCellElectricalStorage()
        if internal_name.lower() == "generator:fuelcell:inverter":
            return GeneratorFuelCellInverter()
        if internal_name.lower() == "generator:fuelcell:stackcooler":
            return GeneratorFuelCellStackCooler()
        if internal_name.lower() == "generator:microchp":
            return GeneratorMicroChp()
        if internal_name.lower(
        ) == "generator:microchp:nonnormalizedparameters":
            return GeneratorMicroChpNonNormalizedParameters()
        if internal_name.lower() == "generator:fuelsupply":
            return GeneratorFuelSupply()
        if internal_name.lower() == "generator:windturbine":
            return GeneratorWindTurbine()
        if internal_name.lower() == "electricloadcenter:generators":
            return ElectricLoadCenterGenerators()
        if internal_name.lower() == "electricloadcenter:inverter:simple":
            return ElectricLoadCenterInverterSimple()
        if internal_name.lower(
        ) == "electricloadcenter:inverter:functionofpower":
            return ElectricLoadCenterInverterFunctionOfPower()
        if internal_name.lower() == "electricloadcenter:inverter:lookuptable":
            return ElectricLoadCenterInverterLookUpTable()
        if internal_name.lower() == "electricloadcenter:storage:simple":
            return ElectricLoadCenterStorageSimple()
        if internal_name.lower() == "electricloadcenter:storage:battery":
            return ElectricLoadCenterStorageBattery()
        if internal_name.lower() == "electricloadcenter:transformer":
            return ElectricLoadCenterTransformer()
        if internal_name.lower() == "electricloadcenter:distribution":
            return ElectricLoadCenterDistribution()
        if internal_name.lower() == "wateruse:equipment":
            return WaterUseEquipment()
        if internal_name.lower() == "wateruse:connections":
            return WaterUseConnections()
        if internal_name.lower() == "wateruse:storage":
            return WaterUseStorage()
        if internal_name.lower() == "wateruse:well":
            return WaterUseWell()
        if internal_name.lower() == "wateruse:raincollector":
            return WaterUseRainCollector()
        if internal_name.lower(
        ) == "faultmodel:temperaturesensoroffset:outdoorair":
            return FaultModelTemperatureSensorOffsetOutdoorAir()
        if internal_name.lower(
        ) == "faultmodel:humiditysensoroffset:outdoorair":
            return FaultModelHumiditySensorOffsetOutdoorAir()
        if internal_name.lower(
        ) == "faultmodel:enthalpysensoroffset:outdoorair":
            return FaultModelEnthalpySensorOffsetOutdoorAir()
        if internal_name.lower(
        ) == "faultmodel:pressuresensoroffset:outdoorair":
            return FaultModelPressureSensorOffsetOutdoorAir()
        if internal_name.lower(
        ) == "faultmodel:temperaturesensoroffset:returnair":
            return FaultModelTemperatureSensorOffsetReturnAir()
        if internal_name.lower(
        ) == "faultmodel:enthalpysensoroffset:returnair":
            return FaultModelEnthalpySensorOffsetReturnAir()
        if internal_name.lower() == "faultmodel:fouling:coil":
            return FaultModelFoulingCoil()
        if internal_name.lower() == "matrix:twodimension":
            return MatrixTwoDimension()
        if internal_name.lower() == "curve:linear":
            return CurveLinear()
        if internal_name.lower() == "curve:quadlinear":
            return CurveQuadLinear()
        if internal_name.lower() == "curve:quadratic":
            return CurveQuadratic()
        if internal_name.lower() == "curve:cubic":
            return CurveCubic()
        if internal_name.lower() == "curve:quartic":
            return CurveQuartic()
        if internal_name.lower() == "curve:exponent":
            return CurveExponent()
        if internal_name.lower() == "curve:bicubic":
            return CurveBicubic()
        if internal_name.lower() == "curve:biquadratic":
            return CurveBiquadratic()
        if internal_name.lower() == "curve:quadraticlinear":
            return CurveQuadraticLinear()
        if internal_name.lower() == "curve:triquadratic":
            return CurveTriquadratic()
        if internal_name.lower() == "curve:functional:pressuredrop":
            return CurveFunctionalPressureDrop()
        if internal_name.lower() == "curve:fanpressurerise":
            return CurveFanPressureRise()
        if internal_name.lower() == "curve:exponentialskewnormal":
            return CurveExponentialSkewNormal()
        if internal_name.lower() == "curve:sigmoid":
            return CurveSigmoid()
        if internal_name.lower() == "curve:rectangularhyperbola1":
            return CurveRectangularHyperbola1()
        if internal_name.lower() == "curve:rectangularhyperbola2":
            return CurveRectangularHyperbola2()
        if internal_name.lower() == "curve:exponentialdecay":
            return CurveExponentialDecay()
        if internal_name.lower() == "curve:doubleexponentialdecay":
            return CurveDoubleExponentialDecay()
        if internal_name.lower() == "table:oneindependentvariable":
            return TableOneIndependentVariable()
        if internal_name.lower() == "table:twoindependentvariables":
            return TableTwoIndependentVariables()
        if internal_name.lower() == "table:multivariablelookup":
            return TableMultiVariableLookup()
        if internal_name.lower() == "fluidproperties:name":
            return FluidPropertiesName()
        if internal_name.lower() == "fluidproperties:glycolconcentration":
            return FluidPropertiesGlycolConcentration()
        if internal_name.lower() == "fluidproperties:temperatures":
            return FluidPropertiesTemperatures()
        if internal_name.lower() == "fluidproperties:saturated":
            return FluidPropertiesSaturated()
        if internal_name.lower() == "fluidproperties:superheated":
            return FluidPropertiesSuperheated()
        if internal_name.lower() == "fluidproperties:concentration":
            return FluidPropertiesConcentration()
        if internal_name.lower() == "currencytype":
            return CurrencyType()
        if internal_name.lower() == "componentcost:adjustments":
            return ComponentCostAdjustments()
        if internal_name.lower() == "componentcost:reference":
            return ComponentCostReference()
        if internal_name.lower() == "componentcost:lineitem":
            return ComponentCostLineItem()
        if internal_name.lower() == "utilitycost:tariff":
            return UtilityCostTariff()
        if internal_name.lower() == "utilitycost:qualify":
            return UtilityCostQualify()
        if internal_name.lower() == "utilitycost:charge:simple":
            return UtilityCostChargeSimple()
        if internal_name.lower() == "utilitycost:charge:block":
            return UtilityCostChargeBlock()
        if internal_name.lower() == "utilitycost:ratchet":
            return UtilityCostRatchet()
        if internal_name.lower() == "utilitycost:variable":
            return UtilityCostVariable()
        if internal_name.lower() == "utilitycost:computation":
            return UtilityCostComputation()
        if internal_name.lower() == "lifecyclecost:parameters":
            return LifeCycleCostParameters()
        if internal_name.lower() == "lifecyclecost:recurringcosts":
            return LifeCycleCostRecurringCosts()
        if internal_name.lower() == "lifecyclecost:nonrecurringcost":
            return LifeCycleCostNonrecurringCost()
        if internal_name.lower() == "lifecyclecost:usepriceescalation":
            return LifeCycleCostUsePriceEscalation()
        if internal_name.lower() == "lifecyclecost:useadjustment":
            return LifeCycleCostUseAdjustment()
        if internal_name.lower() == "parametric:setvalueforrun":
            return ParametricSetValueForRun()
        if internal_name.lower() == "parametric:logic":
            return ParametricLogic()
        if internal_name.lower() == "parametric:runcontrol":
            return ParametricRunControl()
        if internal_name.lower() == "parametric:filenamesuffix":
            return ParametricFileNameSuffix()
        if internal_name.lower() == "output:variabledictionary":
            return OutputVariableDictionary()
        if internal_name.lower() == "output:surfaces:list":
            return OutputSurfacesList()
        if internal_name.lower() == "output:surfaces:drawing":
            return OutputSurfacesDrawing()
        if internal_name.lower() == "output:schedules":
            return OutputSchedules()
        if internal_name.lower() == "output:constructions":
            return OutputConstructions()
        if internal_name.lower() == "output:energymanagementsystem":
            return OutputEnergyManagementSystem()
        if internal_name.lower() == "outputcontrol:surfacecolorscheme":
            return OutputControlSurfaceColorScheme()
        if internal_name.lower() == "output:table:summaryreports":
            return OutputTableSummaryReports()
        if internal_name.lower() == "output:table:timebins":
            return OutputTableTimeBins()
        if internal_name.lower() == "output:table:monthly":
            return OutputTableMonthly()
        if internal_name.lower() == "outputcontrol:table:style":
            return OutputControlTableStyle()
        if internal_name.lower() == "outputcontrol:reportingtolerances":
            return OutputControlReportingTolerances()
        if internal_name.lower() == "output:variable":
            return OutputVariable()
        if internal_name.lower() == "output:meter":
            return OutputMeter()
        if internal_name.lower() == "output:meter:meterfileonly":
            return OutputMeterMeterFileOnly()
        if internal_name.lower() == "output:meter:cumulative":
            return OutputMeterCumulative()
        if internal_name.lower() == "output:meter:cumulative:meterfileonly":
            return OutputMeterCumulativeMeterFileOnly()
        if internal_name.lower() == "meter:custom":
            return MeterCustom()
        if internal_name.lower() == "meter:customdecrement":
            return MeterCustomDecrement()
        if internal_name.lower() == "output:sqlite":
            return OutputSqlite()
        if internal_name.lower() == "output:environmentalimpactfactors":
            return OutputEnvironmentalImpactFactors()
        if internal_name.lower() == "environmentalimpactfactors":
            return EnvironmentalImpactFactors()
        if internal_name.lower() == "fuelfactors":
            return FuelFactors()
        if internal_name.lower() == "output:diagnostics":
            return OutputDiagnostics()
        if internal_name.lower() == "output:debuggingdata":
            return OutputDebuggingData()
        if internal_name.lower() == "output:preprocessormessage":
            return OutputPreprocessorMessage()
        raise ValueError(
            "No DataDictionary known for {}".format(internal_name))

    def __getitem__(self, val):
        if isinstance(val, six.string_types):
            group = self._create_datadict(val).schema['group']
            if group not in self._data:
                self._data[group] = OrderedDict()

            lower_name = val.lower()
            if lower_name not in self._data[group]:
                self._data[group][lower_name] = []

            return self._data[group][lower_name]

        elif isinstance(val, int):
            i = 0
            for group in self._data:
                for key in self._data[group]:
                    for obj in self._data[group][key]:
                        if i == val:
                            return obj
                        i += 1
        else:
            raise TypeError("Wrong type {} for IDF".format(type(val)))

    def __len__(self):
        count = 0
        for group in self._data:
            for key in self._data[group]:
                count += len(self._data[group][key])
        return count

    def __iter__(self):
        for group in self._data:
            for key in self._data[group]:
                for obj in self._data[group][key]:
                    yield obj

    def __contains__(self, key):
        key_lower = key.lower()
        for group in self._data:
            if key_lower in self._data[group]:
                if len(self._data[group][key_lower]) > 0:
                    return True
                break
        return False

    def keys(self):
        keys = []
        for group in self._data:
            for key in self._data[group]:
                if len(self._data[group][key]) > 0:
                    keys.append(key)
        return keys
