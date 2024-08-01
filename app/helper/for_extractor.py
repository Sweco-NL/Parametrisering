from collections import defaultdict
import pandas as pd
from pathlib import Path
import re
from app.helper.foi import FOI
from typing import Union, Dict, List
from general.utilities import Current_date_time

class FOR():
    def __init__(self, content: str):
        self._content = content

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, content: str):
        self._content = content

    @property
    def ksi3(self):
        return float(re.search(r"NEN \S+ tabel A.10: ksi3\s+=\s+(?P<ksi3>\S+)",
                               self.content).groupdict()["ksi3"])

    @property
    def ksi4(self):
        return float(re.search(r"NEN \S+ tabel A.10: ksi4\s+=\s+(?P<ksi4>\S+)",
                               self.content).groupdict()["ksi4"])

    @property
    def ontwerpberekeningen(self):
        output = []
        for item in re.finditer("(Ontwerpberekening\s+\d+\s+met PPN = \S+ m.\s+\**\s+"
                                ".*?CONTROLE BIJ GRENSTOESTAND EQU.*?"
                                "BEREKENING NEGATIEVE KLEEF\s+---+.*?---+\n.*?\n---+.*?"
                                "bruikbaarheidsgrenstoestand..*?Beta_dBruikbaarheid =)",
                                self.content, re.DOTALL):
            output.append(Ontwerpberekening(item.group()))
        return output


