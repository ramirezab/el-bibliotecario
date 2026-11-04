// =====================================================================
// DEMO: arte de Forja, exploración del Oasis de Sal, NPC y transición al combate
// =====================================================================
const ARTE = { meta: null, img: {}, listo: false };
function cargarImg(src) { return new Promise((res, rej) => { const i = new Image(); i.onload = () => res(i); i.onerror = () => rej(new Error('No se pudo cargar ' + src)); i.src = src; }); }
async function cargarArte() {
  const meta = await fetch('arte/hojas.json').then(r => r.json());
  ARTE.meta = meta;
  const nombres = new Set(['suelo.webp', 'fondo_batalla.webp']);
  for (const [k, grupo] of Object.entries(meta)) { if (k.startsWith('_')) continue; for (const a of Object.values(grupo)) if (a && a.img) nombres.add(a.img); }
  for (const n of ['teo', 'teo_dolor', 'nadia', 'basim', 'kiko', 'pavesa']) nombres.add(`retrato_${n}.webp`);
  const lista = [...nombres]; let hechos = 0;
  await Promise.all(lista.map(n => cargarImg('arte/' + n).then(i => { ARTE.img[n] = i; hechos++; showDesc(`Cargando el arte… ${hechos}/${lista.length}`); })));
  ARTE.listo = true;
}

// ---------------------------------------------------------------------- hojas de cuadros
const tmpCv = document.createElement('canvas'); const tmpG = tmpCv.getContext('2d');
function recorteCuadro(a, i) { const [cw, ch] = a.celda; return [(i % a.columnas) * cw, Math.floor(i / a.columnas) * ch, cw, ch]; }
function siluetaCuadro(a, i, col) {
  const [sx, sy, cw, ch] = recorteCuadro(a, i);
  if (tmpCv.width < cw || tmpCv.height < ch) { tmpCv.width = Math.max(tmpCv.width, cw); tmpCv.height = Math.max(tmpCv.height, ch); }
  tmpG.globalCompositeOperation = 'source-over'; tmpG.clearRect(0, 0, cw, ch);
  tmpG.drawImage(ARTE.img[a.img], sx, sy, cw, ch, 0, 0, cw, ch);
  tmpG.globalCompositeOperation = 'source-in'; tmpG.fillStyle = col; tmpG.fillRect(0, 0, cw, ch);
  tmpG.globalCompositeOperation = 'source-over';
  return tmpCv;
}
// dibuja el cuadro i de la animación a con su punto de apoyo en (x, y); flip = -1 lo voltea
function dibujaCuadro(a, i, x, y, flip = 1, esc = 1, sesgo = 0) {
  const [sx, sy, cw, ch] = recorteCuadro(a, i); const [ax, ay] = a.apoyo;
  ctx.save(); ctx.translate(x, y); if (sesgo) ctx.transform(1, 0, sesgo, 1, 0, 0); ctx.scale(flip * esc / RES, esc / RES);
  ctx.imageSmoothingEnabled = true; ctx.imageSmoothingQuality = 'high';
  ctx.drawImage(ARTE.img[a.img], sx, sy, cw, ch, -ax, -ay, cw, ch);
  ctx.restore();
}
function indiceCuadro(a, t0, desde = 0) {
  let i = Math.floor((now - t0) / 1000 * a.fps) + desde;
  return a.bucle ? ((i % a.n) + a.n) % a.n : Math.min(Math.max(i, 0), a.n - 1);
}
// unidades de combate con hoja: animación actual, cuadro y medidas
function setAnim(u, a, desde = 0) { if (u && u.hoja) { u.anim = a; u.animT0 = now; u.animDesde = desde; } }
function infoCuadro(u) {
  const g = ARTE.meta[u.hoja]; let nombre = g[u.anim] ? u.anim : 'reposo'; let a = g[nombre];
  let i = Math.floor((now - (u.animT0 || 0)) / 1000 * a.fps) + (u.animDesde || 0);
  if (a.bucle) i = ((i % a.n) + a.n) % a.n;
  else if (i >= a.n) { u.anim = 'reposo'; u.animT0 = now; u.animDesde = 0; a = g.reposo; i = 0; }
  return { hoja: true, a, i, logW: a.celda[0] / RES * 0.62, logH: a.apoyo[1] / RES };
}
function drawUnitHoja(u, silCol) {
  const f = infoCuadro(u); const x = u.x + u.ox, y = u.y + u.oy;
  if (!silCol) { ctx.save(); ctx.globalAlpha = 0.3 * u.alpha; ctx.fillStyle = '#3a2210'; ctx.beginPath(); ctx.ellipse(u.x + u.ox, u.y + 3, f.logW * 0.5, 9, 0, 0, Math.PI * 2); ctx.fill(); ctx.restore(); }
  const [sx, sy, cw, ch] = recorteCuadro(f.a, f.i); const [ax, ay] = f.a.apoyo;
  ctx.save(); ctx.translate(x, y); ctx.rotate(u.rot); ctx.scale(u.face * u.sx, u.sy); ctx.globalAlpha = u.alpha;
  ctx.scale(1 / RES, 1 / RES); ctx.imageSmoothingEnabled = true; ctx.imageSmoothingQuality = 'high';
  if (silCol) ctx.drawImage(siluetaCuadro(f.a, f.i, silCol), 0, 0, cw, ch, -ax, -ay, cw, ch);
  else {
    ctx.drawImage(ARTE.img[f.a.img], sx, sy, cw, ch, -ax, -ay, cw, ch);
    if (u.flash > 0.01) { ctx.globalAlpha = Math.min(1, u.flash) * u.alpha * 0.85; ctx.drawImage(siluetaCuadro(f.a, f.i, '#fff8e8'), 0, 0, cw, ch, -ax, -ay, cw, ch); }
    if (u.broken) { ctx.globalAlpha = 0.2 + Math.sin(now / 90) * 0.08; ctx.drawImage(siluetaCuadro(f.a, f.i, '#ff3040'), 0, 0, cw, ch, -ax, -ay, cw, ch); }
  }
  ctx.restore();
}
function drawGhostHoja(g, alpha) {
  const f = g.spr; const [cw, ch] = f.a.celda; const [ax, ay] = f.a.apoyo;
  ctx.save(); ctx.globalAlpha = alpha; ctx.translate(g.x, g.y); ctx.scale(g.u.face / RES, 1 / RES); ctx.imageSmoothingEnabled = true;
  ctx.drawImage(siluetaCuadro(f.a, f.i, '#9fb2ff'), 0, 0, cw, ch, -ax, -ay, cw, ch); ctx.restore();
}
// retrato chico para la barra de turnos
const RETRATOS = {};
function retratoChico(key) {
  if (RETRATOS[key]) return RETRATOS[key];
  const c = document.createElement('canvas'); c.width = 48; c.height = 48; const g = c.getContext('2d'); g.imageSmoothingQuality = 'high';
  if (key === 'teo') g.drawImage(ARTE.img['retrato_teo.webp'], 0, 0, 48, 48);
  else if (key === 'pavesa') g.drawImage(ARTE.img['retrato_pavesa.webp'], 0, 0, 48, 48);
  else if (key === 'escarabajo') { const a = ARTE.meta.escarabajo_combate.reposo; const [sx, sy, cw, ch] = recorteCuadro(a, 0); const k = 48 / Math.max(cw, ch); g.drawImage(ARTE.img[a.img], sx, sy, cw, ch, (48 - cw * k) / 2, 48 - ch * k, cw * k, ch * k); }
  return (RETRATOS[key] = c);
}

