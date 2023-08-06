"""Low-level MediaFire API Client"""

from __future__ import unicode_literals

import hashlib
import requests
import logging

import six

from six.moves.urllib.parse import urlencode

from requests_toolbelt import MultipartEncoder
from requests.adapters import HTTPAdapter

API_BASE = 'https://www.mediafire.com'
API_VER = '1.1'

# Retries on connection errors/timeouts
API_ERROR_MAX_RETRIES = 5

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name

# Each API call may have lots of parameters, so disable warning
# pylint: disable=too-many-arguments


class QueryParams(dict):
    """dict tailored for MediaFire requests.

    * won't store None values
    * boolean values are converted to 'yes'/'no'
    """

    def __init__(self, defaults=None):
        super(QueryParams, self).__init__()
        if defaults is not None:
            for key, value in defaults.items():
                self.__setitem__(key, value)

    def __setitem__(self, key, value):
        """Set dict item, handling booleans"""
        if value is not None:
            if value is True:
                value = 'yes'
            elif value is False:
                value = 'no'
            dict.__setitem__(self, key, value)


class MediaFireApiError(Exception):
    """Base class for API errors"""
    def __init__(self, message, code=None):
        """Initialize exception"""
        self.code = code
        self.message = message
        super(MediaFireApiError, self).__init__(message, code)

    def __str__(self):
        """Stringify exception"""
        return "{}: {}".format(self.code, self.message)


