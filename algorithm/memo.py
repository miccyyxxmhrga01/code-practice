
import ctypes
import ctypes.util
import sys

if sys.platform.startswith("win"):
    c_library = ctypes.cdll.msvcrt
else:
    c_library = ctypes.CDLL(ctypes.util.find_library("c"))

malloc = c_library.malloc
free = c_library.free

malloc.argtypes = [ctypes.c_size_t]
malloc.restype = ctypes.c_void_p
free.argtypes = [ctypes.c_void_p]
free.restype = None

how_many = int(input("How many numbers do you want to store? "))

if how_many < 3:
    print("Please enter at least 3 processes.")
    sys.exit()

bytes_needed = how_many * ctypes.sizeof(ctypes.c_int)
address = malloc(bytes_needed)

if not address:
    raise MemoryError("Memory allocation failed!")

print("\nI asked for", bytes_needed, "bytes of memory.")
print("My memory starts at address:", hex(address), "\n")

try:
    my_numbers = (ctypes.c_int * how_many).from_address(address)
    processes = []

    for i in range(how_many):
        number = int(input("Enter number " + str(i + 1) + ": "))
        my_numbers[i] = number
        processes.append("P" + str(i + 1))

    print("\n--- INITIAL RAM (FULL) ---")
    for i in range(how_many):
        print(processes[i], "->", my_numbers[i])

    new_process = "P" + str(how_many + 1)
    new_number = int(input("\nEnter number for " + new_process + ": "))

    print("\nRAM is full!")
    print("Swapping P2 to secondary memory...")

    swapped_process = processes.pop(1)
    swapped_number = my_numbers[1]

    with open("secondary_memory.txt", "w") as file:
        file.write(swapped_process + " -> " + str(swapped_number))

    for i in range(1, how_many - 1):
        my_numbers[i] = my_numbers[i + 1]

    my_numbers[how_many - 1] = new_number
    processes.append(new_process)

    print(swapped_process, "has been swapped out.")
    print(new_process, "has been loaded into RAM.")

    print("\n--- FINAL RAM ---")
    for i in range(how_many):
        print(processes[i], "->", my_numbers[i])

    print("\n--- SECONDARY MEMORY ---")
    with open("secondary_memory.txt", "r") as file:
        print(file.read())

finally:
    free(address)
    print("\nMemory has been freed. Done!")