// ---------------------------------------------------------------------- mundo
const MAPA = { w: 2200, h: 1400 };
const ESTANQUE = { x: 1150, y: 740, rx: 250, ry: 130 };
const PROPS = [
  // palmeras alrededor del estanque
  ['palmera', 880, 590], ['palmera', 1000, 552], ['palmera', 1330, 560], ['palmera', 1475, 650], ['palmera', 1485, 845],
  ['palmera', 1320, 945], ['palmera', 965, 930], ['palmera', 690, 650], ['palmera', 1720, 560], ['palmera', 380, 760],
  ['juncos', 925, 705], ['juncos', 1392, 772], ['juncos', 1100, 885], ['juncos', 1255, 615], ['juncos', 1010, 640],
  // aldea de tiendas
  ['tienda', 440, 905], ['tienda', 625, 850], ['tienda', 505, 1085],
  ['cajas', 708, 912], ['vasijas', 470, 990], ['vasijas_b', 742, 1012], ['cajas_b', 330, 1000],
  // pozo
  ['pozo', 1590, 990], ['vasijas', 1660, 1030], ['cajas', 1520, 1075],
  // rocas, cactus y matas
  ['roca', 300, 500], ['roca_b', 1820, 440], ['roca', 1900, 1110], ['roca_b', 255, 1200], ['roca', 1700, 720], ['roca_b', 395, 680],
  ['roca', 1760, 1250], ['cactus', 1860, 620], ['cactus', 230, 880], ['cactus', 1640, 395], ['cactus', 430, 420], ['cactus', 1980, 980],
  ['arbusto', 600, 600], ['arbusto_b', 1520, 480], ['arbusto', 1950, 880], ['arbusto_b', 345, 1110], ['arbusto', 1220, 1210],
  ['arbusto_b', 880, 1250], ['arbusto', 1690, 1180], ['arbusto_b', 300, 330], ['arbusto', 1250, 1120], ['arbusto_b', 760, 1150],
  // ruinas del norte
  ['arco', 1100, 215], ['columna', 860, 300], ['columna_b', 1340, 290], ['columna', 1450, 395], ['columna_b', 760, 420],
  ['bloque', 975, 360], ['bloque_b', 1245, 375], ['bloque', 1560, 300], ['roca_b', 650, 300],
  // entrada sur: el camino desde el desierto
  ['palmera', 920, 1180], ['palmera', 1270, 1150], ['roca', 960, 1290], ['roca_b', 1215, 1270], ['cactus', 840, 1300],
  ['arbusto', 1180, 1310], ['arbusto_b', 990, 1240], ['vasijas_b', 1235, 1215], ['palmera', 1600, 1260], ['roca', 1450, 1170],
];
// radio de choque de cada elemento (en el suelo) y si se mece con el viento
const CHOQUE = { palmera: 16, juncos: 0, tienda: 62, cajas: 24, cajas_b: 20, vasijas: 22, vasijas_b: 18, pozo: 38, roca: 26, roca_b: 24,
  cactus: 16, arbusto: 0, arbusto_b: 0, arco: 0, columna: 22, columna_b: 22, bloque: 26, bloque_b: 24 };
