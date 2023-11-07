#
# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project.
#

import pandas as pd

from ...table_store import TableContainer
from .verb_input import VerbInput


def difference(input: VerbInput):
    input_table = input.get_input()
    others = input.get_others()
    others = pd.concat(others)

    output = input_table.merge(others, how="left", indicator=True)
    output = output[output["_merge"] == "left_only"]
    output = output.drop("_merge", axis=1)

    return TableContainer(table=output)
