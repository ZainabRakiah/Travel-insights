(function () {
  const form = document.querySelector(".planner-form");
  const results = document.getElementById("trip-results");

  if (results) {
    results.scrollIntoView({ behavior: "smooth", block: "start" });
    results.focus({ preventScroll: true });
  }

  if (!form) return;

  form.addEventListener("submit", () => {
    const btn = form.querySelector(".submit-btn");
    if (btn) {
      btn.disabled = true;
      btn.textContent = "Planning…";
    }
  });
})();
