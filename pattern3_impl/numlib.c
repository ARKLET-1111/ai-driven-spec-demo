#include "numlib.h"
#include <stddef.h>
#include <stdint.h>

int bubble_sort_i32(int32_t *arr, size_t n)
{
    /* Check for NULL pointer when n > 0 */
    if (arr == NULL && n > 0) {
        return NUMILIB_ERR_NULL_PTR;
    }
    /* Check for invalid n (negative) - though size_t is unsigned, keep for future */
    if (n < 0) {
        return NUMILIB_ERR_INVALID_N;
    }
    /* If n == 0, do nothing and return success */
    if (n == 0) {
        return NUMILIB_SUCCESS;
    }

    /* Bubble sort (stable) */
    for (size_t i = 0; i < n - 1; i++) {
        int swapped = 0;
        for (size_t j = 0; j < n - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                /* Swap arr[j] and arr[j+1] */
                int32_t temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
                swapped = 1;
            }
        }
        /* If no swaps, array is sorted */
        if (!swapped) {
            break;
        }
    }

    return NUMILIB_SUCCESS;
}

int gauss_eliminate(double **A, double *b, size_t n, double *x)
{
    /* Check for NULL pointers when n > 0 */
    if (n > 0) {
        if (A == NULL || b == NULL || x == NULL) {
            return NUMILIB_ERR_NULL_PTR;
        }
    }
    /* Check n range */
    if (n == 0 || n > 16) {
        return NUMILIB_ERR_INVALID_N;
    }

    /* Forward elimination with partial pivoting */
    for (size_t col = 0; col < n; col++) {
        /* Find pivot row: max absolute value in column col from row col to n-1 */
        size_t pivot_row = col;
        double max_val = A[col][col] >= 0 ? A[col][col] : -A[col][col];
        for (size_t row = col + 1; row < n; row++) {
            double val = A[row][col] >= 0 ? A[row][col] : -A[row][col];
            if (val > max_val) {
                max_val = val;
                pivot_row = row;
            }
        }

        /* Check if pivot is too small (singular matrix) */
        if (max_val < 1e-12) {
            return NUMILIB_ERR_SINGULAR;
        }

        /* Swap current row with pivot row if needed */
        if (pivot_row != col) {
            /* Swap rows in A */
            double *temp_A = A[col];
            A[col] = A[pivot_row];
            A[pivot_row] = temp_A;
            /* Swap elements in b */
            double temp_b = b[col];
            b[col] = b[pivot_row];
            b[pivot_row] = temp_b;
        }

        /* Eliminate below */
        for (size_t row = col + 1; row < n; row++) {
            double factor = A[row][col] / A[col][col];
            for (size_t inner_col = col; inner_col < n; inner_col++) {
                A[row][inner_col] -= factor * A[col][inner_col];
            }
            b[row] -= factor * b[col];
        }
    }

    /* Back substitution */
    for (size_t row = 0; row < n; row++) {
        /* Start from last row and move upwards */
        size_t i = n - row - 1;
        double sum = b[i];
        for (size_t j = i + 1; j < n; j++) {
            sum -= A[i][j] * x[j];
        }
        /* Check for division by zero (should not happen if pivot check passed) */
        if (A[i][i] == 0.0) {
            /* This should not be reached due to pivot check, but for safety */
            return NUMILIB_ERR_SINGULAR;
        }
        x[i] = sum / A[i][i];
    }

    return NUMILIB_SUCCESS;
}