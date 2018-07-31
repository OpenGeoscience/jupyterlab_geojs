import setuptools

from jupyterlab_geojs import __version__

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name             = 'jupyterlab_geojs',
    version          = __version__,
    author           = 'john Tourtellott',
    author_email     = 'john.tourtellott@kitware.com',
    description      = 'A package for rendering GeoJS scenes in JupyterLab',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url              = 'https://github.com/OpenGeoscience/jupyterlab_geojs',
    license          = 'BSD',
    platforms        = 'Linux, Mac OS X, Windows',
    packages         = ['jupyterlab_geojs'],
    classifiers      = (
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3'
        ),
    keywords         = [
        'jupyter',
        'jupyterlab',
        'extension',
        'geojs'
        ]
    )