class GrenstoestandEqu:
    def __init__(self, content):
        self.content = content

    # @property
    # def filename(self):
    #
    #     return Path(re.search("FILENAME\s+:\s+(?P<filename>.*)", self.content).groupdict()["filename"]).name

    @property
    def ksi3(self):
        return float(re.search(r"NEN 9997-1:2016 tabel A.10: ksi3\s+=\s+(?P<ksi3>\S+)", self.content)
                     .groupdict()["ksi3"])

    @property
    def ksi4(self):
        return float(re.search(r"NEN 9997-1:2016 tabel A.10: ksi4\s+=\s+(?P<ksi4>\S+)", self.content)
                     .groupdict()["ksi4"])

    @property
    def controle_data(self) -> dict:
        return {key: float(value) for key, value in
                re.search("CONTROLE BIJ GRENSTOESTAND EQU\s+"
                          "NEN.*?tabel A.10: ksi3\s+=\s+(?P<ksi3>\S+)\s+"
                          "NEN.*?tabel A.10: ksi4\s+=\s+(?P<ksi4>\S+)\s+"
                          "Rc_k Gemiddeld\s+\(met ksi3\)\s+=\s+(?P<Rc_k_gemiddeld>\S+)\s+"
                          "Rc_k Minimum   \(met ksi4\)\s+=\s+(?P<Rc_k_minimum>\S+)\s+"
                          "Ksi\d is used.\s+"
                          "Rb;k\s+=\s+(?P<Rb_k>\S+)\s+"
                          "Rs;k\s+=\s+(?P<Rs_k>\S+)\s+"
                          "NEN.*?tabel A.6, A.7, A.8: Gamma_b =\s+(?P<gamma_b>\S+)\s+"
                          "NEN.*?tabel A.6, A.7, A.8:\s+Gamma_s =\s+(?P<gamma_s>\S+)\s+"
                          "Rb;d\s+=\s+(?P<Rb_d>\S+)\s+"
                          "Rs;d\s+=\s+(?P<Rs_d>\S+)\s+"
                          "Rc;d\s+=\s+(?P<Rc_d>\S+)",
                          self.content, flags=re.DOTALL).groupdict().items()}


    @property
    def berekeningstoestanden(self):
        grenstoestanden = re.findall(r"BEREKENING GRENSTOESTAND.*?\n\n", self.content, re.DOTALL)
        compiled_regex = re.compile(
            r"BEREKENING GRENSTOESTAND EQU BIJ SONDERING\s+(?P<sondering_naam>.+?)\s+\(PPN\s+=\s+(?P<paalpuntniveau>\S+) m\.\)\s+"
            r"\s+qc;I;gem\s+=\s+(?P<qc_i_gem>\S+)\s+qc;II;gem\s+=\s+(?P<qc_ii_gem>\S+)\s+qc;III;gem =\s+(?P<qc_iii_gem>\S+)\s+"
            r".*?Deq\s+=\s+(?P<Deq>\S+)\s+"
            r".*?alpha_p\s+=\s+(?P<alpha_p>\S+)\s+"
            r".*?beta\s+=\s+(?P<beta>\S+)\s+"
            r".*?s\s+=\s+(?P<s>\S+)\s+"
            r"\s+qb;max;i\s+\[kPa\]\s+=\s+(?P<qb_max_i_voor>\S+)\s+\(voor reductie tot \S+ MPa\)\s+"
            r"qb;max;i\s+\[kPa\]\s+=\s+(?P<qb_max_i_na>\S+)\s+\(na reductie tot \S+ MPa\)\s+"
            r"Rb;cal;max;i\s+\[kN\]\s+=\s+(?P<Rb_cal_max>\S+)\s+per sondering\s+"
            r"Rs;cal;max;i\s+\[kN\]\s+=\s+(?P<Rs_cal_max>\S+)\s+per sondering\s+"
            r"Rc;cal;max;i\s+\[kN\]\s+=\s+(?P<Rc_cal_max>\S+)", re.DOTALL)

        compiled_regex2 = re.compile(
            r"BEREKENING GRENSTOESTAND EQU BIJ SONDERING (?P<sondering_naam>.*?) \(PPN =\s+(?P<paalpuntniveau>\S+) m.\)\s+"
            r"qc;I;gem    =\s+(?P<qc_i_gem>\S+)\s+qc;II;gem  =\s+(?P<qc_ii_gem>\S+)\s+qc;III;gem.*? =\s+(?P<qc_iii_gem>\S+)\s+"
            r".*?Deq\s+=\s+(?P<Deq>\S+)\s+"
            r"qc;I;gem_notplugged    =\s+(?P<qc_i_gem_notplugged>\S+)\s+qc;II;gem_notplugged  =\s+(?P<qc_ii_gem_notplugged>\S+)\s+"
            r"qc;III;gem_notplugged =\s+(?P<qc_iii_gem_notplugged>\S+)\s+"
            r"Deq_notplugged         =\s+(?P<Deq_nogplugged>\S+)\s+"
            r"alpha_p\s+=\s+(?P<alpha_p>\S+)\s+beta\s+=\s+(?P<beta>\S+)\s+s \(plugged\)=\s+(?P<s_plugged>\S+)\s+"
            r"s\(unplugged\)=\s+(?P<s_unplugged>\S+)\s+"
            r"qb;max;i\s+\[kPa\]\s+=\s+(?P<qb_max_i_voor>\S+)\s+\(voor reductie tot 15 MPa\)\s+"
            r"qb;max;i_notplugged \[kPa\] =\s+(?P<qb_max_i_voor_notplugged>\S+)\s+\(voor reductie tot 15 MPa\)\s+"
            r"qb;max;i\s+\[kPa\]\s+=\s+(?P<qb_max_i_na>\S+)\s+\(na reductie tot 15 MPa\)\s+"
            r"qb;max;i_notplugged\s+\[kPa\] =\s+(?P<qb_max_i_na_notplugged>\S+)\s+\(na reductie tot 15 MPa\)\s+"
            r"Frpunt plugged\s+\[kN\] =\s+(?P<Fr_punt_plugged>\S+)\s+"
            r"Frpunt unplugged\s+\[kN\] =\s+(?P<Fr_punt_unplugged>\S+)\s+"
            r"Fr inw unplugged \[kN\] =\s+(?P<Fr_inw_unplugged>\S+)\s+"
            r"Fr unplugged tot \[kN\] =\s+(?P<Fr_unplugged_tot>\S+)\s+"
            r"Rs;max;i;inw\[kN\]  =\s+\S+\s+\(Open buispaal: inwendige wrijving is maatgevend\)\s+"
            r"Rb;cal;max;i\s+\[kN\] =\s+(?P<Rb_cal_max>\S+)\s+per sondering\s+"
            r"Rs;cal;max;i\s+\[kN\] =\s+(?P<Rs_cal_max>\S+)\s+per sondering\s+"
            r"Rc;cal;max;i\s+\[kN\] =\s+(?P<Rc_cal_max>\S+)\s+per sondering"
            , re.DOTALL)

        compiled_regex3 = re.compile(
            r"BEREKENING GRENSTOESTAND EQU BIJ SONDERING (?P<sondering_naam>.*?) \(PPN =\s+(?P<paalpuntniveau>\S+) m.\)\s+"
            r"qc;I;gem    =\s+(?P<qc_i_gem>\S+)\s+qc;II;gem  =\s+(?P<qc_ii_gem>\S+)\s+qc;III;gem.*? =\s+(?P<qc_iii_gem>\S+)\s+"
            r".*?Deq\s+=\s+(?P<Deq>\S+)\s+"
            r"qc;I;gem_notplugged    =\s+(?P<qc_i_gem_notplugged>\S+)\s+qc;II;gem_notplugged  =\s+(?P<qc_ii_gem_notplugged>\S+)\s+"
            r"qc;III;gem_notplugged =\s+(?P<qc_iii_gem_notplugged>\S+)\s+"
            r"Deq_notplugged         =\s+(?P<Deq_nogplugged>\S+)\s+"
            r"alpha_p\s+=\s+(?P<alpha_p>\S+)\s+beta\s+=\s+(?P<beta>\S+)\s+s \(plugged\)=\s+(?P<s_plugged>\S+)\s+"
            r"s\(unplugged\)=\s+(?P<s_unplugged>\S+)\s+"
            r"qb;max;i\s+\[kPa\]\s+=\s+(?P<qb_max_i_voor>\S+)\s+\(voor reductie tot 15 MPa\)\s+"
            r"qb;max;i_notplugged \[kPa\] =\s+(?P<qb_max_i_voor_notplugged>\S+)\s+\(voor reductie tot 15 MPa\)\s+"
            r"qb;max;i\s+\[kPa\]\s+=\s+(?P<qb_max_i_na>\S+)\s+\(na reductie tot 15 MPa\)\s+"
            r"qb;max;i_notplugged\s+\[kPa\] =\s+(?P<qb_max_i_na_notplugged>\S+)\s+\(na reductie tot 15 MPa\)\s+"
            r"Frpunt plugged\s+\[kN\] =\s+(?P<Fr_punt_plugged>\S+)\s+"
            r"Frpunt unplugged\s+\[kN\] =\s+(?P<Fr_punt_unplugged>\S+)\s+"
            r"Fr inw unplugged \[kN\] =\s+(?P<Fr_inw_unplugged>\S+)\s+"
            r"Fr unplugged tot \[kN\] =\s+(?P<Fr_unplugged_tot>\S+)\s+"
            r"Apuntplugged \[m\]\s+=\s+(?P<Apuntplugged>\S+)\s+\(Open buispaal: plug is maatgevend\)\s+"
            r"Rb;cal;max;i\s+\[kN\] =\s+(?P<Rb_cal_max>\S+)\s+per sondering\s+"
            r"Rs;cal;max;i\s+\[kN\] =\s+(?P<Rs_cal_max>\S+)\s+per sondering\s+"
            r"Rc;cal;max;i\s+\[kN\] =\s+(?P<Rc_cal_max>\S+)\s+per sondering"
            , re.DOTALL)

        compiled_regex4 = re.compile(r"\s+(BEREKENING GRENSTOESTAND EQU BIJ SONDERING)\s+(?P<sondering_naam>.+?)\s+\(PPN\s+=\s+(?P<paalpuntniveau>\S+) m\.\)"
                   r"\s+qc;I;gem\s+=\s+(?P<qc_i_gem>\S+)\s+qc;II;gem\s+=\s+(?P<qc_ii_gem>\S+)\s+qc;III;gem =\s+(?P<qc_iii_gem>\S+)"
                   r"\s+.*?Deq\s+=\s+(?P<Deq>\S+)"
                   r"\s+.*?alpha_p\s+=\s+(?P<alpha_p>\S+)\s+.*?beta\s+=\s+(?P<beta>\S+)\s+.*?s\s+=\s+(?P<s>\S+)"
                   r"\s+\s+qb;max;i\s+\[kPa\]\s+=\s+(?P<qb_max_i_voor>\S+)\s+\(voor reductie tot \S+ MPa\)"
                   r"\s+qb;max;i\s+\[kPa\]\s+=\s+(?P<qb_max_i_na>\S+)\s+\(na reductie tot \S+ MPa\)"
                   r"\s+Rb;cal;max;i\s+\[kN\]\s+=\s+(?P<Rb_cal_max>\S+)\s+per sondering"
                   r"\s+Rs;cal;max;i\s+\[kN\]\s+=\s+(?P<Rs_cal_max>\S+)\s+per sondering"
                   r"\s+Rc;cal;max;i\s+\[kN\]\s+=\s+(?P<Rc_cal_max>\S+) per sondering", flags=re.DOTALL)

        compiled_regex5 = \
            re.compile(r"\s*BEREKENING GRENSTOESTAND EQU BIJ SONDERING (?P<sondering_naam>.*?)\s+\(PPN\s+\=\s+(?P<paalpuntniveau>\S+)\s+m\.\)"
                       r"\s+qc;I;gem\s+\=\s+(?P<qc_i_gem>\S+)\s+qc;II;gem\s+=\s+(?P<qc_ii_gem>\S+)\s+qc;III;gem\s+=\s+(?P<qc_iii_gem>\S+)"
                       r"\s+Deq\s+\=\s+(?P<Deq>\S+)"
                       r"\s+qc;I;gem_notplugged\s+\=\s+(?P<qc_i_gem_notplugged>\S+)\s+qc;II;gem_notplugged\s+=\s+(?P<qc_ii_gem_notplugged>\S+)"
                       r"\s+qc;III;gem_notplugged\s=\s+(?P<qc_iii_gem_notplugged>\S+)"
                       r"\s+Deq_notplugged\s+\=\s+(?P<Deq_notplugged>\S+)"
                       r"\s+alpha_p\s+\=\s+(?P<alpha_p>\S+)\s+beta\s+\=\s+(?P<beta>\S+)\s+s\s\(plugged\)\=\s+(?P<s_plugged>\S+)"
                       r"\s+s\(unplugged\)\=\s+(?P<s_unplugged>\S+)"
                       r"\s+qb;max;i\s+\[kPa\]\s+\=\s+(?P<qc_max_i_voor>\S+)\s+\(voor\s+reductie\s+tot\s+\S+\s+MPa\)"
                       r"\s+qb;max;i_notplugged\s+\[kPa\]\s+\=\s+(\S+)\s+\(voor\s+reductie\s+tot\s+\S+\s+MPa\)"
                       r"\s+qb;max;i\s+\[kPa\]\s+\=\s+(?P<qb_max_i_na>\S+)\s+\(na\s+reductie\s+tot\s+\S+\s+MPa\)"
                       r"\s+qb;max;i_notplugged\s+\[kPa\]\s+\=\s+(?P<qb_max_i_notplugged_na>\S+)\s+\(na\s+reductie\s+tot\s+\S+\s+MPa\)"
                       r"\s+Frpunt\s+plugged\s+\[kN\]\s\=\s+(?P<fr_punt_plugged>\S+)"
                       r"\s+Frpunt\s+unplugged\s+\[kN\]\s+\=\s+(?P<fr_pung_unplugged>\S+)"
                       r"\s+Fr\s+inw\s+unplugged\s+\[kN\]\s+\=\s+(?P<fr_inw_unplugged>\S+)"
                       r"\s+Fr unplugged tot \[kN\] \=\s+(?P<fr_unplugged_tot>\S+)"
                       r"\s+Apuntplugged \[m\]\s+=\s+(?P<Apuntplugged>\S+)\s+\(Open buispaal: plug is maatgevend\)"
                       r"\s+Rb;cal;max;i\s+\[kN\] =\s+(?P<Rb_cal_max>\S+)\s+per sondering"
                       r"\s+Rs;cal;max;i\s+\[kN\] =\s+(?P<Rs_cal_max>\S+)\s+per sondering"
                       r"\s+Rc;cal;max;i\s+\[kN\] =\s+(?P<Rc_cal_max>\S+)\s+per sondering",re.DOTALL)

        compiled_regex6 = re.compile("\s*BEREKENING GRENSTOESTAND EQU BIJ SONDERING (?P<sondering_naam>.*?)\s+\(PPN\s+\=\s+(?P<paalpuntniveau>\S+)\s+m\.\)"
                       "\s+qc;I;gem\s+\=\s+(?P<qc_i_gem>\S+)\s+qc;II;gem\s+=\s+(?P<qc_ii_gem>\S+)\s+qc;III;gem\s+=\s+(?P<qc_iii_gem>\S+)"
                       "\s+Deq\s+\=\s+(?P<Deq>\S+)"
                       "\s+qc;I;gem_notplugged\s+\=\s+(?P<qc_i_gem_notplugged>\S+)\s+qc;II;gem_notplugged\s+=\s+(?P<qc_ii_gem_notplugged>\S+)"
                       "\s+qc;III;gem_notplugged\s=\s+(?P<qc_iii_gem_notplugged>\S+)"
                       "\s+Deq_notplugged\s+\=\s+(?P<Deq_notplugged>\S+)"
                       "\s+alpha_p\s+\=\s+(?P<alpha_p>\S+)\s+beta\s+\=\s+(?P<beta>\S+)\s+s\s\(plugged\)\=\s+(?P<s_plugged>\S+)"
                       "\s+s\(unplugged\)\=\s+(?P<s_unplugged>\S+)"
                       "\s+qb;max;i\s+\[kPa\]\s+\=\s+(?P<qc_max_i_voor>\S+)\s+\(voor\s+reductie\s+tot\s+\S+\s+MPa\)"
                       "\s+qb;max;i_notplugged\s+\[kPa\]\s+\=\s+(\S+)\s+\(voor\s+reductie\s+tot\s+\S+\s+MPa\)"
                       "\s+qb;max;i\s+\[kPa\]\s+\=\s+(?P<qb_max_i_na>\S+)\s+\(na\s+reductie\s+tot\s+\S+\s+MPa\)"
                       "\s+qb;max;i_notplugged\s+\[kPa\]\s+\=\s+(?P<qb_max_i_notplugged_na>\S+)\s+\(na\s+reductie\s+tot\s+\S+\s+MPa\)"
                       "\s+Frpunt\s+plugged\s+\[kN\]\s\=\s+(?P<fr_punt_plugged>\S+)"
                       "\s+Frpunt\s+unplugged\s+\[kN\]\s+\=\s+(?P<fr_pung_unplugged>\S+)"
                       "\s+Fr\s+inw\s+unplugged\s+\[kN\]\s+\=\s+(?P<fr_inw_unplugged>\S+)"
                       "\s+Fr unplugged tot \[kN\] \=\s+(?P<fr_unplugged_tot>\S+)"
                       "\s+Rs;max;i;inw\[kN\]\s+\=\s+(\S+)\s+\(Open buispaal: inwendige wrijving is maatgevend\)"
                       "\s+Rb;cal;max;i\s+\[kN\] =\s+(?P<Rb_cal_max>\S+)\s+per sondering"
                       "\s+Rs;cal;max;i\s+\[kN\] =\s+(?P<Rs_cal_max>\S+)\s+per sondering"
                       "\s+Rc;cal;max;i\s+\[kN\] =\s+(?P<Rc_cal_max>\S+)\s+per sondering")

        output = []

        export_as_float = ["Deq",
                           "paalpuntniveau",
                           "qc_i_gem",
                           "qc_ii_gem",
                           "qc_iii_gem",
                           "alpha_p",
                           "beta",
                           "s",
                           "qb_max_i_voor",
                           "qb_max_i_na",
                           "Rb_cal_max",
                           "Rs_cal_max",
                           "Rc_cal_max"]

        for grenstoestand in grenstoestanden:
            if compiled_regex.search(grenstoestand):
                saved = compiled_regex.search(grenstoestand).groupdict()
            elif compiled_regex2.search(grenstoestand):
                saved = compiled_regex2.search(grenstoestand).groupdict()
            elif compiled_regex3.search(grenstoestand):
                saved = compiled_regex3.search(grenstoestand).groupdict()
            elif compiled_regex4.search(grenstoestand):
                saved = compiled_regex4.search(grenstoestand).groupdict()
            elif compiled_regex5.search(grenstoestand):
                saved = compiled_regex5.search(grenstoestand).groupdict()
            elif compiled_regex6.search(grenstoestand):
                saved = compiled_regex6.search(grenstoestand).groupdict()
            else:
                raise NotImplementedError(f"{grenstoestand}")
            float_dict = {key: float(value) for key, value in saved.items() if key in export_as_float}
            not_float_dict = {key: value for key, value in saved.items() if key not in export_as_float}
            total_dict = {**float_dict, **not_float_dict}
            output.append(total_dict)
        return output


