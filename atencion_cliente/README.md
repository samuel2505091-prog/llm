# Sistema de atención al cliente automatizado

Asistente de soporte para una tienda en línea, construido sobre la API de OpenAI y operado desde la terminal. El asistente atiende consultas de pedidos, recomienda productos del catálogo, explica políticas comerciales y escala a un agente humano cuando el caso lo requiere.

Proyecto 3 del módulo 7 (LLM) del curso de Inteligencia Artificial.

---

## Qué hace

El modelo no responde de memoria. Cuando la consulta necesita un dato, llama a una función del sistema (*function calling*) y responde únicamente con lo que esa función devuelve. Las funciones disponibles son:

| Herramienta | Para qué sirve |
|---|---|
| `obtener_pedido` | Estatus, fecha de entrega, paquetería y guía de un pedido |
| `obtener_cliente` | Nombre, antigüedad, nivel y pedidos asociados a un correo |
| `buscar_productos` | Catálogo filtrado por categoría y presupuesto, con precio y existencia |
| `consultar_politica` | Texto vigente de devoluciones, garantía, envíos o facturación |
| `crear_ticket` | Escalamiento a un agente humano, con folio y tiempo de respuesta |

Cada acceso a datos se imprime en pantalla con el prefijo `[sistema]`, de modo que se puede ver en qué momento el modelo decidió consultar y con qué parámetros.

---

## Requisitos

- Python 3.9 o superior
- Una llave de la API de OpenAI

---

## Instalación

```bash
# 1. Clonar el repositorio y entrar a la carpeta del proyecto
git clone https://github.com/samuel2505091-prog/llm.git
cd llm/atencion_cliente

# 2. Crear el entorno virtual
python -m venv venv

# 3. Activarlo
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Configurar la llave
cp .env.example .env
```

Abrir el archivo `.env` y sustituir el valor de `OPENAI_API_KEY` por la llave real. El archivo `.env` está excluido del repositorio mediante `.gitignore`; la llave nunca se sube a GitHub.

---

## Ejecución

**Modo demostración.** Ejecuta tres consultas encadenadas sin necesidad de escribir nada. Es la forma más rápida de revisar el proyecto:

```bash
python main.py --demo
```

Los tres casos que corre son: consulta de un pedido en tránsito, recomendación de laptop con presupuesto máximo, y reclamación por producto dañado que termina en un ticket de escalamiento. Al final imprime el resumen del caso y los folios generados.

**Modo interactivo.** Chat abierto en terminal:

```bash
python main.py
```

Comandos disponibles durante la conversación:

| Comando | Efecto |
|---|---|
| `/nuevo` | Reinicia el caso y descarta el historial |
| `/resumen` | Genera un resumen del caso para bitácora de soporte |
| `/tickets` | Lista los folios generados en la sesión |
| `/salir` | Termina la sesión |

---

## Datos de prueba

La base de datos está simulada en memoria, dentro de `base_datos.py`. Estos son los registros cargados:

**Clientes**

| Correo | Nombre | Nivel |
|---|---|---|
| `ana.lopez@correo.com` | Ana López | Preferente |
| `j.ramirez@correo.com` | Jorge Ramírez | Estándar |

**Pedidos**

| Número | Estatus | Observación |
|---|---|---|
| `TP-10234` | Entregado | Monitor curvo, entregado el 2 de septiembre |
| `TP-10871` | En tránsito | Entrega estimada el 23 de septiembre |
| `TP-11002` | Retenido en almacén | Sin paquetería asignada |

Cualquier otro número de pedido devuelve "no encontrado", lo cual sirve para verificar que el asistente no inventa datos.

---

## Estructura del proyecto

```
atencion_cliente/
├── main.py            Punto de entrada: chat en terminal y modo demo
├── asistente.py       Conversación con la API y ciclo de llamadas a herramientas
├── herramientas.py    Definición de las funciones expuestas al modelo
├── base_datos.py      Base de datos simulada (clientes, pedidos, catálogo, políticas)
├── config.py          Variables de entorno e instrucciones del sistema
├── requirements.txt   Dependencias
├── .env.example       Plantilla de configuración
└── .gitignore         Excluye .env y archivos temporales
```

---

## Cómo funciona internamente

1. El mensaje del cliente se agrega al historial de la conversación.
2. El historial completo se envía a la API junto con la lista de herramientas disponibles.
3. Si el modelo responde con una o varias llamadas a función, el programa las ejecuta contra la base simulada y devuelve los resultados al modelo.
4. El ciclo se repite hasta que el modelo produce una respuesta en texto, con un tope de cinco iteraciones para evitar bucles.
5. La respuesta se muestra al cliente y queda en el historial, de modo que los turnos siguientes conservan el contexto.

Las reglas de conducta del asistente están en `config.py`, dentro de `INSTRUCCIONES_SISTEMA`. Entre ellas: no inventar datos, no prometer plazos ni descuentos que no vengan de una herramienta, y escalar automáticamente los casos de reembolso, producto dañado o cargo indebido.

---

## Qué está simulado

Conforme a los lineamientos del proyecto, las capas de datos se resuelven en memoria en lugar de conectarse a sistemas reales:

- La base de clientes, pedidos y catálogo son diccionarios de Python.
- El registro de tickets vive solo durante la sesión; no persiste en disco.
- Los folios se generan con un número aleatorio.

Lo que no está simulado es la interacción con el modelo: todas las respuestas provienen de llamadas reales a la API de OpenAI.

---

## Configuración opcional

En el archivo `.env` se pueden ajustar:

- `OPENAI_MODEL`: modelo a utilizar. Por defecto `gpt-4o-mini`.
- `OPENAI_TEMPERATURE`: nivel de variabilidad de las respuestas. Por defecto `0.3`, un valor bajo porque en atención a clientes conviene la consistencia sobre la creatividad.
