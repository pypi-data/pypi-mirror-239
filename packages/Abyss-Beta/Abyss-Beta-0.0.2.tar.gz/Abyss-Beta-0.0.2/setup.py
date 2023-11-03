from setuptools import setup


setup(
    name='Abyss-Beta',
    version='0.0.2',
    description='The GUI for the Nebula CLI',
    url='https://github.com/setoyuma/NebulaEngine',
    author='Setoichi',
    author_email='setoichi.dev@gmail.com',
    license='MIT',
    packages=['Nebula'],
    install_requires=[
        'pygame-ce',
        'pygame-gui'
    ],
    classifiers=[
        'Development Status :: 4 - Beta'
    ],
)