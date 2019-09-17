
def save_to_csv(people, drinks, filepath):

    lines = []
    titles = ["People", "Favourite Drinks", "Available Drinks"]

    # try:
    #     with open(filepath, "w") as csv_file:

    # except FileNotFoundError as filenotfound:
    #     print(
    #         f"Could no open the file {filepath}. /nError: {str(filenotfound)}")
    # except Exception as e:
    #     print(
    #         f"Error opening the file {filepath}. /nError: {str(e)}")


people = ['Adrian', 'Alba', 'Julio']
drinks = ['water', 'cocacola', 'coffee']
filepath = "data/data.csv"
save_to_csv(people, drinks, filepath)