def kleef_list(kleef_content: str, key_prefix):
    negatieve_kleef_dict = re.search("BEREKENING NEGATIEVE KLEEF.*?"
                                     "----------------------------------------------------------------------(?P<headers>.*?)"
                                     "----------------------------------------------------------------------\n(?P<rows>.*?)"
                                     "----------------------------------------------------------------------",
                                     kleef_content, re.DOTALL).groupdict()
    output = []
    fnk_compile = re.compile(
        "(?P<sondering_naam>.*)\s+"
        "(?P<paal_nr>\d+)\s+"
        "(?P<paal_group>\S+)\s+"
        "(?P<fnk_k>\S+)\s+"
        "(?P<gamma>\S+)\s+"
        "(?P<fnk_d>\S+)\s+"
        "(?P<sneg>\S+)$")
    for line in negatieve_kleef_dict["rows"].splitlines():
        if "Geen negatieve kleefzone" in line:
            sondering_naam, paal_nr, paal_group, *_ = line.split()
            results_dict = dict(sondering_naam=sondering_naam,
                                paal_nr=paal_nr,
                                paal_group=paal_group,
                                fnk_k=0.0,
                                gamma=0.0,
                                fnk_d=0.0,
                                sneg=0.0)
        else:
            results_dict = fnk_compile.search(line).groupdict()

        sondering_naam = results_dict["sondering_naam"].strip()
        output.append({f"sondering_naam": sondering_naam,
                       f"{key_prefix}_paal_nr": int(results_dict["paal_nr"]),
                       f"{key_prefix}_paal_group": results_dict["paal_group"].strip(),
                       f"{key_prefix}_fnk_k": float(results_dict["fnk_k"]),
                       f"{key_prefix}_gamma": float(results_dict["gamma"]),
                       f"{key_prefix}_fnk_d": float(results_dict["fnk_d"]),
                       f"{key_prefix}_sneg": float(results_dict["sneg"])
                       }
                      )
    return output


