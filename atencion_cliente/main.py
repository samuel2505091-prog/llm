"""Asistente de atencion a clientes en terminal.

Uso:
    python main.py          Inicia el chat interactivo.
    python main.py --demo   Ejecuta tres casos de ejemplo sin escribir nada.
"""

import sys

import base_datos
import config
from asistente import AsistenteSoporte

SEPARADOR = "-" * 68

CASOS_DEMO = [
    "Hola, soy Ana Lopez. Quiero saber donde va mi pedido TP-10871.",
    "Gracias. Ahora busco una laptop para mi hijo, tengo hasta 15 mil pesos.",
    "Una cosa mas: el monitor que compre en agosto llego con la pantalla estrellada "
    "y quiero que me lo repongan. Mi correo es ana.lopez@correo.com",
]


def encabezado() -> None:
    print(SEPARADOR)
    print(f"  Asistente de atencion a clientes - {config.NOMBRE_EMPRESA}")
    print(f"  Modelo: {config.MODELO}")
    print(SEPARADOR)
    print("  Comandos: /nuevo reinicia el caso, /resumen genera la bitacora,")
    print("            /tickets lista los folios generados, /salir termina.")
    print(SEPARADOR)


def mostrar_tickets() -> None:
    if not base_datos.TICKETS:
        print("\nNo se han generado tickets en esta sesion.\n")
        return
    print()
    for ticket in base_datos.TICKETS:
        print(f"  {ticket['folio']} | {ticket['prioridad']:6} | {ticket['motivo']}")
        print(f"  {'':10}respuesta comprometida: {ticket['respuesta_comprometida']}")
    print()


def modo_demo(asistente: AsistenteSoporte) -> None:
    print("\nModo demostracion: tres consultas encadenadas.\n")
    for mensaje in CASOS_DEMO:
        print(f"Cliente: {mensaje}\n")
        respuesta = asistente.responder(mensaje)
        print(f"\nAsistente: {respuesta}\n")
        print(SEPARADOR)
    print("\nResumen del caso para bitacora:\n")
    print(asistente.resumen())
    print()
    mostrar_tickets()


def modo_interactivo(asistente: AsistenteSoporte) -> None:
    while True:
        try:
            entrada = input("\nCliente: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\nSesion terminada.\n")
            return

        if not entrada:
            continue

        if entrada == "/salir":
            print("\nSesion terminada.\n")
            return

        if entrada == "/nuevo":
            asistente.reiniciar()
            print("\nCaso reiniciado. El historial anterior se descarto.\n")
            continue

        if entrada == "/resumen":
            print(f"\nResumen para bitacora:\n\n{asistente.resumen()}\n")
            continue

        if entrada == "/tickets":
            mostrar_tickets()
            continue

        print()
        respuesta = asistente.responder(entrada)
        print(f"\nAsistente: {respuesta}")


def main() -> None:
    config.validar_configuracion()
    asistente = AsistenteSoporte()
    encabezado()

    if "--demo" in sys.argv:
        modo_demo(asistente)
    else:
        modo_interactivo(asistente)


if __name__ == "__main__":
    main()
