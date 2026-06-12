/* ═══════════════════════════════════════════
   facial_registro.js — Registro de cara en perfil
   ═══════════════════════════════════════════ */

var facialStream    = null;
var facialModels    = false;
var capturaLista    = false;
var previewInterval = null;

/* ── Cargar modelos ───────────────────────────────────── */
async function cargarModelosFacial() {
  setFacialStatus('Cargando modelos...');
  try {
    var MODEL_URL = window.FACE_MODEL_URL;
    if (!window.faceapi) {
      await new Promise(function(res, rej) {
        var s    = document.createElement('script');
        s.src    = window.FACE_API_URL;
        s.onload = res;
        s.onerror = rej;
        document.head.appendChild(s);
      });
    }
    await faceapi.nets.tinyFaceDetector.loadFromUri(MODEL_URL);
    await faceapi.nets.faceLandmark68TinyNet.loadFromUri(MODEL_URL);
    await faceapi.nets.faceRecognitionNet.loadFromUri(MODEL_URL);
    facialModels = true;
    setFacialStatus('✓ Modelos listos. Acerca tu rostro a la cámara.');
  } catch(e) {
    setFacialStatus('⚠ Error cargando modelos.');
  }
}

/* ── Cámara ───────────────────────────────────────────── */
async function iniciarCamaraRegistro() {
  if (!facialModels) await cargarModelosFacial();
  try {
    facialStream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'user' } });
    var video = document.getElementById('facial-video');
    video.srcObject = facialStream;
    await video.play();
    document.getElementById('facial-cam-wrap').style.display    = '';
    document.getElementById('btn-facial-cam').style.display     = 'none';
    document.getElementById('btn-facial-capturar').style.display = '';
    document.getElementById('btn-facial-stop').style.display    = '';
    setFacialStatus('Coloca tu rostro frente a la cámara y presiona Capturar.');
    iniciarPreviewRegistro();
  } catch(e) {
    setFacialStatus('⚠ No se pudo acceder a la cámara.');
  }
}

function iniciarPreviewRegistro() {
  var video   = document.getElementById('facial-video');
  var overlay = document.getElementById('facial-overlay');
  var opts    = new faceapi.TinyFaceDetectorOptions({ inputSize: 320, scoreThreshold: 0.5 });

  previewInterval = setInterval(async function() {
    overlay.width  = video.videoWidth;
    overlay.height = video.videoHeight;
    var ctx = overlay.getContext('2d');
    ctx.clearRect(0, 0, overlay.width, overlay.height);

    var det = await faceapi.detectSingleFace(video, opts);
    if (det) {
      var b = det.box;
      ctx.strokeStyle = '#22c55e';
      ctx.lineWidth   = 2;
      ctx.strokeRect(b.x, b.y, b.width, b.height);
      setFacialStatus('✓ Rostro detectado. Presiona Capturar.');
      capturaLista = true;
    } else {
      setFacialStatus('🔍 Buscando rostro...');
      capturaLista = false;
    }
  }, 300);
}

/* ── Capturar descriptor ──────────────────────────────── */
async function capturarDescriptor() {
  if (!capturaLista) {
    setFacialStatus('⚠ Asegúrate que tu rostro sea visible.');
    return;
  }
  clearInterval(previewInterval);
  var video   = document.getElementById('facial-video');
  var opts    = new faceapi.TinyFaceDetectorOptions({ inputSize: 320, scoreThreshold: 0.5 });
  var btnCap  = document.getElementById('btn-facial-capturar');

  setFacialStatus('Procesando... no te muevas.');
  btnCap.disabled = true;

  /* 5 capturas y promediar */
  var descriptores = [];
  for (var i = 0; i < 5; i++) {
    var det = await faceapi.detectSingleFace(video, opts)
      .withFaceLandmarks(true)
      .withFaceDescriptor();
    if (det) descriptores.push(Array.from(det.descriptor));
    await new Promise(function(r){ setTimeout(r, 200); });
  }

  if (descriptores.length < 3) {
    setFacialStatus('⚠ No se pudo capturar bien. Intenta de nuevo.');
    btnCap.disabled = false;
    iniciarPreviewRegistro();
    return;
  }

  var promedio = descriptores[0].map(function(_, idx) {
    return descriptores.reduce(function(s, d){ return s + d[idx]; }, 0) / descriptores.length;
  });

  /* Enviar al servidor */
  try {
    var r = await fetch('/api/facial/registrar/' + window.USUARIO_ID_FAC, {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify({ descriptor: promedio })
    });
    var data = await r.json();
    if (data.ok) {
      setFacialStatus('✓ Rostro registrado exitosamente.');
      detenerCamaraRegistro();
      setTimeout(function(){ window.location.reload(); }, 1200);
    } else {
      setFacialStatus('⚠ Error: ' + data.error);
      btnCap.disabled = false;
    }
  } catch(e) {
    setFacialStatus('⚠ Error de conexión.');
    btnCap.disabled = false;
  }
}

/* ── Eliminar facial ──────────────────────────────────── */
async function eliminarFacial() {
  if (!confirm('¿Eliminar el rostro registrado?')) return;
  var r    = await fetch('/api/facial/eliminar/' + window.USUARIO_ID_FAC, { method: 'POST' });
  var data = await r.json();
  if (data.ok) window.location.reload();
}

/* ── Detener cámara ───────────────────────────────────── */
function detenerCamaraRegistro() {
  clearInterval(previewInterval);
  if (facialStream) {
    facialStream.getTracks().forEach(function(t){ t.stop(); });
    facialStream = null;
  }
  document.getElementById('facial-cam-wrap').style.display       = 'none';
  document.getElementById('btn-facial-cam').style.display        = '';
  document.getElementById('btn-facial-capturar').style.display   = 'none';
  document.getElementById('btn-facial-stop').style.display       = 'none';
  setFacialStatus('Cámara detenida.');
}

/* ── Helper status ────────────────────────────────────── */
function setFacialStatus(msg) {
  var el = document.getElementById('facial-status');
  if (el) el.textContent = msg;
}