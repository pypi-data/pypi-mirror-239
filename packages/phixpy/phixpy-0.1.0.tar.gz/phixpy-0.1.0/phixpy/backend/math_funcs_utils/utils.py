def check_lengths(matrix):
    length = len(matrix[0])
    for row in matrix:
        if len(row) != length:
            raise ValueError("Length of rows must be the same")

def format_matrix(matrix):
    check_lengths(matrix)

    # Find the maximum width for each column
    col_widths = [max(map(len, map(str, col))) for col in zip(*matrix)]

    # Format each row with proper alignment
    formatted_rows = []
    for row in matrix:
        formatted_row = ' '.join(f'{val:>{width}}' for val, width in zip(row, col_widths))
        formatted_row = '[' + formatted_row + ']'
        formatted_rows.append(formatted_row)

    # Join the formatted rows with newline characters
    return '[' + '\n '.join(formatted_rows) + ']'

def get_columns(matrix, col):
    output = []
    for row in matrix:
        output.append(row[col])
    return output


def size(matrix):
    len_row = len(matrix[0])
    return len(matrix)*len_row

def shape(matrix):
    s = size(matrix)
    rows = len(matrix)
    return rows, int(s/rows)

