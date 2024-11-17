
var quill;

document.addEventListener('DOMContentLoaded', function() {
    quill = new Quill('#editor-container', {
        theme: 'snow',
        modules: {
            toolbar: [
                [{ 'header': [1, 2, 3, false] }],
                ['bold', 'italic', 'underline'],
                [{ 'list': 'ordered' }, { 'list': 'bullet' }],
                [{ 'indent': '-1' }, { 'indent': '+1' }],
                [{ 'direction': 'rtl' }],
                [{ 'align': [] }],
                ['clean'],  // Botón para limpiar formato
            ]
        },
        readOnly: true  // Inicializar como solo lectura
    });

    // Selecciona el contenedor del editor
    const editorContainer = document.getElementById('editor-container');
    const toolbar = document.querySelector('.ql-toolbar');  // Selecciona la barra de herramientas
    let isEditorEnabled = false;

    // Función para habilitar el editor
    function enableEditor() {
        quill.enable(true);
        isEditorEnabled = true;
        editorContainer.classList.add('editable');
        toolbar.style.display = 'block';  // Mostrar la barra de herramientas
    }

    // Función para deshabilitar el editor
    function disableEditor() {
        quill.enable(false);
        isEditorEnabled = false;
        editorContainer.classList.remove('editable');
        toolbar.style.display = 'none';  // Ocultar la barra de herramientas
    }

    // Habilitar la edición cuando haces clic en el editor
    editorContainer.addEventListener('click', function(event) {
        event.stopPropagation();  // Prevenir que el clic se propague y deshabilite el editor
        if (!isEditorEnabled) {
            enableEditor();  // Solo habilita si el editor está deshabilitado
        }
    });

    // Deshabilitar la edición cuando se hace clic fuera del editor
    window.addEventListener('click', function(event) {
        // Si el clic ocurrió fuera del editor y no estás interactuando con el toolbar
        if (isEditorEnabled && !editorContainer.contains(event.target) && !event.target.closest('.ql-toolbar')) {
            disableEditor();  // Deshabilitar la edición si el clic es fuera del editor y el toolbar
        }
    });

    // Permitir la selección y aplicación de herramientas sin desactivar el editor
    quill.on('selection-change', function(range, oldRange, source) {
        if (range) {
            // Si hay una selección activa, asegúrate de que el editor esté habilitado
            if (!isEditorEnabled) {
                enableEditor();
            }
        }
    });

    // Habilitar la funcionalidad de eliminar el contenido seleccionado con la tecla "Backspace"
    document.addEventListener('keydown', function(event) {
        if (isEditorEnabled && event.key === 'Backspace') {
            const selection = quill.getSelection();
            if (selection && selection.length > 0) {
                quill.deleteText(selection.index, selection.length);
            }
        }
    });

    // Evitar la desactivación del editor cuando se hace clic dentro de la barra de herramientas
    document.querySelector('.ql-toolbar').addEventListener('click', function(event) {
        event.stopPropagation();
    });
});

// Modal functionality
const titleElement = document.getElementById('projectTitle');
const modal = document.getElementById('modal');
const closeModal = document.getElementsByClassName('close')[0];
const saveTitle = document.getElementById('saveTitle');
const modalProjectTitle = document.getElementById('modalProjectTitle');

// Define translations
const translations = {
    en: {
        successMessage: 'Project title has been successfully updated.',
        errorMessage: 'An error occurred while updating the project title.',
        successMessage1: 'Project job has been successfully updated.',
        errorMessage1: 'An error occurred while updating the project job.',
        successMessage2: 'Project skill has been successfully added.',
        errorMessage2: 'An error occurred while adding the project skill.',
        errorMaxLengthTitle: 'The title cannot exceed 40 characters.',
        errorMaxLengthJob: 'The job position cannot exceed 30 characters.',
        errorEmptyField: 'This field cannot be empty.',
        errorDuration: 'Project duration must be a number up to 3 digits.',
        errorBudget: 'Budget must be a valid positive number.'
    },
    es: {
        successMessage: 'El título del proyecto se ha actualizado con éxito.',
        errorMessage: 'Ocurrió un error al actualizar el título del proyecto.',
        successMessage1: 'El trabajo del proyecto se ha actualizado con éxito.',
        errorMessage1: 'Ocurrió un error al actualizar el trabajo del proyecto.',
        successMessage2: 'La habilidad del proyecto se ha agregado con éxito.',
        errorMessage2: 'Ocurrió un error al agregar habilidad del proyecto.',
        errorMaxLengthTitle: 'El título no puede exceder los 40 caracteres.',
        errorMaxLengthJob: 'El puesto de trabajo no puede exceder los 30 caracteres.',
        errorEmptyField: 'Este campo no puede estar vacío.',
        errorDuration: 'La duración del proyecto debe ser un número de hasta 3 dígitos.',
        errorBudget: 'El presupuesto debe ser un número positivo válido.'
    }
};


/// Get the current language of the page
const currentLanguage = document.documentElement.lang;

function setLanguage(language) {
    if (language === 'en') {
        console.log("Language changed to English")
        location.href = 'index_en.html'; // Redirige a la página en inglés
    } else if (language === 'es') {
        console.log("Idioma cambiado a Español")
        location.href = 'index_es.html'; // Redirige a la página en español
    }
}

// Function to show notification with localized messages
function showNotification(type = 'success', messageKey = 'successMessage') {
    const notification = document.getElementById('notification');
    const message = translations[currentLanguage][messageKey];
    notification.textContent = message;

    if (type === 'error') {
        notification.classList.add('error');
    } else {
        notification.classList.remove('error');
    }

    notification.classList.add('show');
    setTimeout(() => notification.classList.remove('show'), 3000);
}

