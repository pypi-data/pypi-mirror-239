from setuptools import setup

readme =open("./README.md", "r")

setup(
    
    name='pruebalibreria',
    packages = ['pruebalibreria'],
    version = '0.2',
    description = 'Metodo MTR',
    long_description = readme.read(),
    long_description_content_type = 'text/markdown',
    author_email = 'ramosjack066@gmail.com',
    keywords=['testing','logging', 'example'],
    classifiers = [],
    license= 'MIT',
    include_package_data = True,
    install_requires = [
        'pandas == 2.1.2',
        'sklearn ==0.0.post10'
    ],
)
