create database sistemas3
use sistemas3

create table categoria (
id_categoria int primary key,
nombre varchar(25),
descripcion varchar (30),
estado char (1),
)


create table producto(
id_producto int primary key,
codigo_producto varchar (20),
nombre varchar (20),
precio_venta decimal (5,2),
precio_compra decimal (5,2),
stock int,
descripcion varchar (25),
ruta_imagen varchar (500),
estado char (1),
id_categoria int,
constraint fk_categoria foreign key (id_categoria) references categoria (id_categoria),
)

create table proveedor (
id_proveedor int primary key,
id_producto int,
nombre varchar(25),
direccion varchar(25),
estado char(1),
email varchar(25),
constraint fk_producto foreign key (id_producto) references producto (id_producto),

)



create table rol_usuario (
id_rol int primary key,
nombre_rol varchar (20),
descripcion varchar (20),
estado char (1),
)

create table usuario (
id_usuario int primary key,
id_rol int,
nombre varchar(20),
estado char (1),
direccion varchar(25),
email varchar (25),
constraint fk_rol foreign key (id_rol) references rol_usuario (id_rol),
)



create table ingreso (
id_ingreso int primary key ,
id_proveedor int,
id_usuario int,
fecha datetime,
estado char(1),
constraint fk_proveedor foreign key (id_proveedor) references proveedor(id_proveedor),
constraint fk_usuario2 foreign key (id_usuario) references usuario (id_usuario),
)
create table detalle_ingreso(
id_detalleingreso int,
id_ingreso int,
tipo_comprobante varchar(20),
cantidad_ingresada int,
costo_total decimal (4,2),
estado char (1),
constraint fk_ingreso foreign key (id_ingreso) references ingreso (id_ingreso),
)

create table cliente (
id_cliente int primary key,
nombre varchar (40),
telefono int ,
direccion varchar (40),
estado char (1),
)


create table venta(
id_venta int primary key, 
fecha datetime,
id_usuario int,
id_producto int,
id_cliente int,
constraint fk_usuario20 foreign key (id_usuario) references usuario (id_usuario),
constraint fk_producto2 foreign key (id_producto) references producto (id_producto),
constraint fk_cliente2 foreign key (id_cliente) references cliente (id_cliente),
)

create table detalleventa(
id_detalleventa int primary key ,
tipo_comprobante int,
id_venta int,
cantidad_producto int,
precio_total decimal (4,2),
pago decimal (4,2),
vuelto decimal (4,2)
constraint fk_venta foreign key (id_venta) references venta (id_venta),
)

