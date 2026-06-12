-- ══════════════════════════════════════════════
--  INSERTS DE DATOS DE PRUEBA — Konecta
--  19 Colaboradores (rol_id=1) → id 4–22
--   9 Técnicos      (rol_id=2) → id 23–31
--  20 PCs nuevas               → hostname MV-PE-0005 … MV-PE-0024
--  50 Incidencias
-- ══════════════════════════════════════════════

-- ══════════════════════════════════════════════
--  19 COLABORADORES  (ids 4–22)
-- ══════════════════════════════════════════════
INSERT INTO Usuario (nombre, correo, usuario, password, celular, rol_id, primer_ingreso) VALUES
('Ana Flores',       'ana.flores@konecta.pe',       'aflores',   'colab123', '912001001', 1, 0),
('Luis Mendoza',     'luis.mendoza@konecta.pe',     'lmendoza',  'colab123', '912001002', 1, 0),
('María Castillo',   'maria.castillo@konecta.pe',   'mcastillo', 'colab123', '912001003', 1, 0),
('Pedro Vásquez',    'pedro.vasquez@konecta.pe',    'pvasquez',  'colab123', '912001004', 1, 0),
('Rosa Chávez',      'rosa.chavez@konecta.pe',      'rchavez',   'colab123', '912001005', 1, 0),
('Jorge Ramírez',    'jorge.ramirez@konecta.pe',    'jramirez',  'colab123', '912001006', 1, 0),
('Sofía Paredes',    'sofia.paredes@konecta.pe',    'sparedes',  'colab123', '912001007', 1, 0),
('Diego Herrera',    'diego.herrera@konecta.pe',    'dherrera',  'colab123', '912001008', 1, 0),
('Lucía Sánchez',    'lucia.sanchez@konecta.pe',    'lsanchez',  'colab123', '912001009', 1, 0),
('Miguel Quispe',    'miguel.quispe@konecta.pe',    'mquispe',   'colab123', '912001010', 1, 0),
('Valeria Cárdenas', 'valeria.cardenas@konecta.pe', 'vcardenas', 'colab123', '912001011', 1, 0),
('Andrés Palacios',  'andres.palacios@konecta.pe',  'apalacios', 'colab123', '912001012', 1, 0),
('Carmen Guerrero',  'carmen.guerrero@konecta.pe',  'cguerrero', 'colab123', '912001013', 1, 0),
('Raúl Tello',       'raul.tello@konecta.pe',       'rtello',    'colab123', '912001014', 1, 0),
('Natalia Vera',     'natalia.vera@konecta.pe',     'nvera',     'colab123', '912001015', 1, 0),
('Fernando Cano',    'fernando.cano@konecta.pe',    'fcano',     'colab123', '912001016', 1, 0),
('Patricia Lozano',  'patricia.lozano@konecta.pe',  'plozano',   'colab123', '912001017', 1, 0),
('Héctor Muro',      'hector.muro@konecta.pe',      'hmuro',     'colab123', '912001018', 1, 0),
('Gabriela Salas',   'gabriela.salas@konecta.pe',   'gsalas',    'colab123', '912001019', 1, 0);

-- ══════════════════════════════════════════════
--  9 TÉCNICOS  (ids 23–31)
-- ══════════════════════════════════════════════
INSERT INTO Usuario (nombre, correo, usuario, password, celular, rol_id, primer_ingreso) VALUES
('Marco Díaz',       'marco.diaz@konecta.pe',       'mdiaz',    'tec123', '933002001', 2, 0),
('Sandra Peña',      'sandra.pena@konecta.pe',       'spena',    'tec123', '933002002', 2, 0),
('Renzo Alvarado',   'renzo.alvarado@konecta.pe',   'ralvarado','tec123', '933002003', 2, 0),
('Claudia Ibáñez',   'claudia.ibanez@konecta.pe',   'cibanez',  'tec123', '933002004', 2, 0),
('Óscar Fuentes',    'oscar.fuentes@konecta.pe',    'ofuentes', 'tec123', '933002005', 2, 0),
('Milagros Rojas',   'milagros.rojas@konecta.pe',   'mrojas',   'tec123', '933002006', 2, 0),
('Sebastián Lara',   'sebastian.lara@konecta.pe',   'slara',    'tec123', '933002007', 2, 0),
('Daniela Montes',   'daniela.montes@konecta.pe',   'dmontes',  'tec123', '933002008', 2, 0),
('Cristian Aguirre', 'cristian.aguirre@konecta.pe', 'caguirre', 'tec123', '933002009', 2, 0);

