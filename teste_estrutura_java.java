// Pilha usando lista encadeada
class Node {
    int data;
    Node next;
}

class Stack {
    Node top;

    public void push(int data) {
        Node n = new Node();
        n.data = data;
        n.next = top; // Corrigido: "text" → "next"
        top = n;
    }

    public void pop() {
        if (top == null) {
            System.out.println("Stack is empty!");
        } else {
            top = top.next;
        }
    }

    public void print() {
        if (top == null) {
            System.out.println("Stack is empty!");
            return;
        }
        Node pointer = top;
        System.out.print("[");
        while (pointer != null) {
            System.out.print(pointer.data);
            pointer = pointer.next;
            if (pointer != null) {
                System.out.print(", ");
            }
        }
        System.out.println("]");
    }
}
