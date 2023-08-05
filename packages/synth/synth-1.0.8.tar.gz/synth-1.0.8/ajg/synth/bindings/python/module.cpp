//  (C) Copyright 2014 Alvaro J. Genial (http://alva.ro)
//  Use, modification and distribution are subject to the Boost Software License, Version 1.0.
//  (See accompanying file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt).

// TODO? #include <boost/python/detail/wrap_python.hpp>
#include <Python.h>              // This prevents a strange macro issue in pyport.h.
#include <datetime.h>            // Not included by default by Python.h.
#include <ajg/synth/support.hpp> // Must come ahead of everything except Python.h.

#include <boost/python.hpp>
#include <boost/noncopyable.hpp>

#include <ajg/synth/bindings/python/binding.hpp>

BOOST_PYTHON_MODULE(synth) {
    PyDateTime_IMPORT;
    namespace s  = ajg::synth;
    namespace py = boost::python;

    typedef s::default_traits<AJG_SYNTH_CONFIG_DEFAULT_CHAR_TYPE>                   traits_type;
    typedef s::bindings::python::binding<traits_type>                               binding_type;

    binding_type::prime();

    py::def("version", s::bindings::python::version);

    py::scope().attr("CACHE_NONE")        = static_cast<std::size_t>(s::caching_none);
    py::scope().attr("CACHE_ALL")         = static_cast<std::size_t>(s::caching_all);
    py::scope().attr("CACHE_PATHS")       = static_cast<std::size_t>(s::caching_paths);
    py::scope().attr("CACHE_BUFFERS")     = static_cast<std::size_t>(s::caching_buffers);
    py::scope().attr("CACHE_STRINGS")     = static_cast<std::size_t>(s::caching_strings);
    py::scope().attr("CACHE_PER_THREAD")  = static_cast<std::size_t>(s::caching_per_thread);
    py::scope().attr("CACHE_PER_PROCESS") = static_cast<std::size_t>(s::caching_per_process);

    /* XXX: Doesn't work with flag-like (bitwise) enums.
    py::enum_<binding_type::caching_type>("caching")
        .value("NONE", s::caching_none)
        ;
    */

    py::class_<binding_type, boost::noncopyable>("Template", binding_type::constructor_type())
        .def("render_to_file",      &binding_type::render_to_file)
        .def("render_to_path",      &binding_type::render_to_path)
        .def("render_to_string",    &binding_type::render_to_string)
        // TODO: Use a property instead.
        .def("set_default_options", &binding_type::set_default_options).staticmethod("set_default_options")
        ;
}