class PaalZakking:

    def __init__(self, content):
        self.content = content

    @property
    def paal_zakking(self):
        # paal_zakking_compile = re.compile(r"""  BEREKENING ZAKKING VOOR PAAL\s+(?P<paal_nummer>.*?)\s+BIJ SONDERING\s+(?P<sondering_naam>.*?)
        # Fc;tot;i =\s+(?P<Fc_tot>.*?)\s+Rb;cal;max;i;d =\s+(?P<Rb_cal>.*?)\s+Rs;cal;max;i;d =\s+(?P<Rs_cal>.*?)
        # s2\s+=\s+(?P<s2>.*?)\s+Rb;i;d\s+=\s+(?P<Rb>.*?)\s+sb\s+=\s+(?P<sb>.*?)
        # sel\s+=\s+(?P<sel>.*?)\s+s1\s+=\s+(?P<s1>.*?)\s+s\s+=\s+(?P<s>.*)\s+""")
        #         output = []
        #         for paal_nummer, sondering_naam, Fc_tot, Rb_cal, Rs_cal, s2, Rb, sb, sel, s1, s in paal_zakking_compile.findall(
        #                 self.content):
        #             output.append(dict(paal_nummer=int(paal_nummer),
        #                                sondering_naam=sondering_naam,
        #                                      Fc_tot=float(Fc_tot),
        #                                      Rb_cal=float(Rb_cal),
        #                                      Rs_cal=float(Rs_cal),
        #                                      s2=float(s2),
        #                                      Rb=float(Rb),
        #                                      sb=float(sb),
        #                                      sel=float(sel),
        #                                      s1=float(s1),
        #                                      s=float(s)))
        export_as_float = ["Fc_tot", "Rb_cal", "Rs_cal", "s2", "Rb", "sb", "sel", "s1", "s"]
        regex_pattern = "BEREKENING ZAKKING VOOR PAAL\s+(?P<paal_nummer>.*?)\s+BIJ SONDERING\s+(?P<sondering_naam>.*?)\s+" \
                        "Fc;tot;i\s+=\s+(?P<Fc_tot>\S+)\s+Rb;cal;max;i;d\s+=\s+(?P<Rb_cal>\S+)\s+Rs;cal;max;i;d\s+=\s+(?P<Rs_cal>\S+)\s+" \
                        "s2\s+=\s+(?P<s2>\S+)\s+Rb;i;d\s+=\s+(?P<Rb>\S+)\s+sb\s+=\s+(?P<sb>\S+)\s+" \
                        "sel\s+=\s+(?P<sel>\S+)\s+s1\s+=\s+(?P<s1>\S+)\s+s\s+=\s+(?P<s>\S+)"
        output = []
        for i in re.finditer(regex_pattern, self.content, flags=re.DOTALL):
            temp_dict = {}
            for key, value in i.groupdict().items():
                if key in export_as_float:
                    temp_dict[key] = float(value)
                else:
                    temp_dict[key] = value
            output.append(temp_dict)

        return output


