CREATE DATABASE IF NOT EXISTS bd_konecta;
USE bd_konecta;

CREATE TABLE TipoComprobantePago (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(20) NOT NULL UNIQUE,
    estado VARCHAR(20) DEFAULT 'Activo'
);

INSERT INTO TipoComprobantePago (nombre) VALUES
('Factura'),
('Boleta');

CREATE TABLE ComprobantePago (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tipo_comprobante_id INT NOT NULL,

    numero VARCHAR(30) NOT NULL UNIQUE,
    fecha_emision DATE NOT NULL,

    cliente_nombre VARCHAR(100) NOT NULL,
    cliente_documento VARCHAR(15) NOT NULL,
    cliente_telefono VARCHAR(15),

    producto_servicio VARCHAR(100) NOT NULL,
    plan VARCHAR(100) NOT NULL,
    monto DECIMAL(10,2) NOT NULL,

    asesor_venta VARCHAR(100),
    observacion TEXT,

    estado VARCHAR(20) DEFAULT 'Activo',
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (tipo_comprobante_id)
    REFERENCES TipoComprobantePago(id)
);
-- ══════════════════════════════════════════════
--  ROL
-- ══════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS Rol (
  id     INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(50) NOT NULL UNIQUE
);
INSERT INTO Rol (nombre) VALUES ('COLABORADOR'),('TECNICO'),('JEFE_TI');

CREATE TABLE IF NOT EXISTS Usuario (
  id             INT AUTO_INCREMENT PRIMARY KEY,
  nombre         VARCHAR(100) NOT NULL,
  correo         VARCHAR(100) NOT NULL UNIQUE,
  usuario        VARCHAR(80)  NOT NULL UNIQUE,
  password       VARCHAR(255) NOT NULL,
  celular        VARCHAR(20)  DEFAULT NULL,
  rol_id         INT NOT NULL DEFAULT 1,
  primer_ingreso TINYINT(1)  NOT NULL DEFAULT 1,
  activo         TINYINT(1)  NOT NULL DEFAULT 1,
  descriptor_facial TEXT DEFAULT NULL;
  FOREIGN KEY (rol_id) REFERENCES Rol(id)
);

CREATE TABLE IF NOT EXISTS TipoIncidencia (
  id              INT AUTO_INCREMENT PRIMARY KEY,
  nombre_problema VARCHAR(100) NOT NULL UNIQUE,
  descripcion     TEXT
);
INSERT INTO TipoIncidencia (nombre_problema, descripcion) VALUES
('Lentitud',          'PC con bajo rendimiento o lentitud al operar'),
('No enciende',       'El equipo no arranca o no da señal de vida'),
('Se apaga solo',     'El equipo se reinicia o apaga sin intervención'),
('Teclado / mouse',   'Periférico no detectado o sin respuesta'),
('Monitor sin señal', 'Pantalla en negro o sin imagen'),
('Aplicativo no abre','Software de llamadas u otro aplicativo falla al iniciar'),
('Otro',              'Problema no clasificado en las opciones anteriores');

CREATE TABLE IF NOT EXISTS Incidencia (
  id                 INT AUTO_INCREMENT PRIMARY KEY,
  titulo             VARCHAR(150) NOT NULL,
  descripcion        TEXT NOT NULL,
  usuario_id         INT NOT NULL,
  tecnico_id         INT DEFAULT NULL,
  tipo_incidencia_id INT NOT NULL,
  prioridad          ENUM('Bajo','Medio','Alto') NOT NULL DEFAULT 'Bajo',
  estado             ENUM('PENDIENTE','EN_DIAGNOSTICO','PROGRAMADO','RESUELTO') NOT NULL DEFAULT 'PENDIENTE',
  diagnostico        TEXT,
  solucion           TEXT,
  fecha_creacion     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  fecha_cierre       TIMESTAMP NULL DEFAULT NULL,
  ambiente   VARCHAR(10)  DEFAULT NULL AFTER descripcion,
  ip_equipo  VARCHAR(20)  DEFAULT NULL AFTER ambiente,
  FOREIGN KEY (usuario_id)         REFERENCES Usuario(id),
  FOREIGN KEY (tecnico_id)         REFERENCES Usuario(id),
  FOREIGN KEY (tipo_incidencia_id) REFERENCES TipoIncidencia(id)
);

