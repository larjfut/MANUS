# DV Locator System Architecture

## Overview
The DV Locator is a web-embeddable chatbot system that helps survivors and advocates find domestic violence and sexual assault resources based on location.

## System Components

### 1. Backend API (Flask)
- **Endpoint**: `/api/assistant`
- **Method**: POST
- **Input**: JSON with `message` field containing location (county, city, or ZIP)
- **Output**: JSON with `html` field containing formatted results

### 2. Data Layer
- **File**: `dv_orgs.csv`
- **Structure**: Contains organization details including coordinates, services, contact info
- **Fields**: name, address, city, county, zip, latitude, longitude, services, contact_name, contact_phone, contact_email, hotline_number, website_url, type

### 3. Core Logic
- **Geocoding**: Convert location input to coordinates
- **Distance Calculation**: Great-circle distance between user location and organizations
- **Result Filtering**: Return closest 5 organizations within 90 miles, or 5 closest overall if fewer than 5 within range

### 4. Frontend Interface
- **Form**: Simple input for location with submit button
- **Results Display**: Grid layout showing organization cards
- **Styling**: Self-contained CSS with trauma-informed design (purple theme)

## Data Flow
1. User enters location in web form
2. Frontend sends POST request to `/api/assistant`
3. Backend geocodes location to coordinates
4. System calculates distances to all organizations
5. Results filtered and formatted as HTML
6. Frontend displays results in card grid

## JSON Response Schema
```json
{
  "name": "Organization Name",
  "type": "DV" | "SA" | "Dual",
  "address": "123 Main St",
  "city": "City Name",
  "county": "County Name", 
  "zip": "12345",
  "latitude": 40.7128,
  "longitude": -74.0060,
  "distance_miles": 12.4,
  "services": ["Emergency shelter", "Counseling"],
  "contact": {
    "name": "Contact Person",
    "phone": "555-123-4567",
    "email": "contact@org.com",
    "hotline_number": "800-123-4567"
  },
  "website_url": "https://example.org"
}
```

## Geocoding Strategy
- For ZIP codes: Use built-in ZIP to coordinates lookup
- For cities/counties: Use geocoding service (Nominatim/OpenStreetMap API)
- Fallback: Manual coordinate lookup for common locations

## Distance Calculation
- Use Haversine formula for great-circle distance
- Input: Two coordinate pairs (lat1, lon1, lat2, lon2)
- Output: Distance in miles

## Error Handling
- Invalid location input: Return helpful error message
- No organizations found: Return TCFV contact information
- Network errors: Graceful degradation with retry options

