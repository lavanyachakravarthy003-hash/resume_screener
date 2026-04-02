function analyzeResume() {
    let jobDesc = document.getElementById("jobDesc").value;
    let fileInput = document.getElementById("resumeFile");
    let resultBox = document.getElementById("result");

    if (jobDesc === "" || fileInput.files.length === 0) {
        alert("Please enter job description and upload resume!");
        return;
    }

    // Fake loading effect
    resultBox.style.display = "block";
    resultBox.innerHTML = "⏳ Analyzing resume...";

    setTimeout(() => {
        // Dummy score (you can replace with backend logic)
        let score = Math.floor(Math.random() * 40) + 60;

        resultBox.innerHTML = `
            ✅ Resume Score: <b>${score}%</b><br><br>
            ✔ Skills Match: Good<br>
            ✔ Suggestions: Add more Java projects and keywords like Spring Boot.
        `;
    }, 2000);
}