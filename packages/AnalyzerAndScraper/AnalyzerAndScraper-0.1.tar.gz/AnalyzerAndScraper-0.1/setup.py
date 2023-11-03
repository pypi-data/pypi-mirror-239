from setuptools import setup, find_packages

setup(
    name='AnalyzerAndScraper',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
        'beautifulsoup4',
        'textblob',
    ],
    author='Alvaro and Rodrigo',
    author_email='alvaro.ortega@alumni.mondragon.edu',
    description='Una biblioteca para analizar páginas web y sentimientos de texto.',
    url='https://github.com/rodrigocolomo/Scrape_analize',
)
