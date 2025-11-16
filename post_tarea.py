import requests
import json
import os
import urllib.parse
from datetime import datetime
from bs4 import BeautifulSoup
import sys

file_name = sys.argv[1]
assignment_name_encoded=sys.argv[2]
BASE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE, "tareas.txt"), "r", encoding="utf-8") as archive:
  contenido = json.load(archive)

actividad = contenido[assignment_name_encoded]

course_id = actividad["course_id"]
assignment = actividad["plannable_id"]
original_name = actividad["nombre"]
file_type = ""


date = datetime.today().strftime("%Y-%m-%d")
referer = f"https://experiencia21.tec.mx/calendar#view_name=month&view_start={date}"
referer = urllib.parse.quote(referer)
full_referer = f"https://experiencia21.tec.mx/courses/{course_id}/assignments/{assignment}?return_to={referer}"


with open("datos.txt", "r", encoding="utf-8") as cookies:
  cookies = json.load(cookies)

csrf_Token = cookies.get("_csrf_token")
csrf_Token = urllib.parse.unquote(csrf_Token)


def get_Token():
  url = "https://experiencia21.tec.mx/files/pending"


  headers = {
      "Accept": "application/json+canvas-string-ids, application/json, text/plain, */*",
      "Content-Type": "application/x-www-form-urlencoded",
      "X-CSRF-Token": csrf_Token,
      "X-Requested-With": "XMLHttpRequest",
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
      "Origin": "https://experiencia21.tec.mx",
      "Referer": full_referer,
  }


  payload = {
      "name": file_name,
      "on_duplicate": "rename",
      "no_redirect": "true",
      "attachment[intent]": "submit",
      "attachment[asset_string]": f"assignment_{assignment}",
      "attachment[filename]": file_name,
      "attachment[size]": "20",  # parece que es el tamaño en MB o KB según Canvas
      "attachment[context_code]": f"course_{course_id}",
      "attachment[on_duplicate]": "rename",
      "attachment[content_type]": "application/pdf"
  }

  response = requests.post(url, cookies= cookies, params = payload, headers= headers)
  try:
    if response.text.get("status") == "unauthorized":
      return "No tienes acceso a la tarea"
  except AttributeError:
    return str(response.text)
  


def upload_binary(upload_json):
  upload_json = json.loads(upload_json)
  upload_url = upload_json.get("upload_url", "SIN URL")
  upload_params = upload_json.get("upload_params")
    

  file_path = os.path.join(os.getcwd(), file_name)

     
  headers = {
      "Accept": "*/*",
      "Origin": "https://experiencia21.tec.mx",
      "Referer": full_referer,
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
  }

  try:
    files = {
        "file": (file_name, open(file_path, "rb"), "application/pdf"),
    }

  except FileNotFoundError:
    print(f"El archivo '{file_name}' no existe en: {os.getcwd()}")
    files = None
    sys.exit(1)

  response = requests.post(upload_url, data=upload_params, files=files, headers=headers)

  # print("Upload status:", response.status_code)
  json_response = json.loads(response.text)
  return str(json_response.get("id", "No hay id"))



def get_authenticity_token():
  headers = {
      "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
      "Accept-Encoding": "gzip, deflate, br, zstd",
      "Accept-Language": "en-US,en;q=0.9,es;q=0.8",
      "Cache-Control": "max-age=0",
      "Sec-Ch-Ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
      "Sec-Ch-Ua-Mobile": "?0",
      "Sec-Ch-Ua-Platform": '"Windows"',
      "Sec-Fetch-Dest": "document",
      "Sec-Fetch-Mode": "navigate",
      "Sec-Fetch-Site": "none",
      "Sec-Fetch-User": "?1",
      "Upgrade-Insecure-Requests": "1",
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
      "Referer": "https://experiencia21.tec.mx/calendar",
      "Connection": "keep-alive"
  }

  session = requests.Session()
  session.headers.update(headers)
  session.cookies.update(cookies)

  r = session.get(full_referer, allow_redirects=True, timeout=15)

  if(r.status_code != 200):
    r.raise_for_status()
    print("Error en el request")
    sys.exit(0)

  soup = BeautifulSoup(r.text, "html.parser")
  token_tag = soup.find("input", {"name": "authenticity_token"})
  return token_tag["value"]


def submission(authenticity_token, id_):

  url = f"https://experiencia21.tec.mx/courses/{course_id}/assignments/{assignment}/submissions"

  headers = {
      "Accept": "application/json+canvas-string-ids, application/json, text/plain, */*",
      "Content-Type": "application/x-www-form-urlencoded",
      "X-CSRF-Token": csrf_Token,
      "X-Requested-With": "XMLHttpRequest",
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
      "Origin": "https://experiencia21.tec.mx",
      "Referer": full_referer,
  }
    
  payload = {
    "utf8": "✓",
    "authenticity_token": f"{authenticity_token}",
    "submission[submission_type]": "online_upload",
    "submission[attachment_ids]": f"{id_}",
    "submission[eula_agreement_timestamp]": "",
    "attachments[0][uploaded_data]": f"C:\fakepath\{file_name}",
    "submission[comment]": ""
  }

  response = requests.post(url, cookies=cookies, data= payload, headers=headers)
  # print("------------------response.text----------------\n")
  # print(response.text,"\n")
  # print("------------------response.headers----------------\n")
  # print(response.headers,"\n")
  # print("------------------response.Status----------------\n")


  if response.status_code in [200, 201]:
    print("Se mando la tarea")
  else:
    print("No se mando la tarea. Status diferente de 200")









if __name__ == "__main__":
  prev_token = get_Token()
  if prev_token == "No tienes acceso a la tarea":
    sys.exit(0)
  id = upload_binary(prev_token)
  token = get_authenticity_token()
  submission(token,id)

  



