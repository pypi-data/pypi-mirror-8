import ez_setup
ez_setup.use_setuptools()
from setuptools import setup, find_packages


builtin_plugins = [
    'CommandLineSupplier = contexts.plugins.test_target_suppliers:CommandLineSupplier',
    'ExitCodeReporter = contexts.plugins.reporting:ExitCodeReporter',
    'Shuffler = contexts.plugins.shuffling:Shuffler',
    'Importer = contexts.plugins.importing:Importer',
    'AssertionRewritingImporter = contexts.plugins.importing.assertion_rewriting:AssertionRewritingImporter',
    'DecoratorBasedIdentifier = contexts.plugins.identification.decorators:DecoratorBasedIdentifier',
    'NameBasedIdentifier = contexts.plugins.identification:NameBasedIdentifier',
    'TeamCityReporter = contexts.plugins.reporting.teamcity:TeamCityReporter',
    'DotsReporter = contexts.plugins.reporting.cli:DotsReporter',
    'VerboseReporter = contexts.plugins.reporting.cli:VerboseReporter',
    'StdOutCapturingReporter = contexts.plugins.reporting.cli:StdOutCapturingReporter',
    'Colouriser = contexts.plugins.reporting.cli:Colouriser', 'UnColouriser = contexts.plugins.reporting.cli:UnColouriser',
    'FailuresOnlyMaster = contexts.plugins.reporting.cli:FailuresOnlyMaster',
    'FailuresOnlyBefore = contexts.plugins.reporting.cli:FailuresOnlyBefore',
    'FailuresOnlyAfter = contexts.plugins.reporting.cli:FailuresOnlyAfter',
    'FinalCountsReporter = contexts.plugins.reporting.cli:FinalCountsReporter',
    'TimedReporter = contexts.plugins.reporting.cli:TimedReporter',
]


setup(
    name="Contexts",
    version="0.10",
    author="Benjamin Hodgson",
    author_email="benjamin.hodgson@huddle.net",
    url="https://github.com/benjamin-hodgson/Contexts",
    description="""Dead simple descriptive testing for Python. No custom decorators, no context managers, no '.feature' files, no fuss.""",
    long_description="""See the Github project page (https://github.com/benjamin-hodgson/Contexts) for more information.""",
    package_dir={'': 'src'},
    packages=find_packages('src'),
    install_requires=["setuptools >= 1.0"],
    extras_require={'colour': ["colorama >= 0.2.7"]},
    entry_points={
        'console_scripts': ['run-contexts=contexts.__main__:cmd'],
        'contexts.plugins': builtin_plugins,
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Topic :: Software Development",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Software Development :: Testing"
    ]
)
