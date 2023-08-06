from setuptools import setup


setup(
    description="HipChat support for the Python logging module",
    name='hiplogging',
    url='https://github.com/invernizzi/hiplogging',
    version='1.0',
    packages=['hiplogging'],
    author='Luca Invernizzi',
    author_email='invernizzi.l@gmail.com',
    license='MIT',
    keywords=['hipchat', 'log', 'logging'],
    download_url = 'https://github.com/invernizzi/hiplogging/tarball/1.0',
    install_requires=['python-simple-hipchat'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],
)
