// script.js
const baseURL = "http://localhost:5000";

// Function to make a GET request to retrieve the requests
async function getRequests() {
  try {
    const response = await fetch(`${baseURL}/requests`);
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error fetching requests:", error);
    return [];
  }
}

// Function to generate card HTML for a request
function createCard(request) {
  const card = document.createElement("div");
  card.classList.add("card");

  const title = document.createElement("h2");
  title.classList.add("card-title");
  title.textContent = `Request ID: ${request.request_id}`;

  const info = document.createElement("div");
  info.classList.add("card-info");
  info.innerHTML = `
    <p><span>Bank Name:</span> ${request.bank_name}</p>
    <p><span>Manager Name:</span> ${request.manager_name}</p>
    <p><span>Due Date:</span> ${request.due_date}</p>
    <p><span>Branch Name:</span> ${request.branch_name}</p>
  `;

  card.appendChild(title);
  card.appendChild(info);

  return card;
}

// Function to display the requests in the card container
function displayRequests(requests) {
  const cardContainer = document.getElementById("cardContainer");
  cardContainer.innerHTML = "";

  requests.forEach((request) => {
    const card = createCard(request);
    cardContainer.appendChild(card);
  });
}

// Fetch and display the requests on page load
window.onload = async () => {
  const requests = await getRequests();
  displayRequests(requests);
};
