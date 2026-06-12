import pymysql.cursors
from bd import obtenerconexion

class PC():
    def __init__(self, hostname, numero_serie, marca_modelo, area_id,
                 estado, tecnico_id, observaciones):
        self.hostname = hostname
        self.numero_serie = numero_serie
        self.marca_modelo = marca_modelo
        self.area_id = area_id
        self.estado = estado
        self.tecnico_id = tecnico_id
        self.observaciones = observaciones

class Componente():
    def __init__(self, nombre, tipo, cantidad, descripcion):
        self.nombre = nombre
        self.tipo = tipo
        self.cantidad = cantidad
        self.descripcion = descripcion

# ══════════════════════════════════════════════
#  MÓDULO: PC
# ══════════════════════════════════════════════

def obtenerPCs():
    try:
        conn = obtenerconexion()
        with conn:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                sql =  " SELECT p.`id`, p.`hostname`, p.`numero_serie`, p.`marca_modelo`, "
                sql += "        p.`area_id`, p.`estado`, p.`tecnico_id`, p.`observaciones`, "
                sql += "        u.`nombre` AS tecnico_nombre, a.`nombre` AS area_nombre "
                sql += " FROM `PC` p "
                sql += " LEFT JOIN `Usuario` u ON p.`tecnico_id` = u.`id` "
                sql += " LEFT JOIN `Area` a ON p.`area_id` = a.`id` "
                sql += " ORDER BY p.`id` DESC "
                
                cursor.execute(sql)
                resultado = cursor.fetchall()
                return resultado
    except:
        raise

def obtenerPC(pc_id):
    try:
        conn = obtenerconexion()
        with conn:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                sql =  " SELECT p.`id`, p.`hostname`, p.`numero_serie`, p.`marca_modelo`, "
                sql += "        p.`area_id`, p.`estado`, p.`tecnico_id`, p.`observaciones` "
                sql += " FROM `PC` p "
                sql += " WHERE p.`id` = %s "
                
                cursor.execute(sql, (pc_id,))
                resultado = cursor.fetchone()
                return resultado
    except:
        raise

def stockPCs():
    try:
        conn = obtenerconexion()
        with conn:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                sql =  " SELECT COUNT(*) AS `total`, "
                sql += " SUM(CASE WHEN `estado` = 'operativa' THEN 1 ELSE 0 END) AS `operativas`, "
                sql += " SUM(CASE WHEN `estado` = 'en_reparacion' THEN 1 ELSE 0 END) AS `en_reparacion`, "
                sql += " SUM(CASE WHEN `estado` = 'de_baja' THEN 1 ELSE 0 END) AS `de_baja` "
                sql += " FROM `PC` "
                
                cursor.execute(sql)
                resultado = cursor.fetchone()
                if resultado:
                    return {
                        'total': resultado['total'] or 0,
                        'operativas': int(resultado['operativas'] or 0),
                        'en_reparacion': int(resultado['en_reparacion'] or 0),
                        'de_baja': int(resultado['de_baja'] or 0)
                    }
        return {}
    except:
        return {}

def insertarPC(objPC):
    try:
        conn = obtenerconexion()
        if conn:
            with conn:
                with conn.cursor() as cursor:
                    sql =  " INSERT INTO `PC` (`hostname`, `numero_serie`, `marca_modelo`, "
                    sql += "                  `area_id`, `estado`, `tecnico_id`, `observaciones`) "
                    sql += " VALUES (%s, %s, %s, %s, %s, %s, %s) "
                    
                    cursor.execute(sql, (objPC.hostname, objPC.numero_serie, objPC.marca_modelo,
                                         objPC.area_id if objPC.area_id else None, 
                                         objPC.estado, 
                                         objPC.tecnico_id if objPC.tecnico_id else None, 
                                         objPC.observaciones))
                conn.commit()
            return True
        return False
    except:
        return False

def actualizarPC(pc_id, objPC):
    try:
        conn = obtenerconexion()
        if conn:
            with conn:
                with conn.cursor() as cursor:
                    sql =  " UPDATE `PC` "
                    sql += " SET `hostname` = %s, `numero_serie` = %s, `marca_modelo` = %s, "
                    sql += "     `area_id` = %s, `estado` = %s, `tecnico_id` = %s, `observaciones` = %s "
                    sql += " WHERE `id` = %s "
                    
                    cursor.execute(sql, (objPC.hostname, objPC.numero_serie, objPC.marca_modelo,
                                         objPC.area_id if objPC.area_id else None, 
                                         objPC.estado, 
                                         objPC.tecnico_id if objPC.tecnico_id else None, 
                                         objPC.observaciones, pc_id))
                conn.commit()
            return True
        return False
    except:
        return False

# ══════════════════════════════════════════════
#  MÓDULO: COMPONENTE
# ══════════════════════════════════════════════

def obtenerComponentes():
    try:
        conn = obtenerconexion()
        with conn:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = "SELECT `id`, `nombre`, `tipo`, `cantidad`, `descripcion` FROM `Componente` ORDER BY `nombre`"
                cursor.execute(sql)
                resultado = cursor.fetchall()
                return resultado
    except:
        raise

def obtenerComponente(comp_id):
    try:
        conn = obtenerconexion()
        with conn:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = "SELECT `id`, `nombre`, `tipo`, `cantidad`, `descripcion` FROM `Componente` WHERE `id` = %s"
                # CORREGIDO: Se añadió la tupla (comp_id,) requerida por el método execute
                cursor.execute(sql, (comp_id,))
                resultado = cursor.fetchone()
                return resultado
    except:
        raise

def insertarComponente(objComp):
    try:
        conn = obtenerconexion()
        if conn:
            with conn:
                with conn.cursor() as cursor:
                    sql = "INSERT INTO `Componente` (`nombre`, `tipo`, `cantidad`, `descripcion`) VALUES (%s, %s, %s, %s)"
                    cursor.execute(sql, (objComp.nombre, objComp.tipo, objComp.cantidad, objComp.descripcion))
                conn.commit()
            return True
        return False
    except:
        return False

def actualizarComponente(comp_id, objComp):
    try:
        conn = obtenerconexion()
        if conn:
            with conn:
                with conn.cursor() as cursor:
                    sql =  " UPDATE `Componente` "
                    sql += " SET `nombre` = %s, `tipo` = %s, `cantidad` = %s, `descripcion` = %s "
                    sql += " WHERE `id` = %s "
                    cursor.execute(sql, (objComp.nombre, objComp.tipo, objComp.cantidad, objComp.descripcion, comp_id))
                conn.commit()
            return True
        return False
    except:
        return False