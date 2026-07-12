import requests

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

def send_chat_message(pregunta: str, sala_id: str) -> dict:
    """
    Envía una pregunta al backend para que Gemini genere una respuesta 
    basada en los documentos de la sala.
    """
    url = f"{BASE_URL}/chat/" # Apuntamos a la nueva ruta
    
    # El backend espera recibir un JSON con 'pregunta' y 'sala_id'
    payload = {
        "pregunta": pregunta,
        "sala_id": sala_id
    }
    
    try:
        # Usamos 'json=payload' porque en FastAPI (backend) usamos un Pydantic BaseModel
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            # Extraemos directamente la "respuesta" que armamos en nuestro chat.py del backend
            return {"success": True, "data": response.json().get("respuesta", "")}
        else:
            return {"success": False, "error": f"Error {response.status_code}: {response.text}"}
            
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
            # El backend (Pydantic) ya nos devuelve el JSON estructurado
            return {"success": True, "data": response.json()}
        else:
            return {"success": False, "error": f"Error {response.status_code}: {response.text}"}
            
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "No se pudo conectar al servidor para generar la evaluación."}
    except Exception as e:
        return {"success": False, "error": f"Error inesperado: {str(e)}"}

def delete_document(doc_id: str):
    """Llama al endpoint DELETE para borrar el documento del sistema completo."""
    try:
        url = f"{BASE_URL}/documents/{doc_id}"
        response = requests.delete(url)
        
        if response.status_code == 200:
            return {"success": True, "message": response.json().get("message")}
        else:
            return {"success": False, "error": response.json().get("detail", "Error desconocido")}
    except Exception as e:
        return {"success": False, "error": str(e)}
    
def send_chat_message(pregunta: str, sala_id: str, modo_mini: bool = False):
    """
    Envía un mensaje al endpoint de chat de la IA, indicando si estamos en el dashboard.
    """
    try:
        url = f"{BASE_URL}/chat/"
        payload = {
            "pregunta": pregunta,
            "sala_id": sala_id,
            "modo_mini": modo_mini
        }
        
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            return response.json().get("respuesta")
        else:
            return f"Error del servidor: {response.json().get('detail', 'Desconocido')}"
    except Exception as e:
        return f"Error de conexión: {str(e)}"