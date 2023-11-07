from setuptools import setup, find_packages, findall

print("packages: " + str(find_packages()))

setup(
    name='baykit',
    version='0.0.0',
    packages=find_packages(),
    author='Michisuke-P',
    author_email='michisukep@gmail.com',
    description='Baykit',
    license='MIT',
    python_requires=">=3.7",
    url='https://baykit.yokohama/',
    package_data={
    },
    install_requires=[
    ]
)

