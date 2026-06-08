document.addEventListener("DOMContentLoaded", () => {
  const activitiesList = document.getElementById("activities-list");
  const activitySelect = document.getElementById("activity");
  const signupForm = document.getElementById("signup-form");
  const messageDiv = document.getElementById("message");

  async function fetchActivities() {
    try {
      const response = await fetch("/activities");
      const activities = await response.json();

      activitiesList.innerHTML = "";
      activitySelect.innerHTML = '<option value="">-- Select an activity --</option>';

      Object.entries(activities).forEach(([name, details]) => {
        const activityCard = document.createElement("div");
        activityCard.className = "activity-card";

        const spotsLeft = details.max_participants - details.participants.length;

        // Participants list
        let participantsHTML = "<ul class='participants-list'>";
        if (details.participants.length > 0) {
          details.participants.forEach((participant) => {
            participantsHTML += `
              <li>
                ${participant}
                <button class="delete-btn" data-activity="${name}" data-email="${participant}" title="Unregister">🗑️</button>
              </li>`;
          });
        } else {
          participantsHTML += "<li class='no-participants'>No participants yet</li>";
        }
        participantsHTML += "</ul>";

        activityCard.innerHTML = `
          <h4>${name}</h4>
          <p>${details.description}</p>
          <p><strong>Schedule:</strong> ${details.schedule}</p>
          <p><strong>Availability:</strong> ${spotsLeft} spots left</p>
          <div class="parti