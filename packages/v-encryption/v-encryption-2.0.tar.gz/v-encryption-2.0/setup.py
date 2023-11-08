from setuptools import setup, find_packages
 
setup(
    include_package_data=True,
	name="v-encryption",
	version="2.0",
	packages=find_packages(), # permet de récupérer tout les fichiers 
	description="(De)cryption software. Allows you to encrypt or decrypt text based on different encryption keys.",
	url="https://encryption.nexcord.pro/",
	author="V / Lou du Poitou",
	license="ISC",
	python_requires=">=3.9.7",
    install_requires=["requests"],
    requires=["requests"]
)