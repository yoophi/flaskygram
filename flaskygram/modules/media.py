# -*- coding: utf8 -*-
import os

import shortuuid
from flask import current_app, jsonify, request, send_from_directory, abort
from flask.views import MethodView
from werkzeug.utils import secure_filename

from . import api
from .. import oauth
from ..api_1_0.response import error_response, api_response
from ..api_1_0.schema import media_schema, media_items_schema
from ..models import Media
from flaskygram.database import db


@api.route('/media/upload', methods=['POST'])
@oauth.require_oauth('email')
def media_upload():
    """
    Upload file
    ---
    consumes:
      - multipart/form-data
    parameters:
      - name: file
        in: formData
        description: The file to upload
        type: file
        required: true
    produces:
      - application/json
    tags:
      - Media
    description: |
      Get information about a media object.
      The returned type key will allow you to differentiate between `image`
      and `video` media.

      Note: if you authenticate with an OAuth Token, you will receive the
      `user_has_liked` key which quickly tells you whether the current user
      has liked this media item.
    responses:
      200:
        description: OK
        schema:
          $ref: '#/definitions/Media'
    """

    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1] in current_app.config['ALLOWED_EXTENSIONS']

    upload_file = request.files['file']
    if upload_file and allowed_file(upload_file.filename):
        shortcode = shortuuid.uuid()
        ext = upload_file.filename.split('.').pop()
        target_filename = '.'.join([secure_filename(shortcode), ext])
        target_path = os.path.join(current_app.config['UPLOAD_FOLDER'], target_filename)
        upload_file.save(target_path)
        filesize = get_filesize(target_path)

        m = Media(user_id=request.oauth.user.id,
                  name=upload_file.filename,
                  filename=target_filename,
                  filesize=filesize,
                  mimetype=upload_file.mimetype,
                  shortcode=shortcode,
                  dir=current_app.config['UPLOAD_FOLDER'])

        db.session.add(m)
        db.session.commit()

        # return jsonify(media_schema.load(media).data)
        return api_response(media_schema.dump(m).data)

    return error_response(status_code=400)


@api.route('/media/draft', methods=['GET'])
@oauth.require_oauth('email')
def media_draft():
    """
    아직 Post 로 작성되지 않은 Media 들을 보며준다
    ---
    parameters: []
    tags:
      - Media
    responses:
      200:
        description: OK
        schema:
          type: array
          items:
            $ref: '#/definitions/Media'
    security:
      - oauth:
        - email
    """
    user = request.oauth.user
    m_items = Media.query.filter(Media.user_id == user.id).order_by(Media.id.desc())
    return api_response(media_items_schema.dump(m_items).data)


def get_filesize(target_path):
    return os.stat(target_path).st_size


@api.route('/media/<int:media_id>', methods=['GET'])
def media_media_id(media_id):
    """
    Get information about a media object.
    ---
    parameters:
      - name: media_id
        in: path
        description: The media ID
        type: integer
        required: true
    tags:
      - Media
    description: |
      Get information about a media object.
      The returned type key will allow you to differentiate between `image`
      and `video` media.

      Note: if you authenticate with an OAuth Token, you will receive the
      `user_has_liked` key which quickly tells you whether the current user
      has liked this media item.
    responses:
      200:
        description: OK
        schema:
          $ref: '#/definitions/Media'
    """
    media = Media.query.get_or_404(media_id)
    return api_response(media_schema.dump(media).data)


@api.route('/media1/<shortcode>')
def media1_shortcode(shortcode):
    """
    This endpoint returns the same response as **GET** `/media/media_id`.
    ---
    parameters:
      - name: shortcode
        in: path
        description: The media shortcode
        type: string
        required: true
    tags:
      - Media
    description: |
      This endpoint returns the same response as **GET** `/media/media_id`.

      A media object's shortcode can be found in its shortlink URL.
      An example shortlink is `http://instagram.com/p/D/`
      Its corresponding shortcode is D.

    responses:
      200:
        description: OK
        schema:
          $ref: '#/definitions/Media'
    """
    media = Media.query.filter(Media.shortcode == shortcode).first()
    if not media:
        abort(404)

    return api_response(media_schema.dump(media).data)


@api.route('/media/search')
def media_search():
    """
    Search for media in a given area.
    ---
    tags:
      - Media
    description: |
      Search for media in a given area. The default time span is set to 5
      days. The time span must not exceed 7 days. Defaults time stamps cover
      the last 5 days. Can return mix of image and video types.

    parameters:
      - name: LAT
        description: |
          Latitude of the center search coordinate. If used, lng is required.
        type: number
        in: query
      - name: MIN_TIMESTAMP
        description: |
          A unix timestamp. All media returned will be taken later than
          this timestamp.
        type: integer
        in: query
      - name: LNG
        description: |
          Longitude of the center search coordinate. If used, lat is required.
        type: number
        in: query
      - name: MAX_TIMESTAMP
        description: |
          A unix timestamp. All media returned will be taken earlier than this
          timestamp.
        type: integer
        in: query
      - name: DISTANCE
        description:  Default is 1km (distance=1000), max distance is 5km.
        type: integer
        maximum: 5000
        default: 1000
        in: query
    responses:
      200:
        description: OK
        schema:
          type: object
          description: List of all media with added `distance` property
          properties:
            data:
              type: array
              items:
                allOf:
                  - $ref: '#/definitions/Media'
                  -
                    properties:
                      distance:
                        type: number
    """
    return jsonify({})


