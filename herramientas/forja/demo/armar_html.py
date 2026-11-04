"""Arma demo/index.html: toma el prototipo de combate, le cambia el arte por el de Forja y le agrega la
exploración del Oasis de Sal (demo/exploracion.js). Se vuelve a correr cada vez que cambia el prototipo.

  python demo/armar_html.py     (desde herramientas/forja/)
"""
import os
import re

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, '..', '..', '..'))
s = open(os.path.join(RAIZ, 'prototipo', 'index.html'), encoding='utf-8').read()


def cambiar(viejo, nuevo, n=1):
    global s
    assert s.count(viejo) == n, (s.count(viejo), viejo[:90])
    s = s.replace(viejo, nuevo)


# ------------------------------------------------------------------ página y lienzo en alta resolución
cambiar('<div class="marca">El Bibliotecario <small>Prototipo de combate · El Banquete Hueco</small></div>',
        '<div class="marca">El Bibliotecario <small>Demo jugable · El Oasis de Sal</small></div>')
cambiar('<canvas id="cv" width="960" height="540" aria-label="Campo de batalla"></canvas>',
        '<canvas id="cv" width="1920" height="1080" aria-label="Juego"></canvas>')
cambiar('#cv { width: 100%; height: 100%; display: block; image-rendering: pixelated; }',
        '#cv { width: 100%; height: 100%; display: block; }')
s = re.sub(r'<title>.*?</title>', '<title>El Bibliotecario · Demo</title>', s, count=1)
cambiar("const W = 960, H = 540, P = 3, FR = 1000 / 60;",
        "const W = 960, H = 540, P = 3, FR = 1000 / 60, RES = 2; // se dibuja a 1920×1080 con coordenadas de 960×540")
cambiar("""function render() {
  ctx.setTransform(1, 0, 0, 1, 0, 0);""", """function render() {
  if (G.mode === 'explore') { renderExplore(); return; }
  ctx.setTransform(RES, 0, 0, RES, 0, 0);""")
cambiar("  ctx.setTransform(cam.z, 0, 0, cam.z, (1 - cam.z) * W / 2 + sx, (1 - cam.z) * H / 2 + sy);",
        "  ctx.setTransform(cam.z * RES, 0, 0, cam.z * RES, ((1 - cam.z) * W / 2 + sx) * RES, ((1 - cam.z) * H / 2 + sy) * RES);")
cambiar("""  // pantalla
  ctx.setTransform(1, 0, 0, 1, 0, 0);""", """  // pantalla
  ctx.setTransform(RES, 0, 0, RES, 0, 0);""")
cambiar("  ctx.drawImage(BG, -6, -6, W + 12, H + 12);",
        "  ctx.imageSmoothingEnabled = true; ctx.drawImage(ARTE.img['fondo_batalla.webp'] || BG, -6, -6, W + 12, H + 12); ctx.imageSmoothingEnabled = false;")
cambiar("  drawLanterns();\n", "")
cambiar("  if (flashA > 0.01) { ctx.globalAlpha = Math.min(1, flashA); ctx.fillStyle = flashC; ctx.fillRect(0, 0, W, H); ctx.globalAlpha = 1; }\n}",
        "  if (flashA > 0.01) { ctx.globalAlpha = Math.min(1, flashA); ctx.fillStyle = flashC; ctx.fillRect(0, 0, W, H); ctx.globalAlpha = 1; }\n  drawTransicion();\n}")

# ------------------------------------------------------------------ fuera el Teo dibujado de prueba del prototipo
i0 = s.index('// =====================================================================\n// TEO DIBUJADO A MANO')
i1 = s.index('// =====================================================================\n// DATOS: unidades')
s = s[:i0] + s[i1:]
cambiar("  if (usaDibujo(u)) return drawTeoDibujo(u, silCol);\n",
        "  if (u.hoja) return drawUnitHoja(u, silCol);\n  if (u.key === 'pavesa') { u.sy = 1 + Math.sin(now / 90) * 0.04; u.sx = 1 - Math.sin(now / 90) * 0.03; }\n")