-- ══════════════════════════════════════════════
--  20 PCs NUEVAS  (MV-PE-0005 … MV-PE-0024)
--  Áreas: 1=Sala1 2=Sala2 3=Sala3 4=Almacen 5=TI
--  Técnicos disponibles: 2,23–31
-- ══════════════════════════════════════════════
INSERT INTO PC (hostname, numero_serie, marca_modelo, area_id, estado, tecnico_id) VALUES
('MV-PE-0005', 'SN-DELL-11001', 'Dell OptiPlex 3080',   1, 'operativa',     23),
('MV-PE-0006', 'SN-HP-11002',   'HP ProDesk 400 G7',    1, 'operativa',     23),
('MV-PE-0007', 'SN-LEN-11003',  'Lenovo ThinkCentre M70',2,'operativa',     24),
('MV-PE-0008', 'SN-DELL-11004', 'Dell OptiPlex 5080',   2, 'operativa',     24),
('MV-PE-0009', 'SN-HP-11005',   'HP EliteDesk 800 G5',  2, 'en_reparacion', 25),
('MV-PE-0010', 'SN-DELL-11006', 'Dell Vostro 3681',     3, 'operativa',     25),
('MV-PE-0011', 'SN-LEN-11007',  'Lenovo IdeaCentre 310',3, 'operativa',     26),
('MV-PE-0012', 'SN-HP-11008',   'HP ProDesk 600 G5',    3, 'operativa',     26),
('MV-PE-0013', 'SN-DELL-11009', 'Dell OptiPlex 7080',   1, 'en_reparacion', 27),
('MV-PE-0014', 'SN-ACER-11010', 'Acer Veriton M4660',   1, 'operativa',     27),
('MV-PE-0015', 'SN-HP-11011',   'HP Compaq Elite 8300', 2, 'operativa',     28),
('MV-PE-0016', 'SN-DELL-11012', 'Dell OptiPlex 390',    2, 'de_baja',       28),
('MV-PE-0017', 'SN-LEN-11013',  'Lenovo ThinkCentre M90',3,'operativa',     29),
('MV-PE-0018', 'SN-HP-11014',   'HP ProDesk 405 G6',    3, 'operativa',     29),
('MV-PE-0019', 'SN-DELL-11015', 'Dell Precision 3440',  5, 'operativa',     30),
('MV-PE-0020', 'SN-HP-11016',   'HP EliteDesk 705 G4',  5, 'operativa',     30),
('MV-PE-0021', 'SN-LEN-11017',  'Lenovo V530S',          4, 'operativa',     31),
('MV-PE-0022', 'SN-DELL-11018', 'Dell OptiPlex 3060',   4, 'en_reparacion',  2),
('MV-PE-0023', 'SN-HP-11019',   'HP ProDesk 400 G4',    1, 'operativa',      2),
('MV-PE-0024', 'SN-ACER-11020', 'Acer Veriton X2640',   2, 'de_baja',       23);

