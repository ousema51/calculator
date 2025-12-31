// ==========================
// Element references
// ==========================
const solveBtn = document.getElementById("solve-btn");
const problemInput = document.getElementById("problem-input");
const errorMsg = document.getElementById("error-msg");

const outputCard = document.getElementById("output-card");
const outputProblem = document.getElementById("output-problem");
const outputSteps = document.getElementById("output-steps");
const outputAnswer = document.getElementById("output-answer");

// ==========================
// State
// ==========================
let selectedMode = "derivative";

// ==========================
// Mode selection
// ==========================
document.querySelectorAll(".mode-btn").forEach(button => {
  button.addEventListener("click", () => {
    document.querySelectorAll(".mode-btn").forEach(b => b.classList.remove("active"));
    button.classList.add("active");
    selectedMode = button.dataset.mode;
  });
});

// ==========================
// Solve handler
// ==========================
solveBtn.addEventListener("click", async () => {
  const problem = problemInput.value.trim();

  // Validation
  if (!problem) {
    errorMsg.textContent = "Please enter a problem.";
    outputCard.hidden = true;
    return;
  }

  errorMsg.textContent = "";
  outputCard.hidden = false;

  // Reset output
  outputProblem.textContent = "Solving...";
  outputSteps.innerHTML = "";
  outputAnswer.textContent = "";

  try {
    const response = await fetch("http://127.0.0.1:5000/solve", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        mode: selectedMode,
        problem: problem
      })
    });

    // Always parse JSON (even on errors)
    const data = await response.json();

    // Populate output card
    outputProblem.textContent = data.problem || problem;

    outputSteps.innerHTML = "";
    if (Array.isArray(data.steps)) {
      data.steps.forEach(step => {
        const li = document.createElement("li");
        li.textContent = step;
        outputSteps.appendChild(li);
      });
    }

    outputAnswer.textContent = data.answer || "No answer returned.";

  } catch (err) {
    // True connection failure (backend down, CORS, etc.)
    console.error(err);
    outputCard.hidden = true;
    errorMsg.textContent = "Could not connect to backend.";
  }
});
