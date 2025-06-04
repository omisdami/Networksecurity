# Network Security Project

This project is designed to enhance network security by implementing a comprehensive data pipeline for processing and analyzing network data. The key components of the project include:

- **Data Ingestion**: Collects data from various sources, including MongoDB, and processes it into a structured format for further analysis.
- **Data Validation**: Ensures the integrity and quality of the data by validating the number of columns, checking for numerical columns, and detecting dataset drift.
- **Data Transformation**: Transforms the data into a suitable format for model training, including handling missing values and converting data types.
- **Model Training**: Trains machine learning models to predict network security threats using the transformed data.
- **Model Evaluation**: Evaluates the performance of the trained models using classification metrics to ensure they meet the expected accuracy.
- **Cloud Integration**: Syncs data and models with AWS S3 for storage and deployment.

The project is structured to facilitate easy integration and deployment, leveraging tools like FastAPI for API development and Jinja2 for templating.

PROJECT STRUCTURE
![diagram](https://github.com/user-attachments/assets/4be01271-7286-43d2-90f5-4c6854c16eb3)
