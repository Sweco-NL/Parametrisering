import re
from pathlib import Path

from app.helper.deltares_reader import DeltaresReader


class Profiles:
    def __init__(self, content):
        self.content = DeltaresReader(content).extract_first("PROFILES")
        self.excavation_level = float(re.search(r"(.*) : Excavation level \[m\]", self.content.data).groups()[0])

    @property
    def excavation_level(self):
        return self._excavation_level

    @excavation_level.setter
    def excavation_level(self, excavation_level):
        self._excavation_level = excavation_level

    @property
    def template(self):
        template = re.sub(r".*: Excavation level \[m\]",
                          "{excavation_level:12.2f} : Excavation level [m]",
                          self.content.data)
        return template

    def __repr__(self):
        return self.template.format(excavation_level=self.excavation_level)


class PreliminaryDesign:
    def __init__(self, content):
        self.content = DeltaresReader(content).extract_first("PRELIMINARY DESIGN")

        self._pile = None
        pile_names = re.search("\s+(?P<pile_nr>\d+) : Pile type = (?P<pile_name>.*)", self.content.data)
        if pile_names is None:
            raise NotImplementedError(r"Geen palen geselecteerd in het input bestand.")
        pile_dict = re.search("\s+(?P<pile_nr>\d+) : Pile type = (?P<pile_name>.*)", self.content.data).groupdict()
        self.pile_name = pile_dict["pile_name"]
        self._pile_nr = pile_dict["pile_nr"]

    @property
    def pile_nr(self):
        return int(self._pile_nr)

    @pile_nr.setter
    def pile_nr(self, pile_nr):
        self._pile_nr = int(pile_nr)

    @property
    def template(self):
        return re.sub(".* : Pile type.*", "{pile_nr:>5d} : Pile type = {pile_name}", self.content.data)

    def __repr__(self):
        return self.template.format(pile_nr=self.pile_nr,
                                    pile_name=self.pile_name)


class TypesBearingPiles:
    def __init__(self, content: str):
        self.content = DeltaresReader(content).extract_first("TYPES - BEARING PILES").data
        self._pile_type_in_graph = None

    @property
    def shape(self) -> str:
        return re.search("Shape = (?P<shape>.*)", self.content).groupdict()["shape"]

    @property
    def piles(self):
        return {pile_nr: pile_name for pile_nr, pile_name in
                enumerate(re.findall(r"\n(.*)\s+\d+ : Pile type =", self.content))}

    @property
    def pile_type_in_graph(self):
        if self._pile_type_in_graph is None:
            return int(
                re.search("(?P<pile_type_in_graph>\d+)\s+: pile type shown in main graph", self.content).group()[0])
        else:
            return self._pile_type_in_graph

    @pile_type_in_graph.setter
    def pile_type_in_graph(self, pile_type_in_graph: int):
        self._pile_type_in_graph = int(pile_type_in_graph)

    @property
    def template(self):
        template = self.content
        template = re.sub("\d+ : pile type shown in main graph",
                          "{pile_type_in_graph:d} : pile type shown in main graph",
                          template)
        return template

    @property
    def __repr__(self):
        return self.template.format(pile_type_in_graph=self.pile_type_in_graph)


