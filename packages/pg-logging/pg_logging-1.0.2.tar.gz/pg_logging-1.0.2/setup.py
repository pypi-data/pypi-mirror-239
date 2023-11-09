from setuptools import setup
from pg_logging import VERSION

DIST_NAME = "pg_logging"
__author__ = "baozilaji@gmail.com"

setup(
	name=DIST_NAME,
	version=VERSION,
	description="python game: logging",
	packages=[DIST_NAME],
	author=__author__,
	python_requires='>=3.9',
	install_requires=[
		'pg-environment>=0',
	],
)
