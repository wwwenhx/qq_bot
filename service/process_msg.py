from models import RequestModel,SendGroupMsgParams

def process_msg(msg:str, gid:int) -> RequestModel:
    prefix = "ai_bot"
    if not msg.startswith(prefix):
        return None

    # 去掉前缀，再去掉可能的空格
    content = msg[len(prefix):].lstrip()
    action = "send_group_msg"
    send_params = SendGroupMsgParams(message=content, group_id=gid)
    req = RequestModel(action=action, params=send_params)
    return req