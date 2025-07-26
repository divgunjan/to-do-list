#1create an item
#2list items
#3mark them as incomplete at first
#4mark them as complete when done
#5save items

import json

filename = "todolist.json"

def load_tasks():
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except:
        return {"tasks":[]}

def save_tasks(tasks):
    try:
        with open(filename,"w") as file:
            return json.dump(tasks, file)
    except:
        print("Failed to save.")

def view_tasks(tasks):
    task_list = tasks["tasks"]
    if task_list == None or len(task_list) == 0:
        print("No task to display.")
    else:
        print("Your To-Do list:") 
        for index, task in enumerate(task_list):
            status = "[Complete]" if task.get("Complete", False) else "[Pending]"
            print(f"{index+1}. {task['description']} | {status}")

def create_task(tasks):
    description = input("Write a task description.")
    if description:
        tasks["tasks"].append({"description": description, "Complete": False})
        save_tasks(tasks)
        print("Task added.")
    else:
        print("Description is necessary. Task creation failed.")

def mark_task_complete(tasks):
    tasks_list = tasks["tasks"]
    for index, task in enumerate(tasks_list):
        status = not task.get("Complete", False)
        if status: #if any of the tasks is not complete, show description
            print(f"{index+1}. {task["description"]}")
        elif not status:
            print("No pending tasks to show.")
            delete_marked_complete(tasks) #ask for deletion of tasks marked as complete in the list
        else:
            print("There are no pending tasks to show.")
            delete_marked_complete(tasks)

    try:
        task_number = int(input("Enter the task you wish to mark as complete.").strip())
        if 1 <= task_number <= len(tasks_list):
            tasks_list[task_number - 1]["Complete"] = True
            print("Task marked as complete.")
            save_tasks(tasks)
        else:
            print("Invalid number. Task could not be saved.")
    except:
        print("Invalid task number. Task could not be saved.")

#for asking for deleting the "completed" task
class TaskNotCompleteError(Exception):
    pass

def delete_marked_complete(tasks):
        while True:
            view_tasks(tasks)
            tasks_list = tasks["tasks"]
            ask_deleted_number = int(input("Which task number would you like to delete?").strip())
            try:
                if 1 <= ask_deleted_number <= len(tasks_list):
                    if tasks_list[ask_deleted_number-1].get("Complete", False):
                        del tasks_list[ask_deleted_number-1]
                        save_tasks(tasks)
                        print("Task was deleted successfully.")
                        break
                    else:
                        raise TaskNotCompleteError("Task could not be deleted. Task was not marked as complete.")

                else:
                    print("Task deletion cancelled.")
                    break
            except:
                print("Task could not be deleted.")

def delete_task(tasks):
    view_tasks(tasks)
    tasks_list = tasks["tasks"]
    try:
        task_delete_num = int(input("Which task number would you like to delete?").strip())
        if 1 <= task_delete_num <= len(tasks_list):
            del tasks_list[task_delete_num-1]
            print("Task deleted successfully.")
            save_tasks(tasks)
        else:
            print("Task could not be deleted.")

    except:
        print("Task deletion was unsuccessful.")

# def delete_task(tasks):
#     view_tasks(tasks)
#     tasks_list = tasks["tasks"]
#     try:
#         task_delete_num =  list(map(int, input("Which task(s) number would you like to delete?").split(" ")))
#         for task_num in sorted(task_delete_num, reverse=True):
#             if 1 <= task_num <= len(tasks_list):
#                 del tasks_list[task_num]
#                 save_tasks(tasks)
#                 print("Task deleted successfully.")
#             else:
#                 print("Task could not be deleted.")

#     except:
#         print("Task deletion was unsuccessful.")

def main():
    tasks = load_tasks()
    while True:
        print("\nThis is a to-do list application")
        print("1. View Tasks")
        print("2. Add Task")
        print("3. Complete Task")
        print("4. Delete Task")
        print("5. Exit")

        choice = input("Enter your choice.").strip()

        if choice == "1":
            view_tasks(tasks)
        elif choice == "2":
            create_task(tasks)
        elif choice == "3":
            mark_task_complete(tasks)
            ask_delete = str(input("Would you like to delete the completed tasks in your To-Do list?(Y for YES/N for NO)").upper().strip())
            if ask_delete == "Y":
                delete_marked_complete(tasks)
                save_tasks(tasks)
            else:
                ...
        elif choice == "4":
            delete_task(tasks)
        elif choice == "5": #exit
            break
        else:
            print("Invalid command. Please try again.")

main()