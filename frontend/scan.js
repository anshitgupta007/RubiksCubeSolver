// scan.js
//
// Client-side camera scanning: calibrate 6 sticker colors against this
// specific cube/lighting, then classify each of the 9 cells on a face by
// nearest-color distance to the calibrated references (not "first color
// range with any matching pixel", which is what made the original OpenCV
// version fragile under real lighting).
//
// Faces are fixed slots (Front,Right,Back,Left,Top,Bottom -- matching
// src/cube.py's order), not an append-only list: this lets the user
// jump back and recapture any single face without redoing the rest.

export const FACE_NAMES = ['Front', 'Right', 'Back', 'Left', 'Top', 'Bottom'];
const SWATCH_HEX = ['#f2f2ee', '#009b48', '#ffd500', '#0045ad', '#b71234', '#ff5800'];

export class ScanController {
  constructor({ video, overlay, statusEl, faceTrackerEl, onFaceCaptured }) {
    this.video = video;
    this.overlay = overlay;
    this.statusEl = statusEl;
    this.faceTrackerEl = faceTrackerEl;
    this.onFaceCaptured = onFaceCaptured; // (cells, faceIndex) => void

    this.ctx = overlay.getContext('2d');
    this.references = null;              // [[r,g,b], ...] length 6, from calibration
    this.calibrationIndex = 0;
    this.capturedFaces = new Array(6).fill(null); // fixed slots, one per FACE_NAMES entry
    this.activeIndex = 0;                // which face slot "Capture face" writes to next

    this._buildFaceTracker();
    this._drawLoopBound = () => this._drawGrid();
  }

  _buildFaceTracker() {
    this.faceTrackerEl.innerHTML = '';
    this.previews = FACE_NAMES.map((name, i) => {
      const wrap = document.createElement('button');
      wrap.type = 'button';
      wrap.className = 'face-preview';
      wrap.title = `${name} -- click to (re)capture this face`;

      const label = document.createElement('span');
      label.className = 'face-preview__label';
      label.textContent = name;
      wrap.appendChild(label);

      const grid = document.createElement('div');
      grid.className = 'face-preview__grid';
      const cells = [];
      for (let c = 0; c < 9; c++) {
        const cell = document.createElement('span');
        grid.appendChild(cell);
        cells.push(cell);
      }
      wrap.appendChild(grid);

      wrap.addEventListener('click', () => this._onPreviewClick(i));
      this.faceTrackerEl.appendChild(wrap);
      return { wrap, cells };
    });
    this._updateActiveHighlight();
  }

  _onPreviewClick(index) {
    this.activeIndex = index;
    this._updateActiveHighlight();
    const label = this.capturedFaces[index] ? 'Recapturing' : 'Capturing';
    this.statusEl.textContent = `${label} ${FACE_NAMES[index]} face. Show it to the camera and press "Capture face".`;
  }

  _updateActiveHighlight() {
    this.previews.forEach((p, i) => p.wrap.classList.toggle('active', i === this.activeIndex));
  }

