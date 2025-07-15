
from flask import Flask, request, jsonify
from utils import read_database, str_counts, match_profile, regions

app = Flask(__name__)

HEADER_STRS, DB_ROWS = read_database('database.csv')

@app.route('/ping')
def ping():
    return {'status': 'ok'}

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json(force=True)
    dna = data.get('dna', '')
    custom_strs = data.get('strs') or HEADER_STRS
    counts = str_counts(dna, custom_strs)
    person = match_profile(DB_ROWS, counts) if set(custom_strs) == set(HEADER_STRS) else "Custom search - no db match"
    region_list = regions(dna, custom_strs)
    # very naive structure hint: dense cluster
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

if __name__ == '__main__':
    app.run(debug=True)
