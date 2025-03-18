import requests
from datetime import datetime
import os


class ObisDoi:

    def __init__(self):
        self.title = None
        self.publicationYear = datetime.now().year
        self.url = None
        self.prefix = "10.25607"
        self.suffix = None
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
                self.related_identifiers.append({
                    "relationType": "HasPart",
                    "relatedIdentifier": metadata_record["citation_id"],
                    "relatedIdentifierType": "DOI"
                })
            else:
                self.related_identifiers.append({
                    "relationType": "HasPart",
                    "relatedIdentifier": metadata_record["url"],
                    "relatedIdentifierType": "URL"
                })

    def reserve(self):
        payload = {
            "data": {
                "attributes": {
                    # "event": "publish",
                    "prefix": self.prefix,
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
