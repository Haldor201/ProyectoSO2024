function fetchProductos() {
    fetch('http://127.0.0.1:8000/productos/all')
        .then(response => response.json())
        .then(data => {
            const tableBody = document.getElementById('productTableBody');
            tableBody.innerHTML = ''; // Limpiar el cuerpo de la tabla antes de agregar nuevos elementos

            data.forEach(producto => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${producto.id}</td>
                    <td>${producto.nombre}</td>
                    <td>$${producto.precio}</td>
                    <td>${producto.stock}</td>
                    <td>${producto.categoria}</td>
                    <td>${producto.descripcion}</td>
                    <td>
                        <img src="./img/x.png" onclick="borrarProducto('${producto.id}')"/>
                        <img src="./img/edit.png" onclick="mostrarPopup('${producto.id}')""/>
                    </td>
                `;
                tableBody.appendChild(row);
            });
        })
        .catch(error => console.error('Error fetching data:', error));
}
function borrarProducto(codigo) {
    fetch(`http://127.0.0.1:8000/productos/delete?product_id=${codigo}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(() => {
        alert("Producto Eliminado");
        fetchProductos();
    })
    .catch(error => console.error('Error fetching data:', error));
}

function mostrarPopup(codigo) {
    var popup = document.getElementById('popupContainer');
    popup.style.display = 'grid';
    popup.style.justifyContent = 'center';
    fetch(`http://127.0.0.1:8000/productos/${codigo}`)
    .then(response => response.json())
    .then(data => {
        document.getElementById('nombreInput').value = data.nombre || '';
        document.getElementById('descripcionInput').value = data.descripcion || '';
        document.getElementById('precioInput').value = data.precio || '';
        document.getElementById('stockInput').value = data.stock || '';  // Asegúrate de que 'data.stock' no sea undefined o null
        document.getElementById('categoriaInput').value = data.categoria || '';
    })
    .catch(error => console.error('Error fetching data:', error));
    var guardar=document.getElementById('guardar');

    guardar.addEventListener('click',()=>{
        // Obtener los valores de los campos de entrada
        var nombre = document.getElementById('nombreInput').value;
        var descripcion = document.getElementById('descripcionInput').value;
        var precio = document.getElementById('precioInput').value;
        var stock = document.getElementById('stockInput').value;
        var categoria = document.getElementById('categoriaInput').value;
    
        // Construir un objeto con los datos
        var producto = {
            id: codigo,  // Reemplazar con el ID correcto
            nombre: nombre,
            descripcion: descripcion,
            precio: precio,
            stock: stock,
            categoria: categoria
        };
    
        // Realizar la solicitud POST al servidor
        fetch('http://127.0.0.1:8000/productos/update', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(producto),
        })
        .then(response => response.json())
        .then(data => {
            alert("Producto Actualizado")
            fetchProductos()
        })
        .catch(error => console.error('Error fetching data:', error));
    })
}

function cerrarPopup() {
    var popup = document.getElementById('popupContainer');
    popup.style.display = 'none';
}
function actualizar(id){
    var guardar=document.getElementById('guardar');

    guardar.addEventListener('click',()=>{
        // Obtener los valores de los campos de entrada
        var nombre = document.getElementById('nombreInput').value;
        var descripcion = document.getElementById('descripcionInput').value;
        var precio = document.getElementById('precioInput').value;
        var stock = document.getElementById('stockInput').value;
        var categoria = document.getElementById('categoriaInput').value;
        // Construir un objeto con los datos
        var producto = {
            id: id,  // Reemplazar con el ID correcto
            nombre: nombre,
            descripcion: descripcion,
            precio: precio,
            stock: stock,
            categoria: categoria
        };
    
        // Realizar la solicitud POST al servidor
        fetch('http://127.0.0.1:8000/productos/update', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(producto),
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            fetchProductos()
        })
        .catch(error => console.error('Error fetching data:', error));
    })
     
}

fetchProductos();