import sys
import printer_aux
import populate_data
import data
import functions
import file_functions

# Initialize information
# data.people = populate_data.populate()
file_functions.read_data_from_files()
args = sys.argv
functions.check_args(args)
while True:
    printer_aux.print_options()
    functions.get_option()
    printer_aux.enter_to_continue()
