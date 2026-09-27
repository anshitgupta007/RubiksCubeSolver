// cube3d.js
//
// 3D Rubik's cube rendered with three.js.
//
// IMPORTANT: the mapping between (face, row, col) in the solver's array
// format and 3D cubie positions/directions below (FULL_ORIENT and MOVE_SIGNS)
// is NOT a guess. It was derived by brute-force search against the actual
// src/cube.py move logic and verified to reproduce all 18 quarter/half-turn
// moves exactly (see verify_orientation2.py in the repo history / PR).
// Don't hand-edit these constants without re-running that verification --
// a wrong sign or axis here means the "solution" returned by the backend
// would not actually solve the physical cube, even though it would still
// look like a valid list of moves.

import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

// Face indices match src/cube.py exactly: 0=Front,1=Right,2=Back,3=Left,4=Top,5=Bottom
export const FACE_NAMES = ['Front', 'Right', 'Back', 'Left', 'Top', 'Bottom'];
const NORMALS = {
  0: [0, 0, 1], 1: [1, 0, 0], 2: [0, 0, -1],
  3: [-1, 0, 0], 4: [0, 1, 0], 5: [0, -1, 0],
};

// Verified (u, v) basis per face: local "column" and "row" directions in 3D.
const FULL_ORIENT = {
  0: [[1, 0, 0], [0, 1, 0]],
  1: [[0, 0, -1], [0, 1, 0]],
  2: [[-1, 0, 0], [0, 1, 0]],
  3: [[0, 0, 1], [0, 1, 0]],
  4: [[1, 0, 0], [0, 0, -1]],
  5: [[1, 0, 0], [0, 0, 1]],
};

// Verified rotation sign (+1/-1 about the given axis = a clockwise quarter
// turn of that move, matching cube.py's own permutation).
const MOVE_SPEC = {
  R: { axisIdx: 0, layer: 1, axis: 'x', sign: -1 },
  L: { axisIdx: 0, layer: -1, axis: 'x', sign: 1 },
  U: { axisIdx: 1, layer: 1, axis: 'y', sign: -1 },
  D: { axisIdx: 1, layer: -1, axis: 'y', sign: 1 },
  F: { axisIdx: 2, layer: 1, axis: 'z', sign: -1 },
  B: { axisIdx: 2, layer: -1, axis: 'z', sign: 1 },
};

const COLOR_HEX = [0xf2f2ee, 0x009b48, 0xffd500, 0x0045ad, 0xb71234, 0xff5800];
const PLASTIC = 0x111318;

function vecKey(v) { return v.join(','); }

function rotateVec([x, y, z], axis, sign) {
  if (axis === 'x') return [x, -sign * z, sign * y];
  if (axis === 'y') return [sign * z, y, -sign * x];
  return [-sign * y, sign * x, z]; // 'z'
}

export class RubiksCube3D {
  constructor(canvas) {
    this.canvas = canvas;
    this.scene = new THREE.Scene();
    this.camera = new THREE.PerspectiveCamera(38, 1, 0.1, 100);
    this.camera.position.set(5.2, 4.6, 6.2);

    this.renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

    this.controls = new OrbitControls(this.camera, this.renderer.domElement);
    this.controls.enableDamping = true;
    this.controls.dampingFactor = 0.08;
    this.controls.minDistance = 5;
    this.controls.maxDistance = 14;

    this.scene.add(new THREE.AmbientLight(0xffffff, 0.65));
    const key = new THREE.DirectionalLight(0xffffff, 0.9);
    key.position.set(6, 9, 7);
    this.scene.add(key);
    const fill = new THREE.DirectionalLight(0xffffff, 0.35);
    fill.position.set(-6, -3, -5);
    this.scene.add(fill);

    this.group = new THREE.Group();
    this.scene.add(this.group);

    this.cubies = []; // { mesh, pos:[x,y,z] }
    this._buildCubies();
    this._resize();
    window.addEventListener('resize', () => this._resize());

    this._animating = false;
    this._tick();
  }

  _resize() {
    const { clientWidth: w, clientHeight: h } = this.canvas;
    this.renderer.setSize(w, h, false);
    this.camera.aspect = w / h;
    this.camera.updateProjectionMatrix();
  }

