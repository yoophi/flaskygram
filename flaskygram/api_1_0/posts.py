# -*- coding: utf8 -*-
import json

from flask import request
from voluptuous import Schema, Any, MultipleInvalid

from . import api
from .response import api_response, error_response
from .schema import post_schema
from .. import oauth
from ..models import db, Media, Post


@api.route('/posts', methods=['POST'])
@oauth.require_oauth('email')
def post_create():
    """
    새로운 포스트 작성
    ---
    parameters:
      - name: body
        in: body
        schema:
          type: object
          required:
            - media_id
            - text
          properties:
            media_id:
              type: integer
            text:
              type: string

    produces:
      - application/json
    tags:
      - Post
    responses:
      200:
        description: OK
        schema:
          $ref: '#/definitions/Post'
    """
    payload = json.loads(request.data)

    schema = Schema({
        'media_id': int,
        'text': Any(str, unicode)
    })
    try:
        schema(payload)
        media_id = payload.get('media_id')
        text = payload.get('text')
    except MultipleInvalid:
        return error_response()

    current_user_id = request.oauth.user.id

    m = Media.query.get(media_id)

    # media.post_id == NULL 이고 media 의 소유자는 현재 사용자여야 함
    if m.post_id is not None:
        return error_response(status_code=400, message="이미 등록된 미디어 파일입니다")

    if m.user_id != current_user_id:
        return error_response(status_code=400, message="본인의 미디어 파일만 첨부 가능합니다")

    post = Post(text=text, user_id=current_user_id)
    post.media.append(m)

    db.session.add(post)
    db.session.commit()

    return api_response(post_schema.dump(post).data)


def post_update():
    pass


def post_delete():
    pass


def post_get():
    pass
