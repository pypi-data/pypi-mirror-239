from setuptools import setup, find_packages

# __version__ = open('plantseg/__version__.py', encoding='utf-8').read()
long_description = open('README.md', 'r', encoding='utf-8').read()

setup(
    name='run-stardist',  # Replace with your own username
    version='0.1.1',
    author='Qin Yu',
    author_email='qin.yu@embl.de',
    license='bsd-3-clause',
    description='Train and use StarDist models',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/qin-yu/ovules-instance-segmentation',
    packages=find_packages(),
    install_requires=[
        'tensorflow[and-cuda]',
        'stardist',
        'wandb',
        'pydantic==1.*',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Image Processing',
    ],
    keywords='stardist image-processing deep-learning bioimage-analysis nucleus-segmentation',
    python_requires='>=3.10, <3.12',  # >=3.10 for pydantic and <3.12 for tensorflow
    entry_points={
        'console_scripts': [
            'train-stardist=runstardist.train:main',
            'predict-stardist=runstardist.predict:main',
        ],
    },
)

# bump-my-version bump --current-version 0.1.0 patch setup.py
