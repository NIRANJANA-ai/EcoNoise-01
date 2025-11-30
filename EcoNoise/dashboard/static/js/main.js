// Refresh rates
const SNAPSHOT_MS = 1000;
const RANK_MS = 3000;
const MAP_MS = 5000;
const LOCS_MS = 3000;

// Load combined latest snapshot
async function loadSnapshot() {
  try {
    const res = await fetch('/api/snapshot?_=' + Date.now());
    const data = await res.json();
    document.getElementById('snap-location').innerText = data.location ?? '—';
    document.getElementById('snap-sound').innerText = data.sound_class ?? '—';
    document.getElementById('snap-conf').innerText = data.confidence ?? '—';
    document.getElementById('snap-harm').innerText = data.harm_rate ?? '—';
    document.getElementById('snap-time').innerText = data.timestamp ?? '—';
    document.getElementById('snap-total').innerText = data.total_cycles ?? '--';
  } catch (e) {
    console.warn('snapshot fetch failed', e);
  }
}

// Load per-location list
async function loadLocations(){
  try {
    const res = await fetch('/api/locations?_=' + Date.now());
    const j = await res.json();
    const list = j.locations || [];
    const container = document.getElementById('locationsList');
    if (!container) return;
    container.innerHTML = '';
    list.forEach(l => {
      const el = document.createElement('div');
      el.className = 'loc-row';
      const latest = l.latest || {};
      el.innerHTML = `<div class="loc-name">${l.location}</div>
                      <div class="loc-meta">sound: ${latest.predicted_class ?? '—'} | harm: ${latest.harm_rate ?? '—'} | count: ${l.count}</div>`;
      container.appendChild(el);
    });
  } catch (e) {
    console.warn('locations fail', e);
  }
}

// Rankings
async function loadRankings(){
  try {
    const res = await fetch('/api/rankings?_=' + Date.now());
    const arr = await res.json();
    const list = Array.isArray(arr) ? arr : (arr.rankings || arr.areas || []);
    const root = document.getElementById('rank-list');
    if (!root) return;
    root.innerHTML = '';
    if (!list.length) { root.innerHTML = '<p class="muted">No rankings yet</p>'; return; }
    list.forEach((item, i) => {
      const area = item.location || item.Location || item[0] || '—';
      const harm = item.avg_harm || item['Average Harm'] || item[1] || 0;
      const li = document.createElement('li');
      li.innerHTML = `<span>#${i+1}</span><span>${area}</span><span>${(typeof harm==='number')?harm.toFixed(2):harm}</span>`;
      root.appendChild(li);
    });
  } catch (e) { console.warn('rankings', e); }
}

// Map reload
function reloadMap() {
  const frame = document.getElementById('live-map');
  if (!frame) return;
  frame.src = '/map_content?_=' + Date.now();
}

// Monthly analytics helper: prefetch monthly summary for quick link (no chart rendering here)
async function loadMonthlySummary(){
  try {
    const res = await fetch('/api/monthly?_=' + Date.now());
    // we don't render here; monthly page will fetch again when opened
    return await res.json();
  } catch (e) {
    console.warn('monthly fetch fail', e);
  }
}

// start intervals
setInterval(loadSnapshot, SNAPSHOT_MS);
setInterval(loadRankings, RANK_MS);
setInterval(reloadMap, MAP_MS);
setInterval(loadLocations, LOCS_MS);

// initial
loadSnapshot();
loadRankings();
reloadMap();
loadLocations();
