# 📊 Proyecto Aurelion

# 1° Demo: Asincrónica

---

## 1. Tema, problema y solución

##🧩 Tema

**Análisis de ventas y comportamiento de clientes** en una tienda digital, utilizando datos de clientes, productos y transacciones registradas.

## ⚠️ Problema

La empresa ha detectado que algunos **clientes han dejado de comprar** o **no han concretado sus compras**, lo que representa una posible pérdida de ingresos.  
Además, existen **productos con bajas ventas** que podrían estar afectando el flujo de inventario y el crecimiento de la tienda.

## 💡 Solución

El proyecto busca desarrollar un sistema de análisis que permita identificar:

- Clientes inactivos o en riesgo de pérdida.
- Productos con baja rotación que podrían necesitar promoción o campañas de marketing.
- Los productos más vendidos y los clientes más activos para fidelizarlos.

De esta manera, la empresa podrá **tomar decisiones basadas en datos**, optimizando sus estrategias de ventas y marketing.

## 🎯 Objetivos del Proyecto

## Objetivo general:

Analizar la información de ventas, clientes y productos para identificar patrones de compra, productos con baja rotación y clientes inactivos, con el fin de proponer estrategias de mejora en ventas, promoción y retención de clientes.

## Objetivos específicos:

1. Detectar clientes que no han realizado compras.
2. Identificar productos con baja rotación.
3. Determinar los productos más vendidos.
4. Analizar los clientes más activos y su volumen de compra.
5. Generar un reporte de resultados que apoye la toma de decisiones.

---

### 2. Dataset de referencia: fuente, definición, estructura, tipos y escala de medición

### 📚 Fuente

Datos generados con fines educativos (archivos Excel provistos para el proyecto Aurelion).

### 🧾 Definición

Base que representa una **tienda virtual**, con un catálogo de productos, registro de clientes y operaciones de venta.

---

### 🛒 **Productos (productos.xlsx)** — ~100 filas

| Campo           | Tipo  | Escala  |
| --------------- | ----- | ------- |
| id_producto     | int   | Nominal |
| nombre_producto | str   | Nominal |
| categoria       | str   | Nominal |
| precio_unitario | float | Razón   |

**Análisis:**  
Esta tabla contiene el catálogo de productos disponibles. A partir de su información se pueden detectar los artículos más y menos vendidos, evaluar los precios unitarios y clasificar las categorías con mayor rotación.

---

### 👥 **Clientes (clientes.xlsx)** — ~100 filas

| Campo          | Tipo | Escala    |
| -------------- | ---- | --------- |
| id_cliente     | int  | Nominal   |
| nombre_cliente | str  | Nominal   |
| email          | str  | Nominal   |
| ciudad         | str  | Nominal   |
| fecha_alta     | date | Intervalo |

**Análisis:**  
Permite identificar el perfil del cliente y su antigüedad. Con esta tabla se pueden analizar **clientes activos vs. inactivos**, **ciudades con mayor número de compradores** y la evolución temporal de registros.

---

### 💳 **Ventas (ventas.xlsx)** — ~120 filas

| Campo          | Tipo | Escala    |
| -------------- | ---- | --------- |
| id_venta       | int  | Nominal   |
| fecha          | date | Intervalo |
| id_cliente     | int  | Nominal   |
| nombre_cliente | str  | Nominal   |
| email          | str  | Nominal   |
| medio_pago     | str  | Nominal   |

**Análisis:**  
Proporciona información sobre las transacciones realizadas. A partir de esta tabla se puede calcular la **frecuencia de compra** por cliente, los **medios de pago más utilizados** y la **distribución temporal de ventas**.

---

### 📦 **Detalle_Ventas (detalle_ventas.xlsx)** — ~300 filas

| Campo           | Tipo  | Escala  |
| --------------- | ----- | ------- |
| id_venta        | int   | Nominal |
| id_producto     | int   | Nominal |
| nombre_producto | str   | Nominal |
| cantidad        | int   | Razón   |
| precio_unitario | float | Razón   |
| importe         | float | Razón   |

**Análisis:**  
Relaciona las ventas con los productos específicos. Es la tabla clave para determinar **cuáles productos se venden más o menos**, los **ingresos generados por producto** y el **ticket promedio por venta**.

### Análisis de Ficheros de Datos: Aurelion

Este documento describe la estructura y propósito de los ficheros de datos en formato `.xlsx` encontrados en el proyecto.

### Descripción de los Ficheros

Basado en sus nombres, los ficheros representan una base de datos relacional simple:

