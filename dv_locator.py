import csv
import math
import requests
import json
from typing import List, Dict, Tuple, Optional

class DVLocator:
    def __init__(self, csv_file: str):
        """Initialize the DV Locator with organization data from CSV."""
        self.organizations = []
        self.load_data(csv_file)
    
    def load_data(self, csv_file: str):
        """Load organization data from CSV file."""
        try:
            with open(csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # Parse services as a list
                    services = [s.strip() for s in row['services'].split(',')]
                    
                    org = {
                        'name': row['name'],
                        'address': row['address'],
                        'city': row['city'],
                        'county': row['county'],
                        'zip': row['zip'],
                        'latitude': float(row['latitude']),
                        'longitude': float(row['longitude']),
                        'services': services,
                        'contact': {
                            'name': row['contact_name'],
                            'phone': row['contact_phone'],
                            'email': row['contact_email'],
                            'hotline_number': row['hotline_number']
                        },
                        'website_url': row['website_url'],
                        'type': row['type']
                    }
                    self.organizations.append(org)
            print(f"Loaded {len(self.organizations)} organizations")
        except Exception as e:
            print(f"Error loading data: {e}")
            self.organizations = []
    
    def haversine_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculate the great circle distance between two points on Earth.
        Returns distance in miles.
        """
        # Convert latitude and longitude from degrees to radians
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        
        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        # Radius of Earth in miles
        r = 3956
        
        return c * r
    
    def geocode_location(self, location: str) -> Optional[Tuple[float, float]]:
        """
        Convert location string to coordinates.
        Returns (latitude, longitude) tuple or None if not found.
        """
        # Check if it's a ZIP code (5 digits)
        if location.strip().isdigit() and len(location.strip()) == 5:
            return self.geocode_zip(location.strip())
        
        # Try geocoding with Nominatim (OpenStreetMap)
        return self.geocode_nominatim(location)
    
    def geocode_zip(self, zip_code: str) -> Optional[Tuple[float, float]]:
        """Geocode ZIP code using a simple lookup or API."""
        # For demo purposes, using some common Texas ZIP codes
        zip_coords = {
            '78701': (30.2672, -97.7431),  # Austin
            '77002': (29.7604, -95.3698),  # Houston
            '75201': (32.7767, -96.7970),  # Dallas
            '78205': (29.4241, -98.4936),  # San Antonio
            '76102': (32.7555, -97.3308),  # Fort Worth
        }
        
        if zip_code in zip_coords:
            return zip_coords[zip_code]
        
        # Fallback to Nominatim for other ZIP codes
        return self.geocode_nominatim(f"{zip_code}, Texas, USA")
    
    def geocode_nominatim(self, location: str) -> Optional[Tuple[float, float]]:
        """Geocode using Nominatim (OpenStreetMap) API."""
        try:
            url = "https://nominatim.openstreetmap.org/search"
            params = {
                'q': location,
                'format': 'json',
                'limit': 1,
                'countrycodes': 'us'
            }
            headers = {'User-Agent': 'DV-Locator/1.0'}
            
            response = requests.get(url, params=params, headers=headers, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            if data:
                return float(data[0]['lat']), float(data[0]['lon'])
            
        except Exception as e:
            print(f"Geocoding error: {e}")
        
        return None
    
    def find_nearby_organizations(self, location: str) -> List[Dict]:
        """
        Find organizations near the given location.
        Returns up to 5 closest organizations.
        """
        # Geocode the input location
        coords = self.geocode_location(location)
        if not coords:
            return []
        
        user_lat, user_lon = coords
        
        # Calculate distances to all organizations
        org_distances = []
        for org in self.organizations:
            distance = self.haversine_distance(
                user_lat, user_lon,
                org['latitude'], org['longitude']
            )
            
            # Create result object with distance
            result = org.copy()
            result['distance_miles'] = round(distance, 1)
            org_distances.append(result)
        
        # Sort by distance
        org_distances.sort(key=lambda x: x['distance_miles'])
        
        # Apply the result rule:
        # If >= 5 orgs within 90 miles, return closest 5
        # If < 5 orgs within 90 miles, return 5 closest overall
        within_90_miles = [org for org in org_distances if org['distance_miles'] <= 90]
        
        if len(within_90_miles) >= 5:
            return within_90_miles[:5]
        else:
            return org_distances[:5]
    
    def format_results_json(self, organizations: List[Dict]) -> List[Dict]:
        """Format results as JSON according to the specified schema."""
        return organizations
    
    def format_results_html(self, organizations: List[Dict]) -> str:
        """Format results as HTML for embedding."""
        if not organizations:
            return '''
            <div class="empty-state">
                <h3>No organizations found in your area</h3>
                <p>We're sorry, but we couldn't find any domestic violence or sexual assault resources near your location.</p>
                <p>For immediate help, please contact:</p>
                <p><strong>National Domestic Violence Hotline:</strong> <a href="tel:18007997233">1-800-799-7233</a></p>
                <p><strong>National Sexual Assault Hotline:</strong> <a href="tel:18006564673">1-800-656-4673</a></p>
            </div>
            '''
        
        html_parts = []
        for org in organizations:
            services_list = ', '.join(org['services'])
            
            # Create Google Maps link
            maps_url = f"https://www.google.com/maps/search/?api=1&query={org['latitude']},{org['longitude']}"
            
            # Format contact info
            contact_info = []
            if org['contact']['phone']:
                contact_info.append(f"Phone: <a href=\"tel:{org['contact']['phone']}\">{org['contact']['phone']}</a>")
            if org['contact']['hotline_number']:
                contact_info.append(f"Hotline: <a href=\"tel:{org['contact']['hotline_number']}\">{org['contact']['hotline_number']}</a>")
            if org['contact']['email']:
                contact_info.append(f"Email: <a href=\"mailto:{org['contact']['email']}\">{org['contact']['email']}</a>")
            
            contact_html = '<br>'.join(contact_info)
            
            card_html = f'''
            <div class="org-card" data-type="{org['type']}">
                <h3>{org['name']} <span style="font-size: 0.8em; color: var(--lavender);">({org['type']})</span></h3>
                <p><strong>Distance:</strong> {org['distance_miles']} miles</p>
                <p><strong>Address:</strong> <a href="{maps_url}" target="_blank">{org['address']}, {org['city']}, {org['zip']}</a></p>
                <p><strong>Services:</strong> {services_list}</p>
                <p><strong>Contact:</strong><br>{contact_html}</p>
                {f'<p><strong>Website:</strong> <a href="{org["website_url"]}" target="_blank">Visit Website</a></p>' if org['website_url'] else ''}
            </div>
            '''
            html_parts.append(card_html)
        
        return ''.join(html_parts)

# Test the implementation
if __name__ == "__main__":
    locator = DVLocator('/home/ubuntu/dv_orgs.csv')
    
    # Test with different location types
    test_locations = ['Austin', 'Harris County', '75201', 'Houston, TX']
    
    for location in test_locations:
        print(f"\n--- Testing location: {location} ---")
        results = locator.find_nearby_organizations(location)
        print(f"Found {len(results)} organizations")
        
        for org in results[:2]:  # Show first 2 results
            print(f"- {org['name']} ({org['distance_miles']} miles)")

