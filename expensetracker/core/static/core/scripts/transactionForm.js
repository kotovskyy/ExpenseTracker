document.addEventListener('DOMContentLoaded', function () {
    var currencyField = document.querySelector('.currency-field');

    currencyField.addEventListener('changeCurrency', function () {
        this.blur(); // Remove focus when an option is selected
    });
});


document.addEventListener('DOMContentLoaded', function () {
    document.getElementById("transaction_type").addEventListener("change", function () {
        var selectedType = this.value;
        if (selectedType === "I") {
            document.getElementById("where-to-label").innerHTML = "From:";
        }
        if (selectedType === "E") {
            document.getElementById("where-to-label").innerHTML = "To:";
        }
        var categorySelect = document.getElementById("id_category");
        var categoryOptions = categorySelect.options;
    
        for (var i = 0; i < categoryOptions.length; i++) {
            var option = categoryOptions[i];
            var optionType = option.getAttribute("data-type");
    
            if (selectedType === optionType) {
                option.style.display = "block";
            } else {
                option.style.display = "none";
            }
        }

        categorySelect.value = null;
    });
});


// Initial population on page load
document.dispatchEvent(new Event("change"));
