import os
import pandas as pd
from django.test import TestCase, Client
from django.urls import reverse
from io import BytesIO

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class ChartAppTest(TestCase):
    """
    Test suite for the ChartApp application views.

    This class simulates HTTP requests to test the core functionalities:
    index page loading, general chart generation, and region-specific chart generation.
    """

    def setUp(self):
        """
        Set up the test environment: creates a temporary input_data.csv 
        file with predefined data for testing purposes.
        """
        data_dir = os.path.join(BASE_DIR, "static", "chartapp", "data")
        os.makedirs(data_dir, exist_ok=True)
        self.csv_path = os.path.join(data_dir, "input_data.csv")

        data = {
            "Область": ["Київська", "Київська", "Львівська", "Одеська"],
            "Місто/Район": ["Київ", "Бровари", "Львів", "Одеса"],
            "Значення": [100, 50, 200, 150]
        }
        df = pd.DataFrame(data)
        
        df.to_csv(self.csv_path, index=False, encoding='utf-8-sig')

        self.client = Client()

    def test_index_view(self):
        """
        Test that the main index page loads successfully (HTTP 200) 
        and displays the unique list of regions from the CSV data.
        """
        response = self.client.get(reverse('index')) 
        
        self.assertEqual(response.status_code, 200)
        
        self.assertTemplateUsed(response, 'chartapp/index.html')

        self.assertIn('regions', response.context)
        
        self.assertContains(response, "Київська")
        self.assertContains(response, "Одеська")

    def test_chart_png_view_success(self):
        """
        Test the general bar chart view: verifies that the view returns 
        a success status (HTTP 200) and the correct content type (image/png).
        """
        response = self.client.get(reverse('chart_png'))
        
        self.assertEqual(response.status_code, 200)
        
        self.assertEqual(response['Content-Type'], 'image/png')
        
        self.assertGreater(len(response.content), 1000)

    def test_region_chart_view_success(self):
        """
        Test the specific region chart view: verifies generation of the chart 
        for an existing region (Lvivska).
        """
        response = self.client.get(reverse('region_chart', args=['Київська']))
        
        self.assertEqual(response.status_code, 200)
        
        self.assertEqual(response['Content-Type'], 'image/png')
    
    def test_region_chart_view_not_found(self):
        """
        Test the specific region chart view: verifies that it correctly returns 
        HTTP 400 (Bad Request) when an unknown region name is passed.
        """
        response = self.client.get(reverse('region_chart', args=['Незвідана_область']))
        
        self.assertEqual(response.status_code, 400)
        
        self.assertIn("Такої області немає в даних", response.content.decode('utf-8'))