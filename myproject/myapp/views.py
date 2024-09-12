import requests
from django.shortcuts import render
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import base64
import os
import logging
from PIL import Image, ImageOps, ImageDraw
import io

# Setup logging
logger = logging.getLogger(__name__)

def resize_and_convert_image(input_path, output_path, max_size=(400, 400), border_radius=20, save_as='PNG'):
    """Resize the image, apply a border radius, and convert to PNG or JPEG in one function."""
    
    # Open the image
    image = Image.open(input_path)
    
    # Ensure the image is in RGBA mode to handle transparency if saving as PNG
    if save_as.upper() == 'PNG':
        image = image.convert("RGBA")
    else:
        image = image.convert("RGB")
    
    # Resize the image
    image.thumbnail(max_size, Image.LANCZOS)
    
    # Create a mask for the rounded corners
    mask = Image.new("L", image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([0, 0, image.size[0], image.size[1]], radius=border_radius, fill=255)
    
    # Apply the mask to the image to create rounded corners
    image.putalpha(mask)

    # Save the image in the desired format
    image.save(output_path, format=save_as.upper())
    return output_path

def predict(request):
    context = {}
    resized_image_path = None  # Initialize variable
    
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        
        try:
            # Save the uploaded file temporarily
            file_name = default_storage.save(uploaded_file.name, ContentFile(uploaded_file.read()))
            file_path = default_storage.path(file_name)
            
            # Send the file to the API
            with open(file_path, 'rb') as f:
                response = requests.post(
                    'http://54.151.252.221/predict',
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
                
                # Convert and resize the image with rounded corners, save as PNG
                resized_image_path = resize_and_convert_image(file_path, 'resized_image.png', save_as='PNG')
                
                # Convert the resized image to base64 for display
                with open(resized_image_path, 'rb') as image_file:
                    image_base64 = base64.b64encode(image_file.read()).decode('utf-8')
                
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
            # Optionally delete the resized image if not needed
            if resized_image_path and os.path.exists(resized_image_path):
                os.remove(resized_image_path)
    
    return render(request, 'compute_page.html', context)

def index(request):
    return render(request, 'index/index.html')