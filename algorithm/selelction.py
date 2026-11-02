def selection_sort(arr):
    n = len(arr)
    
    for i in range(n):
        min_index = i
        
        for j in range(i + 1, n):
            if arr[j] < arr[min_index]:
                min_index = j
        
        arr[i], arr[min_index] = arr[min_index], arr[i]
    
    return arr


user_input = input("Enter numbers separated by spaces: ")
numbers = [int(x) for x in user_input.split()]

print("Original array:", numbers)

sorted_numbers = selection_sort(numbers)
print("Sorted array:", sorted_numbers)