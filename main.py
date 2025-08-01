from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
import requests as req
import bs4 as bs
import re


@register("nutrimatic", "Loraen_Konpeki", "一个简单的 Nutrimatic 插件", "1.0.0")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""

    @filter.command("nu")
    async def helloworld(self, event: AstrMessageEvent):
        """使用 Nutrimatic 查询表达式，并返回最好10条指令"""
        query_message = event.message_str[3:].strip()  # 用户发的纯文本消息字符串
        if not query_message:
            yield event.plain_result("查询内容为空！")
        # 用户所发的消息的消息链 # from astrbot.api.message_components import *
        message_chain = event.get_messages()
        logger.info(message_chain)
        url = "https://nutrimatic.org/2024"
        data = {
            "q": "nutrimatic",
            "go": "Go"
        }
        logger.info(f"查询内容: {query_message}")
        data['q'] = query_message  # 将查询字符串替换为变量query
        res = req.get(url, params=data)
        soup = bs.BeautifulSoup(res.text, "html.parser")
        spans = soup.find_all('span', limit=10)  # limit=10 只获取前10个匹配的元素
        results = []
        for span in spans:
            style = span.get('style', '')
            font_size_match = re.search(r'font-size:\s*([\d.]+)em', style)
            font_size = font_size_match.group(1) if font_size_match else "未知"
            text = span.get_text(strip=True)
            results.append((font_size, text))
        summary_str = ""
        for i, (size, text) in enumerate(results, 1):
            summary_str += f"{size[:5]:<8} {text}\n"
        summary_str += f"\n显示 {len(results)} 个结果"
        # 发送一条纯文本消息
        yield event.plain_result(summary_str)
        # yield event.plain_result(f"Hello, {user_name}, 你发了 {message_str}!")

    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
