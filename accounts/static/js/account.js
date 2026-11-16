document.querySelectorAll("[data-password-toggle]").forEach((toggle) => {
    const field = document.getElementById(toggle.dataset.passwordToggle);
    const icon = toggle.querySelector("i");

    if (!field || !icon) {
        return;
    }

    toggle.addEventListener("click", () => {
        const isVisible = field.type === "text";
        field.type = isVisible ? "password" : "text";
        toggle.setAttribute("aria-pressed", String(!isVisible));
        toggle.setAttribute("aria-label", isVisible ? "Show password" : "Hide password");
        icon.classList.toggle("bi-eye", isVisible);
        icon.classList.toggle("bi-eye-slash", !isVisible);
    });
});

const signupForm = document.querySelector("#signupForm");
const signupPassword = document.querySelector("#signupPassword");
const confirmPassword = document.querySelector("#confirmPassword");

if (signupForm && signupPassword && confirmPassword) {
    const validatePasswordMatch = () => {
        const passwordsMatch = confirmPassword.value === signupPassword.value;
        confirmPassword.setCustomValidity(passwordsMatch ? "" : "Passwords do not match.");
    };

    signupPassword.addEventListener("input", validatePasswordMatch);
    confirmPassword.addEventListener("input", validatePasswordMatch);
    signupForm.addEventListener("submit", validatePasswordMatch);
}
