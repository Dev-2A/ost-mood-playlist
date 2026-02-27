const API = '/api';

// ── 상태 ────────────────────────────────
let currentSituation = null;
let currentPlayingId = null;

// ── DOM 참조 ─────────────────────────────
const moodInput       = document.getElementById('moodInput');
const topKSelect      = document.getElementById('topK');
const situationSelect = document.getElementById('situationFilter');
const generateBtn     = document.getElementById('generateBtn');
const loading         = document.getElementById('loading');
const errorEl         = document.getElementById('error');
const playlistSection = document.getElementById('playlistSection');
const playlistTitle   = document.getElementById('playlistTitle');
const playlistCount   = document.getElementById('playlistCount');
const playlistEl      = document.getElementById('playlist');
const player          = document.getElementById('player');
const audioPlayer     = document.getElementById('audioPlayer');
const playerTitle     = document.getElementById('playerTitle');
const playerGame      = document.getElementById('playerGame');

// ── 빠른 선택 버튼 ───────────────────────
document.querySelectorAll('.quick-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.quick-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    moodInput.value = btn.dataset.query;
    situationSelect.value = btn.dataset.situation;
    currentSituation = btn.dataset.situation;
  });
});

// ── 플레이리스트 생성 ────────────────────
generateBtn.addEventListener('click', generatePlaylist);
moodInput.addEventListener('keydown', e => {
  if (e.key === 'Enter' && e.ctrlKey) generatePlaylist();
});

async function generatePlaylist() {
  const query = moodInput.value.trim();
  if (!query) {
    showError('기분이나 상황을 입력해주세요.');
    return;
  }

  setLoading(true);
  hideError();
  playlistSection.classList.add('hidden');

  try {
    const res = await fetch(`${API}/playlist`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        query,
        top_k: parseInt(topKSelect.value),
        situation_filter: situationSelect.value || null,
      }),
    });

    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || '서버 오류가 발생했습니다.');
    }

    const data = await res.json();
    renderPlaylist(data);

  } catch (e) {
    showError(e.message);
  } finally {
    setLoading(false);
  }
}

// ── 렌더링 ───────────────────────────────
function renderPlaylist(data) {
  playlistTitle.textContent = `"${data.query}"`;
  playlistCount.textContent = `${data.total}곡`;
  playlistEl.innerHTML = '';

  data.tracks.forEach(track => {
    const card = document.createElement('div');
    card.className = 'track-card';
    card.dataset.id = track.id;
    card.dataset.path = track.file_path;
    card.dataset.title = track.title;
    card.dataset.game = track.game || '';

    const moodTags = track.mood.map(m => `<span class="tag mood">${m}</span>`).join('');
    const sitTags  = track.situation.map(s => `<span class="tag situation">${s}</span>`).join('');

    card.innerHTML = `
      <div class="track-rank">${track.rank}</div>
      <div class="track-info">
        <div class="track-title">${escHtml(track.title)}</div>
        <div class="track-game">${escHtml(track.game || '알 수 없음')}</div>
        <div class="track-tags">${moodTags}${sitTags}</div>
      </div>
      <div class="track-meta">
        <div class="similarity">▶ ${(track.similarity * 100).toFixed(1)}%</div>
        <div>${track.bpm_category} · ${track.energy_level}</div>
        <div>BPM ${track.bpm}</div>
      </div>
    `;

    card.addEventListener('click', () => playTrack(track, card));
    playlistEl.appendChild(card);
  });

  playlistSection.classList.remove('hidden');
}

// ── 재생 ────────────────────────────────
function playTrack(track, card) {
  document.querySelectorAll('.track-card').forEach(c => c.classList.remove('playing'));
  card.classList.add('playing');

  playerTitle.textContent = track.title;
  playerGame.textContent  = track.game || '알 수 없음';

  // file:// 대신 API를 통해 스트리밍
  audioPlayer.src = `${API}/audio/${track.id}`;
  audioPlayer.play().catch(() => {
    showError('파일을 재생할 수 없습니다. 경로를 확인해주세요.');
  });

  player.classList.remove('hidden');
  currentPlayingId = track.id;
}

// ── 유틸 ────────────────────────────────
function setLoading(on) {
  loading.classList.toggle('hidden', !on);
  generateBtn.disabled = on;
}
function showError(msg) { errorEl.textContent = msg; errorEl.classList.remove('hidden'); }
function hideError()     { errorEl.classList.add('hidden'); }
function escHtml(str) {
  return str.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}