﻿# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Time: 23 Nov 2024 Sat 04:23
# Name: description
# Author: CHAU SHING SHING HAMISH

summary = {
    'type': '搜索类型',
    'fgbt': '搜索关键字',
    'searchType': '搜索方式',
    'gbrqStart': '公布日期开始',
    'gbrqEnd': '公布日期结束',
    'sxrqStart': '施行日期开始',
    'sxrqEnd': '施行日期结束',
    'xlwj': '法律文件效力位阶',
    'fgxlwj': '法规文件效力位阶',
    'zdjg': '制定机关',
    'page': '页码',
}

user_options = {
    '搜索类型': 'type',
    '搜索关键字': 'fgbt',
    '搜索范围': 'search-range',
    '搜索方式': 'search-type',
    '时效性': 'search-effectiveness',
    '公布日期开始': 'gbrqStart',
    '公布日期结束': 'gbrqEnd',
    '施行日期开始': 'sxrqStart',
    '施行日期结束': 'sxrqEnd',
    '法律文件效力位阶': 'xlwj',
    '法规文件效力位阶': 'fgxlwj',
    '制定机关': 'zdjg',
    '页码': 'page',
}

# param.type
law_type = {
    '法律': 'flfg',
    '行政法规': 'xzfg',
    '监察法规': 'jcfg',
    '司法解释': 'sfjs',
    '地方性法规': 'dfxfg'
}

# param.searchType
search_type = [
    {
        '标题': 'title',
        '正文': 'content',
        '标题+正文': 'all'
    },
    {
        '模糊搜索': 'vague',
        '精确搜索': 'accurate'
    },
    {
        '尚未生效': '3',
        '有效': '1',
        '已修改': '5',
        '已废止': '9'
    }
]

# param.xlwj
law_level = {
    '宪法': '01',
    '宪法相关法': '02',
    '民法商法': '03',
    '行政法': '04',
    '经济法': '05',
    '社会法': '06',
    '刑法': '07',
    '诉讼与非诉讼程序法': '08',
    '法律解释': 'fljs',
    '有关法律问题和重大问题的决定（部分）': 'flwj',
    '修改、废止的决定': 'flxz'
}

# param.fgxlwj
regulation_level = {
    '行政法规': 'xzfg',
    '监察法规': 'jcfg',
    '省级地方性法规': '2',
    '设区的市地方性法规': '3',
    '自治州自治条例': '4',
    '自治县自治条例': '5',
    '自治州单行条例': '6',
    '自治县单行条例': '7',
    '经济特区法规': '8',
    '海南自由贸易港法规': '9',
    '法规修改、废止的决定': '0902',
    '高法司法解释': '0602',
    '高检司法解释': '0601',
    '联合发布司法解释': '0603',
    '司法解释修改、废止的决定 ': '0903'
}

# param.zdjg
agency = {
    '联合发布': '0603',
    '全国人大': 'qgrmdbdh',
    '全国人大常委会': 'qgrmdbdhcwwyh',
    '国务院': 'gwy',
    '国家监察委员会': 'gjjcwyh',
    '最高人民检察院': '0601',
    '最高人民法院': '0602',
    '北京': '4028814858a4d78b0158a50f344e0048&4028814858a4d78b0158a50fa2ba004c',
    '天津': '4028814858b9b8e50158be80b1fb0004&4028814858b9b8e50158be81c2bd0008',
    '河北': '4028814858a4d78b0158a51071cb0050&4028814858a4d78b0158a513cbac0054',
    '山西': '4028814858b9b8e50158beb88965000d&4028814858b9b8e50158beb9cebd0011',
    '内蒙古': '4028814858b9b8e50158bebb20750015&4028814858b9b8e50158bebbf2630019',
    '辽宁': '4028814858b9b8e50158bebd69e2001d&4028814858b9b8e50158bec078c00021',
    '吉林': '4028814858b9b8e50158bec1c1820025&4028814858b9b8e50158bec2dcbf0029',
    '黑龙江': '4028814858a542db0158a9c8786e004d&4028814858a542db0158a9c9c7c50051',
    '上海': '4028814858b9b8e50158bec45e9a002d&4028814858b9b8e50158bec500350031',
    '江苏': '4028814858b9b8e50158bec5c28a0035&4028814858b9b8e50158bec6abbf0039',
    '浙江': '4028814858b9b8e50158bec7c42f003d&4028814858b9b8e50158beca3c590041',
    '安徽': '40284b82588a199001588a461c70003b&40284b82588a199001588a473c37003f',
    '福建': '4028814858b9b8e50158bed0ae4c0049&4028814858b9b8e50158bed16673004d',
    '江西': '4028814858b9b8e50158bed279b40051&4028814858b9b8e50158bed3084c0055',
    '山东': '4028814858b9b8e50158bed40f6d0059&4028814858b9b8e50158bed4987a005d',
    '河南': '4028814858b9b8e50158bed591680061&4028814858b9b8e50158bed64efb0065',
    '湖北': '4028814858b9b8e50158bed7338f0069&4028814858b9b8e50158bed7c16c006d',
    '湖南': '4028814858b9b8e50158bed8a0d20071&4028814858b9b8e50158bed91af00075',
    '广东': '4028814858b9b8e50158beda43a50079&4028814858b9b8e50158bedab7ea007d',
    '广西': '4028814858b9b8e50158bee02fd50081&4028814858b9b8e50158bee198d40085',
    '海南': '4028814858b9b8e50158bee2d3a10089&4028814858b9b8e50158bee3c9e1008d',
    '重庆': '4028814858b9b8e50158bee5863c0091&4028814858b9b8e50158bee9a3aa0095',
    '四川': '4028814858b9b8e50158beeaa1b70099&4028814858b9b8e50158beeb4757009d',
    '贵州': '4028814858b9b8e50158beec5ac800a1&4028814858b9b8e50158beecfed300a5',
    '云南': '4028814858b9b8e50158beee174200a9&4028814858b9b8e50158beeeaf7b00ad',
    '西藏': '4028814858b9b8e50158beefec0d00b1&4028814858b9b8e50158bef0947c00b5',
    '陕西': '4028814858b9b8e50158bef1d72600b9&4028814858b9b8e50158bef2706800bd',
    '甘肃': '4028814858b9b8e50158bef3797c00c1&4028814858b9b8e50158bef4210100c5',
    '青海': '4028814858b9b8e50158bef53e9e00c9&4028814858b9b8e50158bef5d32f00cd',
    '宁夏': '4028814858b9b8e50158bef6eec900d1&4028814858b9b8e50158bef7e82500d5',
    '新疆': '4028814858b9b8e50158bef9249700d9&4028814858b9b8e50158bef9d8b900dd'
}

user_options_ref = {
    'type': law_type,
    'search-range': search_type[0],
    'search-type': search_type[1],
    'search-effectiveness': search_type[2],
    'xlwj': law_level,
    'fgxlwj': regulation_level,
    'zdjg': agency,
}
