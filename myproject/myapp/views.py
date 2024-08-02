import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
import os

@csrf_exempt
def call_ml_api(request):
    if request.method == 'POST':
        file = request.FILES.get('file')

        if not file:
            return JsonResponse({'error': 'No file provided'}, status=400)

        # Save the file temporarily
        file_path = default_storage.save(file.name, file)
        file_full_path = default_storage.path(file_path)

        # Define the API endpoint
        api_url = 'http://13.250.44.65/predict'  # Replace with your API endpoint

        try:
            with open(file_full_path, 'rb') as f:
                files = {'file': f}
                response = requests.post(api_url, files=files)
                response_data = response.json()

            # Clean up the temporary file
            os.remove(file_full_path)

            # Process the API response
            predicted_class = response_data.get('predicted_class')
            predictions = response_data.get('predictions')

            # Return the response as JSON
            return JsonResponse({
                'predicted_class': predicted_class,
                'predictions': predictions
            })

        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
