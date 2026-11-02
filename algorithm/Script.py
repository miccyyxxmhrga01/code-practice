class Stack:
    def __init__(self, size):
        self.arr = [None] * size   # fixed-size list
        self.top = -1
        self.size_limit = size

    def push(self, x):
        if self.top == self.size_limit - 1:
            print("\n---------")
            print(f"Stack is FULL! Cannot push {x}")
            print("---------\n")
        else:
            self.top += 1
            self.arr[self.top] = x
            print("\n---------")
            print(f"{x} is pushed into the stack")
            print("---------\n")

    def pop(self):
        if self.top == -1:
            print("\n---------")
            print("The stack is EMPTY! Nothing to pop.")
            print("---------\n")
            return None
        else:
            value = self.arr[self.top]
            self.top -= 1
            print("\n---------")
            print(f"{value} popped from the stack")
            print("---------\n")
            return value

    def peek(self):
        if self.top == -1:
            print("\n---------")
            print("Stack is empty, nothing to peek!")
            print("---------\n")
            return None
        else:
            return self.arr[self.top]

    def is_full(self):
        return self.top == self.size_limit - 1

    def is_empty(self):
        return self.top == -1

    def size(self):
        return self.top + 1


# Main Program
if __name__ == "__main__":
    size = int(input("Enter the size of the stack: "))
    s = Stack(size)

    while True:
        print("\nStack Operation Menu:")
        print("1. Push()")
        print("2. Pop()")
        print("3. Size()")
        print("4. Peek()")
        print("5. IsFull()")
        print("6. IsEmpty()")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            val = int(input("Enter a number to push: "))
            s.push(val)
        elif choice == "2":
            s.pop()
        elif choice == "3":
            print("\nSize:", s.size())
        elif choice == "4":
            top_value = s.peek()
            if top_value is not None:
                print("\nTop element:", top_value)
        elif choice == "5":
            print("\nIsFull?:", s.is_full())
        elif choice == "6":
            print("\nIsEmpty?:", s.is_empty())
        elif choice == "7":
            print("Exiting...")
            break
        else:
            print("Invalid Choice!")
