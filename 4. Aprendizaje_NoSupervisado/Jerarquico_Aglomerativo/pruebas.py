"""
M = [[i] for i in range(5)]  # Assuming self.n is defined somewhere
print(M)

if len(M) > 2:
    for x in M[1]:
        M[0].append(x)    
    M.pop(1)  # Remove the 2nd array (index 1)

print(M)
"""

# Suppose 'matrix' is your matrix
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
for row in matrix:
    print(row)
# Function to delete a column from the matrix
def delete_column(matrix, column_index):
    for row in matrix:
        del row[column_index]

# Example usage: deleting the second column (index 1)
delete_column(matrix, 1)
print("NUEVA")
# Print the modified matrix
for row in matrix:
    print(row)
