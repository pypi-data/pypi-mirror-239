import sys
from typing import Union, AsyncGenerator
from urllib.parse import urlparse

import httpx

from ...common.logger import logger
from ...common.storage import BaseStorage
from ...common.types import CrawlerBackTask, CrawlerContent, DatapoolContentType

try:
    from bs4 import BeautifulSoup
except ImportError:
    pass
try:
    from playwright.async_api import Page
except ImportError:
    pass
import re

class BasePluginException(Exception):
    pass


class BasePlugin:
    license_filename = 'LICENSE.txt'

    def __init__(self, storage: BaseStorage):
        self.storage = storage

    async def download(self, url, headers={}):
        try:
            async with httpx.AsyncClient(
                max_redirects=5
            ) as client:  # TODO: 5 should be parameter
                r = await client.get(
                    url, follow_redirects=True, headers=headers
                    
                )  # TODO: follow_redirects should be parameter
                return r.content

        except Exception as e:
            logger.error(f"failed get content of {url}: {e}")

    def parse_url(self, url):
        return urlparse(url)

    def is_supported(self, url):
        raise Exception("implement in child class")

    async def process(
        self, url
    ) -> AsyncGenerator[ Union[CrawlerContent, CrawlerBackTask], None ]:
        raise Exception("implement in child class")

    @staticmethod
    def is_imported(module):
        return module in sys.modules

    @staticmethod
    async def parse_meta_tag(content, meta_name):
        regexp = re.compile("^https://openlicense.ai/t/(\w+)$")
        regexp2 = re.compile('olai\:(\w+)')
        if BasePlugin.is_imported("bs4") and type(content) is BeautifulSoup:
            # TODO: add regexp2 support
            tag = content.find("meta", attrs={"content": regexp})
            if tag is not None:
                return tag.group(1)
        if (
            BasePlugin.is_imported("playwright.async_api")
            and type(content) is Page
        ):
            metas = content.locator(f'meta[name="{meta_name}"]')
            for meta in await metas.all():
                c = await meta.get_attribute("content")
                
                # TODO: combine regexp + regexp2 into single regexp
                tag = regexp.match(c)
                if tag is not None:
                    return tag.group(1)
                else:
                    tag = regexp2.search(c)
                    if tag is not None:
                        return tag.group(1)
        
    @staticmethod
    async def parse_tag_in(content, locator: str = ''):
        regexp = re.compile("olai\:(\w+)")
        regexp2 = re.compile("^https://openlicense.ai/t/(\w+)$")
        if type(content) is str:
            tag = regexp.match(content)
            if tag is None:
                tag = regexp2.match(content)
        elif BasePlugin.is_imported("bs4") and type(content) is BeautifulSoup:
            tag = content.find(locator, attrs={"content": regexp})
            if tag is None:
                tag = regexp2.match(content)
        elif (
            BasePlugin.is_imported("playwright.async_api")
            and type(content) is Page
        ):
            elems = content.locator(locator)
            for elem in await elems.all():
                c = await elem.text_content()
                tag = regexp.match(c)
                if tag is not None:
                    break
                tag = regexp2.match(content)
                if tag is not None:
                    break
                
        if tag is not None:
            return tag.group(1)
                
    @staticmethod
    def get_content_type_by_mime_type( mime ):
        logger.info( f'{mime=}')
        parts = mime.split('/')
        if parts[0] == 'image':
            return DatapoolContentType.Image
        if parts[0] == 'video':
            return DatapoolContentType.Video
        if parts[0] == 'audio':
            return DatapoolContentType.Audio
        if parts[0] == 'text' or mime == 'application/json':
            return DatapoolContentType.Text
        
        raise BasePluginException(f"not supported mime {mime}")