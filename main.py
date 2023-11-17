from flask import Flask, render_template, request

app = Flask(__name__)

todo_list = []

# Function for managing the to-do list
def add_task(task):
    todo_list.append({"task": task, "completed": False})

def view_tasks(completed_only=False):
    sorted_tasks = sorted(todo_list, key=lambda task: (task["completed"], task["task"]))
    if completed_only:
        return [(index + 1, task["task"], task["completed"]) for index, task in enumerate(sorted_tasks) if task["completed"]]
    else:
        return [(index + 1, task["task"], task["completed"]) for index, task in enumerate(sorted_tasks)]

def complete_task(index):
    if 0 <= index < len(todo_list):
        todo_list[index]["completed"] = True

def delete_task(index):
    if 0 <= index < len(todo_list):
        todo_list.pop(index)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "add_task" in request.form:
            task = request.form["task"]
            add_task(task)
        elif "complete_task" in request.form:
            index = int(request.form["complete_task"]) - 1
            complete_task(index)
        elif "delete_task" in request.form:
            index = int(request.form["delete_task"]) - 1
            delete_task(index)

    return render_template("index.html", tasks=view_tasks())

@app.route("/completed-tasks", methods=["GET"])
def completed_tasks():
    return render_template("index.html", tasks=view_tasks(completed_only=True))

if __name__ == "__main__":
    app.run(debug=True)
