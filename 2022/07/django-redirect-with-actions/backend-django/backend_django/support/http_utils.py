from typing import Dict
from urllib import parse


def build_url_with_query_strings(url: str, query_strings: Dict[str, str]):
    url_parse = parse.urlparse(url)
    query = url_parse.query
    url_dict = dict(parse.parse_qsl(query))
    url_dict.update(query_strings)
    url_new_query = parse.urlencode(url_dict)
    url_parse = url_parse._replace(query=url_new_query)
    return parse.urlunparse(url_parse)
