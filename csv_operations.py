# -*- coding: utf-8 -*-

import os
import os.path
import csv


def write_csv_file(csv_path, items):
    with open(csv_path, 'w', newline='', encoding='utf-8') as csv_file:
        spam_writer = csv.writer(csv_file, delimiter='\t')
        for line in items:
            spam_writer.writerow(line)
    return csv_path
