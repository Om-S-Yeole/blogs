document.querySelectorAll('input[name="categories"]').forEach(input => {
    input.addEventListener('change', function () {
        document.getElementById('category-filter-form').submit();
    });
});