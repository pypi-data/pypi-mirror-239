from __future__ import annotations
import json

from .utils.utils import backslash2slash, get_fmt, async_subprocess_exec


class Media:
    def __init__(self, input_path: str):
        self.input_path = backslash2slash(input_path)
        self.fmt = get_fmt(self.input_path)

    async def get_info(self) -> dict:
        """
        查看媒体信息
        :return: 媒体详细信息
        """
        cmd = r'ffprobe -i {} -v error -show_format -show_streams -print_format json'
        res = await async_subprocess_exec(cmd, self.input_path)
        return json.loads(res)
