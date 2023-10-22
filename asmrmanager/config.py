from dataclasses import dataclass
from typing import List, Literal

import toml

from asmrmanager import CONFIG_PATH


@dataclass
class Config:
    username: str
    password: str
    proxy: str
    download_path: str
    storage_path: str
    view_path: str
    tag_filter: List[str]
    editor: str
    filename_filters: List["Filter"]
    download_method: Literal["aria2", "idm"]
    aria2_config: "Aria2Config"


@dataclass
class Filter:
    regex: str = ""  # 正则表达式

    # 该规则是包含还是排除，注意只有满足所有的include规则且不满足所有的exclude规则才会被下载
    type: Literal["include", "exclude"] = "exclude"

    range: Literal["file", "directory", "all"] = "all"  # 该规则针对的文件类型
    excat_match: bool = False  # 是否应精确匹配(从头到尾严格匹配)
    ignore_case: bool = True  # 是否忽略大小写


@dataclass
class Aria2Config:
    host: str = "http://localhost"
    port: int = 6800
    secret: str = ""


_config = toml.load(CONFIG_PATH / 'config.toml')

_filename_filters: list = _config.get('filename_filters', [])
filename_filters = list(
    map(lambda x: Filter(**x) if isinstance(x, dict)
        else Filter(x), _filename_filters)
)
_aria2_config: dict = _config.get('aria2_config', {})
aria2_config = Aria2Config(**_aria2_config)


config = Config(
    username=_config['username'],
    password=_config['password'],
    proxy=_config['proxy'],
    download_path=_config['download_path'],
    storage_path=_config['storage_path'],
    view_path=_config['view_path'],
    tag_filter=_config['tag_filter'],
    editor=_config['editor'],
    filename_filters=filename_filters,
    download_method=_config['download_method'],
    aria2_config=aria2_config)