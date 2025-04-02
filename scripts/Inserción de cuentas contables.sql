--- Eliminación de datos anteriores ---
DO $$ 
DECLARE
    row RECORD;
    seq RECORD;
BEGIN
    -- Truncar todas las tablas en el esquema 'public'
    FOR row IN
        SELECT tablename
        FROM pg_tables
        WHERE schemaname = 'public'
    LOOP
        EXECUTE 'TRUNCATE TABLE ' || quote_ident(row.tablename) || ' CASCADE';
    END LOOP;

    -- Reiniciar las secuencias asociadas
    FOR seq IN
        SELECT c.oid::regclass::text AS sequence_name
        FROM pg_class c
        JOIN pg_namespace n ON n.oid = c.relnamespace
        WHERE c.relkind = 'S' -- 'S' indica que es una secuencia
          AND n.nspname = 'public'
    LOOP
        EXECUTE 'ALTER SEQUENCE ' || quote_ident(seq.sequence_name) || ' RESTART WITH 1';
    END LOOP;
END $$;

-- Insertar cuentas del Activo
INSERT INTO cuentas (cuenta_id, nombre, tipo) VALUES
(10, 'Efectivo', 'Activo'),
(11, 'Inversiones Financieras', 'Activo'),
(12, 'Cuentas Por Cobrar Comerciales - Terceros', 'Activo'),
(13, 'Cuentas Por Cobrar Comerciales - Relacionadas', 'Activo'),
(14, 'Cuentas Por Cobrar Al Personal, A Los Accionistas (Socios), Directores Y Gerentes', 'Activo'),
(16, 'Cuentas Por Cobrar Diversas - Terceros', 'Activo'),
(17, 'Cuentas Por Cobrar Diversas - Relacionadas', 'Activo'),
(18, 'Servicios Y Otros Contratados Por Anticipado', 'Activo'),
(20, 'Mercaderías', 'Activo'),
(21, 'Productos Terminados', 'Activo'),
(22, 'Subproductos, Desechos Y Desperdicios', 'Activo'),
(23, 'Productos En Proceso', 'Activo'),
(24, 'Materias Primas', 'Activo'),
(25, 'Materias Auxiliares, Suministros Y Repuestos', 'Activo'),
(26, 'Envases Y Embalajes', 'Activo'),
(27, 'Activos No Corrientes Mantenidos Para La Venta', 'Activo'),
(28, 'Existencias Por Recibir', 'Activo'),
(29, 'Desvalorización De Existencias', 'Activo'),
(30, 'Inversiones Mobiliarias', 'Activo'),
(31, 'Inversiones Inmobiliarias', 'Activo'),
(32, 'Activos Adquiridos En Arrendamiento Financiero', 'Activo'),
(33, 'Inmuebles, Maquinaria Y Equipo', 'Activo'),
(34, 'Intangibles', 'Activo'),
(35, 'Activos Biológicos', 'Activo'),
(36, 'Desvalorización De Activo Inmovilizado', 'Activo'),
(37, 'Activo Diferido', 'Activo'),
(38, 'Otros Activos', 'Activo'),
(39, 'Depreciación, Amortización Y Agotamiento Acumulado', 'Activo');

-- Insertar cuentas del Pasivo
INSERT INTO cuentas (cuenta_id, nombre, tipo) VALUES
(40, 'Tributos Y Aportes Al Sistema De Pensiones Y De Salud Por Pagar', 'Pasivo'),
(41, 'Remuneraciones Y Participaciones Por Pagar', 'Pasivo'),
(42, 'Cuentas Por Pagar Comerciales – Terceros', 'Pasivo'),
(43, 'Cuentas Por Pagar Comerciales – Relacionadas', 'Pasivo'),
(44, 'Cuentas Por Pagar A Los Accionistas, Directores Y Gerentes', 'Pasivo'),
(45, 'Obligaciones Financieras', 'Pasivo'),
(46, 'Cuentas Por Pagar Diversas – Terceros', 'Pasivo'),
(47, 'Cuentas Por Pagar Diversas – Relacionadas', 'Pasivo'),
(48, 'Provisiones', 'Pasivo'),
(49, 'Pasivo Diferido', 'Pasivo');

-- Insertar cuentas del Patrimonio
INSERT INTO cuentas (cuenta_id, nombre, tipo) VALUES
(50, 'Capital', 'Patrimonio'),
(51, 'Acciones De Inversión', 'Patrimonio'),
(52, 'Capital Adicional', 'Patrimonio'),
(56, 'Resultados No Realizados', 'Patrimonio'),
(57, 'Excedente De Revaluación', 'Patrimonio'),
(58, 'Reservas', 'Patrimonio');

-- Insertar cuentas de Gastos
INSERT INTO cuentas (cuenta_id, nombre, tipo) VALUES
(60, 'Compras', 'Gastos'),
(61, 'Variación De Existencias', 'Gastos'),
(62, 'Gastos De Personal, Directores Y Gerentes', 'Gastos'),
(63, 'Gastos De Servicios Prestados Por Terceros', 'Gastos'),
(64, 'Gastos Por Tributos', 'Gastos'),
(65, 'Otros Gastos De Gestión', 'Gastos'),
(66, 'Pérdida Por Medición De Activos No Financieros Al Valor Razonable', 'Gastos'),
(67, 'Gastos Financieros', 'Gastos'),
(68, 'Valuación Y Deterioro De Activos Y Provisiones', 'Gastos'),
(69, 'Costo De Ventas', 'Gastos');

-- Insertar cuentas de Ingresos
INSERT INTO cuentas (cuenta_id, nombre, tipo) VALUES
(70, 'Ventas', 'Ingresos'),
(71, 'Variación De La Producción Almacenada', 'Ingresos'),
(72, 'Producción De Activo Inmovilizado', 'Ingresos'),
(73, 'Descuentos, Rebajas Y Bonificaciones Obtenidos', 'Ingresos'),
(74, 'Descuentos, Rebajas Y Bonificaciones Concedidos', 'Ingresos'),
(75, 'Otros Ingresos De Gestión', 'Ingresos'),
(76, 'Ganancia Por Medición De Activos No Financieros Al Valor Razonable', 'Ingresos'),
(77, 'Ingresos Financieros', 'Ingresos'),
(78, 'Cargas Cubiertas Por Provisiones', 'Ingresos'),
(79, 'Cargas Imputables A Cuentas De Costos Y Gastos Docente', 'Ingresos');
