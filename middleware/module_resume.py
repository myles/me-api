from __future__ import unicode_literals

import os
import glob

import yaml


def main(app, data):
    resume = {}

    for file in glob.glob(os.path.join(app.data_dir, 'resume/*.yaml')):
        section_name = os.path.basename(file).strip('.yaml')[3:]

        with open(file, 'r') as f:
            section_data = yaml.load(f)

        if section_data:
            resume[section_name] = section_data

    return resume
