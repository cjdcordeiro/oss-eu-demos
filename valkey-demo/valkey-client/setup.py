from setuptools import setup, find_packages
setup(
    name="valkey-client",
    version="0.1",
    packages=["valkey_client"],
    entry_points={
        "console_scripts": [
            "valkey_client=valkey_client.main:main"]
        },
)
