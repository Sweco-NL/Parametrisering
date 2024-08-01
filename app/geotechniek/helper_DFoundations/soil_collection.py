from app.helper.utils import DeltaresReader
import re

class SoilCollection:
    def __init__(self, content):
        self._content = DeltaresReader(content).extract_first("SOIL COLLECTION")
        self._soil_list = [Soil(soil_str) for soil_str in DeltaresReader(content).extract_all("SOIL")]
        self._number_of_soils = len(self._soil_list)
    @property
    def content(self):
        return self._content
    @property
    def soil_list(self):
        return self._soil_list

    @property
    def number_of_soils(self):
        return self._number_of_soils

class Soil:
    def __init__(self, soil_content: str):
        self._content = soil_content
        self._name                  = soil_content.splitlines()[1]
        self._soil_gam_dry          = float(re.search("SoilGamDry=(\S+)",soil_content).groups()[0])
        self._soil_gam_wet          = float(re.search("SoilGamWet=(\S+)",soil_content).groups()[0])
        self._soil_cohesion         = float(re.search("SoilCohesion=(\S+)",soil_content).groups()[0])
        self._soil_phi              = float(re.search("SoilPhi=(\S+)",soil_content).groups()[0])

    @property
    def content(self):
        return self._content

# define parameters as function of class
    @property
    def name(self):
        return self._name

    @property
    def soil_gam_dry(self):
        return self._soil_gam_dry

    @property
    def soil_gam_wet(self):
        return self._soil_gam_wet

    @property
    def soil_cohesion(self):
        return self._soil_cohesion

    @property
    def soil_phi(self):
        return self._soil_phi

    def __repr__(self):
        return self.template.format(name=self.name,
                                    soil_gam_dry=self.soil_gam_dry,
                                    soil_gam_wet=self.soil_gam_wet,
                                    soil_cohesion=self.soil_cohesion,
                                    soil_phi=self.soil_phi)


