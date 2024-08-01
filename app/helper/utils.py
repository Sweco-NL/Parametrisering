import re
from pathlib import Path


class DeltaresReader:
    def __init__(self, content=""):
        self.content = content

    def load_file(self, path):
        self.content = Path(path).open().read()
        return self

    def __str__(self):
        return self.content

    @property
    def lines(self):
        return self.content.splitlines()

    def extract_all(self, start, end=None):
        if end is None:
            end = f"END OF {start}"

        start_tag = f"[{start}]"
        end_tag = f"[{end}]"

        start_indexes = [nr for nr, line in enumerate(self.lines) if line == start_tag]
        end_indexes = [nr for nr, line in enumerate(self.lines) if line == end_tag]
        output = []
        for start_index, end_index in zip(start_indexes, end_indexes):
            output.append("\n".join(self.lines[start_index: end_index + 1]))
        return output

    def extract_first(self, start, end=None, must_have=True) -> str:
        result = list(self.extract_all(start, end))
        if len(result) == 1:
            return result[0]
        if must_have == False:
            return ""
        raise ValueError(f"Did not find 1 result but {len(result)}")

    def extract_all_tables(self, start, end=None, data_splitter=None, strip_data=True):
        records = []
        for block in DeltaresReader(self.content).extract_all(start, end):
            table = DeltaresReader(block).extract_table(start, end, data_splitter, strip_data)
            records.extend(table)
        return records

    def extract_table(self, start, end=None, data_splitter=None, strip_data=True):
        temp = DeltaresReader(DeltaresReader(self.content).extract_first(start, end))
        column_index_start = temp.lines.index("[COLUMN INDICATION]")
        column_index_end = temp.lines.index("[END OF COLUMN INDICATION]")
        data_index_start = temp.lines.index("[DATA]")
        data_index_end = temp.lines.index("[END OF DATA]")

        columns = temp.lines[column_index_start + 1: column_index_end]
        data = temp.lines[data_index_start + 1: data_index_end]

        records = []
        if data_splitter is None:
            for row in data:
                records.append({col: data for col, data in zip(columns, row)})
            return records
        elif data_splitter == "space":
            for row in data:
                row_dict = {}
                for col, value in zip(columns, row.strip().split()):
                    row_dict[col] = value
                records.append(row_dict)
            return records
        elif isinstance(data_splitter, str):
            compiled_splitter = re.compile(data_splitter)
            for row in data:
                row_dict = {}
                if compiled_splitter.findall(row):
                    conversion_dict = {"int": int,
                                       "float": float,
                                       "str": str,
                                       "bool": bool}
                    group_types = re.findall("\<(.*?)\d+\>", data_splitter)
                    regex_result = compiled_splitter.findall(row)

                    for col, group_type, value in zip(columns,
                                                      group_types,
                                                      regex_result[0]):
                        row_dict[col] = conversion_dict[group_type](value)
                    records.append(row_dict)
            return records
        elif isinstance(data_splitter, list):
            for row in data:
                row_dict = {}
                for col, (s, value_type), (e, _) in zip(columns, data_splitter[0:], data_splitter[1:]):
                    value = row[s:e]
                    if strip_data:
                        value = value.strip()
                    row_dict[col] = value_type(value)
                records.append(row_dict)
            return records


def extract_line_by_string(content, search_string):
    if content.count(search_string) == 0:
        raise ValueError(f"{search_string} not found in {content}.")
    elif content.count(search_string) > 1:
        raise ValueError(f"{search_string} found {content.count(search_string)} times in {content}.")
    else:
        for line in content.splitlines():
            if search_string in line:
                return line.split("=")


if __name__ == "__main__":
    shd_path = Path(r"C:\WebApplicatiesGeotechniek\apps_8080\tools\damwand_tool\test\TestUGTBGT.shd")
    verify_step65 = DeltaresReader(shd_path.open().read()).extract_first("VERIFY STEP 6.5 (SERVICEABILITY LIMIT STATE)")
    from pprint import pprint

    DeltaresReader(verify_step65).extract_table("RESUME", data_splitter=[0, 12, 25, 38, 51, 64, 70, 76, 82, 84, 86, 92])

    # with open(r"F:\webapp_data\trekpaal\2023_11_02_09_37_41\Verdiepte ligging.foi") as readfile:
    #     content = readfile.read()

    # print(find_all_blocks("PRELIMINARY DESIGN", content=content))
    # print(re.findall("\[PRELIMINARY DESIGN\].*?\[END OF PRELIMINARY DESIGN\]",content, flags=re.DOTALL))
