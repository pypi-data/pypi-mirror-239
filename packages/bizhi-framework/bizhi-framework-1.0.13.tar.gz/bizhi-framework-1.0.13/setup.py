from setuptools import setup

setup(
    name='bizhi-framework',
    version='1.0.13',
    author='huangwenbin',
    description='bizhi project base framework',
    packages=['bizhi_framework','bizhi_framework.bizhi_web'],
    install_requires=[
        'seven-framework>=1.1.32'
    ],
    password='pypi-AgEIcHlwaS5vcmcCJGMzODEzYWZhLTUyY2EtNDU5OC1iZWNkLTJhNDgxNWViYzE2OQACKlszLCI3N2M3MWVlMy05NGQwLTRiZDEtYWI3YS00OTQ1ZTdlNmQwNzciXQAABiDFZYU2iKKyTt3EdZykU7KO7YnNwiPujkQ-q8m1q8Kvrg'
)

#python setup.py sdist bdist_wheel
#twine upload --username __token__ --password pypi-AgEIcHlwaS5vcmcCJDA4NTVkOTQ2LTIzMDktNDFmOS1hYzk5LTI0NjFjZmU2ZjgxMAACF1sxLFsiYml6aGktZnJhbWV3b3JrIl1dAAIsWzIsWyIwOWIwOWNlOC01YjkwLTQ2ZTAtOGVlNS1jYTUwODA3OTViMWYiXV0AAAYgftFLJuAlJj39FlLn_HFcqMBz8bbcbgUe2ioto84w-nA dist/*