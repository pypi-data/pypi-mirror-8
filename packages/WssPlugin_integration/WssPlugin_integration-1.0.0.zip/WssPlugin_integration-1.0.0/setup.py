from setuptools import setup

setup(
    name='WssPlugin_integration',
    version='1.0.0',
    description='Wss python pluging for creating/updating wss organization inventory',
    author='Yossi Weinberg',
    author_email='yossi.weinberg@whitesourcesoftware.com',
    install_requires=["requests == 2.3.0", "enum34 == 1.0", "jsonpickle == 0.7.2"],
    packages=['plugin', 'agent', 'agent.client', 'agent.api', 'agent.api.dispatch', 'agent.api.model'],
    include_package_data=True,
    license="Apache 2.0"
)