const MECE = { palmera: 0.025, juncos: 0.05, arbusto: 0.03, arbusto_b: 0.03 };
const NPCS = [
  { id: 'nadia', nombre: 'Nadia', x: 640, y: 965, mira: 0 },
  { id: 'basim', nombre: 'Basim', x: 1515, y: 1010, mira: 90 },
  { id: 'kiko', nombre: 'Kiko', x: 1405, y: 990, mira: -90 },
];
const ZONA_RUINAS = { x: 1100, y: 340, r: 120 };

const ZOOM = 0.62; // la cámara de exploración se aleja: el mundo se ve más grande y los personajes más chicos
const X = {
  pj: { x: 1085, y: 1300, yaw: 180, mov: false, t0: 0, paso: 0 },
  sigue: { x: 1040, y: 1320 },           // Pavesa
  cam: { x: 0, y: 0, shake: 0 },
  teclas: {}, destino: null, hablarCon: null,
  dialogo: null, bloqueo: true, flags: {}, paginas: [], tengo: 0,
  polvo: [], arena: [], escarabajo: null, avisos: {}, trans: null, fin: false,
  objetivo: 'Habla con la gente del oasis',
};
function initPaginas() {
  X.paginas = [[300, 575], [1880, 1180], [1560, 230]].map(([x, y], i) => ({ x, y, i, tomada: false }));
}

// ---------------------------------------------------------------------- choques
function libre(x, y, r = 12) {
  if (x < 170 + r || x > MAPA.w - 170 - r || y < 150 || y > MAPA.h - 70) return false;
  if (y > 1310 && (x < 1010 || x > 1170)) return false;
  const e = ESTANQUE; if (((x - e.x) / (e.rx + 10)) ** 2 + ((y - e.y) / (e.ry + 8)) ** 2 < 1) return false;
  for (const [k, px, py] of PROPS) { const c = CHOQUE[k]; if (c && Math.hypot((x - px) * 0.8, (y - py) * 1.4) < c + r) return false; }
  if (X.escarabajo && Math.hypot(x - X.escarabajo.x, (y - X.escarabajo.y) * 1.4) < 70) return false;
  // el arco: dos pilares
  for (const dx of [-50, 50]) if (Math.hypot(x - (1100 + dx), (y - 215) * 1.4) < 18 + r) return false;
  for (const n of NPCS) if (Math.hypot(x - n.x, (y - n.y) * 1.4) < 18 + r) return false;
  return true;
}

// ---------------------------------------------------------------------- diálogos
const SPK = { teo: { nombre: 'Teo', img: 'retrato_teo.webp' }, nadia: { nombre: 'Nadia, mercader', img: 'retrato_nadia.webp' },
  basim: { nombre: 'Basim, guardián del pozo', img: 'retrato_basim.webp' }, kiko: { nombre: 'Kiko', img: 'retrato_kiko.webp' }, pavesa: { nombre: 'Pavesa', img: 'retrato_pavesa.webp' } };
function decir(lineas) {
  return new Promise(res => { X.dialogo = { lineas, i: 0, t0: now, res }; SFX.click(); });
}
function avanzarDialogo() {
  const d = X.dialogo; if (!d) return;
  const txt = d.lineas[d.i][1]; const mostrados = Math.floor((now - d.t0) / 1000 * 48);
  if (mostrados < txt.length) { d.t0 = now - txt.length / 48 * 1000; return; }
  d.i++; SFX.click();
  if (d.i >= d.lineas.length) { X.dialogo = null; d.res(); return; }
  d.t0 = now;
}
async function hablar(n) {
  X.bloqueo = true; X.pj.mov = false;
  // que se miren
  n.mira = Math.atan2(X.pj.x - n.x, X.pj.y - n.y) * 180 / Math.PI;
  X.pj.yaw = Math.atan2(n.x - X.pj.x, n.y - X.pj.y) * 180 / Math.PI;
  const F = X.flags, v = F.victoria;
  if (n.id === 'nadia') {
    if (v) {
      await decir([['nadia', '¡El agua está subiendo! Lo escuché desde aquí: un crujido de sal… y luego, silencio.'],
        ['teo', 'Se metió bajo la arena. Creo que entendió que el oasis tiene dueños.'],
        ['pavesa', 'Dueños, y una llama MUY peligrosa. Que conste.'],
        ['nadia', 'Toma: agua para todo el viaje, dátiles y el mapa de la ruta de las caravanas. El desierto es largo, bibliotecario.']]);
      X.bloqueo = false; finDemo(); return;
    }
    if (!F.mision) {
      await decir([['nadia', '¡Un viajero! Perdona el desorden: la caravana no puede salir. El estanque se está secando.'],
        ['nadia', 'Algo vive bajo las ruinas del norte. Cada noche bebe un poco más del oasis y deja cristales de sal donde pisa.'],
        ['teo', '¿Un Escarabajo de Sal? Leí sobre ellos. Bueno… leí una nota al pie sobre ellos.'],
        ['nadia', 'Si lo espantas, te regalo agua para todo el viaje. Sigue el camino hacia el norte, hasta el arco de piedra.']]);
      F.mision = true; X.objetivo = 'Ve a las ruinas del norte (sigue el camino)'; SFX.fase();
    } else await decir([['nadia', 'El arco de las ruinas está al norte, siguiendo el camino. Ten cuidado con los cristales.']]);
  }
  if (n.id === 'basim') {
    if (v) await decir([['basim', 'Peleaste contestando, no pegando primero. Así se hace.'], ...(X.tengo >= 3 ? [['basim', 'Y juntaste las tres páginas. Guárdalas: el desierto se traga las historias que nadie lee.']] : [])]);
    else if (!F.basim) {
      await decir([['basim', 'Siéntate, muchacho. Este pozo es más viejo que mi abuelo, y mi abuelo era muy viejo.'],
        ['basim', 'Un consejo para pelear: no se gana pegando primero. Se gana contestando.'],
        ['basim', 'Cuando la bestia ataque verás un glifo dentro de un círculo de tinta que se cierra. Contesta justo cuando lo toque.'],
        ['basim', 'J para los golpes ◆. Espacio para saltar las olas ▲. Flechas para los conjuros ◯. Y K para esquivar lo que no se puede parar ✦.']]);
      F.basim = true;
    } else await decir([['basim', 'Recuerda: J ◆, Espacio ▲, flechas ◯ y K ✦. Contesta cuando el círculo toque el glifo.']]);
  }
  if (n.id === 'kiko') {
    if (v) await decir([['kiko', '¡Lo viste! ¡Era ENORME! Yo sabía que no me lo inventé.']]);
    else if (!F.kiko) {
      await decir([['kiko', '¿Eres un mago? ¡Haz un truco! …¿No? Bueno.'],
        ['pavesa', 'Yo soy el truco.'],
        ['kiko', '¡LA LLAMA HABLA! …Ejem. Ayer vi cristales de sal moviéndose cerca del arco. Mi mamá dice que me lo inventé.'],
        ['kiko', 'Ah, y si ves páginas brillando, son de un libro que se voló con el viento. ¡Hay tres!']]);
      F.kiko = true;
    } else await decir([['kiko', `¿Encontraste las páginas? Llevas ${X.tengo} de 3.`]]);
  }
  X.bloqueo = false;
}

