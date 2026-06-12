from flask import Flask, render_template, request, redirect, url_for, jsonify
from markupsafe import escape
from usuarioAD import Usuario, verificarLogin, registrarUsuario, obtenerUsuarios, obtenerUsuario, actualizarUsuario, cambiarEstadoUsuario, cambiarPassword, actualizarDatosPersonales, obtenerRoles, obtenerTecnicos, obtenerDescriptoresFaciales, guardarDescriptorFacial, eliminarDescriptorFacial
from incidenciaAD import Incidencia, insertarIncidencia, actualizarEstadoIncidencia, asignarTecnico, listarIncidencias, obtenerIncidenciaxId, obtenerTiposIncidencia, tecnicoConMenorCola
from dashboard_IncidenciasAD import reporteResumen, reportePorTipo, reportePorTecnico, calcularProyeccionMensual
from inventarioAD import PC, Componente, obtenerPCs, obtenerPC, insertarPC, actualizarPC, obtenerComponentes, obtenerComponente, insertarComponente, actualizarComponente, stockPCs
from EstructuraOrganizacionalAD import Area, listarAreas, obtenerArea, insertarArea, actualizarArea, eliminarArea, listarUsuariosConArea, asignarAreaAUsuario, listarPCsConUsuario, asignarUsuarioAPC, listarUsuariosSinPC

app = Flask(__name__)

@app.errorhandler(400)
def error_400(e): return render_template('error400.html'), 400
@app.errorhandler(500)
def error_500(e): return render_template('error500.html'), 500

# ─── AUTH ─────────────────────────────────────────────────────────
@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        error = None
        mensaje = request.args.get('mensaje')
        if request.method == 'POST':
            usuario_form  = request.form['usuario'].strip()
            password_form = request.form['password'].strip()
            if not usuario_form or not password_form:
                error = 'Completa todos los campos'
            else:
                resultado_usuario = verificarLogin(usuario_form, password_form)
                if resultado_usuario:
                    if resultado_usuario.get('primer_ingreso') == 1 or resultado_usuario.get('primer_ingreso') is True:
                        return redirect(url_for('cambiar_password', usuario_id=resultado_usuario['id']))
                    else:
                        
                        if resultado_usuario.get('rol_nombre') in ['COLABORADOR', 'TECNICO']:
                            return redirect(url_for('lista_incidencias', usuario_id=resultado_usuario['id']))
                        else:
                            return redirect(url_for('dashboard', usuario_id=resultado_usuario['id']))
                error = 'Usuario o contraseña incorrectos'
        return render_template('form_login.html', error=error, mensaje=mensaje)
    except:
        return "<p>Problemas en el procesamiento del login</p>"
@app.route('/registrarse', methods=['GET', 'POST'])
def registrarse():
    try:
        error = None
        if request.method == 'POST':
            nombre   = request.form['nombre'].strip()
            correo   = request.form['correo'].strip()
            usuario  = request.form['usuario'].strip()
            password = request.form['password'].strip()
            celular  = request.form['celular'].strip()
            if not nombre or not correo or not usuario or not password:
                error = 'Completa todos los campos obligatorios'
            elif len(password) < 6:
                error = 'La contraseña debe tener mínimo 6 caracteres'
            elif celular and (not celular.isdigit() or len(celular) != 9):
                error = 'El celular debe tener 9 dígitos'
            else:
                objUsuario = Usuario(nombre, correo, usuario, password, celular, 1)
                exito, mensaje_db = registrarUsuario(objUsuario)
                if exito:
                    return redirect(url_for('login', mensaje='Cuenta creada. Ya puedes iniciar sesión.'))
                error = mensaje_db
        return render_template('form_registrarse.html', error=error)
    except:
        return "<p>Problemas en el procesamiento del registro público</p>"

@app.route('/salir')
def salir():
    try:
        return redirect(url_for('login', mensaje='Sesión cerrada correctamente'))
    except:
        return "<p>Problemas al cerrar la sesión en el servidor</p>"

