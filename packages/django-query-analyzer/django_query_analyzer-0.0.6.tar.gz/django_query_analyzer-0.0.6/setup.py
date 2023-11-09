from setuptools import setup, find_packages

setup(
    name="django_query_analyzer",
    version="0.0.6",
    description="Django app for query analysis and monitoring",
    author="Muhammed Shaheen",
    author_email="muhammedshaheen.tkb@gmail.com",
    license='MIT',
    # package_data={
    #         "django_query_analyzer": ["templates/django_query_analyzer/*.html"],
    # },
    package_dir={"": "django_query_analyzer"},
    packages=find_packages(where="src"),
    include_package_data=True,
    install_requires=[
        "Django",
        # Add any other dependencies here
    ],

)
