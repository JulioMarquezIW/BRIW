
def save_to_csv(people, drinks, filepath):

    # Lock for the bigest list
    biggest = []
    smallest = []
    if len(drinks) >= len(people):
        biggest = drinks
        smallest = people
    else:
        smallest = drinks
        biggest = people

    try:
        with open(filepath, "w") as drinks_file:
            drinks_file.write("Drinks\n")
            for drink in drinks:
                drinks_file.write(f"{drink}\n")
    except FileNotFoundError as filenotfound:
        print(
            f"Could no open the file {filepath}. /nError: {str(filenotfound)}")
    except Exception as e:
        print(
            f"Error opening the file {filepath}. /nError: {str(e)}")


people = ['Adrian', 'Alba', 'Julio']
drinks = ['water', 'cocacola', 'coffee']
filepath = "dataWithoutLibray.csv"
save_to_csv(people, drinks, filepath)