# ─── DASHBOARD ────────────────────────────────────────────────────
@app.route('/dashboard/<int:usuario_id>')
def dashboard(usuario_id):
    try:
        user = obtenerUsuario(usuario_id)
        if not user: return redirect(url_for('login'))
        es_colaborador    = (user['rol_nombre'] == 'COLABORADOR')
        es_tecnico_o_jefe = (user['rol_nombre'] in ['TECNICO', 'JEFE_TI'])
        return render_template('dashboard.html',
            id_del_usuario=usuario_id, user=user,
            incidencias=listarIncidencias(solo_propios=es_colaborador, usuario_id=usuario_id, pagina=1, por_pagina=8),
            resumen=reporteResumen() if es_tecnico_o_jefe else {},
            stock=stockPCs() if es_tecnico_o_jefe else {})
    except Exception as e:
        return f"<b style='color:red;'>ERROR REAL:</b> {e}"

# ─── PERFIL ───────────────────────────────────────────────────────
@app.route('/mi_perfil/<int:usuario_id>', methods=['GET', 'POST'])
def mi_perfil(usuario_id):
    try:
        user = obtenerUsuario(usuario_id)
        if not user: return redirect(url_for('login'))
        error = mensaje = None
        if request.method == 'POST':
            accion = request.form.get('accion')
            if accion == 'datos':
                n   = request.form.get('nombre', '').strip()
                c   = request.form.get('correo', '').strip()
                cel = request.form.get('celular', '').strip()
                if not n or not c: error = 'Nombre y correo son obligatorios'
                elif cel and (not cel.isdigit() or len(cel) != 9): error = 'El celular debe tener 9 dígitos'
                else:
                    ok, msg = actualizarDatosPersonales(usuario_id, n, c, cel)
                    if ok:
                        mensaje = 'Datos actualizados'
                        user = obtenerUsuario(usuario_id)
                    else: error = msg
            elif accion == 'password':
                pa = request.form.get('password_actual', '')
                pn = request.form.get('password_nueva', '').strip()
                pc = request.form.get('password_confirmacion', '').strip()
                if not all([pa, pn, pc]): error = 'Completa todos los campos'
                elif len(pn) < 6: error = 'Mínimo 6 caracteres'
                elif pn != pc: error = 'Las contraseñas no coinciden'
                else:
                    ok, msg = cambiarPassword(usuario_id, pa, pn, pc)
                    if ok: mensaje = 'Contraseña actualizada'
                    else: error = msg
        return render_template('form_mi_perfil.html', id_del_usuario=usuario_id, user=user, error=error, mensaje=mensaje)
    except:
        return "<p>Problemas en el procesamiento del perfil del usuario</p>"

@app.route('/cambiar_password/<int:usuario_id>', methods=['GET', 'POST'])
def cambiar_password(usuario_id):
    try:
        user = obtenerUsuario(usuario_id)
        if not user: return redirect(url_for('login'))
        error = None
        if request.method == 'POST':
            pa = request.form.get('password_actual', '')
            pn = request.form.get('password_nueva', '').strip()
            pc = request.form.get('password_confirmacion', '').strip()
            if not all([pa, pn, pc]): error = 'Completa todos los campos'
            elif len(pn) < 6: error = 'Mínimo 6 caracteres'
            elif pn != pc: error = 'Las contraseñas no coinciden'
            else:
                ok, msg = cambiarPassword(usuario_id, pa, pn, pc)
                if ok: return redirect(url_for('dashboard', usuario_id=usuario_id))
                error = msg
        return render_template('form_cambiar_password.html', id_del_usuario=usuario_id, user=obtenerUsuario(usuario_id), error=error)
    except:
        return "<p>Problemas en el cambio de contraseña obligatorio</p>"

