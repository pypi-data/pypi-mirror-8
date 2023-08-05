from setuptools import setup


setup(
    name='alation',
    author='Alation Engineering',
    author_email='engineering@alation.com',
    version='0.1.13',
    packages=['alation'],
    entry_points={
        'console_scripts': [
            'alation-setup = alation.main:setup',
            'alation-query = alation.main:print_sql',
            'alation-result = alation.main:print_result'
        ]
    }
)