// ---------------------------------------------------------------------- entrada
const MOVER = { w: [0, -1], arrowup: [0, -1], s: [0, 1], arrowdown: [0, 1], a: [-1, 0], arrowleft: [-1, 0], d: [1, 0], arrowright: [1, 0] };
document.addEventListener('keydown', e => {
  if (G.mode !== 'explore') return;
  const k = e.key.toLowerCase();
  if (MOVER[k]) { X.teclas[k] = true; X.destino = null; e.preventDefault(); }
  if (e.repeat) return;
  if (k === 'e' || k === ' ' || k === 'enter') { e.preventDefault(); interactuar(); }
});
document.addEventListener('keyup', e => { X.teclas[e.key.toLowerCase()] = false; });
window.addEventListener('blur', () => { X.teclas = {}; });
cv.addEventListener('pointerdown', e => {
  if (G.mode !== 'explore') return;
  const r = cv.getBoundingClientRect();
  const x = (e.clientX - r.left) / r.width * W / ZOOM + X.cam.x, y = (e.clientY - r.top) / r.height * H / ZOOM + X.cam.y;
  if (X.dialogo) { avanzarDialogo(); return; }
  if (X.bloqueo) return;
  const n = NPCS.find(n => Math.hypot(x - n.x, y - (n.y - 40)) < 50);
  X.destino = n ? { x: n.x, y: n.y + 34 } : { x, y }; X.hablarCon = n || null;
});
function cercano() { return NPCS.find(n => Math.hypot(X.pj.x - n.x, (X.pj.y - n.y) * 1.2) < 110); }
function interactuar() {
  if (X.dialogo) { avanzarDialogo(); return; }
  if (X.bloqueo) return;
  const n = cercano(); if (n) hablar(n);
}

