from fastapi import WebSocket, WebSocketDisconnect, APIRouter
import asyncio
import websockets

graphy_service = APIRouter(tags=["Graphy Service"])
BINANCE_WS_URL = "wss://stream.binance.com:9443/ws/btcusdt@kline_1h"


async def connect_to_binance(ws: WebSocket):
    while True:
        try:
            async with websockets.connect(BINANCE_WS_URL) as binance_ws:
                while True:
                    data = await binance_ws.recv()
                    await ws.send_text(data)
        except websockets.ConnectionClosed:
            print("Binance WebSocket connection closed. Reconnecting in 5 seconds...")
            await asyncio.sleep(5)


@graphy_service.websocket("/ws/bitcoin")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("Connection open")

    binance_task = asyncio.create_task(connect_to_binance(websocket))

    try:
        await binance_task 
    except WebSocketDisconnect:
        print("Client WebSocket disconnected.")
    finally:
        binance_task.cancel()  
        print("Connection closed")
