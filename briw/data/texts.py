
NOT_EMPTY = 'Cannot be empty, please retry'
ENTER_NAME = 'Enter the name (Just press enter to abort): '
ENTER_FAVOURITE_DRINK = 'Enter the favourite drink: '
NEW_PERSON = 'NEW PERSON DETAILS ->'
PRESS_ENTER = 'Please press enter to continue...'
PEOPLE = 'people'
DRINK = 'drink'
DRINKS = 'drinks'
ROUNDS = 'rounds'
INCORRECT_NUMBER_ARGUMENTS = 'Incorrect number of arguments'
ENTRY_INTEGER = 'Please entry an integer.'
DRINK_NAME = 'Enter the drink name please, (Just press enter to abort): '
ENTER_OPTION = 'Enter the option (0): '
INCORRECT_OPTION = 'Incorrect option, please retry: '
ERROR_FILE = 'The previous data will not be loaded, but you can still use the application.'
ENTRY_BOOLEAN = 'Please enter Y or N.'
QUESTION_ADD_DRINK = 'Do you want to add the favourite drink? (y/N): '
NOT_FAVOURITE_DRINK = 'No favorite drink for now'
ENTER_DRINK_ID = 'Enter the drink ID please (0 to abort): '
ENTER_PERSON_ID = 'Enter the person ID please (0 to abort): '
FAVOURITE_DRINK_UPDATED = 'Favourite drink updated. =)'
WANT_TO_SAVE = 'Do you want to save all your changes? (y/N): '
ALL_SAVED = "\n\tALL DATA SAVED!!"
DUPLICATE_NAME = "Duplicate name, please retry:"
ROUND_FAVOURITE_DRINKS = "Do you want to place an order for all your classmates with their favorite drinks? (y/N): "
ALL_PEOPLE_WANT_DRINKS = "Everybody wants drinks? (y/N): "
ASK_PEOPLE_IDS = "Add the ID of a list of ID separated by commas of the persons who want a drink (just press enter to abort): "
PEOPLE_WHO_WANT_DRINK = "People who want drinks"
ROUND_DATE = "Round date : "
NO_ROUNDS = "No rounds saved"
PEOPLE_WITHOUT_FAVOURITE_DRINK = "The next list of people doesn't have a favorite drink. Please select a drink for each one."
ASK_BREWER = "Who's going to prepare the round? Please enter the id, just press enter to abort: "
BREWER = "Brewer"
MORE_ROUNDS = "Show more rounds?(y/N):  "
ROUND_ID = "Round id"
CREATED_ROUND = "Round created!"
STATUS = "Status"
CLOSE = "Close"
OPEN = "Open"
CREATED_ORDER = "Order added!"
OPEN_ROUND_INFO = "There is already an open round, join it or close it to start a new one."
NOT_OPEN_ROUND = "There are no open rounds."
CONFIRM_CLOSE_ROUND = "Are you sure you want to close the round? (y/N): "
ROUND_CLOSED = "Round closed!"
ORDER_NOT_ADDED = "the new order couldn't be saved."
ROUND_NOT_ADDED = "the new round couldn't be saved."
PERSON_NOT_ADDED = "the new user couldn't be saved."
DRINK_NOT_ADDED = "the new drink couldn't be saved."
ROUND_NOT_CLOSED = "the round couldn't be closed."
DATABASE_ERROR = 'Database error, '
FAVUOIRTE_DRINK_NOT_SETTED = 'favourite drink will not be setted'
NOT_ROUNDS = 'There are no rounds'
NOT_ORDERS = 'There are no orders'


DATE_FORMAT = "%m/%d/%Y, %H:%M:%S"

GOODBYE = "\n\tGOODBYE!!\n\n"

AVAILABLE_ARGUMENTS_OPTIONS = """
    Only one argument available.
    Available arguments:
    -> get-people
    -> get-drinks
"""

OPTIONS = """

        WELCOME TO BrIW!!

        [1] Get Drinks
        [2] Get People
        [3] Get Preferences
        [4] Add drink
        [5] Add people
        [6] Set favourite drink
        [7] Create a round
        [8] Add order to round
        [9] Close open round
        [10] Print rounds
        [11] Help
        [0] Exit

    """


HELP_MESSAGE = """

    This is a project that allows to store and manage the people of a group and their favorite drinks, facilitating the interaction of the team when requesting a drink.

    Once the project is started, you can choose any of the available options, which will guide you through simple steps, if necessary interaction, to perform the different actions available.

    The project will continue to ask for any option, unless you choose the option zero number, in this case, the program will close.

    The value between () indicate the default value.

    Thanks and enjoy.

"""
