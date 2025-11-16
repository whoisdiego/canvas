import os #sirve para poder acceder a los archivos de la maquina
import json # dar formato a lo que esta escrito
import base64 # la AES key, la que se usa para encryptar las cookies esta en base 64,esta encriptada 

import time
import sqlite3
import shutil
from pathlib import Path
from datetime import datetime, timedelta #sirve para ver de que hora es la cookie ...
# datetime es como la base y timedelta es el desplaso del tiempo

import win32crypt # pip install pypiwin32
from Crypto.Cipher import AES # pip install pycryptodome


def get_chrome_datetime(chromedate):
    # Regresa un objeto datetime(), con la fecha actualizada
    #chrome ocupa 86400000000 como fecha invalida, entcones dice que si la fecha no es invalida ni tampoco 0, cualquier numero mayor a cero es verdad
    #deltatime es un plazo en el tiempo
    if chromedate != 86400000000 and chromedate:
        try:
            return datetime(1601, 1, 1) + timedelta(microseconds=chromedate)
        except Exception as e:
            print(f"Error: {e}, chromedate: {chromedate}")
            return chromedate
    else:
        return ""

def get_encryption_key():
    #obtener la direccion donde esta la llave
    #os sirve para poder acceder al sistema, como a los archivos y comandos (os.system: dir, echo, del, ...)
    #os.path.join() une en una direccion de path
    #environ da las variables de entorno
    local_state_path = os.path.join(os.environ["USERPROFILE"],
                                    "AppData", "Local", "Google", "Chrome",
                                    "User Data", "Local State")
    
    with open(local_state_path, "r", encoding="utf-8") as f:
        local_state = f.read()
        local_state = json.loads(local_state)

    # decode the encryption key from Base64
    key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    # remove 'DPAPI' str
    key = key[5:]
    # return decrypted key that was originally encrypted
    # using a session key derived from current user's logon credentials
    # doc: http://timgolden.me.uk/pywin32-docs/win32crypt.html
    return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]

def decrypt_data(data, key):
    try:
        # de la data que esta guardada los 12 bytes depsues de los bytes es un numero aleatorio para cada data alamcenada la cual es un metodo de seguirdad, los primeros tres es un prefijo
        iv = data[3:15]
        data = data[15:]
        # generate cipher

        # Galois/Counter (GCM)
        # se crea un objeto con la key, iv, y selecciona el modo en el cual fue cifrado (AES.MODE_GC), es un metodo donde se tiene la key, tiene un counter y una flag
        cipher = AES.new(key, AES.MODE_GCM, iv)

        # Con el objeto se le decifra lo que se le haya puesto en data, se le quita los ultimos 16 bytes porque son la flag que indica si fue modificado algo en los datos. Para despues decodificarlo, lo pasa a una string
        return cipher.decrypt(data)[:-16].decode()

    except:
        try:
            # si los datos no estaban cifrados con AES-GCM se viene a este try donde solo se intenta desencriptarlos con DPAPI, para pasarlo a una string
            return str(win32crypt.CryptUnprotectData(data, None, None, None, 0)[1])
        except:
            # not supported
            return ""
        

def get_accounts():
    path_perfiles = os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data"

    nombre_cuentas = []
    for i in range(os.listdir(path_perfiles)):
        path_prof = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                                "Google", "Chrome", "User Data",f"Profile {i}")
        if os.path.isfile(path_prof):
            path_prof = os.path.join(path_prof, "Preferences")
            with open(path_prof, "r", encoding = "utf-8") as ar:
                archivo = json.load(ar)
            correo = archivo["account_info"]["email"]
        nombre_cuentas.append(correo)



def load_cookies():
    #para checar tiempo
    # inicio = time.time()

    # localidad de las cookies
    db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                            "Google", "Chrome", "User Data", "Default", "Network", "Cookies")
    
    
    
    filename = "Cookies.db"
    try:
        shutil.copy2(db_path, filename)
    except:
        import shadowcopy
        shadowcopy.shadow_copy(db_path, filename)    



    # establece una coneccion con la base de datos
    db = sqlite3.connect(f'file:{filename}?mode=ro', uri=True)
    # ignora errores por la traduccion de bytes, quiere pasar de binario de la base de datos a texto
    db.text_factory = lambda b: b.decode(errors="ignore")

    # crea un objeto al cual se le puede hacer queries
    cursor = db.cursor()
    dominio1 = ".tec.mx%"
    dominio2 = "%experiencia21%"

    cursor.execute("""
    SELECT host_key, name, value, creation_utc, last_access_utc, expires_utc, encrypted_value
    FROM cookies
    WHERE host_key LIKE ? OR  host_key LIKE ?""", (dominio1, dominio2))


    # también puedes buscar por dominio, por ejemplo: youtube.com
    # cursor.execute("""
    # SELECT host_key, name, value, creation_utc, last_access_utc, expires_utc, encrypted_value
    # FROM cookies
    # WHERE host_key LIKE '%youtube.com%'""")

    # obtiene la AES key
    key = get_encryption_key()
    #la informacion que se recibio de la query la cual es una lista de tuples [("expriencia21", "xd", "lol"), ...]

    #direccion en la cual va estar el archivo para que pueda tomarlo
    scipt_location = os.path.dirname(os.path.abspath(__file__))

    flag = False

    with open(os.path.join(scipt_location, "datos.txt"), "w", encoding="utf-8") as archivo:
        archivo.write('{')
        for host_key, name, value, creation_utc, last_access_utc, expires_utc, encrypted_value in cursor.fetchall():
            if name =="canvas_session":
                flag = True
            if not value:
                decrypted_value = decrypt_data(encrypted_value, key)
            else:
                decrypted_value = value
            #dar la estructura de json para la request
            archivo.write(f""""{name}":"{decrypted_value}",\n""")
            
    if flag == False:
        db.commit()
        db.close()
        return False
    # Ahora eliminamos la última coma y agregamos la llave de cierre
    with open(os.path.join(scipt_location, "datos.txt"), "r+", encoding="utf-8") as archivo:
        contenido = archivo.read()
        # Quitamos el último carácter si es coma o salto de línea
        contenido = contenido.rstrip(",\n")
        contenido += "}"
        #mover el punto al inicio del archivo file.seek(desplazamiento, desde que posicion = 0)
        archivo.seek(0)
        archivo.write(contenido)
        archivo.truncate()


    # commit changes
    db.commit()
    # close connection
    db.close()
    

    # #para checar tiempo
    # fin = time.time()
    # print(f"Tiempo de ejecución: {fin - inicio:.6f} segundos")


if __name__ == "__main__":
    load_cookies()