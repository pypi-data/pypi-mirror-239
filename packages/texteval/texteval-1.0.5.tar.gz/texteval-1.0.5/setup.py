from setuptools import setup, find_packages

with open("/home/dipankar/dev/projects/texteval/README.md", "r") as f:
    description = f.read()

setup(
    name="texteval",
    version='1.0.5',
    author='Dipankar',
    license='MIT',
    author_email='dipankarmedhi11@gmail.com',
    description='Small python package to calculate the sentence similarity metrics.',
    long_description=description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
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