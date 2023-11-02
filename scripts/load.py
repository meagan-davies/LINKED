import csv
from linkers_website.apps.linkers.models import Linker

def run():
    # Put in the path to the file
    file_path = "./scripts/linker-database.csv"

    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row if it exists

        for linker in reader:
            aasequence = linker[1]
            length = int(linker[0])
            linker_type = linker[2]

            linker_instance = Linker(aasequence=aasequence, length=length, type=linker_type)
            linker_instance.save()
