document.addEventListener("DOMContentLoaded", function () {
  const btn = document.getElementById("theme-toggle");
  const sun = document.getElementById("icon-sun");
  const moon = document.getElementById("icon-moon");
  if (!btn || !sun || !moon) return;

  function setTheme(dark) {
    if (dark) {
      document.documentElement.classList.add("dark");
      sun.style.display = "block";
      moon.style.display = "none";
      localStorage.setItem("theme", "dark");
    } else {
      document.documentElement.classList.remove("dark");
      sun.style.display = "none";
      moon.style.display = "block";
      localStorage.setItem("theme", "light");
    }
  }

  const userTheme = localStorage.getItem("theme");
  setTheme(userTheme === "dark" || !userTheme);

  btn.addEventListener("click", function () {
    const isDark = document.documentElement.classList.contains("dark");
    setTheme(!isDark);
  });
});
