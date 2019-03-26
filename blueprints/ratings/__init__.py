# -*- coding: utf-8 -*-

from app import App
from starlette.responses import JSONResponse, PlainTextResponse
from starlette.requests import Request
from endpoints import Endpoint
from .methods import get_list
from templating import templates
from asyncpg import Connection

bp = App()


@bp.route("/{gametype}/{page:int}.json")
class RatingsJson(Endpoint):
    async def _get(self, request: Request, con: Connection):
        page = request.path_params.get("page", 0)
        gametype_id = request.path_params.get("gametype_id")
        return JSONResponse(await get_list(con, gametype_id, page))


@bp.route("/{gametype}/")
@bp.route("/{gametype}/{page:int}/")
class RatingsHtml(Endpoint):
    async def _get(self, request: Request, con: Connection):
        page = request.path_params.get("page", 0)
        gametype_id = request.path_params.get("gametype_id")
        show_inactive = request.query_params.get("show_inactive", False)
        if show_inactive:
            show_inactive = True

        context = await get_list(con, gametype_id, page, show_inactive)
        context['request'] = request
        context['current_page'] = page
        context['gametype'] = request.path_params['gametype']
        return templates.TemplateResponse("ratings_list.html", context)
