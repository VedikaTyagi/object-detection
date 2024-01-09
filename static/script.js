function displayImageOnCanvas(imageFile) {
    const canvas = document.getElementById('outputCanvas');
    const ctx = canvas.getContext('2d');

    const reader = new FileReader();
    reader.onload = function(event) {
        const img = new Image();
        img.onload = function() {
            canvas.width = img.width;
            canvas.height = img.height;
            ctx.drawImage(img, 0, 0);
        };
        img.src = event.target.result;
    };
    reader.readAsDataURL(imageFile);
}



function drawBoundingBoxes(ctx, detectedObjects) {
    detectedObjects.forEach(obj => {
        const label = obj.label;
        const confidence = obj.confidence;
        const boundingBox = obj.bounding_box;

        const [x1, y1, x2, y2] = boundingBox;

        ctx.beginPath();
        ctx.rect(x1, y1, x2 - x1, y2 - y1);
        ctx.lineWidth = 2;
        ctx.strokeStyle = 'red';
        ctx.stroke();

        ctx.font = '14px Arial';
        ctx.fillStyle = 'red';
        ctx.fillText(`${label} ${confidence}`, x1, y1 - 5);
    });
}

function uploadImage() {
    const fileInput = document.getElementById('imageInput');
    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append('file', file);

    displayImageOnCanvas(file); // Display the uploaded image on the canvas

    fetch('/detect_objects', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        const canvas = document.getElementById('outputCanvas');
        const ctx = canvas.getContext('2d');

        drawBoundingBoxes(ctx, data.detected_objects);
    })
    .catch(error => console.error('Error:', error));
}