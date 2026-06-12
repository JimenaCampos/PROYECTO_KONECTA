import pymysql.cursors
from bd import obtenerconexion

class Usuario():
    def __init__(self, nombre, correo, usuario, password, celular, rol_id):
        self.nombre = nombre
        self.correo = correo
        self.usuario = usuario
        self.password = password
        self.celular = celular
        self.rol_id = rol_id

def verificarLogin(usuario, password):
    try:
        conn = obtenerconexion()
        with conn:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = (
                    "SELECT u.`id`, u.`nombre`, u.`correo`, u.`usuario`, u.`password`, "
                    "       u.`celular`, u.`rol_id`, u.`activo`, u.`primer_ingreso`, "
                    "       u.`descriptor_facial`, r.`nombre` AS rol_nombre "
                    "FROM `Usuario` u "
                    "JOIN `Rol` r ON u.`rol_id` = r.`id` "
                    "WHERE (u.`usuario` = %s OR u.`correo` = %s) AND u.`password` = %s AND u.`activo` = 1"
                )
                cursor.execute(sql, (usuario, usuario, password))
                return cursor.fetchone()
    except:
        raise

def registrarUsuario(objUsuario):
    try:
        conn = obtenerconexion()
        if conn:
            with conn:
                with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                    cursor.execute("SELECT `id` FROM `Usuario` WHERE `correo` = %s", (objUsuario.correo,))
                    if cursor.fetchone():
                        return False, "El correo ya está registrado"
                    cursor.execute("SELECT `id` FROM `Usuario` WHERE `usuario` = %s", (objUsuario.usuario,))
                    if cursor.fetchone():
                        return False, "El usuario ya está en uso"
                with conn.cursor() as cursor:
                    sql = (
                        "INSERT INTO `Usuario` (`nombre`, `correo`, `usuario`, `password`, `celular`, `rol_id`) "
                        "VALUES (%s, %s, %s, %s, %s, %s)"
                    )
                    cursor.execute(sql, (objUsuario.nombre, objUsuario.correo, objUsuario.usuario,
                                         objUsuario.password, objUsuario.celular, objUsuario.rol_id))
                conn.commit()
            return True, ""
        return False, "Error de conexión"
    except:
        raise

def obtenerUsuarios():
    try:
        conn = obtenerconexion()
        with conn:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = (
                    "SELECT u.`id`, u.`nombre`, u.`correo`, u.`usuario`, u.`celular`, "
                    "       u.`rol_id`, u.`activo`, r.`nombre` AS rol_nombre "
                    "FROM `Usuario` u "
                    "JOIN `Rol` r ON u.`rol_id` = r.`id` "
                    "ORDER BY u.`nombre`"
                )
                cursor.execute(sql)
                return cursor.fetchall()
    except:
        raise

def obtenerUsuario(uid):
    try:
        conn = obtenerconexion()
        with conn:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = (
                    "SELECT u.`id`, u.`nombre`, u.`correo`, u.`usuario`, u.`celular`, "
                    "       u.`rol_id`, u.`activo`, u.`descriptor_facial`, r.`nombre` AS rol_nombre "
                    "FROM `Usuario` u "
                    "JOIN `Rol` r ON u.`rol_id` = r.`id` "
                    "WHERE u.`id` = %s"
                )
                cursor.execute(sql, (uid,))
                return cursor.fetchone()
    except:
        raise

def actualizarUsuario(uid, nombre, correo, celular, rol_id):
    try:
        conn = obtenerconexion()
        if conn:
            with conn:
                with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                    cursor.execute("SELECT `id` FROM `Usuario` WHERE `correo` = %s AND `id` != %s", (correo, uid))
                    if cursor.fetchone():
                        return False, "El correo ya pertenece a otro usuario"
                with conn.cursor() as cursor:
                    sql = "UPDATE `Usuario` SET `nombre`=%s, `correo`=%s, `celular`=%s, `rol_id`=%s WHERE `id`=%s"
                    cursor.execute(sql, (nombre, correo, celular, rol_id, uid))
                conn.commit()
            return True, ""
        return False, "Error de conexión"
    except:
        raise

