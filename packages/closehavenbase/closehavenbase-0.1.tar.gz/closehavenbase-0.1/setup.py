from setuptools import setup, find_packages

setup(
    name="closehavenbase",
    version="0.1",
    author='Test',
    author_email='raj.p@logicrays.com',
    description='Custom exception handiling ',
    packages=find_packages(),
    install_requires = [
        'fastapi==0.103.2',
        'pydantic==2.4.2'
    ]
)
