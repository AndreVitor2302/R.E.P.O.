let input = document.getElementById("inputBox");
input.addEventListener("keydown", validate);

function validate() {
    let form = document.querySelector(".mainform");
    let pattern = /^[^ ]+@[^ ]+\.[a-z]{2,3}$/;

    if (input.value.match(pattern)) {
        form.classList.add("valido");
        form.classList.remove("invalido");
    } else {
        form.classList.add("invalido");
        form.classList.remove("valido");
    }
}