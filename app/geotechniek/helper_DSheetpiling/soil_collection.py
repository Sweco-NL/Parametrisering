from app.helper.utils import DeltaresReader
import re
class SoilCollection:
    def __init__(self, soil_collection_content : str):
        self._content = soil_collection_content
        self._soil_list = [Soil(soil_str) for soil_str in DeltaresReader(soil_collection_content).extract_all("SOIL")]
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
        self._soil_delta            = float(re.search("SoilDelta=(\S+)",soil_content).groups()[0])
        self._soil_cur_kb1          = float(re.search("SoilCurKb1=(\S+)",soil_content).groups()[0])
        self._soil_cur_kb2          = float(re.search("SoilCurKb2=(\S+)", soil_content).groups()[0])
        self._soil_cur_kb3          = float(re.search("SoilCurKb3=(\S+)", soil_content).groups()[0])

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

    @property
    def soil_delta(self):
        return self._soil_delta

    @property
    def soil_cur_kb1(self):
        return self._soil_cur_kb1

    @property
    def soil_cur_kb2(self):
        return self._soil_cur_kb2

    @property
    def soil_cur_kb3(self):
        return self._soil_cur_kb3

# define functions to change name of selected parameters
    @name.setter
    def name(self, name):
        self._name = name

    @soil_gam_dry.setter
    def soil_gam_dry(self, soil_gam_dry):
        if soil_gam_dry < 0:
            raise ValueError(f"soil_gam_dry can not be less then 0. Found value {soil_gam_dry} for {self.name}")
        self._soil_gam_dry = float(soil_gam_dry)

    @soil_gam_wet.setter
    def soil_gam_wet(self, soil_gam_wet):
        if soil_gam_wet < 0:
            raise ValueError(f"soil_gam_wet can not be less then 0. Found value {soil_gam_wet} for {self.name}")
        self._soil_gam_wet = float(soil_gam_wet)

    @soil_cohesion.setter
    def soil_cohesion(self, soil_cohesion):
        if soil_cohesion < 0:
            raise ValueError(f"soil_cohesion can not be less then 0. Found value {soil_cohesion} for {self.name}")
        self._soil_cohesion = float(soil_cohesion)

    @soil_phi.setter
    def soil_phi(self, soil_phi):
        if soil_phi < 0:
            raise ValueError(f"soil_phi can not be less then 0. Found value {soil_phi} for {self.name}")
        self._soil_phi = float(soil_phi)

    @soil_gam_dry.setter
    def soil_gam_dry(self, soil_gam_dry):
        if soil_gam_dry < 0:
            raise ValueError(f"soil_delta can not be less then 0. Found value {soil_gam_dry} for {self.name}")
        self._soil_dry = float(soil_gam_dry)

    @soil_cur_kb1.setter
    def soil_cur_kb1(self, soil_cur_kb1):
        if soil_cur_kb1 < 0:
            raise ValueError(f"soil_cur_kb1 can not be less then 0. Found value {soil_cur_kb1} for {self.name}")
        self._soil_cur_kb1 = float(soil_cur_kb1)

    @soil_cur_kb2.setter
    def soil_cur_kb2(self, soil_cur_kb2):
        if soil_cur_kb2 < 0:
            raise ValueError(f"soil_cur_kb1 can not be less then 0. Found value {soil_cur_kb2} for {self.name}")
        self._soil_cur_kb2 = float(soil_cur_kb2)

    @soil_cur_kb3.setter
    def soil_cur_kb3(self, soil_cur_kb3):
        if soil_cur_kb3 < 0:
            raise ValueError(f"soil_cur_kb1 can not be less then 0. Found value {soil_cur_kb3} for {self.name}")
        self._soil_cur_kb3 = float(soil_cur_kb3)

#define template for selected parameters
    @property
    def template(self):
        template = self.content

        template_split_lines = template.splitlines()
        template_split_lines[1] = "{name}"
        template = "\n".join(template_split_lines)

        template = re.sub("SoilGamDry=\S+", "SoilGamDry={soil_gam_dry:.2f}", template)

        template = re.sub("SoilGamWet=\S+", "SoilGamDry={soil_gam_dry:.2f}", template)

        template = re.sub("SoilCohesion=\S+", "SoilCohesion={soil_cohesion:.2f}", template)

        template = re.sub("SoilPhi=\S+", "SoilPhi={soil_phi:.2f}", template)

        template = re.sub("SoilDelta=\S+", "SoilDelta={soil_delta:.2f}", template)

        template = re.sub("SoilCurKb1=\S+", "SoilDelta={soil_cur_kb1:.2f}", template)

        template = re.sub("SoilCurKb2=\S+", "SoilDelta={soil_cur_kb2:.2f}", template)

        template = re.sub("SoilCurKb3=\S+", "SoilDelta={soil_cur_kb3:.2f}", template)

        return template

    def __repr__(self):
        return self.template.format(name=self.name,
                                    soil_gam_dry=self.soil_gam_dry,
                                    soil_gam_wet=self.soil_gam_wet,
                                    soil_cohesion=self.soil_cohesion,
                                    soil_phi=self.soil_phi,
                                    soil_delta=self.soil_delta,
                                    soil_cur_kb1=self.soil_cur_kb1,
                                    soil_cur_kb2=self.soil_cur_kb2,
                                    soil_cur_kb3=self.soil_cur_kb3)

