from setuptools import setup, find_packages

setup(
    name='django-facebook-pages-statistic',
    version=__import__('facebook_pages_statistic').__version__,
    description='Application for storing Facebook Pages statistic for different timesnaps',
    long_description=open('README.md').read(),
    author='ramusus',
    author_email='ramusus@gmail.com',
    url='https://github.com/ramusus/django-facebook-pages-statistic',
    download_url='http://pypi.python.org/pypi/django-facebook-pages-statistic',
    license='BSD',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False, # because we're including media that Django needs
    install_requires=[
        'django-facebook-api>=0.1.22',
        'django-facebook-pages',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