class PositionsBearingPiles:
    def __init__(self, content: str):
        self.content = DeltaresReader(content).extract_first("POSITIONS - BEARING PILES").data
        self._index = None
        self._x = None
        self._y = None
        self._pileheadlevel = None
        self._surcharge = None
        self._limit_state_str_geo = None
        self._limit_state_service = None
        self._pile_name = None
        extracted_dict = re.search("\[DATA\]"
                                   "\n"
                                   "(?P<index>.{6})"
                                   "(?P<x>.{10})"
                                   "(?P<y>.{10})"
                                   "(?P<pileheadlevel>.{10})"
                                   "(?P<surcharge>.{10})"
                                   "(?P<limit_state_str_geo>.{10})"
                                   "(?P<limit_state_service>.{10})"
                                   "\s+\'(?P<pile_name>.*)\'"
                                   "\n"
                                   "\[END OF DATA\]", self.content,
                                   flags=re.DOTALL).groupdict()
        for key, value in extracted_dict.items():
            setattr(self, key, value)

        # if self.content != self.__str__:
        #     raise NotImplementedError("When initiating self.content and self.output were found to be different.")

    @property
    def index(self) -> int:
        return int(self._index)

    @index.setter
    def index(self, index: int):
        self._index = int(index)

    @property
    def x(self) -> float:
        return float(self._x)

    @x.setter
    def x(self, x: float):
        self._x = float(x)

    @property
    def y(self) -> float:
        return float(self._y)

    @y.setter
    def y(self, y: float):
        self._y = float(y)

    @property
    def pileheadlevel(self):
        return float(self._pileheadlevel)

    @pileheadlevel.setter
    def pileheadlevel(self, pileheadlevel: float):
        self._pileheadlevel = float(pileheadlevel)

    @property
    def surcharge(self):
        return float(self._surcharge)

    @surcharge.setter
    def surcharge(self, surcharge: float):
        self._surcharge = float(surcharge)

    @property
    def limit_state_str_geo(self):
        return float(self._limit_state_str_geo)

    @limit_state_str_geo.setter
    def limit_state_str_geo(self, limit_state_str_geo: float):
        self._limit_state_str_geo = float(limit_state_str_geo)

    @property
    def limit_state_service(self):
        return float(self._limit_state_service)

    @limit_state_service.setter
    def limit_state_service(self, limit_state_service: float):
        self._limit_state_service = float(limit_state_service)

    @property
    def pile_name(self):
        return self._pile_name

    @pile_name.setter
    def pile_name(self, pile_name):
        self._pile_name = pile_name

    @property
    def template(self):
        template = re.sub("\[DATA\].*\[END OF DATA\]",
                          "[DATA]\n"
                          "{index:>6d}"
                          "{x:>10.2f}"
                          "{y:>10.2f}"
                          "{pileheadlevel:>10.2f}"
                          "{surcharge:>10.2f}"
                          "{limit_state_str_geo:>10.2f}"
                          "{limit_state_service:>10.2f}"
                          " \'{pile_name}\'\n"
                          "[END OF DATA]", self.content, flags=re.DOTALL)
        return template

    def __repr__(self):
        return self.template.format(index=self.index,
                                    x=self.x,
                                    y=self.y,
                                    pileheadlevel=self.pileheadlevel,
                                    surcharge=self.surcharge,
                                    limit_state_str_geo=self.limit_state_str_geo,
                                    limit_state_service=self.limit_state_service,
                                    pile_name=self.pile_name)


class FOI:
    def __init__(self, content):
        self.content = content
        self.types_bearing_piles = TypesBearingPiles(self.content)

        self.preliminary_design = PreliminaryDesign(self.content)
        self.profiles = Profiles(self.content)
        self.positions_bearing_piles = PositionsBearingPiles(self.content)
        self.calculation_options = CalculationOptions(self.content)
        self.calculation_type = Calculationtype(self.content)

    @property
    def version(self):
        return tuple(map(int, re.search(r"D-Foundations version (?P<version>.*)", self.content)
                         .groupdict()["version"].split(".")))

    @property
    def template(self):
        template = re.sub("\[PRELIMINARY DESIGN\].*\[END OF PRELIMINARY DESIGN\]",
                          "{preliminary_design}",
                          self.content, flags=re.DOTALL)
        template = re.sub("\[POSITIONS - BEARING PILES\].*\[END OF POSITIONS - BEARING PILES\]",
                          "{positions_bearing_piles}",
                          template, flags=re.DOTALL)
        template = re.sub("\[PROFILES\].*\[END OF PROFILES\]",
                          "{profiles}",
                          template, flags=re.DOTALL)
        template = re.sub("\[CALCULATION OPTIONS\].*\[END OF CALCULATION OPTIONS\]",
                          "{calculation_options}",
                          template, flags=re.DOTALL)
        template = re.sub("\[CALCULATIONTYPE\].*\[END OF CALCULATIONTYPE\]",
                          "{calculation_type}",
                          template, flags=re.DOTALL)
        return template

    def __str__(self):
        return self.template.format(preliminary_design=self.preliminary_design.__repr__(),
                                    positions_bearing_piles=self.positions_bearing_piles.__repr__(),
                                    profiles=self.profiles.__repr__(),
                                    calculation_options=self.calculation_options.__repr__(),
                                    calculation_type=self.calculation_type.__repr__())

    @property
    def new_file_name(self):
        return f"{float(self.profiles.excavation_level):.2f} {self.preliminary_design.pile_name}.foi".replace("/", "_")

    def save_to_file(self, new_file_name="{new_file_name}.foi", output_folder=None):
        # if output_folder:
        #     foi_path = Path(output_folder) / new_file_name.format(new_file_name=self.new_file_name)
        # else:
        #     foi_path = Path(new_file_name.format(new_file_name=self.new_file_name))
        foi_path = Path(output_folder) / self.new_file_name

        with open(foi_path, "w+") as writefile:
            writefile.write(self.__str__())


