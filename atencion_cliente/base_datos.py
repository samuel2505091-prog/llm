"""Base de datos simulada.

En un sistema real estas funciones consultarian un ERP o una base de datos.
Aqui se resuelven en memoria y se imprime en pantalla cada acceso, para que
quien revise el proyecto vea en que momento el modelo decide consultar datos.
"""

import random
from datetime import datetime, timedelta

CLIENTES = {
    "ana.lopez@correo.com": {
        "nombre": "Ana Lopez",
        "antiguedad_meses": 26,
        "nivel": "Preferente",
        "pedidos": ["TP-10234", "TP-10871"],
    },
    "j.ramirez@correo.com": {
        "nombre": "Jorge Ramirez",
        "antiguedad_meses": 3,
        "nivel": "Estandar",
        "pedidos": ["TP-11002"],
    },
}

PEDIDOS = {
    "TP-10234": {
        "cliente": "ana.lopez@correo.com",
        "estatus": "Entregado",
        "fecha_pedido": "2026-08-28",
        "fecha_entrega": "2026-09-02",
        "paqueteria": "Estafeta",
        "guia": "EST-884213905",
        "articulos": [{"sku": "MON-27C", "descripcion": "Monitor curvo 27 pulgadas", "cantidad": 1}],
        "total_mxn": 5499.00,
    },
    "TP-10871": {
        "cliente": "ana.lopez@correo.com",
        "estatus": "En transito",
        "fecha_pedido": "2026-09-15",
        "fecha_entrega": "2026-09-23",
        "paqueteria": "DHL",
        "guia": "DHL-5520148877",
        "articulos": [{"sku": "TEC-MEC1", "descripcion": "Teclado mecanico inalambrico", "cantidad": 2}],
        "total_mxn": 3180.00,
    },
    "TP-11002": {
        "cliente": "j.ramirez@correo.com",
        "estatus": "Retenido en almacen",
        "fecha_pedido": "2026-09-18",
        "fecha_entrega": None,
        "paqueteria": None,
        "guia": None,
        "articulos": [{"sku": "LAP-14AIR", "descripcion": "Laptop ultraligera 14 pulgadas", "cantidad": 1}],
        "total_mxn": 21990.00,
        "nota_interna": "Pago verificado. Pendiente de asignacion de paqueteria.",
    },
}

CATALOGO = [
    {"sku": "LAP-14AIR", "nombre": "Laptop ultraligera 14 pulgadas", "categoria": "laptops",
     "precio_mxn": 21990.00, "existencia": 12},
    {"sku": "LAP-15PRO", "nombre": "Laptop de trabajo 15 pulgadas", "categoria": "laptops",
     "precio_mxn": 32500.00, "existencia": 4},
    {"sku": "LAP-13ECO", "nombre": "Laptop basica 13 pulgadas", "categoria": "laptops",
     "precio_mxn": 12800.00, "existencia": 27},
    {"sku": "MON-27C", "nombre": "Monitor curvo 27 pulgadas", "categoria": "monitores",
     "precio_mxn": 5499.00, "existencia": 9},
    {"sku": "MON-24P", "nombre": "Monitor plano 24 pulgadas", "categoria": "monitores",
     "precio_mxn": 3299.00, "existencia": 0},
    {"sku": "TEC-MEC1", "nombre": "Teclado mecanico inalambrico", "categoria": "accesorios",
     "precio_mxn": 1590.00, "existencia": 35},
    {"sku": "AUD-ANC2", "nombre": "Audifonos con cancelacion de ruido", "categoria": "accesorios",
     "precio_mxn": 2750.00, "existencia": 18},
]

POLITICAS = {
    "devoluciones": (
        "Se aceptan devoluciones dentro de los 30 dias naturales posteriores a la entrega, "
        "con empaque original y comprobante de compra. El reembolso se aplica al metodo de "
        "pago original en un plazo de 5 a 10 dias habiles."
    ),
    "garantia": (
        "Todos los equipos de computo tienen 12 meses de garantia directa con el fabricante. "
        "Los accesorios tienen 6 meses de garantia con la tienda."
    ),
    "envios": (
        "Envio sin costo en compras superiores a 2,000 pesos. El tiempo de entrega estimado es "
        "de 3 a 7 dias habiles segun la zona."
    ),
    "facturacion": (
        "La factura se solicita dentro del mismo mes de la compra desde el portal, con el numero "
        "de pedido y la constancia de situacion fiscal."
    ),
}

TICKETS = []


def _traza(mensaje: str) -> None:
    """Muestra en pantalla el acceso a la base de datos simulada."""
    print(f"   [sistema] {mensaje}")


def obtener_pedido(numero_pedido: str) -> dict:
    _traza(f"consultando base de datos de pedidos: {numero_pedido}")
    pedido = PEDIDOS.get(numero_pedido.strip().upper())
    if not pedido:
        return {"encontrado": False, "numero_pedido": numero_pedido}
    return {"encontrado": True, "numero_pedido": numero_pedido.strip().upper(), **pedido}


def obtener_cliente(correo: str) -> dict:
    _traza(f"consultando base de datos de clientes: {correo}")
    cliente = CLIENTES.get(correo.strip().lower())
    if not cliente:
        return {"encontrado": False, "correo": correo}
    return {"encontrado": True, "correo": correo.strip().lower(), **cliente}


def buscar_productos(categoria: str = "", presupuesto_maximo: float = 0.0) -> dict:
    _traza(f"consultando catalogo: categoria='{categoria or 'todas'}', tope={presupuesto_maximo or 'sin tope'}")
    resultados = CATALOGO
    if categoria:
        resultados = [p for p in resultados if p["categoria"] == categoria.strip().lower()]
    if presupuesto_maximo:
        resultados = [p for p in resultados if p["precio_mxn"] <= presupuesto_maximo]
    return {"total": len(resultados), "productos": resultados}


def consultar_politica(tema: str) -> dict:
    _traza(f"consultando politicas comerciales: {tema}")
    texto = POLITICAS.get(tema.strip().lower())
    return {"encontrada": bool(texto), "tema": tema, "texto": texto}


def crear_ticket(motivo: str, prioridad: str, correo_cliente: str = "") -> dict:
    folio = f"SOP-{random.randint(10000, 99999)}"
    compromiso = datetime.now() + timedelta(hours=24 if prioridad == "alta" else 72)
    ticket = {
        "folio": folio,
        "motivo": motivo,
        "prioridad": prioridad,
        "correo_cliente": correo_cliente,
        "creado": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "respuesta_comprometida": compromiso.strftime("%Y-%m-%d %H:%M"),
    }
    TICKETS.append(ticket)
    _traza(f"registrando ticket en el sistema de soporte: {folio} ({prioridad})")
    return ticket
