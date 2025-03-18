from obisdois import ObisDoi
from dotenv import load_dotenv


doi = ObisDoi()
doi.suffix = "aaaaaa"
doi.title = "OBIS export"
dataset_ids = ["8b0d5fdd-6a3f-48c7-a4aa-84f39f2df647", "d2df1c14-912e-4f8b-b1aa-2877cc0f4793"]
doi.set_related(dataset_ids)
doi.reserve()
