# GTA 3d Mapper
Una herramienta sencilla, que sirve para poner en la carpeta input los modelos (`.dff`, `.txd`), y copiarlos a la carpeta output, pero con los nombres indicados en `skin_models.txt`, se copiaran las veces que sean necesarias, para completar la cantidad de `models` indicados.

Ejemplo de uso:
```bat
python main.py --mode "normal" --run
```

Compilar con `pyinstaller` (Jala en muchos OS, probado en Win y Linux):
```bash
pyinstaller --onefile --console --name "gta_3d_mapper" main.py 
```

