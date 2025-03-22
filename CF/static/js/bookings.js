document.addEventListener("DOMContentLoaded", async function () {
    const sportSelection = document.querySelector("#sportSelect");
    const coachSelect = document.querySelector("#coachSelect");
    const sessionDate = document.querySelector("#sessionDate");
    const sessionTime = document.querySelector("#sessionTime");
    const form = document.querySelector("#bookingForm");

    const response = await fetch("/coach_sports/",{
            method: "GET",
        }
    )

    if(response.ok){
        const data = await response.json();
        data.sports.forEach(sport => {
            sportSelection.innerHTML += `<option value="${sport.id}">${sport.name}</option>`;
        });
        // Load available coaches based on selected sport

        sportSelection.addEventListener("change", async function () {
            const sportId = sportSelection.value;
            if (!sportId) {
                coachSelect.innerHTML = '<option value="">Choose a coach</option>';
                return;
            }
            const selectedSport = data.sports.find(sport => sport.id == sportId);
            if (!selectedSport) {
                console.error("Selected sport not found");
                return;
            }
            coachSelect.innerHTML = '<option value="">Choose a coach</option>';

            selectedSport.coaches.forEach(coach => {
                coachSelect.innerHTML += `<option value="${coach.id}">${coach.name}</option>`;
            });
            
        });
    }

    // CSRF token retrieval
    function getCSRFToken() {
        return document.querySelector("input[name='csrfmiddlewaretoken']").value;
    }

    

    // Form submission handling
    form.addEventListener("submit", async function (event) {
        event.preventDefault();

        // const formData = {
        //     sport: sportSelection.value,
        //     coach: coachSelect.value,
        //     date: sessionDate.value,
        //     time: sessionTime.value
        // };
        const formData = new FormData(form);

        try {
            const response = await fetch("/make-booking/", {
                method: "POST",
                headers: {
                    // "Content-Type": "application/json",
                    "X-CSRFToken": getCSRFToken(),
                },
                body: formData,
            });

            const result = await response.json();

            if (response.ok) {
                alert(result.message);
                form.reset();
            } else {
                alert("Error: " + result.error);
            }
        } catch (error) {
            console.error("Error submitting form:", error);
            alert("An error occurred while processing your request.");
        }
    });
});
