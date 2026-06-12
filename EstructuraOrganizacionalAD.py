import pymysql.cursors
from bd import obtenerconexion

class Area():
    def __init__(self, nombre, descripcion, responsable, activa=1):
        self.nombre = nombre
        self.descripcion = descripcion
        self.responsable = responsable
        self.activa = activa


def listarAreas():
    try:
        conn = obtenerconexion()
        with conn:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = (
                    "SELECT a.*, COUNT(p.`id`) AS total_pcs "
                    "FROM `Area` a "
                    "LEFT JOIN `PC` p ON p.`area_id` = a.`id` "
                    "GROUP BY a.`id` "
                    "ORDER BY a.`nombre`"
                )
                cursor.execute(sql)
                return cursor.fetchall()
    except:
        raise

def obtenerArea(area_id):
    try:
        conn = obtenerconexion()
        with conn:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = "SELECT * FROM `Area` WHERE `id` = %s"
                cursor.execute(sql, (area_id,))
                return cursor.fetchone()
    except:
        raise

def insertarArea(obj):
    try:
        conn = obtenerconexion()
        if conn:
            with conn:
                # Cursor estándar para operaciones de escritura con commit explícito
                with conn.cursor() as cursor:
                    sql = "INSERT INTO `Area` (`nombre`, `descripcion`, `responsable`, `activa`) VALUES (%s, %s, %s, %s)"
                    cursor.execute(sql, (obj.nombre, obj.descripcion, obj.responsable, obj.activa))
                conn.commit()
            return True
        return False
    except:
        raise

def actualizarArea(area_id, obj):
    try:
        conn = obtenerconexion()
        if conn:
            with conn:
                with conn.cursor() as cursor:
                    sql = "UPDATE `Area` SET `nombre` = %s, `descripcion` = %s, `responsable` = %s, `activa` = %s WHERE `id` = %s"
                    cursor.execute(sql, (obj.nombre, obj.descripcion, obj.responsable, obj.activa, area_id))
                conn.commit()
            return True
        return False
    except:
        raise

def eliminarArea(area_id):
    try:
        conn = obtenerconexion()
        if conn:
            with conn:
                with conn.cursor() as cursor:
                    sql = "DELETE FROM `Area` WHERE `id` = %s"
                    cursor.execute(sql, (area_id,))
                conn.commit()
            return True
        return False
    except:
        raise

def listarUsuariosConArea():
    try:
        conn = obtenerconexion()
        with conn:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = (
                    "SELECT u.`id`, u.`nombre`, u.`correo`, u.`activo`, r.`nombre` AS rol_nombre, "
                    "       a.`id` AS area_id, a.`nombre` AS area_nombre "
                    "FROM `Usuario` u "
                    "JOIN `Rol` r ON u.`rol_id` = r.`id` "
                    "LEFT JOIN `Area` a ON u.`area_id` = a.`id` "
                    "ORDER BY a.`nombre`, u.`nombre`"
                )
                cursor.execute(sql)
                return cursor.fetchall()
    except:
        raise

def asignarAreaAUsuario(usuario_id, area_id):
    try:
        conn = obtenerconexion()
        if conn:
            with conn:
                with conn.cursor() as cursor:
                    sql = "UPDATE `Usuario` SET `area_id` = %s WHERE `id` = %s"
                    cursor.execute(sql, (area_id or None, usuario_id))
                conn.commit()
            return True
        return False
    except:
        raise

def listarPCsConUsuario():
    try:
        conn = obtenerconexion()
        with conn:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = (
                    "SELECT p.`id`, p.`hostname`, p.`marca_modelo`, p.`estado`, "
                    "       a.`nombre` AS area_nombre, u.`id` AS usuario_id, u.`nombre` AS usuario_nombre "
                    "FROM `PC` p "
                    "LEFT JOIN `Area` a ON p.`area_id` = a.`id` "
                    "LEFT JOIN `Usuario` u ON p.`usuario_id` = u.`id` "
                    "ORDER BY p.`hostname`"
                )
                cursor.execute(sql)
                return cursor.fetchall()
    except:
        raise

def asignarUsuarioAPC(pc_id, usuario_id):
    try:
        conn = obtenerconexion()
        if conn:
            with conn:
                with conn.cursor() as cursor:
                    sql = "UPDATE `PC` SET `usuario_id` = %s WHERE `id` = %s"
                    cursor.execute(sql, (usuario_id or None, pc_id))
                conn.commit()
            return True
        return False
    except:
        raise

def listarUsuariosSinPC():
    try:
        conn = obtenerconexion()
        with conn:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = (
                    "SELECT u.`id`, u.`nombre`, r.`nombre` AS rol_nombre "
                    "FROM `Usuario` u "
                    "JOIN `Rol` r ON u.`rol_id` = r.`id` "
                    "WHERE u.`activo` = 1 "
                    "ORDER BY u.`nombre`"
                )
                cursor.execute(sql)
                return cursor.fetchall()
    except:
        raise