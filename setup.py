from setuptools import setup

setup(
    name="SpatialTemporalImage-CMPT365",
    version="1.0",
    description="Generates and analyzes STIs for videos and creates"
                "a enhanced video.",
    author="Maheeppartap Singh""Conor Murphy",
    packages=['src'],
    install_requires=[
        'opencv-python',
        'matplotlib',
        'numpy'
    ]
)