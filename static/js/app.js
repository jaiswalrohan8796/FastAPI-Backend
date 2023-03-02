// delete button click handler
async function deleteTodoByID(id) {
    const res = await fetch(`/delete/${id}`, { method: "DELETE" });
    if (res.status == 200) {
        console.log(`Success to delete item ${id}`);
        location.reload();
    } else {
        console.log(`Failed to delete item ${id}`);
    }
}

//disable add todo button unless input is filled

const inputElement = document.getElementById("todo-input");
const buttonElement = document.getElementById("todo-button");

inputElement.addEventListener("input", function () {
    buttonElement.disabled = inputElement.value.trim() === "";
});
async function sendTodo() {
    if (buttonElement.disabled == true) {
        console.log("Input is empty");
        return;
    }
    const todo = inputElement.value.trim();
    const res = await fetch("/add", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            todo: todo,
        }),
    });
    if (res.status == 200) {
        console.log("todo added");
        location.reload();
    } else {
        console.log("todo adding failed");
    }
}

//edit todo by id

async function editTodoById(todo_id) {
    const res = await fetch(`/edit/${todo_id}`, { method: "GET" });
    if (res.status == 200) {
        console.log(`Success to delete item ${todo_id}`);
        location.reload();
    } else {
        console.log(`Failed to delete item ${todo_id}`);
    }
}
