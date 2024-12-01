import csv
from pathlib import Path

from pyrepa import analyze_project

INPUT_ROOT_PATH = "~/lfp/lfp-backend/src"
OUTPUT_PATH = "output/lfp_src_dependencies.csv"

if __name__ == "__main__":

    dependencies = analyze_project(
        Path(INPUT_ROOT_PATH).expanduser()
    )

    with open(
        OUTPUT_PATH, "w", newline="", encoding="utf-8",
    ) as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["calling", "called"])
        csv_writer.writerows(dependencies)
