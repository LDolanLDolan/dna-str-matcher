from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import read_database, str_counts, match_profile, regions
from os import environ

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests (required for GitHub Pages)

# Load database and header STRs
HEADER_STRS, DB_ROWS = read_database('database.csv')

@app.route('/ping')
def ping():
    return {'status': 'ok'}

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json(force=True)
    dna = data.get('dna', '')
    custom_strs = data.get('strs') or HEADER_STRS

    # Count STRs
    counts = str_counts(dna, custom_strs)

    # Match profile only if using default STRs
    person = match_profile(DB_ROWS, counts) if set(custom_strs) == set(HEADER_STRS) else "Custom search - no db match"

    # Find regions for highlighting
    region_list = regions(dna, custom_strs)

    # Naive structure hint (just clustered STRs)
    hint = None
    if region_list:
        starts = [r['start'] for r in region_list]
        ends = [r['end'] for r in region_list]
        hint = f'Potential gene-like region {min(starts)}-{max(ends)}'

    return jsonify({
        'match': person,
        'str_counts': counts,
        'regions': region_list,
        'structure_hint': hint
    })

# Run app with correct host/port for Render.com
if __name__ == '__main__':
    port = int(environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
