def normalize_newlines(text: str) -> str:
    """
    将各种换行符统一为单个换行符
    1. 将转义的 \n 转成真实换行
    2. 将连续换行压缩为单个换行
    """
    if not text:
        return ""

    # 先把接口返回的转义字符 \n 变成真实换行
    text = text.replace("\\n", "\n")

    # 再把连续多个换行压缩成单个换行
    while "\n\n" in text:
        text = text.replace("\n\n", "\n")

    # 去掉开头和结尾多余的换行
    return text.strip()