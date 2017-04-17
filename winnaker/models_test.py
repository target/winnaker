# given the build text, expect parsed items
from winnaker.models import Build

trigger_details = """myusername
2016-09-13 10:43:13 CDT
DETAIL:
STACK: api
"""
execution_summary = """Status: SUCCEEDED
Duration: 11:13
"""

build = Build(trigger_details, execution_summary)
assert build.username == "myusername"
assert build.status == "SUCCEEDED"
assert build.status_is_valid()
assert build.duration == "11:13"
assert str(build.datetime_started) == "2016-09-13 10:43:13"