cambiar("  if (!teo || !teo.chain || !teo.visible || TEO_DIBUJO.listo) return;", "  if (!teo || !teo.chain || !teo.visible || true) return;")
s = re.sub(r"    if \(TEO_DIBUJO\.listo\) \{.*?\}\n    else \{ const pt = portrait\('teo', \[8, 3, 11, 14\]\); ctx\.drawImage\(pt, 90, 20, pt\.width \* 18, pt\.height \* 18\); \}",
           "    ctx.imageSmoothingEnabled = true; ctx.drawImage(ARTE.img['retrato_teo.webp'], 70, 10, 280, 280); ctx.imageSmoothingEnabled = false;", s, flags=re.S)
assert 'TEO_DIBUJO' not in s and 'usaDibujo' not in s

# ------------------------------------------------------------------ medidas de sprites (hojas de Forja o pixeles)
cambiar("function headY(u) { const s = curSprite(u); return u.y + u.oy - s.height * P; }",
        "const sw = s => s.logW || s.width * P, sh = s => s.logH || s.height * P;\nfunction headY(u) { const s = curSprite(u); return u.y + u.oy - sh(s); }")
cambiar("function midY(u) { const s = curSprite(u); return u.y + u.oy - s.height * P * 0.55; }",
        "function midY(u) { const s = curSprite(u); return u.y + u.oy - sh(s) * 0.55; }")
cambiar("function curSprite(u) { if (u.key === 'don')", "function curSprite(u) { if (u.hoja) return infoCuadro(u); if (u.key === 'don')")
cambiar("const s = curSprite(u), w = s.width * P, h = s.height * P;", "const s = curSprite(u), w = sw(s), h = sh(s);")
cambiar("  const spr = curSprite(u); const w = spr.width * P, h = spr.height * P;", "  const spr = curSprite(u); const w = sw(spr), h = sh(spr);")
cambiar("  for (const g of ghosts) { const a = g.a * (1 - g.t / g.life); ctx.save();",
        "  for (const g of ghosts) { const a = g.a * (1 - g.t / g.life); if (g.spr.hoja) { drawGhostHoja(g, a); continue; } ctx.save();")
cambiar("const w = g.spr.width * P, h = g.spr.height * P;", "const w = sw(g.spr), h = sh(g.spr);")
cambiar("""function portrait(key, rect) {
  if (PORT[key]) return PORT[key];""", """function portrait(key, rect) {
  if (ARTE.listo && ['teo', 'pavesa', 'escarabajo'].includes(key)) return retratoChico(key);
  if (PORT[key]) return PORT[key];""")

# ------------------------------------------------------------------ unidades, el escarabajo y sus movimientos
cambiar("    key, def: d, name: d.name, side, x, y,", "    key, def: d, name: d.name, side, x, y, hoja: d.hoja, anim: 'reposo', animT0: 0, animDesde: 0,")
cambiar("  teo:      { name: 'Teo', spr: 'teo', hp: 260,", "  teo:      { name: 'Teo', spr: 'teo', hoja: 'teo_combate', hp: 260,")
cambiar("const DEFS = {", """const DEFS = {
  escarabajo: { name: 'Escarabajo de Sal', spr: 'escarabajo', hoja: 'escarabajo_combate', hp: 1150, post: 90, atk: 44, pod: 36, def: 22, res: 20, vel: 96,
                rank: 'mini', alcance: 205, port: [0, 0, 1, 1], aff: { brasa: 'D', luna: 'D', fis: 'R' }, moves: ['pinzas', 'oleaje', 'escupitajo', 'embestida'] },""")
cambiar("const MOVES = {", """const MOVES = {
  pinzas:     { name: 'Tenazas de Sal', melee: true, hits: [{ g: 'F', pot: 34 }, { g: 'F', pot: 34, at: 430, finta: 320 }] },
  oleaje:     { name: 'Oleaje de Arena', hits: [{ g: 'A', pot: 44, mode: 'wave' }] },
  escupitajo: { name: 'Escupitajo de Sal', hits: [{ g: 'M', pot: 30, letters: 2, mode: 'orb' }] },
  embestida:  { name: 'Embestida', melee: true, hits: [{ g: 'U', pot: 42, mode: 'grab' }] },""")
s = re.sub(r"const ENCOUNTERS = \[.*?\n\];",
           "const ENCOUNTERS = [\n  { name: 'El Escarabajo de Sal', foes: ['escarabajo'], par: 7, intro: 'Los cristales de su lomo zumban. Bebió el agua del oasis y quiere más.' },\n];",
           s, count=1, flags=re.S)
