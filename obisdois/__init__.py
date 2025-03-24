import requests
from datetime import datetime
import os
import logging
import csv
import re


pattern = re.compile(r'10\.\S+')
url_pattern = re.compile(r'^(https?://\S+)$')
doi_pattern = re.compile(r'^10\.\d{4,9}\/[-._;()/:a-zA-Z0-9]+$')


def fix_doi(input: str):
    return input.replace("%2F", "/")


class ObisDoi:

    def __init__(self):
        self.title = None
        self.publicationYear = datetime.now().year
        self.url = None
        self.prefix = "10.25607"
        self.suffix = None
        self.types = {
            "ris": "DATA",
            "bibtex": "misc",
            "citeproc": "dataset",
            "schemaOrg": "Dataset",
            "resourceTypeGeneral": "Dataset"
        }
        self.creators = [
            {
                "name": "Ocean Biodiversity Information System (OBIS)",
                "nameType": "Organizational",
            }
        ]
        self.related_identifiers = []
        self.publisher = "Ocean Biodiversity Information System (OBIS)"

    def set_related(self, dataset_ids):
        self.related_identifiers = []
        for dataset_id in dataset_ids:
            metadata_record = requests.get(f"https://api.obis.org/dataset/{dataset_id}").json()["results"][0]
            if metadata_record["citation_id"] is not None:
                if "doi" in metadata_record["citation_id"] or metadata_record["citation_id"].startswith("10."):
                    match = pattern.search(metadata_record["citation_id"].strip())
                    if match:
                        identifier = match.group()
                    else:
                        raise Exception(f"No DOI found in citation identifier: {metadata_record['citation_id']}")
                    identifier_type = "DOI"
                elif metadata_record["citation_id"].startswith("http"):
                    identifier = metadata_record["citation_id"].strip()
                    identifier_type = "URL"
                else:
                    identifier = metadata_record["url"].strip()
                    identifier_type = "URL"
            else:
                identifier = metadata_record["url"].strip()
                identifier_type = "URL"
            
            if identifier_type == "DOI":
                identifier = fix_doi(identifier)

            if not bool(url_pattern.match(identifier) or doi_pattern.match(identifier)):
                raise Exception(f"Invalid identifier for {dataset_id}: {identifier}")
            
            self.related_identifiers.append({
                "relationType": "HasPart",
                "relatedIdentifier": identifier,
                "relatedIdentifierType": identifier_type
            })
            logging.info(f"Added {dataset_id}: {identifier_type} {identifier}")

    def export_related(self, export_path: str):
        with open(export_path, "w") as f:
            writer = csv.DictWriter(f, fieldnames=["related_identifier"], delimiter="\t")
            writer.writeheader()
            for related_identifier in self.related_identifiers:
                writer.writerow({
                    "related_identifier": related_identifier["relatedIdentifier"]
                })

    def reserve(self):
        payload = {
            "data": {
                "attributes": {
                    # "event": "publish",
                    "prefix": self.prefix,
                    "types": self.types,
                    "doi": f"{self.prefix}/obis.export.{self.suffix}",
                    "creators": self.creators,
                    "titles": [{
                        "title": self.title
                    }],
                    "publisher": self.publisher,
                    "publicationYear": datetime.now().year,
                    "url": f"https://obis.org/export/{self.suffix}",
                    "relatedIdentifiers": self.related_identifiers
                }
            }
        }

        headers = {
            "Content-Type": "application/vnd.api+json"
        }
        response = requests.post("https://api.datacite.org/dois", json = payload, headers=headers, auth=(os.getenv("DOI_USER"), os.getenv("DOI_PASSWORD")))
        return(response.json())