def cambiarEstadoUsuario(uid, activo):
    try:
        conn = obtenerconexion()
        if conn:
            with conn:
                with conn.cursor() as cursor:
                    cursor.execute("UPDATE `Usuario` SET `activo`=%s WHERE `id`=%s", (activo, uid))
                conn.commit()
            return True
        return False
    except:
        raise

def cambiarPassword(uid, pwd_actual, pwd_nueva, pwd_conf):
    try:
        conn = obtenerconexion()
        if conn:
            with conn:
                with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                    cursor.execute("SELECT `id` FROM `Usuario` WHERE `id`=%s AND `password`=%s", (uid, pwd_actual))
                    if not cursor.fetchone():
                        return False, "Contraseña actual incorrecta"
                if pwd_nueva != pwd_conf:
                    return False, "Las contraseñas no coinciden"
                if len(pwd_nueva) < 6:
                    return False, "Mínimo 6 caracteres"
                with conn.cursor() as cursor:
                    cursor.execute("UPDATE `Usuario` SET `password`=%s WHERE `id`=%s", (pwd_nueva, uid))
                conn.commit()
            return True, ""
        return False, "Error de conexión"
    except:
        raise

def actualizarDatosPersonales(uid, nombre, correo, celular):
    try:
        conn = obtenerconexion()
        if conn:
            with conn:
                with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                    cursor.execute("SELECT `id` FROM `Usuario` WHERE `correo`=%s AND `id`!=%s", (correo, uid))
                    if cursor.fetchone():
                        return False, "El correo ya está en uso"
                with conn.cursor() as cursor:
                    cursor.execute("UPDATE `Usuario` SET `nombre`=%s, `correo`=%s, `celular`=%s WHERE `id`=%s",
                                   (nombre, correo, celular, uid))
                conn.commit()
            return True, ""
        return False, "Error de conexión"
    except:
        raise

def obtenerTecnicos():
    try:
        conn = obtenerconexion()
        with conn:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = (
                    "SELECT u.`id`, u.`nombre` "
                    "FROM `Usuario` u "
                    "JOIN `Rol` r ON u.`rol_id` = r.`id` "
                    "WHERE r.`nombre` IN ('TECNICO', 'JEFE_TI') AND u.`activo` = 1 "
                    "ORDER BY u.`nombre`"
                )
                cursor.execute(sql)
                return cursor.fetchall()
    except:
        raise

def obtenerRoles():
    try:
        conn = obtenerconexion()
        with conn:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("SELECT `id`, `nombre` FROM `Rol` ORDER BY `id`")
                return cursor.fetchall()
    except:
        raise

# ══════════════════════════════════════════════
#  RECONOCIMIENTO FACIAL
# ══════════════════════════════════════════════
def obtenerDescriptoresFaciales():
    try:
        conn = obtenerconexion()
        with conn:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(
                    "SELECT `id`, `nombre`, `descriptor_facial` "
                    "FROM `Usuario` WHERE `activo`=1 AND `descriptor_facial` IS NOT NULL"
                )
                return cursor.fetchall()
    except:
        raise

def guardarDescriptorFacial(uid, descriptor_json):
    try:
        conn = obtenerconexion()
        if conn:
            with conn:
                with conn.cursor() as cursor:
                    cursor.execute("UPDATE `Usuario` SET `descriptor_facial`=%s WHERE `id`=%s",
                                   (descriptor_json, uid))
                conn.commit()
            return True
        return False
    except:
        raise

def eliminarDescriptorFacial(uid):
    try:
        conn = obtenerconexion()
        if conn:
            with conn:
                with conn.cursor() as cursor:
                    cursor.execute("UPDATE `Usuario` SET `descriptor_facial`=NULL WHERE `id`=%s", (uid,))
                conn.commit()
            return True
        return False
    except:
        raise