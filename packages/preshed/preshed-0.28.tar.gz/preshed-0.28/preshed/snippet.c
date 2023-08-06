#include <stddef.h>
#include <stdint.h>

typedef uint64_t __pyx_t_7preshed_4maps_key_t;

struct __pyx_t_7preshed_4maps_Cell {
  __pyx_t_7preshed_4maps_key_t key;
  void *value;
};


static struct __pyx_t_7preshed_4maps_Cell *__pyx_f_7preshed_4maps__find_cell(struct __pyx_t_7preshed_4maps_Cell *__pyx_v_cells, size_t const __pyx_v_size, __pyx_t_7preshed_4maps_key_t const __pyx_v_key) {
  size_t __pyx_v_i;
  struct __pyx_t_7preshed_4maps_Cell *__pyx_r;
  int __pyx_t_1;
  int __pyx_t_2;

  /* "preshed/maps.pyx":140
 * cdef inline Cell* _find_cell(Cell* cells, const size_t size, const key_t key) nogil:
 *     # Modulo for powers-of-two via bitwise &
 *     cdef size_t i = (key & (size - 1))             # <<<<<<<<<<<<<<
 *     while cells[i].key != 0 and cells[i].key != key:
 *         i = (i + 1) & (size - 1)
 */
  __pyx_v_i = (__pyx_v_key & (__pyx_v_size - 1));

  /* "preshed/maps.pyx":141
 *     # Modulo for powers-of-two via bitwise &
 *     cdef size_t i = (key & (size - 1))
 *     while cells[i].key != 0 and cells[i].key != key:             # <<<<<<<<<<<<<<
 *         i = (i + 1) & (size - 1)
 *     return &cells[i]
 */
  while (1) {
    __pyx_t_2 = (((__pyx_v_cells[__pyx_v_i]).key != 0) != 0);
    if (__pyx_t_2) {
      goto __pyx_L6_next_and;
    } else {
      __pyx_t_1 = __pyx_t_2;
      goto __pyx_L5_bool_binop_done;
    }
    __pyx_L6_next_and:;
    __pyx_t_2 = (((__pyx_v_cells[__pyx_v_i]).key != __pyx_v_key) != 0);
    __pyx_t_1 = __pyx_t_2;
    __pyx_L5_bool_binop_done:;
    if (!__pyx_t_1) break;

    /* "preshed/maps.pyx":142
 *     cdef size_t i = (key & (size - 1))
 *     while cells[i].key != 0 and cells[i].key != key:
 *         i = (i + 1) & (size - 1)             # <<<<<<<<<<<<<<
 *     return &cells[i]
 * 
 */
    __pyx_v_i = ((__pyx_v_i + 1) & (__pyx_v_size - 1));
  }

  /* "preshed/maps.pyx":143
 *     while cells[i].key != 0 and cells[i].key != key:
 *         i = (i + 1) & (size - 1)
 *     return &cells[i]             # <<<<<<<<<<<<<<
 * 
 * 
 */
  __pyx_r = (&(__pyx_v_cells[__pyx_v_i]));
  goto __pyx_L0;

  /* "preshed/maps.pyx":138
 * 
 * @cython.cdivision
 * cdef inline Cell* _find_cell(Cell* cells, const size_t size, const key_t key) nogil:             # <<<<<<<<<<<<<<
 *     # Modulo for powers-of-two via bitwise &
 *     cdef size_t i = (key & (size - 1))
 */

  /* function exit code */
  __pyx_L0:;
  return __pyx_r;
}