-- ══════════════════════════════════════════════
--  50 INCIDENCIAS
--  usuario_id: colaboradores 3–22
--  tecnico_id: técnicos 2,23–31
--  tipo_incidencia_id: 1=Lentitud 2=No enciende 3=Se apaga solo
--                      4=Teclado/mouse 5=Monitor sin señal
--                      6=Aplicativo no abre 7=Otro
-- ══════════════════════════════════════════════
INSERT INTO Incidencia
(titulo, descripcion, usuario_id, tecnico_id, tipo_incidencia_id, prioridad, estado, diagnostico, solucion, fecha_creacion, fecha_cierre)
VALUES
-- RESUELTAS (25)
('PC muy lenta al iniciar',          'Tarda más de 20 minutos en cargar el escritorio.',                  4,  2,  1,'Alto',  'RESUELTO', 'Disco duro con sectores dañados y exceso de programas en inicio.', 'Se limpió el inicio de Windows y se desfragmentó el disco.',           '2026-01-08 08:00:00','2026-01-08 10:30:00'),
('No enciende el equipo',            'Presioné el botón y no pasa nada, sin luces.',                       5,  23, 2,'Alto',  'RESUELTO', 'Cable de poder suelto en la fuente.',                              'Se aseguró el cable interno de la fuente de poder.',                  '2026-01-10 09:00:00','2026-01-10 09:45:00'),
('Mouse no mueve el cursor',         'El mouse óptico no responde aunque está conectado.',                 6,  24, 4,'Bajo',  'RESUELTO', 'Puerto USB dañado.',                                               'Se cambió a otro puerto USB y se actualizó el driver.',               '2026-01-14 11:00:00','2026-01-14 11:20:00'),
('Monitor en negro',                 'La pantalla no muestra imagen aunque el PC enciende.',              7,  25, 5,'Alto',  'RESUELTO', 'Cable VGA oxidado.',                                               'Se reemplazó el cable VGA por uno nuevo.',                            '2026-01-18 08:30:00','2026-01-18 09:00:00'),
('CRM no abre',                      'El sistema de llamadas muestra error al iniciar sesión.',            8,  26, 6,'Alto',  'RESUELTO', 'Java desactualizado.',                                             'Se actualizó Java a la versión 17 LTS.',                              '2026-01-22 07:45:00','2026-01-22 08:10:00'),
('Teclado escribe solo',             'Aparecen caracteres solos sin presionar teclas.',                    9,  27, 4,'Medio', 'RESUELTO', 'Tecla atascada por líquido derramado.',                            'Se limpió el teclado y se reemplazó.',                                '2026-01-25 14:00:00','2026-01-25 14:30:00'),
('PC se apaga sola',                 'Se reinicia sin previo aviso cada hora.',                           10, 28, 3,'Alto',  'RESUELTO', 'Temperatura del procesador muy alta.',                             'Se limpió el disipador y se cambió la pasta térmica.',                '2026-02-03 08:00:00','2026-02-03 09:30:00'),
('Excel se cierra solo',             'Al abrir archivos grandes se cierra inesperadamente.',              11, 29, 6,'Medio', 'RESUELTO', 'Memoria RAM insuficiente para archivos planos.',                   'Se amplió la RAM de 4GB a 8GB.',                                      '2026-02-07 10:00:00','2026-02-07 11:45:00'),
('No conecta a red',                 'No hay acceso a internet ni a la intranet.',                        12, 30, 7,'Alto',  'RESUELTO', 'Driver de red corrupto.',                                          'Se reinstalaron los drivers de la tarjeta de red.',                   '2026-02-11 09:00:00','2026-02-11 09:50:00'),
('Pantalla con rayas',               'Líneas horizontales fijas en toda la pantalla.',                    13, 31, 5,'Medio', 'RESUELTO', 'Panel LCD dañado.',                                                'Se reemplazó el monitor por uno de repuesto.',                        '2026-02-15 11:30:00','2026-02-15 13:00:00'),
('Audio sin sonido',                 'Los auriculares no suenan durante las llamadas.',                   14,  2, 7,'Alto',  'RESUELTO', 'Dispositivo de audio deshabilitado en Windows.',                   'Se habilitó el dispositivo desde el panel de sonido.',                '2026-02-18 08:00:00','2026-02-18 08:15:00'),
('PC no reconoce USB',               'El token de seguridad no es detectado.',                           15, 23, 4,'Medio', 'RESUELTO', 'Puerto USB frontal dañado.',                                       'Se habilitó el USB trasero como alternativa.',                        '2026-02-22 10:00:00','2026-02-22 10:25:00'),
('Lentitud en navegador',            'Chrome tarda mucho en cargar cualquier página.',                   16, 24, 1,'Bajo',  'RESUELTO', 'Caché y cookies acumulados, extensiones en conflicto.',             'Se limpió el caché y se desactivaron extensiones innecesarias.',      '2026-03-02 09:30:00','2026-03-02 10:00:00'),
('Error al imprimir',                'La impresora no responde desde ningún equipo.',                    17, 25, 7,'Medio', 'RESUELTO', 'IP de impresora cambiada tras reinicio del router.',               'Se asignó IP estática en el servidor DHCP.',                          '2026-03-06 11:00:00','2026-03-06 12:00:00'),
('Windows en bucle de actualización','Lleva horas en 35% y reinicia constantemente.',                    18, 26, 1,'Alto',  'RESUELTO', 'Carpeta SoftwareDistribution corrupta.',                           'Se limpió la carpeta y se forzó la actualización manual.',            '2026-03-10 08:00:00','2026-03-10 10:00:00'),
('Escritorio no carga',              'Inicia sesión pero el escritorio queda en negro.',                 19, 27, 1,'Alto',  'RESUELTO', 'Perfil de usuario corrupto.',                                      'Se creó un nuevo perfil de usuario y se migraron los datos.',         '2026-03-14 09:00:00','2026-03-14 11:30:00'),
('Cursor se mueve solo',             'El puntero se desplaza sin que nadie toque el mouse.',             20, 28, 4,'Medio', 'RESUELTO', 'Mouse con sensor dañado por caída.',                               'Se reemplazó el mouse por uno nuevo del almacén.',                   '2026-03-18 14:00:00','2026-03-18 14:20:00'),
('No abre aplicativo de planillas',  'Pantalla gris sin texto al ejecutarlo.',                            4, 29, 6,'Medio', 'RESUELTO', 'Permisos de ejecución revocados en la última política de grupo.',  'Se restauraron los permisos vía GPO.',                                '2026-03-22 10:00:00','2026-03-22 11:00:00'),
('Equipo pitando al encender',       'Tres pitidos cortos y no da video.',                                5, 30, 2,'Alto',  'RESUELTO', 'Módulo de RAM con falso contacto.',                                'Se retiró y reinsertó la memoria, limpiando los contactos.',          '2026-03-26 08:00:00','2026-03-26 08:40:00'),
('Fecha y hora incorrecta',          'El reloj se atrasa cada vez que se reinicia.',                      6, 31, 7,'Bajo',  'RESUELTO', 'Batería CMOS agotada.',                                            'Se reemplazó la pila CR2032 de la placa madre.',                      '2026-03-30 09:00:00','2026-03-30 09:20:00'),
('Ventilador hace ruido',            'Zumbido fuerte desde dentro del case.',                             7,  2, 3,'Bajo',  'RESUELTO', 'Cooler del procesador con polvo acumulado.',                       'Se limpió el ventilador con aire comprimido.',                        '2026-04-03 11:00:00','2026-04-03 11:30:00'),
('No carga la intranet',             'Error de certificado al entrar al portal interno.',                 8, 23, 6,'Medio', 'RESUELTO', 'Hora del sistema desincronizada con el servidor NTP.',             'Se configuró la sincronización automática de hora.',                  '2026-04-07 09:00:00','2026-04-07 09:15:00'),
('Pantalla muy oscura',              'El brillo está al mínimo y no se puede subir.',                    9, 24, 5,'Bajo',  'RESUELTO', 'Driver de pantalla desactualizado.',                               'Se actualizó el driver de video desde el administrador de dispositivos.','2026-04-11 10:00:00','2026-04-11 10:30:00'),
('Archivos desaparecidos',           'El usuario no encuentra sus documentos en el escritorio.',         10, 25, 7,'Alto',  'RESUELTO', 'Archivos movidos a carpeta temporal por limpieza automática.',     'Se restauraron los archivos desde la papelera de reciclaje.',         '2026-04-15 14:00:00','2026-04-15 14:45:00'),
('PC huele a quemado',               'Olor a plástico quemado y se apagó sola.',                        11, 26, 3,'Alto',  'RESUELTO', 'Condensador quemado en la placa madre.',                           'Se reemplazó la placa madre por una en stock.',                       '2026-04-19 08:00:00','2026-04-19 10:00:00'),

