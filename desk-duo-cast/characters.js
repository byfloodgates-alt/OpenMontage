// Reusable cast for the "desk duo" promo style.
//   createHost(THREE)  -> { root, update(state) }   the seated presenter
//   createBot(THREE)   -> { root, update(state) }   the red screen-faced robot on its stand
// Everything is low-poly and flat-shaded; colours are in PALETTE so every film uses the same ones.
// State is plain numbers, so a timeline can drive it frame by frame (deterministic renders).

export const PALETTE = {
  skin: 0x9a5a3c, skinShadow: 0x7a4430,
  hair: 0x1c1c20, beard: 0x2a1c17, brow: 0x16120f,
  hoodie: 0x1f4d5a, hoodieDark: 0x173a45, string: 0xe9e2d6,
  pants: 0x1d2230, shoe: 0x2b1f1a,
  chair: 0x262b33, chairMetal: 0x3a3e44,
  eyeWhite: 0xf4efe6, pupil: 0x111111, mouth: 0x3a1410, teeth: 0xf1ebe0,
  bot: 0xc4502e, botDark: 0x9c3c22, visor: 0x0b0b0d, rim: 0xeadfca,
  glow: 0xffe2a0, antennaBall: 0xe8c23a, ring: 0xf2e9dc, stand: 0x141416,
};

const flat = (THREE, color, o = {}) =>
  new THREE.MeshStandardMaterial({ color, flatShading: true, roughness: 0.78, metalness: 0, ...o });

function mesh(THREE, geo, mat, x = 0, y = 0, z = 0) {
  const m = new THREE.Mesh(geo, mat);
  m.position.set(x, y, z);
  m.castShadow = m.receiveShadow = true;
  return m;
}

