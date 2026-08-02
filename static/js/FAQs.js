
(function () {
    var searchInput = document.getElementById('faqSearchInput');
    var categoryBar = document.getElementById('faqCategoryBar');
    var faqList = document.getElementById('faqList');
    var emptyState = document.getElementById('faqEmptyState');
    if (!searchInput || !faqList) return;

    var items = Array.prototype.slice.call(faqList.querySelectorAll('.faq-item'));
    var groups = Array.prototype.slice.call(faqList.querySelectorAll('.faq-group'));
    var activeCategory = 'all';

    function applyFilter() {
        var query = searchInput.value.trim().toLowerCase();
        var visibleCount = 0;

        items.forEach(function (item) {
            var matchesCategory = activeCategory === 'all' || item.dataset.category === activeCategory;
            var text = item.textContent.toLowerCase();
            var matchesSearch = query === '' || text.indexOf(query) !== -1;
            var visible = matchesCategory && matchesSearch;

            item.classList.toggle('faq-hidden', !visible);
            if (query !== '') item.open = visible;
            if (visible) visibleCount++;
        });

        groups.forEach(function (group) {
            var hasVisible = group.querySelectorAll('.faq-item:not(.faq-hidden)').length > 0;
            group.style.display = hasVisible ? '' : 'none';
        });

        emptyState.classList.toggle('show', visibleCount === 0);
    }

    searchInput.addEventListener('input', applyFilter);

    categoryBar.addEventListener('click', function (e) {
        var btn = e.target.closest('.faq-cat-btn');
        if (!btn) return;
        categoryBar.querySelectorAll('.faq-cat-btn').forEach(function (b) { b.classList.remove('active'); });
        btn.classList.add('active');
        activeCategory = btn.dataset.category;
        applyFilter();
    });
})();
