"""
IO for islatu
"""

# Copyright (c) Andrew R. McCluskey
# Distributed under the terms of the MIT License
# author: Andrew R. McCluskey

import numpy as np
import pandas as pd


class I07Dat:
    """
    i07 dat file parsing.

    Attributes:
        file_path (str): The location of the ``.dat`` file on disk.
    """

    def __init__(self, file_path):

        self.file_path = file_path
        self.metadata, self.data = _parse(self.file_path)

    @property
    def q_vectors(self):
        if isinstance(self.data, pd.DataFrame):
            return np.array(self.data["qdcd"])
        else:
            raise ValueError("No")

    @property
    def images(self):
        if isinstance(self.data, pd.DataFrame):
            return self.data["file"]


def _parse(file_path):
    """
    Parsing the .dat file from I07.

    Args:
        (str): The ``.dat`` file to be read.
    
    Returns:
        (dict): The metadata from the ``.dat`` file. 
        (pd.DataFrame): The data from the ``.dat`` file. 
    """
    f_open = open(file_path, "r")
    # Neither the data nor the metadata are being read yet.
    data_reading = False
    metadata_reading = False

    # Create the dictionaries to be populated.
    data_dict = {}
    metadata_dict = {}
    # Create the list to be filled with lists for each line
    data_lines = []

    for line in f_open:
        # This string incidates the start of the metadata.
        if "<MetaDataAtStart>" in line:
            metadata_reading = True
        # This string indicates the end of the metadata.
        if "</MetaDataAtStart>" in line:
            metadata_reading = False
        # This string indicates the start of the data.
        if " &END" in line:
            data_reading = True
            # Set counter to minus two, such that when is
            # reaches the data it is 0.
            count = -2
        # When the metadata section is being read populate the metadata_dict
        if metadata_reading:
            if "=" in line:
                metadata_in_line = []
                for i in line.split("=")[1:]:
                    try:
                        j = float(i)
                    except ValueError:
                        j = i
                    metadata_in_line.append(j)
                metadata_dict[line.split("=")[0]] = metadata_in_line
        # When the data section is being read, make the list of the zeroth line
        # the titles and everything after is the data_lines list of lists.
        if data_reading:
            count += 1
            if count == 0:
                titles = line.split()
            if count > 0:
                data_lines.append(line.split())
    f_open.close()
    # Sort the data_lines list of lists to transpore and make into a dict where
    # the keys are the titles.
    for j in range(len(data_lines[0])):
        list_to_add = []
        for i in range(len(data_lines)):
            try:
                list_to_add.append(float(data_lines[i][j]))
            except ValueError:
                list_to_add.append(data_lines[i][j])
        data_dict[titles[j]] = list_to_add
    return metadata_dict, pd.DataFrame(data_dict)
