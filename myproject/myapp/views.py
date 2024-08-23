import requests
from django.shortcuts import render
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import base64
import os
import logging
from PIL import Image
import io

# Setup logging
logger = logging.getLogger(__name__)

def resize_image(image, max_size=(400, 400)):
    """Resize the image to fit within a box of max_size."""
    image.thumbnail(max_size, Image.LANCZOS)
    return image

def predict(request):
    context = {}
    
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        
        try:
            # Save the uploaded file temporarily
            file_name = default_storage.save(uploaded_file.name, ContentFile(uploaded_file.read()))
            file_path = default_storage.path(file_name)
            
            # Send the file to the API
            with open(file_path, 'rb') as f:
                response = requests.post(
                    'http://13.250.44.65/predict',
                    files={'file': f}
                )
            
            # Process the API response
            if response.status_code == 200:
                result = response.json()
                predicted_class = result.get('predicted_class')
                predictions = result.get('predictions')[0]
                
                # Define the class names based on your model's output
                class_names = ['โรคใบจุดมะเขือเทศ', 'โรคใบไหม้', 'โรคใบจุดวงกลม', 'ใบสุขภาพดี']
                prediction_confidences = {class_name: round(confidence * 100, 2) for class_name, confidence in zip(class_names, predictions)}
                
                # Get the class with the highest confidence
                highest_confidence_class = max(prediction_confidences, key=prediction_confidences.get)
                highest_confidence = prediction_confidences[highest_confidence_class]
                
                # Convert the image to base64 for display
                with open(file_path, 'rb') as image_file:
                    # Open the image
                    image = Image.open(image_file)
                    
                    # Resize the image
                    image = resize_image(image)
                    
                    # Convert the resized image to a byte stream
                    buffered = io.BytesIO()
                    image.save(buffered, format="JPEG")
                    
                    # Encode the byte stream to base64
                    image_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
                
                context = {
                    'predicted_class': highest_confidence_class,
                    'prediction_confidence': highest_confidence,
                    'image_base64': image_base64,
                }
            else:
                context['error'] = 'Error in classification API'
                logger.error(f"API error: {response.status_code} - {response.text}")
        
        except Exception as e:
            context['error'] = 'An error occurred while processing the file.'
            logger.error(f"Error processing file: {e}")
        
        finally:
            # Delete the temporary file
            if os.path.exists(file_path):
                default_storage.delete(file_name)
    
    return render(request, 'compute_page.html', context)