class UGT:
    def __init__(self, content: str):
        self.content = content

    @property
    def ugt_content(self):
        return re.search("(?P<ugt>grenstoestand.*Beta_dGEO)", self.content, flags=re.DOTALL).groupdict()["ugt"]

    @property
    def paal_zakking_data(self) -> dict:

        export_as_float = ["Fc_tot", "Rb_cal", "Rs_cal", "s2", "Rb", "sb", "sel", "s1", "s"]
        regex_pattern = "BEREKENING ZAKKING VOOR PAAL\s+(?P<paal_nummer>.*?)\s+BIJ SONDERING\s+(?P<sondering_naam>.*?)\s*\n.*?\n*" \
                        "Fc;tot;i\s+=\s+(?P<Fc_tot>\S+)\s+Rb;cal;max;i;d\s+=\s+(?P<Rb_cal>\S+)\s+Rs;cal;max;i;d\s+=\s+(?P<Rs_cal>\S+)\s+" \
                        "s2\s+=\s+(?P<s2>\S+)\s+Rb;i;d\s+=\s+(?P<Rb>\S+)\s+sb\s+=\s+(?P<sb>\S+)\s+" \
                        "sel\s+=\s+(?P<sel>\S+)\s+s1\s+=\s+(?P<s1>\S+)\s+s\s+=\s+(?P<s>\S+)"
        output = []

        for i in re.finditer(regex_pattern, self.ugt_content, flags=re.DOTALL):
            temp_dict = {}
            for key, value in i.groupdict().items():
                if key in export_as_float:
                    temp_dict[f"ugt_{key}"] = float(value)
                elif key == "sondering_naam":
                    temp_dict[key] = value
                else:
                    temp_dict[f"ugt_{key}"] = value
            output.append(temp_dict)

        return output

    @property
    def kleef_data(self):
        return kleef_list(self.ugt_content, "ugt")


