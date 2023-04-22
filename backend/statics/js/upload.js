const fileInput = document.getElementById('file-upload');
const dropZone = document.getElementById('file-drop-zone');

// Add a listener for when files are dropped onto the drop zone
dropZone.addEventListener('drop', (event) => {
  event.preventDefault();

  // Get the files that were dropped onto the drop zone
  const files = event.dataTransfer.files;

  // Set the file input element to contain the dropped files
  fileInput.files = files;
});

// Add a listener for when files are dragged over the drop zone
dropZone.addEventListener('dragover', (event) => {
  event.preventDefault();
});

// Add a listener for when files are dragged out of the drop zone
dropZone.addEventListener('dragleave', (event) => {
  event.preventDefault();
});

