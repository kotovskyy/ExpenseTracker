function changePeriod(direction, path) {
    const monthNames = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ];

    const currentPeriod = document.querySelector('.period-text').innerText.trim().split(' ');
    const currentMonth = currentPeriod[0];
    const currentYear = currentPeriod[1];

    const monthNumber = monthNames.indexOf(currentMonth) + 1;

    var newMonth = (direction === 'prev') ? monthNumber-1 : monthNumber+1;
    var newYear = parseInt(currentYear);
    
    if (newMonth > 12) {
        newMonth = 1;
        newYear = newYear + 1;
    }
    if (newMonth <= 0) {
        newMonth = 12;
        newYear = newYear - 1;
    }

    window.location.href = `/${path}/?month=${newMonth}&year=${newYear}`;
}

function openCategoryPage(category_id){
    var cat_id = parseInt(category_id);
    window.location.href = `/categories/${cat_id}/`;
}

function editCategory(category_id){
    let form = document.getElementById("editCategoryForm_"+category_id);
    form.submit();
}

function editAccount(account_id) {
    let form = document.getElementById("editAccountForm_"+account_id);
    form.submit();
}

function editTransaction(transaction_id) {
    let form = document.getElementById("editTransactionForm_"+transaction_id);
    form.submit();
}

function deleteTransaction(transaction_id) {
    let confirmDelete = confirm("Are you sure you want to delete this transaction?\nYou won't be able to restore removed data.");
    if (confirmDelete) {
        let form = document.getElementById("deleteTransactionForm_"+transaction_id);
        form.submit();
    }
}

function deleteAccount(account_id, n_transactions) {
    let confirmDelete = confirm("Are you sure you want to delete this account?\nAll transactions ("+n_transactions+") associated with this account will be removed.");
    if (confirmDelete) {
        let form = document.getElementById("deleteAccountForm_"+account_id);
        form.submit();
    }
}

function deleteCategory(category_id, n_transactions){
    let confirmDelete = confirm("Are you sure you want to delete this category?\nAll transactions ("+n_transactions+") associated with this category will be removed.");
    if (confirmDelete) {
        let form = document.getElementById("deleteCategoryForm_"+category_id);
        form.submit();
    }
}

document.addEventListener('DOMContentLoaded', function () {
    var currencyField = document.querySelector('.currency-field');

    currencyField.addEventListener('change', function () {
        this.blur(); 
    });
});


