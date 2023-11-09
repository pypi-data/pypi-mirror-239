from setuptools import setup, find_packages

setup(
    name="django_query_analyzer",
    version="0.0.7",
    description="Django app for query analysis and monitoring",
    author="Muhammed Shaheen",
    author_email="muhammedshaheen.tkb@gmail.com",
    license='MIT',
    # package_data={
    #         "django_query_analyzer": ["templates/django_query_analyzer/*.html"],
    # },
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Django",
    ],

)
