from distutils.core import setup
setup(
    name = 'saklient',
    version = '0.0.1.3',
    description = 'SAKURA Internet API Client Library',
    author='SAKURA Internet Inc.',
    author_email='dev-support-ml@sakura.ad.jp',
    url = 'http://cloud.sakura.ad.jp/',
    keywords = ['cloud'],
    package_dir = {'saklient':'saklient'},
    classifiers = [
        'Programming Language :: Python :: 3',
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
