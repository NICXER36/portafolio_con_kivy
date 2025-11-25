## 📱 Portafolio Móvil con KivyMD

Este es un proyecto de aplicación móvil multiplataforma desarrollado con *Kivy* y la extensión *KivyMD* para crear una interfaz de usuario moderna y adaptable al estilo Material Design. La aplicación funciona como un *portafolio digital personal* para mostrar proyectos, habilidades e información de contacto de manera interactiva.

-----

### ✨ Características Principales

  * *Diseño Moderno:* Interfaz basada en *Material Design* gracias a KivyMD.
  * *Multiplataforma:* Capacidad de desplegarse en *Android, **iOS, **Windows, **macOS* y *Linux*.
  * *Estructura Modular:* Código organizado para facilitar el mantenimiento y la escalabilidad.
  * *Navegación Intuitiva:* Uso de Screens y Bottom Navigation (o similar) para una experiencia de usuario fluida.

-----

### 🚀 Instalación

Sigue estos pasos para configurar y ejecutar el proyecto localmente.

#### 1\. Clonar el Repositorio

Abre tu terminal o Git Bash y ejecuta:

bash
git clone https://github.com/NICXER36/portafolio_con_kivy.git
cd portafolio_con_kivy


#### 2\. Configurar el Entorno

Se recomienda usar un entorno virtual para manejar las dependencias:

bash
# Crear el entorno virtual (si usas Python 3)
python -m venv venv
# Activar el entorno virtual
# En Windows:
.\venv\Scripts\activate
# En Linux/macOS:
source venv/bin/activate


#### 3\. Instalar Dependencias

El proyecto requiere *Kivy* y *KivyMD*. Instálalos usando pip:

bash
pip install kivy==2.2.1
pip install kivymd


> *Nota:* La versión específica de Kivy puede variar. Si encuentras problemas, consulta la documentación oficial de Kivy para tu sistema operativo.

#### 4\. Ejecutar la Aplicación

Una vez instaladas las dependencias, ejecuta el archivo principal de la aplicación (por ejemplo, main.py):

bash
python main.py


-----

### ⚙ Despliegue (Build de Producción)

Para generar un paquete de aplicación móvil (APK para Android, por ejemplo), se utiliza *Buildozer*.

#### 1\. Instalar Buildozer

Asegúrate de tener *Buildozer* instalado. En un entorno Linux o en WSL/máquina virtual Linux (recomendado):

bash
pip install buildozer


#### 2\. Inicializar y Configurar

En la raíz del proyecto, inicializa Buildozer. Esto creará el archivo de configuración buildozer.spec:

bash
buildozer init


Edita el archivo buildozer.spec para configurar los metadatos de tu aplicación (nombre, paquete, versión, orientación, etc.).

#### 3\. Compilar para Android

Para generar un APK (.apk), ejecuta el siguiente comando. La primera compilación tardará mucho tiempo, ya que descargará todas las herramientas necesarias (SDK de Android, NDK, etc.).

bash
buildozer android debug


El archivo APK generado se encontrará en el directorio ./bin/.

-----

### 🤖 Uso de Inteligencia Artificial en el Desarrollo

Durante el proceso de creación de este portafolio, se emplearon modelos de IA como *Gemini* y *ChatGPT* para optimizar el código, generar contenido y resolver problemas específicos de Kivy/KivyMD.

#### 💡 Prompts Inventados utilizados:

| Herramienta | Tipo de Tarea | Prompt Ejemplo |
| :--- | :--- | :--- |
| *Gemini IA* | Optimización de Código | "Optimiza el siguiente código KivyMD para asegurar un alto rendimiento en la carga de imágenes grandes en un MDBoxLayout. El código actual es: [bloque de código]" |
| *Gemini IA* | Debugging de Layout | "Estoy intentando que un MDBottomNavigation se muestre correctamente en Android, pero la barra de estado lo oculta. ¿Cómo debo modificar mi clase principal para usar Window.softinput_mode = 'below_target' y resolver este problema de layout?" |
| *ChatGPT* | Generación de Contenido | "Genera una descripción concisa y profesional para un proyecto de 'Sistema de Gestión de Inventario' que se pueda incluir en la sección de portafolio de la app." |
| *ChatGPT* | Diseño de Interfaz | "Sugiere una paleta de colores Material Design moderna para una app de portafolio con un tema oscuro y dame los códigos hexadecimales para KivyMD." |

-----

### 👥 Autores

Este proyecto fue desarrollado por:

  * *Nicolas Huenchullan*
  * *Paola Montes*
  * *Catalina Salas*
  * *Jorge Candia*
