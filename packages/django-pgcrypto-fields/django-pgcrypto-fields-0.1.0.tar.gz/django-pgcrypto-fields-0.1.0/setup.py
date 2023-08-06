from setuptools import find_packages, setup


version = '0.1.0'


setup(
    name='django-pgcrypto-fields',
    packages=find_packages(),
    include_package_data=True,
    version=version,
    license='BSD',
    description='Encrypted fields dealing with pgcrypto postgres extension.',
    author='Incuna Ltd',
    author_email='admin@incuna.com',
    url='https://github.com/incuna/django-pgcrypto-fields',
)