-- EN DIAGNÓSTICO (13)
('Lentitud extrema en Chrome',       'El navegador tarda 5 minutos en abrir.',                          12, 27, 1,'Medio', 'EN_DIAGNOSTICO','Analizando procesos en segundo plano y uso de RAM.',              NULL,'2026-05-02 08:00:00',NULL),
('Monitor parpadea',                 'La pantalla titila constantemente.',                              13, 28, 5,'Medio', 'EN_DIAGNOSTICO','Revisando cable de video y configuración de frecuencia.',         NULL,'2026-05-04 09:00:00',NULL),
('Error de IP duplicada',            'Windows alerta de conflicto de dirección IP.',                   14, 29, 7,'Alto',  'EN_DIAGNOSTICO','Rastreando el dispositivo con la misma IP en la red.',            NULL,'2026-05-06 10:00:00',NULL),
('Teclado inalámbrico no conecta',   'No empareja con el receptor USB.',                               15, 30, 4,'Bajo',  'EN_DIAGNOSTICO','Verificando frecuencia del receptor y batería del teclado.',      NULL,'2026-05-07 11:00:00',NULL),
('PC no pasa del logo',              'Se congela en la pantalla de inicio de Dell.',                   16, 31, 2,'Alto',  'EN_DIAGNOSTICO','Revisando POST y estado del disco duro con diagnóstico.',         NULL,'2026-05-08 08:30:00',NULL),
('Aplicativo de RRHH falla',         'Error de conexión al servidor al iniciar.',                      17,  2, 6,'Alto',  'EN_DIAGNOSTICO','Verificando credenciales de red y disponibilidad del servidor.',  NULL,'2026-05-09 09:00:00',NULL),
('Sonido entrecortado',              'El audio se corta cada pocos segundos en llamadas.',              18, 23, 7,'Medio', 'EN_DIAGNOSTICO','Analizando driver de audio y configuración de latencia.',         NULL,'2026-05-10 10:30:00',NULL),
('Windows no activa',                'Muestra marca de agua de activación.',                           19, 24, 1,'Bajo',  'EN_DIAGNOSTICO','Verificando licencia KMS corporativa.',                           NULL,'2026-05-11 08:00:00',NULL),
('Impresora imprime borroso',        'Los documentos salen con texto difuso.',                          20, 25, 7,'Medio', 'EN_DIAGNOSTICO','Revisando nivel de tóner y cabezales de impresión.',              NULL,'2026-05-12 11:00:00',NULL),
('PC reinicia al usar Excel',        'Solo al abrir Excel con macros se reinicia.',                     4, 26, 3,'Alto',  'EN_DIAGNOSTICO','Analizando volcado de memoria y temperatura bajo carga.',         NULL,'2026-05-13 09:30:00',NULL),
('Disco duro hace ruido',            'Se escucha un clic repetitivo desde el case.',                    5, 27, 7,'Alto',  'EN_DIAGNOSTICO','Ejecutando diagnóstico S.M.A.R.T. del disco.',                   NULL,'2026-05-14 08:00:00',NULL),
('Red cae cada 10 minutos',          'Se desconecta del servidor de llamadas periódicamente.',          6, 28, 7,'Alto',  'EN_DIAGNOSTICO','Revisando tarjeta de red, switch y cable de conexión.',           NULL,'2026-05-15 10:00:00',NULL),
('Pantalla negra tras suspensión',   'Al volver de suspensión la pantalla queda apagada.',              7, 29, 5,'Medio', 'EN_DIAGNOSTICO','Analizando configuración de energía y driver de gráficos.',       NULL,'2026-05-16 09:00:00',NULL),

