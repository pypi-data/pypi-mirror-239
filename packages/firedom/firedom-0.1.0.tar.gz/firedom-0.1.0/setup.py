from setuptools import setup

setup(
    name='firedom',
    version='0.1.0',
    description='Simple Firestore ORM',
    url='https://github.com/afuenzalida/firedom',
    author='Andrés Fuenzalida',
    author_email='a.fuenzalida1494@gmail.com',
    license='MIT',
    packages=['firedom'],
    install_requires=[
        'google-cloud-firestore>=2.13.1',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.11',
    ],
)
