import csv
import pandas as pd
import re
import json
import xml.etree.ElementTree as ET
from django.core.management.base import BaseCommand
from poi.models import PointOfInterest

class Command(BaseCommand):
    """
    Metadata about this command.
    """
    help = "Import POI data from CSV, JSON and XML files."

    def add_arguments(self, parser):
        """
        Entry point for subclassed commands to add custom arguments.
        """
        parser.add_argument("file_paths", nargs="+", type=str)

    def handle(self, *args, **options):
        """
        The actual logic of the command. Subclasses must implement
        this method.
        """
        for file_path in options["file_paths"]:
            if file_path.endswith(".csv"):
                self.import_csv(file_path)
            elif file_path.endswith(".json"):
                self.import_json(file_path)
            elif file_path.endswith(".xml"):
                self.import_xml(file_path)
            else:
                self.stdout.write(self.style.ERROR(f"Unsupported file type: {file_path}"))

    def import_csv(self, file_path):
        with pd.read_csv(file_path, chunksize=1) as csv_file:
            for chunk in csv_file:
                try:
                    ratings_list = self.parse_ratings(str(chunk["poi_ratings"]))
                    avg_rating = sum(ratings_list) / len(ratings_list) if ratings_list else 0
                    latitude = float(chunk["poi_latitude"].iloc[0])
                    longitude = float(chunk["poi_longitude"].iloc[0])
                    self.create_or_update_data({
                        "external_ID": chunk["poi_id"].iloc[0],
                        "name": chunk["poi_name"].iloc[0],
                        "latitude": latitude,
                        "longitude": longitude,
                        "category": chunk["poi_category"].iloc[0],
                        "avg_rating": avg_rating
                    })
                except ValueError as e:
                    self.stdout.write(self.style.ERROR(f"Error processing row: {e}"))
                    continue

    def import_json(self, file_path):
        with open(file_path, mode="r") as json_file:
            json_data = json.load(json_file)
            for item in json_data:
                avg_rating = sum(item["ratings"]) / len(item["ratings"]) if item["ratings"] else 0
                self.create_or_update_data({
                    "external_ID": item["id"],
                    "name": item["name"],
                    "latitude": item["coordinates"]["latitude"],
                    "longitude": item["coordinates"]["longitude"],
                    "category": item["category"],
                    "avg_rating": avg_rating
                })

    def import_xml(self, file_path):
        tree = ET.parse(file_path)
        root = tree.getroot()
        for item in root.findall("DATA_RECORD"):
            ratings_str = item.find("pratings").text
            ratings = [int(r) for r in ratings_str.split(",")] if ratings_str else []
            avg_rating = sum(ratings) / len(ratings) if ratings else 0
            self.create_or_update_data({
                "external_ID": item.find("pid").text,
                "name": item.find("pname").text,
                "latitude": float(item.find("platitude").text),
                "longitude": float(item.find("plongitude").text),
                "category": item.find("pcategory").text,
                "avg_rating": avg_rating
            })

    def create_or_update_data(self, poi_data):
        poi, created = PointOfInterest.objects.update_or_create(
            external_ID=poi_data["external_ID"],
             defaults={
                "name": poi_data["name"],
                "latitude": poi_data["latitude"],
                "longitude": poi_data["longitude"],
                "category": poi_data["category"],
                "avg_rating": poi_data["avg_rating"]
            }
        )
        action = "Created" if created else "Updated"
        self.stdout.write(self.style.SUCCESS(f"{action} PoI: {poi.name} with external ID {poi.external_ID}"))

    def parse_ratings(self, ratings_str):
        # Strip curly braces and parse the string into a list of floats
        match = re.search(r"\{(.*?)\}", ratings_str)
        if match:
            numbers_str = match.group(1)
            numbers_str_list = numbers_str.split(",")
            numbers_float_list = [float(num.strip()) for num in numbers_str_list]
            return numbers_float_list
        else:
            return []