// Diccionario que contiene los países y sus respectivas ciudades
const citiesByCountry = {
    // América Latina
    'AR': ['Buenos Aires', 'Córdoba', 'Rosario', 'Mendoza'],
    'BR': ['São Paulo', 'Rio de Janeiro', 'Brasilia', 'Salvador'],
    'CL': ['Santiago', 'Valparaíso', 'Concepción', 'La Serena'],
    'CO': ['Bogotá', 'Medellín', 'Cali', 'Cartagena'],
    'PE': ['Lima', 'Cusco', 'Arequipa', 'Trujillo'],
    'MX': ['Ciudad de México', 'Guadalajara', 'Monterrey', 'Puebla'],

    // América del Norte
    'US': ['New York', 'Los Angeles', 'Chicago', 'Houston'],
    'CA': ['Toronto', 'Vancouver', 'Montreal', 'Calgary'],

    // Europa
    'ES': ['Madrid', 'Barcelona', 'Valencia', 'Sevilla'],
    'FR': ['Paris', 'Lyon', 'Marseille', 'Toulouse'],
    'DE': ['Berlin', 'Hamburg', 'Munich', 'Frankfurt'],
    'IT': ['Rome', 'Milan', 'Naples', 'Turin'],
    'UK': ['London', 'Manchester', 'Birmingham', 'Liverpool'],

    // Asia
    'CN': ['Beijing', 'Shanghai', 'Shenzhen', 'Guangzhou'],
    'JP': ['Tokyo', 'Osaka', 'Kyoto', 'Yokohama'],
    'IN': ['Mumbai', 'Delhi', 'Bangalore', 'Chennai'],
    'KR': ['Seoul', 'Busan', 'Incheon', 'Daegu'],
    'SG': ['Singapore'],
    'ID': ['Jakarta', 'Surabaya', 'Bandung', 'Medan'],
    'TH': ['Bangkok', 'Chiang Mai', 'Pattaya', 'Phuket']
};

// Función que se ejecuta cuando se selecciona un país
function updateCities() {
    const countrySelect = document.getElementById('country');
    const citySelect = document.getElementById('city');
    const selectedCountry = countrySelect.value;

    // Limpiar las opciones previas de la ciudad
    citySelect.innerHTML = '';

    // Obtener las ciudades del país seleccionado
    const cities = citiesByCountry[selectedCountry];

    // Agregar las nuevas opciones de ciudades
    cities.forEach(city => {
        const option = document.createElement('option');
        option.value = city;
        option.textContent = city;
        citySelect.appendChild(option);
    });
}
document.addEventListener('DOMContentLoaded', function() {
    const countrySelect = document.getElementById('id_country');
    const citySelect = document.getElementById('id_city');

    countrySelect.addEventListener('change', function() {
        const countryId = this.value;

        fetch(`/ajax/load-cities/?country=${countryId}`)
            .then(response => response.json())
            .then(cities => {
                // Clear the previous options
                citySelect.innerHTML = '<option value="">Select City</option>';

                // Add the new options
                cities.forEach(city => {
                    const option = document.createElement('option');
                    option.value = city.id;
                    option.textContent = city.name;
                    citySelect.appendChild(option);
                });
            })
            .catch(error => console.error('Error:', error));
    });
});
