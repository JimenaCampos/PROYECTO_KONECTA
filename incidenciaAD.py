import pymysql.cursors
from bd import obtenerconexion 

class Incidencia():
    def __init__(self, idIncidencia, titulo, descripcion, ambiente, ip_equipo,
                 usuario_id, tipo_incidencia_id, prioridad):
        self.idIncidencia       = idIncidencia
        self.titulo             = titulo
        self.descripcion        = descripcion
        self.ambiente           = ambiente
        self.ip_equipo          = ip_equipo
        self.usuario_id         = usuario_id
        self.tipo_incidencia_id = tipo_incidencia_id
        self.prioridad          = prioridad

def obtenerTiposIncidencia():
    try:
        conn = obtenerconexion() 
        with conn:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = "SELECT `id`, `nombre_problema`, `descripcion` FROM `TipoIncidencia` ORDER BY `nombre_problema`"
                cursor.execute(sql)
                result = cursor.fetchall()
                return result
    except:    
        raise

def contarIncidencias(solo_propios=False, usuario_id=None, estado=None, prioridad=None, tecnico_id=None):
    try:
        conn = obtenerconexion()
        with conn:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = "SELECT COUNT(*) AS total FROM `Incidencia` i"
                sql += " WHERE 1=1"
                params = []
                
                if solo_propios and usuario_id:
                    sql += " AND i.`usuario_id` = %s"
                    params.append(usuario_id)
                if estado:
                    sql += " AND i.`estado` = %s"
                    params.append(estado)
                if prioridad:
                    sql += " AND i.`prioridad` = %s"
                    params.append(prioridad)
                if tecnico_id:
                    sql += " AND i.`tecnico_id` = %s"
                    params.append(tecnico_id)
                    
                cursor.execute(sql, tuple(params) if params else None)
                result = cursor.fetchone()
                
                if result:
                    return result.get('total', 0) if isinstance(result, dict) else result[0]
                return 0
    except:
        raise

def listarIncidencias(solo_propios=False, usuario_id=None, estado=None, prioridad=None, tecnico_id=None, pagina=1, por_pagina=10, orden='DESC'):
    try:
        conn = obtenerconexion()
        with conn:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                sql =  "SELECT i.`id`, i.`titulo`, i.`descripcion`, i.`ambiente`, i.`ip_equipo`,"
                sql += " i.`usuario_id`, i.`tecnico_id`, i.`tipo_incidencia_id`,"
                sql += " i.`prioridad`, i.`estado`, i.`diagnostico`, i.`solucion`, i.`fecha_creacion`, i.`fecha_cierre`,"
                sql += " u.`nombre` AS usuario_nombre, tec.`nombre` AS tecnico_nombre, ti.`nombre_problema`"
                sql += " FROM `Incidencia` i"
                sql += " JOIN `Usuario` u ON i.`usuario_id` = u.`id`"
                sql += " LEFT JOIN `Usuario` tec ON i.`tecnico_id` = tec.`id`"
                sql += " JOIN `TipoIncidencia` ti ON i.`tipo_incidencia_id` = ti.`id`"
                sql += " WHERE 1=1"

                params = []
                if solo_propios and usuario_id:
                    sql += " AND i.`usuario_id` = %s"
                    params.append(usuario_id)
                if estado:
                    sql += " AND i.`estado` = %s"
                    params.append(estado)
                if prioridad:
                    sql += " AND i.`prioridad` = %s"
                    params.append(prioridad)
                if tecnico_id:
                    sql += " AND i.`tecnico_id` = %s"
                    params.append(tecnico_id)

                orden_sql = 'ASC' if orden == 'ASC' else 'DESC'
                sql += f" ORDER BY i.`fecha_creacion` {orden_sql} LIMIT %s OFFSET %s"
                offset = (pagina - 1) * por_pagina
                params.extend([por_pagina, offset])

                cursor.execute(sql, tuple(params))
                return cursor.fetchall()
    except:
        raise

