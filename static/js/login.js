/* ═══════════════════════════════════════════
   login.js — Reconocimiento facial en login
   ═══════════════════════════════════════════ */

var stream       = null;
var intervalo    = null;
var usuarioMatch = null;
var modelsLoaded = false;

/* ── Tabs ─────────────────────────────────────────────── */
function switchTab(tab) {
  document.getElementById('panel-pwd').style.display  = tab === 'pwd'  ? '' : 'none';
  document.getElementById('panel-face').style.display = tab === 'face' ? '' : 'none';
  document.getElementById('tab-pwd').classList.toggle('active',  tab === 'pwd');
  document.getElementById('tab-face').classList.toggle('active', tab === 'face');
  if (tab !== 'face') detenerCamara();
}

/* ── Status / Loader ──────────────────────────────────── */
function setStatus(tipo, msg) {
  var el = document.getElementById('face-status');
  el.className   = 'lf-status lf-status-' + tipo;
  el.textContent = msg;
}
function showLoader(msg) {
  document.getElementById('lf-loader').style.display = 'flex';
  document.getElementById('lf-loader-msg').textContent = msg || 'Cargando...';
}
function hideLoader() {
  document.getElementById('lf-loader').style.display = 'none';
}

/* ── Cargar modelos face-api ──────────────────────────── */
async function cargarModelos() {
  showLoader('Cargando modelos de reconocimiento...');
  try {
    var MODEL_URL = window.FACE_MODEL_URL;
    await faceapi.nets.tinyFaceDetector.loadFromUri(MODEL_URL);
    await faceapi.nets.faceLandmark68TinyNet.loadFromUri(MODEL_URL);
    await faceapi.nets.faceRecognitionNet.loadFromUri(MODEL_URL);
    modelsLoaded = true;
    hideLoader();
    setStatus('wait', '📷 Activa la cámara para identificarte');
  } catch(e) {
    hideLoader();
    setStatus('error', '⚠ Error cargando modelos. Usa contraseña.');
  }
}

/* ── Cámara ───────────────────────────────────────────── */
async function iniciarCamara() {
  if (!modelsLoaded) {
    setStatus('scanning', 'Espera, cargando modelos...');
    return;
  }
  try {
    stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'user' } });
    var video = document.getElementById('face-video');
    video.srcObject = stream;
    await video.play();
    document.getElementById('lf-cam-wrap').style.display    = '';
    document.getElementById('btn-camara').style.display     = 'none';
    document.getElementById('btn-detener').style.display    = '';
    document.getElementById('face-resultado').style.display = 'none';
    setStatus('scanning', '🔍 Buscando tu rostro...');
    iniciarDeteccion();
  } catch(e) {
    setStatus('error', '⚠ No se pudo acceder a la cámara');
  }
}

function detenerCamara() {
  if (intervalo) { clearInterval(intervalo); intervalo = null; }
  if (stream)    { stream.getTracks().forEach(function(t){ t.stop(); }); stream = null; }
  document.getElementById('lf-cam-wrap').style.display       = 'none';
  document.getElementById('btn-camara').style.display        = '';
  document.getElementById('btn-detener').style.display       = 'none';
  document.getElementById('face-resultado').style.display    = 'none';
  setStatus('wait', '📷 Activa la cámara para identificarte');
  usuarioMatch = null;
}