// ---------------------------------------------------------------------- actualización
function updExplore(dt) {
  const s = dt / 1000, pj = X.pj;
  let vx = 0, vy = 0;
  if (!X.bloqueo && !X.dialogo) {
    for (const [k, [dx, dy]] of Object.entries(MOVER)) if (X.teclas[k]) { vx += dx; vy += dy; }
    if (!vx && !vy && X.destino) {
      const dx = X.destino.x - pj.x, dy = X.destino.y - pj.y, d = Math.hypot(dx, dy);
      if (d < 6) { X.destino = null; if (X.hablarCon) { const n = X.hablarCon; X.hablarCon = null; if (cercano() === n) hablar(n); } }
      else { vx = dx / d; vy = dy / d; }
    }
  }
  const m = Math.hypot(vx, vy);
  if (m > 0) {
    vx /= m; vy /= m;
    const vel = 175;
    const nx = pj.x + vx * vel * s, ny = pj.y + vy * vel * s * 0.92;
    let movio = false;
    if (libre(nx, pj.y)) { pj.x = nx; movio = true; }
    if (libre(pj.x, ny)) { pj.y = ny; movio = true; }
    if (!movio && X.destino) X.destino = null;
    pj.yaw = Math.atan2(vx, vy) * 180 / Math.PI;
    if (!pj.mov) { pj.mov = true; pj.t0 = now; }
    pj.paso += dt;
    if (pj.paso > 190) { pj.paso = 0; X.polvo.push({ x: pj.x + rnd(-6, 6), y: pj.y + rnd(-2, 3), t: 0, life: 520, r: rnd(4, 7) }); }
  } else if (pj.mov) { pj.mov = false; pj.t0 = now; }
  // Pavesa sigue a Teo flotando
  const fx = pj.x - 46 * Math.sign(Math.sin(pj.yaw * Math.PI / 180) || 1), fy = pj.y + 8;
  X.sigue.x += (fx - X.sigue.x) * Math.min(1, s * 3.2); X.sigue.y += (fy - X.sigue.y) * Math.min(1, s * 3.2);
  if (Math.random() < 0.3 * dt / 16.67) X.polvo.push({ x: X.sigue.x + rnd(-6, 6), y: X.sigue.y - 50 + rnd(-6, 6), t: 0, life: rnd(500, 900), r: rnd(1.5, 3), brasa: true, vy: rnd(-40, -20) });
  for (let i = X.polvo.length - 1; i >= 0; i--) { const p = X.polvo[i]; p.t += dt; if (p.vy) p.y += p.vy * s; if (p.t > p.life) X.polvo.splice(i, 1); }
  // viento con granos de arena
  if (Math.random() < 0.9 * dt / 16.67) X.arena.push({ x: X.cam.x - 20, y: X.cam.y + rnd(0, H / ZOOM), vx: rnd(90, 200), vy: rnd(-8, 12), t: 0, life: rnd(4000, 7000), r: rnd(1, 2.2) });
  for (let i = X.arena.length - 1; i >= 0; i--) { const p = X.arena[i]; p.t += dt; p.x += p.vx * s; p.y += (p.vy + Math.sin(p.t / 300) * 10) * s; if (p.t > p.life) X.arena.splice(i, 1); }
  // páginas perdidas
  for (const p of X.paginas) if (!p.tomada && Math.hypot(pj.x - p.x, pj.y - p.y) < 40) {
    p.tomada = true; X.tengo++; SFX.letra(X.tengo); SFX.firme();
    for (let k = 0; k < 18; k++) X.polvo.push({ x: p.x + rnd(-10, 10), y: p.y - 30 + rnd(-10, 10), t: 0, life: rnd(500, 900), r: rnd(2, 4), brasa: true, oro: true, vy: rnd(-80, -20) });
    showBanner(`Página perdida ${X.tengo}/3`, ['"Había una vez un reino…"', '"…que se negó a que algo terminara."', '"Mil años después, alguien tuvo que escribirle la última página."'][X.tengo - 1], '#ffe08a', 2200);
  }
  // avisos y la emboscada en las ruinas
  const enRuinas = Math.hypot(pj.x - ZONA_RUINAS.x, (pj.y - ZONA_RUINAS.y) * 1.2) < ZONA_RUINAS.r;
  if (enRuinas && !X.flags.mision && !X.avisos.ruinas && !X.bloqueo) {
    X.avisos.ruinas = true; X.bloqueo = true;
    decir([['teo', 'Las ruinas. Todo está quieto… demasiado quieto.'], ['pavesa', '¿Y si primero preguntamos qué vive aquí? Digo. Por ser prudentes. No por miedo.']]).then(() => { X.bloqueo = false; });
  }
  if (enRuinas && X.flags.mision && !X.flags.emboscada && !X.bloqueo) emboscada();
  // cámara
  const VW = W / ZOOM, VH = H / ZOOM;
  const cx = clamp(pj.x - VW / 2, 0, MAPA.w - VW), cy = clamp(pj.y - VH * (X.dialogo ? 0.36 : 0.55), 0, MAPA.h - VH);
  X.cam.x += (cx - X.cam.x) * Math.min(1, s * 5); X.cam.y += (cy - X.cam.y) * Math.min(1, s * 5);
  X.cam.shake *= Math.pow(0.86, dt / 16.67);
  if (X.escarabajo) X.escarabajo.t += dt;
}

async function emboscada() {
  X.flags.emboscada = true; X.bloqueo = true; X.pj.mov = false; X.pj.yaw = 180; X.destino = null;
  await wait(300);
  SFX.tragar(); X.cam.shake = 9;
  X.escarabajo = { x: 1100, y: 300, t: 0 };
  for (let k = 0; k < 60; k++) X.polvo.push({ x: 1100 + rnd(-80, 80), y: 300 + rnd(-20, 20), t: 0, life: rnd(600, 1300), r: rnd(4, 10), vy: rnd(-90, -10) });
  showBanner('¡El Escarabajo de Sal!', 'Los cristales de su lomo zumban', '#f6d9a8', 1800);
  await wait(1300);
  await decir([['teo', 'Eso… no es una nota al pie.'], ['pavesa', 'Bien. Bien, bien, bien. ¿Plan? ¿Tenemos plan?'], ['teo', 'Contestar. Como dijo Basim.']]);
  await transicion();
  X.escarabajo = null;
  const r = await pelea();
  if (r === 'win') {
    X.flags.victoria = true; X.objetivo = 'Vuelve con Nadia, junto a las tiendas';
    G.mode = 'explore'; mostrarPad(false); renderCmds(null, 'Explora: WASD o flechas para moverte, E para hablar, o toca el suelo.');
    showDesc('El escarabajo se hundió en la arena. El agua del oasis vuelve a subir.');
    await destapar();
    await decir([['pavesa', '¡Ja! ¿Lo viste huir? Lo asusté yo. Con mi presencia.'], ['teo', 'Vamos a avisarle a Nadia.']]);
  } else {
    G.mode = 'explore'; mostrarPad(false); X.flags.emboscada = false;
    X.pj.y = 520; await destapar();
    await decir([['teo', 'Necesito recuperar el aliento… El escarabajo sigue en las ruinas. Cuando esté listo, vuelvo.']]);
  }
  X.bloqueo = false;
}

