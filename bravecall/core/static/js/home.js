document.addEventListener("DOMContentLoaded", function () {
    const profileDropdownToggle = document.getElementById("profile-dropdown-toggle");
    const dropdownMenu = document.getElementById("dropdown-menu");

    if (profileDropdownToggle && dropdownMenu) {
        profileDropdownToggle.addEventListener("click", function (event) {
            event.stopPropagation(); 
            dropdownMenu.style.display = dropdownMenu.style.display === "block" ? "none" : "block";
        });

        document.addEventListener("click", function (event) {
            if (!profileDropdownToggle.contains(event.target) && !dropdownMenu.contains(event.target)) {
                dropdownMenu.style.display = "none";
            }
        });
    }

    function generateCalendar() {
        const calendarElement = document.getElementById("calendar");
        if (!calendarElement) return;

        const today = new Date();
        const currentYear = today.getFullYear();
        const currentMonth = today.getMonth();
        const currentDay = today.getDate();
        const monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];

        let firstDay = new Date(currentYear, currentMonth, 1).getDay();
        let daysInMonth = new Date(currentYear, currentMonth + 1, 0).getDate();

        let calendarHTML = `<div class="calendar-header">
                                <button id="prevMonth">&lt;</button>
                                <span>${monthNames[currentMonth]} ${currentYear}</span>
                                <button id="nextMonth">&gt;</button>
                            </div>
                            <table class="calendar-table">
                                <thead>
                                    <tr>
                                        <th>Sun</th><th>Mon</th><th>Tue</th><th>Wed</th><th>Thu</th><th>Fri</th><th>Sat</th>
                                    </tr>
                                </thead>
                                <tbody><tr>`;

        let day = 1;
        for (let i = 0; i < 6; i++) {
            for (let j = 0; j < 7; j++) {
                if (i === 0 && j < firstDay) {
                    calendarHTML += `<td></td>`;
                } else if (day > daysInMonth) {
                    break;
                } else {
                    calendarHTML += `<td class="${day === currentDay ? 'today' : ''}">${day}</td>`;
                    day++;
                }
            }
            if (day > daysInMonth) break;
            calendarHTML += `</tr><tr>`;
        }

        calendarHTML += `</tr></tbody></table>`;
        calendarElement.innerHTML = calendarHTML;
    }

    generateCalendar();

    const tips = [
        "Always stay aware of your surroundings.",
        "Trust your instincts—leave if you feel unsafe.",
        "Avoid isolated areas, especially at night.",
        "Keep emergency contacts easily accessible.",
        "Use well-lit paths and stay in groups whenever possible."
    ];
    let currentTip = 0;

    window.nextTip = function () {
        const tipText = document.getElementById("tip-text");
        if (tipText) {
            tipText.innerText = tips[(currentTip = (currentTip + 1) % tips.length)];
        }
    };

    const logoutLink = document.getElementById("logoutLink");
    const logoutModal = document.getElementById("logoutModal");
    const confirmLogout = document.getElementById("confirmLogout");
    const cancelLogout = document.getElementById("cancelLogout");

    if (logoutModal) {
        logoutModal.style.display = "none";

        if (logoutLink) {
            logoutLink.addEventListener("click", function (event) {
                event.preventDefault();
                logoutModal.style.display = "flex";
            });
        }

        if (confirmLogout) {
            confirmLogout.addEventListener("click", function () {
                window.location.href = "/logout/";
            });
        }

        if (cancelLogout) {
            cancelLogout.addEventListener("click", function () {
                logoutModal.style.display = "none";
            });
        }

        window.addEventListener("click", function (event) {
            if (event.target === logoutModal) {
                logoutModal.style.display = "none";
            }
        });
    }
});
