async function editSave(todo_id) {
    inputElement = document.getElementById("todo-desc");
    if (inputElement.value.trim() === "") {
        return;
    }
    const todo = inputElement.value;
    const res = await fetch(`./${todo_id}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            todo: todo,
        }),
    });
    if (res.status == 200) {
        console.log("todo edit success");
        location.href = "/";
    } else {
        console.log("todo edit failed");
    }
}
