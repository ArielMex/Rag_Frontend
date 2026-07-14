import requests
import random
import re
import unicodedata

# URL base donde está corriendo el backend
BASE_URL = "http://localhost:8000/api"

def upload_document(file_name: str, file_bytes: bytes, sala_id: str) -> dict:
    """
    Envía un documento PDF al backend para su procesamiento RAG.
    """
    url = f"{BASE_URL}/documents/upload"
    
    archivos = {
        "file": (file_name, file_bytes, "application/pdf")
    }
    
    parametros = {
        "sala_id": sala_id
    }
    
    try:
        response = requests.post(url, params=parametros, files=archivos)
        
        if response.status_code in [200, 201]:
            return {"success": True, "data": response.json()}
        else:
            return {"success": False, "error": f"Error {response.status_code}: {response.text}"}
            
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "No se pudo conectar al servidor. Verifica que el backend esté encendido."}
    except Exception as e:
        return {"success": False, "error": f"Error inesperado: {str(e)}"}

def get_documents(sala_id: str) -> list:
    """
    Consulta al backend los documentos reales que existen en la base de datos para esta sala.
    """
    url = f"{BASE_URL}/documents" 
    parametros = {"sala_id": sala_id}
    
    try:
        response = requests.get(url, params=parametros)
        if response.status_code == 200:
            return response.json()
        return []
    except Exception:
        return []

def send_chat_message(pregunta: str, sala_id: str, modo_mini: bool = False) -> dict:
    """
    Envía una pregunta al backend para que Gemini genere una respuesta 
    basada en los documentos de la sala, soportando el modo_mini del dashboard.
    """
    url = f"{BASE_URL}/chat/"
    
    payload = {
        "pregunta": pregunta,
        "sala_id": sala_id,
        "modo_mini": modo_mini
    }
    
    try:
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            return {"success": True, "data": response.json().get("respuesta", "")}
        else:
            return {"success": False, "error": f"Error del servidor: {response.json().get('detail', 'Desconocido')}"}
            
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "No se pudo conectar al servidor de chat."}
    except Exception as e:
        return {"success": False, "error": f"Error inesperado: {str(e)}"}
    
def generar_quiz_api(sala_id: str, tema: str, cantidad_preguntas: int = 3) -> dict:
    """
    Se comunica con el backend para solicitar un JSON estructurado 
    con las preguntas del quiz generadas por Gemini.
    """
    url = f"{BASE_URL}/chat/quiz" 
    
    payload = {
        "sala_id": sala_id,
        "tema": tema,
        "cantidad_preguntas": cantidad_preguntas
    }
    
    try:
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            return {"success": True, "data": response.json()}
        else:
            return {"success": False, "error": f"Error {response.status_code}: {response.text}"}
            
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "No se pudo conectar al servidor para generar la evaluación."}
    except Exception as e:
        return {"success": False, "error": f"Error inesperado: {str(e)}"}

def delete_document(doc_id: str):
    """
    Llama al endpoint DELETE para borrar el documento del sistema completo.
    """
    try:
        url = f"{BASE_URL}/documents/{doc_id}"
        response = requests.delete(url)
        
        if response.status_code == 200:
            return {"success": True, "message": response.json().get("message")}
        else:
            return {"success": False, "error": response.json().get("detail", "Error desconocido")}
    except Exception as e:
        return {"success": False, "error": str(e)}

def obtener_salas() -> list:
    """
    Trae todas las salas de estudio registradas desde el backend.
    """
    url = f"{BASE_URL}/v1/salas/listar"
    
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.json()
        return []
    except Exception:
        return []

def crear_sala(payload_sala: dict) -> dict:
    """
    Envía los datos de una nueva sala al backend (id, nombre_sala, codigo_acceso).
    """
    url = f"{BASE_URL}/v1/salas/crear"
    
    try:
        response = requests.post(url, json=payload_sala, timeout=5)
        
        if response.status_code in [200, 201]:
            return {"success": True, "data": response.json()}
        else:
            return {"success": False, "error": f"Error {response.status_code}: {response.text}"}
            
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "No se pudo conectar al servidor."}
    except Exception as e:
        return {"success": False, "error": f"Error inesperado: {str(e)}"}

