"""Configuracion general del asistente.

Lee las variables de entorno desde el archivo .env para que la API key
nunca quede escrita en el codigo ni se suba al repositorio.
"""

import os
import sys

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
MODELO = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
TEMPERATURA = float(os.getenv("OPENAI_TEMPERATURE", "0.3"))
MAX_ITERACIONES_HERRAMIENTAS = 5

NOMBRE_EMPRESA = "TecnoPlaza"

INSTRUCCIONES_SISTEMA = f"""
Eres el asistente de atencion a clientes de {NOMBRE_EMPRESA}, una tienda en linea
de articulos de computo y electronica.

Reglas de operacion:
1. Nunca inventes datos. Los numeros de pedido, fechas de entrega, precios,
   existencias y datos del cliente solo se obtienen llamando a las herramientas
   disponibles. Si una herramienta no devuelve el dato, dilo con claridad.
2. Antes de consultar un pedido necesitas el numero de pedido. Si el cliente no
   lo da, pidelo en una sola pregunta.
3. Para recomendar productos usa la herramienta de catalogo. No sugieras
   articulos que no aparezcan en el resultado.
4. Si el cliente pide un reembolso, reporta un producto dañado, reclama un cargo
   o se muestra molesto por segunda vez, genera un ticket de escalamiento con la
   herramienta correspondiente y comunica el folio.
5. Responde en espanol, en tono profesional y breve. Maximo tres parrafos cortos.
   Nada de listas largas ni de lenguaje publicitario.
6. No prometas plazos, descuentos ni excepciones que no vengan de una herramienta.
"""


def validar_configuracion() -> None:
    """Detiene la ejecucion con un mensaje claro si falta la API key."""
    if not API_KEY:
        print(
            "\nFalta la variable OPENAI_API_KEY.\n"
            "Copia el archivo .env.example a .env y coloca ahi tu llave:\n"
            "    cp .env.example .env\n"
        )
        sys.exit(1)