  _tick() {
    requestAnimationFrame(() => this._tick());
    this.controls.update();
    this.renderer.render(this.scene, this.camera);
  }

  _buildCubies() {
    const size = 0.94;
    const geo = new THREE.BoxGeometry(size, size, size);
    for (let x = -1; x <= 1; x++) {
      for (let y = -1; y <= 1; y++) {
        for (let z = -1; z <= 1; z++) {
          if (x === 0 && y === 0 && z === 0) continue;
          const materials = [
            new THREE.MeshLambertMaterial({ color: PLASTIC }), // +x
            new THREE.MeshLambertMaterial({ color: PLASTIC }), // -x
            new THREE.MeshLambertMaterial({ color: PLASTIC }), // +y
            new THREE.MeshLambertMaterial({ color: PLASTIC }), // -y
            new THREE.MeshLambertMaterial({ color: PLASTIC }), // +z
            new THREE.MeshLambertMaterial({ color: PLASTIC }), // -z
          ];
          const mesh = new THREE.Mesh(geo, materials);
          mesh.position.set(x, y, z);
          mesh.userData.colors = [null, null, null, null, null, null]; // per material index, logical color id 0-5 or null
          this.group.add(mesh);
          this.cubies.push({ mesh, pos: [x, y, z] });
        }
      }
    }
  }

  // Material index per three.js BoxGeometry convention: [+x,-x,+y,-y,+z,-z]
  static _matIndexForDir([dx, dy, dz]) {
    if (dx === 1) return 0;
    if (dx === -1) return 1;
    if (dy === 1) return 2;
    if (dy === -1) return 3;
    if (dz === 1) return 4;
    return 5; // dz === -1
  }

  _cubieAt(pos) {
    return this.cubies.find(c => vecKey(c.pos) === vecKey(pos));
  }

  // Paint every sticker from a 6x9 faces array (Front,Right,Back,Left,Top,Bottom
  // order, each 9 stickers row-major), matching src/cube.py exactly. No move
  // animation -- used for initial load, scan results, and reset.
  // Given a world-space direction and a cubie's current (axis-aligned)
  // rotation, find which local material index currently faces that
  // world direction. Needed because after 90-degree rotations, a
  // cubie's local +x face (material index 0) may now point along
  // world -z, etc.
  static _localMatIndexForWorldDir(mesh, worldDir) {
    const v = new THREE.Vector3(...worldDir);
    const invQuat = mesh.quaternion.clone().invert();
    v.applyQuaternion(invQuat);
    const rounded = [Math.round(v.x), Math.round(v.y), Math.round(v.z)];
    return RubiksCube3D._matIndexForDir(rounded);
  }

  setState(faces) {
    for (const cubie of this.cubies) {
      cubie.mesh.rotation.set(0, 0, 0); // safe: every sticker gets repainted below anyway
      for (let i = 0; i < 6; i++) {
        cubie.mesh.material[i].color.setHex(PLASTIC);
        cubie.mesh.userData.colors[i] = null;
      }
    }
    for (let f = 0; f < 6; f++) {
      const n = NORMALS[f];
      const [u, v] = FULL_ORIENT[f];
      for (let r = 0; r < 3; r++) {
        for (let c = 0; c < 3; c++) {
          const ucoord = c - 1;
          const vcoord = 1 - r;
          const pos = [0, 1, 2].map(i => n[i] + u[i] * ucoord + v[i] * vcoord);
          const cubie = this._cubieAt(pos);
          const color = faces[f][r * 3 + c];
          // setState is only ever called on a freshly-built or reset cube
          // (identity rotation), so world dir == local dir here.
          const matIdx = RubiksCube3D._matIndexForDir(n);
          cubie.mesh.material[matIdx].color.setHex(COLOR_HEX[color]);
          cubie.mesh.userData.colors[matIdx] = color;
        }
      }
    }
  }

