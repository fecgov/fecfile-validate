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
args = parser.parse_args()
VERBOSE = args.verbose
DEBUG = args.debug
EXCEL_FILENAME = args.excel_filename

run_verification(EXCEL_FILENAME, VERBOSE, DEBUG)