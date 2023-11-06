from setuptools import setup, find_packages

setup(
    name="monsterclient",
    version="1.0.3",
    packages=find_packages(),
    install_requires=["click", "requests", "curlify"],
    entry_points="""
      [console_scripts]
      monster=monsterclient.monster:main
      """,
)
