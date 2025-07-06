#gmail
from email.message import EmailMessage
import smtplib

##google sheets
import pandas as pd
import pygsheets

##whatsapp 
from heyoo import WhatsApp

#openai
from openai import OpenAI
from time import sleep
import json

##Obtener el api key
from dotenv import load_dotenv
import os
load_dotenv()

##credenciales
APP_PASSWORD_GMAIL=os.getenv("APP_PASSWORD_GMAIL")
CORREO_REMITENTE=os.getenv("EMAIL_REMITENTE")
OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
#WHATSAPP_API_TOKEN=os.getenv("WHATSAPP_API_TOKEN")
#PHONE_NUMBER_ID=os.getenv("PHONE_NUMBER_ID")
GOOGLE_SHEETS_ID= os.getenv("GOOGLE_SHEETS_ID")


client = OpenAI(api_key=OPENAI_API_KEY) 


#----------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------
#------------------------------------------------ conexion a email ----------------------------------------------------
##conexion a email
def enviar_correo(nombre_lead, correo_lead, mensaje_para_lead):
  try:
    remitente = CORREO_REMITENTE #Del cual se va a lanzar el correo de forma automática -----------------------------------
    destinatario = correo_lead
    mensaje = mensaje_para_lead

    email = EmailMessage()
    email["From"] = remitente
    email["To"] = destinatario
    email["Subject"] = "Mensaje Importante de Datapath para ti " + nombre_lead
    email.set_content(mensaje)

    smtp = smtplib.SMTP_SSL("smtp.gmail.com")
    smtp.login(remitente, APP_PASSWORD_GMAIL) # Contraseña de aplicaciones "asistente_openai" --------------------------------------------------
    smtp.sendmail(remitente, destinatario, email.as_string())
    smtp.quit()
    return True
  
  except:
    return False

#----------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------
#-------------------------------------------- conexion a google sheets ------------------------------------------------
def registrar_google_sheets(nombre, correo, programa):
    # ID de tu hoja de Google Sheets
    sheet_id = GOOGLE_SHEETS_ID
    sheet_name = "Interesados"

    # Leer el CSV como DataFrame
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    df = pd.read_csv(url)
    print("Antes de agregar:")
    print(df)

    # Calcular nuevo ID incremental
    if df.empty:
        new_id = 1
    else:
        # Asegurarse de que la columna ID sea numérica (columna 0)
        df.iloc[:, 0] = pd.to_numeric(df.iloc[:, 0], errors='coerce').fillna(0).astype(int)
        new_id = df.iloc[:, 0].max() + 1

    # Agregar la nueva fila
    df.loc[len(df.index)] = [new_id, nombre, correo, programa]

    print("Después de agregar:")
    print(df)

    try:
        # Autenticación con cuenta de servicio
        service_account_path = 'src/project-asistente-openai-eapr-b764cd1bb3a9.json'
        gc = pygsheets.authorize(service_file=service_account_path)

        # Abrir la hoja
        sh = gc.open_by_url(f"https://docs.google.com/spreadsheets/d/{sheet_id}")

        # Seleccionar la primera hoja
        wks = sh[0]

        # Subir el dataframe completo (sobrescribe)
        wks.set_dataframe(df, (1,1))

        return True
    except Exception as e:
        print("Error:", e)
        return False


#----------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------
#------------------------------------------- enviar mensaje por whatsapp ----------------------------------------------
#def enviar_whatsapp(numero_whatsapp_asesor,mensaje_asesor):
  #conexion a whatsapp
  #"""para enviar mensajea a whatsaap"""
  #try:
    #messenger = WhatsApp(WHATSAPP_API_TOKEN, ## TOKEN
                        #phone_number_id=PHONE_NUMBER_ID #ID_NUMBER
                        #)
    # For sending a Text messages
    messenger.send_message(mensaje_asesor, numero_whatsapp_asesor)
    #return True
  #except:
    #return False

#----------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------
## Ejecutar el RUN
def run_excecuter(run):
  while True:

    run_status=client.beta.threads.runs.retrieve(
        thread_id=run.thread_id,
        run_id=run.id
    )

    if run_status.status =="completed":
      print("accion terminada")
      break


    elif run_status.status=="requires_action":
      print("requiere accion")

      list_of_actions=run_status.required_action.submit_tool_outputs.tool_calls

      print("-----"*20)
      print(list_of_actions)
      print("-----"*20)

      tools_output_list=[] # guardo las salidas de las funciones/tools

      for accion in list_of_actions:

        if accion.function.name =="registrar_google_sheets":

          nombre=accion.function.name
          argumentos=json.loads(accion.function.arguments)


          print("Nombre de la funcion a ejecutar: ", nombre)
          print("Argumentos de la función: ", argumentos)

          interesado_agregado=registrar_google_sheets(argumentos["nombre_lead"],argumentos["correo_lead"],argumentos["producto_de_interes"])

          tools_output_list.append(
              {
                  "tool_call_id": accion.id,
                  "output": str(interesado_agregado)
              }
          )

        elif accion.function.name =="enviar_correo":

          nombre=accion.function.name
          argumentos=json.loads(accion.function.arguments)


          print("Nombre de la funcion a ejecutar: ", nombre)
          print("Argumentos de la funcion: ", argumentos)

          correo_enviado=enviar_correo(argumentos["nombre_lead"],argumentos["correo_lead"],argumentos["mensaje_para_lead"])

          tools_output_list.append(
              {
                  "tool_call_id": accion.id,
                  "output": str(correo_enviado)
              }
          )

        elif accion.function.name =="enviar_whatsapp":


          nombre=accion.function.name
          argumentos=json.loads(accion.function.arguments)


          print("Nombre de la funcion a ejecutar: ", nombre)
          print("Argumentos de la funcion: ", argumentos)

          whatsapp_enviado=enviar_whatsapp(numero_whatsapp_asesor=argumentos["numero_whatsapp_asesor"],mensaje_asesor=argumentos["mensaje_asesor"])

          tools_output_list.append(
              {
                  "tool_call_id": accion.id,
                  "output": str(whatsapp_enviado)
              }
          )

        else:
          return "No se encontró la accion"


      print("ejecucion de acciones ha terminado")
      print(tools_output_list)
      client.beta.threads.runs.submit_tool_outputs(
          thread_id=run.thread_id,
          run_id=run.id,
          tool_outputs=tools_output_list
      )


    else:
      print("Esperando respuesta del Asistente")
      sleep(3)


#if __name__=="__main__":
#  enviar_correo(correo_lead="kevin.inofuente.colque.27@gmail.com",mensaje_para_lead="hola", nombre_lead="kevin")