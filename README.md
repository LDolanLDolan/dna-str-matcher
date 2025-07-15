
# DNA STR Matcher+

Web‑based edition of Harvard CS50's **DNA** problem — with four powerful enhancements:

1. **Custom STR Search** – enter any STRs you like.
2. **Repeated Region Highlighting** – see runs highlighted in your sequence.
3. **Structure Viewer** – quick hint of dense STR clusters (pseudo gene region).
4. **REST API** – `/analyze` endpoint for programmatic access.

## Live Demo
- **Frontend:** GitHub Pages  
- **Backend:** Render.com (`/analyze` JSON API)

## Quickstart (local)

```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python app.py
# Visit http://127.0.0.1:5000
```

## Deploy

### 1⃣  Render (Backend)

1. Create a new **Web Service**:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python app.py`
2. Add a **`PORT`** environment variable (Render auto‑populates).
3. Note the base URL (e.g. `https://dna-str-matcher.onrender.com`).

### 2⃣  GitHub Pages (Frontend)

1. Change `apiBase` in `frontend/script.js` to your Render URL.
2. Push `frontend/` contents to the `gh-pages` branch **or** enable *Pages* on `main` with `/frontend` as root.

## API Example

```bash
curl -X POST https://your-url.onrender.com/analyze \
     -H "Content-Type: application/json" \
     -d '{"dna":"AGAT...","strs":["AGAT","AATG","TATC"]}'
```

**Response**

```json
{
  "match": "Lita Doolan",
  "str_counts": { "AGAT": 3, "AATG": 2, "TATC": 4 },
  "regions": [{"str":"AGAT","start":0,"end":11}],
  "structure_hint": "Potential gene-like region 0-36"
}
```

## Credits

- Built by **@LDolanLDolan** adapting Harvard **CS50x** DNA problem.
