from bd import obtenerconexion

def obtener_tipos_comprobante():
    conexion = obtenerconexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute(
                """SELECT id, nombre
                FROM TipoComprobantePago
                WHERE estado = 'Activo'
                ORDER BY nombre ASC"""
            )
            return cursor.fetchall()
    except Exception:
        print("Error al obtener tipos de comprobante:")
        return []
    finally:
        conexion.close()

def obtener_comprobantes():
    conexion = obtenerconexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute(
                """SELECT
                cp.id, tcp.nombre AS tipo_comprobante,
                cp.numero,
                cp.fecha_emision, cp.cliente_nombre,
                cp.cliente_documento, cp.cliente_telefono,
                cp.producto_servicio,
                cp.plan, cp.monto, cp.asesor_venta,
                cp.observacion, cp.estado
                FROM ComprobantePago cp
                INNER JOIN TipoComprobantePago tcp
                ON cp.tipo_comprobante_id = tcp.id
                ORDER BY cp.creado_en DESC
                """
            )
            return cursor.fetchall()
    except Exception as error:
        print("Error al obtener comprobantes: ", error)
        return[]
    finally:
        conexion.close()

def registrar_comprobante(
        tipo_comprobante_id, numero,
        fecha_emision, cliente_nombre,
        cliente_documento, cliente_telefono,
        producto_servicio, plan, monto,
        asesor_venta, observacion
):
    conexion = obtenerconexion()

    try:
        with conexion.cursor() as cursor:
            cursor.execute("""
            INSERT INTO ComprobantePago (tipo_comprobante_id, numero,
            fecha_emision, cliente_nombre,
            cliente_documento, cliente_telefono,
            producto_servicio, plan, monto,
            asesor_venta, observacion)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """ ,(
            tipo_comprobante_id, numero,
            fecha_emision, cliente_nombre,
            cliente_documento, cliente_telefono,
            producto_servicio, plan, monto,
            asesor_venta, observacion    
            ))
            conexion.commit()
            return True,"Comprobante Registrado"
    except Exception as error:
        print("Error al registrar")
        return False, "No se pudo Registrar"
    finally:
        conexion.close()

def modificar_comprobante(id, tipo_Comprobante_id,
                          numero, fecha_emision, cliente_nombre,
                          cliente_documento, cliente_telefono,
                          producto_servicio, plan, monto, asesor_venta,
                          observacion):
    conexion=obtenerconexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("""
            UPDATE ComprobantePago SET
            tipo_Comprobante_id= %s,
            numero = %s, 
            fecha_emision = %s, 
            cliente_nombre = %s,
            cliente_documento = %s, 
            cliente_telefono = %s,
            producto_servicio = %s,
            plan = %s,
            monto = %s,
            asesor_venta = %s,
            observacion = %s      
            WHERE id = %s
            """, (
                tipo_Comprobante_id,
                numero, fecha_emision, cliente_nombre,
                cliente_documento, cliente_telefono,
                producto_servicio, plan, monto, asesor_venta,
                observacion,id
            ))

            conexion.commit()
            return True, "Comprobante Modificado"
        
    except Exception as error:
        print("Error al modificar ", error)
        return False, "No se pudo modificar"
    finally:
        conexion.close()

