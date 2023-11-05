import asyncio
import csv
from datetime import datetime
from pathlib import Path
import random

from pyrogram.types import Message, InlineKeyboardMarkup
from pyrogram.enums import MessageEntityType
from pyrogram.errors import RPCError

from ...utils import truncate_str, flatten
from ..link import Link
from ..lock import pornemby_nohp

from .base import Monitor


class PornembyMonitor:
    class PornembyNoHPMonitor(Monitor):
        name = "Pornemby 血量耗尽停止发言"
        chat_user = "PronembyTGBot2_bot"
        chat_name = "Pornemby"
        chat_keyword = "(.*)血量已耗尽。"
        additional_auth = ["pornemby_pack"]

        async def on_trigger(self, message: Message, key, reply):
            for me in message.entities:
                if me.type == MessageEntityType.TEXT_MENTION:
                    if me.user.id == self.client.me.id:
                        pornemby_nohp[self.client.me.id] = datetime.today().date()

    class PornembyDragonRainMonitor(Monitor):
        name = "Pornemby 红包雨"
        chat_user = "PronembyTGBot2_bot"
        chat_name = "Pornemby"
        chat_keyword = [None]
        additional_auth = ["pornemby_pack"]

        async def on_trigger(self, message: Message, key, reply):
            if message.reply_markup:
                if isinstance(message.reply_markup, InlineKeyboardMarkup):
                    buttons = flatten(message.reply_markup.inline_keyboard)
                    for b in buttons:
                        if "红包奖励" in b.text:
                            try:
                                await message.click(0)
                            except TimeoutError:
                                self.log.info("检测到 Pornemby 抢红包雨, 但没有抢到红包.")
                            except RPCError:
                                self.log.info("检测到 Pornemby 抢红包雨, 但没有抢到红包.")
                            else:
                                self.log.info("检测到 Pornemby 抢红包雨, 已点击.")
                            return

    class PornembyDoubleMonitor(Monitor):
        name = "Pornemby 怪兽自动翻倍"
        chat_user = "PronembyTGBot2_bot"
        chat_name = "Pornemby"
        chat_keyword = "击杀者\s+(.*)\s+是否要奖励翻倍"
        additional_auth = ["pornemby_pack"]

        async def on_trigger(self, message: Message, key, reply):
            for me in message.entities:
                if me.type == MessageEntityType.TEXT_MENTION:
                    if me.user.id == self.client.me.id:
                        if isinstance(message.reply_markup, InlineKeyboardMarkup):
                            try:
                                await message.click(0)
                            except RPCError:
                                pass
                            else:
                                self.log.info("检测到 Pornemby 怪兽击败, 已点击翻倍.")
                                return

    class PornembyRegisterMonitor(Monitor):
        name = "Pornemby 抢注"
        chat_name = "Pornemby"
        chat_user = "PornembyTGBot_bot"
        chat_keyword = "开 放 注 册"
        additional_auth = ["pornemby_pack"]

        async def on_trigger(self, message: Message, key, reply):
            try:
                await message.click(0)
            except TimeoutError:
                self.log.info("检测到 Pornemby 抢注, 但没有抢到.")
            except RPCError:
                self.log.info("检测到 Pornemby 抢注, 但没有抢到.")
            else:
                self.log.info("检测到 Pornemby 抢注, 已点击.")

    class PornembyAnswerResultMonitor(Monitor):
        name = "Pornemby 科举答案"
        chat_name = ["Pornemby", "PornembyFun"]
        chat_keyword = r"问题\d*：(.*?)\n+A:(.*)\n+B:(.*)\n+C:(.*)\n+D:(.*)\n+答案为：([ABCD])"
        additional_auth = ["pornemby_pack"]

        key_map = {"A": 1, "B": 2, "C": 3, "D": 4}

        async def on_trigger(self, message: Message, key, reply):
            spec = f"[gray50]({truncate_str(key[0], 10)})[/]"
            self.log.info(f"本题正确答案为 {key[5]} ({key[self.key_map[key[5]]]}): {spec}.")

    class PornembyAnswerMonitor(Monitor):
        name = "Pornemby 科举"
        chat_name = ["Pornemby", "PornembyFun"]
        chat_user = "pornemby_question_bot"
        chat_keyword = r"问题\d*：(.*?)\n+(A:.*\n+B:.*\n+C:.*\n+D:.*)\n(?!\n*答案)"
        additional_auth = ["pornemby_pack"]

        cache = {}
        lock = asyncio.Lock()

        key_map = {
            "A": "🅰",
            "B": "🅱",
            "C": "🅲",
            "D": "🅳",
        }

        def __init__(self, *args, **kw):
            super().__init__(*args, **kw)
            self.cache_file = Path(self.basedir) / "pornemby_question.csv"
            self.update_task = None

        async def update_cache(self, to_date=None):
            cache_timestamp = self.cache_file.with_name("pornemby_question.timestamp")
            self.cache_file.parent.mkdir(parents=True, exist_ok=True)
            if not self.cache_file.exists():
                created = True
                to_date = datetime.fromtimestamp(0)
                self.log.info("首次使用 Pornemby 科举, 正在缓存问题答案历史.")
            else:
                created = False
                if cache_timestamp.exists() and not to_date:
                    with open(cache_timestamp) as f:
                        try:
                            to_date = datetime.fromtimestamp(float(f.read()))
                        except ValueError:
                            to_date = datetime.fromtimestamp(0)
                else:
                    to_date = datetime.fromtimestamp(0)
                self.log.info(f"正在更新问题答案历史缓存.")
                self.log.debug(f"上一次问题答案历史写入于 {to_date.strftime('%Y-%m-%d %H:%M')}.")
            count = 0
            qs = 0
            finished = False
            with open(self.cache_file, mode="a+", newline="") as csvfile:
                writer = csv.writer(csvfile)
                if created:
                    writer.writerow(["Question", "A", "B", "C", "D", "Answer"])
                while not finished:
                    finished = True
                    m: Message
                    async for m in self.client.get_chat_history("PornembyFun", limit=100, offset=count):
                        if m.date < to_date:
                            break
                        count += 1
                        finished = False
                        if m.text:
                            for key in PornembyMonitor.PornembyAnswerResultMonitor.keys(m):
                                qs += 1
                                writer.writerow(key)
                    if count and (finished or count % 500 == 0):
                        self.log.info(f"读取问题答案历史: 已读取 {qs} 问题 / {count} 信息.")
                        await asyncio.sleep(2)
            self.log.debug(f"已向问题答案历史缓存写入 {qs} 条问题.")
            with open(cache_timestamp, "w+", encoding="utf-8") as f:
                f.write(str(datetime.now().timestamp()))

        async def read_cache(self):
            if not self.cache_file.exists():
                return {}
            questions = {}
            with open(self.cache_file, "r") as csvfile:
                rows = csv.DictReader(csvfile)
                for row in rows:
                    entry = dict(row)
                    questions[entry["Question"]] = entry["Answer"]
            self.log.debug(f"已从问题答案历史缓存读取 {len(questions)} 条问题.")
            return questions

        async def update(self):
            try:
                await asyncio.wait_for(self.lock.acquire(), 1)
            except asyncio.TimeoutError:
                self.log.debug("等待其他协程缓存问题答案历史.")
                async with self.lock:
                    return True
            else:
                try:
                    await self.update_cache()
                    self.__class__.cache = await self.read_cache()
                    return True
                finally:
                    self.lock.release()

        async def cache_watchdog(self):
            try:
                while True:
                    secs = 3600 * 12
                    self.log.debug(f"等待 {secs} 秒后进行缓存更新.")
                    await asyncio.sleep(secs)
                    await self.update()
            except asyncio.CancelledError:
                raise

        async def init(self):
            self.update_task = asyncio.create_task(self.cache_watchdog())
            return await self.update()

        async def on_trigger(self, message: Message, key, reply):
            spec = f"[gray50]({truncate_str(key[0], 10)})[/]"
            result = self.cache.get(key[0], None)
            if result:
                self.log.info(f"从缓存回答问题为{result}: {spec}.")
            elif self.config.get("only_history", False):
                self.log.info(f"未从历史缓存找到问题, 请自行回答: {spec}.")
            else:
                for retries in range(3):
                    self.log.debug(f"未从历史缓存找到问题, 开始请求云端问题回答: {spec}.")
                    result, by = await Link(self.client).answer(key[0] + "\n" + key[1])
                    if result:
                        self.log.info(f"请求 {by or '云端'} 问题回答为{result}: {spec}.")
                        break
                    else:
                        self.log.info(f"云端问题回答错误或超时, 正在重试: {spec}.")
                else:
                    self.log.info(f"错误次数超限, 回答失败: {spec}.")
                    return
            try:
                await asyncio.sleep(random.uniform(2, 4))
                answer = await message.click(self.key_map[result])
                self.log.debug(f"回答返回值: {answer.message} {spec}.")
            except KeyError:
                self.log.info(f"点击失败: {result} 不是可用的答案 {spec}.")
            except RPCError:
                self.log.info(f"点击失败: 问题已失效.")
