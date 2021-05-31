import re

from dataclasses import dataclass
from typing import List
from typing import Optional

from regex_dataclasses.exceps import TextIsFalsyException
from regex_dataclasses.text_utils import strip_left_and_right_sides


@dataclass(frozen=True)
class TextDetails:
    is_valid: bool
    hashtags: Optional[List[str]] = None
    slugs: Optional[List[str]] = None


pattern_valid_text = re.compile(r".* ?@GenieOfTheLamp concedes (#[a-zA-Z]{1,} ?)+$")
pattern_hashtags = re.compile(r"(#[a-zA-Z]{1,})")
pattern_camel_case_conversion = re.compile(r"(?!^)([A-Z]+)")


def check_text_and_grab_its_details(text: str) -> TextDetails:
    cleaned_text = strip_left_and_right_sides(text)

    if not cleaned_text:
        raise TextIsFalsyException

    match = pattern_valid_text.match(text)

    if not match:
        return TextDetails(False)

    all_hashtags = pattern_hashtags.findall(text)

    hashtags = []
    slugs = []

    for hashtag in all_hashtags:
        tag = hashtag.replace("#", "")
        almost_slug = pattern_camel_case_conversion.sub(r"-\1", tag)
        slug = almost_slug.lower()
        hashtags.append(tag)
        slugs.append(slug)

    return TextDetails(True, hashtags, slugs)