// ---------------------------------------------------------------------- transición de tinta y paso al combate
function transicion() { return new Promise(res => { X.trans = { t0: now, dur: 750, tapa: true, res }; }); }
function destapar() { return new Promise(res => { X.trans = { t0: now, dur: 750, tapa: false, res }; }); }
const MANCHAS = Array.from({ length: 26 }, (_, i) => ({ x: (i * 377) % 960, y: (i * 211) % 540, r: 120 + (i * 53) % 110, d: (i * 29) % 220 }));
function drawTransicion() {
  const tr = X.trans; if (!tr) return;
  const p = clamp((now - tr.t0) / tr.dur, 0, 1), q = tr.tapa ? p : 1 - p;
  ctx.save(); ctx.setTransform(RES, 0, 0, RES, 0, 0); ctx.fillStyle = '#140e18';
  for (const m of MANCHAS) { const k = clamp((q * (tr.dur + 220) - m.d) / tr.dur, 0, 1) * 1.4; if (k <= 0) continue; ctx.beginPath(); ctx.arc(m.x, m.y, m.r * k, 0, Math.PI * 2); ctx.fill(); }
  if (q > 0.98) ctx.fillRect(0, 0, W, H);
  ctx.restore();
  if (p >= 1) { X.trans = null; if (!tr.tapa) tr.res(); else { tr.res(); } }
}
function mostrarPad(si) { const pad = document.getElementById('pad'); if (pad) pad.style.display = si ? '' : 'none'; const a = document.querySelector('.ayuda'); if (a) a.style.display = si ? '' : 'none'; }
async function pelea() {
  G.mode = 'battle'; mostrarPad(true);
  setupEncounter(0);
  X.trans = { t0: now, dur: 750, tapa: false, res: () => {} };
  while (true) {
    let r;
    try { r = await runBattle(0); } catch (err) { console.error(err); showDesc('Error interno: ' + err.message); return 'lose'; }
    G.activeHits = []; G.pendingTrazo = null;
    if (r === 'lose') {
      showBanner('Derrota', '', '#ff9aa0', 1500); await wait(1200);
      const ch = await defeatCard();
      if (ch === 'retry') continue;
      await transicion(); return 'lose';
    }
    await victory();
    await gradeCard(0);
    await transicion();
    return 'win';
  }
}

