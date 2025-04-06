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
INSERT INTO cuentas (cuenta_id, nombre, tipo, naturaleza) VALUES
(10, 'Efectivo', 'Activo', 'Deudora'),
(11, 'Inversiones Financieras', 'Activo', 'Deudora'),
(12, 'Cuentas Por Cobrar Comerciales - Terceros', 'Activo', 'Deudora'),
(13, 'Cuentas Por Cobrar Comerciales - Relacionadas', 'Activo', 'Deudora'),
(14, 'Cuentas Por Cobrar Al Personal, Accionistas, Directores y Gerentes', 'Activo', 'Deudora'),
(16, 'Cuentas Por Cobrar Diversas - Terceros', 'Activo', 'Deudora'),
(17, 'Cuentas Por Cobrar Diversas - Relacionadas', 'Activo', 'Deudora'),
(18, 'Servicios Y Otros Contratados Por Anticipado', 'Activo', 'Deudora'),
(20, 'Mercaderías', 'Activo', 'Deudora'),
(21, 'Productos Terminados', 'Activo', 'Deudora'),
(22, 'Subproductos, Desechos Y Desperdicios', 'Activo', 'Deudora'),
(23, 'Productos En Proceso', 'Activo', 'Deudora'),
(24, 'Materias Primas', 'Activo', 'Deudora'),
(25, 'Materias Auxiliares, Suministros Y Repuestos', 'Activo', 'Deudora'),
(26, 'Envases Y Embalajes', 'Activo', 'Deudora'),
(27, 'Activos No Corrientes Mantenidos Para La Venta', 'Activo', 'Deudora'),
(28, 'Existencias Por Recibir', 'Activo', 'Deudora'),
(29, 'Desvalorización De Existencias', 'Activo', 'Acreedora'),
(30, 'Inversiones Mobiliarias', 'Activo', 'Deudora'),
(31, 'Inversiones Inmobiliarias', 'Activo', 'Deudora'),
(32, 'Activos Adquiridos En Arrendamiento Financiero', 'Activo', 'Deudora'),
(33, 'Inmuebles, Maquinaria Y Equipo', 'Activo', 'Deudora'),
(34, 'Intangibles', 'Activo', 'Deudora'),
(35, 'Activos Biológicos', 'Activo', 'Deudora'),
(36, 'Desvalorización De Activo Inmovilizado', 'Activo', 'Acreedora'),
(37, 'Activo Diferido', 'Activo', 'Deudora'),
(38, 'Otros Activos', 'Activo', 'Deudora'),
(39, 'Depreciación, Amortización Y Agotamiento Acumulado', 'Activo', 'Acreedora'),

-- Insertar cuentas del Pasivo
(40, 'Tributos Y Aportes Al Sistema De Pensiones Y De Salud Por Pagar', 'Pasivo', 'Acreedora'),
(41, 'Remuneraciones Y Participaciones Por Pagar', 'Pasivo', 'Acreedora'),
(42, 'Cuentas Por Pagar Comerciales – Terceros', 'Pasivo', 'Acreedora'),
(43, 'Cuentas Por Pagar Comerciales – Relacionadas', 'Pasivo', 'Acreedora'),
(44, 'Cuentas Por Pagar A Los Accionistas, Directores Y Gerentes', 'Pasivo', 'Acreedora'),
(45, 'Obligaciones Financieras', 'Pasivo', 'Acreedora'),
(46, 'Cuentas Por Pagar Diversas – Terceros', 'Pasivo', 'Acreedora'),
(47, 'Cuentas Por Pagar Diversas – Relacionadas', 'Pasivo', 'Acreedora'),
(48, 'Provisiones', 'Pasivo', 'Acreedora'),
(49, 'Pasivo Diferido', 'Pasivo', 'Acreedora'),

-- Insertar cuentas del Patrimonio
(50, 'Capital', 'Patrimonio', 'Acreedora'),
(51, 'Acciones De Inversión', 'Patrimonio', 'Acreedora'),
(52, 'Capital Adicional', 'Patrimonio', 'Acreedora'),
(56, 'Resultados No Realizados', 'Patrimonio', 'Acreedora'),
(57, 'Excedente De Revaluación', 'Patrimonio', 'Acreedora'),
(58, 'Reservas', 'Patrimonio', 'Acreedora'),

-- Insertar cuentas de Gastos
(60, 'Compras', 'Gastos', 'Deudora'),
(61, 'Variación De Existencias', 'Gastos', 'Deudora'),
(62, 'Gastos De Personal, Directores Y Gerentes', 'Gastos', 'Deudora'),
(63, 'Gastos De Servicios Prestados Por Terceros', 'Gastos', 'Deudora'),
(64, 'Gastos Por Tributos', 'Gastos', 'Deudora'),
(65, 'Otros Gastos De Gestión', 'Gastos', 'Deudora'),
(66, 'Pérdida Por Medición De Activos No Financieros Al Valor Razonable', 'Gastos', 'Deudora'),
(67, 'Gastos Financieros', 'Gastos', 'Deudora'),
(68, 'Valuación Y Deterioro De Activos Y Provisiones', 'Gastos', 'Deudora'),
(69, 'Costo De Ventas', 'Gastos', 'Deudora'),

-- Insertar cuentas de Ingresos
(70, 'Ventas', 'Ingresos', 'Acreedora'),
(71, 'Variación De La Producción Almacenada', 'Ingresos', 'Acreedora'),
(72, 'Producción De Activo Inmovilizado', 'Ingresos', 'Acreedora'),
(73, 'Descuentos, Rebajas Y Bonificaciones Obtenidos', 'Ingresos', 'Acreedora'),
(74, 'Descuentos, Rebajas Y Bonificaciones Concedidos', 'Gastos', 'Deudora'),
(75, 'Otros Ingresos De Gestión', 'Ingresos', 'Acreedora'),
(76, 'Ganancia Por Medición De Activos No Financieros', 'Ingresos', 'Acreedora'),
(77, 'Ingresos Financieros', 'Ingresos', 'Acreedora'),
(78, 'Cargas Cubiertas Por Provisiones', 'Ingresos', 'Acreedora'),
(79, 'Cargas Imputables A Cuentas De Costos Y Gastos Docente', 'Ingresos', 'Acreedora');