class BGT:
    def __init__(self, content: str):
        self.content = content

    @property
    def bgt_content(self):
        return re.search("(?P<bgt>bruikbaarheidsgrenstoestand.*Beta_dBruikbaarheid)", self.content,
                         flags=re.DOTALL).groupdict()["bgt"]

    @property
    def paal_zakking_data(self) -> dict:

        export_as_float = ["Fc_tot", "Rb_cal", "Rs_cal", "s2", "Rb", "sb", "sel", "s1", "s"]
        regex_pattern = "BEREKENING ZAKKING VOOR PAAL\s+(?P<paal_nummer>.*?)\s+BIJ SONDERING\s+(?P<sondering_naam>.*?)\s*\n.*?\n*" \
                        "Fc;tot;i\s+=\s+(?P<Fc_tot>\S+)\s+Rb;cal;max;i;d\s+=\s+(?P<Rb_cal>\S+)\s+Rs;cal;max;i;d\s+=\s+(?P<Rs_cal>\S+)\s+" \
                        "s2\s+=\s+(?P<s2>\S+)\s+Rb;i;d\s+=\s+(?P<Rb>\S+)\s+sb\s+=\s+(?P<sb>\S+)\s+" \
                        "sel\s+=\s+(?P<sel>\S+)\s+s1\s+=\s+(?P<s1>\S+)\s+s\s+=\s+(?P<s>\S+)"
        output = []
        for i in re.finditer(regex_pattern, self.bgt_content, flags=re.DOTALL):
            temp_dict = {}
            for key, value in i.groupdict().items():
                if key in export_as_float:
                    temp_dict[f"bgt_{key}"] = float(value)
                elif key == "sondering_naam":
                    temp_dict[key] = value
                else:
                    temp_dict[f"bgt_{key}"] = value
            output.append(temp_dict)
        return output

    @property
    def kleef_data(self):
        return kleef_list(self.bgt_content, "bgt")


class Ontwerpberekening:
    def __init__(self, ontwerpberekening_content: str):
        self.content = ontwerpberekening_content
        self._grenstoestand_equ = GrenstoestandEqu(ontwerpberekening_content)
        self._ugt = UGT(self.content)
        self._bgt = BGT(self.content)
        # self._negatieve_kleef_blok = NegatieveKleef(self.content)
        # self._paal_zakking = PaalZakking(self.content)

    @property
    def grenstoestand_equ(self):
        return self._grenstoestand_equ

    @property
    def negatieve_kleef_blok(self):
        return self._negatieve_kleef_blok

    @property
    def paal_zakking(self):
        return self._paal_zakking

    @property
    def ugt(self):
        return self._ugt

    @property
    def bgt(self):
        return self._bgt

    @property
    def all_data(self) -> List[dict]:
        raise ValueError("Edit code below")
        output = []

        # for grenstoestand_equ, negatieve_kleef_blok, paal_zakking in zip(self.grenstoestand_equ,
        #                                                                  self.negatieve_kleef_blok,
        #                                                                  self.paal_zakking):
        #
        #
        # temp_dict = {**grenstoestand_equ.data,
        #              **negatieve_kleef_blok.data,
        #              **paal_zakking.data}
        # output.append(temp_dict)
        return output


# @property
# def paal_punt_niveau(self):
#     search_paal_punt_niveau = re.search("(?P<ontwerpberekening>\d+)\s+met PPN = (?P<ppn>\S+) m.", self.content)
#     if search_paal_punt_niveau is None:
#         raise NotImplementedError("Paalpuntniveau niet gevonden in for bestand.")
#     else:
#         return float(search_paal_punt_niveau.groupdict()["ppn"])
#
# @property
# def paal_punt_index(self):
#     search_paal_punt_niveau = re.search("(?P<ontwerpberekening>\d+)\s+met PPN = (?P<ppn>\S+) m.", self.content)
#     if search_paal_punt_niveau is None:
#         raise NotImplementedError("Paalpuntniveau niet gevonden in for bestand.")
#     else:
#         return int(search_paal_punt_niveau.groupdict()["ontwerpberekening"])
#

#
# @property
# def berekening_zakking(self):
#     compiled_regex = re.compile("""BEREKENING ZAKKING VOOR PAAL\s+(?P<paalnr>\S+) BIJ SONDERING DKM001

# Fc;tot;i =\s+(?P<Fc_tot>\S+)\s+Rb;cal;max;i;d\s+=\s+(?P<Rc_cal_max>\S+)\s+Rs;cal;max;i;d =\s+(?P<Rs_cal_max>\S+)
# s2\s+=\s+(?P<s2>\S+)\s+Rb;i;d\s+=\s+(?P<Rb>\S+)\s+sb\s+=\s+(?P<sb>\S+)
# sel\s+=\s+(?P<sel>\S+)\s+s1\s+=\s+(?P<s1>\S+)\s+s\s+=\s+(?P<s>\S+)""")
#         return compiled_regex.finditer(self.content)

class Berekeningstoestand:

    def __init__(self, berekenings_dict: Dict):
        self.berekenings_dict = berekenings_dict

    @property
    def sondering_naam(self):
        return int(self.berekenings_dict["sondering_naam"])

    @property
    def paalpuntniveau(self):
        return float(self.berekenings_dict["paalpuntniveau"])

    @property
    def qc_i_gem(self):
        return float(self.berekenings_dict["qc_i_gem"])

    @property
    def qc_ii_gem(self):
        return float(self.berekenings_dict["qc_ii_gem"])

    @property
    def qc_iii_gem(self):
        return float(self.berekenings_dict["qc_iii_gem"])

    @property
    def Deq(self):
        return float(self.berekenings_dict["Deq"])

    @property
    def alpha_p(self):
        return float(self.berekenings_dict["alpha_p"])

    @property
    def beta(self):
        return float(self.berekenings_dict["beta"])

    @property
    def s(self):
        return float(self.berekenings_dict["s"])

    @property
    def qb_max_i_voor(self):
        return float(self.berekenings_dict["qb_max_i_voor"])

    @property
    def qb_max_i_na(self):
        return float(self.berekenings_dict["qb_max_i_na"])

    @property
    def Rb_cal(self):
        return float(self.berekenings_dict["Rb_cal"])

    @property
    def Rs_cal(self):
        return float(self.berekenings_dict["Rs_cal"])

    @property
    def Rc_cal(self):
        return float(self.berekenings_dict["Rc_cal"])


