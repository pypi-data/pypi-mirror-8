from setuptools import setup, find_packages

version = '0.5.3'

setup(name='instrumental',
      version=version,
      description="A condition/decision coverage tool for Python",
      long_description="""\
Instrumental automatically instruments your code to add function calls that
reveal execution characteristics. Instrumental can then monitor
execution of your code and report back to you on how your source was executed.

When you run a script with Instrumental, it will tell you which decisions and
conditions haven't been fully exercised. So for a decision in an if statement,
it will tell you if the decision only ever evaluated True or False. Instrumental
will also tell you if the conditions in boolean decisions (and, or) were ever
executed both True and False.

As an example: if you usually say

python setup.py nosetests

you can say

instrumental -rS -t <packagename> setup.py nosetests

where packagename is the name of your project's top-level package.

For more information visit `the Instrumental documentation <http://instrumental.readthedocs.org//en/latest>`_.

Announcements and discussion about instrumental can be found on the
"python-instrumental-discuss" google group.

Please file bug reports and enhancement requests `on bitbucket <http://bitbucket.org/desmaj/instrumental>`_.

""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='ast condition decision coverage',
      author='Matthew J Desmarais',
      author_email='matthew.desmarais@gmail.com',
      url='',
      license='GPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'astkit>=0.5.4',
        'mako',
        ],
      tests_require=[
        'fudge',
        ],
      entry_points="""
      [console_scripts]
      instrumental = instrumental.run:main
      instrumental-tools = instrumental.tools:main
      [nose.plugins]
      instrumental-tag = instrumental.plugins.nose.tag_test_cases:InstrumentalTagPlugin
      """,
      )
