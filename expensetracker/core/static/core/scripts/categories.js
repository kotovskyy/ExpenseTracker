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


