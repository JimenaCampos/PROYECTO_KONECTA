import pymysql.cursors
from bd import obtenerconexion

def reporteResumen():
    try:
        conn = obtenerconexion()
        if conn:
            with conn:
                with conn.cursor() as cursor:
                    sql =  " SELECT COUNT(*) AS `total`, "
                    sql += " SUM(CASE WHEN `estado` = 'RESUELTO' THEN 1 ELSE 0 END) AS `resueltos`, "
                    sql += " SUM(CASE WHEN `estado` = 'PENDIENTE' THEN 1 ELSE 0 END) AS `pendientes`, "
                    sql += " SUM(CASE WHEN `estado` IN ('EN_DIAGNOSTICO', 'PROGRAMADO') THEN 1 ELSE 0 END) AS `en_proceso` "
                    sql += " FROM `Incidencia` "
                    cursor.execute(sql)
                    resultado = cursor.fetchone()
                    if resultado:
                        # Acceso por clave (DictCursor heredado de bd.py)
                        if isinstance(resultado, dict):
                            return {
                                'total': resultado.get('total') or 0,
                                'resueltos': int(resultado.get('resueltos') or 0),
                                'pendientes': int(resultado.get('pendientes') or 0),
                                'en_proceso': int(resultado.get('en_proceso') or 0)
                            }
                        return {
                            'total': resultado[0] or 0,
                            'resueltos': int(resultado[1] or 0),
                            'pendientes': int(resultado[2] or 0),
                            'en_proceso': int(resultado[3] or 0)
                        }
        return {}
    except:
        return {}

def reportePorTipo():
    try:
        conn = obtenerconexion()
        if conn:
            with conn:
                with conn.cursor() as cursor:
                    sql =  " SELECT ti.`nombre_problema`, COUNT(i.`id`) AS `cantidad` "
                    sql += " FROM `Incidencia` i "
                    sql += " JOIN `TipoIncidencia` ti ON i.`tipo_incidencia_id` = ti.`id` "
                    sql += " GROUP BY ti.`id`, ti.`nombre_problema` "
                    sql += " ORDER BY `cantidad` DESC "
                    sql += " LIMIT 7 "
                    cursor.execute(sql)
                    resultado = cursor.fetchall()
                    
                    datos = []
                    for row in resultado:
                        if isinstance(row, dict):
                            datos.append({'nombre_problema': row.get('nombre_problema'), 'cantidad': row.get('cantidad')})
                        else:
                            datos.append({'nombre_problema': row[0], 'cantidad': row[1]})
                    return datos
        return []
    except:
        return []

def reportePorTecnico():
    try:
        conn = obtenerconexion()
        if conn:
            with conn:
                with conn.cursor() as cursor:
                    sql =  " SELECT u.`nombre`, COUNT(i.`id`) AS `total_asignados`, "
                    sql += " IFNULL(SUM(CASE WHEN i.`estado` = 'RESUELTO' THEN 1 ELSE 0 END), 0) AS `resueltos`, "
                    sql += " IFNULL(SUM(CASE WHEN i.`estado` != 'RESUELTO' AND i.`id` IS NOT NULL THEN 1 ELSE 0 END), 0) AS `pendientes` "
                    sql += " FROM `Usuario` u "
                    sql += " LEFT JOIN `Incidencia` i ON i.`tecnico_id` = u.`id` "
                    sql += " WHERE u.`rol_id` IN (2, 3) "
                    sql += " GROUP BY u.`id`, u.`nombre` "
                    sql += " ORDER BY `total_asignados` DESC "
                    cursor.execute(sql)
                    resultado = cursor.fetchall()
                    
                    datos = []
                    for row in resultado:
                        if isinstance(row, dict):
                            datos.append({'nombre': row.get('nombre'), 'total_asignados': int(row.get('total_asignados') or 0), 'resueltos': int(row.get('resueltos') or 0), 'pendientes': int(row.get('pendientes') or 0)})
                        else:
                            datos.append({'nombre': row[0], 'total_asignados': int(row[1] or 0), 'resueltos': int(row[2] or 0), 'pendientes': int(row[3] or 0)})
                    return datos
        return []
    except:
        return []

def calcularProyeccionMensual():
    try:
        conn = obtenerconexion()
        if conn:
            with conn:
                with conn.cursor() as cursor:
                    sql =  " SELECT DATE_FORMAT(`fecha_creacion`, '%Y-%m') AS `periodo`, "
                    sql += " COUNT(`id`) AS `reales` "
                    sql += " FROM `Incidencia` "
                    sql += " GROUP BY DATE_FORMAT(`fecha_creacion`, '%Y-%m') "
                    sql += " ORDER BY `periodo` ASC "
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    
                    if not result:
                        return []

                    datos_finales = []
                    sum_x = 0
                    sum_y = 0
                    sum_xy = 0
                    sum_x2 = 0
                    n = len(result)

                    for index, row in enumerate(result):
                        x = index + 1
                        y = int(row[1] if not isinstance(row, dict) else row.get('reales', 0))
                        
                        sum_x += x
                        sum_y += y
                        sum_xy += x * y
                        sum_x2 += x ** 2

                        periodo = row[0] if not isinstance(row, dict) else row.get('periodo')
                        datos_finales.append({
                            'periodo': periodo,
                            'reales': y,
                            'proyeccion': '-'
                        })

                    denominador = (n * sum_x2 - sum_x ** 2)
                    if n >= 2 and denominador != 0:
                        pendiente = (n * sum_xy - sum_x * sum_y) / denominador
                        interseccion = (sum_y - pendiente * sum_x) / n
                        
                        siguiente_periodo = n + 1
                        calculo_proyeccion = int(pendiente * siguiente_periodo + interseccion)
                        if calculo_proyeccion < 0: 
                            calculo_proyeccion = 0

                        datos_finales.append({
                            'periodo': 'Proyección Próximo Mes',
                            'reales': '-',
                            'proyeccion': calculo_proyeccion
                        })
                    
                    return datos_finales
        return []
    except:
        return []