from setuptools import setup


setup(
        name = 'fastqp',
        provides = 'fastqp',
        version = "0.1.5",
        author = 'Matthew Shirley',
        author_email = 'mdshw5@gmail.com',
        url = 'http://mattshirley.com',
        description = 'Simple NGS read quality assessment using Python',
        license = 'MIT',
        packages = ['fastqp', 'fastqp.backports'],
        install_requires=['six', 'matplotlib', 'numpy', 'pyfaidx'],
        entry_points = { 'console_scripts': [ 'fastqp = fastqp.cli:main' ] },
        classifiers = [
                "Development Status :: 4 - Beta",
                "License :: OSI Approved :: MIT License",
                "Environment :: Console",
                "Intended Audience :: Science/Research",
                "Natural Language :: English",
                "Operating System :: Unix",
                "Programming Language :: Python :: 2.6",
                "Programming Language :: Python :: 2.7",
                "Programming Language :: Python :: 3.3",
                "Programming Language :: Python :: 3.4",
                "Topic :: Scientific/Engineering :: Bio-Informatics"
        ]
)
