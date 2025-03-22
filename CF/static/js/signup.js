document.addEventListener('DOMContentLoaded', function() {
    const signupForm = document.getElementById('signupForm');
    
    if (signupForm) {
        signupForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            try {
                // Safely get values with error handling
                const firstname = document.getElementById('first_name')?.value || '';
                const lastname = document.getElementById('last_name')?.value || '';
                const email = document.getElementById('email')?.value || '';
                const password = document.getElementById('password')?.value || '';
                const confirmPassword = document.getElementById('confirmPassword')?.value || '';
                
                // Get the user type from the hidden input that's updated by the UI
                const userType = document.getElementById('userType')?.value || '';

                if (!firstname || !lastname || !email || !password || !confirmPassword || !userType) {
                    alert("All fields are required");
                    return;
                }

                if (password !== confirmPassword) {
                    alert("Passwords do not match");
                    return;
                }

                const formData = new FormData(signupForm);

                fetch("/auth/signup/", {
                    method: "POST",
                    body: formData,
                    headers: {
                        "X-Requested-With": "XMLHttpRequest"
                    }
                })
                .then(response => response.json())
                .then(data => {
                    console.log("Signup response:", data);
                    if (data.redirect_url) {
                        // Store user data in localStorage
                        if (data.user) {
                            localStorage.setItem('user', JSON.stringify(data.user));
                        }
                        // Redirect to the dashboard
                        window.location.href = data.redirect_url;
                    } else {
                        alert(data.error || "An error occurred during signup");
                    }
                })
                .catch(error => {
                    console.error("Error:", error);
                    alert("An error occurred during signup");
                });
            } catch (err) {
                console.error("Form submission error:", err);
                alert("An error occurred. Please check your form fields and try again.");
            }
        });
    } else {
        console.error("Signup form not found on page!");
    }
});