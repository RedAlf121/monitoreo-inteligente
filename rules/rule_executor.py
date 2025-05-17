from pyswip import Prolog
import os

def compare():
    prolog = Prolog()
    prolog.consult("prueba.pl",)
    print(list(prolog.query("talla(1,Y)")))
    
if __name__ == "__main__":
    compare()