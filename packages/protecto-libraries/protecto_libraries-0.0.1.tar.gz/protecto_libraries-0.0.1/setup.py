import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='protecto_libraries',
    version='0.0.1',
    author='Protecto',
    author_email='developer@protecto.ai',
    description='Tokenisation Package',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://bitbucket.org/onedpo/privacy_vault_library/src/develop/',
    project_urls={
        "Bug Tracker": "https://bitbucket.org/onedpo/privacy_vault_library/src/develop/issues"
    },
    license='MIT',
    packages=['protecto_privacy_vault'],
    install_requires=['requests>=2.26.0'],

)
