document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("loginForm");
  const errorContainer = document.getElementById("errorContainer");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData(form);
    const response = await fetch("/login", {
      method: "POST",
      body: formData,
    });
    const data = await response.json();

    if (data.success) {
      window.location.href = "/home"; // Redirige si el login es exitoso
    } else {
      errorContainer.textContent = data.error;
    }
  });
});