class DFoundations():

    def __init__(self, foi_path: Union[str, Path]):
        self._foi_path = Path(foi_path).with_suffix(".foi")
        self._for_path = Path(foi_path).with_suffix(".for")
        self._fos_path = Path(foi_path).with_suffix(".fod")
        self._fod_path = Path(foi_path).with_suffix(".fos")
        self._err_path = Path(foi_path).with_suffix(".err")
        self._for = FOR(self.for_path.open().read())

        self.foi = FOI(self._foi_path.open().read())

        def validate_for():
            ...
            # content = self._for_path.open().read()
            # from collections import defaultdict
            # aantal_dict = defaultdict(lambda :0)
            # for ontwerpberekening in re.finditer(r" Ontwerpberekening.*?Beta_dBruikbaarheid = 0",content,flags=re.DOTALL):
            #     aantal_dict["equ"] += ontwerpberekening.group().count("BEREKENING GRENSTOESTAND EQU BIJ SONDERING")
            #     aantal_dict["qc;I;gem"] += ontwerpberekening.group().count("qc;I;gem")
            # aantal_equ += ontwerpberekening.group().count("BEREKENING GRENSTOESTAND EQU BIJ SONDERING")
            #
            # r"BEREKENING GRENSTOESTAND EQU BIJ SONDERING"

        validate_for()

    @property
    def foi_path(self):
        if self._foi_path.exists():
            return self._foi_path
        raise FileExistsError(f"Foi file niet gevonden op {self.foi_path}")

    @property
    def for_path(self):
        if self._for_path.exists():
            return self._for_path
        raise FileExistsError(f"For file niet gevonden op {self.for_path}")

    @property
    def fos_path(self):
        if self._fos_path.exists():
            return self._fos_path
        raise FileExistsError(f"Fos file niet gevonden op {self.fos_path}")

    @property
    def fod_path(self):
        if self._fod_path.exists():
            return self._fod_path
        raise FileExistsError(f"Fod file niet gevonden op {self.fod_path}")

    @property
    def err_path(self):
        return self._err_path

    @property
    def has_error_file(self):
        return self._err_path.exists()

    @property
    def foi_name(self):
        return self.foi_path.stem

    @property
    def excavation_depth(self):
        return self.foi.profiles.excavation_level

    @property
    def raw_data(self) -> pd.DataFrame:

        foi_name = self.foi_path.name
        ontgravingsniveau = self.excavation_depth
        meta_data_dict = dict(foi_name=foi_name, ontgravingsniveau=ontgravingsniveau)

        output = []
        for ontwerpberekening in self._for.ontwerpberekeningen:

            all_lines = ontwerpberekening.grenstoestand_equ.berekeningstoestanden + \
                        ontwerpberekening.ugt.kleef_data + \
                        ontwerpberekening.ugt.paal_zakking_data + \
                        ontwerpberekening.bgt.kleef_data + \
                        ontwerpberekening.bgt.paal_zakking_data

            sondering_namen = [line["sondering_naam"] for line in all_lines]
            sorted_uniek_sondering_namen = sorted(list(set(sondering_namen)), key=lambda x: sondering_namen.index(x))
            grenstoestand_dict = {line["sondering_naam"]: line for line in
                                  ontwerpberekening.grenstoestand_equ.berekeningstoestanden}

            ugt_kleef_dict = {line["sondering_naam"]: line for line in ontwerpberekening.ugt.kleef_data}
            ugt_zakking_dict = {line["sondering_naam"]: line for line in ontwerpberekening.ugt.paal_zakking_data}

            bgt_kleef_dict = {line["sondering_naam"]: line for line in ontwerpberekening.bgt.kleef_data}
            bgt_zakking_dict = {line["sondering_naam"]: line for line in ontwerpberekening.bgt.paal_zakking_data}

            for sondering_naam in sorted_uniek_sondering_namen:


                output.append({**{"pile_name": self.foi.preliminary_design.pile_name,
                                  "ksi3": self._for.ksi3,
                                  "ksi4": self._for.ksi4,
                                  "fugt": self.foi.positions_bearing_piles.limit_state_str_geo,
                                  "fbgt": self.foi.positions_bearing_piles.limit_state_service},
                               **meta_data_dict,
                               **grenstoestand_dict[sondering_naam],

                               **ugt_kleef_dict[sondering_naam],
                               **ugt_zakking_dict[sondering_naam],

                               **bgt_kleef_dict[sondering_naam],
                               **bgt_zakking_dict[sondering_naam]})
        return output

    @property
    def data_var_max_12(self) -> pd.DataFrame:
        def bereken_variatie_coeff(df):
            return df["Rc_cal_max"].std() / df["Rc_cal_max"].mean()

        df = pd.DataFrame.from_records(self.raw_data)
        output = []
        for key, sub_df in df.groupby(["pile_name", "paalpuntniveau"]):

            while len(sub_df) >= 2 and bereken_variatie_coeff(sub_df) > 0.12:
                sub_df = sub_df[sub_df["Rc_cal_max"] != sub_df["Rc_cal_max"].max()]

            if len(sub_df) >= 2:
                var_coefficient = bereken_variatie_coeff(sub_df)*100
            else:
                var_coefficient = None


            sb_gem = sub_df["bgt_sb"].mean()
            s1_gem = sub_df["bgt_s1"].mean()

            ksi3 = sub_df["ksi3"].iloc[0]
            ksi4 = sub_df["ksi4"].iloc[0]

            Rc_cal_max_gem = sub_df["Rc_cal_max"].mean()

            Rc_gem_ksi3 = Rc_cal_max_gem / ksi3

            Rc_min_ksi4 = min(sub_df["Rc_cal_max"].apply(lambda Rc_cal_max: Rc_cal_max / ksi4))

            Rc_d_ksi3 = Rc_gem_ksi3 / 1.2

            Rc_d_ksi4 = Rc_min_ksi4 / 1.2

            if Rc_gem_ksi3 < Rc_min_ksi4:
                Rc_d = Rc_d_ksi3
                fnk_d = sub_df["ugt_fnk_d"].mean()
            else:
                Rc_d = Rc_d_ksi4
                fnk_d = sub_df[sub_df["Rc_cal_max"] == min(sub_df["Rc_cal_max"])]["ugt_fnk_d"].iloc[0]

            output.append({"Foi name": sub_df["foi_name"].iloc[0],
                           "Ontgravingsniveau [m NAP+]": sub_df["ontgravingsniveau"].iloc[0],
                           "Paalpuntniveau [m NAP]": sub_df["paalpuntniveau"].iloc[0],
                           "Paaltype [-]": sub_df["pile_name"].iloc[0],
                           "Fugt [kN]": round(sub_df["fugt"].iloc[0]),
                           "Fbgt [kn]": round(sub_df["fbgt"].iloc[0]),
                           "Rc;d [kN]": round(Rc_d),
                           "Fc;net;d [kN]": round(fnk_d),
                           "Rc;net;d [kN]": round(Rc_d - fnk_d),
                           "s1;gem [m]": s1_gem,
                           "sb;gem [m]": sb_gem,
                           "var.coeff [%]": var_coefficient,
                           "CPT's [gebruikt]": ",".join(sub_df["sondering_naam"].to_list())
                           })
        return pd.DataFrame.from_records(output).iloc[::-1]

    @property
    def tabel_per_paaltype(self) -> pd.DataFrame:
        def bereken_variatie_coeff(df):
            return df["Rc_cal_max"].std() / df["Rc_cal_max"].mean()

        df = pd.DataFrame.from_records(self.raw_data)
        output = []
        for key, sub_df in df.groupby(["pile_name", "paalpuntniveau"]):

            while len(sub_df) >= 2 and bereken_variatie_coeff(sub_df) > 0.12:
                sub_df = sub_df[sub_df["Rc_cal_max"] != sub_df["Rc_cal_max"].max()]

            if len(sub_df) >= 2:
                var_coefficient = bereken_variatie_coeff(sub_df)*100
            else:
                var_coefficient = None

            ksi3 = sub_df["ksi3"].iloc[0]
            ksi4 = sub_df["ksi4"].iloc[0]

            Rc_cal_max_gem = sub_df["Rc_cal_max"].mean()

            Rc_gem_ksi3 = Rc_cal_max_gem / ksi3

            Rc_min_ksi4 = min(sub_df["Rc_cal_max"].apply(lambda Rc_cal_max: Rc_cal_max / ksi4))

            Rc_d_ksi3 = Rc_gem_ksi3 / 1.2

            Rc_d_ksi4 = Rc_min_ksi4 / 1.2

            paaltype =  sub_df["pile_name"].iloc[0]

            if Rc_gem_ksi3 < Rc_min_ksi4:
                Rc_d = Rc_d_ksi3
                fnk_d = sub_df["ugt_fnk_d"].mean()
            else:
                Rc_d = Rc_d_ksi4
                fnk_d = sub_df[sub_df["Rc_cal_max"] == min(sub_df["Rc_cal_max"])]["ugt_fnk_d"].iloc[0]

            output.append({"Ontgravingsniveau [m NAP+]": sub_df["ontgravingsniveau"].iloc[0],
                           "Paalpuntniveau [m NAP]": sub_df["paalpuntniveau"].iloc[0],
                           f"{paaltype} Rc;net;d [kN]": round(Rc_d - fnk_d)
                           })

        return output

