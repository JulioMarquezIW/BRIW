import sys
import printer_aux
import populate_data
import data
import functions

# Initialize information
data.people = populate_data.populate()
args = sys.argv
functions.check_args(args)
while True:
    printer_aux.print_options()
    functions.get_option()
    printer_aux.enter_to_continue()
