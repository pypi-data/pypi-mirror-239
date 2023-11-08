from setuptools import setup, find_packages

setup(
    name='flask-fusion',
    version='0.1',
    description='A simple Flask library for UI components',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Flask',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
