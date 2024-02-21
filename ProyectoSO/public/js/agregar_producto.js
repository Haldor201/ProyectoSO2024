document.addEventListener('DOMContentLoaded', function () {
    // Obtener el botón y agregar un event listener
    var agregarButton = document.getElementById('agregar');
    agregarButton.addEventListener('click', agregarProducto);

    // Función para agregar un nuevo producto
    function agregarProducto() {
        // Obtener los valores de los campos de entrada
        var nombre = document.getElementById('nombreInput').value;
        var descripcion = document.getElementById('descripcionInput').value;
        var precio = document.getElementById('precioInput').value;
        var stock = document.getElementById('stockInput').value;
        var categoria = document.getElementById('categoriaInput').value;
        if(nombre==""||descripcion==""||precio==""||stock==""||categoria==""){
            alert("Rellene los campos")
        }
        // Construir un objeto con los datos
        var nuevoProducto = {
            nombre: nombre,
            descripcion: descripcion,
            precio: precio,
            stock: stock,
            categoria: categoria
        };

        // Realizar la solicitud POST al servidor
        fetch('http://127.0.0.1:8000/productos/new', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(nuevoProducto),
        })
        .then(response => response.json())
        .then(data => {
            alert("Producto Agregado")
            window.location='ProductoLista.html'
        })
        .catch(error => console.error('Error fetching data:', error));
    }
});