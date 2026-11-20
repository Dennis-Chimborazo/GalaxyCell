# GalaxyCell

**Sistema web de inventario de pantallas para celulares, gestión de clientes y consulta de ventas.**

GalaxyCell reúne en un panel las tareas de un negocio de repuestos para celulares. Permite controlar las existencias de cada modelo de pantalla, mantener actualizada la información de los clientes y consultar el detalle de las ventas registradas.

## Funcionalidades

| Módulo | Qué permite hacer |
| --- | --- |
| Acceso | Iniciar y cerrar sesión para acceder al panel de gestión. |
| Inventario de pantallas | Registrar pantallas, agregar existencias y editar o eliminar registros de inventario. Las existencias se organizan por modelo, tipo de pantalla y precio. |
| Clientes | Consultar, registrar y actualizar clientes con su identificación, nombre y dirección. |
| Ventas | Consultar un listado paginado de los detalles de venta y filtrarlos por identificación del cliente o nombre de la pantalla. Cada detalle relaciona una pantalla y su tipo con la cantidad y los precios de compra y venta. |

Cuando se agregan existencias para el mismo modelo, tipo y precio, GalaxyCell suma las unidades al registro existente. Si cambia el tipo o el precio, el inventario conserva un registro separado.

## Tecnologías

- **Python y Django 6** para los modelos, formularios, vistas y la autenticación.
- **PostgreSQL 15** para almacenar los datos. El repositorio incluye una configuración de Docker Compose para levantar la base de datos en desarrollo.
- **Tailwind CSS** para los estilos, **HTMX** para actualizar secciones del panel y **Alpine.js** para las interacciones de la interfaz.

## Estructura del proyecto

| Ruta | Contenido |
| --- | --- |
| [`apps/`](apps/) | Módulos de acceso, panel, pantallas, clientes y ventas. |
| [`config/`](config/) | Configuración y rutas principales de Django. |
| [`core/`](core/) | Vistas base y utilidades compartidas. |
| [`templates/`](templates/), [`theme/`](theme/) y [`static/`](static/) | Plantillas, componentes, estilos y recursos gráficos. |
| [`docker/`](docker/) | Configuración de Docker Compose para PostgreSQL. |
