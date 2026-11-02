

import java.util.Scanner;

public class Stack {
    int arr[];
    int top = -1;
    
    // Constructor: creates stack with given size
    Stack(int size){
        arr = new int[size];
    }

    // Push method
    void push(int x){
        if(top == arr.length-1){
            System.out.println("\n---------");
            System.out.println("Stack is FULL! Cannot push " + x);
            System.out.println("---------\n");
        } else {
            arr[++top] = x;
            System.out.println("\n---------");
            System.out.println(x + " is pushed in the stack");
            System.out.println("---------\n");
        }
    }

    // Pop method
    int pop(){
        if(top == -1){
            System.out.println("\n---------");
            System.out.println("The stack is EMPTY! Nothing to pop.");
            System.out.println("---------\n");
            return -1;
        } else {
            System.out.println("\n---------");
            System.out.println(arr[top] + " popped from the stack.");
            System.out.println("---------\n");
            return arr[top--];
        }
    }

    // Peek method
    int peek(){
        if(top == -1){
            System.out.println("\n---------");
            System.out.println("Stack is empty, nothing to peek!");
            System.out.println("---------\n");
            return -1;
        } else {
            return arr[top];
        }
    }

    // Check if full
    boolean isFull(){
        return top == arr.length-1;
    }

    // Check if empty
    boolean isEmpty(){
        return top == -1;
    }

    // Get size
    int size(){
        return top + 1;
    }
    
    // Main method
    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);
        
        System.out.print("Enter a size of the stack: ");
        int size = scan.nextInt();
        Stack s = new Stack(size);
        
        while(true){
            System.out.println("\nStack Operation Menu:");
            System.out.println("1. Push()");
            System.out.println("2. Pop()");
            System.out.println("3. Size()");
            System.out.println("4. Peek()");
            System.out.println("5. IsFull()");
            System.out.println("6. IsEmpty()");
            System.out.println("7. Exit");
            
            System.out.print("Enter your choice: ");
            int choice = scan.nextInt();
            
            switch(choice){
                case 1:
                    System.out.print("Enter a number to push: ");
                    int val = scan.nextInt();
                    s.push(val);
                    break;
                case 2:
                    s.pop();
                    break;
                case 3:
                    System.out.println("\nSize: " + s.size());
                    break;
                case 4:
                    int topValue = s.peek();
                    if(topValue != -1)
                        System.out.println("\nTop element: " + topValue);
                    break;
                case 5:
                    System.out.println("\nIsFull?: " + s.isFull());
                    break;
                case 6:
                    System.out.println("\nIsEmpty?: " + s.isEmpty());
                    break;
                case 7:
                    System.out.println("Exiting...");
                    scan.close();
                    return;
                default:
                    System.out.println("Invalid Choice!");
            }
        }
    }
}
