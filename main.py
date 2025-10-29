import asyncio
import websockets
import os
import json
from dotenv import load_dotenv
from models import ResponseModel, RequestModel
from service import process_msg,langchain_reply
# 载入 .env 文件
load_dotenv()

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
NAPCAT_WS_URL = os.getenv("NAPCAT_WS_URL")

async def recv_loop(ws, send_queue: asyncio.Queue):
    """接收消息协程"""
    while True:
        msg = await ws.recv()
        data = json.loads(msg)

        if data.get("post_type") == "message" and data.get("message_type") == "group":
            try:
                parsed_msg = ResponseModel(**data)
                print("📩 收到消息:", parsed_msg.raw_message)

                # 处理消息并放入发送队列
                res: RequestModel | None = process_msg(parsed_msg.raw_message, parsed_msg.group_id)
                if res is not None:
                    await send_queue.put(res)
            except Exception as e:
                print("解析失败:", e)
        else:
            print("📩 收到系统消息:", msg)

async def send_loop(ws, send_queue: asyncio.Queue):
    while True:
        res: RequestModel = await send_queue.get()
        try:
            await ws.send(res.model_dump_json())
            print("✅ 已发送消息:", res.model_dump_json())
        except Exception as e:
             print("发送失败:", e)

async def connect_napcat():
    uri = f"{NAPCAT_WS_URL}?access_token={ACCESS_TOKEN}"
    print(f"正在连接到 Napcat WebSocket: {uri}")
    async with websockets.connect(uri) as ws:
        print("✅ 已连接成功！等待消息中...\n")

        send_queue = asyncio.Queue()  # 创建发送队列
        # 并发运行接收和发送协程
        await asyncio.gather(
            recv_loop(ws, send_queue),
            send_loop(ws, send_queue)
        )

asyncio.run(connect_napcat())