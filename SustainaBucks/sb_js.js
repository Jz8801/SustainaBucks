document.addEventListener('DOMContentLoaded', () => {
    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    const captureBtn = document.getElementById('captureBtn');
    let stream;
    const webcamElement = document.getElementById('webcam');
    const canvasElement = document.getElementById('canvas');
    const captureButton = document.getElementById('capture');
    const uploadForm = document.getElementById('uploadForm');
    const imageDataInput = document.getElementById('imageData');
    const context = canvasElement.getContext('2d');
    let videoTracks;
    function enableWebcam() {
        webcamElement.style.display = 'block';
        captureButton.style.display = 'block';
        uploadForm.style.display = 'none';
        setupWebcam();
    }
    function enableUpload() {
        webcamElement.style.display = 'none';
        captureButton.style.display = 'none';
        uploadForm.style.display = 'block';
        if (videoTracks) {
            videoTracks.forEach(track => track.stop());
        }
    }


    // Access webcam on page load
    navigator.mediaDevices.getUserMedia({ video: true })
        .then((stream) => {
            video.srcObject = stream;
            video.play();
        })
        .catch((error) => {
            console.error('Error accessing webcam:', error);
        });

    // Capture photo when the button is clicked
    captureBtn.addEventListener('click', () => {
        const context = canvas.getContext('2d');

        // Draw the current video frame on the canvas
        context.drawImage(video, 0, 0, canvas.width, canvas.height);

        // Stop the video stream to release resources
        stream.getTracks().forEach(track => track.stop());

        // Convert canvas content to a data URL representing the captured image
        const imageDataURL = canvas.toDataURL('image/png');

        // Now you can send imageDataURL to your server for analysis using AJAX or other methods
        // Example: sendToServer(imageDataURL);
    });

});
