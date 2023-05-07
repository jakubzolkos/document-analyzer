const shrink_btn = document.querySelector(".shrink-btn");
const tooltip_elements = document.querySelectorAll(".tooltip-element");
const sidebarLinks = document.querySelectorAll('.sidebar-links a');
const activeTab = document.querySelector('.active-tab');

const myLink = document.getElementById('link');

myLink.addEventListener('click', (e) => {
  if (e.target.href === window.location.href) {
    e.preventDefault();
  }
});

// Function to update the active tab position
function updateActiveTab() {
  sidebarLinks.forEach((link, index) => {
    if (link.classList.contains('active')) {
      activeTab.style.top = `${2.5 + 58 * index}px`;
    }
  });
}

// Update the active tab position initially
updateActiveTab();

// Add click event listeners to sidebar links
sidebarLinks.forEach(link => {
  link.addEventListener('click', () => {
    // Remove 'active' class from all links
    sidebarLinks.forEach(link => link.classList.remove('active'));
    
    // Add 'active' class to the clicked link
    link.classList.add('active');
    
    // Update the active tab position
    updateActiveTab();
  });
});


let activeIndex;

shrink_btn.addEventListener("click", () => {
  document.body.classList.toggle("shrink");
  setTimeout(moveActiveTab, 400);

  shrink_btn.classList.add("hovered");

  setTimeout(() => {
    shrink_btn.classList.remove("hovered");
  }, 500);
});

// function moveActiveTab() {
//   const activeLink = document.querySelector(".sidebar-links a.active");
//   if (activeLink) {
//     activeIndex = Array.from(sidebar_links).indexOf(activeLink);
//     let topPosition = activeIndex * 58 + 2.5;
//     active_tab.style.top = `${topPosition}px`;
//   }
// }

// function changeLink() {
//   sidebar_links.forEach((sideLink) => sideLink.classList.remove("active"));
//   this.classList.add("active");

//   activeIndex = this.dataset.active;

//   moveActiveTab();
// }

sidebar_links.forEach((link) => link.addEventListener("click", changeLink));

function showTooltip() {
  let tooltip = this.parentNode.lastElementChild;
  let spans = tooltip.children;
  let tooltipIndex = this.dataset.tooltip;

  Array.from(spans).forEach((sp) => sp.classList.remove("show"));
  spans[tooltipIndex].classList.add("show");

  tooltip.style.top = `${(100 / (spans.length * 2)) * (tooltipIndex * 2 + 1)}%`;
}

tooltip_elements.forEach((elem) => {
  elem.addEventListener("mouseover", showTooltip);
});

// document.addEventListener("DOMContentLoaded", moveActiveTab);
