# flk-crawler
[![Pylint](https://github.com/hamishzx/flk-crawler/actions/workflows/pylint.yml/badge.svg)](https://github.com/hamishzx/flk-crawler/actions/workflows/pylint.yml)
[![PR Welcome Badge](https://badgen.net/https/pr-welcome-badge.vercel.app/api/badge/hamishzx/flk-crawler)](https://github.com/hamishzx/flk-crawler/issues?q=archived:false+is:issue+is:open+sort:updated-desc+label%3A%22help%20wanted%22%2C%22good%20first%20issue%22)

Used to download files from a mysterious flk-npc-xxx-cn site, what it's for is what it's for.

用于下载国家法律法规数据数据库（flk-npc-gov-cn）的文件，暂时决定保持更新并完善功能。
## Disclaimer

本项目仅用于学术研究或资料参考，使用者在使用本工具时必须遵守中华人民共和国及所在地相关法律法规，不得利用本工具进行任何非法活动，并应当自行承担使用网络爬虫的风险和后果。

This project is ONLY for academic research, reference and general information purposes only.

The user MUST comply with relevant laws and regulations in the People's Republic of China and the place of their residence in the use of this tool, and shall NOT use this tool for any illegal activities.

Use of this tool in some unauthorised circumstances might NOT be safe and thus is at the user's SOLE risk.

Author of this project accepts NO responsibility or liability for any consequences of the use of this tool.

## Availability
Test passed on:

![Edge](https://img.shields.io/badge/Edge-0078D7?style=for-the-badge&logo=Microsoft-edge&logoColor=white) Microsoft Edge 131.0.2903.63 (Official build) (64-bit).

And should be available on other versions of Microsoft Edge.

## Requirements
- Microsoft Edge, with corresponding webdriver.
- Python 3.8 or higher.

## Usage
```sh
pip install -r requirements.txt
vi ./src/search.py # Change directory at L42
python ./src/main.py
```