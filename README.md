# cammseb

Aplicación de gestión integral para un centro de estética y cosmetología. Optimiza la atención al cliente, diagnóstico personalizado y control financiero de servicios.

## Tecnologías Requeridas

- **Python**: Versión 3.8 o superior
- **Bibliotecas**:
  - nicegui: Para la interfaz web interactiva
  - sqlalchemy: Para el manejo de la base de datos

## Instalación y Despliegue

### Paso 1: Instalar Python
Descargue e instale Python desde el sitio oficial: [python.org](https://www.python.org/downloads/)

Asegúrese de marcar la opción "Add Python to PATH" durante la instalación.

### Paso 2: Clonar o Descargar el Proyecto
Clone este repositorio o descargue los archivos del proyecto en una carpeta local.

### Paso 3: Instalar Dependencias
Abra una terminal o línea de comandos en la carpeta del proyecto y ejecute:

```
pip install -r requirements.txt
```

Esto instalará las bibliotecas necesarias: nicegui y sqlalchemy.

### Paso 4: Ejecutar la Aplicación
En la terminal, ejecute:

```
python app.py
```

La aplicación se iniciará y estará disponible en su navegador web en la dirección: `http://localhost:8080`

### Base de Datos
La aplicación utiliza SQLite como base de datos, que se crea automáticamente en el archivo `cammseb.db` en la carpeta del proyecto. No requiere configuración adicional.

## Funcionalidades
- **Gestión de Citas**: Registro de clientas, servicios y fechas.
- **Asistente de Diagnóstico**: Recomendaciones basadas en tipo de piel y estado del cabello.
- **Calculadora de Costos**: Cálculo de precios finales con margen de ganancia.
- **Visualización de Datos**: Tabla dinámica de registros.

## Notas
- La base de datos es "code-first": Las tablas se crean automáticamente al ejecutar la aplicación por primera vez.
- Los datos se mantienen entre sesiones gracias a SQLite.