from flask import Blueprint, request, jsonify
import os
from src.dv_locator import DVLocator

assistant_bp = Blueprint('assistant', __name__)

# Initialize the DV Locator with the CSV data
csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'dv_orgs.csv')
locator = DVLocator(csv_path)

@assistant_bp.route('/assistant', methods=['POST'])
def assistant():
    """
    Main endpoint for the DV Locator assistant.
    Expects JSON with 'message' field containing location.
    Returns JSON with 'html' field containing formatted results.
    """
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({
                'error': 'Missing message field',
                'html': '<div class="empty-state">Please provide a location to search for resources.</div>'
            }), 400
        
        location = data['message'].strip()
        if not location:
            return jsonify({
                'error': 'Empty location',
                'html': '<div class="empty-state">Please provide a location to search for resources.</div>'
            }), 400
        
        # Find nearby organizations
        organizations = locator.find_nearby_organizations(location)
        
        # Format as HTML for the frontend
        html_results = locator.format_results_html(organizations)
        
        # Also provide JSON data for programmatic access
        json_results = locator.format_results_json(organizations)
        
        return jsonify({
            'html': html_results,
            'data': json_results,
            'location': location,
            'count': len(organizations)
        })
        
    except Exception as e:
        error_html = f'''
        <div class="empty-state">
            <h3>Sorry, something went wrong</h3>
            <p>We encountered an error while searching for resources. Please try again.</p>
            <p>For immediate help, please contact:</p>
            <p><strong>National Domestic Violence Hotline:</strong> <a href="tel:18007997233">1-800-799-7233</a></p>
            <p><strong>National Sexual Assault Hotline:</strong> <a href="tel:18006564673">1-800-656-4673</a></p>
        </div>
        '''
        
        return jsonify({
            'error': str(e),
            'html': error_html
        }), 500

@assistant_bp.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'organizations_loaded': len(locator.organizations)
    })

