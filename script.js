document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");
    const loadingDiv = document.createElement("p");
    loadingDiv.id = "loading";
    loadingDiv.textContent = "Generating team... Please wait.";
    loadingDiv.style.display = "none";
    document.body.appendChild(loadingDiv);

    form.addEventListener("submit", function () {
        loadingDiv.style.display = "block";
    });
});

function closeAlert() {
    document.getElementById("customAlert").style.display = "none";
}

document.addEventListener("DOMContentLoaded", function () {
    const alertBox = document.getElementById("customAlert");
    const agreeCheckbox = document.getElementById("agreeCheckbox");
    const agreeButton = document.getElementById("agreeButton");

    // Show the alert when page loads
    alertBox.style.display = "block";

    // Enable button only when checkbox is checked
    agreeCheckbox.addEventListener("change", function () {
        agreeButton.disabled = !this.checked;
    });

    // Hide alert when "Continue" button is clicked
    agreeButton.addEventListener("click", function () {
        alertBox.style.display = "none";
    });
});