// Save title and update the title element
saveTitle.onclick = function () {
    const titleValue = modalProjectTitle.value.trim();
    if (titleValue === '') {
        showNotification('error', 'errorEmptyField');
        return;
    }
    if (titleValue.length > 40) {
        showNotification('error', 'errorMaxLengthTitle');
        return;
    }
    titleElement.textContent = titleValue;
    modal.style.display = 'none';
    showNotification('success', 'successMessage');
};

// Modal close and open events
titleElement.onclick = function () {
    modal.style.display = 'flex';
    modal.classList.add('open');
};
closeModal.onclick = function () {
    modal.style.display = 'none';
    modal.classList.remove('open');
};
window.onclick = function (event) {
    if (event.target == modal) {
        modal.style.display = 'none';
        modal.classList.remove('open');
    }
};





// Variables for job position modal
const jobElement = document.getElementById('jobPosition'); // Cambia el selector por el ID
const modalJob = document.getElementById('modal-job');
const closeJobModal = document.getElementsByClassName('close-job')[0];
const saveJobPosition = document.getElementById('saveJob');
const modalJobPosition = document.getElementById('modalJobPosition');

// Save job position with validation
saveJobPosition.onclick = function () {
    const jobValue = modalJobPosition.value.trim();
    if (jobValue === '') {
        showNotification('error', 'errorEmptyField');
        return;
    }
    if (jobValue.length > 30) {
        showNotification('error', 'errorMaxLengthJob');
        return;
    }
    jobElement.textContent = jobValue;
    modalJob.style.display = 'none';
    showNotification('success', 'successMessage1');
};


// Abrir el modal de puesto de trabajo
jobElement.onclick = function() {
    modalJob.style.display = 'flex';
    modalJob.classList.add('open');
};

// Cerrar el modal al hacer clic fuera de él
window.onclick = function(event) {
    if (event.target == modalJob) {
        modalJob.style.display = 'none';
        modalJob.classList.remove('open');
    }
};

// Seleccionar todos los badges
const badges = document.querySelectorAll('.badge-custom');

// Agregar evento click a cada badge
badges.forEach(badge => {
badge.addEventListener('click', () => {
    // Alternar la clase 'selected' cuando se hace clic
    badge.classList.toggle('selected');
});
});



const addSkillButton = document.getElementById('addSkillButton');
const addSkillModal = document.getElementById('addSkillModal');
const saveSkillButton = document.getElementById('saveSkillButton');
const newSkillInput = document.getElementById('newSkill');
const skillContainer = document.querySelector('.d-flex.flex-wrap.mb-3');
const modalSkill = document.getElementById('addSkillModal');
const closeSkillModal = document.getElementsByClassName('close-skill')[0];

// Mostrar modal al hacer clic en el botón "+"
addSkillButton.addEventListener('click', () => {
  addSkillModal.style.display = 'flex';
});

// Agregar nueva habilidad al hacer clic en "Agregar"
saveSkillButton.addEventListener('click', () => {
  const newSkill = newSkillInput.value.trim();
  if (newSkill) {
    // Crear un nuevo span para la habilidad
    const newSkillBadge = document.createElement('span');
    newSkillBadge.classList.add('badge', 'badge-custom', 'm-1');
    newSkillBadge.textContent = newSkill;

    // Agregar el nuevo badge al contenedor de habilidades
    skillContainer.insertBefore(newSkillBadge, addSkillButton);

    // Limpiar el campo de texto y ocultar el modal
    newSkillInput.value = '';
    addSkillModal.style.display = 'none';

    // Agregar el evento de selección a la nueva habilidad
    newSkillBadge.addEventListener('click', () => {
      newSkillBadge.classList.toggle('selected');
    });
  }
});

// Cerrar el modal al hacer clic fuera del contenido
addSkillModal.addEventListener('click', (e) => {
  if (e.target === addSkillModal) {
    addSkillModal.style.display = 'none';
  }
});

// Cerrar el modal de puesto de trabajo
closeSkillModal.onclick = function() {
    modalSkill.style.display = 'none';
    modalSkill.classList.remove('open');
};

// Cerrar el modal de puesto de trabajo
closeJobModal.onclick = function() {
    modalJob.style.display = 'none';
    modalJob.classList.remove('open');
};


function showNotificationSkill(type = 'success') {
    const notification = document.getElementById('notificationSkill');

    // Get the appropriate message based on language
    const message = type === 'success' ? translations[currentLanguage].successMessage2 : translations[currentLanguage].errorMessage2;
    
    notification.textContent = message;

    // Apply the type (success or error)
    if (type === 'error') {
        notification.classList.add('error');
    } else {
        notification.classList.remove('error');
    }

    // Show the notification
    notification.classList.add('show');

    // Hide the notification after 3 seconds
    setTimeout(() => {
        notification.classList.remove('show');
    }, 3000);
}
document.getElementById('saveSkillButton').addEventListener('click', function() {
    showNotificationSkill('success'); // Asume que la acción es exitosa
    modalSkill.style.display = 'none';
});



// Permitir seleccionar habilidades al hacer clic en ellas
document.querySelectorAll('.badge-custom').forEach(skill => {
    skill.addEventListener('click', function() {
        this.classList.toggle('selected');  // Alternar la clase 'selected' cuando se hace clic
    });
});

// Permitir seleccionar habilidades al hacer clic en ellas
document.querySelectorAll('.badge-custom').forEach(skill => {
    skill.addEventListener('click', function() {
        // Alternar la clase 'selected' para marcar o desmarcar la habilidad
        this.classList.toggle('selected');
    });
});
