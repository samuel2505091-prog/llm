"""Herramientas que el modelo puede invocar (function calling).

Cada entrada de HERRAMIENTAS describe a la API de OpenAI que funcion existe y
que parametros necesita. El modelo decide cuando llamarla; este modulo se
encarga de ejecutarla contra la base de datos simulada y devolver el resultado.
"""

import json

import base_datos

HERRAMIENTAS = [
    {
        "type": "function",
        "function": {
            "name": "obtener_pedido",
            "description": (
                "Consulta el estatus, la fecha de entrega, la paqueteria y los articulos de "
                "un pedido a partir de su numero. Usar siempre que el cliente pregunte por "
                "el estado de una compra."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "numero_pedido": {
                        "type": "string",
                        "description": "Numero de pedido, por ejemplo TP-10871.",
                    }
                },
                "required": ["numero_pedido"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "obtener_cliente",
            "description": (
                "Consulta los datos de un cliente por su correo electronico: nombre, "
                "antiguedad, nivel y pedidos asociados."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "correo": {
                        "type": "string",
                        "description": "Correo electronico registrado del cliente.",
                    }
                },
                "required": ["correo"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "buscar_productos",
            "description": (
                "Busca productos en el catalogo por categoria y presupuesto maximo. "
                "Devuelve precio y existencia. Usar antes de recomendar cualquier articulo."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "categoria": {
                        "type": "string",
                        "enum": ["laptops", "monitores", "accesorios"],
                        "description": "Categoria del catalogo.",
                    },
                    "presupuesto_maximo": {
                        "type": "number",
                        "description": "Precio maximo en pesos mexicanos.",
                    },
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "consultar_politica",
            "description": (
                "Devuelve el texto vigente de una politica comercial de la tienda."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "tema": {
                        "type": "string",
                        "enum": ["devoluciones", "garantia", "envios", "facturacion"],
                        "description": "Tema de la politica a consultar.",
                    }
                },
                "required": ["tema"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "crear_ticket",
            "description": (
                "Registra un ticket de escalamiento a un agente humano. Usar en reembolsos, "
                "productos daniados, cargos indebidos o cuando el caso no se pueda resolver."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "motivo": {
                        "type": "string",
                        "description": "Resumen del caso en una linea.",
                    },
                    "prioridad": {
                        "type": "string",
                        "enum": ["alta", "normal"],
                        "description": "Alta para cargos indebidos, danios o entregas vencidas.",
                    },
                    "correo_cliente": {
                        "type": "string",
                        "description": "Correo del cliente si ya se conoce.",
                    },
                },
                "required": ["motivo", "prioridad"],
            },
        },
    },
]

_FUNCIONES = {
    "obtener_pedido": base_datos.obtener_pedido,
    "obtener_cliente": base_datos.obtener_cliente,
    "buscar_productos": base_datos.buscar_productos,
    "consultar_politica": base_datos.consultar_politica,
    "crear_ticket": base_datos.crear_ticket,
}


def ejecutar(nombre: str, argumentos_json: str) -> str:
    """Ejecuta la funcion solicitada por el modelo y devuelve el resultado en JSON."""
    funcion = _FUNCIONES.get(nombre)
    if funcion is None:
        return json.dumps({"error": f"La herramienta {nombre} no existe."}, ensure_ascii=False)

    try:
        argumentos = json.loads(argumentos_json) if argumentos_json else {}
        resultado = funcion(**argumentos)
    except TypeError as error:
        resultado = {"error": f"Argumentos invalidos para {nombre}: {error}"}
    except Exception as error:  # noqa: BLE001
        resultado = {"error": f"Fallo la ejecucion de {nombre}: {error}"}

    return json.dumps(resultado, ensure_ascii=False, default=str)