@api.route('/media/popular')
def media_popular():
    """
    Get a list of what media is most popular at the moment.
    ---
    tags:
      - Media
    description: |
      Get a list of what media is most popular at the moment.
      Can return mix of image and video types.
    responses:
      200:
        description: OK
        schema:
          type: object
          properties:
            data:
              type: array
              items:
                $ref: '#/definitions/Media'
    """
    return jsonify({})


class PostCommentApi(MethodView):
    def get(self, media_id):
        """
        Get a list of recent comments on a media object.
        ---
        parameters:
          - name: media_id
            in: path
            description: Media ID
            type: integer
            required: true
        tags:
          - Comments
        description: |
          Get a list of recent comments on a media object.
        responses:
          200:
            description: OK
            schema:
              properties:
                meta:
                  properties:
                    code:
                      type: number
                data:
                  type: array
                  items:
                    $ref: '#/definitions/Comment'
        """
        return jsonify({})

    def post(self, media_id):
        """
        Create a comment on a media object with the following rules:
        ---
        parameters:
          - name: media_id
            in: path
            description: Media ID
            type: integer
            required: true
          - name: TEXT
            description: |
              Text to post as a comment on the media object as specified in
              media_id.
            in: body
            schema:
              type: number
        tags:
          - Comments
          - Media
        description: |
          Create a comment on a media object with the following rules:

          * The total length of the comment cannot exceed 300 characters.
          * The comment cannot contain more than 4 hashtags.
          * The comment cannot contain more than 1 URL.
          * The comment cannot consist of all capital letters.
        security:
          - oauth:
              - email
        responses:
          200:
            description: OK
            schema:
              type: object
              properties:
                meta:
                  properties:
                    code:
                      type: number
                data:
                  type: object
        """
        return jsonify({})

    def delete(self, media_id):
        """
        Remove a comment either on the authenticated user's media object or
        ---
        parameters:
          - name: media_id
            in: path
            description: Media ID
            type: integer
            required: true
        tags:
          - Comments
        description: |
          Remove a comment either on the authenticated user's media object or
          authored by the authenticated user.
        responses:
          200:
            description: OK
            schema:
              type: object
              properties:
                meta:
                  properties:
                    code:
                      type: number
                data:
                  type: object
        """
        return jsonify({})


class MediaLikeApi(MethodView):
    def get(self, media_id):
        """
        Get a list of users who have liked this media.
        ---
        parameters:
          - name: media_id
            in: path
            description: Media ID
            type: integer
            required: true
        tags:
          - Likes
          - Media
        responses:
          200:
            description: OK
            schema:
              properties:
                meta:
                  properties:
                    code:
                      type: number
                data:
                  type: array
                  items:
                    $ref: '#/definitions/Like'
        """
        return jsonify({})

    def post(self, media_id):
        """
        Set a like on this media by the currently authenticated user.
        ---
        parameters:
          - name: media_id
            in: path
            description: Media ID
            type: integer
            required: true
        tags:
          - Likes
        security:
          - oauth:
              - email
        responses:
          200:
            description: OK
            schema:
              type: object
              properties:
                meta:
                  properties:
                    code:
                      type: number
                data:
                  type: object
        """
        return jsonify({})

    def delete(self, media_id):
        """
        Remove a like on this media by the currently authenticated user.
        ---
        parameters:
          - name: media_id
            in: path
            description: Media ID
            type: integer
            required: true
        tags:
          - Likes
        responses:
          200:
            description: OK
            schema:
              type: object
              properties:
                meta:
                  properties:
                    code:
                      type: number
                data:
                  type: object
        """
        return jsonify({})


@api.route('/m/<shortcode>')
def media_file(shortcode):
    """
    shortcode 에 해당하는 미디어 파일을 전송한다.
    ---
    parameters:
      - name: shortcode
        in: path
        description: The media shortcode
        type: string
        required: true
    tags:
      - Media
    responses:
      200:
        description: OK
        schema:
          type: file
    """
    media = Media.query.filter(Media.shortcode == shortcode).first()
    if not media:
        abort(404)

    return send_from_directory(media.dir, media.filename)


api.add_url_rule('/media/<media_id>/comments', view_func=PostCommentApi.as_view('media_comment'))
api.add_url_rule('/media/<media_id>/likes', view_func=MediaLikeApi.as_view('media_like'))
