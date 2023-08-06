from distutils.core import setup


setup(
    name='crosservice',
    version='0.2.0',
    packages=['crosservice'],
    install_requires=open('requirements.txt').read(),
    license='GPL',
    author='derfenix',
    author_email='derfenix@gmail.com',
    description='Cross-service comunication python library',
    url='https://github.com/derfenix/crosservice',
    download_url='https://github.com/derfenix/crosservice/archive/v.0.2.0'
                 '.tar.gz',
    keywords=['testing', 'logging', 'example'],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
    ],
)
