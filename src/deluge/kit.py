# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Copyright (c) 2021
#
# See the LICENSE file for details
# see the AUTHORS file for authors
# ----------------------------------------------------------------------

#--------------------
# System wide imports
# -------------------

import os
import time
import logging
import datetime
import xml.etree.ElementTree as ET

import tabulate
import jinja2


# ----------------
# Module constants
# ----------------

HTML_TEMPLATE = 'kit-template.j2'

# -----------------------
# Module global variables
# -----------------------

log = logging.getLogger("deluge")

# ----------------------
# Command implementation
# ----------------------

def render(template_name, context):
    environment = jinja2.Environment(loader=jinja2.PackageLoader('deluge','templates'))
    return environment.get_template(template_name).render(context)


def parse_xml_file(input_file):
    try:
        tree = ET.parse(input_file)
        root = tree.getroot()
    except ET.ParseError:
        # Bad formed XML files are processed with this hack:
        #  - Skip lines 2 and 3 of such bad formed files
        # and reprocess the resulting string
        with open(input_file) as f:
            oldlines = f.readlines()
        lines = [oldlines[0]]
        lines.extend(oldlines[3:])
        print(lines)
        tree = ET.fromstring(''.join(lines))
        root = tree # fromstring directly returns an Element, not ElementTree
    table = []
    for sound in root.find('soundSources').findall('sound'):
        name = sound.find('name').text
        filename1 = sound.find('osc1').find('fileName').text
        #filename2 = sound.find('osc2').find('fileName').text
        table.append((name,filename1))
    return table

    
def generate_html(input_file, output_file, table):
    name = os.path.splitext(os.path.basename(input_file))[0]
    context = {'name': name, 'table': table}
    html_contents = render(HTML_TEMPLATE, context)
    with open(output_file, 'w') as outfile:
        outfile.write(html_contents)

# ----------------------
# COMMAND IMPLEMENTATION
# ----------------------


def list(options):
    log.info("Listing deluge kit info from input file {0}".format(options.input_file))
    
    table = parse_xml_file(options.input_file)
    print(tabulate.tabulate(table, tablefmt="outline", headers=["NAME","SAMPLES FILE"]))
    if(options.output_file):
        generate_html(options.input_file, options.output_file, table)


    
