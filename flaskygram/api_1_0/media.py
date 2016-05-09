from flask import jsonify, request
from flask.views import MethodView
from . import api


@api.route('/media/upload', methods=['POST'])
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
    return jsonify({'method': request.method,
                    'filename': request.files['file'].filename})


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
    return jsonify({})


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
    return jsonify({})


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


class MediaCommentApi(MethodView):
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
              - comments
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
              - comments
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


api.add_url_rule('/media/<media_id>/comments', view_func=MediaCommentApi.as_view('media_comment'))
api.add_url_rule('/media/<media_id>/likes', view_func=MediaLikeApi.as_view('media_like'))
