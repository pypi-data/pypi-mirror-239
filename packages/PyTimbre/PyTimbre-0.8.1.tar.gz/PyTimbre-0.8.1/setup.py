from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

    with open('HISTORY.md') as history_file:
        HISTORY = history_file.read()

        with open('LICENSE.txt') as license_file:
            LICENSE = license_file.read()

setup(
    name='PyTimbre',
    version='0.8.1',
    description='Python conversion of Timbre Toolbox',
    long_description_content_type="text/markdown",
    long_description=README + '\n\n' + HISTORY + '\n\n' + LICENSE,
    license='MIT',
    packages=find_packages('src'),
    author='Dr. Frank Mobley',
    author_email='frank.mobley.1@afrl.af.mil',
    keywords=['machine learning', 'feature extraction', 'MATLAB', 'audio'],
    url='https://gitlab.com/python-audio-feature-extraction/pytimbre',
    download_url='',
    install_requires=[
        'numpy>=1.21.5',
        'pandas>=1.4.3',
        'scipy>=1.9.1',
        'statsmodels>=0.13.2',
        'colorednoise>=2.1.0',
        'python_speech_features~=0.6'
    ],
    package_dir={'': 'src'}
)
