import asyncio
# import json
# import re
# import traceback
import os

# from bs4 import BeautifulSoup
# from playwright.async_api import Locator, Page
from playwright.async_api import TimeoutError as PlaywriteTimeoutError
from playwright.async_api import async_playwright

from pytube import YouTube
from pytube.exceptions import AgeRestrictedError as PytubeAgeRestrictedError

from ....common.logger import logger
from ....common.storage import BaseStorage
from ....common.types import (
#    CrawlerBackTask,
    CrawlerContent,
    CrawlerNop,
    DatapoolContentType,
)
from ..base_plugin import BasePlugin


class YoutubeChannelPlugin(BasePlugin):
    def __init__(self, storage):
        super().__init__(storage)
        self.channel_name = None
        # self.video_id = None
        self.tag_id = None

    def is_supported(self, url):
        u = self.parse_url(url)
        # logger.info( f'dataphoenix.info {u=}')
        if ( u.netloc == "youtube.com" or u.netloc == 'www.youtube.com' ):
            if u.path[0:2] == '/@':
                self.channel_name = u.path.split('/')[1]
                return True
            # elif u.path[0:6] == '/watch' and u.query[0:2] == 'v=':
            #     self.video_id = u.query[2:13]
            #     return True
            
        return False

    async def process(self, url):
        logger.info(f"youtube_channel::process({url})")

        async with async_playwright() as playwright:
            self.webkit = playwright.chromium
            self.browser = await self.webkit.launch()
            self.context = await self.browser.new_context()
            self.page = await self.context.new_page()

            # if self.channel_name is not None:
            url = f'https://www.youtube.com/{self.channel_name}/about'

            logger.info(f"loading url {url}")
            await self.page.goto(url)
            logger.info(f"loaded {url=}")
            
            # ps = await self.page.locator("meta").all()
            # for p in ps:
            #     html = await p.evaluate( "node => node.outerHTML" )
            #     logger.info( f'meta: {html}')
            
            # check if <meta/> tag exists with our tag
            #self.tag_id = await BasePlugin.parse_tag_in(self.page, 'meta[property="og:description"]')
            self.tag_id = await BasePlugin.parse_meta_tag(self.page, 'description')
            if not self.tag_id:
                logger.info("No #description tag found, give up")
                
                return

            logger.info(f"{self.tag_id=}")

            url = f'https://www.youtube.com/{self.channel_name}/videos'

            logger.info(f"loading url {url}")
            await self.page.goto(url)
            logger.info(f"loaded {url=}")

            logger.info("parsing feed")
            async for yielded in self._process_feed(url):
                yield yielded
            # else:
            #     async for yielded in self._process_video(url):
            #         yield yielded

    # async def _process_video(self, url):
        
    #     storage_id = BaseStorage.gen_id(url)
    #     logger.info(f"putting video into {storage_id=}")

    #     await self.storage.put(
    #         storage_id,
    #         json.dumps({"header": header, "excerpt": excerpt, "body": body}),
    #     )
        
    #     yield CrawlerContent(
    #         tag_id=self.header_tag_id,
    #         type=DatapoolContentType.Text,
    #         storage_id=storage_id,
    #         url=url,
    #     )

    async def _process_feed(self, url):
        total_videos = 0
        #iter = 0
        while True:
            #logger.info( 'scrolling  to bottom')
            #await self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            #container = self.page.locator('.ytd-app#content')
            #await container.evaluate("node => {node.scrollTop=node.scrollHeight;}")
            #logger.info( 'scrolled')
            
            videos = await self.page.locator("ytd-rich-item-renderer").all()
                                          
            n = len(videos)
            logger.info(f"videos on page {n=}")                
            
            i = total_videos
            while i < n:
                try:
                    href = await videos[i].locator("a#video-title-link").get_attribute("href", timeout=100)
                    title = await videos[i].locator('yt-formatted-string#video-title').text_content()
                    logger.info( f'{i=} {href=} {title=}')
                    
                    video_url = "https://www.youtube.com" + href
                    storage_id = BaseStorage.gen_id(video_url)
                    
                    youtube = YouTube(video_url)
                    video = youtube.streams.first()
                    tmp_path = video.download(output_path='/tmp', filename=storage_id)
                    
                    logger.info('downloded video')
                    
                    raw_video = open( tmp_path, 'rb' ).read()
                    
                    await self.storage.put(
                        storage_id,
                        raw_video
                    )
                    #TODO: title and other meta data can be put into separate storage item ( for example storage_id+"_meta" ) as json
                    #for displaying at openlicense.ai 
                    
                    logger.info( f'put video into storage {storage_id=}')
                    os.remove( tmp_path )
                    
                    yield CrawlerContent(tag_id=self.tag_id,
                                        type=DatapoolContentType.Video,
                                        storage_id=storage_id,
                                        url=video_url)
                    i += 1
                except PlaywriteTimeoutError as e:
                    #element may be not ready yet, no problems, will get it on the next iteration
                    logger.info( 'get_attribute timeout exception' )
                    break
                except PytubeAgeRestrictedError as e:
                    #TODO: should be able to bypass this. 
                    #For now skip such videos
                    i += 1

            total_videos = i        
            

            # logger.info( 'creating button locator')
            spinner = self.page.locator("#spinner")
            
            #scroll to  bottom. (js window.scrollTo etc does not work for some reason..)
            await self.page.mouse.wheel(0,600)

            # logger.info( 'getting disabled attr')
            spinner_exists = await spinner.count()

            logger.info(f"{spinner_exists=}")
            if not spinner_exists and n > 0 and total_videos == n:  #all videos are processed
                logger.info( 'spinner gone, done')
                break

            await asyncio.sleep(1)

        yield CrawlerNop()

