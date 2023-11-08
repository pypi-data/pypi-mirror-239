# Librería Python para Extracción de Datos del DPI en Imágenes mediante Textract

Esta librería Python ha sido desarrollada como parte del trabajo de graducación llevado a cabo en la Universidad de San Carlos de Guatemala, en la Facultad de Ingeniería, Escuela de Ingeniería en Ciencias y Sistemas. La librería ha sido diseñada y desarrollada para permitir una fácil integración con el servicio Textract de AWS. Esto garantiza que los usuarios puedan aprovechar la potencia de Textract para la extracción de datos de DPI de manera sencilla. Se realizaron adaptaciones específicas en el servicio Textract para garantizar que la identificación de datos en los DPI sea precisa y eficiente. El proyecto ha sido desarrollado por Luis Manuel Morales López, bajo la asesoría de Msc. Lic. Mariano Mackenzie Asturias Miranda.

## Objetivo

El objetivo principal de esta librería es proporcionar una herramienta que permita la identificación simplificada de datos en documentos DPI, con alta precisión y confiabilidad. Esto tiene aplicaciones en una variedad de ámbitos donde la extracción de datos de DPI sea necesaria, como la automatización de procesos, validación de identidad y más.

## Instalación

Puedes instalar esta librería a través de PyPI utilizando el siguiente comando:

```bash
pip install dpi-textract
```

## Uso

### Ejemplo 1

```python
import dpi_textract as dpi


dpi.client(
    aws_access_key_id="your_id",
    aws_secret_access_key="your_key"
)

mi_dpi = dpi.analyze_dpi(dpi_path_front="your path")


print("CUI:")
print(dpi.cui())
print(dpi.name())

# > CUI:
# > 9876 54321 0123
# > Luis Manuel
```


### Ejemplo 2

```python
import dpi_textract as dpi
import json

dpi.client(
    aws_access_key_id="you_id",
    aws_secret_access_key="your_key"
)

mi_dpi = dpi.analyze_dpi(dpi_path_front="you_path_front",dpi_path_back="your_path_back")

mi_json = json.dumps(mi_dpi, indent=4)
print(mi_json)

# > {
# >     "CUI": "9876 54321 0123",
# >     "PAIS DE NACIMIENTO": "GTM",
# >     "FECHA DE NACIMIENTO": "21DIC2000",
# >     "SEXO": "MASCULINO",
# >     "NACIONALIDAD": "GTM",
# >     "APELLIDOS": "TUS APELLIDOS",
# >     "NOMBRES": "TUS NOMBRES",
# >     "EMISION": "21DIC2000",
# >     "VERSION": "001",
# >     "EXPIRACION": "21DIC2000",
# >     "ESTADO CIVIL": "SOLTERO",
# >     "SERIE": "0000000000001",
# >     "COMUNIDAD": "ESPAÑOL",
# >     "VECINDAD": "GUATEMALA GUATEMALA",
# >     "LUGAR DE NACIMIENTO": "GUATEMALA GUATEMALA"
# > }
```

## Contribuciones

Se agradecen las contribuciones de la comunidad para mejorar esta librería.

## Contacto

Si tienes alguna pregunta o comentario, no dudes en ponerte en contacto con el desarrollador:

- Email: soy.lmml@gmail.com

---

¡Gracias por utilizar la librería! Espero que sea una herramienta útil para tus proyectos.