from obisdois import ObisDoi
from dotenv import load_dotenv
import csv
import logging


logging.basicConfig(level=logging.INFO)


with open("data/identifiers.csv", "r") as f:
    reader = csv.DictReader(f)
    dataset_ids = [row["dataset_id"] for row in list(reader)]

doi = ObisDoi()
doi.suffix = "234a34a8"
doi.title = "Custom OBIS export on 2023-06-28: The uncharted geographic and ecological niche boundaries of marine fishes."
doi.set_related(dataset_ids)
doi.populate()
doi.export_related("data/datasets.tsv")
doi.reserve()
