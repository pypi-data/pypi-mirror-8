""" Data objects in group "Compliance Objects"
"""

from collections import OrderedDict
import logging
from pyidf.helper import DataObject

logger = logging.getLogger("pyidf")
logger.addHandler(logging.NullHandler())



class ComplianceBuilding(DataObject):

    """ Corresponds to IDD object `Compliance:Building`
        Building level inputs related to compliance to building standards, building codes, and beyond energy code programs.
    """
    schema = {'min-fields': 1,
              'name': u'Compliance:Building',
              'pyname': u'ComplianceBuilding',
              'format': None,
              'fields': OrderedDict([(u'building rotation for appendix g',
                                      {'name': u'Building Rotation for Appendix G',
                                       'pyname': u'building_rotation_for_appendix_g',
                                       'default': 0.0,
                                       'required-field': False,
                                       'autosizable': False,
                                       'autocalculatable': False,
                                       'type': u'real',
                                       'unit': u'deg'})]),
              'extensible-fields': OrderedDict(),
              'unique-object': True,
              'required-object': False,
              'group': u'Compliance Objects'}

    @property
    def building_rotation_for_appendix_g(self):
        """Get building_rotation_for_appendix_g.

        Returns:
            float: the value of `building_rotation_for_appendix_g` or None if not set

        """
        return self["Building Rotation for Appendix G"]

    @building_rotation_for_appendix_g.setter
    def building_rotation_for_appendix_g(self, value=None):
        """  Corresponds to IDD field `Building Rotation for Appendix G`
        Additional degrees of rotation to be used with the requirement in ASHRAE Standard 90.1 Appendix G
        that states that the baseline building should be rotated in four directions.

        Args:
            value (float): value for IDD Field `Building Rotation for Appendix G`
                Units: deg
                if `value` is None it will not be checked against the
                specification and is assumed to be a missing value

        Raises:
            ValueError: if `value` is not a valid value
        """
        self["Building Rotation for Appendix G"] = value


