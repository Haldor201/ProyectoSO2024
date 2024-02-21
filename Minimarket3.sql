CREATE DATABASE sistemas2;
USE sistemas2;


CREATE TABLE categoria (
    id_categoria INT PRIMARY KEY,
    nombre VARCHAR(25),
    descripcion VARCHAR(30),
    estado CHAR(1)
);

INSERT INTO categoria VALUES 
(1, 'Electrónicos', 'Categoría de electrónicos', 'A'),
(2, 'Ropa', 'Categoría de ropa', 'A');

-- Crea la tabla producto con la columna stock calculada
CREATE FUNCTION dbo.CalcularStock(@id_producto INT)
RETURNS INT
AS
BEGIN
    DECLARE @stock INT;

    SELECT @stock = ISNULL(SUM(cantidad_producto1), 0) -
                   ISNULL((SELECT SUM(cantidad_producto2) FROM detalleventa WHERE id_producto = @id_producto), 0)
    FROM proveedor
    WHERE id_producto = @id_producto;

    RETURN @stock;
END;

CREATE TABLE producto (
    id_producto INT PRIMARY KEY,
    codigo_producto VARCHAR(20),
    nombre VARCHAR(20),
    precio_venta DECIMAL(6,2),
    stock AS dbo.CalcularStock(id_producto),
    descripcion VARCHAR(25),
    ruta_imagen VARCHAR(255),
    estado CHAR(1),
    id_categoria INT,
    CONSTRAINT fk_categoria FOREIGN KEY (id_categoria) REFERENCES categoria (id_categoria)
);


INSERT INTO producto VALUES 
(1, 'P001', 'Laptop', 1200.00,  'laptop hp', '/images/laptop.jpg', 'A', 1),
(2, 'P002', 'Camisa', 25.00,'Camisita', '/images/camisa.jpg', 'A', 2);

CREATE TABLE proveedor (
    id_proveedor INT PRIMARY KEY,
    id_producto INT,
    cantidad_producto1 INT,
    nombre VARCHAR(25),
    direccion VARCHAR(25),
    estado CHAR(1),
    precio_compra DECIMAL(6,2),
	email VARCHAR(50),
    CONSTRAINT fk_producto FOREIGN KEY (id_producto) REFERENCES producto (id_producto)
);

INSERT INTO proveedor VALUES 
(1, 1, 100, 'Proveedor1', 'Dirección1', 'A', 50.00, 'proveedor1@email.com'),
(2, 2, 150, 'Proveedor2', 'Dirección2', 'A', 30.00, 'proveedor2@email.com');

CREATE TABLE rol_usuario (
    id_rol INT PRIMARY KEY,
    nombre_rol VARCHAR(20),
    descripcion VARCHAR(20),
    estado CHAR(1)
);


INSERT INTO rol_usuario VALUES 
(1, 'Admin', 'Admin sistema', 'A'),
(2, 'Vendedor', 'Vendedor productos', 'A');


CREATE TABLE usuario (
    id_usuario INT PRIMARY KEY,
    id_rol INT,
    contraseña VARCHAR(20),
    nombre VARCHAR(20),
    estado CHAR(1),
    direccion VARCHAR(25),
    email VARCHAR(50), -- adjusted size
    CONSTRAINT fk_rol FOREIGN KEY (id_rol) REFERENCES rol_usuario (id_rol)
);


INSERT INTO usuario VALUES 
(1, 1, 'admin123', 'Administra', 'A', 'Calle Admin', 'admin@gmail.com'),
(2, 2, 'vendedor123', 'Vender', 'A', 'Calle Vendedor', 'vendedor@gmail.com');


CREATE TABLE ingreso (
    id_ingreso INT PRIMARY KEY,
    id_proveedor INT,
    id_usuario INT,
    estado CHAR(1),
    CONSTRAINT fk_proveedor FOREIGN KEY (id_proveedor) REFERENCES proveedor(id_proveedor),
    CONSTRAINT fk_usuario2 FOREIGN KEY (id_usuario) REFERENCES usuario (id_usuario)
);


INSERT INTO ingreso (id_ingreso,id_proveedor,id_usuario,estado) VALUES 
(1, 1, 1,  'A'),
(2, 2, 2,  'A');


CREATE TABLE detalle_ingreso (
    id_detalleingreso INT,
    id_ingreso INT,
    fecha DATETIME DEFAULT GETDATE(),
	tipo_comprobante VARCHAR(20),
    cantidad_ingresada INT,
    costo_total DECIMAL(8,2),
    estado CHAR(1),
    CONSTRAINT fk_ingreso FOREIGN KEY (id_ingreso) REFERENCES ingreso (id_ingreso)
);


INSERT INTO detalle_ingreso(id_detalleingreso,id_ingreso,tipo_comprobante,cantidad_ingresada,costo_total,estado) VALUES 
(1, 1, 'Factura', 10, 8000.00, 'A'),
(2, 2, 'Boleta', 20, 300.00, 'A');


CREATE TABLE cliente (
    id_cliente INT PRIMARY KEY,
    nombre VARCHAR(40),
    telefono INT ,
    direccion VARCHAR(40),
    estado CHAR(1)
);


INSERT INTO cliente VALUES 
(1, 'Cliente 1', 123456789, 'Calle Cliente 1', 'A'),
(2, 'Cliente 2', 987654321, 'Calle Cliente 2', 'A');


-- Create venta table
CREATE TABLE venta (
    id_venta INT PRIMARY KEY,
    id_producto INT,
    id_cliente INT,
	CONSTRAINT fk_producto3 FOREIGN KEY (id_producto) REFERENCES producto (id_producto),
    CONSTRAINT fk_cliente3 FOREIGN KEY (id_cliente) REFERENCES cliente (id_cliente),

);


INSERT INTO venta VALUES 
(1, 1, 1 ),
(2, 2, 2);



CREATE FUNCTION dbo.CalcularPrecioTotal(@id_producto INT, @cantidad_producto1 INT)
RETURNS DECIMAL(9,2)
AS
BEGIN
    DECLARE @precio_venta DECIMAL(9,2);

    SELECT @precio_venta = precio_venta
    FROM producto
    WHERE id_producto = @id_producto;

    RETURN @precio_venta * @cantidad_producto1;
END;




CREATE TABLE detalleventa (
    id_detalleventa INT PRIMARY KEY,
    tipo_comprobante VARCHAR(20),
    id_venta INT,
    fecha DATETIME DEFAULT GETDATE(),
    cantidad_producto2 INT,
    id_producto INT,
	id_usuario int,
    precio_total AS dbo.CalcularPrecioTotal(id_producto, cantidad_producto2),
    pago DECIMAL(6,2),
    vuelto AS (pago - dbo.CalcularPrecioTotal(id_producto, cantidad_producto2)),
    CONSTRAINT fk_venta4 FOREIGN KEY (id_venta) REFERENCES venta (id_venta),
    CONSTRAINT fk_producto4 FOREIGN KEY (id_producto) REFERENCES producto (id_producto),
	CONSTRAINT fk_usuario4 FOREIGN KEY (id_usuario) REFERENCES usuario (id_usuario),
);


-- Insert sample data for detalleventa table
INSERT INTO detalleventa (id_detalleventa,tipo_comprobante,id_venta,cantidad_producto2,id_producto,id_usuario,pago) VALUES 
(1, 'Factura', 1, 5, 1, 1,8000.00),
(2, 'Boleta', 2, 3, 2, 2,5000.00);

select*from producto;	  
select*from usuario;	  
select *from detalleventa;
select *from rol_usuario;

select email,estado,nombre,direccion from usuario where email=="admin@gmail.com"