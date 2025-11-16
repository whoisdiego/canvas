import requests
import time
import os
import json
from datetime import datetime, date, timedelta
import urllib.parse
import unicodedata
import re




def available_hmw():
  script_location = os.path.dirname(os.path.abspath(__file__))

  try:
    with open(os.path.join(script_location,"datos.txt"), "r", encoding="utf-8") as f:
      contenido = f.read().rstrip()   
      if not contenido.endswith("}"):
        return False
      cookies = json.loads(contenido)
      
  except FileNotFoundError:
    from get_cookies import load_cookies
    flag = load_cookies()
    if not flag:
      return False
    with open(os.path.join(script_location,"datos.txt"), "r", encoding="utf-8") as cookies:
        cookies = json.load(cookies)


  csrf_Token = cookies.get("_csrf_token", "No token")

  csrf_Token = urllib.parse.unquote(csrf_Token)
  

  #diferencia del dia presente para poder ver las tareas anterires
  diferencia = timedelta(days = 0)
  time = datetime.today() - diferencia

  time_string = time.strftime("%Y-%m-%d")

  url = "https://experiencia21.tec.mx/api/v1/planner/items"


  payload = {
      "order" : "asc",
      "start_date": f"{time_string}T06:00:00.000Z",
      "page": "bookmark:WyJ2aWV3aW5nIixbIjIwMjUtMTEtMDQgMDU6NTk6NTkuMDAwMDAwIiwyMDczNzM1OF1d",
      "per_page": "10",
      "order" : "asc"
  }

  headers = {
      "Accept": "application/json+canvas-string-ids, application/json, text/plain, */*",
      "Accept-Encoding": "gzip, deflate, br, zstd",
      "Accept-Language": "en-US,en;q=0.9,es;q=0.8",
      "X-Csrf-Token": csrf_Token,
      "X-Requested-With": "XMLHttpRequest",
      "Referer": "https://experiencia21.tec.mx/",

      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
  }

  response = requests.get(url, cookies= cookies, params = payload, headers= headers)
  response_json = json.loads(response.text)


  
  if isinstance(response_json, dict):
    from get_cookies import load_cookies
    load_cookies()
    with open(os.path.join(script_location,"datos.txt"), "r", encoding="utf-8") as cookies:
        cookies = json.load(cookies)
    response_ = requests.get(url, cookies= cookies, params = payload, headers= headers)
    response_json = json.loads(response_.text)



  
  hash_map = {}
  for tarea in response_json:
    if tarea.get("plannable_type") == "assignment":
      nombre = tarea["plannable"]["title"]
      course_id = tarea.get("course_id") 
      plannable_id = tarea.get("plannable_id") 
      nombre = tarea["plannable"]["title"]

      tareas_={"course_id": f"{course_id}","plannable_id": f"{plannable_id}","nombre": f"{nombre}"}


      texto_limpio = unicodedata.normalize("NFD", nombre)
      texto_limpio = "".join(c for c in texto_limpio if unicodedata.category(c) != "Mn")
      # # Reemplazar espacios múltiples por guiones bajos
      texto_limpio = re.sub(r" +", "_", texto_limpio.strip())

      hash_map[texto_limpio] = tareas_
      print(f"{texto_limpio}\n")
  
  with open(os.path.join(script_location,"tareas.txt"), "w", encoding="utf-8") as archive:
    json.dump(hash_map, archive, ensure_ascii=False, indent=4)
  return ""
  










if __name__ == "__main__":
  string_= available_hmw()
  if(type(string_) == bool): 
    print("Debes de inciar experiencia21")

        


        


  





# https://experiencia21.tec.mx/courses/611388/assignments/20773504?module_item_id=38757491