// ---------------------------------------------------------------------- dibujo de la exploración
function yawCuadro(yaw) {
  let q = Math.round(yaw / 45) * 45; q = ((q + 180) % 360 + 360) % 360 - 180;
  if (q === -180) q = 180;
  return q < 0 ? [-q, -1] : [q, 1];
}
function yawNpc(yaw) {
  let q = Math.round(yaw / 90) * 90; q = ((q + 180) % 360 + 360) % 360 - 180;
  if (q === -180) q = 180;
  return q < 0 ? [-q, -1] : [q, 1];
}
function sombra(x, y, rx, ry = rx * 0.36, a = 0.26) { ctx.fillStyle = `rgba(90,52,20,${a})`; ctx.beginPath(); ctx.ellipse(x, y, rx, ry, 0, 0, Math.PI * 2); ctx.fill(); }
function renderExplore() {
  ctx.setTransform(RES, 0, 0, RES, 0, 0); ctx.globalAlpha = 1; ctx.globalCompositeOperation = 'source-over';
  const sh = X.cam.shake ? rnd(-X.cam.shake, X.cam.shake) : 0;
  const cx = Math.round(X.cam.x * RES) / RES, cy = Math.round(X.cam.y * RES) / RES;
  ctx.imageSmoothingEnabled = false;
  ctx.drawImage(ARTE.img['suelo.webp'], cx * RES, cy * RES, W / ZOOM * RES, H / ZOOM * RES, sh, sh, W, H);
  ctx.scale(ZOOM, ZOOM); ctx.translate(-cx + sh, -cy + sh);
  // agua: brillos que se mueven
  const e = ESTANQUE, agua = X.flags.victoria ? 1 : 0.55;
  ctx.save(); ctx.beginPath(); ctx.ellipse(e.x, e.y, e.rx - 8, e.ry - 6, 0, 0, Math.PI * 2); ctx.clip();
  ctx.strokeStyle = `rgba(230,255,255,${0.55 * agua})`; ctx.lineWidth = 2.2; ctx.lineCap = 'round';
  for (let i = 0; i < 16; i++) {
    const a = i * 2.4, rr = 0.25 + (i * 0.37) % 0.65, x = e.x + Math.cos(a) * e.rx * rr + Math.sin(now / 1400 + i) * 12, y = e.y + Math.sin(a) * e.ry * rr;
    const al = 0.5 + 0.5 * Math.sin(now / 600 + i * 1.7); ctx.globalAlpha = al;
    ctx.beginPath(); ctx.moveTo(x - 10, y); ctx.quadraticCurveTo(x, y - 3, x + 10, y); ctx.stroke();
  }
  ctx.restore();
  // polvo de pasos (debajo de todo)
  for (const p of X.polvo) if (!p.brasa) { const k = p.t / p.life; ctx.fillStyle = `rgba(214,180,124,${0.55 * (1 - k)})`; ctx.beginPath(); ctx.ellipse(p.x, p.y - k * 8, p.r * (1 + k * 1.5), p.r * 0.6 * (1 + k), 0, 0, Math.PI * 2); ctx.fill(); }
  // todo lo que tiene profundidad, ordenado por y
  const cosas = [];
  for (const [k, x, y] of PROPS) cosas.push({ y, f: () => { const a = ARTE.meta.props[k]; if (!a) return; if (CHOQUE[k]) sombra(x, y, a.celda[0] / RES * 0.28); dibujaCuadro(a, 0, x, y, 1, 1, MECE[k] ? MECE[k] * Math.sin(now / 900 + x * 0.01) : 0); } });
  for (const n of NPCS) cosas.push({ y: n.y, f: () => { const [q, flip] = yawNpc(n.mira); const a = ARTE.meta[n.id]['reposo_' + q]; sombra(n.x, n.y, 26); dibujaCuadro(a, indiceCuadro(a, n.x * 7), n.x, n.y, flip); } });
  const pj = X.pj;
  cosas.push({ y: pj.y, f: () => { const [q, flip] = yawCuadro(pj.yaw); const a = ARTE.meta.teo[(pj.mov ? 'caminar_' : 'reposo_') + q]; sombra(pj.x, pj.y, 28); dibujaCuadro(a, indiceCuadro(a, pj.t0), pj.x, pj.y, flip); } });
  cosas.push({ y: X.sigue.y, f: () => { const [q, flip] = yawNpc(pj.yaw); const a = ARTE.meta.pavesa[(pj.mov ? 'caminar_' : 'reposo_') + q]; sombra(X.sigue.x, X.sigue.y, 12, 4, 0.18); dibujaCuadro(a, indiceCuadro(a, 0), X.sigue.x, X.sigue.y - 22, flip); } });
  if (X.escarabajo) { const b = X.escarabajo, k = clamp(b.t / 900, 0, 1); cosas.push({ y: b.y, f: () => { const a = ARTE.meta.escarabajo.reposo_20; sombra(b.x, b.y, 70 * k); ctx.save(); ctx.globalAlpha = k; dibujaCuadro(a, indiceCuadro(a, 0), b.x, b.y + (1 - k) * 40, 1, 0.7 + 0.3 * k); ctx.restore(); } }); }
  for (const p of X.paginas) if (!p.tomada) cosas.push({ y: p.y, f: () => dibujaPagina(p) });
  cosas.sort((a, b) => a.y - b.y).forEach(c => c.f());
  // brasas de Pavesa y destellos
  ctx.globalCompositeOperation = 'lighter';
  for (const p of X.polvo) if (p.brasa) { const k = p.t / p.life; ctx.fillStyle = p.oro ? `rgba(255,224,138,${1 - k})` : `rgba(255,150,60,${0.9 * (1 - k)})`; ctx.beginPath(); ctx.arc(p.x, p.y, p.r * (1 - k * 0.5), 0, Math.PI * 2); ctx.fill(); }
  ctx.globalCompositeOperation = 'source-over';
  for (const p of X.arena) { ctx.fillStyle = `rgba(250,226,180,${0.6 * Math.min(1, (p.life - p.t) / 800)})`; ctx.fillRect(p.x, p.y, p.r * 2.4, p.r); }
  // burbuja para hablar
  const n = !X.bloqueo && !X.dialogo && cercano();
  if (n) { const b = Math.sin(now / 200) * 2; ctx.save(); ctx.setTransform(RES, 0, 0, RES, 0, 0); ctx.translate((n.x - cx) * ZOOM, (n.y - cy) * ZOOM - 84 + b); ctx.fillStyle = '#f6ecd6'; ctx.strokeStyle = '#3a2a18'; ctx.lineWidth = 2; ctx.beginPath(); ctx.roundRect(-36, -14, 72, 28, 8); ctx.fill(); ctx.stroke(); ctx.fillStyle = '#7a1d22'; ctx.font = '600 15px "Pixelify Sans", monospace'; ctx.textAlign = 'center'; ctx.fillText('E  Hablar', 0, 5); ctx.restore(); }
  // pantalla
  ctx.setTransform(RES, 0, 0, RES, 0, 0);
  const v = ctx.createRadialGradient(W / 2, H / 2, H * 0.45, W / 2, H / 2, H * 0.95); v.addColorStop(0, 'rgba(0,0,0,0)'); v.addColorStop(1, 'rgba(70,30,10,0.32)'); ctx.fillStyle = v; ctx.fillRect(0, 0, W, H);
  drawHudExplore();
  drawDialogo();
  drawBanner();
  drawTransicion();
}
function dibujaPagina(p) {
  sombra(p.x, p.y, 10, 3.5, 0.2);
  dibujaCuadro(ARTE.meta.props.pagina, 0, p.x, p.y - 16 + Math.sin(now / 400 + p.i) * 4);
}
function drawHudExplore() {
  ctx.save();
  ctx.font = 'italic 17px "IM Fell English", Georgia, serif';
  const txt = 'Objetivo: ' + X.objetivo; const w = ctx.measureText(txt).width + 28;
  ctx.fillStyle = 'rgba(246,236,214,0.92)'; ctx.strokeStyle = '#6b5332'; ctx.lineWidth = 2;
  ctx.beginPath(); ctx.roundRect(14, 12, w, 32, 4); ctx.fill(); ctx.stroke();
  ctx.fillStyle = '#2a2018'; ctx.fillText(txt, 28, 34);
  ctx.beginPath(); ctx.roundRect(W - 132, 12, 118, 32, 4); ctx.fillStyle = 'rgba(246,236,214,0.92)'; ctx.fill(); ctx.stroke();
  ctx.fillStyle = '#7a1d22'; ctx.textAlign = 'right'; ctx.fillText(`Páginas ${X.tengo}/3`, W - 26, 34);
  ctx.restore();
}
function drawDialogo() {
  const d = X.dialogo; if (!d) return;
  const [quien, txt] = d.lineas[d.i]; const spk = SPK[quien];
  const n = Math.floor((now - d.t0) / 1000 * 48); const vis = txt.slice(0, n);
  // el cuadro va abajo, salvo que tape a Teo: entonces sube
  const x = 70, w = W - 140, h = 158, y = (X.pj.y - X.cam.y) * ZOOM > 300 ? 54 : 362;
  ctx.save();
  ctx.fillStyle = 'rgba(246,236,214,0.97)'; ctx.strokeStyle = '#3a2a18'; ctx.lineWidth = 3;
  ctx.beginPath(); ctx.roundRect(x, y, w, h, 10); ctx.fill(); ctx.stroke();
  ctx.strokeStyle = '#b89a6a'; ctx.lineWidth = 1.2; ctx.beginPath(); ctx.roundRect(x + 6, y + 6, w - 12, h - 12, 7); ctx.stroke();
  // retrato
  const px = x + 14, py = y + 14, ps = 130;
  ctx.fillStyle = '#e2cfa6'; ctx.beginPath(); ctx.roundRect(px, py, ps, ps, 8); ctx.fill();
  ctx.save(); ctx.beginPath(); ctx.roundRect(px, py, ps, ps, 8); ctx.clip(); ctx.imageSmoothingEnabled = true; ctx.imageSmoothingQuality = 'high';
  ctx.drawImage(ARTE.img[spk.img], px - 6, py - 2, ps + 12, ps + 12);
  ctx.restore();
  ctx.strokeStyle = '#3a2a18'; ctx.lineWidth = 2; ctx.beginPath(); ctx.roundRect(px, py, ps, ps, 8); ctx.stroke();
  // nombre y texto
  ctx.fillStyle = '#7a1d22'; ctx.font = '600 16px "Pixelify Sans", monospace'; ctx.fillText(spk.nombre.toUpperCase(), px + ps + 18, y + 34);
  ctx.fillStyle = '#2a2018'; ctx.font = '20px "IM Fell English", Georgia, serif';
  const lineas = wrapTextW(vis, w - ps - 60, ctx); lineas.forEach((l, i) => ctx.fillText(l, px + ps + 18, y + 64 + i * 26));
  if (n >= txt.length && Math.floor(now / 350) % 2) { ctx.fillStyle = '#7a1d22'; ctx.font = '16px "Pixelify Sans", monospace'; ctx.textAlign = 'right'; ctx.fillText('▼ E', x + w - 20, y + h - 16); }
  ctx.restore();
}
function wrapTextW(t, maxW, c) {
  const out = []; let line = '';
  for (const word of t.split(' ')) { const test = line ? line + ' ' + word : word; if (c.measureText(test).width > maxW && line) { out.push(line); line = word; } else line = test; }
  if (line) out.push(line); return out;
}

