import { RubiksCube3D } from './cube3d.js';
import { ScanController } from './scan.js';


const API_BASE = window.RUBIKS_API_BASE || 'http://localhost:8000';

const canvas = document.getElementById('cubeCanvas');
const cube3d = new RubiksCube3D(canvas);
cube3d.reset();

const apiStatusEl = document.getElementById('apiStatus');
const statusLine = document.getElementById('statusLine');
const moveLog = document.getElementById('moveLog');
const moveCountEl = document.getElementById('moveCount');
const playback = document.getElementById('playback');
const speedSlider = document.getElementById('speedSlider');

let currentSolution = [];

function setStatus(msg) { statusLine.textContent = msg; }

function renderMoveLog(moves) {
  moveLog.innerHTML = '';
  moves.forEach((m, i) => {
    const tag = document.createElement('span');
    tag.className = 'move-tag';
    tag.textContent = m;
    tag.dataset.index = i;
    moveLog.appendChild(tag);
  });
  moveCountEl.textContent = moves.length ? `${moves.length} moves` : '';
  playback.hidden = moves.length === 0;
}

function highlightMove(index) {
  [...moveLog.children].forEach((el, i) => el.classList.toggle('active', i === index));
}

async function checkBackend() {
  try {
    const res = await fetch(`${API_BASE}/health`);
    if (!res.ok) throw new Error();
    apiStatusEl.textContent = 'backend connected';
    apiStatusEl.className = 'api-status ok';
  } catch {
    apiStatusEl.textContent = 'backend unreachable';
    apiStatusEl.className = 'api-status down';
  }
}
checkBackend();

// ---- Scramble / Reset ----
document.getElementById('btnScramble').addEventListener('click', async () => {
  setStatus('Scrambling…');
  renderMoveLog([]);
  const moves = cube3d.scrambleMoves(20);
  await cube3d.applySequence(moves, 90);
  setStatus('Scrambled. Ready to solve.');
});

document.getElementById('btnReset').addEventListener('click', () => {
  cube3d.reset();
  renderMoveLog([]);
  setStatus('Reset to solved.');
});

// ---- Solve ----
document.getElementById('btnSolve').addEventListener('click', async () => {
  setStatus('Solving…');
  const faces = cube3d.getState();
  try {
    const res = await fetch(`${API_BASE}/solve`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ faces }),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || 'Solve failed');

    currentSolution = data.solution;
    renderMoveLog(currentSolution);
    setStatus(`Solved in ${data.move_count} moves. Press "Play solution" to watch.`);
  } catch (err) {
    setStatus(`Error: ${err.message}`);
  }
});

// ---- Playback ----
document.getElementById('btnPlayback').addEventListener('click', async () => {
  if (!currentSolution.length) return;
  const btn = document.getElementById('btnPlayback');
  btn.disabled = true;
  let i = 0;
  await cube3d.applySequence(currentSolution, Number(speedSlider.value), () => {
    highlightMove(i);
    i++;
  });
  highlightMove(-1);
  btn.disabled = false;
  setStatus('Solution played. Cube should now be solved.');
});

// ---- Scan (camera) ----
const scanPanel = document.getElementById('scanPanel');
const btnScanToggle = document.getElementById('btnScanToggle');
const btnCalibrate = document.getElementById('btnCalibrate');
const btnCapture = document.getElementById('btnCapture');

let scanCtl = null;
let scanState = 'idle'; // idle | calibrating | capturing

btnScanToggle.addEventListener('click', async () => {
  const opening = scanPanel.hidden;
  scanPanel.hidden = !opening;
  if (opening && !scanCtl) {
    scanCtl = new ScanController({
      video: document.getElementById('scanVideo'),
      overlay: document.getElementById('scanOverlay'),
      statusEl: document.getElementById('scanStatus'),
      faceTrackerEl: document.getElementById('faceTracker'),
    });
    try {
      await scanCtl.start();
    } catch (err) {
      document.getElementById('scanStatus').textContent =
        'Camera access failed: ' + err.message;
    }
  }
});

btnCalibrate.addEventListener('click', () => {
  scanState = 'calibrating';
  scanCtl.beginCalibration();
  btnCapture.disabled = false;
  btnCapture.textContent = 'Capture color';
});

btnCapture.addEventListener('click', () => {
  if (scanState === 'calibrating') {
    const done = scanCtl.captureCalibrationSample();
    if (done) {
      scanState = 'capturing';
      btnCapture.textContent = 'Capture face';
    }
  } else {
    scanCtl.captureFace();

    if (scanCtl.isComplete()) finishScan();
  }
});

function finishScan() {

  cube3d.setState(scanCtl.capturedFaces);
  renderMoveLog([]);
  setStatus('Cube loaded from camera scan. Click any face preview to recapture it if something looks wrong, then re-solve.');
}
