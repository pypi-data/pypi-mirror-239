#
# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project.
#

import pandas as pd

from ...table_store import TableContainer
from .verb_input import VerbInput


def intersect(input: VerbInput):
    input_table = input.get_input()
    others = input.get_others()
    others = pd.concat(others)

    output = input_table.merge(others, how="left", indicator=True)
    output = output[output["_merge"] == "both"]
    output = output.drop("_merge", axis=1).reset_index(drop=True)

    return TableContainer(table=output)
