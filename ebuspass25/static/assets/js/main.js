
(function() {
  "use strict";
  function uploadAudio() {
    let formData = new FormData(document.getElementById('audioForm'));
    const loadingSpinner = document.getElementById('loadingSpinner');
    const resultDiv = document.getElementById('transcriptionResult');

    loadingSpinner.style.display = 'block';
    resultDiv.innerText = '';

    fetch('/upload/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest',  // Helps Django recognize the request as AJAX
            'X-CSRFToken': '{{ csrf_token }}'      // Add CSRF token
        }
    })
    .then(response => response.text())
    .then(data => {
        // Hide loading spinner
        loadingSpinner.style.display = 'none';
        // Display the transcription result
        resultDiv.innerText = data;
    })
    .catch(error => {
        console.error('Error:', error);
        loadingSpinner.style.display = 'none';
        resultDiv.innerText = "An error occurred while processing.";
    });
}

// Event listener for button click
document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('.btn-primary').addEventListener('click', uploadAudio);
});

})();