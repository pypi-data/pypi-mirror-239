"""Tensor class that provides useful methods for working with matrices"""


import copy


class Tensor():
    """Tensor class that stores matrix and providers useful methods"""

    dims: list[int] = []
    data: list[float] = []

    strict_dim_check: bool = False

    def __init__(self, data, strict_dim_check=False):
        self.data = data
        self.get_shape()

        self.strict_dim_check = strict_dim_check

    def __str__(self):
        return self.data.__str__()

    def __repr__(self):
        return self.data.__str__()

    def get_shape(self):
        """Calculates the shape of matrix"""
        array = self.data
        size = len(self.data)
        dimension = []

        i = 0

        while (i < size):
            item = array[i]

            dimension.append(size)

            if (isinstance(item, float) or isinstance(item, int)):
                break

            size = len(item)
            array = item

            i = 0

        self.dims = tuple(dimension)

    def inverse(self):
        """TODO: calculates an inverse of a matrix"""

    def _to_rref(self, matrix):
        """Puts a matrix into reduces row echelon form"""

        if not self.is_2d():
            raise ValueError(
                f"Array should be 2d, but got {self.dims}")

        m, n = self.dims

        outer_row_index = 0
        outer_col_index = 0

        while (outer_col_index < n and outer_row_index < m):
            row = matrix[outer_row_index]
            pivot_entry = row[outer_col_index]

            if pivot_entry == 0:
                col_has_all_zeros = self.check_column(
                    matrix, outer_col_index, lambda item, index: item == 0)

                if col_has_all_zeros:
                    outer_col_index += 1
                    continue

                index_to_swap = self.find_non_zero_row(
                    matrix, outer_row_index, outer_col_index)

                if not index_to_swap:
                    outer_col_index += 1
                    continue

                self.swap_rows(matrix, outer_row_index, index_to_swap)

                row = matrix[outer_row_index]
                pivot_entry = row[outer_col_index]

            if pivot_entry != 1:
                self.update_row(matrix, outer_row_index,
                                lambda item, index: item / pivot_entry)

            for row_index in range(m):
                row_to_update = matrix[row_index]
                row_item = row_to_update[outer_col_index]

                if row_index == outer_row_index:
                    continue

                self.update_row(matrix, row_index, lambda item,
                                index: item + -row_item * row[index])

            outer_row_index += 1
            outer_col_index += 1

        return matrix

    def to_rref(self):
        """Puts a matrix into reduces row echelon form"""
        data = list(self.data)
        return Tensor(self._to_rref(data))

    def to_rref_with_augmented_matrix(self, matrix_to_augment):
        augmented_matrix = self.augment_matrix(
            matrix_to_augment=matrix_to_augment)
        return Tensor(self._to_rref(augmented_matrix))

    def determinant(self):
        """Calculates a determinant of a matrix"""
        if not self.is_2d_square():
            raise ValueError(
                f"Array should be square and 2d, but got {self.dims}")

    # Util methods
    def is_2d(self):
        """Checks if matrix provided by you is 2 dimensional"""
        return len(self.dims) == 2

    def is_2d_square(self):
        """Checks if matrix provided by you is 2 dimensional and square"""
        return self.is_2d() and self.dims[0] == self.dims[1]

    def update_row(self, matrix, i: int, update_func):
        """Update row of a matrix by index"""
        row = matrix[i]
        for col_index, item in enumerate(row):
            row[col_index] = update_func(item, col_index)

    def check_row(self, matrix, row_index: int, check_func):
        """Run a function for every element of a row"""
        row = matrix[row_index]
        for col_index, item in enumerate(row):
            match = check_func(item, col_index)
            if not match:
                return False

        return True

    def check_column(self, matrix, col_index: int, check_func):
        """Run a function for every element of a column"""
        for row_index, item in enumerate(matrix):
            item = matrix[row_index][col_index]

            match = check_func(item, row_index)
            if not match:
                return False

        return True

    def find_non_zero_row(self, matrix, row_index: int, col_index: int):
        """Finds a first non zero row on some specific column"""
        m = self.dims[0]

        try:
            index = row_index + 1
            while (index < m):
                item = matrix[index][col_index]

                if item != 0:
                    return index

                index += 1

        except IndexError:
            return None

    def swap_rows(self, matrix, row_index_1: int, row_index_2: int):
        """Swap two rows by indexes"""
        matrix[row_index_1], matrix[row_index_2] = matrix[row_index_2], matrix[row_index_1]

    def augment_matrix(self, matrix_to_augment):
        """Augment matrix with other matrix(or vector) and put's it into reduces row echelon form"""
        data = self.copy_data()
        for index, row in enumerate(data):
            row.extend(matrix_to_augment[index])

        return data

    def copy_data(self):
        """Deeply copies the data"""
        return copy.deepcopy(self.data)
