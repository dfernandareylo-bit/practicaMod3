import os
import psycopg2
import getpass

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "credenciales")
DB_USER = os.getenv("DB_USER", "Admin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "p4ssw0rdDB")

def conectar_db():
    try:
        return psycopg2.connect(
            host=DB_HOST, port=DB_PORT,
            database=DB_NAME, user=DB_USER, password=DB_PASSWORD
            )
    except Exception as e:
        print("Error de conexión:", e)
        return None
                
def obtener_datos_usuario(username, password):
    conn = conectar_db()
    if not conn:
        return
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                           SELECT u.id_usuario, u.nombre, u.correo, u.telefono, u.fecha_nacimiento
                           FROM credenciales c
                           JOIN usuarios u ON c.id_usuario = u.id_usuario
                           WHERE c.username = %s AND c.password_hash = %s;
                           """, (username, password))
            usuario = cursor.fetchone()
            
            if usuario:
                print("\nDatos del usuario encontrado:")
                print(f"ID: {usuario[0]}")
                print(f"Nombre: {usuario[1]}")
                print(f"Correo: {usuario[2]}")
                print(f"Teléfono: {usuario[3]}")
                print(f"Fecha de Nacimiento: {usuario[4]}")
            else:
                print("\nUsuario o contraseña incorrectos.")
    except Exception as e:
        print("Error al consultar la base de datos:", e)
    finally:
        conn.close()

def registrar_nuevo_usuario():
    conn = conectar_db()
    if not conn:
        return
    
    try:
        nombre = input("Nombre completo: ")
        correo = input("Correo electrónico: ")
        telefono = input("Teléfono: ")
        fecha_nacimiento = input("Fecha de nacimiento (YYYY-MM-DD): ")
        username = input("Nombre de usuario: ")
        password = getpass.getpass("Contraseña: ")

        with conn.cursor() as cursor:
            # Insertar usuarios
            cursor.execute("""
                INSERT INTO usuarios (nombre, correo, telefono, fecha_nacimiento)
                VALUES (%s, %s, %s, %s)
                RETURNING id_usuario;
            """, (nombre, correo, telefono, fecha_nacimiento))
            
            id_usuario = cursor.fetchone()[0]

            # Insertar redenciales
            cursor.execute("""
                INSERT INTO credenciales (id_usuario, username, password_hash)
                VALUES (%s, %s, %s);
            """, (id_usuario, username, password))
            
            conn.commit()
            print("Usuario registrado correctamente.")
    except Exception as e:
        conn.rollback()
        print("Error al registrar el usuario:", e)
    finally:
        conn.close()
                                                
if __name__ == "__main__":
    print("Menú (Capture una opción)")
    print("\n")
    print("1. Iniciar sesión")
    print("2. Registrar nuevo usuario")
    opcion = input("Seleccione una opción (1/2): ")
    
    if opcion == "1":
        user = input("Ingrese su usuario: ")
        pwd = getpass.getpass("Ingrese su contraseña: ")
        obtener_datos_usuario(user, pwd)
    elif opcion == "2":
        registrar_nuevo_usuario()
    else:
        print("Opción no válida.")