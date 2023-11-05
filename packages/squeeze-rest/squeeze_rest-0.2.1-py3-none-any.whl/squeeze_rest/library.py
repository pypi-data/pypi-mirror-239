from flask import Blueprint, request, current_app
import squeeze_jrpc.queries

from squeeze_rest.player import track_from_jrpc

bp = Blueprint('library', __name__, url_prefix='/library')


@bp.route('/artists')
def artists_search():
    return squeeze_jrpc.queries.artists(
            server(), sanitise_query_params(request.args))


@bp.route('/artists/<int:id>')
def get_artist(id):
    artists = squeeze_jrpc.queries.artists(server(), {'artist_id': id})
    try:
        return artists[0]
    except KeyError:
        return '', 404


@bp.route('/tracks')
def tracks_search():
    return [track_from_jrpc(track) for track in squeeze_jrpc.queries.tracks(
            server(), sanitise_query_params(request.args))]


@bp.route('/albums')
def albums_search():
    return squeeze_jrpc.queries.albums(
            server(), sanitise_query_params(request.args))


@bp.route('/albums/<int:id>')
def get_album(id):
    albums = squeeze_jrpc.queries.albums(server(), {'album_id': id})
    try:
        return albums[0]
    except KeyError:
        return '', 404


def server():
    return (current_app.config['LMS_HOST'], current_app.config['LMS_PORT'])


def sanitise_query_params(params):
    return {k: v for k, v in params.items()
            if k in ['search', 'track_id', 'album_id', 'artist_id', 'sort']}