-- PROGRAMADAS (6)
('Mantenimiento preventivo Sala 1',  'Limpieza interna y cambio de pasta térmica de 6 equipos.',        8, 30, 1,'Bajo',  'PROGRAMADO', NULL, NULL, '2026-05-17 09:00:00', NULL),
('Migración a SSD Sala 2',           'Cambio de HDD a SSD en 4 equipos lentos.',                       9, 31, 1,'Medio', 'PROGRAMADO', NULL, NULL, '2026-05-18 10:00:00', NULL),
('Actualización de drivers red',     'Actualización masiva de drivers de red en Sala 3.',              10,  2, 7,'Bajo',  'PROGRAMADO', NULL, NULL, '2026-05-19 08:00:00', NULL),
('Cambio de teclados defectuosos',   'Reemplazo de 8 teclados en mal estado en Sala 1.',              11, 23, 4,'Bajo',  'PROGRAMADO', NULL, NULL, '2026-05-20 15:00:00', NULL),
('Instalación suite ofimática',      'Instalación de Microsoft 365 en equipos nuevos.',               12, 24, 6,'Medio', 'PROGRAMADO', NULL, NULL, '2026-05-21 09:00:00', NULL),
('Revisión de cableado estructurado','Inspección y reemplazo de cables de red dañados.',              13, 25, 7,'Bajo',  'PROGRAMADO', NULL, NULL, '2026-05-22 08:00:00', NULL),

-- PENDIENTES (6)
('Mouse doble clic solo',            'El clic izquierdo hace doble clic sin querer.',                  14, NULL, 4,'Bajo',  'PENDIENTE', NULL, NULL, '2026-05-24 09:00:00', NULL),
('No hay sonido en auriculares',     'Los headsets no suenan aunque están conectados.',                15, NULL, 7,'Medio', 'PENDIENTE', NULL, NULL, '2026-05-25 10:00:00', NULL),
('Lentitud al iniciar sesión',       'Tarda 15 minutos desde que ingresa la contraseña.',             16, NULL, 1,'Medio', 'PENDIENTE', NULL, NULL, '2026-05-26 08:30:00', NULL),
('PC se congela en llamadas',        'El equipo se cuelga durante las gestiones telefónicas.',        17, NULL, 3,'Alto',  'PENDIENTE', NULL, NULL, '2026-05-26 11:00:00', NULL),
('Error al acceder a carpetas red',  'No puede abrir las carpetas compartidas del servidor.',         18, NULL, 7,'Alto',  'PENDIENTE', NULL, NULL, '2026-05-27 09:00:00', NULL),
('Webcam no detectada',              'El sistema de videollamadas no encuentra la cámara.',            19, NULL, 7,'Medio', 'PENDIENTE', NULL, NULL, '2026-05-28 10:30:00', NULL);