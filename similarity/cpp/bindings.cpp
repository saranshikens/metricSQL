#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "ght.h"

namespace py = pybind11;

PYBIND11_MODULE(ght_cpp, m) {

    py::class_<GHTIndex>(m, "GHTIndex")

        .def(py::init<int>())

        .def(
            "build",
            &GHTIndex::build
        )

        .def(
            "nearest_neighbor",
            &GHTIndex::nearest_neighbor
        )

        .def(
            "top_k_search",
            &GHTIndex::top_k_search
        );
}