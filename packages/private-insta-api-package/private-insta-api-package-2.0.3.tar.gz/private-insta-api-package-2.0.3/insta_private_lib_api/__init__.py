import logging
from urllib.parse import urlparse

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from insta_private_lib_api.mixins.account import AccountMixin
from insta_private_lib_api.mixins.album import DownloadAlbumMixin, UploadAlbumMixin
from insta_private_lib_api.mixins.auth import LoginMixin
from insta_private_lib_api.mixins.bloks import BloksMixin
from insta_private_lib_api.mixins.challenge import ChallengeResolveMixin
from insta_private_lib_api.mixins.clip import DownloadClipMixin, UploadClipMixin
from insta_private_lib_api.mixins.collection import CollectionMixin
from insta_private_lib_api.mixins.comment import CommentMixin
from insta_private_lib_api.mixins.direct import DirectMixin
from insta_private_lib_api.mixins.explore import ExploreMixin
from insta_private_lib_api.mixins.fbsearch import FbSearchMixin
from insta_private_lib_api.mixins.fundraiser import FundraiserMixin
from insta_private_lib_api.mixins.hashtag import HashtagMixin
from insta_private_lib_api.mixins.highlight import HighlightMixin
from insta_private_lib_api.mixins.igtv import DownloadIGTVMixin, UploadIGTVMixin
from insta_private_lib_api.mixins.insights import InsightsMixin
from insta_private_lib_api.mixins.location import LocationMixin
from insta_private_lib_api.mixins.media import MediaMixin
from insta_private_lib_api.mixins.multiple_accounts import MultipleAccountsMixin
from insta_private_lib_api.mixins.note import NoteMixin
from insta_private_lib_api.mixins.notification import NotificationMixin
from insta_private_lib_api.mixins.password import PasswordMixin
from insta_private_lib_api.mixins.photo import DownloadPhotoMixin, UploadPhotoMixin
from insta_private_lib_api.mixins.private import PrivateRequestMixin
from insta_private_lib_api.mixins.public import (
    ProfilePublicMixin,
    PublicRequestMixin,
    TopSearchesPublicMixin,
)
from insta_private_lib_api.mixins.share import ShareMixin
from insta_private_lib_api.mixins.story import StoryMixin
from insta_private_lib_api.mixins.timeline import ReelsMixin
from insta_private_lib_api.mixins.totp import TOTPMixin
from insta_private_lib_api.mixins.track import TrackMixin
from insta_private_lib_api.mixins.user import UserMixin
from insta_private_lib_api.mixins.video import DownloadVideoMixin, UploadVideoMixin

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Used as fallback logger if another is not provided.
DEFAULT_LOGGER = logging.getLogger("insta_private_lib_api")


class Client(
    PublicRequestMixin,
    ChallengeResolveMixin,
    PrivateRequestMixin,
    TopSearchesPublicMixin,
    ProfilePublicMixin,
    LoginMixin,
    ShareMixin,
    TrackMixin,
    FbSearchMixin,
    HighlightMixin,
    DownloadPhotoMixin,
    UploadPhotoMixin,
    DownloadVideoMixin,
    UploadVideoMixin,
    DownloadAlbumMixin,
    NotificationMixin,
    UploadAlbumMixin,
    DownloadIGTVMixin,
    UploadIGTVMixin,
    MediaMixin,
    UserMixin,
    InsightsMixin,
    CollectionMixin,
    AccountMixin,
    DirectMixin,
    LocationMixin,
    HashtagMixin,
    CommentMixin,
    StoryMixin,
    PasswordMixin,
    DownloadClipMixin,
    UploadClipMixin,
    ReelsMixin,
    ExploreMixin,
    BloksMixin,
    TOTPMixin,
    MultipleAccountsMixin,
    NoteMixin,
    FundraiserMixin,
):
    proxy = None

    def __init__(
        self,
        settings: dict = {},
        proxy: str = None,
        delay_range: list = None,
        logger=DEFAULT_LOGGER,
        **kwargs,
    ):

        super().__init__(**kwargs)

        self.settings = settings
        self.logger = logger
        self.delay_range = delay_range

        self.set_proxy(proxy)

        self.init()

    def set_proxy(self, dsn: str):
        if dsn:
            assert isinstance(
                dsn, str
            ), f'Proxy must been string (URL), but now "{dsn}" ({type(dsn)})'
            self.proxy = dsn
            proxy_href = "{scheme}{href}".format(
                scheme="http://" if not urlparse(self.proxy).scheme else "",
                href=self.proxy,
            )
            self.public.proxies = self.private.proxies = {
                "http": proxy_href,
                "https": proxy_href,
            }
            return True
        self.public.proxies = self.private.proxies = {}
        return False