cambiar("  if (mv.melee) await moveTo(e, target.x + (e.def.boss ? 170 : 118), target.y + 2, 300);\n  else { e.ox = 10; tween(e, { ox: 0 }, 300); }",
        "  if (mv.melee) await moveTo(e, target.x + (e.def.alcance || (e.def.boss ? 170 : 118)), target.y + 2, 300);\n  else { e.ox = 10; tween(e, { ox: 0 }, 300); }\n  setAnim(e, 'ataque', 4);")
cambiar("  t.flash = 1; tween(t, { flash: 0 }, 200);\n  if (t.hp <= 0) kill(t);", "  t.flash = 1; tween(t, { flash: 0 }, 200); setAnim(t, 'golpe');\n  if (t.hp <= 0) kill(t);")
cambiar("setAnim(teo, 'ataque'); teo.rot = 0.18;", "setAnim(teo, 'ataque', 9); teo.rot = 0.08;")
cambiar("    setAnim(teo, 'ataque'); teo.rot = 0.2;", "    setAnim(teo, 'ataque', 9); teo.rot = 0.08;")
cambiar("  const pos = enc.foes.length === 1 ? [[715, 455]] : [[640, 425], [800, 462]];", "  const pos = enc.foes.length === 1 ? [[720, 458]] : [[640, 425], [800, 462]];")
cambiar("  initRibbon();\n}", "  initRibbon(); G.folioA = 0;\n}")
cambiar("ctx.fillStyle = '#7a1d22'; ctx.font = '600 13px \"Pixelify Sans\", monospace'; ctx.fillText('FOLIO', x + 12, y + 18);",
        "ctx.fillStyle = '#7a1d22'; ctx.font = '600 13px \"Pixelify Sans\", monospace'; ctx.fillText('CONSEJO', x + 12, y + 18);")
cambiar("showDesc('Folio: ' + m.text);", "showDesc('Consejo: ' + m.text);")
# el escarabajo es ancho: Teo y Pavesa se paran más lejos para golpearlo
cambiar("  await moveTo(teo, e.x + e.ox - 120, teo.y, 160);", "  await moveTo(teo, e.x + e.ox - (e.def.alcance ? 178 : 120), teo.y, 160);")
cambiar("  await moveTo(teo, t.x + t.ox - 120, teo.y, 260);", "  await moveTo(teo, t.x + t.ox - (t.def.alcance ? 178 : 120), teo.y, 260);")
cambiar("    await moveTo(pavesa, target.x + target.ox - 90, pavesa.y, 220);", "    await moveTo(pavesa, target.x + target.ox - (target.def.alcance ? 150 : 90), pavesa.y, 220);")
# arena en vez de paja dorada
cambiar("color: 'rgba(255,214,140,0.55)', kind: 'chaff'", "color: 'rgba(246,222,176,0.6)', kind: 'chaff'")

# ------------------------------------------------------------------ Pavesa dibujada, exploración y arranque
cambiar("SP.pavesa = mk(22, 16, g => {", "SP.pavesaPixel = mk(22, 16, g => {")
cambiar("// =====================================================================\n// BUCLE PRINCIPAL",
        open(os.path.join(AQUI, 'exploracion.js'), encoding='utf-8').read() + "\nSP.pavesa = pintaPavesa();\n\n// =====================================================================\n// BUCLE PRINCIPAL")
cambiar("""  update(dt);
  render();
  requestAnimationFrame(frame);""", """  update(dt);
  if (G.mode === 'explore') updExplore(dt);
  render();
  requestAnimationFrame(frame);""")
# el título y la campaña del prototipo se reemplazan por los de la demo
i0 = s.index('function titleScreen() {')
i1 = s.index('function grade(st, enc) {')
s = s[:i0] + s[i1:]
i0 = s.index('function finalCard() {')
i1 = s.index('async function victory() {')
s = s[:i0] + s[i1:]
i0 = s.index('async function campaign(start) {')
i1 = s.index('\n}\n', i0) + 3
s = s[:i0] + s[i1:]
cambiar("""function boot() {
  titleScreen();
  requestAnimationFrame(frame);
}""", """async function boot() {
  try { await cargarArte(); } catch (err) { showDesc('No se pudo cargar el arte: ' + err.message); return; }
  titleScreen();
  requestAnimationFrame(frame);
}""")

open(os.path.join(RAIZ, 'demo', 'index.html'), 'w', encoding='utf-8').write(s)
print('demo/index.html', len(s), 'caracteres')
