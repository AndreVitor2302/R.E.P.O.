def show_menu():
    print("\nToDo List Menu: ")
    print("1. View ToDo List")
    print("2. Add Task")
    print("3. Remove Task")
    print("4. Exit")
def view_task(tasks):
    if not tasks:
        print("\nNo tasks in the list.")
    else:
        print("\nToDo List:")
        for i, task in enumerate(tasks, start=1):
            print(f"{i}. {task}")
def add_task(tasks):
    task = input("\nEnter the task to add: ")
    tasks.append(task)
    print("Task added")
def remove_task(tasks):
    view_task(task)
    try:
        task_num = int(input("\nEnter the task number to remove: "))
        if 1 <= task_num <= len(tasks):
            removed = tasks.pop(task_num - 1)
            print(f"Task '{removed}' removed.")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid number.")
def main():
    task = []
    while True:
        show_menu()
        choice = input("Choose an option (1-4): ")
        if choice == '1':
            view_task(task)
        elif choice == '2':
            add-task(task)
        elif choice == '3':
            remove_task(task)
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid choice")
if __name__ == "__main__":
    main()