1.  `clientes.xlsx`: Contiene la lista y los datos de todos los clientes. Cada fila representa un cliente único con su información (ID, nombre, etc.).

2.  `productos.xlsx`: Funciona como el catálogo de productos. Cada fila detalla un producto (ID, nombre, precio, stock, etc.).

3.  `ventas.xlsx`: Registra las transacciones de venta. Cada fila es una venta individual, vinculada a un cliente y con una fecha específica.

4.  `detalle_ventas.xlsx`: Es la tabla que conecta las ventas con los productos. Detalla qué productos y en qué cantidad se incluyeron en cada venta.

### ¿Están Normalizados?

**Sí, la estructura que sugieren los nombres de los ficheros indica que los datos están normalizados.**

La normalización es una práctica de diseño de bases de datos que busca organizar los datos para reducir la redundancia y mejorar su integridad. La estructura actual cumple con estos principios:

- **No hay redundancia de datos:** En lugar de repetir la información completa de un producto en cada venta, se utiliza un `ID de producto` para referenciarlo. Lo mismo ocurre con los clientes.
- **Separación de entidades:** Cada tipo de dato (cliente, producto, venta) tiene su propio fichero (tabla), lo que mantiene el modelo organizado.
- **Relaciones mediante IDs:** Los ficheros se vinculan entre sí usando identificadores (IDs), lo cual es el fundamento de un modelo de datos relacional.

### Para una confirmación definitiva sería necesario inspeccionar las columnas de cada fichero, pero la nomenclatura y la separación de los ficheros son un claro indicativo de un diseño de datos normalizado y eficiente.

#### 3. Información, pasos, pseudocódigo y diagrama del programa (Sprint 1)

En esta etapa, el programa funciona como un **visor interactivo de la documentación**, para que el usuario pueda consultar la información clave desde la terminal.

---

#### 3.1 Contenidos accesibles desde el menú

1. Tema, problema y solución
2. Dataset de referencia y estructura
3. Análisis por tabla
4. Escalas de medición
5. Sugerencias y mejoras con Copilot
6. Salir

---

#### 3.2 Pasos

1. Cargar en memoria los textos de esta documentación (por ejemplo, leyendo este `.md` o un módulo `textos.py`).
2. Mostrar un menú numérico con las secciones enumeradas arriba.
3. Según la opción elegida, imprimir el texto correspondiente en pantalla.
4. Permitir volver al menú hasta seleccionar “Salir”.

---

#### 3.3 Pseudocódigo

```text
Inicio
    Cargar textos/plantillas de documentación en un diccionario
    Mientras True:
        Mostrar menú:
            1. Tema, problema y solución
            2. Dataset de referencia
            3. Estructura y análisis por tabla
            4. Escalas de medición
            5. Sugerencias y mejoras con Copilot
            6. Salir
        Leer opción del usuario
        Si opción está entre 1 y 5:
            Imprimir texto asociado
        Si opción == 6:
            Romper bucle
Fin
```

#### 3.4 Diagrama de flujo

##### 4.Escalas de medición

Escala Descripción Ejemplo
Nominal Clasifica sin jerarquía ni orden; se usa para identificar o agrupar elementos. Nombre de producto, ciudad, categoría
Ordinal Ordena categorías, pero sin definir distancias precisas entre ellas. Nivel de satisfacción (bajo, medio, alto)
Intervalo Posee distancias iguales entre valores, pero no tiene un cero absoluto. Fechas o temperatura en °C
Razón Posee cero absoluto y permite comparaciones proporcionales. Precio, cantidad, importe

Aplicación al dataset:

Variables Nominales: id_cliente, nombre_producto, categoría, medio_pago, ciudad.

Variables De Intervalo: fecha, fecha_alta.

Variables De Razón: precio_unitario, cantidad, importe.

###### 5. Sugerencias y mejoras aplicadas con Copilot

Separar la documentación en módulos
Extraer los textos de cada sección a un archivo Python (por ejemplo, textos.py) para facilitar la reutilización y el mantenimiento.

Agregar búsqueda por palabra clave
Permitir que el usuario busque términos específicos dentro de la documentación desde el menú.

Opción de exportar sección
Añadir una función para guardar la sección mostrada en pantalla en un archivo .txt o .md.

Tests automáticos
Implementar pruebas unitarias que verifiquen que cada opción del menú imprime la sección correcta.

Mejorar la experiencia de usuario

Validar la entrada del usuario para evitar errores.
Permitir volver atrás o salir en cualquier momento.
Mostrar mensajes claros en caso de opción inválida.
Posible ampliación futura

Conectar el visor a una base de datos real.
Visualizar los datos en un dashboard interactivo.
