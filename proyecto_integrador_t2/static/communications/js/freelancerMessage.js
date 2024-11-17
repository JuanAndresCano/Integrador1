// Función para hacer scroll hacia abajo en la lista de mensajes
function scrollToBottom() {
    var messagesDiv = document.getElementById("messages");
    if (messagesDiv) {
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }
}

// Ejecutar el scroll cuando la página haya terminado de cargar
window.onload = scrollToBottom;

// Escuchar cuando HTMX carga nuevos mensajes y hacer scroll hacia abajo
document.addEventListener('htmx:afterSwap', function(evt) {
    if (evt.detail.target.id === 'messages') {
        scrollToBottom();
    }
});

// Limpiar la entrada después de enviar el mensaje
document.addEventListener('htmx:wsAfterSend', function(evt) {
    const inputField = document.querySelector('.input-container input');
    if (inputField) {
        inputField.value = '';
    }
});

// Escuchar el WebSocket y hacer scroll hacia abajo cuando se reciba un nuevo mensaje
document.addEventListener('htmx:wsMessage', function(evt) {
    scrollToBottom();
});
