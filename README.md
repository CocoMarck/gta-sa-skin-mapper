# GTA 3d Skin Mapper
Una herramienta sencilla, que sirve para poner en la carpeta input los modelos (`.dff`, `.txd`), y copiarlos a la carpeta output, pero con los nombres indicados en `skin_models.txt`, se copiaran las veces que sean necesarias, para completar la cantidad de `models` indicados.

Ejemplo de uso:
```bash
gta-3d-mapper --mode "normal" --run
```

Compilar con `pyinstaller` (Jala en muchos OS, probado en Win y Linux):
```bash
pyinstaller --onefile main.py
```

