from jinja2 import escape, Undefined, contextfunction
from starlette.templating import Jinja2Templates
import typing

from .db import cache


def render_ql_nickname(nickname):
    nickname = str(escape(nickname))
    for i in range(8):
        nickname = nickname.replace("^" + str(i), '</span><span class="qc' + str(i) + '">')
    return '<span class="qc7">' + nickname + '</span>';


def seconds_to_mmss(value):
    seconds = int(escape(value))
    m, s = divmod(seconds, 60)
    return "%02d:%02d" % (m, s)


class Templates(Jinja2Templates):
    def __init__(self, directory: str) -> None:
        @contextfunction
        def url_for(context: dict, name: str, **path_params: typing.Any) -> str:
            request = context["request"]
            path_params = {k: v for k, v in path_params.items() if not isinstance(v, Undefined)}
            return request.url_for(name, **path_params)

        super().__init__(directory)
        self.env.filters['ql_nickname'] = render_ql_nickname
        self.env.filters['seconds_to_mmss'] = seconds_to_mmss
        self.env.globals['gametype_names'] = cache.GAMETYPE_NAMES
        self.env.globals['url_for'] = url_for


templates = Templates(directory='templates')
