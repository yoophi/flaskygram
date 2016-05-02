from flask import jsonify
from . import api


@api.route('/locations/<location_id>')
def locations_location_id(location_id):
    """
    Get information about a location.
    ---
    parameters:
      - name: location_id
        description: Location ID
        in: path
        type: integer
        required: true
    tags:
      - Location
    description: Get information about a location.
    responses:
      200:
        description: OK
        schema:
          type: object
          properties:
            data:
              $ref: '#/definitions/Location'
    """
    return jsonify({})


@api.route('/locations/<location_id>/media/recent')
def locations_location_id_media_recent(location_id):
    """
    Get a list of recent media objects from a given location.
    ---
    parameters:
      - name: location_id
        description: Location ID
        in: path
        type: integer
        required: true
    tags:
      - Location
      - Media
    description: Get a list of recent media objects from a given location.
    parameters:
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


@api.route('/locations/search')
def locations_search():
    """
    tags:
      - Location
    description: Search for a location by geographic coordinate.
    parameters:
      - name: distance
        in: query
        description: Default is 1000m (distance=1000), max distance is 5000.
        type: integer

      - name: facebook_places_id
        in: query
        description: |
          Returns a location mapped off of a Facebook places id. If used, a
          Foursquare id and lat, lng are not required.
        type: integer

      - name: foursquare_id
        in: query
        description: |
          returns a location mapped off of a foursquare v1 api location id.
          If used, you are not required to use lat and lng. Note that this
          method is deprecated; you should use the new foursquare IDs with V2
          of their API.
        type: integer

      - name: lat
        in: query
        description: |
          atitude of the center search coordinate. If used, lng is required.
        type: number

      - name: lng
        in: query
        description: |
          ongitude of the center search coordinate. If used, lat is required.
        type: number

      - name: foursquare_v2_id
        in: query
        description: |
          Returns a location mapped off of a foursquare v2 api location id. If
          used, you are not required to use lat and lng.
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
                $ref: '#/definitions/Location'
    """
    return jsonify({})


@api.route('/geographies/<geo_id>/media/recent')
def geographies_geo_id_media_recent():
    """
    Get recent media from a geography subscription that you created.
    ---
    parameters:
      - name: geo_id
        in: path
        description: Geolocation ID
        type: integer
        required: true
    description: |
      Get recent media from a geography subscription that you created.
      **Note**: You can only access Geographies that were explicitly created
      by your OAuth client. Check the Geography Subscriptions section of the
      [real-time updates page](https://instagram.com/developer/realtime/).
      When you create a subscription to some geography
      that you define, you will be returned a unique geo_id that can be used
      in this query. To backfill photos from the location covered by this
      geography, use the [media search endpoint
      ](https://instagram.com/developer/endpoints/media/).
    parameters:
      - name: count
        in: query
        description: Max number of media to return.
        type: integer
      - name: min_id
        in: query
        description: Return media before this `min_id`.
        type: integer
    responses:
      200:
        description: OK
    tags:
      - Location
    """
    return jsonify({})
