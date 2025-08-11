// यह फंक्शन तब तक इंतज़ार करेगा जब तक उसे बताया गया एलिमेंट न मिल जाए
function whenElementExists(selector, callback) {
    const interval = setInterval(function() {
        const element = document.querySelector(selector);
        if (element) {
            clearInterval(interval);
            callback(element);
        }
    }, 100); // हर 100ms में चेक करेगा
}

// जब #id_course वाला एलिमेंट मिल जाए, तब यह कोड चलाओ
whenElementExists("#id_course", function(courseSelect) {
    const semesterSelect = document.querySelector("#id_current_semester");

    if (!semesterSelect) return;

    // सेमेस्टर को अपडेट करने वाला मेन फंक्शन
    const updateSemesters = async () => {
        const courseId = courseSelect.value;
        const currentSelectedSemester = semesterSelect.value; // पुराना सिलेक्शन याद रखना

        semesterSelect.innerHTML = '<option value="">---------</option>'; // लिस्ट को खाली करना

        if (!courseId) return;

        try {
            const response = await fetch(`/admissions/ajax/get-semesters-for-course/${courseId}/`);
            const data = await response.json();

            let isCurrentSelectedStillValid = false;

            if (data.semesters) {
                data.semesters.forEach(semester => {
                    const option = document.createElement('option');
                    option.value = semester.id;
                    option.innerText = `Semester ${semester.semester_number}`;
                    semesterSelect.appendChild(option);

                    if (option.value == currentSelectedSemester) {
                        isCurrentSelectedStillValid = true;
                    }
                });
            }

            // अगर पुराना वाला सेमेस्टर नई लिस्ट में भी मौजूद है, तो उसे फिर से चुन लो
            if (isCurrentSelectedStillValid) {
                semesterSelect.value = currentSelectedSemester;
            }

        } catch (error) {
            console.error("Error fetching semesters:", error);
        }
    };

    // जब भी कोर्स बदला जाए, सेमेस्टर अपडेट करो
    courseSelect.addEventListener("change", updateSemesters);

    // पेज लोड होने पर भी एक बार चलाओ (अगर कोर्स पहले से चुना हुआ है)
    if (courseSelect.value) {
        updateSemesters();
    }
});