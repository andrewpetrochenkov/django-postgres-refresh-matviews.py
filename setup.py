import setuptools

setuptools.setup(
    name='django-postgres-refresh-matviews',
    version='2020.12.5',
    install_requires=open('requirements.txt').read().splitlines(),
    packages=setuptools.find_packages()
)
