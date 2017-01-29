from setuptools import setup

setup(
    name='Visual Search Engine',
    version='1.0',
    author='Hubert Legęć',
    packages=['visual_search_engine'],
    install_requires=['NumPy', 'cv2', 'flask', 'scipy', 'flask-pymongo', 'pymongo'],
    test_suite='tests'
)