# ─── USUARIOS ─────────────────────────────────────────────────────
@app.route('/usuarios/<int:usuario_id>')
def usuarios(usuario_id):
    try:
        pagina = int(request.args.get('pagina', 1))
        q      = request.args.get('q', '').strip()
        rol_f  = request.args.get('rol', '').strip()
        pp     = 10
        todos  = obtenerUsuarios()
        if q:     todos = [u for u in todos if q.lower() in u['nombre'].lower() or q.lower() in u['usuario'].lower()]
        if rol_f: todos = [u for u in todos if u['rol_nombre'] == rol_f]
        total  = len(todos)
        tp     = max(1, -(-total // pp))
        pagina = max(1, min(pagina, tp))
        lista  = todos[(pagina-1)*pp : pagina*pp]
        return render_template('lista_usuarios.html',
            id_del_usuario=usuario_id, user=obtenerUsuario(usuario_id),
            usuarios=lista, roles=obtenerRoles(),
            total=total, pagina=pagina, total_pags=tp,
            q=q, rol_f=rol_f, error=None, mensaje=None)
    except:
        return "<p>Problemas en el procesamiento del listado de usuarios</p>"

@app.route('/usuarios/<int:usuario_id>/nuevo', methods=['POST'])
def nuevo_usuario(usuario_id):
    try:
        n   = request.form.get('nombre', '').strip()
        c   = request.form.get('correo', '').strip()
        us  = request.form.get('usuario', '').strip()
        p   = request.form.get('password', '').strip()
        cel = request.form.get('celular', '').strip()
        rol = request.form.get('rol_id', '1')
        error = None
        if not all([n, c, us, p]): error = 'Todos los campos son obligatorios'
        elif len(p) < 6: error = 'Contraseña mínimo 6 caracteres'
        elif cel and (not cel.isdigit() or len(cel) != 9): error = 'El celular debe tener 9 dígitos'
        else:
            ok, msg = registrarUsuario(Usuario(n, c, us, p, cel, int(rol)))
            if not ok: error = msg
        todos = obtenerUsuarios()
        return render_template('lista_usuarios.html',
            id_del_usuario=usuario_id, user=obtenerUsuario(usuario_id),
            usuarios=todos[:10], roles=obtenerRoles(),
            total=len(todos), pagina=1, total_pags=max(1, -(-len(todos)//10)),
            q='', rol_f='',
            error=error, mensaje='Usuario creado exitosamente' if not error else None)
    except:
        return "<p>Problemas en el registro del nuevo usuario</p>"

@app.route('/usuarios/<int:usuario_id>/editar/<int:id_usuario_destino>', methods=['GET', 'POST'])
def editar_usuario(usuario_id, id_usuario_destino):
    try:
        user = obtenerUsuario(id_usuario_destino)
        if not user: return redirect(url_for('usuarios', usuario_id=usuario_id))
        error = None
        if request.method == 'POST':
            n   = request.form.get('nombre', '').strip()
            c   = request.form.get('correo', '').strip()
            cel = request.form.get('celular', '').strip()
            rol = request.form.get('rol_id', '1')
            if not n or not c: error = 'Nombre y correo son obligatorios'
            elif cel and (not cel.isdigit() or len(cel) != 9): error = 'El celular debe tener 9 dígitos'
            else:
                ok, msg = actualizarUsuario(id_usuario_destino, n, c, cel, int(rol))
                if ok: return redirect(url_for('usuarios', usuario_id=usuario_id))
                error = msg
        return render_template('form_usuario_edit.html', id_del_usuario=usuario_id, user=user, roles=obtenerRoles(), error=error)
    except:
        return "<p>Problemas en la edición del usuario</p>"

@app.route('/usuarios/<int:usuario_id>/estado/<int:id_usuario_destino>/<int:activo>')
def estado_usuario(usuario_id, id_usuario_destino, activo):
    try:
        if id_usuario_destino != usuario_id: cambiarEstadoUsuario(id_usuario_destino, activo)
        return redirect(url_for('usuarios', usuario_id=usuario_id))
    except:
        return "<p>Problemas al cambiar el estado del usuario</p>"

# ─── INCIDENCIAS ──────────────────────────────────────────────────
@app.route("/incidencias/<int:usuario_id>/nueva")
def cargar_formulario_incidencia(usuario_id):
    try:
        return render_template('form_incidencia.html', id_del_usuario=usuario_id, user=obtenerUsuario(usuario_id), tipos=obtenerTiposIncidencia())
    except:
        return "<p>Problemas al cargar el formulario de registros</p>"

@app.route("/incidencias/<int:usuario_id>/guardar", methods=['POST'])
def guardar_incidencia(usuario_id):
    try:
        user = obtenerUsuario(usuario_id)
        if user['rol_nombre'] == 'JEFE_TI':
            return "<p>Error de permisos: El Jefe de TI no está autorizado para registrar incidencias.</p>"
        ambiente  = request.form.get('ambiente', '').strip()
        ip_equipo = request.form.get('ip_equipo', '').strip()
        objIncidencia = Incidencia(
            0,
            request.form['titulo'].strip(),
            request.form['descripcion'].strip(),
            ambiente,
            ip_equipo,
            usuario_id,
            int(request.form['tipo_incidencia_id']),
            request.form['prioridad']
        )
        ok, incidencia_id = insertarIncidencia(objIncidencia)
        if ok and incidencia_id:
            tecnico_id = tecnicoConMenorCola()
            if tecnico_id:
                asignarTecnico(incidencia_id, tecnico_id)
            return redirect(url_for('lista_incidencias', usuario_id=usuario_id))
        return "<p>Problemas en la inserción de la incidencia</p>"
    except:
        return "<p>Problemas en el procesamiento y registro de la incidencia</p>"

@app.route("/incidencias/<int:usuario_id>")
@app.route("/mis_incidencias/<int:usuario_id>", endpoint="incidencias")
def lista_incidencias(usuario_id):
    try:
        user = obtenerUsuario(usuario_id)
        es_colaborador = (user['rol_nombre'] == 'COLABORADOR')
        orden = 'ASC' if not es_colaborador else 'DESC'
        resultado = listarIncidencias(solo_propios=es_colaborador, usuario_id=usuario_id,
                                      pagina=1, por_pagina=100, orden=orden)
        return render_template('lista_incidenciaPrincipal.html',
            id_del_usuario=usuario_id, user=obtenerUsuario(usuario_id), incidencias=resultado)
    except:
        return "<p>Problemas en el procesamiento del listado de incidencias</p>"

@app.route("/incidencias/<int:usuario_id>/detalle/<int:idIncidencia>")
def ver_detalle_incidencia(usuario_id, idIncidencia):
    try:
        user = obtenerUsuario(usuario_id)
        return render_template('form_inicidencia_edit.html',
            id_del_usuario=usuario_id, user=obtenerUsuario(usuario_id),
            incidencia=obtenerIncidenciaxId(idIncidencia),
            tecnicos=obtenerTecnicos(),
            rol_del_usuario=user['rol_nombre'] if user else '')
    except:
        return "<p>Problemas al procesar el detalle de la incidencia</p>"

@app.route("/incidencias/<int:usuario_id>/asignar_tecnico", methods=['POST'])
def asignar_tecnico_incidencia(usuario_id):
    try:
        id_incidencia = request.form['idIncidencia']
        if asignarTecnico(id_incidencia, request.form['tecnico_id']):
            return redirect(url_for('ver_detalle_incidencia', usuario_id=usuario_id, idIncidencia=id_incidencia))
        return "<p>Problemas al asignar el técnico responsable</p>"
    except:
        return "<p>Problemas en el procesamiento de la asignación técnica</p>"

@app.route("/incidencias/<int:usuario_id>/actualizar_estado", methods=['POST'])
def actualizar_estado_incidencia(usuario_id):
    try:
        id_incidencia = request.form['idIncidencia']
        if actualizarEstadoIncidencia(id_incidencia, request.form['estado'],
                                       request.form['diagnostico'].strip(),
                                       request.form['solucion'].strip()):
            return redirect(url_for('ver_detalle_incidencia', usuario_id=usuario_id, idIncidencia=id_incidencia))
        return "<p>Problemas en la actualización del estado del registro</p>"
    except:
        return "<p>Problemas en el procesamiento de la actualización</p>"

@app.route("/dashboard_incidencias_estrategico/<int:usuario_id>")
@app.route("/dashboard_incidencias/<int:usuario_id>", endpoint="dashboard_incidencias")
def dashboard_incidencias_estrategico(usuario_id):
    try:
        user = obtenerUsuario(usuario_id)
        es_colaborador = (user['rol_nombre'] == 'COLABORADOR')
        return render_template('form_dashboard_Incidencias.html',
            id_del_usuario=usuario_id, user=obtenerUsuario(usuario_id),
            resumen=reporteResumen(), por_tipo=reportePorTipo(),
            por_tecnico=reportePorTecnico(), proyeccion=calcularProyeccionMensual(),
            incidencias=listarIncidencias(solo_propios=es_colaborador, usuario_id=usuario_id, pagina=1, por_pagina=10))
    except:
        return "<p>Problemas al procesar el dashboard estratégico de incidencias</p>"

# ─── INVENTARIO ───────────────────────────────────────────────────
@app.route('/inventario/<int:usuario_id>')
def inventario(usuario_id):
    try:
        pagina   = int(request.args.get('pagina', 1))
        q        = request.args.get('q', '').strip()
        estado_f = request.args.get('estado', '').strip()
        area_f   = request.args.get('area', '').strip()
        pp       = 10
        todas    = obtenerPCs()
        if q:        todas = [p for p in todas if q.lower() in p['hostname'].lower() or q.lower() in (p['marca_modelo'] or '').lower() or q.lower() in (p['numero_serie'] or '').lower()]
        if estado_f: todas = [p for p in todas if p['estado'] == estado_f]
        if area_f:   todas = [p for p in todas if str(p.get('area_id') or '') == area_f]
        total  = len(todas)
        tp     = max(1, -(-total // pp))
        pagina = max(1, min(pagina, tp))
        pcs    = todas[(pagina-1)*pp : pagina*pp]
        return render_template('lista_inventario.html',
            id_del_usuario=usuario_id, user=obtenerUsuario(usuario_id),
            pcs=pcs, stock=stockPCs(), tecnicos=obtenerTecnicos(), areas=listarAreas(),
            total=total, pagina=pagina, total_pags=tp,
            q=q, estado_f=estado_f, area_f=area_f)
    except:
        return "<p>Problemas en el procesamiento del inventario</p>"

@app.route('/inventario/<int:usuario_id>/nueva', methods=['POST'])
def nueva_pc(usuario_id):
    try:
        error = None
        h   = request.form['hostname'].strip().upper()
        ns  = request.form['numero_serie'].strip().upper()
        mm  = request.form['marca_modelo'].strip()
        aid = request.form['area_id'].strip()
        est = request.form.get('estado', 'operativa')
        tec = request.form['tecnico_id'].strip()
        obs = request.form['observaciones'].strip()
        if not h: error = 'El hostname es obligatorio'
        elif not ns: error = 'El número de serie es obligatorio'
        else:
            if insertarPC(PC(h, ns, mm, int(aid) if aid else None, est, int(tec) if tec else None, obs)):
                return redirect(url_for('inventario', usuario_id=usuario_id))
            error = "Error al registrar la PC en la base de datos"
        todas = obtenerPCs()
        return render_template('lista_inventario.html',
            id_del_usuario=usuario_id, user=obtenerUsuario(usuario_id),
            pcs=todas[:10], stock=stockPCs(), tecnicos=obtenerTecnicos(), areas=listarAreas(),
            total=len(todas), pagina=1, total_pags=max(1, -(-len(todas)//10)),
            q='', estado_f='', area_f='', error=error)
    except:
        return "<p>Problemas en la inserción de la PC</p>"

@app.route('/inventario/<int:usuario_id>/editar/<int:pc_id>', methods=['GET', 'POST'])
def editar_pc(usuario_id, pc_id):
    try:
        error = None
        if request.method == 'POST':
            h   = request.form['hostname'].strip().upper()
            ns  = request.form['numero_serie'].strip().upper()
            mm  = request.form['marca_modelo'].strip()
            aid = request.form['area_id'].strip()
            est = request.form.get('estado', 'operativa')
            tec = request.form['tecnico_id'].strip()
            obs = request.form['observaciones'].strip()
            if not h: error = 'El hostname es obligatorio'
            elif not ns: error = 'El número de serie es obligatorio'
            else:
                if actualizarPC(pc_id, PC(h, ns, mm, int(aid) if aid else None, est, int(tec) if tec else None, obs)):
                    return redirect(url_for('inventario', usuario_id=usuario_id))
                error = "Error al actualizar los datos en el servidor"
        return render_template('form_pc_edit.html', id_del_usuario=usuario_id, user=obtenerUsuario(usuario_id),
                               pc=obtenerPC(pc_id), error=error, tecnicos=obtenerTecnicos(), areas=listarAreas())
    except:
        return "<p>Problemas en la edición de la PC</p>"

# ─── COMPONENTES ──────────────────────────────────────────────────
@app.route('/componentes/<int:usuario_id>')
def componentes(usuario_id):
    try:
        pagina = int(request.args.get('pagina', 1))
        q      = request.args.get('q', '').strip()
        tipo_f = request.args.get('tipo', '').strip()
        pp     = 10
        todos  = obtenerComponentes()
        if q:      todos = [c for c in todos if q.lower() in c['nombre'].lower()]
        if tipo_f: todos = [c for c in todos if c['tipo'] == tipo_f]
        total  = len(todos)
        tp     = max(1, -(-total // pp))
        pagina = max(1, min(pagina, tp))
        lista  = todos[(pagina-1)*pp : pagina*pp]
        return render_template('lista_componentes.html',
            id_del_usuario=usuario_id, user=obtenerUsuario(usuario_id),
            componentes=lista, total=total, pagina=pagina, total_pags=tp,
            q=q, tipo_f=tipo_f)
    except:
        return "<p>Problemas en el procesamiento de componentes</p>"

@app.route('/componentes/<int:usuario_id>/nueva', methods=['POST'])
def nuevo_componente(usuario_id):
    try:
        error = None
        n   = request.form['nombre'].strip()
        tip = request.form.get('tipo', 'Otro')
        qs  = request.form['cantidad'].strip()
        des = request.form['descripcion'].strip()
        if not n: error = 'El nombre es obligatorio'
        elif len(n) < 3: error = 'Nombre mínimo 3 caracteres'
        else:
            try:
                q = int(qs)
                if q < 0: raise ValueError
            except ValueError: error = 'La cantidad debe ser un número mayor o igual a 0'
        if not error:
            if insertarComponente(Componente(n, tip, q, des)):
                return redirect(url_for('componentes', usuario_id=usuario_id))
            error = "Error al insertar el componente en el almacén"
        todos = obtenerComponentes()
        return render_template('lista_componentes.html',
            id_del_usuario=usuario_id, user=obtenerUsuario(usuario_id),
            componentes=todos[:10], total=len(todos), pagina=1,
            total_pags=max(1, -(-len(todos)//10)), q='', tipo_f='', error=error)
    except:
        return "<p>Problemas en la inserción del componente</p>"

@app.route('/componentes/<int:usuario_id>/editar/<int:comp_id>', methods=['GET', 'POST'])
def editar_componente(usuario_id, comp_id):
    try:
        error = None
        if request.method == 'POST':
            n   = request.form['nombre'].strip()
            tip = request.form.get('tipo', 'Otro')
            qs  = request.form['cantidad'].strip()
            des = request.form['descripcion'].strip()
            if not n: error = 'El nombre es obligatorio'
            elif len(n) < 3: error = 'Nombre mínimo 3 caracteres'
            else:
                try:
                    q = int(qs)
                    if q < 0: raise ValueError
                except ValueError: error = 'La cantidad debe ser un número mayor o igual a 0'
            if not error:
                if actualizarComponente(comp_id, Componente(n, tip, q, des)):
                    return redirect(url_for('componentes', usuario_id=usuario_id))
                error = "Error al guardar los cambios del componente"
        return render_template('form_componente_edit.html', id_del_usuario=usuario_id,
                               user=obtenerUsuario(usuario_id), comp=obtenerComponente(comp_id), error=error)
    except:
        return "<p>Problemas en la edición del componente</p>"

# ─── ESTRUCTURA ORGANIZACIONAL ────────────────────────────────────
@app.route('/estructura/<int:usuario_id>')
def estructura(usuario_id):
    try:
        return render_template('lista_estructura.html', id_del_usuario=usuario_id, user=obtenerUsuario(usuario_id), areas=listarAreas())
    except:
        return "<p>Problemas al cargar el panel de estructura organizacional</p>"

@app.route('/estructura/<int:usuario_id>/areas')
def estructura_areas(usuario_id):
    try:
        return render_template('lista_areas.html', id_del_usuario=usuario_id, user=obtenerUsuario(usuario_id), areas=listarAreas(), error=None, mensaje=None)
    except:
        return "<p>Problemas al cargar el listado de áreas</p>"

@app.route('/estructura/<int:usuario_id>/areas/nueva', methods=['POST'])
def nueva_area(usuario_id):
    try:
        n   = request.form.get('nombre', '').strip()
        des = request.form.get('descripcion', '').strip()
        res = request.form.get('responsable', '').strip()
        error = mensaje = None
        if not n: error = 'El nombre del área es obligatorio'
        elif len(n) < 3: error = 'Nombre mínimo 3 caracteres'
        else:
            if insertarArea(Area(n, des, res)): mensaje = 'Área registrada exitosamente'
            else: error = 'El área ya existe en el sistema'
        return render_template('lista_areas.html', id_del_usuario=usuario_id, user=obtenerUsuario(usuario_id), areas=listarAreas(), error=error, mensaje=mensaje)
    except:
        return "<p>Problemas en el registro de la nueva área</p>"

@app.route('/estructura/<int:usuario_id>/areas/editar/<int:area_id>', methods=['GET', 'POST'])
def editar_area(usuario_id, area_id):
    try:
        area = obtenerArea(area_id)
        if not area: return redirect(url_for('estructura_areas', usuario_id=usuario_id))
        error = None
        if request.method == 'POST':
            n   = request.form.get('nombre', '').strip()
            des = request.form.get('descripcion', '').strip()
            res = request.form.get('responsable', '').strip()
            act = int(request.form.get('activa', 1))
            if not n: error = 'El nombre es obligatorio'
            elif len(n) < 3: error = 'Nombre mínimo 3 caracteres'
            else:
                if actualizarArea(area_id, Area(n, des, res, act)):
                    return redirect(url_for('estructura_areas', usuario_id=usuario_id))
                error = 'Error al actualizar los datos de la área'
        return render_template('form_area_edit.html', id_del_usuario=usuario_id, user=obtenerUsuario(usuario_id), area=area, error=error)
    except:
        return "<p>Problemas en la edición del área</p>"

@app.route('/estructura/<int:usuario_id>/areas/eliminar/<int:area_id>')
def eliminar_area(usuario_id, area_id):
    try:
        eliminarArea(area_id)
        return redirect(url_for('estructura_areas', usuario_id=usuario_id))
    except:
        return "<p>Problemas al intentar eliminar el área seleccionada</p>"

@app.route('/estructura/<int:usuario_id>/usuarios_area')
def estructura_usuarios_area(usuario_id):
    try:
        return render_template('lista_usuarios_area.html', id_del_usuario=usuario_id, user=obtenerUsuario(usuario_id), usuarios=listarUsuariosConArea(), areas=listarAreas(), error=None, mensaje=None)
    except:
        return "<p>Problemas al cargar las asignaciones de usuarios</p>"

@app.route('/estructura/<int:usuario_id>/usuarios_area/asignar', methods=['POST'])
def asignar_area_usuario(usuario_id):
    try:
        uid = request.form.get('usuario_id', '').strip()
        aid = request.form.get('area_id', '').strip()
        error = mensaje = None
        if not uid or not aid: error = 'Selecciona un usuario y un área de la lista'
        else:
            if asignarAreaAUsuario(int(uid), int(aid)): mensaje = 'Asignación guardada correctamente'
            else: error = 'Error al guardar la asignación'
        return render_template('lista_usuarios_area.html', id_del_usuario=usuario_id, user=obtenerUsuario(usuario_id), usuarios=listarUsuariosConArea(), areas=listarAreas(), error=error, mensaje=mensaje)
    except:
        return "<p>Problemas al procesar la asignación del usuario</p>"

@app.route('/estructura/<int:usuario_id>/usuarios_area/editar/<int:id_usuario_destino>', methods=['GET', 'POST'])
def editar_usuario_area(usuario_id, id_usuario_destino):
    try:
        ulist = listarUsuariosConArea()
        user  = next((x for x in ulist if x['id'] == id_usuario_destino), None)
        if not user: return redirect(url_for('estructura_usuarios_area', usuario_id=usuario_id))
        error = None
        if request.method == 'POST':
            aid = request.form.get('area_id', '').strip()
            if asignarAreaAUsuario(id_usuario_destino, int(aid) if aid else None):
                return redirect(url_for('estructura_usuarios_area', usuario_id=usuario_id))
            error = 'Error al actualizar la asignación del área'
        return render_template('form_usuario_area_edit.html', id_del_usuario=usuario_id, user=user, areas=listarAreas(), error=error)
    except:
        return "<p>Problemas en la edición de área de usuario</p>"

@app.route('/estructura/<int:usuario_id>/pcs_usuario')
def estructura_pcs_usuario(usuario_id):
    try:
        return render_template('lista_pcs_usuario.html', id_del_usuario=usuario_id, user=obtenerUsuario(usuario_id), pcs=listarPCsConUsuario(), usuarios=listarUsuariosSinPC(), error=None, mensaje=None)
    except:
        return "<p>Problemas al cargar las asignaciones de equipos</p>"

@app.route('/estructura/<int:usuario_id>/pcs_usuario/asignar', methods=['POST'])
def asignar_usuario_pc(usuario_id):
    try:
        pid = request.form.get('pc_id', '').strip()
        uid = request.form.get('usuario_id', '').strip()
        error = mensaje = None
        if not pid: error = 'Selecciona una PC'
        else:
            if asignarUsuarioAPC(int(pid), int(uid) if uid else None): mensaje = 'Asignación de equipo guardada'
            else: error = 'Error al guardar la asignación'
        return render_template('lista_pcs_usuario.html', id_del_usuario=usuario_id, user=obtenerUsuario(usuario_id), pcs=listarPCsConUsuario(), usuarios=listarUsuariosSinPC(), error=error, mensaje=mensaje)
    except:
        return "<p>Problemas al procesar la asignación del equipo</p>"

@app.route('/estructura/<int:usuario_id>/pcs_usuario/editar/<int:pc_id>', methods=['GET', 'POST'])
def editar_pc_usuario(usuario_id, pc_id):
    try:
        pcs = listarPCsConUsuario()
        pc  = next((p for p in pcs if p['id'] == pc_id), None)
        if not pc: return redirect(url_for('estructura_pcs_usuario', usuario_id=usuario_id))
        error = None
        if request.method == 'POST':
            uid = request.form.get('usuario_id', '').strip()
            if asignarUsuarioAPC(pc_id, int(uid) if uid else None):
                return redirect(url_for('estructura_pcs_usuario', usuario_id=usuario_id))
            error = 'Error al actualizar el usuario responsable'
        return render_template('form_pc_usuario_edit.html', id_del_usuario=usuario_id, user=obtenerUsuario(usuario_id), pc=pc, usuarios=listarUsuariosSinPC(), error=error)
    except:
        return "<p>Problemas en la edición de la PC asignada</p>"

# ─── API RECONOCIMIENTO FACIAL ────────────────────────────────────
@app.route('/api/facial/descriptores')
def api_facial_descriptores():
    try:
        import json
        usuarios = obtenerDescriptoresFaciales()
        resultado = []
        for u in usuarios:
            try:
                desc = json.loads(u['descriptor_facial'])
                resultado.append({'id': u['id'], 'nombre': u['nombre'], 'descriptor': desc})
            except: pass
        return jsonify(resultado)
    except:
        return jsonify([])

@app.route('/api/facial/registrar/<int:usuario_id>', methods=['POST'])
def api_facial_registrar(usuario_id):
    try:
        import json
        data = request.get_json()
        if not data or 'descriptor' not in data:
            return jsonify({'ok': False, 'error': 'Sin descriptor'})
        guardarDescriptorFacial(usuario_id, json.dumps(data['descriptor']))
        return jsonify({'ok': True})
    except:
        return jsonify({'ok': False, 'error': 'Error al guardar'})

@app.route('/api/facial/eliminar/<int:usuario_id>', methods=['POST'])
def api_facial_eliminar(usuario_id):
    try:
        eliminarDescriptorFacial(usuario_id)
        return jsonify({'ok': True})
    except:
        return jsonify({'ok': False, 'error': 'Error al eliminar'})

@app.route('/api/facial/login', methods=['POST'])
def api_facial_login():
    try:
        data = request.get_json()
        if not data or 'usuario_id' not in data:
            return jsonify({'ok': False, 'error': 'Sin usuario_id'})
        user = obtenerUsuario(int(data['usuario_id']))
        if not user or not user.get('activo'):
            return jsonify({'ok': False, 'error': 'Usuario no encontrado'})
        return jsonify({
            'ok':             True,
            'usuario_id':     user['id'],
            'rol_nombre':     user['rol_nombre'],
            'primer_ingreso': user.get('primer_ingreso', 0)
        })
    except:
        return jsonify({'ok': False, 'error': 'Error interno'})

if __name__ == '__main__':
    app.run(debug=False)