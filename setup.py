from setuptools import Extension, setup
import numpy

setup(
    ext_modules=[
        Extension(
            name="neighborhood_correlation.nchelparr",  # as it would be imported
                               # may include packages/namespaces separated by `.`

            sources=["src/nchelparr.c"], # all sources are compiled into a single binary file

            include_dirs=[numpy.get_include()], 
        ),
    ]
)
