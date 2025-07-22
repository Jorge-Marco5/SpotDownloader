const urlForm = document.getElementById('urlForm');
const youtubeUrlInput = document.getElementById('youtubeUrl');
const result = document.getElementById('result');

// Expresión regular para validar URLs de YouTube
const youtubeRegex = /^(https?:\/\/)?(www\.)?(youtube\.com\/watch\?v=|youtu\.be\/)[\w-]{11}([&?][^\s]*)?$/;

// --- Validación en tiempo real al escribir en el campo de la URL ---
youtubeUrlInput.addEventListener('input', function () {
    const url = this.value.trim();

    // Si el campo está vacío, ocultar el mensaje de resultado
    if (url === '') {
        result.textContent = '';
        result.style.display = 'none';
        return;
    }

    // Mostrar el elemento de resultado para dar feedback
    result.style.display = 'block';
    if (youtubeRegex.test(url)) {
        result.textContent = '✅ URL válida';
        result.style.color = 'green';
    } else {
        result.textContent = '❌ URL no válida de YouTube';
        result.style.color = 'red';
        result.style.margin = '20px 0 20px 0';
    }
});

// --- Manejo del envío del formulario al hacer clic en el botón ---
urlForm.addEventListener('submit', function (e) {
    e.preventDefault();

    const urlInput = youtubeUrlInput.value.trim();

    if (youtubeRegex.test(urlInput)) {
        // La URL es válida, ocultar el mensaje de validación y mostrar "Buscando..."
        result.style.display = "none"; // Se corrige "None" a "none"
        mensajeBuscandoActive();
        // Aquí es donde deberías realizar la llamada al backend para procesar la URL.
        // Por ejemplo, usando fetch() para enviar la URL al servidor.
    } else {
        // Si la URL no es válida al intentar enviar, nos aseguramos de que el mensaje de error sea visible.
        result.textContent = '❌ URL no válida de YouTube';
        result.style.color = 'red';
        result.style.display = 'block';
        // NOTA: Se ha eliminado `location.href="/DYT"` porque redirigir al usuario
        // por un error de validación es una mala experiencia de usuario.
    }
});

    function mensajeDescarga(){
        let mensaje = document.getElementById("Alerta");
        mensaje.style.display = "none";
    }
    function msgCargando(){
        let mensaje = document.getElementById("Alerta");
        mensaje.style.display = "block";
        mensaje.textContent = "Convirtiendo, espere un momento...";
    }

    mensajeDescarga();
//Muestra el mensaje buscando
    function mensajeBuscandoInactivo(){
        let buscando = document.getElementById("mensajeBuscando");
        buscando.style.display = "none";
    }
    
    function mensajeBuscandoActive(){
        let buscando = document.getElementById("mensajeBuscando");
        buscando.style.display = "block";
        buscando.textContent = "Buscando...";
    }

    mensajeBuscandoInactivo();

        const audioFileInput = document.getElementById('audioFile');
        const audioPlayer = document.getElementById('audioPlayer');

        audioFileInput.addEventListener('change', (event) => {
        const file = event.target.files[0];
        if (file) {
            const fileURL = URL.createObjectURL(file);
            audioPlayer.src = fileURL;
            audioPlayer.play();
        }
        });
