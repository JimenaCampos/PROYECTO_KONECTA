import pymysql.cursors

# ── Conexión — igual al docente ────────────────────────────────
def obtenerconexion():
    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            database='bd_konecta',
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except:
        return None



