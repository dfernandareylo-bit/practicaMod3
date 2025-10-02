-- Crear tabla de usuarios
CREATE TABLE IF NOT EXISTS usuarios (
id_usuario SERIAL PRIMARY KEY,
nombre VARCHAR(100) NOT NULL,
correo VARCHAR(255) UNIQUE,
telefono VARCHAR(20),
fecha_nacimiento DATE
);
--Crear tabla de puestos de trabajo
CREATE TABLE IF NOT EXISTS puestos (
id_puesto SERIAL PRIMARY KEY,
descripcion VARCHAR(100) NOT NULL
);
-- Crear tabla de credenciales
CREATE TABLE IF NOT EXISTS credenciales (
id_credencial SERIAL PRIMARY KEY,
id_usuario INT NOT NULL,
id_puesto INT NOT NULL,
username VARCHAR(50) UNIQUE NOT NULL,
password_hash VARCHAR(255) NOT NULL,
CONSTRAINT fk_usuario
FOREIGN KEY (id_usuario)
REFERENCES usuarios(id_usuario)
ON DELETE CASCADE,se
CONSTRAINT fk_puesto
FOREIGN KEY (id_puesto)
REFERENCES puestos(id_puesto)
ON DELETE CASCADE
);

