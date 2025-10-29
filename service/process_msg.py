from models import RequestModel,SendGroupMsgParams
import requests
from dotenv import load_dotenv
import os
from utils import normalize_newlines

# 载入 .env 文件
load_dotenv()

LANGCHAIN_API = os.getenv("LANGCHAIN_API")

def process_msg(msg:str, gid:int) -> RequestModel:
    prefix = "ai_bot"
    if not msg.startswith(prefix):
        return None

    # 去掉前缀，再去掉可能的空格
    content = msg[len(prefix):].lstrip()
    action = "send_group_msg"
    reply=langchain_reply(content)
    reply=normalize_newlines(reply)
    send_params = SendGroupMsgParams(message=reply, group_id=gid)
    req = RequestModel(action=action, params=send_params)
    return req

def langchain_reply(msg:str) -> str:
    payload = {
        "message":msg
    }

    try:
        api=LANGCHAIN_API+"chat"
        response = requests.post(api, json=payload)
        response.raise_for_status()
        data = response.json()
        return data.get("reply")  # 假设接口返回 {"reply": "..."}
    except Exception as e:
        print(f"❌ 调用 Chat 接口失败: {e}")
        return None