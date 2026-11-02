import json

FILE_PATH = "data/raw/84184NED_observations.json"

with open(FILE_PATH, "r", encoding="utf-8") as file:
    observations = json.load(file)

years_to_check = ["2018JJ00", "2019JJ00", "2024JJ00"]

for year in years_to_check:
    print(f"\n{'=' * 65}")
    print(f"YEAR: {year}")
    print("=" * 65)

    for observation in observations:
        if (
            observation["Perioden"] == year
            and observation["Measure"] == "M002011"
            and observation["Pensioenuitvoerders"] == "T001424"
        ):
            print(
                f"Scheme: {observation['Pensioenregelingen']} | "
                f"Status: {observation['StatusPensioenaanspraken']} | "
                f"Value: {observation['Value']}"
            )