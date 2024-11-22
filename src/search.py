# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Time: 25 Nov 2024 Mon 17:58
# Name: search
# Author: CHAU SHING SHING HAMISH

import os
import re
import asyncio
import aiofiles
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.edge.service import Service


async def rename_file(download_dir, old_name_base, new_name_base):
    # Downloaded file may be in .doc or .docx format, check both
    old_name_doc = os.path.join(download_dir, f'{old_name_base}.doc')
    old_name_docx = os.path.join(download_dir, f'{old_name_base}.docx')

    while True:
        if os.path.exists(old_name_doc):
            old_name = old_name_doc
            break
        if os.path.exists(old_name_docx):
            old_name = old_name_docx
            break
        await asyncio.sleep(1)

    file_extension = os.path.splitext(old_name)[1]
    new_name = f'{new_name_base}{file_extension}'
    new_path = os.path.join(download_dir, new_name)

    async with aiofiles.open(old_name, 'rb') as f:
        async with aiofiles.open(new_path, 'wb') as nf:
            await nf.write(await f.read())

    os.remove(old_name)
    print(f'已重命名文件：{new_path}')

async def search(spider):
    download_dir = r'path\to\yours'
    ser = Service()
    edge_options = webdriver.EdgeOptions()
    edge_options.use_chromium = True
    # Set download directory
    edge_options.add_experimental_option('prefs', { 'download.default_directory': download_dir })
    web_driver = webdriver.Edge(service=ser, options=edge_options)
    web_driver.maximize_window()
    web_driver.get('edge://settings/downloads')
    # Edge will open a new tab to preview office files, disable it
    toggle = web_driver.execute_script('''
                return document.querySelector('input[aria-label="Open Office files in the browser"]');
        ''')
    toggle.click()

    # situations below, always return False to let it back to main menu, see display_menu() in menu.py
    if not spider.fetch():
        print('获取法律列表超时。')
        return False
    # No more laws or no laws found
    if not spider.next():
        if spider.pages == 0:
            print('无结果，请修改搜索条件后重试')
        else:
            print('下载完成')
        return False
    while law := spider.next():
        # response url is ./xxxxx so need to append the root url
        page_url = law['url'].replace('./', spider.page_url_root)
        retry_time = 0
        while True:
            try:
                print(f'打开：{law["title"]}')
                web_driver.get(page_url)
                # every page has a unique qr code with file name as src, use it to get source file name
                png_dld = web_driver.find_element('id', 'codeMa')
                file_base = re.search(r'/(.[^/]*).png', png_dld.get_attribute('src')).group(1)
                # could be stuck from server, try again
                if len(file_base) < 32:
                    raise NoSuchElementException('Invalid file name')
                # download btn
                law_dld = web_driver.find_element('id', 'downLoadFile')
                law_dld.click()
                print(f"下载：{law['title']}，文件名：{file_base}")
                await rename_file(download_dir, file_base, f"{law['title']}")
                break
            except NoSuchElementException:
                if retry_time < 3:
                    print(f"打开失败：{law['title']}，重试")
                    web_driver.refresh()
                    retry_time += 1
                else:
                    print(f"下载失败：{law['title']}")
                    return False
    return True
