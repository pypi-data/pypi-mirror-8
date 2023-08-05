# encoding: utf-8
from __future__ import unicode_literals

import re

from .common import InfoExtractor
from ..utils import (
    compat_urllib_request,
    compat_urllib_parse,
    ExtractorError,
    clean_html,
    unified_strdate,
    compat_str,
)


class NocoIE(InfoExtractor):
    _VALID_URL = r'http://(?:(?:www\.)?noco\.tv/emission/|player\.noco\.tv/\?idvideo=)(?P<id>\d+)'
    _LOGIN_URL = 'http://noco.tv/do.php'
    _NETRC_MACHINE = 'noco'

    _TEST = {
        'url': 'http://noco.tv/emission/11538/nolife/ami-ami-idol-hello-france/',
        'md5': '0a993f0058ddbcd902630b2047ef710e',
        'info_dict': {
            'id': '11538',
            'ext': 'mp4',
            'title': 'Ami Ami Idol - Hello! France',
            'description': 'md5:4eaab46ab68fa4197a317a88a53d3b86',
            'upload_date': '20140412',
            'uploader': 'Nolife',
            'uploader_id': 'NOL',
            'duration': 2851.2,
        },
        'skip': 'Requires noco account',
    }

    def _real_initialize(self):
        self._login()

    def _login(self):
        (username, password) = self._get_login_info()
        if username is None:
            return

        login_form = {
            'a': 'login',
            'cookie': '1',
            'username': username,
            'password': password,
        }
        request = compat_urllib_request.Request(self._LOGIN_URL, compat_urllib_parse.urlencode(login_form))
        request.add_header('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')

        login = self._download_json(request, None, 'Logging in as %s' % username)

        if 'erreur' in login:
            raise  ExtractorError('Unable to login: %s' % clean_html(login['erreur']), expected=True)

    def _real_extract(self, url):
        mobj = re.match(self._VALID_URL, url)
        video_id = mobj.group('id')

        medias = self._download_json(
            'https://api.noco.tv/1.0/video/medias/%s' % video_id, video_id, 'Downloading video JSON')

        formats = []

        for fmt in medias['fr']['video_list']['default']['quality_list']:
            format_id = fmt['quality_key']

            file = self._download_json(
                'https://api.noco.tv/1.0/video/file/%s/fr/%s' % (format_id.lower(), video_id),
                video_id, 'Downloading %s video JSON' % format_id)

            file_url = file['file']
            if not file_url:
                continue

            if file_url == 'forbidden':
                raise ExtractorError(
                    '%s returned error: %s - %s' % (
                        self.IE_NAME, file['popmessage']['title'], file['popmessage']['message']),
                    expected=True)

            formats.append({
                'url': file_url,
                'format_id': format_id,
                'width': fmt['res_width'],
                'height': fmt['res_lines'],
                'abr': fmt['audiobitrate'],
                'vbr': fmt['videobitrate'],
                'filesize': fmt['filesize'],
                'format_note': fmt['quality_name'],
                'preference': fmt['priority'],
            })

        self._sort_formats(formats)

        show = self._download_json(
            'https://api.noco.tv/1.0/shows/show/%s' % video_id, video_id, 'Downloading show JSON')[0]

        upload_date = unified_strdate(show['indexed'])
        uploader = show['partner_name']
        uploader_id = show['partner_key']
        duration = show['duration_ms'] / 1000.0
        thumbnail = show['screenshot']

        episode = show.get('show_TT') or show.get('show_OT')
        family = show.get('family_TT') or show.get('family_OT')
        episode_number = show.get('episode_number')

        title = ''
        if family:
            title += family
        if episode_number:
            title += ' #' + compat_str(episode_number)
        if episode:
            title += ' - ' + episode

        description = show.get('show_resume') or show.get('family_resume')

        return {
            'id': video_id,
            'title': title,
            'description': description,
            'thumbnail': thumbnail,
            'upload_date': upload_date,
            'uploader': uploader,
            'uploader_id': uploader_id,
            'duration': duration,
            'formats': formats,
        }