CREATE TABLE IF NOT EXISTS Area (
  id          INT AUTO_INCREMENT PRIMARY KEY,
  nombre      VARCHAR(100) NOT NULL UNIQUE,
  descripcion TEXT,
  responsable VARCHAR(100) DEFAULT NULL,
  activa      TINYINT(1)  NOT NULL DEFAULT 1,
  creado_en   TIMESTAMP   DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS PC (
  id             INT AUTO_INCREMENT PRIMARY KEY,
  hostname       VARCHAR(50)  NOT NULL UNIQUE,
  numero_serie   VARCHAR(80)  NOT NULL UNIQUE,
  marca_modelo   VARCHAR(100) NOT NULL DEFAULT '',
  area_id        INT DEFAULT NULL,
  estado         ENUM('operativa','en_reparacion','de_baja') NOT NULL DEFAULT 'operativa',
  tecnico_id     INT DEFAULT NULL,
  usuario_id     INT DEFAULT NULL,
  observaciones  TEXT,
  registrado_en  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  actualizado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (tecnico_id) REFERENCES Usuario(id) ON DELETE SET NULL,
  FOREIGN KEY (area_id)    REFERENCES Area(id)    ON DELETE SET NULL,
  FOREIGN KEY (usuario_id) REFERENCES Usuario(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS Componente (
  id            INT AUTO_INCREMENT PRIMARY KEY,
  nombre        VARCHAR(100) NOT NULL,
  tipo          VARCHAR(80)  NOT NULL,
  cantidad      INT NOT NULL DEFAULT 0,
  descripcion   TEXT,
  registrado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE Usuario
  ADD COLUMN area_id INT NULL,
  ADD CONSTRAINT fk_usuario_area FOREIGN KEY (area_id) REFERENCES Area(id) ON DELETE SET NULL;

INSERT INTO Usuario (nombre, correo, usuario, password, celular, rol_id, primer_ingreso) VALUES
('Erick Torres', 'erick.torres@konecta.pe', 'etorres', 'admin123',       '944111222', 3, 0),
('Juan Rios',    'juan.rios@konecta.pe',    'jrios',   'tecnico123',     '944333444', 2, 0),
('Carlos Ruiz',  'carlos.ruiz@konecta.pe',  'cruiz',   'colaborador123', '944555666', 1, 0);

INSERT INTO Area (nombre, descripcion) VALUES
('Sala 1',  'Sala de operaciones 1'),
('Sala 2',  'Sala de operaciones 2'),
('Sala 3',  'Sala de operaciones 3'),
('Almacen', 'Almacen de equipos'),
('TI',      'Area de Tecnologia de la Informacion');

INSERT INTO PC (hostname, numero_serie, marca_modelo, area_id, estado, tecnico_id) VALUES
('MV-PE-0001', 'SN-DELL-84712', 'Dell OptiPlex 3080', 1, 'operativa',     2),
('MV-PE-0002', 'SN-HP-33021',   'HP ProDesk 400 G7',  2, 'en_reparacion', 2),
('MV-PE-0003', 'SN-DELL-90144', 'Dell OptiPlex 7080', 3, 'operativa',     NULL),
('MV-PE-0004', 'SN-HP-77403',   'HP EliteDesk 800',   4, 'operativa',     NULL);

INSERT INTO Componente (nombre, tipo, cantidad, descripcion) VALUES
('Teclado USB Logitech', 'Periférico', 15, 'Teclados de repuesto'),
('Mouse óptico HP',      'Periférico', 12, 'Mouse de repuesto'),
('Memoria RAM 8GB DDR4', 'Hardware',    8, 'Módulos RAM para reemplazo'),
('Disco SSD 256GB',      'Hardware',    5, 'Discos para reemplazo'),
('Cable HDMI 1.5m',      'Cable',      10, 'Cables de video');