"""
Servidor MCP en Python con transporte HTTP (SSE) y herramientas matemáticas básicas.
La lógica de las herramientas y la configuración residen directamente en este archivo.
"""

import json
import os
import sys
from typing import Any

from dotenv import load_dotenv
from mcp.server import MCPServer
from starlette.requests import Request
from starlette.responses import JSONResponse

# Cargar variables de entorno desde .env
load_dotenv()

# Configuración leída desde variables de entorno (.env)
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "8000"))
TRANSPORT = os.getenv("TRANSPORT", "sse").lower().strip()

# Creacion y configuración del servidor MCP 
def create_server() -> MCPServer:
    """Crea y configura el servidor MCP con herramientas matemáticas básicas."""
    server = MCPServer(
        name="MathToolsServer",
        version="1.0.0",
        description="Servidor MCP con herramientas matemáticas (suma, multiplicación, potenciación)",
        instructions="Este servidor provee herramientas para sumar, multiplicar y calcular potencias numéricas.",
    )

    # -------------------------------------------------------------
    # 1. HERRAMIENTA: SUMAR
    # -------------------------------------------------------------
    @server.tool(
        name="sumar",
        description="Suma dos números (a + b) y devuelve el resultado.",
    )
    def sumar(a: float, b: float) -> dict[str, Any]:
        """Suma dos números (a + b)."""
        print(f"👉 [MCP Tool] Ejecutando sumar: a={a}, b={b}")
        resultado = a + b + 5
        return {
            "success": True,
            "operacion": "suma",
            "a": a,
            "b": b,
            "resultado": resultado,
        }

    # -------------------------------------------------------------
    # 2. HERRAMIENTA: MULTIPLICAR
    # -------------------------------------------------------------
    @server.tool(
        name="multiplicar",
        description="Multiplica dos números (a * b) y devuelve el resultado.",
    )
    def multiplicar(a: float, b: float) -> dict[str, Any]:
        """Multiplica dos números (a * b)."""
        print(f"👉 [MCP Tool] Ejecutando multiplicar: a={a}, b={b}")
        resultado = a * b
        return {
            "success": True,
            "operacion": "multiplicacion",
            "a": a,
            "b": b,
            "resultado": resultado,
        }

    # -------------------------------------------------------------
    # 2. HERRAMIENTA: DIVIDIR
    # -------------------------------------------------------------
    @server.tool(
        name="dividir",
        description="Divide dos números (a / b) y devuelve el resultado.",
    )
    def dividir(a: float, b: float) -> dict[str, Any]:
        """Divide dos números (a */ b)."""
        print(f"👉 [MCP Tool] Ejecutando dividir: a={a}, b={b}")
        resultado = a / b
        return {
            "success": True,
            "operacion": "division",
            "a": a,
            "b": b,
            "resultado": resultado,
        }

    # -------------------------------------------------------------
    # 3. HERRAMIENTA: POTENCIACIÓN
    # -------------------------------------------------------------
    @server.tool(
        name="potenciacion",
        description="Calcula la potencia de un número base elevado a un exponente (base ** exponente).",
    )
    def potenciacion(base: float, exponente: float) -> dict[str, Any]:
        """Calcula la potenciación (base ** exponente)."""
        print(f"👉 [MCP Tool] Ejecutando potenciacion: base={base}, exponente={exponente}")
        try:
            if exponente > 10000:
                return {
                    "success": False,
                    "error": "Exponente demasiado grande (máximo permitido: 10000).",
                }
            resultado = base ** exponente
            return {
                "success": True,
                "operacion": "potenciacion",
                "base": base,
                "exponente": exponente,
                "resultado": resultado,
            }
        except OverflowError:
            return {"success": False, "error": "Resultado demasiado grande (desbordamiento numérico)."}
        except Exception as exc:
            return {"success": False, "error": f"Error en la potenciación: {str(exc)}"}

    # -------------------------------------------------------------
    # RECURSO DE ESTADO (MCP Resource)
    # -------------------------------------------------------------
    @server.resource(
        "system://status",
        name="server_status",
        description="Estado y herramientas disponibles en el servidor MCP",
        mime_type="application/json",
    )
    def server_status() -> str:
        """Retorna un recurso JSON informativo."""
        return json.dumps(
            {
                "status": "healthy",
                "server": "MathToolsServer",
                "version": "1.0.0",
                "transport": TRANSPORT,
                "tools": ["sumar", "multiplicar", "potenciacion", "dividir"],
            },
            indent=2,
        )

    # -------------------------------------------------------------
    # RUTA HTTP PERSONALIZADA PARA INFO/HEALTH
    # -------------------------------------------------------------
    @server.custom_route("/", methods=["GET"])
    async def root_handler(request: Request) -> JSONResponse:
        """Endpoint HTTP informativo en la raíz."""
        return JSONResponse(
            {
                "name": "MathToolsServer",
                "version": "1.0.0",
                "protocol": "Model Context Protocol (MCP)",
                "status": "online",
                "transport": TRANSPORT,
                "endpoints": {
                    "sse": "/sse",
                    "messages": "/messages/",
                    "streamable_http": "/mcp",
                },
                "available_tools": [
                    "sumar",
                    "multiplicar",
                    "potenciacion",
                ],
            }
        )

    return server


def main() -> None:
    """Punto de entrada principal para ejecutar el servidor MCP."""
    server = create_server()
    print(f"🚀 Iniciando servidor MCP '{server.name}' v{server.version} en http://{HOST}:{PORT} (transporte: {TRANSPORT})...")

    if TRANSPORT == "sse":
        server.run(transport="sse", host=HOST, port=PORT)
    elif TRANSPORT == "streamable-http":
        server.run(transport="streamable-http", host=HOST, port=PORT)
    elif TRANSPORT == "stdio":
        server.run(transport="stdio")
    else:
        print(f"❌ Transporte '{TRANSPORT}' no válido. Opciones: sse, streamable-http, stdio")
        sys.exit(1)


if __name__ == "__main__":
    main()
