from pyswip import Prolog
import os

def compare():
    prolog = Prolog()
    # Normaliza la ruta para evitar problemas con caracteres de escape
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "prueba.pl"))
    normalized_path = file_path.replace('\\', '/')
    prolog.consult(f"{normalized_path}")
    for result in prolog.query("talla(5, Y)"):
        print(f"Resultado: {result['Y']}")

if __name__ == "__main__":
    compare()