def obtenerIncidenciaxId(p_idIncidencia):
    try:
        conn = obtenerconexion()
        with conn:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                sql =  "SELECT i.`id`, i.`titulo`, i.`descripcion`, i.`ambiente`, i.`ip_equipo`,"
                sql += " i.`usuario_id`, i.`tecnico_id`, i.`tipo_incidencia_id`,"
                sql += " i.`prioridad`, i.`estado`, i.`diagnostico`, i.`solucion`, i.`fecha_creacion`, i.`fecha_cierre`,"
                sql += " u.`nombre` AS usuario_nombre, tec.`nombre` AS tecnico_nombre, ti.`nombre_problema`"
                sql += " FROM `Incidencia` i"
                sql += " JOIN `Usuario` u ON i.`usuario_id` = u.`id`"
                sql += " LEFT JOIN `Usuario` tec ON i.`tecnico_id` = tec.`id`"
                sql += " JOIN `TipoIncidencia` ti ON i.`tipo_incidencia_id` = ti.`id`"
                sql += " WHERE i.`id` = %s"
                cursor.execute(sql, (p_idIncidencia,))
                return cursor.fetchone()
    except:
        raise

def insertarIncidencia(objIncidencia):
    try:
        conn = obtenerconexion()
        if conn:
            with conn:
                with conn.cursor() as cursor:
                    sql =  "INSERT INTO `Incidencia` (`titulo`, `descripcion`, `ambiente`, `ip_equipo`,"
                    sql += " `usuario_id`, `tipo_incidencia_id`, `prioridad`)"
                    sql += " VALUES (%s, %s, %s, %s, %s, %s, %s)"
                    cursor.execute(sql, (objIncidencia.titulo, objIncidencia.descripcion,
                                         objIncidencia.ambiente, objIncidencia.ip_equipo,
                                         objIncidencia.usuario_id, objIncidencia.tipo_incidencia_id,
                                         objIncidencia.prioridad))
                    incidencia_id = cursor.lastrowid
                conn.commit()
            return True, incidencia_id
        return False, None
    except:
        raise

def asignarTecnico(p_idIncidencia, p_tecnicoId):
    try:
        conn = obtenerconexion()
        if conn:
            with conn:
                with conn.cursor() as cursor:
                    sql =  "UPDATE `Incidencia`"
                    sql += " SET `tecnico_id` = %s"
                    sql += " WHERE `id` = %s"
                    cursor.execute(sql, (p_tecnicoId, p_idIncidencia,))
                conn.commit()
            return True
        return False
    except:
        return False

def actualizarEstadoIncidencia(p_idIncidencia, p_estado, p_diagnostico, p_solucion):
    try:
        conn = obtenerconexion()
        if conn:
            with conn:
                with conn.cursor() as cursor:
                    cierre = "NOW()" if p_estado == 'RESUELTO' else "NULL"
                    sql =  "UPDATE `Incidencia`"
                    sql += " SET `estado` = %s ,"
                    sql += "     `diagnostico` = %s ,"
                    sql += "     `solucion` = %s ,"
                    sql += f"    `fecha_cierre` = {cierre}"
                    sql += " WHERE `id` = %s"
                    cursor.execute(sql, (p_estado, p_diagnostico, p_solucion, p_idIncidencia,))
                conn.commit()
            return True
        return False
    except:
        return False
def tecnicoConMenorCola():
    """Retorna el id del técnico (TECNICO o JEFE_TI) con menos incidencias activas."""
    try:
        conn = obtenerconexion()
        with conn:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = (
                    "SELECT u.`id`, COUNT(i.`id`) AS cola "
                    "FROM `Usuario` u "
                    "JOIN `Rol` r ON u.`rol_id` = r.`id` "
                    "LEFT JOIN `Incidencia` i "
                    "  ON i.`tecnico_id` = u.`id` "
                    "  AND i.`estado` NOT IN ('RESUELTO') "
                    "WHERE r.`nombre` IN ('TECNICO','JEFE_TI') AND u.`activo` = 1 "
                    "GROUP BY u.`id` "
                    "ORDER BY cola ASC, RAND() "
                    "LIMIT 1"
                )
                cursor.execute(sql)
                result = cursor.fetchone()
                return result['id'] if result else None
    except:
        raise