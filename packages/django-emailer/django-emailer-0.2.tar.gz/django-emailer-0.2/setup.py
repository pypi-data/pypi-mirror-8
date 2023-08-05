from setuptools import find_packages, setup


setup(
    name='django-emailer',
    version='0.2',
    author='Evandro Myller',
    author_email='emyller@7ws.co',
    description='Template based email sending with SMTP connection management',
    url='https://github.com/7ws/django-emailer',
    install_requires=[
        'django >= 1.5',
    ],
    packages=find_packages(),
    include_package_data=True,
    keywords=['django', 'email', 'smtp'],
    classifiers=[
        'Framework :: Django',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python',
        'Topic :: Software Development',
    ],
)
