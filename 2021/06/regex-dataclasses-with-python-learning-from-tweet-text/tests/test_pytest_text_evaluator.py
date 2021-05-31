import pytest

from regex_dataclasses.exceps import TextIsFalsyException
from regex_dataclasses.text_evaluator import check_text_and_grab_its_details


def test_should_evaluate_text_as_valid_given_keyword_and_one_hashtag_presence():
    # Arrange
    sample_tweet = "@GenieOfTheLamp concedes #VillainJafar"
    # Act
    result = check_text_and_grab_its_details(sample_tweet)
    # Assert
    assert result.is_valid
    assert result.hashtags == ["VillainJafar"]
    assert result.slugs == ["villain-jafar"]


def test_should_evaluate_text_as_valid_given_keyword_and_two_hashtags_presence():
    # Arrange
    sample_tweet = "@GenieOfTheLamp concedes #FirstWish #SecondWish"
    # Act
    result = check_text_and_grab_its_details(sample_tweet)
    # Assert
    assert result.is_valid
    assert result.hashtags == ["FirstWish", "SecondWish"]
    assert result.slugs == ["first-wish", "second-wish"]


def test_should_evaluate_text_as_invalid_given_missing_keyword():
    # Arrange
    sample_tweet = "@GenieOfTheLamp #FirstWish #SecondWish"
    # Act
    result = check_text_and_grab_its_details(sample_tweet)
    # Assert
    assert not result.is_valid


def test_should_evaluate_text_as_invalid_given_wrong_keyword():
    # Arrange
    sample_tweet = "@GenieOfTheLamp creates #FirstWish #SecondWish"
    # Act
    result = check_text_and_grab_its_details(sample_tweet)
    # Assert
    assert not result.is_valid


def test_should_throw_exception_when_text_is_none_or_empty():
    # Arrange
    sample_tweet = "@GenieOfTheLamp creates #FirstWish #SecondWish"
    # Act and assert
    with pytest.raises(TextIsFalsyException):
        check_text_and_grab_its_details("")
    with pytest.raises(AttributeError):
        check_text_and_grab_its_details(None)
