import unittest

from regex_dataclasses.exceps import TextIsFalsyException
from regex_dataclasses.text_evaluator import check_text_and_grab_its_details


class TestTextEvaluator(unittest.TestCase):
    def test_should_evaluate_text_as_valid_given_keyword_and_one_hashtag_presence(self):
        # Arrange
        sample_tweet = "@GenieOfTheLamp concedes #VillainJafar"
        # Act
        result = check_text_and_grab_its_details(sample_tweet)
        # Assert
        self.assertTrue(result.is_valid)
        self.assertEqual(result.hashtags, ["VillainJafar"])
        self.assertEqual(result.slugs, ["villain-jafar"])

    def test_should_evaluate_text_as_valid_given_keyword_and_two_hashtags_presence(self):
        # Arrange
        sample_tweet = "@GenieOfTheLamp concedes #FirstWish #SecondWish"
        # Act
        result = check_text_and_grab_its_details(sample_tweet)
        # Assert
        self.assertTrue(result.is_valid)
        self.assertEqual(result.hashtags, ["FirstWish", "SecondWish"])
        self.assertEqual(result.slugs, ["first-wish", "second-wish"])

    def test_should_evaluate_text_as_invalid_given_missing_keyword(self):
        # Arrange
        sample_tweet = "@GenieOfTheLamp #FirstWish #SecondWish"
        # Act
        result = check_text_and_grab_its_details(sample_tweet)
        # Assert
        self.assertFalse(result.is_valid)

    def test_should_evaluate_text_as_invalid_given_wrong_keyword(self):
        # Arrange
        sample_tweet = "@GenieOfTheLamp creates #FirstWish #SecondWish"
        # Act
        result = check_text_and_grab_its_details(sample_tweet)
        # Assert
        self.assertFalse(result.is_valid)

    def test_should_throw_exception_when_text_is_none_or_empty(self):
        # Arrange
        sample_tweet = "@GenieOfTheLamp creates #FirstWish #SecondWish"
        # Act and assert
        with self.assertRaises(TextIsFalsyException):
            check_text_and_grab_its_details("")
        with self.assertRaises(AttributeError):
            check_text_and_grab_its_details(None)