  // Read the current sticker arrangement back into the same 6x9 array format,
  // by inverting the same (row,col) <-> 3D mapping used in setState.
  getState() {
    const arr = Array.from({ length: 6 }, () => new Array(9).fill(null));
    for (let f = 0; f < 6; f++) {
      const n = NORMALS[f];
      const [u, v] = FULL_ORIENT[f];
      for (let r = 0; r < 3; r++) {
        for (let c = 0; c < 3; c++) {
          const ucoord = c - 1;
          const vcoord = 1 - r;
          const pos = [0, 1, 2].map(i => n[i] + u[i] * ucoord + v[i] * vcoord);
          const cubie = this._cubieAt(pos);
          const matIdx = RubiksCube3D._localMatIndexForWorldDir(cubie.mesh, n);
          arr[f][r * 3 + c] = cubie.mesh.userData.colors[matIdx];
        }
      }
    }
    return arr;
  }

  reset() {
    const solved = Array.from({ length: 6 }, (_, f) => new Array(9).fill(f));
    this.setState(solved);
  }

  // Animate a single move ("R", "U'", "F2", ...). Resolves when done.
  applyMove(move, durationMs = 250) {
    return new Promise(resolve => {
      const base = move[0];
      const spec = MOVE_SPEC[base];
      let sign = spec.sign;
      let turns = 1;
      if (move.endsWith("'")) sign = -sign;
      else if (move.endsWith('2')) turns = 2;

      this._doTurns(spec, sign, turns, durationMs, resolve);
    });
  }

  _doTurns(spec, sign, turnsLeft, durationMs, resolve) {
    if (turnsLeft === 0) { resolve(); return; }

    const affected = this.cubies.filter(c => c.pos[spec.axisIdx] === spec.layer);
    const pivot = new THREE.Group();
    this.group.add(pivot);
    for (const c of affected) pivot.attach(c.mesh);

    const axisVec = { x: new THREE.Vector3(1, 0, 0), y: new THREE.Vector3(0, 1, 0), z: new THREE.Vector3(0, 0, 1) }[spec.axis];
    const targetAngle = sign * (Math.PI / 2);

    const start = performance.now();
    const step = (now) => {
      const t = Math.min(1, (now - start) / durationMs);
      const eased = 1 - Math.pow(1 - t, 3); // ease-out cubic
      pivot.rotation.set(0, 0, 0);
      pivot.rotateOnWorldAxis(axisVec, targetAngle * eased);
      if (t < 1) {
        requestAnimationFrame(step);
      } else {
        // Bake the rotation into each cubie's world transform, snap to
        // integer grid positions/axis-aligned rotations, then reparent
        // back to the main group so the next move's layer selection
        // (which reads c.pos) is correct.
        for (const c of affected) {
          pivot.updateMatrixWorld(true);
          this.group.attach(c.mesh);
          c.mesh.position.set(
            Math.round(c.mesh.position.x),
            Math.round(c.mesh.position.y),
            Math.round(c.mesh.position.z)
          );
          const e = new THREE.Euler().setFromQuaternion(c.mesh.quaternion, 'XYZ');
          c.mesh.rotation.set(
            Math.round(e.x / (Math.PI / 2)) * (Math.PI / 2),
            Math.round(e.y / (Math.PI / 2)) * (Math.PI / 2),
            Math.round(e.z / (Math.PI / 2)) * (Math.PI / 2)
          );
          c.pos = [c.mesh.position.x, c.mesh.position.y, c.mesh.position.z];
        }
        this.group.remove(pivot);
        this._doTurns(spec, sign, turnsLeft - 1, durationMs, resolve);
      }
    };
    requestAnimationFrame(step);
  }

  async applySequence(moves, durationMs, onStep) {
    for (const move of moves) {
      await this.applyMove(move, durationMs);
      if (onStep) onStep(move);
    }
  }

  scrambleMoves(n = 20) {
    const moves = ['R', "R'", 'R2', 'L', "L'", 'L2', 'U', "U'", 'U2',
                   'D', "D'", 'D2', 'F', "F'", 'F2', 'B', "B'", 'B2'];
    const seq = [];
    for (let i = 0; i < n; i++) seq.push(moves[Math.floor(Math.random() * moves.length)]);
    return seq;
  }
}
