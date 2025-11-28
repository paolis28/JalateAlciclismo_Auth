-- Crear base de datos
CREATE DATABASE IF NOT EXISTS ciclismo CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE ciclismo;

-- ==========================
-- TABLA: ROL
-- ==========================
CREATE TABLE rol (
    id_rol INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(45) NOT NULL
);

-- ==========================
-- TABLA: USUARIO
-- ==========================
CREATE TABLE usuario (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    id_rol INT NOT NULL,
    nombre VARCHAR(45) NOT NULL,
    apellido_paterno VARCHAR(45),
    apellido_materno VARCHAR(45),
    contrasena VARCHAR(85) NOT NULL,
    correo VARCHAR(45) UNIQUE NOT NULL,
    url_foto TEXT,
    FOREIGN KEY (id_rol) REFERENCES rol(id_rol)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- ==========================
-- TABLA: EVENTO
-- ==========================
CREATE TABLE evento (
    id_evento INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(45) NOT NULL,
    descripcion VARCHAR(255),
    cantidad_participantes_dis INT DEFAULT 0,
    origen_carrera VARCHAR(45),
    km DOUBLE,
    url_banner TEXT
);

-- ==========================
-- TABLA: RUTA
-- ==========================
CREATE TABLE ruta (
    id_ruta INT AUTO_INCREMENT PRIMARY KEY,
    id_evento INT NOT NULL,
    nombre VARCHAR(45) NOT NULL,
    descripcion VARCHAR(255),
    url_imagen TEXT,
    FOREIGN KEY (id_evento) REFERENCES evento(id_evento)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- ==========================
-- TABLA: USUARIO_EVENTO
-- (relación N:N entre usuarios y eventos)
-- ==========================
CREATE TABLE usuario_evento (
    id_usuario_evento INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    id_evento INT NOT NULL,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (id_evento) REFERENCES evento(id_evento)
        ON DELETE CASCADE ON UPDATE CASCADE,
    UNIQUE KEY (id_usuario, id_evento) -- para evitar duplicados
);
-- ==========================
-- INSERTS BASE
-- ==========================
INSERT INTO rol (nombre) VALUES
('Admin'),
('Ciclista');

INSERT INTO usuario (id_rol, nombre, apellido_paterno, correo, contrasena)
VALUES (1, 'Administrador', 'General', 'admin@ciclismo.com', 'admin123');

INSERT INTO evento (nombre, descripcion, cantidad_participantes_dis, origen_carrera, km)
VALUES ('Carrera de Montaña', 'Ruta en la sierra con paisajes naturales', 50, 'San Cristóbal', 25.5);

INSERT INTO ruta (id_evento, nombre, descripcion)
VALUES (1, 'Ruta de Montaña', 'Ruta de nivel medio con pendientes y curvas cerradas');


ALTER TABLE ruta
ADD COLUMN id_usuario INT NULL,
ADD COLUMN lat_inicio DOUBLE NULL,
ADD COLUMN lng_inicio DOUBLE NULL,
ADD COLUMN lat_fin DOUBLE NULL,
ADD COLUMN lng_fin DOUBLE NULL,
ADD COLUMN distancia DOUBLE NULL,
ADD FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
    ON DELETE SET NULL ON UPDATE CASCADE;
