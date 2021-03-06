import cgi
import logging
import pathlib
import urllib.parse

from pathvalidate import sanitize_filename

from .typing import (ResourceId, Union)

LOGGER = logging.getLogger(__name__)


def extract_filename_from_headers(headers: dict) -> Union[None, str]:
    h = headers['content-disposition']

    _, parsed = cgi.parse_header(h)
    filename = parsed.get('filename*')
    if filename is not None:
        expected_encoding = "UTF-8''"
        if filename.startswith(expected_encoding):
            filename = filename.replace(expected_encoding, '')
            try:
                filename = urllib.parse.unquote(filename)
                sanitized_name = sanitize_filename(filename, platform='auto')
            except Exception as e:
                filename = None
                LOGGER.warning(
                    'Problem while extracting the filename from '
                    'the headers: {!r}'.format(e)
                )
        else:
            filename = None

    if filename is None:
        filename = parsed.get('filename')
        sanitized_name = sanitize_filename(filename, platform='auto')

    return sanitized_name


def generate_raster_tiles_url(base_url: str,
                              access_token: str,
                              dataset: ResourceId,
                              tile_format: str) -> str:
    """Returns the URL template to share raster tiles.

    Args:
        base_url: URL of the platform.

        access_token: Share token for ``dataset``.

        dataset: Identifier of the dataset to create a URL for.

        tile_format: Format of tiles.

    """
    scheme, netloc, _, _, _, _ = urllib.parse.urlparse(base_url)
    query = 'access_token={}'.format(access_token)
    service = 'tileserver/tiles'
    tile = '{z}/{x}/{y}.' + tile_format
    path_template = '{service}/{dataset}/{tile}'
    path = path_template.format(service=service, dataset=dataset, tile=tile)

    url = urllib.parse.urlunparse((scheme, netloc, path, '', query, ''))
    return url


def generate_vector_tiles_url(base_url: str,
                              access_token: str,
                              collection: ResourceId,
                              tile_format: str) -> str:
    """Returns the URL template to share vector tiles.

    Args:
        base_url: URL of the platform.

        access_token: Share token for ``collection`` dataset.

        collection: Identifier of the dataset to create a URL for.

        tile_format: Format of tiles.

    """
    scheme, netloc, _, _, _, _ = urllib.parse.urlparse(base_url)
    query = 'access_token={}'.format(access_token)
    service = 'map-service/features/collection-mvt'
    tile = '{z}/{x}/{y}.' + tile_format
    path_template = '{service}/{collection}/{tile}'
    path = path_template.format(service=service, collection=collection,
                                tile=tile)

    url = urllib.parse.urlunparse((scheme, netloc, path, '', query, ''))
    return url
