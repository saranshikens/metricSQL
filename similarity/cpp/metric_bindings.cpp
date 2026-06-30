#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "metric_ght.h"

namespace py = pybind11;

PYBIND11_MODULE(metric_ght_cpp, m)
{
    py::class_<MetricGHT>(
        m,
        "MetricGHT"
    )

    .def(
        py::init<int>()
    )

    .def(
        "build",
        &MetricGHT::build
    )

    .def(
        "top_k_search",
        &MetricGHT::top_k_search
    );
}