"""Capa de conversacion contra la API de OpenAI.

Mantiene el historial del chat, envia cada turno al modelo y resuelve el ciclo
de llamadas a herramientas hasta obtener una respuesta en texto para el cliente.
"""

from openai import OpenAI

import config
import herramientas


class AsistenteSoporte:
    def __init__(self) -> None:
        self.cliente = OpenAI(api_key=config.API_KEY)
        self.historial = [{"role": "system", "content": config.INSTRUCCIONES_SISTEMA}]

    def reiniciar(self) -> None:
        """Descarta la conversacion actual y deja solo las instrucciones."""
        self.historial = [{"role": "system", "content": config.INSTRUCCIONES_SISTEMA}]

    def _llamar_modelo(self):
        return self.cliente.chat.completions.create(
            model=config.MODELO,
            messages=self.historial,
            tools=herramientas.HERRAMIENTAS,
            tool_choice="auto",
            temperature=config.TEMPERATURA,
        )

    def responder(self, mensaje_usuario: str) -> str:
        """Procesa un turno completo y devuelve el texto para el cliente."""
        self.historial.append({"role": "user", "content": mensaje_usuario})

        for _ in range(config.MAX_ITERACIONES_HERRAMIENTAS):
            try:
                respuesta = self._llamar_modelo()
            except Exception as error:  # noqa: BLE001
                return f"No fue posible contactar al modelo. Detalle tecnico: {error}"

            mensaje = respuesta.choices[0].message

            if not mensaje.tool_calls:
                texto = mensaje.content or ""
                self.historial.append({"role": "assistant", "content": texto})
                return texto.strip()

            # El modelo pidio datos: se registran las llamadas y se ejecutan.
            self.historial.append(
                {
                    "role": "assistant",
                    "content": mensaje.content,
                    "tool_calls": [
                        {
                            "id": llamada.id,
                            "type": "function",
                            "function": {
                                "name": llamada.function.name,
                                "arguments": llamada.function.arguments,
                            },
                        }
                        for llamada in mensaje.tool_calls
                    ],
                }
            )

            for llamada in mensaje.tool_calls:
                resultado = herramientas.ejecutar(
                    llamada.function.name, llamada.function.arguments
                )
                self.historial.append(
                    {
                        "role": "tool",
                        "tool_call_id": llamada.id,
                        "name": llamada.function.name,
                        "content": resultado,
                    }
                )

        return (
            "El caso requiere revision manual. Se sugiere solicitar el folio de soporte "
            "a un agente humano."
        )

    def resumen(self) -> str:
        """Genera un resumen del caso para dejarlo en la bitacora de soporte."""
        turnos = [m for m in self.historial if m["role"] in ("user", "assistant")]
        if not turnos:
            return "No hay conversacion que resumir."

        peticion = list(self.historial) + [
            {
                "role": "user",
                "content": (
                    "Redacta un resumen del caso en maximo cinco lineas, en tercera persona, "
                    "indicando el motivo de contacto, los datos consultados y el resultado. "
                    "No agregues informacion que no aparezca en la conversacion."
                ),
            }
        ]
        try:
            respuesta = self.cliente.chat.completions.create(
                model=config.MODELO,
                messages=peticion,
                temperature=0.2,
            )
        except Exception as error:  # noqa: BLE001
            return f"No fue posible generar el resumen. Detalle tecnico: {error}"

        return (respuesta.choices[0].message.content or "").strip()
