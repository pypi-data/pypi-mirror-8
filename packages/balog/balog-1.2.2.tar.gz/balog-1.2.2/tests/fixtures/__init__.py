from __future__ import unicode_literals
import json
import os

import my_consumers


def get_for_reals_path(file_name):
    return os.path.join(
        os.path.dirname(
            os.path.realpath(__file__)
        ),
        file_name
    )


def load_json(path):
    path = get_for_reals_path(path)
    with open(path) as f:
        return json.load(f)


def load_text(path):
    path = get_for_reals_path(path)
    return open(path).read()
