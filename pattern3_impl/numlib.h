#ifndef NUMLIB_H
#define NUMLIB_H

#include <stddef.h>
#include <stdint.h>

#define NUMILIB_SUCCESS        (0)   /* 成功 */
#define NUMILIB_ERR_NULL_PTR   (-1)  /* NULLポインタ引数 */
#define NUMILIB_ERR_INVALID_N  (-2)  /* n <= 0 または制限超過 */
#define NUMILIB_ERR_SINGULAR   (-3)  /* 特異行列（ピボット < 1e-12） */

int bubble_sort_i32(int32_t *arr, size_t n);
int gauss_eliminate(double **A, double *b, size_t n, double *x);

#endif /* NUMLIB_H */