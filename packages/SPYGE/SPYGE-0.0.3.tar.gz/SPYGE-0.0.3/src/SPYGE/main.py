import tkinter as tk
import colorama
import os
import pathlib

def test(i):
    print(colorama.Fore.LIGHTGREEN_EX + "Test " + str(i) + " passed...")
    
class GraphicsExtension:
    def __init__(self) -> None:
        self.BASE_DIR = pathlib.Path(__file__).parent
        if not os.path.exists(self.BASE_DIR / "spyge_data_files/"):
            raise FileNotFoundError("Directory \"spyge_data_files/\" excpected")
            
gr = GraphicsExtension()