// ---------------------------------------------------------------- host
export function createHost(THREE) {
  const P = PALETTE, M = (c, o) => flat(THREE, c, o);
  const root = new THREE.Group();
  const box = (w, h, d) => new THREE.BoxGeometry(w, h, d);

  // chair (root origin = floor under the seat centre; seat top at y = 0.5)
  const chair = new THREE.Group();
  const cm = M(P.chair), metal = M(P.chairMetal, { roughness: 0.5, metalness: 0.3 });
  chair.add(mesh(THREE, box(0.62, 0.1, 0.58), cm, 0, 0.45, 0));
  const back = mesh(THREE, box(0.6, 0.95, 0.12), cm, 0, 1.0, -0.3); back.rotation.x = -0.08; chair.add(back);
  for (const s of [-1, 1]) {
    chair.add(mesh(THREE, box(0.06, 0.05, 0.42), cm, s * 0.36, 0.72, 0.0));
    chair.add(mesh(THREE, box(0.04, 0.24, 0.04), metal, s * 0.36, 0.6, -0.05));
  }
  chair.add(mesh(THREE, new THREE.CylinderGeometry(0.035, 0.035, 0.36, 8), metal, 0, 0.22, 0));
  for (let i = 0; i < 5; i++) {
    const leg = mesh(THREE, box(0.05, 0.04, 0.34), metal, 0, 0.05, 0);
    leg.geometry.translate(0, 0, 0.17); leg.rotation.y = (i / 5) * Math.PI * 2; chair.add(leg);
  }
  root.add(chair);

  // body pivot: everything above the hips leans/breathes from here
  const hips = new THREE.Group(); hips.position.set(0, 0.55, -0.02); root.add(hips);
  const hoodie = M(P.hoodie), hoodieDark = M(P.hoodieDark);
  const torsoGeo = new THREE.CylinderGeometry(0.27, 0.31, 0.62, 6, 1); torsoGeo.scale(1.08, 1, 0.72);
  const torso = mesh(THREE, torsoGeo, hoodie, 0, 0.33, 0); torso.rotation.y = Math.PI / 6; hips.add(torso);
  // hood collar + strings + pocket
  const hood = mesh(THREE, new THREE.TorusGeometry(0.17, 0.06, 5, 8), hoodieDark, 0, 0.64, -0.02);
  hood.rotation.x = Math.PI / 2 - 0.25; hips.add(hood);
  for (const s of [-1, 1]) hips.add(mesh(THREE, box(0.018, 0.17, 0.018), M(P.string), s * 0.06, 0.5, 0.215));
  hips.add(mesh(THREE, box(0.34, 0.13, 0.03), hoodieDark, 0, 0.17, 0.215));

  // neck/head pivot
  const neck = new THREE.Group(); neck.position.set(0, 0.66, 0.01); hips.add(neck);
  neck.add(mesh(THREE, new THREE.CylinderGeometry(0.075, 0.085, 0.1, 6), M(P.skinShadow), 0, 0.03, 0));
  const head = new THREE.Group(); head.position.set(0, 0.24, 0.02); neck.add(head);
  const skullGeo = new THREE.IcosahedronGeometry(0.2, 1); skullGeo.scale(0.95, 1.08, 1.0);
  head.add(mesh(THREE, skullGeo, M(P.skin)));
  // beard: lower shell, slightly larger than the skull
  const beardGeo = new THREE.SphereGeometry(0.205, 10, 6, 0, Math.PI * 2, Math.PI * 0.64, Math.PI * 0.36);
  beardGeo.scale(0.97, 1.1, 1.03);
  const beard = mesh(THREE, beardGeo, M(P.beard)); beard.position.y = -0.005; head.add(beard);
  // hair: flat-top cap with a forward peak, tilted back a touch
  const hairGeo = new THREE.SphereGeometry(0.215, 10, 5, 0, Math.PI * 2, 0, Math.PI * 0.42);
  hairGeo.scale(1.0, 0.95, 1.06);
  const hair = mesh(THREE, hairGeo, M(P.hair), 0, 0.035, -0.01); hair.rotation.x = -0.18; head.add(hair);
  const peak = mesh(THREE, box(0.26, 0.06, 0.1), M(P.hair), 0, 0.17, 0.12); peak.rotation.x = 0.2; head.add(peak);
  for (const s of [-1, 1]) {
    const ear = mesh(THREE, new THREE.IcosahedronGeometry(0.045, 0), M(P.skinShadow), s * 0.19, 0.0, -0.01);
    ear.scale.set(0.6, 1, 1); head.add(ear);
  }
  const nose = mesh(THREE, new THREE.IcosahedronGeometry(0.035, 0), M(P.skinShadow), 0, -0.01, 0.205);
  nose.scale.set(1, 0.9, 0.9); head.add(nose);

  const eyes = [], pupils = [], brows = [], lids = [];
  for (const s of [-1, 1]) {
    const eye = mesh(THREE, new THREE.SphereGeometry(0.029, 10, 8), M(P.eyeWhite, { roughness: 0.4 }), s * 0.072, 0.045, 0.176);
    eye.scale.set(1, 1.1, 0.6); head.add(eye); eyes.push(eye);
    const pupil = mesh(THREE, new THREE.SphereGeometry(0.016, 8, 6), M(P.pupil, { roughness: 0.3 }), s * 0.072, 0.045, 0.192);
    pupil.scale.set(1, 1.1, 0.5); head.add(pupil); pupils.push(pupil);
    const lid = mesh(THREE, new THREE.SphereGeometry(0.032, 10, 6, 0, Math.PI * 2, 0, Math.PI / 2), M(P.skin), s * 0.072, 0.045, 0.176);
    lid.scale.set(1, 1.1, 0.65); lid.rotation.x = -Math.PI * 0.5; head.add(lid); lids.push(lid);
    const brow = mesh(THREE, box(0.1, 0.03, 0.035), M(P.brow), s * 0.08, 0.11, 0.18);
    head.add(brow); brows.push(brow);
  }
  const mouth = new THREE.Group(); mouth.position.set(0, -0.075, 0.186); head.add(mouth);
  const mouthHole = mesh(THREE, box(0.07, 0.024, 0.02), M(P.mouth, { roughness: 0.9 }));
  const teeth = mesh(THREE, box(0.06, 0.012, 0.02), M(P.teeth), 0, 0.01, 0.004);
  mouth.add(mouthHole, teeth);

  // arms: shoulder -> elbow -> hand
  const arms = [];
  for (const s of [-1, 1]) {
    const sh = new THREE.Group(); sh.position.set(s * 0.33, 0.58, 0); hips.add(sh);
    const upperGeo = box(0.15, 0.34, 0.15); upperGeo.translate(0, -0.17, 0);
    sh.add(mesh(THREE, upperGeo, hoodie));
    const el = new THREE.Group(); el.position.set(0, -0.33, 0); sh.add(el);
    const foreGeo = box(0.135, 0.3, 0.135); foreGeo.translate(0, -0.15, 0);
    el.add(mesh(THREE, foreGeo, hoodie));
    el.add(mesh(THREE, box(0.145, 0.04, 0.145), hoodieDark, 0, -0.29, 0));
    const hand = mesh(THREE, new THREE.IcosahedronGeometry(0.07, 0), M(P.skin), 0, -0.35, 0.01);
    hand.scale.set(0.9, 1.05, 0.8); el.add(hand);
    arms.push({ sh, el, s });
  }

  // legs (seated): thigh forward, shin down
  for (const s of [-1, 1]) {
    const hip = new THREE.Group(); hip.position.set(s * 0.14, 0.55, 0.0); root.add(hip);
    const thighGeo = box(0.19, 0.18, 0.5); thighGeo.translate(0, 0, 0.25);
    hip.add(mesh(THREE, thighGeo, M(P.pants)));
    const knee = new THREE.Group(); knee.position.set(0, 0, 0.47); hip.add(knee);
    const shinGeo = box(0.16, 0.46, 0.17); shinGeo.translate(0, -0.23, 0);
    knee.add(mesh(THREE, shinGeo, M(P.pants)));
    knee.add(mesh(THREE, box(0.17, 0.09, 0.27), M(P.shoe), 0, -0.48, 0.05));
    knee.rotation.x = 0.12;
  }

  // state: talk 0..1 (mouth open), smile -1..1, brows -1 (frown) .. 1 (raised), browTilt (sceptical),
  //        look [x,y] -1..1, blink 0..1, headTurn/headTilt/headNod (rad), lean (rad), breathe 0..1,
  //        armL/armR: { raise, out, bend } in rad, gesture adds to the right arm.
  function update(st = {}) {
    const g = (k, d = 0) => (st[k] ?? d);
    hips.rotation.x = g('lean') + Math.sin(g('breathe') * Math.PI * 2) * 0.01;
    hips.scale.y = 1 + Math.sin(g('breathe') * Math.PI * 2) * 0.006;
    neck.rotation.y = g('headTurn'); neck.rotation.z = g('headTilt'); neck.rotation.x = g('headNod');
    const talk = Math.max(0, Math.min(1, g('talk')));
    const smile = g('smile');
    mouthHole.scale.set(1 + smile * 0.35 - talk * 0.15, 0.6 + talk * 2.2, 1);
    mouth.rotation.z = 0; teeth.visible = talk > 0.15 || smile > 0.4;
    teeth.position.y = 0.005 + talk * 0.012;
    const [lx, ly] = st.look ?? [0, 0];
    pupils.forEach((p, i) => { p.position.x = eyes[i].position.x + lx * 0.011; p.position.y = 0.045 + ly * 0.01; });
    const blink = Math.max(0, Math.min(1, g('blink')));
    lids.forEach((l) => { l.rotation.x = -Math.PI * 0.5 + blink * Math.PI * 0.5; l.visible = blink > 0.02; });
    const b = g('brows'), tilt = g('browTilt');
    brows.forEach((br, i) => {
      const s = i === 0 ? -1 : 1;
      br.position.y = 0.11 + b * 0.022 + (s > 0 ? tilt * 0.02 : 0);
      br.rotation.z = s * (-b * 0.18) + (b < 0 ? s * 0.12 * -b : 0);
    });
    const arm = (a, d) => {
      const o = st[a] ?? {};
      d.sh.rotation.x = -(o.raise ?? 0.55);
      d.sh.rotation.z = d.s * (o.out ?? 0.12);
      d.el.rotation.x = -(o.bend ?? 0.9);
    };
    arm('armL', arms[0]); arm('armR', arms[1]);
  }
  update({});
  return { root, update, parts: { head, neck, hips } };
}

