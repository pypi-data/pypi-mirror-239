#include "../pykdt.hpp"

namespace napf {

void init_float_trees(py::module_& m) {
  add_kdt_pyclass<float, 1, 1>(m, "KDTfD1L1");
  add_kdt_pyclass<float, 1, 2>(m, "KDTfD1L2");
  add_kdt_pyclass<float, 2, 1>(m, "KDTfD2L1");
  add_kdt_pyclass<float, 2, 2>(m, "KDTfD2L2");
  add_kdt_pyclass<float, 3, 1>(m, "KDTfD3L1");
  add_kdt_pyclass<float, 3, 2>(m, "KDTfD3L2");
  add_kdt_pyclass<float, 4, 1>(m, "KDTfD4L1");
  add_kdt_pyclass<float, 4, 2>(m, "KDTfD4L2");
  add_kdt_pyclass<float, 5, 1>(m, "KDTfD5L1");
  add_kdt_pyclass<float, 5, 2>(m, "KDTfD5L2");
  add_kdt_pyclass<float, 6, 1>(m, "KDTfD6L1");
  add_kdt_pyclass<float, 6, 2>(m, "KDTfD6L2");
  add_kdt_pyclass<float, 7, 1>(m, "KDTfD7L1");
  add_kdt_pyclass<float, 7, 2>(m, "KDTfD7L2");
  add_kdt_pyclass<float, 8, 1>(m, "KDTfD8L1");
  add_kdt_pyclass<float, 8, 2>(m, "KDTfD8L2");
  add_kdt_pyclass<float, 9, 1>(m, "KDTfD9L1");
  add_kdt_pyclass<float, 9, 2>(m, "KDTfD9L2");
  add_kdt_pyclass<float, 10, 1>(m, "KDTfD10L1");
  add_kdt_pyclass<float, 10, 2>(m, "KDTfD10L2");
  add_kdt_pyclass<float, 11, 1>(m, "KDTfD11L1");
  add_kdt_pyclass<float, 11, 2>(m, "KDTfD11L2");
  add_kdt_pyclass<float, 12, 1>(m, "KDTfD12L1");
  add_kdt_pyclass<float, 12, 2>(m, "KDTfD12L2");
  add_kdt_pyclass<float, 13, 1>(m, "KDTfD13L1");
  add_kdt_pyclass<float, 13, 2>(m, "KDTfD13L2");
  add_kdt_pyclass<float, 14, 1>(m, "KDTfD14L1");
  add_kdt_pyclass<float, 14, 2>(m, "KDTfD14L2");
  add_kdt_pyclass<float, 15, 1>(m, "KDTfD15L1");
  add_kdt_pyclass<float, 15, 2>(m, "KDTfD15L2");
  add_kdt_pyclass<float, 16, 1>(m, "KDTfD16L1");
  add_kdt_pyclass<float, 16, 2>(m, "KDTfD16L2");
  add_kdt_pyclass<float, 17, 1>(m, "KDTfD17L1");
  add_kdt_pyclass<float, 17, 2>(m, "KDTfD17L2");
  add_kdt_pyclass<float, 18, 1>(m, "KDTfD18L1");
  add_kdt_pyclass<float, 18, 2>(m, "KDTfD18L2");
  add_kdt_pyclass<float, 19, 1>(m, "KDTfD19L1");
  add_kdt_pyclass<float, 19, 2>(m, "KDTfD19L2");
  add_kdt_pyclass<float, 20, 1>(m, "KDTfD20L1");
  add_kdt_pyclass<float, 20, 2>(m, "KDTfD20L2");
}

} // namespace napf
