from setuptools import setup

setup(
    name="stiDetection",
    version="1.0",
    description="Generates and analyzes STIs for videos and creates"
                "a enhanced video.",
    author="Maheeppartap Singh""Conor Murphy",
    packages=['src'
               ],
    install_requires=[
        'opencv-python',
        'matplotlib',
        'numpy'
    ],
    scripts=['src/CLI.py',
             'src/transitionDetector.py',
             'src/videoEnhancer.py',
             'src/transitions.py',
             'src/randomColourGen.py',
             'src/videoBreakdown.py',
             'src/videoSpecs.py'
             ],

    entry_points={
      'console_scripts': [
          'TRANSformer = CLI:main'
      ]
    }
)