// ---------------------------------------------------------------- bot
export function createBot(THREE, opts = {}) {
  const STAND = opts.stand ?? 0.62; // pole length; the reference uses a short desk stand (~0.25)
  const P = PALETTE, M = (c, o) => flat(THREE, c, o);
  const root = new THREE.Group();

  // stand (root origin = foot of the stand); head centre at y = 1.05
  root.add(mesh(THREE, new THREE.CylinderGeometry(0.22, 0.24, 0.03, 16), M(P.stand, { roughness: 0.4 }), 0, 0.015, 0));
  root.add(mesh(THREE, new THREE.CylinderGeometry(0.018, 0.018, STAND, 8), M(P.stand, { roughness: 0.4 }), 0, STAND / 2 + 0.02, 0));

  const HY = STAND + 0.43;
  const head = new THREE.Group(); head.position.y = HY; root.add(head);
  const R = 0.42;
  head.add(mesh(THREE, new THREE.IcosahedronGeometry(R, 2), M(P.bot, { roughness: 0.62 })));

  // visor: a glossy black cap facing +z, with a cream rim
  const CAP = 0.78;
  const visorGeo = new THREE.SphereGeometry(R * 1.008, 40, 16, 0, Math.PI * 2, 0, CAP);
  visorGeo.rotateX(Math.PI / 2);
  head.add(mesh(THREE, visorGeo, new THREE.MeshStandardMaterial({ color: P.visor, roughness: 0.38, metalness: 0.1 })));
  const rimR = R * Math.sin(CAP), rimZ = R * Math.cos(CAP);
  head.add(mesh(THREE, new THREE.TorusGeometry(rimR * 1.01, 0.011, 6, 48), new THREE.MeshStandardMaterial({ color: P.rim, emissive: P.rim, emissiveIntensity: 0.35, roughness: 0.4 }), 0, 0, rimZ + 0.004));

  // glowing face elements, placed on the visor's curve
  const glowMat = new THREE.MeshBasicMaterial({ color: P.glow });
  const onVisor = (m, x, y) => { m.position.set(x, y, Math.sqrt(Math.max(0, (R * 1.02) ** 2 - x * x - y * y))); m.lookAt(x * 3, y * 3, 3); return m; };
  const eyeL = onVisor(new THREE.Mesh(new THREE.BoxGeometry(0.07, 0.042, 0.004), glowMat), -0.085, 0.06);
  const eyeR = onVisor(new THREE.Mesh(new THREE.BoxGeometry(0.07, 0.042, 0.004), glowMat), 0.085, 0.06);
  head.add(eyeL, eyeR);
  const BARS = 9, bars = [];
  for (let i = 0; i < BARS; i++) {
    const x = (i - (BARS - 1) / 2) * 0.024;
    const bar = onVisor(new THREE.Mesh(new THREE.BoxGeometry(0.013, 0.024, 0.004), glowMat), x, -0.075);
    head.add(bar); bars.push(bar);
  }
  const mouthLine = onVisor(new THREE.Mesh(new THREE.BoxGeometry(0.09, 0.012, 0.004), glowMat), 0, -0.07);
  head.add(mouthLine);

  // ears, antenna, ring
  for (const s of [-1, 1]) {
    const ear = mesh(THREE, new THREE.CylinderGeometry(0.075, 0.085, 0.07, 8), M(P.botDark), s * (R + 0.01), 0.0, -0.02);
    ear.rotation.z = Math.PI / 2; head.add(ear);
    const cap = mesh(THREE, new THREE.CylinderGeometry(0.045, 0.045, 0.03, 8), M(P.bot), s * (R + 0.05), 0, -0.02);
    cap.rotation.z = Math.PI / 2; head.add(cap);
  }
  const ant = mesh(THREE, new THREE.CylinderGeometry(0.012, 0.014, 0.2, 6), M(P.botDark), 0.05, R + 0.08, -0.04);
  ant.rotation.z = -0.12; head.add(ant);
  const ball = mesh(THREE, new THREE.IcosahedronGeometry(0.035, 1), new THREE.MeshStandardMaterial({ color: P.antennaBall, emissive: P.antennaBall, emissiveIntensity: 0.25, flatShading: true }), 0.075, R + 0.19, -0.04);
  head.add(ball);
  const ringPivot = new THREE.Group(); ringPivot.rotation.set(1.25, 0, -0.22); head.add(ringPivot);
  ringPivot.add(mesh(THREE, new THREE.TorusGeometry(R * 1.42, 0.005, 4, 96), new THREE.MeshStandardMaterial({ color: P.ring, roughness: 0.5, emissive: P.ring, emissiveIntensity: 0.2 })));

  // state: talk 0..1, t (seconds, drives the waveform), mood 'neutral'|'happy'|'squint'|'wide'|'sad',
  //        look [x,y] -1..1, blink 0..1, headTurn/headTilt/headNod, bob (seconds, idle hover), ringSpin (rad)
  function update(st = {}) {
    const t = st.t ?? 0, talk = Math.max(0, Math.min(1, st.talk ?? 0)), mood = st.mood ?? 'neutral';
    const bob = st.bob ?? t;
    head.position.y = HY + Math.sin(bob * 2.1) * 0.008;
    head.rotation.set(st.headNod ?? 0, st.headTurn ?? 0, st.headTilt ?? 0);
    ringPivot.rotation.z = -0.22 + (st.ringSpin ?? t * 0.25);
    const [lx, ly] = st.look ?? [0, 0];
    const blink = Math.max(0, Math.min(1, st.blink ?? 0));
    const eh = { neutral: 1, happy: 0.55, squint: 0.35, wide: 1.5, sad: 0.8 }[mood] ?? 1;
    [eyeL, eyeR].forEach((e, i) => {
      const x = (i ? 0.085 : -0.085) + lx * 0.03, y = 0.06 + ly * 0.025 + (mood === 'happy' ? 0.01 : 0);
      onVisor(e, x, y);
      e.scale.set(mood === 'wide' ? 0.8 : 1, Math.max(0.08, eh * (1 - blink)), 1);
      e.rotation.z += mood === 'sad' ? (i ? -0.25 : 0.25) : mood === 'squint' ? (i ? 0.15 : -0.15) : 0;
    });
    // mouth: a flat line at rest, a waveform of bars while talking
    mouthLine.visible = talk < 0.05;
    mouthLine.scale.x = mood === 'happy' ? 1.25 : mood === 'sad' ? 0.7 : 1;
    bars.forEach((b, i) => {
      b.visible = talk >= 0.05;
      const env = Math.sin((i + 0.5) / BARS * Math.PI);
      const wob = 0.55 + 0.45 * Math.sin(t * 23 + i * 1.7) * Math.sin(t * 9.3 + i * 0.6);
      b.scale.y = 0.4 + talk * env * wob * 3.2;
      const curve = mood === 'happy' ? -Math.pow((i - (BARS - 1) / 2) / 4, 2) * -0.02 : 0;
      onVisor(b, (i - (BARS - 1) / 2) * 0.024 + lx * 0.02, -0.075 + ly * 0.02 + curve);
    });
  }
  update({});
  return { root, update, parts: { head } };
}

// ---------------------------------------------------------------- shared lighting for the warm room look
export function addWarmLights(THREE, scene) {
  scene.add(new THREE.HemisphereLight(0xffc996, 0x3a2216, 0.9));
  const key = new THREE.DirectionalLight(0xffd2a0, 3.0);
  key.position.set(-2.5, 3.5, 3.0); key.castShadow = true;
  key.shadow.mapSize.set(2048, 2048); key.shadow.bias = -0.0005;
  Object.assign(key.shadow.camera, { left: -3, right: 3, top: 3, bottom: -3, near: 0.5, far: 15 });
  scene.add(key);
  const rim = new THREE.DirectionalLight(0xffa860, 1.6); rim.position.set(2.5, 2.5, -3); scene.add(rim);
  const fill = new THREE.PointLight(0xff9a50, 1.2, 6); fill.position.set(1.5, 1.2, 1.5); scene.add(fill);
}
