from obisdois import ObisDoi
from dotenv import load_dotenv
import csv
import logging


logging.basicConfig(level=logging.INFO)


# licenses file from obis-export
with open("../licenses.tsv", "r") as f:
    reader = csv.DictReader(f, delimiter="\t")
    dataset_ids = [row["id"] for row in list(reader)]

doi = ObisDoi()
doi.suffix = "b89117cd"  # b89117cd-150e-4438-be3a-71a7b7e9a866
doi.title = "Ocean Biodiversity Information System (OBIS) Occurrence Data - 2025-03-25."
doi.set_related(dataset_ids)
doi.populate()
doi.url = "https://github.com/iobis/obis-open-data"
doi.doi = f"{doi.prefix}/obis.occurrence.{doi.suffix}"
doi.reserve()
