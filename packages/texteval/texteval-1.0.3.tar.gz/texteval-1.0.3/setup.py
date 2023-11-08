from setuptools import setup, find_packages

setup(
    name="texteval",
    version='1.0.3',
    author='Dipankar',
    license='MIT',
    author_email='dipankarmedhi11@gmail.com',
    description='Small python package to calculate the sentence similarity metrics.',
    packages=find_packages(),
    readme='/home/dipankar/dev/projects/texteval/README.md',
    keywords='sentence similarity text python metrics cosine rouge bleu',
    install_requires = [
        'nltk==3.8.1',
        'rouge==1.0.1',
        'scikit-learn==1.3.2',

    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
    ],
    python_requires='>= 3.8',
)