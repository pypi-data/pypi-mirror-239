from setuptools import setup

setup(
    name='bizhi-framework',
    version='1.0.11',
    author='huangwenbin',
    description='bizhi project base framework',
    packages=['bizhi_framework','bizhi_framework.bizhi_web'],
    install_requires=[
        'seven-framework>=1.1.32'
    ],
    password='pypi-AgEIcHlwaS5vcmcCJGMzODEzYWZhLTUyY2EtNDU5OC1iZWNkLTJhNDgxNWViYzE2OQACKlszLCI3N2M3MWVlMy05NGQwLTRiZDEtYWI3YS00OTQ1ZTdlNmQwNzciXQAABiDFZYU2iKKyTt3EdZykU7KO7YnNwiPujkQ-q8m1q8Kvrg'
)

#python setup.py sdist bdist_wheel
#twine upload --username __token__ --password pypi-AgEIcHlwaS5vcmcCJGMzODEzYWZhLTUyY2EtNDU5OC1iZWNkLTJhNDgxNWViYzE2OQACKlszLCI3N2M3MWVlMy05NGQwLTRiZDEtYWI3YS00OTQ1ZTdlNmQwNzciXQAABiDFZYU2iKKyTt3EdZykU7KO7YnNwiPujkQ-q8m1q8Kvrg dist/*