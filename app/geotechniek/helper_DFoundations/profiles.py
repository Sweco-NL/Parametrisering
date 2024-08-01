from app.helper.utils import DeltaresReader
import re


class Profiles:
    def __init__(self, content):
        self._content = DeltaresReader(content).extract_first("PROFILES")
        self._excavation_level = float(re.search(r"(.*) : Excavation level \[m\]", self._content).groups()[0])
        self._number_CPTs = int(re.search(r"(.*) = number of items", self._content).groups()[0])
        self._CPT_list = [CPTs(i) for i in re.findall(r"Matching(.*?)(?=Matching CPT|\[END OF PROFILES\])", self._content, re.DOTALL)]
        self._length_CPT_list = len(self._CPT_list)

    @property
    def excavation_level(self):
        return self._excavation_level

    @excavation_level.setter
    def excavation_level(self, excavation_level):
        self._excavation_level = excavation_level

#    @property
#    def template(self):
#        template = re.sub(r".*: Excavation level \[m\]",
#                          "{excavation_level:12.2f} : Excavation level [m]",
#                          self.content)
#        template =  re.sub(r".* =  number of items",
#                          "{number_CPTs:12.2f} = number of items",
#                          template)
#        return template

    @property
    def number_CPTs(self):
        return self._number_CPTs

    @number_CPTs.setter
    def number_CPTs(self, number_CPTs):
        self._number_CPTs = number_CPTs

    @property
    def CPT_list(self):
        return self._CPT_list

    @CPT_list.setter
    def CPT_list(self, CPT_list):
        self._CPT_list = str(CPT_list)

    @property
    def length_CPT_list(self):
        return self._length_CPT_list

    @length_CPT_list.setter
    def length_CPT_list(self, length_CPT_list):
        self._length_CPT_list = length_CPT_list

class CPTs:
    def __init__(self, CPT_content : str):
        self._content = CPT_content
        self._name = str(re.search("CPT*\s\S\s(\S+)", CPT_content).groups()[0])
        self._xcoord = float(re.search("(.*) : X coordinate", self._content).groups()[0])
        self._ycoord = float(re.search("(.*) : Y coordinate", self._content).groups()[0])
        self._waterlevel = float(re.search("(.*) : Phreatic level", self._content).groups()[0])
        self._pile_tip_level = float(re.search("(.*) : Pile tip level", self._content).groups()[0])
        self._OCR = float(re.search("(.*) : Overconsolidation ratio of bearing layer", self._content).groups()[0])
        self._top_positive_skin = float(re.search("(.*) : Top of positive skin friction zone", self._content).groups()[0])
        self._bottom_negative_skin = float(re.search("(.*) : Bottom of negative skin friction zone", self._content).groups()[0])
        self._number_of_layers = int(re.search("(.*) : Number of layers", self._content).groups()[0])
        self._soil_list = [soilprofiles(i) for i in re.findall(r"(?<=Layer)(.*?)(?=\[%\])", self._content, re.DOTALL)]

    @property
    def content(self):
        return self._content

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def xcoord(self):
        return self._xcoord

    @xcoord.setter
    def xcoord(self, xcoord):
        self._xcoord = xcoord

    @property
    def ycoord(self):
        return self._ycoord

    @ycoord.setter
    def ycoord(self, ycoord):
        self._ycoord = ycoord

    @property
    def waterlevel(self):
        return self._waterlevel

    @waterlevel.setter
    def waterlevel(self, waterlevel):
        self._waterlevel = waterlevel

    @property
    def pile_tip_level(self):
        return self._pile_tip_level

    @pile_tip_level.setter
    def pile_tip_level(self, pile_tip_level):
        self._pile_tip_level = pile_tip_level

    @property
    def OCR(self):
        return self._OCR

    @OCR.setter
    def OCR(self, OCR):
        self._OCR = OCR

    @property
    def top_positive_skin(self):
        return self._top_positive_skin

    @top_positive_skin.setter
    def top_positive_skin(self, top_positive_skin):
        self._top_positive_skin = top_positive_skin

    @property
    def bottom_negative_skin(self):
        return self._bottom_negative_skin

    @bottom_negative_skin.setter
    def bottom_negative_skin(self, bottom_negative_skin):
        self._bottom_negative_skin = bottom_negative_skin

    @property
    def number_of_layers(self):
        return self._number_of_layers

    @number_of_layers.setter
    def number_of_soils(self, number_of_layers):
        self._number_of_layers = number_of_layers

    @property
    def soil_list(self):
        return self._soil_list

    @soil_list.setter
    def CPT_list(self, soil_list):
        self._soil_list = str(soil_list)

class soilprofiles:
    def __init__(self, soilprofile_content : str):
        self._content = soilprofile_content
        self._material = str(re.search("Material = (.*)", self._content).groups()[0])
        self._toplevel = float(re.search("(.*) : Top level \[m\]", self._content).groups()[0])

    @property
    def content(self):
        return self._content

    @property
    def material(self):
        return self._material

    @material.setter
    def name(self, material):
        self._material = material

    @property
    def toplevel(self):
        return self._toplevel

    @toplevel.setter
    def name(self, toplevel):
        self._toplevel = toplevel

#TO DO: soil profiles uitlezen. Dan andere app maken die alles kan gaan listen