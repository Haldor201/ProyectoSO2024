
const btnNew_user=document.getElementById("new_user");
function registerUser() {
    // Obtener los datos del formulario
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const password1 = document.getElementById('password1').value;
    if(email==""||password==""||password1==""){
        alert("Rellene los campos")
    }else{
        if(password!=password1){
            alert("Las contraseñas no coinciden")
        }else{
            // Construir el objeto de datos a enviar
            const userData = {
                email: email,
                password: password
            };
    
            // Realizar la solicitud Fetch
            fetch('http://127.0.0.1:8000/usersjwt/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(userData)
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Error en la solicitud');
                }
                return response.json();
            })
            .then(data => {
                // Manejar la respuesta exitosa
                alert('Usuario registrado con éxito:', data.email);
            })
            .catch(error => {
                // Manejar errores
                alert('Usuario Existente', error);
                console.log(error);
            });
        }
    }
}

const loginForm = document.getElementById('loginForm');

loginForm.addEventListener('submit', async function(event) {
    event.preventDefault();

    const formData = new FormData(loginForm);
    const userData = {
        username: formData.get('username'),
        password: formData.get('password'),
        grant_type: 'password',
        scope: 'read write',
    };
    if(formData.get("username")==""||formData.get("password")==""){
        alert("Rellene los campos")
    }else{
        try {
            const response = await fetch('http://127.0.0.1:8000/usersjwt/loginJWT', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams(userData),
            });
    
            if (!response.ok) {
                throw new Error('Error en la solicitud');
            }
    
            const data = await response.json();
            console.log('Usuario autenticado:', data.acces_token);
            window.location.href = 'ProductoLista.html';
            // Aquí puedes realizar acciones adicionales después del inicio de sesión exitoso
        } catch (error) {
            alert("Usuario no encontrado")
        }
    }
});

btnNew_user.addEventListener("click",registerUser)