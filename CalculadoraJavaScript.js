const currDisplay = document.querySelector(".curr-display");
const prevDisplay = document.querySelector(".prev-display");
const numbers = document.querySelectorAll(".number");
const operands = document.querySelectorAll(".operation");
const cleanBtn = document.querySelector(".clear");
const delBtn = document.querySelector(".delete");
const equalBtn = document.querySelector(".equal");

let operation = null;
let previousValue = "";
let currentValue = "";

function appendNumber(number) {
    if (number === "." && currentValue.includes(".")) return;
    currentValue += number;
    currDisplay.innerText = currentValue;
}

function chooseOperation(op) {
    if (currentValue === "") return;
    if (previousValue !== "") {
        compute();
    }
    operation = op;
    previousValue = currentValue;
    prevDisplay.innerText = `${previousValue} ${operation}`;
    currentValue = "";
    currDisplay.innerText = "";
}

function clearDisplay() {
    currentValue = "";
    previousValue = "";
    operation = null;
    currDisplay.innerText = "";
    prevDisplay.innerText = "";
}

function compute() {
    let result;
    const prev = parseFloat(previousValue);
    const curr = parseFloat(currentValue);
    if (isNaN(prev) || isNaN(curr)) return;
    switch (operation) {
        case "+":
            result = prev + curr;
            break;
        case "-":
            result = prev - curr;
            break;
        case "*":
            result = prev * curr;
            break;
        case "/":
            result = prev / curr;
            break;
        default:
            return;
    }
    currentValue = result.toString();
    currDisplay.innerText = currentValue;
    prevDisplay.innerText = "";
    operation = null;
    previousValue = "";
}

numbers.forEach((number) => {
    number.addEventListener("click", () => {
        appendNumber(number.innerText);
    });
});

operands.forEach((operand) => {
    operand.addEventListener("click", () => {
        chooseOperation(operand.innerText);
    });
});

cleanBtn.addEventListener("click", () => {
    clearDisplay();
});

equalBtn.addEventListener("click", () => {
    compute();
});

delBtn.addEventListener("click", () => {
    currentValue = currentValue.slice(0, -1);
    currDisplay.innerText = currentValue;
});
