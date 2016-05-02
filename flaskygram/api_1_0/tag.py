from flask import jsonify

from . import api


@api.route('/tags/<tag_name>')
def tags_tag_name(tag_name):
    """
    Get information about a tag object.
    ---
    parameters:
      - $ref: '#/parameters/tag_name'
    tags:
      - Tags
    description: Get information about a tag object.
    responses:
      200:
        description: OK
        schema:
          $ref: '#/definitions/Tag'
    """
    return jsonify({})


@api.route('/tags/<tag_name>/media/recent')
def tags_tag_name_media_recent(tag_name):
    """
    Get a list of recently tagged media.
    ---
    parameters:
      - $ref: '#/parameters/tag_name'
    tags:
      - Tags
    description: |
      Get a list of recently tagged media. Use the `max_tag_id` and
      `min_tag_id` parameters in the pagination response to paginate through
      these objects.
    responses:
      200:
        description: OK
        schema:
          properties:
            data:
              type: array
              items:
                $ref: '#/definitions/Tag'
    """
    return jsonify({})


@api.route('/tags/search')
def tags_search():
    """
    Search tags.
    ---
    tags:
      - Tags
    parameters:
      - name: q
        description: |
          A valid tag name without a leading #. (eg. snowy, nofilter)
        in: query
        type: string
    responses:
      200:
        description: OK
        schema:
          type: object
          properties:
            meta:
              properties:
                code:
                  type: integer
            data:
              type: array
              items:
                $ref: '#/definitions/Tag'
    """
    return jsonify({})


