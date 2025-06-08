import os
import requests
from typing import Dict, Any
from mcp.server.fastmcp import FastMCP


def get_api_key() -> str:
    """Get TinyURL API Key from environment variables"""
    api_key = os.getenv("TINYURL_API_KEY")
    if not api_key:
        raise ValueError("TINYURL_API_KEY environment variable must be set")
    return api_key


# 实例化 FastMCP，命名为 tinyurl
mcp = FastMCP("tinyurl")


@mcp.tool()
def create_short_url(url: str) -> Dict[str, Any]:
    """
    将长链接转换为短链接

    :param url: 待转换为短链接的URL
    :return: Dict类型，包含短链接的信息
    """
    try:
        api_key = get_api_key()
        endpoint = f"https://api.tinyurl.com/create?api_token={api_key}"

        # 准备请求参数
        payload = {"url": url}

        # 设置请求头
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }
        # 发送POST请求
        respoense = requests.post(endpoint, headers=headers, json=payload)
        respoense.raise_for_status()

        # 返回API response
        return respoense.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Unable to create short link:{str(e)}"}
    except ValueError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": f"Error occurred while creating short link :{str(e)}"}


# 定义main函数，用于启动mcp服务器
def main():
    """Star MCP Server"""
    mcp.run()


if __name__ == '__main__':
    main()
