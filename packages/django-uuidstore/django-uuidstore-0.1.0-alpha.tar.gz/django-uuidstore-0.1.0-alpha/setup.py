from setuptools import setup
from uuidstore import __version__

setup(
    name="django-uuidstore",
    version=__version__,
    author="Mike Hurt",
    author_email="mike@mhtechnical.net",
    description="Site-wide UUIDs for Django projects",
    license="MIT",
    keywords="django uuid orm model utility",
    url="https://bitbucket.org/mhurt/django-uuidstore",
    packages=['uuidstore'],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        # "Programming Language :: Python :: 2",
        # "Programming Language :: Python :: 3",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    install_requires=[
        'django-uuid-pk >= 0.2',
        'Django >= 1.5',
        ],
    # test_suite='',
    tests_require=[
        'django-uuid-pk >= 0.2',
        'Django >= 1.5',
        ]
)
