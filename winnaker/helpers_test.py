import os
import random
import string
from helpers import get_env


def test_get_env():
    random_string = ''.join(random.choice(string.lowercase) for i in range(15))
    print "Random String: {}".format(random_string)
    os.environ["WINNAKER_TEST_ENV_VAR"] = "testingtesting"
    assert get_env("WINNAKER_TEST_ENV_VAR",
                   "nottherightthing") == "testingtesting"
    assert get_env(random_string, "thedefault") == "thedefault"
    return True


assert test_get_env()