class Calculationtype:
    def __init__(self, content):
        self.content = DeltaresReader(content).extract_first("CALCULATIONTYPE").data
        self._main_calculation_type = re.search(" (\d) : Main calculationtype", self.content).group()[1]
        self._sub_calculation_type = re.search(" (\d) : Sub calculationtype", self.content).group()[1]
        self.possible_combinations = {(1, 0): "Design calculation",
                                      (1, 1): "Complete calculation",
                                      (0, 2): "Indication bearing capacity",
                                      (0, 3): "Bearing capacity at fixed pile type levels",
                                      (0, 4): "Pile tip levels and net bearing capacity"
                                      }

    def is_valid(self):
        calculation_combination = (self.main_calculation_type, self.sub_calculation_type)

        if self.possible_combinations.get(calculation_combination):
            return True
        else:
            raise NotImplementedError(
                r"The combination of main_calculation_type and sub_calculation_type is not valid.\n"
                fr"Main_calculation_type is {self.main_calculation_type}\n"
                fr"Sub_calculation_type is {self.sub_calculation_type}")

    @property
    def current_calculation_type(self) -> str:
        return self.possible_combinations[self.main_calculation_type, self.sub_calculation_type]

    @property
    def design_calculation(self) -> bool:
        return self.main_calculation_type == 1 and self.sub_calculation_type == 0

    @design_calculation.setter
    def design_calculation(self, design_calculation):
        if design_calculation:
            self.main_calculation_type = 1
            self.sub_calculation_type = 0

    @property
    def main_calculation_type(self):
        return int(self._main_calculation_type)

    @main_calculation_type.setter
    def main_calculation_type(self, main_calcuation_type: int):
        self._main_calculation_type = int(main_calcuation_type)

    @property
    def sub_calculation_type(self):
        return int(self._sub_calculation_type)

    @sub_calculation_type.setter
    def sub_calculation_type(self, sub_calculation_type: int):
        self._sub_calculation_type = int(sub_calculation_type)

    @property
    def template(self):
        template = re.sub(" (?P<main_calculation_type>\d) : Main calculationtype",
                          " {main_calculation_type} : Main calculationtype",
                          self.content)

        template = re.sub(" (?P<sub_calculation_type>\d) : Sub calculationtype",
                          " {sub_calculation_type} : Sub calculationtype",
                          template)
        return template

    def __repr__(self):
        # Before writing the output it should be checked that the output is valid.
        self.is_valid()
        output = self.template.format(main_calculation_type=self.main_calculation_type,
                                      sub_calculation_type=self.sub_calculation_type)
        return output


class CalculationOptions:
    def __init__(self, content):
        self.content = DeltaresReader(content).extract_first("CALCULATION OPTIONS").data
        self._write_intermediate_results = bool(
            re.search(r"(\d) : Write intermediate results =.*", self.content).groups()[0])

    @property
    def write_intermediate_results(self):
        return bool(self._write_intermediate_results)

    @write_intermediate_results.setter
    def write_intermediate_results(self, write_intermediate_results: bool):
        self._write_intermediate_results = bool(write_intermediate_results)

    @property
    def write_intermediate_results_uppercase_bool(self):
        return str(bool(self.write_intermediate_results)).upper()

    @property
    def template(self):
        template = re.sub(r"(\d) : Write intermediate results =.*",
                          r"{write_intermediate_results:d} : Write intermediate results = {write_intermediate_results_uppercase_bool}",
                          self.content)
        return template

    def __repr__(self):
        return self.template.format(write_intermediate_results=self.write_intermediate_results,
                                    write_intermediate_results_uppercase_bool=self.write_intermediate_results_uppercase_bool)
