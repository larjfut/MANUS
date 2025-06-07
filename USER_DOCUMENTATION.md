# DV Locator System - User Documentation

## Overview
The DV Locator is a web-embeddable chatbot system that helps survivors and advocates quickly find domestic violence (DV) and sexual assault (SA) resources based on location. The system provides a trauma-informed interface with a soothing purple color scheme and displays the closest 5 organizations within 90 miles of the user's location.

## System Components

### 1. Backend API (Flask)
- **Location**: `/home/ubuntu/dv-locator-api/`
- **Main file**: `src/main.py`
- **API endpoint**: `/api/assistant` (POST)
- **Health check**: `/api/health` (GET)

### 2. Frontend Interface
- **Location**: `/home/ubuntu/dv-locator-api/src/static/index.html`
- **Features**: Responsive design, trauma-informed styling, accessibility support

### 3. Data File
- **Location**: `/home/ubuntu/dv-locator-api/dv_orgs.csv`
- **Contains**: 12 sample organizations across Texas with complete contact information

## Quick Start

### Running Locally
1. Navigate to the project directory:
   ```bash
   cd /home/ubuntu/dv-locator-api
   ```

2. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```

3. Start the server:
   ```bash
   python src/main.py
   ```

4. Open your browser to: `http://localhost:5000`

### Using the System
1. Enter a location (city, county, or ZIP code) in the search box
2. Click "Find Resources" to search for nearby organizations
3. View results displayed as cards with contact information
4. Click addresses to open in Google Maps
5. Click phone numbers or emails to contact organizations directly

## API Usage

### Search for Resources
```bash
curl -X POST http://localhost:5000/api/assistant \
  -H "Content-Type: application/json" \
  -d '{"message": "Austin, TX"}'
```

### Response Format
```json
{
  "html": "<div class=\"org-card\">...</div>",
  "data": [
    {
      "name": "Safe Haven Shelter",
      "type": "DV",
      "address": "123 Main Street",
      "city": "Austin",
      "county": "Travis",
      "zip": "78701",
      "latitude": 30.2672,
      "longitude": -97.7431,
      "distance_miles": 0.3,
      "services": ["Emergency shelter", "Counseling", "Legal advocacy"],
      "contact": {
        "name": "Sarah Johnson",
        "phone": "512-555-0101",
        "email": "sarah@safehaven.org",
        "hotline_number": "800-799-7233"
      },
      "website_url": "https://safehaven.org"
    }
  ],
  "location": "Austin, TX",
  "count": 5
}
```

## Customization

### Adding Organizations
Edit the `dv_orgs.csv` file to add new organizations. Required fields:
- name, address, city, county, zip
- latitude, longitude (for distance calculations)
- services (comma-separated list)
- contact_name, contact_phone, contact_email, hotline_number
- website_url, type (DV, SA, or Dual)

### Styling Changes
Modify the CSS variables in `src/static/index.html`:
```css
:root {
  --purple-dk: #11001C;    /* Dark background */
  --purple-mid: #220135;   /* Card background */
  --purple-accent: #520380; /* Accent color */
  --lavender: #AC95C1;     /* Text highlights */
  --text: #EEE6F6;         /* Main text */
}
```

### Geocoding Configuration
The system uses OpenStreetMap's Nominatim service for geocoding. For production use, consider:
- Adding API keys for commercial geocoding services
- Implementing rate limiting
- Adding caching for frequently searched locations

## Deployment Options

### Option 1: Local Development
- Use the built-in Flask development server
- Suitable for testing and local demonstrations

### Option 2: Production Deployment
- Use a WSGI server like Gunicorn
- Configure reverse proxy with Nginx
- Set up SSL certificates for HTTPS
- Configure environment variables for production settings

### Option 3: Cloud Deployment
- Deploy to platforms like Heroku, AWS, or Google Cloud
- Ensure all dependencies are listed in `requirements.txt`
- Configure environment variables for database connections if needed

## Security Considerations

### For Production Use
1. **Environment Variables**: Store sensitive configuration in environment variables
2. **HTTPS**: Always use HTTPS in production to protect user privacy
3. **Rate Limiting**: Implement rate limiting to prevent abuse
4. **Input Validation**: The system includes basic input validation, but consider additional sanitization
5. **CORS**: Currently configured to allow all origins; restrict in production

### Privacy Protection
- The system doesn't store user search queries
- No personal information is collected or logged
- All searches are processed in real-time without persistence

## Troubleshooting

### Common Issues
1. **Port Already in Use**: Change the port in `src/main.py` if 5000 is occupied
2. **CSV Not Found**: Ensure `dv_orgs.csv` is in the project root directory
3. **Geocoding Failures**: Check internet connection and Nominatim service availability
4. **CORS Errors**: Ensure Flask-CORS is installed and configured

### Logs and Debugging
- Enable Flask debug mode for detailed error messages
- Check browser console for JavaScript errors
- Monitor network requests in browser developer tools

## Support and Maintenance

### Regular Updates
- Update organization contact information regularly
- Monitor geocoding service availability
- Test functionality with new browser versions
- Update dependencies for security patches

### Monitoring
- Monitor API response times
- Track search success rates
- Monitor geocoding service usage
- Check for broken links in organization websites

## Contact Information
For technical support or questions about the DV Locator system, refer to the system documentation or contact your technical administrator.

