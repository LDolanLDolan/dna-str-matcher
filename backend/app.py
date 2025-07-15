from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import read_database, str_counts, match_profile, regions
from os import environ

app = Flask(__name__)

# Keep the working CORS setup
CORS(app, origins="*", 
     methods=["GET", "POST", "OPTIONS"], 
     allow_headers=["Content-Type", "Authorization"])

HEADER_STRS, DB_ROWS = read_database('database.csv')

@app.route('/ping')
def ping():
    return {'status': 'ok'}

@app.route('/analyze', methods=['POST', 'OPTIONS'])
def analyze():
    # Handle preflight OPTIONS request
    if request.method == 'OPTIONS':
        response = jsonify({})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return response, 200
    
    try:
        data = request.get_json(force=True)
        dna = data.get('dna', '')
        custom_strs = data.get('strs') or HEADER_STRS
        
        counts = str_counts(dna, custom_strs)
        person = match_profile(DB_ROWS, counts) if set(custom_strs) == set(HEADER_STRS) else "Custom search - no db match"
        region_list = regions(dna, custom_strs)
        
        hint = None
        if region_list:
            starts = [r['start'] for r in region_list]
            ends = [r['end'] for r in region_list]
            hint = f'Potential gene-like region {min(starts)}–{max(ends)}'
        
        response = jsonify({
            'match': person,
            'str_counts': counts,
            'regions': region_list,
            'structure_hint': hint
        })
        
        # Keep working CORS headers
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
        
    except Exception as e:
        error_response = jsonify({'error': str(e)})
        error_response.headers.add('Access-Control-Allow-Origin', '*')
        return error_response, 500

if __name__ == '__main__':
    port = int(environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
