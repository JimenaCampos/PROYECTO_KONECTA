import pymysql.cursors
from bd import obtenerconexion


def obtener_tipos_comprobante():
    try:
        conn = obtenerconexion()
        with conn:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = (
                    "SELECT `id`, `nombre` "
                    "FROM `TipoComprobantePago` "
                    "WHERE `estado` = 'Activo' "
                    "ORDER BY `nombre` ASC"
                )
                cursor.execute(sql)
                return cursor.fetchall()
    except:
        return []


def obtener_comprobantes():
    try:
        conn = obtenerconexion()
        with conn:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = (
                    "SELECT cp.`id`, tcp.`nombre` AS tipo_comprobante, "
                    "       cp.`fecha_emision`, cp.`cliente_nombre`, "
                    "       cp.`cliente_documento`, cp.`cliente_telefono`, "
                    "       cp.`producto_servicio`, cp.`plan`, cp.`monto`, "
                    "       cp.`asesor_venta`, cp.`observacion`, cp.`estado` "
                    "FROM `ComprobantePago` cp "
                    "INNER JOIN `TipoComprobantePago` tcp ON cp.`tipo_comprobante_id` = tcp.`id` "
                    "ORDER BY cp.`id` DESC"
                )
                cursor.execute(sql)
                return cursor.fetchall()
    except:
        return []


def registrar_comprobante(tipo_comprobante_id, fecha_emision, cliente_nombre,
                          cliente_documento, cliente_telefono, producto_servicio,
                          plan, monto, asesor_venta, observacion):
    try:
        conn = obtenerconexion()
        if conn:
            with conn:
                with conn.cursor() as cursor:
                    sql = (
                        "INSERT INTO `ComprobantePago` "
                        "(`tipo_comprobante_id`, `fecha_emision`, `cliente_nombre`, "
                        " `cliente_documento`, `cliente_telefono`, `producto_servicio`, "
                        " `plan`, `monto`, `asesor_venta`, `observacion`) "
                        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    )
                    cursor.execute(sql, (
                        tipo_comprobante_id, fecha_emision, cliente_nombre,
                        cliente_documento, cliente_telefono, producto_servicio,
                        plan, monto, asesor_venta, observacion
                    ))
                conn.commit()
            return True, "Comprobante registrado correctamente"
        return False, "Error de conexión"
    except:
        return False, "No se pudo registrar el comprobante"
