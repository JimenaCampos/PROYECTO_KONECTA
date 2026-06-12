/* chatbot_konecta.js — Konecta · Asistente navegable con historial persistente */

(function () {

  // ── Árbol de temas ───────────────────────────────────────────
  var TEMAS = [
    {
      id: 'incidencias',
      label: 'Incidencias',
      resumen: 'El modulo de incidencias permite registrar, asignar y dar seguimiento a los problemas tecnicos reportados por los colaboradores.',
      subtemas: [
        { label: 'Como registro una incidencia?',     resp: 'Ve a <b>Incidencias → Nueva incidencia</b>. Completa el tipo, descripcion y equipo relacionado. La incidencia queda en estado <b>PENDIENTE</b> y es visible para los tecnicos.' },
        { label: 'Cuales son los estados?',           resp: '<b>PENDIENTE</b> → recien registrada.<br><b>EN_DIAGNOSTICO</b> → un tecnico la esta revisando.<br><b>PROGRAMADO</b> → tiene fecha de atencion asignada.<br><b>RESUELTO</b> → el tecnico la cerro con solucion.' },
        { label: 'Quien puede ver mis incidencias?',  resp: 'El <b>Colaborador</b> solo ve sus propias incidencias. El <b>Tecnico</b> y el <b>Jefe TI</b> ven todas las incidencias del sistema.' },
        { label: 'Quien resuelve una incidencia?',    resp: 'El <b>Tecnico</b> es asignado a la incidencia y es quien cambia los estados hasta marcarla como RESUELTO. El Jefe TI tambien puede gestionarlas.' },
      ]
    },
    {
      id: 'inventario',
      label: 'Inventario de PCs',
      resumen: 'El inventario registra todas las computadoras y sus componentes. Permite rastrear el estado y la asignacion de cada equipo.',
      subtemas: [
        { label: 'Como registro una PC?',             resp: 'Ve a <b>Inventario → Nueva PC</b>. Ingresa el codigo, nombre, area asignada y estado inicial. Solo el Tecnico y el Jefe TI pueden registrar equipos.' },
        { label: 'Como agrego componentes?',          resp: 'Desde el detalle de cada PC puedes agregar componentes (procesador, RAM, disco, etc.) con su descripcion y estado. Cada cambio queda registrado en el historial.' },
        { label: 'Que estados tiene una PC?',         resp: 'Las PCs pueden estar en: <b>OPERATIVO</b> (funcionando normal), <b>EN_REPARACION</b> (siendo atendida), <b>BAJA</b> (dada de baja del sistema), o <b>EN_ALMACEN</b> (sin asignar).' },
        { label: 'Quien puede editar el inventario?', resp: 'Solo el <b>Tecnico</b> y el <b>Jefe TI</b> pueden crear, editar y cambiar el estado de PCs y componentes. El Colaborador solo puede consultarlos.' },
      ]
    },
    {
      id: 'usuarios',
      label: 'Usuarios y roles',
      resumen: 'Hay tres roles en el sistema. Cada uno tiene permisos distintos. Solo el Jefe TI puede gestionar usuarios.',
      subtemas: [
        { label: 'Cuales son los roles?',             resp: '<b>COLABORADOR:</b> registra incidencias y ve sus tickets.<br><b>TECNICO:</b> gestiona incidencias, inventario y comprobantes.<br><b>JEFE_TI:</b> acceso total — usuarios, reportes, estructura organizacional y todo lo del tecnico.' },
        { label: 'Como creo un usuario?',             resp: 'Ve a <b>Administracion → Usuarios → Nuevo usuario</b>. Solo disponible para el Jefe TI. Completa nombre, correo, usuario de login, contrasena temporal, celular y rol.' },
        { label: 'Como cambio mi contrasena?',        resp: 'Ve a <b>Mi perfil → Cambiar contrasena</b>. Ingresa tu contrasena actual y la nueva (minimo 6 caracteres). Al primer ingreso el sistema te obliga a cambiarla.' },
        { label: 'Puedo desactivar un usuario?',      resp: 'Si, el Jefe TI puede desactivar usuarios desde la lista de usuarios. Un usuario desactivado no puede iniciar sesion pero sus datos se conservan.' },
      ]
    },
    {
      id: 'estructura',
      label: 'Estructura organizacional',
      resumen: 'Permite gestionar las areas de la empresa, asignar usuarios a areas y PCs a usuarios.',
      subtemas: [
        { label: 'Como creo un area?',                resp: 'Ve a <b>Organizacion → Estructura → Nueva area</b>. Ingresa el nombre y tipo de unidad. Solo el Jefe TI puede gestionar la estructura.' },
        { label: 'Como asigno un usuario a un area?', resp: 'Desde el detalle del area, usa la seccion de integrantes para buscar y agregar usuarios. Un usuario puede pertenecer a una sola area.' },
        { label: 'Como asigno una PC a un usuario?',  resp: 'Desde el inventario, en el detalle de la PC, puedes asignarla a un usuario especifico del sistema. Tambien se puede hacer desde la estructura del area.' },
        { label: 'Que tipos de unidad existen?',      resp: 'Los tipos de unidad (Gerencia, Departamento, Area, Equipo, etc.) se gestionan desde <b>Organizacion → Tipos de unidad</b>. El Jefe TI puede crear y eliminar tipos.' },
      ]
    },
    {
      id: 'comprobantes',
      label: 'Comprobantes',
      resumen: 'Los comprobantes registran el trabajo realizado por el tecnico al resolver una incidencia.',
      subtemas: [
        { label: 'Que es un comprobante?',            resp: 'Es el registro formal del trabajo tecnico realizado. Incluye descripcion de la solucion, materiales usados, tiempo empleado y firma del colaborador conforme.' },
        { label: 'Cuando se genera?',                 resp: 'El Tecnico genera el comprobante cuando cierra una incidencia como RESUELTO. Es obligatorio para marcar la incidencia como resuelta.' },
        { label: 'Quien puede ver los comprobantes?', resp: 'El Tecnico ve los comprobantes que el genero. El Jefe TI puede ver todos los comprobantes del sistema.' },
        { label: 'Puedo editar un comprobante?',      resp: 'No. Los comprobantes son registros definitivos una vez creados. Esto garantiza la trazabilidad del trabajo tecnico realizado.' },
      ]
    },
    {
      id: 'dashboard',
      label: 'Dashboard y reportes',
      resumen: 'El dashboard muestra un resumen del estado del sistema. Los reportes avanzados solo estan disponibles para el Jefe TI.',
      subtemas: [
        { label: 'Que ve el Colaborador en el dashboard?',  resp: 'Ve sus ultimas incidencias registradas y su estado actual. No tiene acceso a metricas globales.' },
        { label: 'Que ve el Tecnico en el dashboard?',      resp: 'Ve las incidencias recientes de todo el sistema, el stock de PCs y un resumen de tickets por estado.' },
        { label: 'Que reportes tiene el Jefe TI?',          resp: 'Accede a: resumen general, incidencias por tipo, carga por tecnico y proyeccion lineal mensual de incidencias. Exportable a Excel y PDF.' },
        { label: 'Como exporto los reportes?',              resp: 'Desde la seccion de Reportes usa los botones de exportacion. El sistema genera Excel con SheetJS y PDF con html2pdf directamente en el navegador.' },
      ]
    },
  ];

  // ── Historial persistente ────────────────────────────────────
  var STORAGE_KEY = 'konecta_chat_historial';

  function guardarHistorial(lista) {
    try { sessionStorage.setItem(STORAGE_KEY, JSON.stringify(lista)); } catch (e) {}
  }

  function cargarHistorial() {
    try {
      var d = sessionStorage.getItem(STORAGE_KEY);
      return d ? JSON.parse(d) : [];
    } catch (e) { return []; }
  }

  // ── Referencias DOM ──────────────────────────────────────────
  var burbuja    = document.getElementById('chat-burbuja');
  var panel      = document.getElementById('chat-panel');
  var cerrarBtn  = document.getElementById('chat-cerrar');
  var mensajesEl = document.getElementById('chat-mensajes');
  var sugsEl     = document.getElementById('chat-sugerencias');
  var inputEl    = document.getElementById('chat-input');
  var enviarBtn  = document.getElementById('chat-enviar');

  if (!burbuja) return;

  var historialDatos = cargarHistorial();
  var temaActual     = null;

  // ── Mensajes ─────────────────────────────────────────────────
  function agregarMensaje(texto, tipo, guardar) {
    var div = document.createElement('div');
    div.className = 'chat-msg chat-msg-' + tipo;
    div.innerHTML = texto;
    mensajesEl.appendChild(div);
    mensajesEl.scrollTop = mensajesEl.scrollHeight;
    if (guardar !== false) {
      historialDatos.push({ texto: texto, tipo: tipo });
      guardarHistorial(historialDatos);
    }
  }

  function mostrarSugerencias(lista, callbacks) {
    sugsEl.innerHTML = '';
    lista.forEach(function (txt, i) {
      var btn = document.createElement('button');
      btn.className = 'chat-sug';
      btn.textContent = txt;
      btn.onclick = callbacks ? callbacks[i] : function () { procesarTexto(txt); };
      sugsEl.appendChild(btn);
    });
  }

  // ── Menu principal ───────────────────────────────────────────
  function mostrarMenuPrincipal() {
    temaActual = null;
    var labels    = TEMAS.map(function (t) { return t.label; });
    var callbacks = TEMAS.map(function (t) {
      return (function (tema) {
        return function () { abrirTema(tema); };
      })(t);
    });
    mostrarSugerencias(labels, callbacks);
  }

  // ── Abrir tema ───────────────────────────────────────────────
  function abrirTema(tema) {
    temaActual = tema;
    agregarMensaje(tema.label, 'user');
    agregarMensaje(tema.resumen, 'bot');

    var labels    = tema.subtemas.map(function (s) { return s.label; });
    var callbacks = tema.subtemas.map(function (s) {
      return (function (sub) {
        return function () { responderSubtema(sub); };
      })(s);
    });
    labels.push('Ver todos los temas');
    callbacks.push(function () {
      agregarMensaje('Ver todos los temas', 'user');
      agregarMensaje('Aqui estan todos los temas disponibles:', 'bot');
      mostrarMenuPrincipal();
    });
    mostrarSugerencias(labels, callbacks);
  }

  // ── Subtema ──────────────────────────────────────────────────
  function responderSubtema(subtema) {
    agregarMensaje(subtema.label, 'user');
    agregarMensaje(subtema.resp, 'bot');

    var labels    = [];
    var callbacks = [];

    if (temaActual) {
      temaActual.subtemas.forEach(function (s) {
        if (s.label !== subtema.label) {
          labels.push(s.label);
          callbacks.push((function (sub) {
            return function () { responderSubtema(sub); };
          })(s));
        }
      });
    }

    labels.push('Quieres saber algo mas?');
    callbacks.push(function () {
      agregarMensaje('Quieres saber algo mas?', 'user');
      agregarMensaje('Claro, aqui estan todos los temas:', 'bot');
      mostrarMenuPrincipal();
    });
    mostrarSugerencias(labels, callbacks);
  }

  // ── Texto libre ──────────────────────────────────────────────
  function procesarTexto(texto) {
    if (!texto.trim()) return;
    inputEl.value = '';

    var q = texto.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');

    for (var i = 0; i < TEMAS.length; i++) {
      var t = TEMAS[i];
      for (var j = 0; j < t.subtemas.length; j++) {
        var s  = t.subtemas[j];
        var sl = s.label.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
        if (q.split(' ').some(function (w) { return w.length > 3 && sl.indexOf(w) !== -1; })) {
          agregarMensaje(texto, 'user');
          temaActual = t;
          responderSubtema(s);
          return;
        }
      }
    }

    var mapa = {
      'incidencia': 'incidencias', 'ticket': 'incidencias',
      'inventario': 'inventario',  'pc': 'inventario', 'equipo': 'inventario', 'componente': 'inventario',
      'usuario': 'usuarios',       'rol': 'usuarios', 'contrasena': 'usuarios', 'perfil': 'usuarios',
      'area': 'estructura',        'organizacion': 'estructura', 'estructura': 'estructura',
      'comprobante': 'comprobantes',
      'reporte': 'dashboard',      'dashboard': 'dashboard', 'estadistica': 'dashboard',
    };

    var temaId = null;
    for (var clave in mapa) {
      if (q.indexOf(clave) !== -1) { temaId = mapa[clave]; break; }
    }

    agregarMensaje(texto, 'user');

    if (temaId) {
      for (var k = 0; k < TEMAS.length; k++) {
        if (TEMAS[k].id === temaId) { abrirTema(TEMAS[k]); return; }
      }
    }

    agregarMensaje('No encontre informacion exacta. Elige un tema:', 'bot');
    mostrarMenuPrincipal();
  }

  // ── Restaurar historial ──────────────────────────────────────
  function restaurarHistorial() {
    if (historialDatos.length === 0) {
      agregarMensaje('Hola! Soy el asistente de <b>Konecta</b>. Te ayudo a entender el sistema. Que necesitas saber?', 'bot', false);
      mostrarMenuPrincipal();
    } else {
      historialDatos.forEach(function (m) {
        var div = document.createElement('div');
        div.className = 'chat-msg chat-msg-' + m.tipo;
        div.innerHTML = m.texto;
        mensajesEl.appendChild(div);
      });
      mensajesEl.scrollTop = mensajesEl.scrollHeight;
      mostrarSugerencias(
        ['Continuar navegando', 'Reiniciar chat'],
        [
          function () { mostrarMenuPrincipal(); },
          function () {
            historialDatos = [];
            guardarHistorial([]);
            mensajesEl.innerHTML = '';
            sugsEl.innerHTML = '';
            agregarMensaje('Hola! Soy el asistente de <b>Konecta</b>. Que necesitas saber?', 'bot');
            mostrarMenuPrincipal();
          }
        ]
      );
    }
  }

  // ── Eventos ──────────────────────────────────────────────────
  burbuja.addEventListener('click', function () {
    panel.classList.toggle('abierto');
    if (panel.classList.contains('abierto') && mensajesEl.children.length === 0) {
      restaurarHistorial();
    }
  });

  cerrarBtn.addEventListener('click', function () {
    panel.classList.remove('abierto');
  });

  enviarBtn.addEventListener('click', function () {
    procesarTexto(inputEl.value);
  });

  inputEl.addEventListener('keydown', function (e) {
    if (e.key === 'Enter') procesarTexto(inputEl.value);
  });

})();