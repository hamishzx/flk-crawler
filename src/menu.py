# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Time: 24 Nov 2024 Sun 23:24
# Name: menu
# Author: CHAU SHING SHING HAMISH
import gc
import os
import sys
import time
import description
from crawler import Spider
from search import search

spider = Spider()

def get_reverse(options, value):
    # get key from value
    for key, val in options.items():
        if val == value:
            return key
    return None

def get_options(param_name, op):
    options = {}
    # options for different operations, mainly in description.py
    if op == 'display':
        options['q'] = '返回主菜单'
        if param_name == 'main':
            options = {
                '1': '修改',
                '2': '开始搜索',
                'q': '退出'
            }
        elif param_name == 'main-edit':
            for k, v in enumerate(description.user_options, start=1):
                options[str(k)] = v
        elif param_name in description.user_options_ref:
            for k, v in enumerate(description.user_options_ref[param_name], start=1):
                options[str(k)] = v
    elif op == 'menu':
        options['q'] = 'main'
        if param_name == 'main':
            options = {
                '1': 'main-edit',
                '2': 'main-start',
                'q': 'main-exit'
            }
        elif param_name == 'main-edit':
            for k, v in enumerate(description.user_options, start=1):
                options[str(k)] = description.user_options[v]
        elif param_name in description.user_options_ref:
            for k, v in enumerate(description.user_options_ref[param_name], start=1):
                options[str(k)] = description.user_options_ref[param_name][v]
    return options

def print_options(title, options):
    print(f'-----------------{title}-----------------')
    for k in options:
        print(f'[{k}] {options[k]}')

def show_current_settings():
    print('-----------------当前搜索设置-----------------\n')
    for key, value in spider.params.items():
        # only print settings that could be modified
        if key in description.summary:
            if key in ['type', 'xlwj', 'fgxlwj', 'zdjg']:
                print(f'{description.summary[key]}: {[get_reverse(description.user_options_ref[key], value)
                                                      for value in value.split(',')] if value else ''}')
            elif key == 'searchType':
                for i, v in enumerate(value.split(';')):
                    if i == 0:
                        print(f'搜索范围：{get_reverse(description.search_type[0], v)}')
                    elif i == 1:
                        print(f'搜索方式：{get_reverse(description.search_type[1], v)}')
                    elif i == 2:
                        print(f'时效性：{[get_reverse(description.search_type[2], vv) for vv in v.split(',')]}')
            else:
                print(f'{description.summary[key]}: {value}')

def validate_choice(param, choice, options):
    if choice == 'q' or param == 'fgbt':
        return True
    if param in ['gbrqStart', 'gbrqEnd', 'sxrqStart', 'sxrqEnd']:
        try:
            time.strptime(choice, '%Y%m%d')
            return True
        except ValueError:
            pass
    elif param == 'page':
        return choice.isdigit()
    elif param in ['search-effectiveness']:
        return all(c in options for c in choice)
    elif choice.isdigit():
        return bool(choice in options)
    return False

def submit_choice(param, choice, options):
    if param in ['fgbt', 'page']:
        spider.set_param(param, choice)
    elif param in ['gbrqStart', 'gbrqEnd', 'sxrqStart', 'sxrqEnd']:
        spider.set_param(param, f'{choice[:4]}-{choice[4:6]}-{choice[6:]}')
    elif param == 'search-range':
        current_search_type = spider.params['searchType'].split(';')
        current_search_type[0] = options[choice]
        spider.set_param('searchType', ';'.join(current_search_type))
    elif param == 'search-type':
        current_search_type = spider.params['searchType'].split(';')
        current_search_type[1] = options[choice]
        spider.set_param('searchType', ';'.join(current_search_type))
    elif param in ['xlwj', 'fgxlwj', 'zdjg', 'search-effectiveness']:
        submit_multi_choice(param, choice, options)
        options[choice] = param if options[choice] != 'main' else 'main'
        return options
    else:
        spider.set_param(param, options[choice])
    options[choice] = 'main'
    return options

def submit_multi_choice(param, choice, options):
    if choice == 'q':
        return
    if param in ['xlwj', 'fgxlwj', 'zdjg']:
        current_value = spider.params[param].split(',')
        if options[choice] in current_value:
            current_value.remove(options[choice])
        else:
            current_value.append(options[choice])
        if current_value and not current_value[0]:
            current_value.pop(0)
        spider.set_param(param, ','.join(current_value))
    elif param == 'search-effectiveness':
        current_search_type = spider.params['searchType'].split(';')
        try:
            current_value = current_search_type[2].split(',')
            if options[choice] in current_value:
                current_value.remove(options[choice])
            else:
                current_value.append(options[choice])
            current_search_type[2] = ','.join(current_value)
        except IndexError:
            current_search_type.append(options[choice])
        if not current_search_type[2]:
            # remove the trailing semicolon
            current_search_type.pop()
        spider.set_param('searchType', ';'.join(current_search_type))

async def display_menu(param):
    # Clear the console
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
    # Init menu options
    options = get_options(param, 'menu')
    display_menu_content(param)

    choice = input('输入要修改的值或q返回主菜单：')

    while not validate_choice(param, choice, options):
        if param in ['gbrqStart', 'gbrqEnd', 'sxrqStart', 'sxrqEnd']:
            choice = input('输入有误，日期格式为YYYYMMDD，请重新输入：')
        elif param == 'page':
            choice = input('输入有误，页码为整数，请重新输入：')
        else:
            choice = input('输入有误，请重新输入：')

    if param in list(description.user_options.values()):
        options = submit_choice(param, choice, options)

    if options[choice] == 'main-start':
        if not await search(spider):
            for i in range(3):
                print(f'返回主菜单：{3 - i}')
                time.sleep(1)
        await display_menu('main')
    elif options[choice] == 'main-exit':
        gc.collect()
        sys.exit(0)
    else:
        await display_menu(options[choice])

def display_menu_content(param_name):
    if param_name.startswith('main'):
        show_current_settings()
        if param_name == 'main':
            print_options('操作选项', get_options(param_name, 'display'))
        else:
            print_options('更改参数', get_options(param_name, 'display'))
    elif param_name in ['xlwj', 'fgxlwj', 'zdjg', 'search-effectiveness']:
        display_menu_content_multi(param_name)
    else:
        print_options(get_reverse(description.user_options, param_name),
                      get_options(param_name, 'display'))

def display_menu_content_multi(param_name):
    # some are multiselect param, need to see them in real time
    title = get_reverse(description.user_options, param_name)
    options = get_options(param_name, 'display')
    print(f'-----------------{title}-----------------')
    if param_name in ['xlwj', 'fgxlwj', 'zdjg']:
        current_settings = spider.params[param_name].split(',') if spider.params[param_name] else ''
    else:
        try:
            current_settings = spider.params['searchType'].split(';')[2].split(',')
        except IndexError:
            current_settings = ''
    # as current_settings are code for request, need to get its display title here
    if current_settings:
        current_settings = [get_reverse(description.user_options_ref[param_name], v) for v in current_settings]
    for k, v in options.items():
        if v in current_settings:
            print(f'[{k}] {v} √')
        else:
            print(f'[{k}] {v}')
