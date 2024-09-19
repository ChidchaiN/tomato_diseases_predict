# Tomato Diseases Prediction

## Overview

The Tomato Diseases Prediction project aims to provide a machine learning model that can predict various diseases affecting tomato plants based on images. This project integrates image processing and prediction algorithms to help identify common tomato leaf diseases.

## Features

- Image processing to detect and predict tomato leaf diseases.
- Integration with a machine learning model for accurate predictions.
- Web-based interface for uploading and processing images.
- Visualization of predictions and recommendations.

## Installation

To set up the project locally, follow these steps:

1. **Clone the Repository**

    ```bash
    git clone https://github.com/ChidchaiN/tomato_diseases_predict.git
    cd tomato_diseases_predict
    ```

2. **Create a Virtual Environment**

    ```bash
    python -m venv venv
    ```

3. **Activate the Virtual Environment**

    - On Windows:

      ```bash
      venv\Scripts\activate
      ```

    - On macOS/Linux:

      ```bash
      source venv/bin/activate
      ```

4. **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

5. **Run Migrations**

    ```bash
    python manage.py migrate
    ```

6. **Start the Development Server**

    ```bash
    python manage.py runserver
    ```

    The application will be available at `http://127.0.0.1:8000/`.

## Usage

1. Navigate to the web application in your browser.
2. Upload an image of a tomato leaf to receive a prediction of the disease.
3. The application will display the predicted disease and relevant advice.

## Website Images

Here are some screenshots of the web application:

- **Homepage**
  ![Upload Image Page](https://github.com/ChidchaiN/tomato_diseases_predict.git/docs/Screenshot_19-9-2024_232737_3.0.97.52.jpeg)
  
- **Upload Image Page**
  ![Upload Image Page](https://github.com/ChidchaiN/tomato_diseases_predict.git/docs/Screenshot_19-9-2024_232752_3.0.97.52.jpeg)
  
- **Prediction Results Page**
  ![Prediction Results Page](https://github.com/ChidchaiN/tomato_diseases_predict.git/docs/Screenshot 2024-09-19 232821.png)

## Contributing

If you'd like to contribute to this project, please follow these guidelines:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them with descriptive messages.
4. Push your changes to your forked repository.
5. Submit a pull request detailing your changes.

## Contact

For any questions or feedback, please reach out to [Chidchai](mailto:chidchai.nkt7@gmail.com).

## Acknowledgements

- [Django](https://www.djangoproject.com/) - Web framework used
- [TensorFlow](https://www.tensorflow.org/) - Machine learning framework used
- [GitHub](https://github.com/) - Code hosting and collaboration platform
