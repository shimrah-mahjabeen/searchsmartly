from django.test import TestCase

# Create your tests here.
from unittest.mock import patch, MagicMock, mock_open
from pandas import DataFrame
import pandas as pd
from xml.etree import ElementTree as ET
from poi.management.commands.import_poi_data import Command


class ImportPoisCommandTestCase(TestCase):
    @patch('poi.management.commands.import_poi_data.pd.read_csv')
    @patch('poi.management.commands.import_poi_data.Command.create_or_update_data')
    def test_import_csv(self, mock_create_or_update_data, mock_read_csv):
        mock_data = [
            {"poi_id": "1", "poi_name": "Test POI CSV", "poi_category": "Restaurant", "poi_latitude": "34.22", "poi_longitude": "-118.62", "poi_ratings": "{3.0,4.0,3.0,5.0,2.0,3.0}"}
        ]
        mock_df_iter = (DataFrame([row]) for row in mock_data)

        mock_read_csv.return_value = mock_df_iter
        command_instance = Command().import_csv('dummy/path/test_pois.csv')

        ratings_list = [3.0, 4.0, 3.0, 5.0, 2.0, 3.0]
        avg_rating = sum(ratings_list) / len(ratings_list)

        mock_create_or_update_data.assert_called_once_with({
            "external_ID": "1",
            "name": "Test POI CSV",
            "latitude": 34.22,
            "longitude": -118.62,
            "category": "Restaurant",
            "avg_rating": avg_rating
        })


    @patch('poi.management.commands.import_poi_data.Command.create_or_update_data')
    @patch('builtins.open', new_callable=mock_open, read_data='[{"id": "2", "name": "Test POI JSON", "coordinates": {"latitude": 34.22, "longitude": -118.62}, "category": "Restaurant", "ratings": [3.0, 4.0, 3.0, 5.0, 2.0, 3.0]}]')
    def test_import_json(self, mock_file_open, mock_create_or_update_data):

        command_instance = Command().import_json('dummy/path/test_pois.json')

        ratings_list = [3.0, 4.0, 3.0, 5.0, 2.0, 3.0]
        avg_rating = sum(ratings_list) / len(ratings_list)

        mock_create_or_update_data.assert_called_once_with({
            "external_ID": "2",
            "name": "Test POI JSON",
            "latitude": 34.22,
            "longitude": -118.62,
            "category": "Restaurant",
            "avg_rating": avg_rating
        })

    @patch('poi.management.commands.import_poi_data.Command.create_or_update_data')
    @patch('xml.etree.ElementTree.parse')
    def test_import_xml(self, mock_et_parse, mock_create_or_update_data):
        # Mock XML structure
        xml_string = """
        <root>
            <DATA_RECORD>
                <pid>1</pid>
                <pname>Test POI XML</pname>
                <pcategory>Restaurant</pcategory>
                <platitude>34.22</platitude>
                <plongitude>-118.62</plongitude>
                <pratings>3, 4, 3, 5, 2, 3</pratings>
            </DATA_RECORD>
        </root>
        """
        root = ET.fromstring(xml_string)
        mock_et_parse.return_value = MagicMock(getroot=MagicMock(return_value=root))
        command_instance = Command().import_xml('dummy/path/test_pois.xml')

        ratings_list = [3, 4, 3, 5, 2, 3]
        avg_rating = sum(ratings_list) / len(ratings_list)

        mock_create_or_update_data.assert_called_once_with({
            "external_ID": "1",
            "name": "Test POI XML",
            "latitude": 34.22,
            "longitude": -118.62,
            "category": "Restaurant",
            "avg_rating": avg_rating
        })

