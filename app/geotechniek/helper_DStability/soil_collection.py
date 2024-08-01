from app.helper.utils import DeltaresReader
import re

class SoilCollection:
    def __init__(self, soil_collection_content):
        self._content = soil_collection_content
        self._soil_list = [Soil(soil_str) for soil_str in DeltaresReader(soil_collection_content).extract_all("SOIL")]
        self._number_of_soils = int(len(self._soil_list))
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
        self._content           = soil_content
        self._name              = soil_content.splitlines()[1]
        self._soil_gam_dry      = float(re.search("SoilGamDry=(\S+)",soil_content).groups()[0])
        self._soil_gam_wet      = float(re.search("SoilGamWet=(\S+)",soil_content).groups()[0])
        self._soil_cohesion     = float(re.search("SoilCohesion=(\S+)",soil_content).groups()[0])
        self._soil_phi          = float(re.search("SoilPhi=(\S+)",soil_content).groups()[0])
        self._soil_dilatancy    = float(re.search("SoilDilatancy=(\S+)",soil_content).groups()[0])

    @property
    def content(self):
        return self._content
    @property
    def name(self):
        return self._name
    @property
    def soil_gam_dry(self : float):
        return self._soil_gam_dry
    @property
    def soil_gam_wet(self : float):
        return self._soil_gam_wet
    @property
    def soil_cohesion(self : float):
        return self._soil_cohesion
    @property
    def soil_phi(self : float):
        return self._soil_phi
    @property
    def soil_dilatancy(self : float):
        return self._soil_dilatancy

    @name.setter
    def name(self, name : float):
        self._name = name

    @soil_gam_dry.setter
    def soil_gam_dry(self, soil_gam_dry : float):
        if soil_gam_dry < 0.0:
            raise ValueError(f"soil_gam_dry can not be less then 0. Found value {soil_gam_dry} for {self.name}")
        self._soil_gam_dry = float(soil_gam_dry)

    @soil_gam_wet.setter
    def soil_gam_wet(self, soil_gam_wet : float):
        if soil_gam_wet < 0.0:
            raise ValueError(f"soil_gam_wet can not be less then 0. Found value {soil_gam_wet} for {self.name}")
        self._soil_gam_wet = float(soil_gam_wet)

    @soil_cohesion.setter
    def soil_cohesion(self, soil_cohesion : float):
        if soil_cohesion < 0.0:
            raise ValueError(f"soil_cohesion can not be less then 0. Found value {soil_cohesion} for {self.name}")
        self._soil_cohesion = float(soil_cohesion)

    @soil_phi.setter
    def soil_phi(self, soil_phi : float):
        if soil_phi < 0.0 or soil_phi > 90.0:
            raise ValueError(f"soil_phi has values between 0 and 90. Found value {soil_phi} for {self.name}")
        self._soil_phi = float(soil_phi)

    @soil_dilatancy.setter
    def soil_dilatancy(self, soil_dilatancy : float):
        if soil_dilatancy < 0.0:
            raise ValueError(f"soil_dilatancy can not be less then 0. Found value {soil_dilatancy} for {self.name}")
        self._soil_dilatancy = float(soil_dilatancy)

    @property
    def template(self):
        template = self.content

        template_split_lines = template.splitlines()
        template_split_lines[1] = "{name}"
        template = "\n".join(template_split_lines)

        template = re.sub("SoilGamDry=\S+", "SoilGamDry={soil_gam_dry:.2f}", template)

        template = re.sub("SoilGamWet=\S+", "SoilGamDry={soil_gam_wet:.2f}", template)

        template = re.sub("SoilCohesion=\S+", "SoilCohesion={soil_cohesion:.2f}", template)

        template = re.sub("SoilPhi=\S+", "SoilPhi={soil_phi:.2f}", template)

        template = re.sub("SoilDilatancy=\S+", "SoilPhi={soil_dilatancy:.2f}", template)

        return template

    def __repr__(self):
        return self.template.format(name=self.name,
                                    soil_gam_dry=self.soil_gam_dry,
                                    soil_gam_wet=self.soil_gam_wet,
                                    soil_cohesion=self.soil_cohesion,
                                    soil_phi=self.soil_phi,
                                    soil_dilatancy=self.soil_dilatancy)
