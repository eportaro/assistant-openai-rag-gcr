## Paso 0: Vinculación
gcloud init

## Paso 1: Creación del repositorio
gcloud artifacts repositories create repo-chat-streamlit-datapath --repository-format docker --project project-mlops-10-streamlit --location us-central1

## Paso 2: Crear la imagen de mi APLICACION y subir al repositorio
gcloud builds submit --config=cloudbuild.yaml --project project-asistente-openai-eapr

## Paso 3: Comando para despliegue o ejecución de la imagen en el repositorio
gcloud run services replace service.yaml --region us-central1 --project project-asistente-openai-eapr

## Paso 4: OPCIONAL, Dar permisos de acceso a mi APLICACION.
gcloud run services set-iam-policy servicio-chatbot-kevin-inofuente gcr-service-policy.yaml --region us-central1 --project project-mlops-10-streamlit

## el estado actual de tu servicio de Cloud Run
gcloud run services describe servicio-asistente-openai-eduardo-portaro --region us-central1 --project project-asistente-openai-eapr
