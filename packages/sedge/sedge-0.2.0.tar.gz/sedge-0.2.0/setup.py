from setuptools import setup, find_packages

dev_requires = ['flake8', 'nose']
install_requires = ['requests']

setup(
    name = "sedge",
    version = "0.2.0",
    packages = find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    extras_require = {
        'dev': dev_requires
    },
    install_requires = install_requires,
    entry_points = {
        'console_scripts': [
            'sedge = sedge.cli:main',
        ],
    }
)