def unirse_a_sala_api(usuario_id: str, sala_id: str, codigo_verificacion: str) -> dict:
    """
    Inscribe a un usuario en una sala validando el código de acceso.
    Envía los IDs en el JSON del body y el código por la URL.
    """
    url = f"{BASE_URL}/v1/salas/unirse"
    
    payload = {
        "usuario_id": usuario_id,
        "sala_id": sala_id
    }
    
    parametros = {
        "codigo_verificacion": codigo_verificacion
    }
    
    try:
        response = requests.post(url, json=payload, params=parametros, timeout=5)
        
        if response.status_code in [200, 201]:
            return {"success": True, "data": response.json()}
        else:
            return {"success": False, "error": response.json().get("detail", f"Error {response.status_code}")}
            
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "No se pudo conectar al servidor."}
    except Exception as e:
        return {"success": False, "error": f"Error inesperado: {str(e)}"}

def obtener_miembros_sala(sala_id: str) -> list:
    """
    Trae todas las inscripciones (miembros) asociadas a una sala de estudio.
    """
    url = f"{BASE_URL}/v1/salas/{sala_id}/miembros"
    
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.json()
        return []
    except Exception:
        return []

def login(email: str, password: str) -> dict:
    """
    Inicia sesión con email y password. Devuelve access_token y refresh_token.
    """
    url = f"{BASE_URL}/v1/auth/login"
    payload = {"email": email, "password": password}
    try:
        response = requests.post(url, json=payload, timeout=5)
        if response.status_code == 200:
            return {"success": True, "data": response.json()}
        else:
            return {"success": False, "error": response.json().get("detail", f"Error {response.status_code}")}
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "No se pudo conectar al servidor. Verifica que el backend esté encendido."}
    except Exception as e:
        return {"success": False, "error": f"Error inesperado: {str(e)}"}


def refrescar_token(refresh_token: str) -> dict:
    """
    Renueva el access_token usando el refresh_token vigente.
    """
    url = f"{BASE_URL}/v1/auth/refresh"
    payload = {"refresh_token": refresh_token}
    try:
        response = requests.post(url, json=payload, timeout=5)
        if response.status_code == 200:
            return {"success": True, "data": response.json()}
        else:
            return {"success": False, "error": response.json().get("detail", f"Error {response.status_code}")}
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "No se pudo conectar al servidor."}
    except Exception as e:
        return {"success": False, "error": f"Error inesperado: {str(e)}"}


def obtener_usuario_actual(access_token: str) -> dict:
    """
    Consulta la info del token actual (GET /auth/me).
    """
    url = f"{BASE_URL}/v1/auth/me"
    headers = {"Authorization": f"Bearer {access_token}"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            return {"success": True, "data": response.json()}
        else:
            return {"success": False, "error": response.json().get("detail", f"Error {response.status_code}")}
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "No se pudo conectar al servidor."}
    except Exception as e:
        return {"success": False, "error": f"Error inesperado: {str(e)}"}

def registrar_usuario(payload_usuario: dict) -> dict:
    """
    Registra un nuevo usuario (POST /users/register).
    payload_usuario debe coincidir con tu schema real de registro,
    p. ej. {"email": ..., "password": ..., "nombre": ...}
    """
    url = f"{BASE_URL}/v1/users/register"
    try:
        response = requests.post(url, json=payload_usuario, timeout=5)
        if response.status_code in [200, 201]:
            return {"success": True, "data": response.json()}
        else:
            return {"success": False, "error": response.json().get("detail", f"Error {response.status_code}")}
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "No se pudo conectar al servidor."}
    except Exception as e:
        return {"success": False, "error": f"Error inesperado: {str(e)}"}

def generar_username(full_name: str) -> str:
    """
    Genera un username válido (^[a-zA-Z0-9_-]+$, 3-50 chars) a partir del nombre completo.
    Agrega un sufijo numérico aleatorio para reducir choques de unicidad.
    """
    texto_normalizado = unicodedata.normalize("NFKD", full_name)
    texto_sin_acentos = "".join(c for c in texto_normalizado if not unicodedata.combining(c))

    base = texto_sin_acentos.lower().strip().replace(" ", "_")
    base = re.sub(r"[^a-zA-Z0-9_\-]", "", base)

    if len(base) < 3:
        base = (base + "usuario")[:10]

    sufijo = str(random.randint(1000, 9999))
    username = f"{base}_{sufijo}"

    return username[:50]

def obtener_perfil(access_token: str) -> dict:
    """
    Trae el perfil completo del usuario autenticado (GET /users/me).
    """
    url = f"{BASE_URL}/v1/users/me"
    headers = {"Authorization": f"Bearer {access_token}"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            return {"success": True, "data": response.json()}
        else:
            return {"success": False, "error": response.json().get("detail", f"Error {response.status_code}")}
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "No se pudo conectar al servidor."}
    except Exception as e:
        return {"success": False, "error": f"Error inesperado: {str(e)}"}