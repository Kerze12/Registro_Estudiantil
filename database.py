# Importa el módulo pymysql para la conexión con la base de datos MySQL
import pymysql

# Define la clase Data que proporciona métodos para interactuar con la base de datos
class Data:
    
    def __init__(self):
        # Establece la conexión con la base de datos MySQL
        self.conn = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            db='registro_estudiantes'
        )
        # Crea un objeto de cursor para ejecutar consultas
        self.cursor = self.conn.cursor()

    def close_connection(self):
        # Cierra la conexión a la base de datos
        self.conn.close()

    def InsertItems(self, element):
        # Inserta un nuevo elemento en la tabla 'listado' con los valores proporcionados
        sql = "insert into listado(Nombre, Materia, Nota, Jornada, Estado) values('{}', '{}', '{}', '{}', '{}')".format(element[0],element[1],element[2],element[3],element[4])
        # Ejecuta la consulta SQL
        self.cursor.execute(sql)
        # Guarda los cambios en la base de datos
        self.conn.commit()

    def ReturnOneItem(self, ref):
        # Consulta un elemento por nombre en la tabla 'listado'
        sql = "select * from listado where Nombre = '{}'".format(ref)
        self.cursor.execute(sql)
        # Retorna la información del elemento o 'None' si no se encuentra
        return self.cursor.fetchone()

    def ReturnForSubject(self, ref):
        # Consulta elementos por materia en la tabla 'listado'
        sql = "select * from listado where Materia = '{}'".format(ref)
        self.cursor.execute(sql)
        # Retorna una lista de filas que cumplen con el criterio
        return self.cursor.fetchall()

    def returnAllElements(self):
        # Consulta todos los elementos en la tabla 'listado'
        sql = "select * from listado"
        self.cursor.execute(sql)
        # Retorna una lista de todas las filas
        return self.cursor.fetchall()

    def Delete(self, ref):
        # Elimina un elemento por nombre en la tabla 'listado'
        sql = "delete from listado where Nombre = '{}'".format(ref)
        self.cursor.execute(sql)
        # Guarda los cambios en la base de datos
        self.conn.commit()

    def UpdateItem(self, element, ref):
        # Actualiza un elemento por nombre en la tabla 'listado' con nuevos valores
        sql = "update listado set Nombre = '{}', Materia = '{}', Nota = '{}', Jornada = '{}', Estado = '{}' where Nombre = '{}'".format(element[0],element[1],element[2],element[3],element[4], ref)
        # Ejecuta la consulta SQL
        self.cursor.execute(sql)
        # Guarda los cambios en la base de datos
        self.conn.commit()

# Ejemplo de uso
'''
# Crea un objeto Data para interactuar con la base de datos
d = Data()
# Obtiene todos los elementos de la tabla 'listado'
users = d.returnAllElements()
# Imprime cada elemento
for i in users:
    print(i)

# No olvides cerrar la conexión después de su uso
d.close_connection()
'''
