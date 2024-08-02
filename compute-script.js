document.getElementById('submit').addEventListener('click', async () => {
    const inputFile = document.getElementById('input').files[0];

    if (!inputFile) {
      alert('Please select a file.');
      return;
    }

    const formData = new FormData();
    formData.append('file', inputFile);

    try {
      const response = await fetch('http://127.0.0.1:8000/api/predict/', {
        method: 'POST',
        body: formData
      });

      const data = await response.json();
      document.getElementById('output').innerText = JSON.stringify(data);
    } catch (error) {
      console.error('Error:', error);
      document.getElementById('output').innerText = 'Error occurred while processing the request.';
    }
  });