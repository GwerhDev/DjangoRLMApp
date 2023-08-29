# DjangoRLMApp
Challenge para puesto de trabajo Machine Learning: Simple App de Regresión Lineal Múltiple

## Recursos

Existe un repositorio disponible en [git](https://github.com/GwerhDev/DjangoRLMApp).

Existe una versión [online](djangorlmapp.netlify.app) en Netlify.

## Instalación

Utilizar [pip](https://pypi.org/project/pip/) para instalar las dependencias.

```bash
pip install -r requirements.txt
```
Utilizar [pyton](https://www.python.org/) para levantar el servidor en local. `http://localhost:8000`
```bash
python manage.py runserver
```

## Uso
- En la Landing Page, selecciona un archivo xlsx.
- A continuación, se visualizará el contenido del archivo seleccionado y podrás ingresar una variable dependiente y múltiples variables independientes del archivo. 
- Dar click al botón "Aplicar Regresión Lineal Múltiple"".
- Se graficarán los datos y predicciones del modelo.

## Tecnologías

[Django](https://www.djangoproject.com/), [Pandas](https://pandas.pydata.org/)