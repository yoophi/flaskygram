# -*- coding: utf-8 -*-
from flask import jsonify, request

from flaskygram.core.api_1_0 import api
from flaskygram.core.api_1_0.response import api_response
from flaskygram.core.api_1_0.schema import user_schema
from flaskygram.extensions import oauth


@api.route('/users/<user_id>')
def user_get(user_id):
    """
    Get basic information about a user.
    ---
    parameters:
      - $ref: '#/parameters/user_id'
    security:
      - oauth:
        - email
    tags:
      - Users
    responses:
      200:
        description: The user object
        schema:
          type: object
          properties:
            data:
              $ref: '#/definitions/User'
    """
    return jsonify({})


@api.route('/users/self/feed')
@oauth.require_oauth('email')
def users_self_feed():
    """
    See the authenticated user's feed.
    ---
    tags:
      - Users
    parameters:
      - name: count
        in: query
        description: Count of media to return.
        type: integer
      - name: max_id
        in: query
        description: Return media earlier than this max_id.s
        type: integer
      - name: min_id
        in: query
        description: Return media later than this min_id.

        type: integer
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


@api.route('/users/<user_id>/media/recent')
def user_media_recent(user_id):
    """
    Get the most recent media published by a user.
    ---
    parameters:
      - $ref: '#/parameters/user_id'
    tags:
      - Users
    responses:
      200:
        description: |
          Get the most recent media published by a user. To get the most recent
          media published by the owner of the access token, you can use `self`
          instead of the `user_id`.
        schema:
          type: object
          properties:
            data:
              type: array
              items:
                $ref: '#/definitions/Media'
    parameters:
      - name: count
        in: query
        description: Count of media to return.
        type: integer
      - name: max_timestamp
        in: query
        description: Return media before this UNIX timestamp.
        type: integer
      - name: min_timestamp
        in: query
        description: Return media after this UNIX timestamp.
        type: integer
      - name: min_id
        in: query
        description: Return media later than this min_id.
        type: string
      - name: max_id
        in: query
        description: Return media earlier than this max_id.
        type: string
    """
    return jsonify({})


@api.route('/users/self/media/liked')
def users_self_media_liked():
    """
    See the list of media liked by the authenticated user.
    ---
    tags:
      - Users
    description: |
      See the list of media liked by the authenticated user.
      Private media is returned as long as the authenticated user
      has permissionto view that media. Liked media lists are only
      available for the currently authenticated user.
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
    parameters:
      - name: count
        in: query
        description: Count of media to return.
        type: integer
      - name: max_like_id
        in: query
        description: Return media liked before this id.
        type: integer
    """
    return jsonify({})


@api.route('/users/search')
def users_search():
    """
    Search for a user by name.
    ---
    tags:
      - Users
    description: Search for a user by name.
    parameters:
      - name: q
        in: query
        description: A query string
        type: string
        required: true
      - name: count
        in: query
        description: Number of users to return.
        type: string
    responses:
      200:
        description: OK
        schema:
          type: object
          properties:
            data:
              type: array
              items:
                $ref: '#/definitions/MiniProfile'
    """
    return jsonify({})


@api.route('/users/<user_id>/follows')
def user_follows(user_id):
    """
    Get the list of users this user follows.
    ---
    parameters:
      - $ref: '#/parameters/user_id'
    tags:
      - Relationships
    responses:
      200:
        description: OK
        schema:
          properties:
            data:
              type: array
              items:
                $ref: '#/definitions/MiniProfile'
    """
    return jsonify({})


@api.route('/users/<user_id>/followed-by')
def user_followed_by(user_id):
    """
    Get the list of users this user is followed by.
    ---
    parameters:
      - $ref: '#/parameters/user_id'
    tags:
      - Relationships
    responses:
      200:
        description: OK
        schema:
          properties:
            data:
              type: array
              items:
                $ref: '#/definitions/MiniProfile'
    """
    return jsonify({})


@api.route('/users/self/requested-by')
def users_self_requested_by():
    """
    List the users who have requested this user's permission to follow.
    ---
    tags:
      - Relationships
    responses:
      200:
        description: OK
        schema:
          properties:
            meta:
              properties:
                code:
                  type: integer
            data:
              type: array
              items:
                $ref: '#/definitions/MiniProfile'
    """
    return jsonify({})


@api.route('/users/<user_id>/relationship', methods=['POST'])
def user_relationship(user_id):
    """
    Modify the relationship between the current user and thetarget user.
    ---
    parameters:
      - $ref: '#/parameters/user_id'
    tags:
      - Relationships
    security:
      - oauth:
        - email
    parameters:
      - name: action
        in: body
        description: One of follow/unfollow/block/unblock/approve/ignore.
        schema:
          type: string
          enum:
            - follow
            - unfollow
            - block
            - unblock
            - approve
    responses:
      200:
        description: OK
        schema:
          properties:
            data:
              type: array
              items:
                $ref: '#/definitions/MiniProfile'
    """
    return jsonify({})


@api.route('/users/self')
@oauth.require_oauth('email')
def users_self():
    """
    현재 사용자의 정보 가져오기
    ---
    tags:
      - Users
    parameters: []
    responses:
      '200':
        description: successful operation
        schema:
          $ref: '#/definitions/User'
    security:
      - oauth:
          - email
    """

    user = request.oauth.user

    return api_response(user_schema.dump(user).data)


@api.route('/users', methods=['POST'])
def user_create():
    """
    회원 가입하기
    ---
    tags:
      - Users
    responses:
      '200':
        description: 회원가입 성공
        schema:
          $ref: '#/definitions/User'
    :return:
    """
    pass