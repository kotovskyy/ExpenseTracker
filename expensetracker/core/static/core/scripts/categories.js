function openCategoryPage(category_id){
    var cat_id = parseInt(category_id);
    window.location.href = `/categories/${cat_id}/`;
}