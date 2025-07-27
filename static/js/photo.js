document.getElementById('id_image').onchange = function(event) {
    const file = event.target.files[0];
    if (file) {
        // Создаём временный URL для выбранного файла
        const objectUrl = URL.createObjectURL(file);

        // Обновляем src у изображения
        document.getElementById('previewImage').src = objectUrl;
    }
};