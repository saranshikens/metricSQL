from setuptools import setup
from pybind11.setup_helpers import (
    Pybind11Extension,
    build_ext
)

ext_modules = [

    Pybind11Extension(

        "ght_cpp",

        [
            "bindings.cpp",
            "ght.cpp"
        ],

        cxx_std=17
    ),

    Pybind11Extension(

        "metric_ght_cpp",

        [
            "metric_bindings.cpp",
            "metric_ght.cpp"
        ],

        cxx_std=17
    )
]

setup(

    name="metric_cpp",

    ext_modules=ext_modules,

    cmdclass={
        "build_ext": build_ext
    }
)