class MediaFireApi(object):  # pylint: disable=too-many-public-methods
    """Low-level HTTP API Client"""

    def __init__(self):
        """Initialize MediaFire Client"""

        self.http = requests.Session()
        self.http.mount('https://',
                        HTTPAdapter(max_retries=API_ERROR_MAX_RETRIES))

        self._session = None
        self._action_tokens = {}

    @staticmethod
    def _build_uri(action):
        """Build endpoint URI from action"""
        return '/api/' + API_VER + '/' + action + '.php'

    def _build_query(self, uri, params=None, action_token_type=None):
        """Prepare query string"""

        if params is None:
            params = QueryParams()

        params['response_format'] = 'json'

        session_token = None

        if action_token_type in self._action_tokens:
            # Favor action token
            using_action_token = True
            session_token = self._action_tokens[action_token_type]
        else:
            using_action_token = False
            if self._session:
                session_token = self._session['session_token']

        if session_token:
            params['session_token'] = session_token

        # make order of parameters predictable for testing
        keys = list(params.keys())
        keys.sort()

        query = urlencode([tuple([key, params[key]]) for key in keys])

        if not using_action_token and self._session:
            secret_key_mod = int(self._session['secret_key']) % 256

            signature_base = (str(secret_key_mod) +
                              self._session['time'] +
                              uri + '?' + query).encode('ascii')

            query += '&signature=' + hashlib.md5(signature_base).hexdigest()

        return query

    def request(self, action, params=None, action_token_type=None,
                upload_info=None, headers=None):
        """Perform request to MediaFire API

        action -- "category/name" of method to call
        params -- dict of parameters or query string
        action_token_type -- action token to use: None, "upload", "image"
        upload_info -- in case of upload, dict of "fd" and "filename"
        headers -- additional headers to send (used for upload)

        session_token and signature generation/update is handled automatically
        """

        uri = self._build_uri(action)

        if type(params) is six.text_type:
            query = params
        else:
            query = self._build_query(uri, params, action_token_type)

        if headers is None:
            headers = {}

        if upload_info is None:
            # Use request body for query
            data = query
            headers['Content-Type'] = 'application/x-www-form-urlencoded'
        else:
            # Use query string for query since payload is file
            uri += '?' + query

            if "filename" in upload_info:
                data = MultipartEncoder(
                    fields={'file': (
                        upload_info["filename"],
                        upload_info["fd"],
                        'application/octet-stream'
                    )}
                )
                headers["Content-Type"] = data.content_type
            else:
                data = upload_info["fd"]
                headers["Content-Type"] = 'application/octet-stream'

        logger.debug("uri=%s query=%s",
                     uri, query if not upload_info else None)

        response = self.http.post(API_BASE + uri, data=data,
                                  headers=headers, stream=True)

        return self._process_response(response)

    def _process_response(self, response):
        """Parse response"""

        forward_raw = False
        content_type = response.headers['Content-Type']
        if content_type != 'application/json':
            logger.debug("headers: %s", response.headers)
            # API BUG: text/xml content-type with json payload
            # http://forum.mediafiredev.com/showthread.php?136
            if content_type == 'text/xml':
                # we never request xml
                if response.text.lstrip().startswith('{'):
                    logger.debug("API BUG: text/xml content-type "
                                 "with JSON payload")
                else:
                    forward_raw = True
            else:
                # _process_response can't deal with non-json,
                # return response as is
                forward_raw = True

        if forward_raw:
            response.raise_for_status()
            return response

        logger.debug("response: %s", response.text)

        # if we are here, then most likely have json
        try:
            response_node = response.json()['response']
        except ValueError:
            # promised JSON but failed
            raise MediaFireApiError("JSON decode failure")

        if response_node.get('new_key', 'no') == 'yes':
            self._regenerate_secret_key()

        # check for errors
        if response_node['result'] != 'Success':
            raise MediaFireApiError(response_node['message'],
                                    response_node['error'])

        return response_node

    def _regenerate_secret_key(self):
        """Regenerate secret key

        http://www.mediafire.com/developers/core_api/1.1/getting_started/#call_signature
        """
        # Don't regenerate the key if we have none
        if self._session and 'secret_key' in self._session:
            self._session['secret_key'] = (
                int(self._session['secret_key']) * 16807) % 2147483647

    @property
    def session(self):
        """Returns current session information"""
        return self._session

    @session.setter
    def session(self, value):
        """Set session token

        value -- dict returned by user/get_session_token"""

        # unset session token
        if value is None:
            self._session = None
            return

        if type(value) is not dict:
            raise ValueError("session info is required")

        session_parsed = {}

        for key in ["session_token", "time", "secret_key"]:
            if key not in value:
                raise ValueError("Missing parameter: {}".format(key))
            session_parsed[key] = value[key]

        for key in ["ekey", "pkey"]:
            # nice to have, but not mandatory
            if key in value:
                session_parsed[key] = value[key]

        self._session = session_parsed

    @session.deleter
    def session(self):
        """Unset session"""
        self._session = None

    # TODO: Remove in 0.5
    def set_session_token(self, session_token=None):
        """DEPRECTATED, use api.session = session_token"""
        self.session = session_token

    def set_action_token(self, type_=None, action_token=None):
        """Set action tokens

        type_ -- either "upload" or "image"
        action_token -- string obtained from user/get_action_token,
                        set None to remove the token
        """
        if action_token is None:
            del self._action_tokens[type_]
        else:
            self._action_tokens[type_] = action_token

    def user_fetch_tos(self):
        """user/fetch_tos

        http://www.mediafire.com/developers/core_api/1.1/user/#fetch_tos
        """

        return self.request("user/fetch_tos")

    def user_accept_tos(self, acceptance_token):
        """user/accept_tos

        http://www.mediafire.com/developers/core_api/1.1/user/#user_top
        """

        return self.request("user/accept_tos", QueryParams({
            "acceptance_token": acceptance_token
        }))

    def user_get_session_token(self, app_id=None, email=None, password=None,
                               ekey=None, fb_access_token=None,
                               tw_oauth_token=None,
                               tw_oauth_token_secret=None, api_key=None):
        """user/get_session_token

        http://www.mediafire.com/developers/core_api/1.1/user/#get_session_token
        """

        if app_id is None:
            raise ValueError("app_id must be defined")

        params = QueryParams({
            'application_id': str(app_id),
            'token_version': 2,
            'response_format': 'json'
        })

        if fb_access_token:
            params['fb_access_token'] = fb_access_token
            signature_keys = ['fb_access_token']
        elif tw_oauth_token and tw_oauth_token_secret:
            params['tw_oauth_token'] = tw_oauth_token
            params['tw_oauth_token_secret'] = tw_oauth_token_secret
            signature_keys = ['tw_oauth_token',
                              'tw_oauth_token_secret']
        elif (email or ekey) and password:
            signature_keys = []
            if email:
                signature_keys.append('email')
                params['email'] = email

            if ekey:
                signature_keys.append('ekey')
                params['ekey'] = ekey

            params['password'] = password
            signature_keys.append('password')
        else:
            ValueError("Credentials not provided")

        signature_keys.append('application_id')

        signature = hashlib.sha1()
        for key in signature_keys:
            signature.update(str(params[key]).encode('ascii'))

        # Note: If the app uses a callback URL to provide its API key,
        # or if it does not have the "Require Secret Key" option checked,
        # then the API key may be omitted from the signature
        if api_key:
            signature.update(api_key.encode('ascii'))

        query = urlencode(params)
        query += '&signature=' + signature.hexdigest()

        return self.request('user/get_session_token', params=query)

    def user_renew_session_token(self):
        """user/renew_session_token:

        http://www.mediafire.com/developers/core_api/1.1/user/#renew_session_token
        """
        return self.request('user/renew_session_token')

    def user_get_action_token(self, type_=None, lifespan=None):
        """user/get_action_token

        http://www.mediafire.com/developers/core_api/1.1/user/#get_action_token
        """
        return self.request('user/get_action_token', QueryParams({
            'type': type_,
            'lifespan': lifespan
        }))

    def user_destroy_action_token(self, action_token=None):
        """user/destroy_action_token

        http://www.mediafire.com/developers/core_api/1.1/user/#destroy_action_token
        """
        return self.request('user/destroy_action_token', QueryParams({
            'action_token': action_token
        }))

    def user_get_avatar(self):
        """user/get_avatar

        http://www.mediafire.com/developers/core_api/1.1/user/#get_avatar
        """
        return self.request("user/get_avatar")

    def user_get_info(self):
        """user/get_info

        http://www.mediafire.com/developers/core_api/1.1/user/#get_info
        """
        return self.request("user/get_info")

    def user_get_limits(self):
        """user/get_limits

        http://www.mediafire.com/developers/core_api/1.1/user/#get_limits
        """
        return self.request("user/get_limits")

    def user_get_settings(self):
        """user/get_settings

        http://www.mediafire.com/developers/core_api/1.1/user/#get_settings
        """
        return self.request("user/get_settings")

    def user_set_avatar(self, action=None, quick_key=None, url=None):
        """user/set_avatar

        http://www.mediafire.com/developers/core_api/1.1/user/#set_avatar
        """
        return self.request("user/set_avatar", QueryParams({
            "action": action,
            "quick_key": quick_key,
            "url": url
        }))

    def user_update(self, display_name=None, first_name=None, last_name=None,
                    email=None, password=None, current_password=None,
                    birth_date=None, gender=None, website=None, subdomain=None,
                    location=None, newsletter=None, primary_usage=None,
                    timezone=None):
        """
        user/update

        http://www.mediafire.com/developers/core_api/1.1/user/#update
        """
        return self.request("user/update", QueryParams({
            "display_name": display_name,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": password,
            "current_password": current_password,
            "birth_date": birth_date,
            "gender": gender,
            "website": website,
            "subdomain": subdomain,
            "location": location,
            "newsletter": newsletter,
            "primary_usage": primary_usage,
            "timezone": timezone
        }))

    def folder_get_info(self, folder_key=None, device_id=None, details=None):
        """folder/get_info

        http://www.mediafire.com/developers/core_api/1.1/folder/#get_info
        """
        return self.request('folder/get_info', QueryParams({
            'folder_key': folder_key,
            'device_id': device_id,
            'details': details
        }))

    def folder_get_content(self, folder_key=None, content_type=None,
                           filter_=None, device_id=None, order_by=None,
                           order_direction=None, chunk=None, details=None):
        """folder/get_content

        http://www.mediafire.com/developers/core_api/1.1/folder/#get_content
        """
        return self.request('folder/get_content', QueryParams({
            'folder_key': folder_key,
            'content_type': content_type,
            'filter': filter_,
            'device_id': device_id,
            'order_by': order_by,
            'order_direction': order_direction,
            'chunk': chunk,
            'details': details
        }))

    def folder_update(self, folder_key, foldername=None, description=None,
                      privacy=None, privacy_recursive=None, mtime=None):
        """folder/update

        http://www.mediafire.com/developers/core_api/1.1/folder/#update
        """
        return self.request('folder/update', QueryParams({
            'folder_key': folder_key,
            'foldername': foldername,
            'description': description,
            'privacy': privacy,
            'privacy_recursive': privacy_recursive,
            'mtime': mtime
        }))

    def folder_create(self, foldername=None, parent_key=None,
                      allow_duplicate_name=None, mtime=None):
        """folder/create

        http://www.mediafire.com/developers/core_api/1.1/folder/#create
        """
        return self.request('folder/create', QueryParams({
            'foldername': foldername,
            'parent_key': parent_key,
            'allow_duplicate_name': allow_duplicate_name,
            'mtime': mtime
        }))

    def folder_delete(self, folder_key):
        """folder/delete

        http://www.mediafire.com/developers/core_api/1.1/folder/#delete
        """
        return self.request('folder/delete', QueryParams({
            'folder_key': folder_key
        }))

    def folder_purge(self, folder_key):
        """folder/purge

        http://www.mediafire.com/developers/core_api/1.1/folder/#purge
        """
        return self.request('folder/purge', QueryParams({
            'folder_key': folder_key
        }))

    def folder_move(self, folder_key_src, folder_key_dst=None):
        """folder/move

        http://www.mediafire.com/developers/core_api/1.1/folder/#move
        """
        return self.request('folder/move', QueryParams({
            'folder_key_src': folder_key_src,
            'folder_key_dst': folder_key_dst
        }))

    def upload_check(self, filename=None, folder_key=None, filedrop_key=None,
                     size=None, hash_=None, path=None, resumable=None):
        """upload/check

        http://www.mediafire.com/developers/core_api/1.1/upload/#check
        """
        return self.request('upload/check', QueryParams({
            'filename': filename,
            'folder_key': folder_key,
            'filedrop_key': filedrop_key,
            'size': size,
            'hash': hash_,
            'path': path,
            'resumable': resumable
        }))

    def upload_simple(self, fd, filename, folder_key=None, path=None,
                      filedrop_key=None, action_on_duplicate=None,
                      mtime=None, file_size=None, file_hash=None):
        """upload/simple

        http://www.mediafire.com/developers/core_api/1.1/upload/#simple
        """
        action = 'upload/simple'

        params = QueryParams({
            'folder_key': folder_key,
            'path': path,
            'filedrop_key': filedrop_key,
            'action_on_duplicate': action_on_duplicate,
            'mtime': mtime
        })

        headers = QueryParams({
            'X-Filesize': file_size,
            'X-Filehash': file_hash,
            'X-Filename': filename.encode('utf-8')
        })

        upload_info = {
            "fd": fd,
        }

        return self.request(action, params, action_token_type="upload",
                            upload_info=upload_info, headers=headers)

    def upload_resumable(self, fd, filesize, filehash, unit_hash, unit_id,
                         unit_size, quick_key=None, action_on_duplicate=None,
                         mtime=None, version_control=None, folder_key=None,
                         filedrop_key=None, path=None, previous_hash=None):
        """upload/resumable

        http://www.mediafire.com/developers/core_api/1.1/upload/#resumable
        """
        action = 'upload/resumable'

        headers = {
            'x-filesize': filesize,
            'x-filehash': filehash,
            'x-unit-hash': unit_hash,
            'x-unit-id': unit_id,
            'x-unit-size': unit_size
        }

        params = QueryParams({
            'quick_key': quick_key,
            'action_on_duplicate': action_on_duplicate,
            'mtime': mtime,
            'version_control': version_control,
            'folder_key': folder_key,
            'filedrop_key': filedrop_key,
            'path': path,
            'previous_hash': previous_hash
        })

        upload_info = {
            "fd": fd,
            "filename": "chunk"
        }

        return self.request(action, params, action_token_type="upload",
                            upload_info=upload_info, headers=headers)

    def upload_instant(self, filename, size, hash_, quick_key=None,
                       folder_key=None, filedrop_key=None, path=None,
                       action_on_duplicate=None, mtime=None,
                       version_control=None, previous_hash=None):
        """upload/instant

        http://www.mediafire.com/developers/core_api/1.1/upload/#instant
        """
        return self.request('upload/instant', QueryParams({
            'filename': filename,
            'size': size,
            'hash': hash_,
            'quick_key': quick_key,
            'folder_key': folder_key,
            'filedrop_key': filedrop_key,
            'path': path,
            'action_on_duplicate': action_on_duplicate,
            'mtime': mtime,
            'version_control': version_control,
            'previous_hash': previous_hash
        }))

    def upload_poll(self, key):
        """upload/poll

        http://www.mediafire.com/developers/core_api/1.1/upload/#poll_upload
        """
        return self.request('upload/poll_upload', QueryParams({
            'key': key
        }))

    def file_get_info(self, quick_key=None):
        """file/get_info

        http://www.mediafire.com/developers/core_api/1.1/file/#get_info
        """
        return self.request('file/get_info', QueryParams({
            'quick_key': quick_key
        }))

    def file_get_links(self, quick_key, link_type=None):
        """file/get_links

        http://www.mediafire.com/developers/core_api/1.1/file/#get_links
        """
        return self.request('file/get_links', QueryParams({
            'quick_key': quick_key,
            'link_type': link_type,
        }))

    def file_update(self, quick_key, filename=None, description=None,
                    mtime=None, privacy=None):
        """file/update

        http://www.mediafire.com/developers/core_api/1.1/file/#update
        """
        return self.request('file/update', QueryParams({
            'quick_key': quick_key,
            'filename': filename,
            'description': description,
            'mtime': mtime,
            'privacy': privacy
        }))

    def file_update_file(self, quick_key, file_extension=None, filename=None,
                         description=None, mtime=None, privacy=None,
                         timezone=None):
        """file/update_file

        http://www.mediafire.com/developers/core_api/1.1/file/#update_file
        """
        return self.request('file/update', QueryParams({
            'quick_key': quick_key,
            'file_extension': file_extension,
            'filename': filename,
            'description': description,
            'mtime': mtime,
            'privacy': privacy,
            'timezone': timezone
        }))

    def file_delete(self, quick_key):
        """file/delete

        http://www.mediafire.com/developers/core_api/1.1/file/#delete
        """
        return self.request('file/delete', QueryParams({
            'quick_key': quick_key
        }))

    def file_move(self, quick_key, folder_key=None):
        """file/move

        http://www.mediafire.com/developers/core_api/1.1/file/#move
        """
        return self.request('file/move', QueryParams({
            'quick_key': quick_key,
            'folder_key': folder_key
        }))

    def file_purge(self, quick_key):
        """file/purge

        http://www.mediafire.com/developers/core_api/1.1/file/#purge
        """
        return self.request('file/purge', QueryParams({
            'quick_key': quick_key
        }))

    def file_zip(self, keys, confirm_download=None, meta_only=None):
        """file/zip

        http://www.mediafire.com/developers/core_api/1.1/file/#zip
        """
        return self.request('file/zip', QueryParams({
            'keys': keys,
            'confirm_download': confirm_download,
            'meta_only': meta_only
        }))

    def system_get_info(self):
        """system/get_info

        http://www.mediafire.com/developers/core_api/1.1/system/#get_info
        """
        return self.request('system/get_info')

    def system_get_status(self):
        """system/get_status

        http://www.mediafire.com/developers/core_api/1.1/system/#get_status
        """
        return self.request('system/get_status')
