# -*- coding: utf8 -*-
import inspect
import os
import json
from urlparse import urlparse
import yaml
from flask import render_template, jsonify, current_app, url_for
from flask.ext.cors import cross_origin
from flask.ext.swagger import swagger
from . import main


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@main.route('/spec')
@cross_origin()
def spec():
    """
    info:
      version: v1
      title: Flaskygram API
      description: |
        The first version of the Instagram API is an exciting step forward towards
        making it easier for users to have open access to their data. We created it
        so that you can surface the amazing content Instagram users share every
        second, in fun and innovative ways.

        Build something great!

        Once you've
        [registered your client](http://instagram.com/developer/register/) it's easy
        to start requesting data from Instagram.

        All endpoints are only accessible via https and are located at
        `api.instagram.com`. For instance: you can grab the most popular photos at
        the moment by accessing the following URL with your client ID
        (replace CLIENT-ID with your own):
        ```
          https://api.instagram.com/v1/media/popular?client_id=CLIENT-ID
        ```
        You're best off using an access_token for the authenticated user for each
        endpoint, though many endpoints don't require it.
        In some cases an access_token will give you more access to information, and
        in all cases, it means that you are operating under a per-access_token limit
        vs. the same limit for your single client_id.


        ## Limits
        Be nice. If you're sending too many requests too quickly, we'll send back a
        `503` error code (server unavailable).
        You are limited to 5000 requests per hour per `access_token` or `client_id`
        overall. Practically, this means you should (when possible) authenticate
        users so that limits are well outside the reach of a given user.

        ## Deleting Objects
        We do our best to have all our URLs be
        [RESTful](http://en.wikipedia.org/wiki/Representational_state_transfer).
        Every endpoint (URL) may support one of four different http verbs. GET
        requests fetch information about an object, POST requests create objects,
        PUT requests update objects, and finally DELETE requests will delete
        objects.

        Since many old browsers don't support PUT or DELETE, we've made it easy to
        fake PUTs and DELETEs. All you have to do is do a POST with _method=PUT or
        _method=DELETE as a parameter and we will treat it as if you used PUT or
        DELETE respectively.

        ## Structure

        ### The Envelope
        Every response is contained by an envelope. That is, each response has a
        predictable set of keys with which you can expect to interact:
        ```json
        {
            "meta": {
                "code": 200
            },
            "data": {
                ...
            },
            "pagination": {
                "next_url": "...",
                "next_max_id": "13872296"
            }
        }
        ```

        #### META
        The meta key is used to communicate extra information about the response to
        the developer. If all goes well, you'll only ever see a code key with value
        200. However, sometimes things go wrong, and in that case you might see a
        response like:
        ```json
        {
            "meta": {
                "error_type": "OAuthException",
                "code": 400,
                "error_message": "..."
            }
        }
        ```

        #### DATA
        The data key is the meat of the response. It may be a list or dictionary,
        but either way this is where you'll find the data you requested.
        #### PAGINATION
        Sometimes you just can't get enough. For this reason, we've provided a
        convenient way to access more data in any request for sequential data.
        Simply call the url in the next_url parameter and we'll respond with the
        next set of data.
        ```json
        {
            ...
            "pagination": {
                "next_url": "https://api.instagram.com/v1/tags/puppy/media/recent?access_token=fb2e77d.47a0479900504cb3ab4a1f626d174d2d&max_id=13872296",
                "next_max_id": "13872296"
            }
        }
        ```
        On views where pagination is present, we also support the "count" parameter.
        Simply set this to the number of items you'd like to receive. Note that the
        default values should be fine for most applications - but if you decide to
        increase this number there is a maximum value defined on each endpoint.

        ### JSONP
        If you're writing an AJAX application, and you'd like to wrap our response
        with a callback, all you have to do is specify a callback parameter with
        any API call:
        ```
        https://api.instagram.com/v1/tags/coffee/media/recent?access_token=fb2e77d.47a0479900504cb3ab4a1f626d174d2d&callback=callbackFunction
        ```
        Would respond with:
        ```js
        callbackFunction({
            ...
        });
        ```
      termsOfService: http://instagram.com/about/legal/terms/api

    ################################################################################
    #                  Host, Base Path, Schemes and Content Types                  #
    ################################################################################
    host: api.instagram.com
    basePath: /v1
    schemes:
      - https
    produces:
      - application/json
    consumes:
      - application/json

    ################################################################################
    #                                   Tags                                       #
    ################################################################################
    tags:
      - name: Users
      - name: Relationships
        description: |
          Relationships are expressed using the following terms:

          **outgoing_status**: Your relationship to the user. Can be "follows",
            "requested", "none".
          **incoming_status**: A user's relationship to you. Can be "followed_by",
            "requested_by", "blocked_by_you", "none".
      - name: Media
        description: |
          At this time, uploading via the API is not possible. We made a conscious
          choice not to add this for the following reasons:

          * Instagram is about your life on the go â€“ we hope to encourage photos
            from within the app.
          * We want to fight spam & low quality photos. Once we allow uploading
            from other sources, it's harder to control what comes into the Instagram
            ecosystem. All this being said, we're working on ways to ensure users
            have a consistent and high-quality experience on our platform.
      - name: Commnts
      - name: Likes
      - name: Tags
      - name: Location
      - name: Subscribtions

    ################################################################################
    #                                  Security                                    #
    ################################################################################
    securityDefinitions:
      oauth:
        type: oauth2
        flow: implicit
        authorizationUrl: https://instagram.com/oauth/authorize/?client_id=CLIENT-ID&redirect_uri=REDIRECT-URI&response_type=token
        scopes:
          basic: |
           to read any and all data related to a user (e.g. following/followed-by
            lists, photos, etc.) (granted by default)
          comments: to create or delete comments on a userâ€™s behalf
          relationships: to follow and unfollow users on a userâ€™s behalf
          likes: to like and unlike items on a userâ€™s behalf
      key:
        type: apiKey
        in: query
        name: access_token
    security:
      - oauth:
        - basic
        - comments
        - relationships
        - likes
      - key: []

    ################################################################################
    #                                   Parameters                                 #
    ################################################################################
    parameters:
      user_id:
        name: user_id
        in: path
        description: The user identifier number
        type: number
        required: true
      tag_name:
        name: tag_name
        in: path
        description: Tag name
        type: string
        required: true

    ################################################################################
    #                                 Definitions                                  #
    ################################################################################
    definitions:
      User:
        type: object
        properties:
          id:
            type: integer
          username:
            type: string
          full_name:
            type: string
          profile_picture:
            type: string
          bio:
            type: string
          website:
            type: string
          counts:
            type: object
            properties:
              media:
                type: integer
              follows:
                type: integer
              follwed_by:
                type: integer
      Media:
        type: object
        properties:
          created_time:
            description: Epoc time (ms)
            type: integer
          type:
            type: string
          filter:
            type: string
          tags:
            type: array
            items:
              $ref: '#/definitions/Tag'
          id:
            type: integer
          user:
            $ref: '#/definitions/MiniProfile'
          users_in_photo:
            type: array
            items:
              $ref: '#/definitions/MiniProfile'
          location:
            $ref: '#/definitions/Location'
          comments::
            type: object
            properties:
              count:
                type: integer
              data:
                type: array
                items:
                  $ref: '#/definitions/Comment'
          likes:
            type: object
            properties:
              count:
                type: integer
              data:
                type: array
                items:
                  $ref: '#/definitions/MiniProfile'
          images:
            properties:
              low_resolution:
                $ref: '#/definitions/Image'
              thumbnail:
                $ref: '#/definitions/Image'
              standard_resolution:
                $ref: '#/definitions/Image'
          videos:
            properties:
              low_resolution:
                $ref: '#/definitions/Image'
              standard_resolution:
                $ref: '#/definitions/Image'
      Location:
        type: object
        properties:
          id:
            type: string
          name:
            type: string
          latitude:
            type: number
          longitude:
            type: number
      Comment:
        type: object
        properties:
          id:
            type: string
          created_time:
            type: string
          text:
            type: string
          from:
            $ref: '#/definitions/MiniProfile'
      Like:
        type: object
        properties:
          user_name:
            type: string
          first_name:
            type: string
          last_name:
            type: string
          type:
            type: string
          id:
            type: string
      Tag:
        type: object
        properties:
          media_count:
            type: integer
          name:
            type: string
      Image:
        type: object
        properties:
          width:
            type: integer
          height:
            type: integer
          url:
            type: string
      MiniProfile:
        type: object
        description: A shorter version of User for likes array
        properties:
          user_name:
            type: string
          full_name:
            type: string
          id:
            type: integer
          profile_picture:
            type: string
    """
    swag = swagger(current_app)
    swag.update(yaml.load(inspect.getdoc(spec)))
    return jsonify(swag)


def get_netloc():
    parsed_url = urlparse(url_for('main.spec', _external=True))
    return parsed_url.netloc
