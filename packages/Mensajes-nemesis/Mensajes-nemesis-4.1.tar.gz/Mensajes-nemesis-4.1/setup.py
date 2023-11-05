from setuptools import setup, find_packages

setup(
	name="Mensajes-nemesis",
	version="4.1",
	description="Este es un paquete de ejemplo",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
	author="Smarquez",
	author_email="snemesis@gmail.com",
	url="http://nemesis.net",
    license_files=['LINCENSE'],
    packages=find_packages(),
    test_suite='tests',
    install_requires=[paquete.strip() for paquete in open('requirements.txt').readlines()],
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Utilities'
 	]
)