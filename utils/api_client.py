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