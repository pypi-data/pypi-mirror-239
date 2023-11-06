from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mdhub",
    version="0.1.0",
    description="Convert Markdown files to styled HTML with a GitHub-like appearance. Easily switch between light and dark modes.",
    author="GlizzyKingDreko",  # Update this
    author_email="glizzykingdreko@protonmail.com",  # Update this
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        'beautifulsoup4',
        'chardet',
        'mistune',
        'Pygments'
    ],
    entry_points={
        "console_scripts": [
            "mdhub = mdhub.cli:main",
        ],
    },
    package_data={
        'mdhub': ['models/*.css'],
    },
    include_package_data=True,
)