/* ── Detección ────────────────────────────────────────── */
async function iniciarDeteccion() {
  var descriptores = [];
  try {
    var r = await fetch('/api/facial/descriptores');
    descriptores = await r.json();
  } catch(e) {
    setStatus('error', '⚠ Error cargando datos');
    return;
  }
  if (!descriptores.length) {
    setStatus('warn', 'No hay rostros registrados aún');
    return;
  }

  var labeled = descriptores.map(function(u) {
    return new faceapi.LabeledFaceDescriptors(
      u.id + '|' + u.nombre,
      [new Float32Array(u.descriptor)]
    );
  });
  var matcher      = new faceapi.FaceMatcher(labeled, 0.45);
  var opts         = new faceapi.TinyFaceDetectorOptions({ inputSize: 320, scoreThreshold: 0.5 });
  var video        = document.getElementById('face-video');
  var overlay      = document.getElementById('face-overlay');
  var consecutivos = 0;

  intervalo = setInterval(async function() {
    if (!stream) return;
    overlay.width  = video.videoWidth;
    overlay.height = video.videoHeight;
    var ctx = overlay.getContext('2d');
    ctx.clearRect(0, 0, overlay.width, overlay.height);

    var dets = await faceapi
      .detectAllFaces(video, opts)
      .withFaceLandmarks(true)
      .withFaceDescriptors();

    if (!dets.length) {
      consecutivos = 0;
      setStatus('scanning', '🔍 No detecto rostro, acércate...');
      return;
    }

    var det      = dets[0];
    var match    = matcher.findBestMatch(det.descriptor);
    var box      = det.detection.box;

    ctx.strokeStyle = match.label === 'unknown' ? '#ef4444' : '#22c55e';
    ctx.lineWidth   = 3;
    ctx.strokeRect(box.x, box.y, box.width, box.height);

    if (match.label !== 'unknown') {
      consecutivos++;
      var partes    = match.label.split('|');
      var uid       = partes[0];
      var nombre    = partes[1];
      var confianza = Math.round((1 - match.distance) * 100);

      ctx.fillStyle = '#22c55e';
      ctx.font      = '13px sans-serif';
      ctx.fillText(nombre + ' ' + confianza + '%', box.x, box.y - 6);
      setStatus('found', '✓ ' + nombre + ' — ' + confianza + '% de coincidencia');

      if (consecutivos >= 8) {
        clearInterval(intervalo);
        usuarioMatch = { id: uid, nombre: nombre, confianza: confianza };
        document.getElementById('face-nombre').textContent =
          '👤 ' + nombre + ' (' + confianza + '% de coincidencia)';
        document.getElementById('face-resultado').style.display = '';
      }
    } else {
      consecutivos = 0;
      setStatus('scanning', '🔍 Rostro detectado, buscando coincidencia...');
    }
  }, 200);
}

/* ── Confirmar login ──────────────────────────────────── */
async function confirmarLogin() {
  if (!usuarioMatch) return;
  var btn = document.getElementById('btn-confirmar');
  btn.disabled    = true;
  btn.textContent = 'Verificando...';
  try {
    var r = await fetch('/api/facial/login', {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify({ usuario_id: usuarioMatch.id })
    });
    var data = await r.json();
    if (data.ok) {
      detenerCamara();
      setStatus('found', '✓ Ingresando...');
      if (data.primer_ingreso) {
        window.location.href = '/cambiar_password/' + data.usuario_id;
      } else if (data.rol_nombre === 'ADMIN' || data.rol_nombre === 'JEFE_TI') {
        window.location.href = '/dashboard/' + data.usuario_id;
      } else {
        window.location.href = '/incidencias/' + data.usuario_id;
    }
    } else {
      setStatus('error', '⚠ ' + (data.error || 'Error al ingresar'));
      btn.disabled    = false;
      btn.textContent = '✓ Confirmar ingreso';
    }
  } catch(e) {
    setStatus('error', '⚠ Error de conexión');
    btn.disabled    = false;
    btn.textContent = '✓ Confirmar ingreso';
  }
}

/* ── Init ─────────────────────────────────────────────── */
document.addEventListener('DOMContentLoaded', function() {
  var s    = document.createElement('script');
  s.src    = window.FACE_API_URL;
  s.onload = cargarModelos;
  s.onerror = function() {
    var tab = document.getElementById('tab-face');
    if (tab) { tab.disabled = true; tab.title = 'face-api.js no encontrado'; }
  };
  document.head.appendChild(s);
});