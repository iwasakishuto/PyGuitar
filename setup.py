# coding: utf-8
# ref: https://packaging.python.org/tutorials/packaging-projects/
import os
import setuptools
import guitar

DESCRIPTION = 'PyGuitar generates an easy-to-practice chord book.'

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

def setup_package():
    metadata = dict(
        name='PyGuitar',
        version=guitar.__version__,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type='text/markdown',
        author='Shuto Iwasaki',
        author_email='cabernet.rock@gmail.com',
        license='MIT',
        project_urls={
            'Source Code': 'https://github.com/iwasakishuto/PyGuitar',
        },
        packages=setuptools.find_packages(),
        package_data={'guitar': ['data/*']},
        python_requires=">=3.6",
        install_requires=[
            # 'numpy>=1.15.1',
            'matplotlib>=2.2.4',
            # 'seaborn>=0.10.0',
        ],
        extras_require={
          'tests': ['pytest'],
        },
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Other Audience',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.6',
            'Topic :: Software Development :: Libraries',
            'Topic :: Software Development :: Libraries :: Python Modules',
        ],
    )
    setuptools.setup(**metadata)

if __name__ == "__main__":
    setup_package()
