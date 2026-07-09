import base64
import os

def get_image_base64(ruta_imagen: str) -> str:
    """Convierte una imagen local a cadena Base64 para usar en HTML inyectado."""
    try:
        if os.path.exists(ruta_imagen):
            with open(ruta_imagen, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode()
                # Ajusta el tipo MIME según la extensión de tu archivo (png, jpg, svg)
                return f"data:image/png;base64,{encoded_string}"
        return ""
    except Exception as e:
        return ""