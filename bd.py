import pymysql.cursors

def obtenerconexion():
    try:
        connection = pymysql.connect(
            host='JimenaCampos.mysql.pythonanywhere-services.com',
            user='JimenaCampos',
            password='Aitana27*',  
            database='JimenaCampos$bd_konecta',
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except Exception as e:
        # Esto va a obligar a Python a escupir el error matemático/servidor exacto
        raise Exception(f"Error de conexión detallado: {e}")