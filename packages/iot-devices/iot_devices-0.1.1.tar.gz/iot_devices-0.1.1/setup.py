from setuptools import setup

setup(
    name='iot_devices',
    version='0.1.1',
    author="Daniel Dunn",
    author_email="dannydunn@eternityforest.com",
    packages=['iot_devices',],
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