  async start() {
    this.stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } });
    this.video.srcObject = this.stream;
    await this.video.play();
    this._resizeOverlay();
    this._scanning = true;
    requestAnimationFrame(this._drawLoopBound);
  }

  stop() {
    this._scanning = false;
    if (this.stream) this.stream.getTracks().forEach(t => t.stop());
  }

  _resizeOverlay() {
    this.overlay.width = this.video.clientWidth;
    this.overlay.height = this.video.clientHeight;
  }

  _drawGrid() {
    this._resizeOverlay();
    const { width: w, height: h } = this.overlay;
    this.ctx.clearRect(0, 0, w, h);
    const size = Math.min(w, h) * 0.6;
    const x0 = (w - size) / 2, y0 = (h - size) / 2;
    this.ctx.strokeStyle = 'rgba(255,255,255,0.85)';
    this.ctx.lineWidth = 1.5;
    for (let i = 0; i <= 3; i++) {
      const x = x0 + (size / 3) * i;
      this.ctx.beginPath(); this.ctx.moveTo(x, y0); this.ctx.lineTo(x, y0 + size); this.ctx.stroke();
      const y = y0 + (size / 3) * i;
      this.ctx.beginPath(); this.ctx.moveTo(x0, y); this.ctx.lineTo(x0 + size, y); this.ctx.stroke();
    }
    if (this._scanning) requestAnimationFrame(this._drawLoopBound);
  }

  // Median per channel over a small block, rather than a mean: a mean is
  // easily dragged off by a handful of blown-out specular-highlight pixels
  // on a glossy sticker, which was a likely cause of misclassification.
  _sampleCell(row, col) {
    const vw = this.video.videoWidth, vh = this.video.videoHeight;
    if (!vw || !vh) return [128, 128, 128]; // camera not ready yet
    if (!this._offscreen) this._offscreen = document.createElement('canvas');
    this._offscreen.width = vw; this._offscreen.height = vh;
    const octx = this._offscreen.getContext('2d', { willReadFrequently: true });
    octx.drawImage(this.video, 0, 0, vw, vh);

    const size = Math.min(vw, vh) * 0.6;
    const x0 = (vw - size) / 2, y0 = (vh - size) / 2;
    const cellW = size / 3, cellH = size / 3;
    const cx = x0 + cellW * (col + 0.5);
    const cy = y0 + cellH * (row + 0.5);
    const sampleSize = Math.max(8, Math.floor(Math.min(cellW, cellH) * 0.3));

    const data = octx.getImageData(
      Math.round(cx - sampleSize / 2), Math.round(cy - sampleSize / 2),
      sampleSize, sampleSize
    ).data;

    const rs = [], gs = [], bs = [];
    for (let i = 0; i < data.length; i += 4) {
      rs.push(data[i]); gs.push(data[i + 1]); bs.push(data[i + 2]);
    }
    const median = arr => {
      const s = [...arr].sort((a, b) => a - b);
      return s[Math.floor(s.length / 2)];
    };
    return [median(rs), median(gs), median(bs)];
  }

  beginCalibration() {
    this.calibrationIndex = 0;
    this.references = new Array(6).fill(null);
    this.statusEl.textContent =
      'Calibrating: hold sticker color 1 of 6 in the center cell, then press "Capture color". ' +
      'Any 6 distinct colors work, in any order -- just be consistent when scanning faces.';
  }

  captureCalibrationSample() {
    const [r, g, b] = this._sampleCell(1, 1);
    this.references[this.calibrationIndex] = [r, g, b];
    this.calibrationIndex++;
    if (this.calibrationIndex < 6) {
      this.statusEl.textContent = `Hold sticker color ${this.calibrationIndex + 1} of 6 in the center cell, then capture.`;
      return false;
    }
    this.statusEl.textContent = `Calibrated. Show the ${FACE_NAMES[this.activeIndex]} face and press "Capture face".`;
    return true;
  }

  _classify([r, g, b]) {
    let best = 0, bestDist = Infinity;
    for (let i = 0; i < 6; i++) {
      const [rr, rg, rb] = this.references[i];
      const d = (r - rr) ** 2 + (g - rg) ** 2 + (b - rb) ** 2;
      if (d < bestDist) { bestDist = d; best = i; }
    }
    return best;
  }

  // Captures into the currently-active face slot (whichever preview is
  // highlighted -- either the next empty one, or one the user clicked to
  // redo). Always overwrite-safe: capturing an already-filled slot just
  // replaces it.
  captureFace() {
    const cells = [];
    for (let row = 0; row < 3; row++) {
      for (let col = 0; col < 3; col++) {
        cells.push(this._classify(this._sampleCell(row, col)));
      }
    }
    const index = this.activeIndex;
    this.capturedFaces[index] = cells;
    this._paintPreview(index, cells);
    if (this.onFaceCaptured) this.onFaceCaptured(cells, index);

    const nextEmpty = this.capturedFaces.findIndex(f => f === null);
    if (nextEmpty === -1) {
      this.statusEl.textContent = 'All 6 faces captured. Check each preview below -- click any face to recapture it, or load the cube.';
    } else {
      this.activeIndex = nextEmpty;
      this._updateActiveHighlight();
      this.statusEl.textContent = `Captured ${FACE_NAMES[index]}. Now show the ${FACE_NAMES[nextEmpty]} face and press "Capture face".`;
    }
    return this.isComplete();
  }

  _paintPreview(index, cells) {
    const { wrap, cells: cellEls } = this.previews[index];
    wrap.classList.add('done');
    cells.forEach((colorId, i) => {
      cellEls[i].style.background = SWATCH_HEX[colorId];
    });
  }

  isComplete() {
    return this.capturedFaces.every(f => f !== null);
  }

  isCalibrated() {
    return !!this.references && this.references.every(r => r);
  }

  reset() {
    this.capturedFaces = new Array(6).fill(null);
    this.references = null;
    this.activeIndex = 0;
    this.previews.forEach(({ wrap, cells }) => {
      wrap.classList.remove('done', 'active');
      cells.forEach(c => { c.style.background = ''; });
    });
    this._updateActiveHighlight();
  }
}
