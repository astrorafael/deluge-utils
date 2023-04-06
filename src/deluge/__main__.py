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

import sys
import argparse
import os.path
import logging
#import logging.handlers
import traceback
import importlib


# -------------
# Local imports
# -------------

from . import  __version__


# -----------------------
# Module global variables
# -----------------------

log = logging.getLogger("deluge")

# -----------------------
# Module global functions
# -----------------------

def configureLogging(options):
	if options.verbose:
		level = logging.DEBUG
	elif options.quiet:
		level = logging.WARN
	else:
		level = logging.INFO
	
	log.setLevel(level)
	# Log formatter
	#fmt = logging.Formatter('%(asctime)s - %(name)s [%(levelname)s] %(message)s')
	fmt = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
	# create console handler and set level to debug
	if not options.no_console:
		ch = logging.StreamHandler()
		ch.setFormatter(fmt)
		ch.setLevel(level)
		log.addHandler(ch)
	# Create a file handler
	if options.log_file:
		#fh = logging.handlers.WatchedFileHandler(options.log_file)
		fh = logging.FileHandler(options.log_file)
		fh.setFormatter(fmt)
		fh.setLevel(level)
		log.addHandler(fh)


def python2_warning():
	if sys.version_info[0] < 3:
		log.warning("This software des not run under Python 2 !")


def setup(options):
	python2_warning()
	

# =================== #
# THE ARGUMENT PARSER #
# =================== #

def createParser():
	# create the top-level parser
	name = os.path.split(os.path.dirname(sys.argv[0]))[-1]
	parser    = argparse.ArgumentParser(prog=name, description="DELUGE KIT UTILITY")

	# Global options
	parser.add_argument('--version', action='version', version='{0} {1}'.format(name, __version__))
	group = parser.add_mutually_exclusive_group()
	group.add_argument('-v', '--verbose', action='store_true', help='Verbose output.')
	group.add_argument('-q', '--quiet',   action='store_true', help='Quiet output.')
	parser.add_argument('-nk','--no-console', action='store_true', help='Do not log to console.')
	parser.add_argument('--log-file', type=str, default=None, help='Optional log file')

	
	# --------------------------
	# Create first level parsers
	# --------------------------
	subparser = parser.add_subparsers(dest='command')
	parser_entries    = subparser.add_parser('kit',    help='Deluge Kit utils')
	

	# ----------------
	# Entries Commands
	# ----------------

	subparser = parser_entries.add_subparsers(dest='subcommand')

	parser_transf = subparser.add_parser('list', help='List Kit instruments info as CSV')
	parser_transf.add_argument('-i','--input-file',  type=str, required=True, help='Input XML file')
	parser_transf.add_argument('-o','--output-file', type=str, default=None, help='Optional output HTML file')

	return parser

# ================ #
# MAIN ENTRY POINT #
# ================ #

def main():
	'''
	Utility entry point
	'''
	try:
		options = createParser().parse_args(sys.argv[1:])
		configureLogging(options)
		setup(options)
		name = os.path.split(os.path.dirname(sys.argv[0]))[-1]
		command  = f"{options.command}"
		subcommand = options.subcommand
		try:
			command = importlib.import_module(command, package=name)
		except ModuleNotFoundError:	# when debugging module in git source tree ...
			command  = f".{options.command}"
			command = importlib.import_module(command, package=name)
		log.info(f"============== {name} {__version__} ==============")
		getattr(command, subcommand)(options)
	except KeyboardInterrupt as e:
		log.critical("[%s] Interrupted by user ", __name__)
	except Exception as e:
		log.critical("[%s] Fatal error => %s", __name__, str(e) )
		traceback.print_exc()
	finally:
		pass

main()

