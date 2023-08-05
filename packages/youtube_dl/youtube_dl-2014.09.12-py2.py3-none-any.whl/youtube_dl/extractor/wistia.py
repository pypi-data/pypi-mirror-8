from __future__ import unicode_literals

import json
import re

from .common import InfoExtractor


class WistiaIE(InfoExtractor):
    _VALID_URL = r'https?://(?:fast\.)?wistia\.net/embed/iframe/(?P<id>[a-z0-9]+)'

    _TEST = {
        'url': 'http://fast.wistia.net/embed/iframe/sh7fpupwlt',
        'md5': 'cafeb56ec0c53c18c97405eecb3133df',
        'info_dict': {
            'id': 'sh7fpupwlt',
            'ext': 'mov',
            'title': 'Being Resourceful',
            'duration': 117,
        },
    }

    def _real_extract(self, url):
        mobj = re.match(self._VALID_URL, url)
        video_id = mobj.group('id')

        webpage = self._download_webpage(url, video_id)
        data_json = self._html_search_regex(
            r'Wistia\.iframeInit\((.*?), {}\);', webpage, 'video data')

        data = json.loads(data_json)

        formats = []
        thumbnails = []
        for atype, a in data['assets'].items():
            if atype == 'still':
                thumbnails.append({
                    'url': a['url'],
                    'resolution': '%dx%d' % (a['width'], a['height']),
                })
                continue
            if atype == 'preview':
                continue
            formats.append({
                'format_id': atype,
                'url': a['url'],
                'width': a['width'],
                'height': a['height'],
                'filesize': a['size'],
                'ext': a['ext'],
                'preference': 1 if atype == 'original' else None,
            })

        self._sort_formats(formats)

        return {
            'id': video_id,
            'title': data['name'],
            'formats': formats,
            'thumbnails': thumbnails,
            'duration': data.get('duration'),
        }