// ---------------------------------------------------------------------- inicio y fin de la demo
function titleScreen() {
  G.mode = 'explore'; X.bloqueo = true; initPaginas();
  mostrarPad(false);
  renderCmds(null, 'Explora: WASD o flechas para moverte, E para hablar, o toca el suelo para caminar.');
  showDesc('Demo jugable: exploración, NPC, una pelea con la Réplica y el arte hecho con Forja.');
  const c = card(`
    <h1>El Bibliotecario</h1>
    <p class="sub">Demo jugable · El Oasis de Sal</p>
    <p>Teo y Pavesa llegan a un oasis que se está secando. Habla con la gente, busca las páginas perdidas y enfrenta lo que vive bajo las ruinas.</p>
    <p><b>WASD</b> o <b>flechas</b> para moverte (o toca el suelo) · <b>E</b>, <b>Espacio</b> o <b>Enter</b> para hablar.</p>
    <p>En combate: ◆ <b>J</b> desviar · ◯ <b>flechas</b> refutar · ▲ <b>Espacio</b> saltar · ✦ <b>K</b> esquivar.</p>
    ${optionsHtml()}
    <div class="acciones"><button class="btn-grande" id="t-start">Comenzar</button></div>`);
  wireOptions(c);
  c.querySelector('#t-start').addEventListener('click', async () => {
    audioInit(); closeCard();
    await wait(400);
    await decir([['teo', 'El Oasis de Sal. Según el mapa del viejo, aquí empieza el desierto de verdad.'],
      ['pavesa', '¿Agua? ¿Dónde? Yo solo veo arena… y arena con sombrero.'],
      ['teo', 'Hay gente junto a las tiendas. Preguntemos antes de seguir.']]);
    X.bloqueo = false;
  });
}
function finDemo() {
  if (X.fin) return; X.fin = true; X.bloqueo = true; SFX.victoria();
  const c = card(`<h1>Fin de la demo</h1>
    <p class="sub">El agua vuelve al Oasis de Sal. Páginas encontradas: ${X.tengo} de 3.</p>
    <p>Esto fue una prueba de cómo se mueve <b>El Bibliotecario</b>: exploración en vista cenital, NPC con diálogos, una pelea con la Réplica y sus efectos, y todo el arte dibujado con Forja.</p>
    <div class="acciones"><button class="btn-grande" id="f-again">Jugar otra vez</button><a class="btn-sec" href="../" id="f-lore">Leer la biblia</a></div>`);
  c.querySelector('#f-again').addEventListener('click', () => location.reload());
}