def tabel_per_ontgravingsdiepte_en_paalpuntniveau(date_folder: Current_date_time) -> pd.DataFrame:
    """
    Maakt een tabel met als index de ontgravingsdiepte en het paalpuntniveau. De overige kolommen zijn het paaltype
    met Rc;net;d.


    Ontgravingsniveau [m NAP+]   Paalpuntniveau [m NAP]   Rect 320x320 Rc;net;d
    --------------------------- ------------------------ -----------------------
                             1                    -20.0                      12
                             1                    -20.5                      18
                             1                    -21.0                      32

    Parameters
    ----------
    date_folder : Path naar de date_folder. Uitgangspunt is dat daaronder ook de output_folder zit.

    Returns
    -------

    """
    # Create a temporary dictionary to store records by pilename.
    pile_dict = defaultdict(list)
    # Iterate over the for files
    for foi_file in Path(date_folder.output_folder).rglob("*.for"):
        # Create a DFoundatios instance of every file
        dfoundations = DFoundations(foi_file)
        # Collect the records for every pile in a list with dicts.
        # [{"Ontgravingsniveau [m NAP+]": ...,
        #   "Paalpuntniveau [m NAP]": ...,
        #  f"{paaltype} Rc;net;d [kN]": ...} , ... , ... , ... ]
        paaltype_records = dfoundations.tabel_per_paaltype
        # Extend any existing records with the newly acquired records.
        pile_dict[dfoundations.foi.preliminary_design.pile_name].extend(paaltype_records)

    temp_df = None
    for key,value in pile_dict.items():
        df = pd.DataFrame.from_records(value)

        if temp_df is None:
            temp_df = df
        else:
            temp_df = pd.merge(temp_df, df, on=["Ontgravingsniveau [m NAP+]", "Paalpuntniveau [m NAP]"], how="outer",
                               validate="one_to_one")
    return temp_df.sort_values(["Ontgravingsniveau [m NAP+]", "Paalpuntniveau [m NAP]"],
                               ascending=[True,False])