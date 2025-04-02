function showPopup(projectName) {
    const popup = document.getElementById("popup");
    const title = document.getElementById("popup-title");
    const description = document.getElementById("popup-description");

    // You can customize this part with more dynamic data
    if (projectName === 'Hackathon 1') {
        title.innerText = "Hackathon 1 - Winner";
        description.innerHTML = "Team: Alice, Bob, Charlie<br>Contributions: Alice - Project Manager, Bob - Developer, Charlie - Designer";
    } else if (projectName === 'Hackathon 2') {
        title.innerText = "Hackathon 2 - Finalist";
        description.innerHTML = "Team: Dave, Eve<br>Contributions: Dave - Developer, Eve - Designer";
    } else if (projectName === 'ConnectEd') {
        title.innerText = "ConnectEd - Social Networking App";
        description.innerHTML = "Team: John, Sarah, Emma<br>Contributions: John - Lead Developer, Sarah - Backend Developer, Emma - UI/UX Designer";
    } else {
        // Add cases for other projects
        title.innerText = projectName;
        description.innerText = "Project details to be added.";
    }

    popup.style.display = "flex";
}

function closePopup() {
    document.getElementById("popup").style.display = "none";
}
