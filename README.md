# Sistema Cine PY

Este proyecto es un sistema de reserva de entradas de cine creado con Python y Tkinter para la interfaz gráfica de usuario. Permite a los usuarios buscar películas, seleccionar entradas, elegir asientos y comprar combos de comida, todo ello mientras aplican promociones y generan un resumen de su compra.

## Caracteristicas

1. **Listado de películas**:
- Muestra una lista de películas con imágenes, sinopsis y duraciones.
- Filtra películas por género, clasificación e idioma.

2. **Selección de entradas**:
- Los usuarios pueden seleccionar tipos de entradas (infantil, adulto, tercera edad) y métodos de pago (tarjeta o efectivo).
- Los precios se calculan en función del tipo de entrada y las promociones activas.

3. **Selección de asientos**:
- Plano de asientos interactivo para elegir los asientos disponibles.
- Validación en tiempo real de la disponibilidad de asientos.

4. **Selección de combos**:
- Muestra combos de comida y bebida con precios.
- Permite la personalización de selecciones (p. ej., palomitas de maíz adicionales, tamaños de bebidas).

5. **Promociones**:
- Muestra promociones actuales y las aplica automáticamente en función de las selecciones del usuario.

6. **Resumen de compra**:
- Proporciona un resumen detallado de la compra del usuario, incluida la película seleccionada, los tipos de entradas, los combos, las promociones y el importe total.

## Requisitos

- Python 3.x
- Tkinter
- SQL Server database libraries

## Instruccion de configuracion

1. Clona el repositorio o descarga el .zip de la URL:
   ```
   git clone <repository-url>
   ```

2. Navega al directorio del proyecto o verifica estar en el directorio:
   ```
   Algo similar a esto:
   D:\user\Escritorio\Josue\JosuJosue\Proyectos\sistema_cine_py>

   SI no esta asi, usa el siguiente comando en la consola
   cd movie-ticket-booking
   ```

3. Instala las dependencias requeridas:
   ```
   pip install -r requirements.txt
   ```
4. Usa el archivo SQL en el Management Studio (2012)

5. Ejecuta la aplicacion:
   ```
   python src/main.py
   ```


