# -*- coding: utf8 -*-
import os
from datetime import datetime
from io import BytesIO
from os import path

import shortuuid
from flask import current_app, jsonify, request, send_from_directory, abort
from flask.views import MethodView
from s3_saver import S3Saver
from werkzeug.utils import secure_filename

from flaskygram.core.api_1_0 import api
from flaskygram.core.api_1_0.response import error_response, api_response
from flaskygram.core.api_1_0.schema import media_schema, media_items_schema
from flaskygram.database import db
from flaskygram.extensions import oauth
from flaskygram.library.get_setting_value import get_setting_value
from flaskygram.modules.media.models import Media


@api.route('/media/upload1', methods=['POST'])
@oauth.require_oauth('email')
def media_upload1():
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

    def prefix_file_utcnow2(model, file_data):
        parts = path.splitext(file_data.filename)
        return secure_filename('%s%s' % (datetime.utcnow().strftime('%Y-%m-%d-%H-%M-%S'), parts[1]))

    media = Media()
    media.user_id = request.oauth.user.id

    upload_file = request.files.get('file')
    if upload_file and allowed_file(upload_file.filename):
        # Initialise s3-saver.
        image_saver = S3Saver(
            storage_type=get_setting_value('USE_S3') and 's3' or None,
            bucket_name=get_setting_value('S3_BUCKET_NAME'),
            access_key_id=get_setting_value('AWS_ACCESS_KEY_ID'),
            access_key_secret=get_setting_value('AWS_SECRET_ACCESS_KEY'),
            field_name='image',
            storage_type_field='image_storage_type',
            bucket_name_field='image_storage_bucket_name',
            base_path=get_setting_value('UPLOADS_FOLDER'),
            static_root_parent=path.abspath(get_setting_value('PROJECT_ROOT')))

        current_app.logger.info(upload_file)

        if upload_file.filename:
            filename = prefix_file_utcnow2(media, upload_file)

            # Best to pass in a BytesIO to S3Saver, containing the
            # contents of the file to save. A file from any source
            # (e.g. in a Flask form submission, a
            # werkzeug.datastructures.FileStorage object; or if
            # reading in a local file in a shell script, perhaps a
            # Python file object) can be easily converted to BytesIO.
            # This way, S3Saver isn't coupled to a Werkzeug POST
            # request or to anything else. It just wants the file.
            temp_file = BytesIO()
            upload_file.save(temp_file)

            # Save the file. Depending on how S3Saver was initialised,
            # could get saved to local filesystem or to S3.
            image_saver.save(
                temp_file,
                get_setting_value('THINGY_IMAGE_RELATIVE_PATH') + filename,
                media)

            db.session.add(media)
            db.session.commit()
            current_app.logger.info('Thingy saved success')

        return api_response(media_schema.dump(media).data)

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
