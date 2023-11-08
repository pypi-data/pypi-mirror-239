import setuptools
PACKAGE_NAME = "bert-local"
package_dir = PACKAGE_NAME.replace("-", "_")

with open('README.md') as f:
    readme = f.read()

setuptools.setup(
    name=PACKAGE_NAME,  
    version='0.0.5',
    author="Circlez",
    author_email="info@circles.zone",
    description="PyPI Package for Circles Local Bert Python",
    long_description="This is a package for sharing common Logger function used in different repositories",
    long_description_content_type="text/markdown",
    url="https://github.com/circles",
    packages=[package_dir],
    package_dir={package_dir: f'{package_dir}/src'},
    package_data={package_dir: ['*.py']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    install_requires=[ 
        'mysql-connector>=2.2.9',
        'python-dotenv>=1.0.0',
        'pymysql>=1.1.0',
        'logzio-python-handler>=4.1.1',
        'pytest>=7.4.3',
        'logger-local>=0.0.71',
        'transformers>=4.35.0',
        'torch>=2.1.0',
        'numpy>=1.26.1',
        'pandas>=2.1.2'
    ],
 )
