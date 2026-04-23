# Selenium E2E Tests with PyTest

Este es un entorno maduro de automatización End-To-End (E2E) escrito en Python. 
Empleamos **PyTest** para controlar la aserción y flujo de ejecución y **pytest-html** para la creación visual de nuestra reportería incluyendo capturas de pantalla de los fallos.

## Requisitos
Asegúrate de contar con Python instalado y desde la terminal lanza este comando para instalar las librerías necesarias:
```bash
pip install -r requirements.txt
```

## ¿Cómo ejecutar el paquete de pruebas?
Estando en la esta raíz del proyecto, ejecuta siempre tu terminal apuntando hacia la carpeta de `tests/`:

```bash
pytest tests/
```

Una vez completado el comando en rojo o verde, ve a tu carpeta `reports/`, busca dentro el archivo `clinical_authority_report.html` y ábrelo con doble click en Chrome para ver el Dashboard interactivo.
