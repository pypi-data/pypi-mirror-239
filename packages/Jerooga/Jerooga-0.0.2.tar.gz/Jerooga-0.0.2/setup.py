from setuptools import setup, find_packages

setup(
    name="Jerooga",
    version="0.0.2",
    packages=find_packages(),
    include_package_data=True,
    package_data={"Jerooga": ["Textures/*"]},  # Specify the texture files
    install_requires=[
        # List your package dependencies here
        'pygame'
    ],
)
