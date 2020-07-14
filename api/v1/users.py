from urllib.parse import parse_qs

from flask import make_response, redirect, request
from flask_mico import ApiView
from flask_mico.conf import settings
from flask_mico.error import AuthenticationRequiredError, InvalidParameterError

from core.common.request import requests
from core.models.user import User


class LoginApiView(ApiView):

    def get(self):
        gh_code = request.args.get("code", None)
        if gh_code is None:
            raise InvalidParameterError()
        _resp = requests.post("https://github.com/login/oauth/access_token",
                              json={"client_id": settings.GH_CLIENT_ID,
                                    "client_secret": settings.GH_CLIENT_SECRET,
                                    "code": gh_code})
        _data = parse_qs(_resp.text)
        access_token = _data["access_token"][0]
        _resp = requests.get(
            "https://api.github.com/user?access_token=" + access_token)
        user_infos = _resp.json()
        if not(user_infos and user_infos.get("login", None)):
            raise AuthenticationRequiredError()

        response = make_response(redirect(settings.FRONT_HOST))
        username, avatar_url = User.create_gh_user(user_infos)
        response.set_cookie("username", username)
        response.set_cookie("avatarUrl", avatar_url)
        return response
