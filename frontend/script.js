
const apiBase = 'https://YOUR-RENDER-URL.onrender.com';
document.getElementById('analyze').onclick = async () => {
  const dna = document.getElementById('dna').value.trim();
  const strs = document.getElementById('strs').value.split(',').map(s => s.trim()).filter(Boolean);
  const resultBox = document.getElementById('result');
  resultBox.textContent = 'Analyzing...';
  try {
    const res = await fetch(apiBase + '/analyze', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ dna, strs })
    });
    const data = await res.json();
    resultBox.textContent = JSON.stringify(data, null, 2);
    highlightRegions(dna, data.regions);
  } catch (err) {
    resultBox.textContent = 'Error: ' + err;
  }
};

function highlightRegions(sequence, regions) {
  let highlighted = '';
  let idx = 0;
  regions.sort((a,b)=>a.start-b.start);
  regions.forEach(r => {
    highlighted += sequence.slice(idx, r.start);
    highlighted += '<mark>' + sequence.slice(r.start, r.end) + '</mark>';
    idx = r.end;
  });
  highlighted += sequence.slice(idx);
  document.getElementById('highlight').innerHTML = highlighted;
}
