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
        self._soil_cv           = float(re.search("SoilCv=(\S+)",soil_content).groups()[0])
        self._drained           = int(re.search("SoilDrained=(\S+)",soil_content).groups()[0])
        self._soil_OCR          = float(re.search("SoilOCR=(\S+)",soil_content).groups()[0])
        self._soil_POP          = float(re.search("SoilPOP=(\S+)",soil_content).groups()[0])
        self._soil_equivalent_age = float(re.search("SoilEquivalentAge=(\S+)",soil_content).groups()[0])
        self._soil_RR           = float(re.search("SoilRRatio=(\S+)",soil_content).groups()[0])
        self._soil_CR           = float(re.search("SoilCRatio=(\S+)",soil_content).groups()[0])
        self._soil_Ca           = float(re.search("SoilCa=(\S+)",soil_content).groups()[0])

    @property
    def content(self):
        return self._content
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
    def soil_cv(self):
        return self._soil_cv
    @property
    def soil_drained(self):
        return self._drained
    @property
    def soil_OCR(self):
        return self._soil_OCR
    @property
    def soil_POP(self):
        return self._soil_POP
    @property
    def soil_equivalent_age(self):
        return self._soil_equivalent_age
    @property
    def soil_RR(self):
        return self._soil_RR
    @property
    def soil_CR(self):
        return self._soil_CR
    @property
    def soil_Ca(self):
        return self._soil_Ca

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

    @soil_cv.setter
    def soil_cv(self, soil_cv):
        if soil_cv < 0:
            raise ValueError(f"soil_cv can not be less then 0. Found value {soil_cv} for {self.name}")
        self._soil_cv = float(soil_cv)

    @soil_drained.setter
    def soil_drained(self, soil_drained):
        if soil_drained != 0 and soil_drained != 1:
            raise ValueError(f"soil_drained can only be 0 or 1. Found value {soil_drained} for {self.name}")
        self._soil_drained = float(soil_drained)

    @soil_OCR.setter
    def soil_OCR(self, soil_OCR):
        if soil_OCR < 0:
            raise ValueError(f"soil_OCR can not be less then 0. Found value {soil_OCR} for {self.name}")
        self._soil_OCR = float(soil_OCR)

    @soil_POP.setter
    def soil_POP(self, soil_POP):
        if soil_POP < 0:
            raise ValueError(f"soil_POP can not be less then 0. Found value {soil_POP} for {self.name}")
        self._soil_POP = float(soil_POP)

    @soil_equivalent_age.setter
    def soil_equivalent_age(self, soil_equivalent_age):
        if soil_equivalent_age < 0:
            raise ValueError(f"soil_equivalent_age can not be less then 0. Found value {soil_equivalent_age} for {self.name}")
        self._soil_equivalent_age = float(soil_equivalent_age)

    @soil_RR.setter
    def soil_RR(self, soil_RR):
        if soil_RR < 0:
            raise ValueError(f"soil_RR can not be less then 0. Found value {soil_RR} for {self.name}")
        self._soil_RR = float(soil_RR)

    @soil_CR.setter
    def soil_CR(self, soil_CR):
        if soil_CR < 0:
            raise ValueError(f"soil_CR can not be less then 0. Found value {soil_CR} for {self.name}")
        self._soil_CR = float(soil_CR)

    @soil_Ca.setter
    def soil_Ca(self, soil_Ca):
        if soil_Ca < 0:
            raise ValueError(f"soil_Ca can not be less then 0. Found value {soil_Ca} for {self.name}")
        self._soil_Ca = float(soil_Ca)

    @property
    def template(self):
        template = self.content

        template_split_lines = template.splitlines()
        template_split_lines[1] = "{name}"
        template = "\n".join(template_split_lines)

        template = re.sub("SoilGamDry=\S+", "SoilGamDry={soil_gam_dry:.2f}", template)

        template = re.sub("SoilGamWet=\S+", "SoilGamDry={soil_gam_dry:.2f}", template)

        template = re.sub("SoilCv=\S+", "SoilCv={soil_cv:.2f}", template)

        template = re.sub("SoilDrained=\S+", "SoilDrained={soil_drained:.2f}", template)

        template = re.sub("SoilOCR=\S+", "SoilOCR={soil_OCR:.2f}", template)

        template = re.sub("SoilPOP=\S+", "SoilPOP={soil_POP:.2f}", template)

        template = re.sub("SoilEquivalentAge=\S+", "SoilEquivalentAge={soil_equivalent_age:.2f}", template)

        template = re.sub("SoilRRatio=\S+", "SoilRRatio={soil_RR:.2f}", template)

        template = re.sub("SoilCRatio=\S+", "SoilCRatio={soil_CR:.2f}", template)

        template = re.sub("SoilCa=\S+", "SoilCa={soil_Ca:.2f}", template)

        return template

    def __repr__(self):
        return self.template.format(name=self.name,
                                    soil_gam_dry=self.soil_gam_dry,
                                    soil_gam_wet=self.soil_gam_wet,
                                    soil_cv=self.soil_cv,
                                    soil_drained=self.soil_drained,
                                    soil_OCR=self.soil_OCR,
                                    soil_POP=self.soil_POP,
                                    soil_equivalent_age=self.soil_equivalent_age,
                                    soil_RR=self.soil_RR,
                                    soil_CR=self._soil_CR,
                                    soil_Ca=self.soil_Ca)
