from setuptools import setup, find_packages

setup(
    name='iot_devices',
    version='0.1.12',
    author="Daniel Dunn",
    author_email="dannydunn@eternityforest.com",
    packages=find_packages(),
    package_data={'':["*.json"]},
    license='MIT',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/EternityForest/iot_devices",
    dependencies = [
        "paho.mqtt",
        "urwid",
        "scullery",
        "yeelight",
        "colorzero"
    ]
)
