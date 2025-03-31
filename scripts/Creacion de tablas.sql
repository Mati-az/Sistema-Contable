DROP TABLE IF EXISTS cuentas CASCADE;
CREATE TABLE cuentas (
	cuenta_id CHAR(2) PRIMARY KEY,
	nombre VARCHAR(100) NOT NULL,
	tipo VARCHAR(20) CHECK (tipo IN ('Activo', 'Pasivo', 'Patrimonio', 'Ingresos', 'Gastos')) NOT NULL,
	saldo DECIMAL (15,2) DEFAULT 0.00
);

DROP TABLE IF EXISTS transacciones CASCADE;
CREATE TABLE transacciones (
	transaccion_id SERIAL PRIMARY KEY,
	fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	descripcion TEXT
);

DROP TABLE IF EXISTS detalles_transacciones CASCADE;
CREATE TABLE detalles_transacciones (
	detalle_id SERIAL PRIMARY KEY,
	transaccion_id INT NOT NULL,
	cuenta_id CHAR(2) NOT NULL,
	tipo_asiento VARCHAR(20) CHECK (tipo_asiento IN ('Debe', 'Haber')) NOT NULL,
	monto DECIMAL(15,2) NOT NULL,
	FOREIGN KEY (transaccion_id) REFERENCES transacciones (transaccion_id) ON DELETE CASCADE,
	FOREIGN KEY (cuenta_id) REFERENCES cuentas (cuenta_id) ON DELETE CASCADE
);