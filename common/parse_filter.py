from typing import Literal
from config import config
import re

def name_should_download(name: str, type_: Literal['directory', 'file']):
    for filter_ in config.name_filters:
        range_check = filter_.range == 'all' or filter_.range == type_
        if not range_check:
            continue

        flag = re.IGNORECASE if filter_.ignore_case else 0

        match_method = re.fullmatch if filter_.excat_match else re.search

        regex_match = bool(match_method(filter_.regex, name, flag))

        if regex_match ^ (filter_.type == 'include'):
            return False

    return True


if __name__ == '__main__':
    print(name_should_download('効果音なしver', type_='directory'))