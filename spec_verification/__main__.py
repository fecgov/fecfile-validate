"""
This script checks for differences between this repo's JSON files and a spec spreadsheet.
The script will scan the working directory for a spreadsheet ending with ".xlsx" unless
the user passes in a valid  spreadsheet file name.

The JSON schema standard can be found here:
http://json-schema.org/
"""


from verify_against_spreadsheet import run_verification
import argparse


parser = argparse.ArgumentParser(
    description=""
    "This script checks for differences between this "
    "repo's JSON files and a spec spreadsheet.\n"
    "The script will scan the local directory for a "
    'spreadsheet ending with ".xlsx" unless the user\n'
    "passes in a valid  spreadsheet file name.\n\n"
)
parser.add_argument(
    "excel_filename",
    default=None,
    nargs="?",  # Allows for 0 or 1 filenames to be specified
    help="an excel filename that will be parsed to generate JSON schema docs",
)
parser.add_argument(
    "-v", "--verbose", help="record and print minor errors", action="store_true"
)
parser.add_argument(
    "-d",
    "--debug",
    help="Prints the names of sheets and fields as the script works",
    action="store_true",
)
parser.add_argument(
    "-s",
	"--save",
	help="Saves a copy of the report to a .txt file",
	action="store_true"
)
args = parser.parse_args()
VERBOSE = args.verbose  # Controls whether or not checks for minor errors are run
DEBUG = args.debug  	# If true, script will print its state in great detail as it runs
SAVE = args.save
EXCEL_FILENAME = args.excel_filename

run_verification(EXCEL_FILENAME, SAVE, VERBOSE, DEBUG,)
