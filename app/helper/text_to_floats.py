from typing import List


def string_to_list_of_floats(input_str: str) -> List[float]:
    """
    Converts a string to a list of floats
    Parameters
    ----------
    input_str : The input string.

    Returns
    -------

    """
    # Example "1 2 3 4 5" -> [1.0,2.0,3.0,4.0,5.0]
    # Example "1
    # 2
    # 3
    # 4
    # 5
    #
    # " -> [1.0,2.0,3.0,4.0,5.0]
    #
    # Example "2.0 3.0" -> [2.0, 3.0]
    #
    # Example "2,0 3,0" -> [2.0, 3.0]
    #
    # Example "2,0 2,0 2,0 3,0" -> [2.0, 3.0]
    return list(set(float(item) for item in input_str.replace(",", ".").split() if len(item)))
