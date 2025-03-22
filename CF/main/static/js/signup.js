document.addEventListener('DOMContentLoaded', function() {
    const userTypeOptions = document.querySelectorAll('.user-type-option');
    const userTypeInput = document.getElementById('userType');
    
    if (userTypeInput) {
        userTypeOptions.forEach(option => {
            option.addEventListener('click', function() {
                // Remove 'selected' class from all options
                userTypeOptions.forEach(opt => opt.classList.remove('selected'));
                
                // Add 'selected' class to clicked option
                this.classList.add('selected');
                
                // Update hidden input value
                userTypeInput.value = this.getAttribute('data-type');
                console.log("User type set to:", userTypeInput.value);
            });
        });
    } else {
        console.error("User type input element not found");
    }
});
