
document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('filter-form');
    const grid = document.getElementById('product-grid');
    const searchInput = document.getElementById('search-input');
    const clearBtn = document.getElementById('clear-filters-btn');
    let timeout = null;

    function fetchProducts(url) {
        grid.style.opacity = '0.5';
        fetch(url)
            .then(res => res.text())
            .then(html => {
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, 'text/html');
                const newGrid = doc.getElementById('product-grid');

                if (!newGrid) {
                    console.error("Django returned an error. Check server logs.");
                    grid.style.opacity = '1';
                    return;
                }

                grid.innerHTML = newGrid.innerHTML;
                grid.style.opacity = '1';
                window.history.pushState(null, '', url);
            });
    }

    function updateGrid() {
        const params = new URLSearchParams(new FormData(form));
        for (const [key, value] of [...params.entries()]) {
            if (!value) params.delete(key);
        }
        fetchProducts(`${form.action}?${params.toString()}`);
    }

    form.addEventListener('change', (e) => {
        if (e.target.classList.contains('filter-input')) updateGrid();
    });

    searchInput.addEventListener('input', () => {
        clearTimeout(timeout);
        timeout = setTimeout(updateGrid, 500);
    });

    form.addEventListener('submit', (e) => {
        if (e.target.classList.contains('js-add-to-cart')) return;
        e.preventDefault();
        updateGrid();
    });

    clearBtn.addEventListener('click', () => {
        form.reset();
        form.querySelectorAll('input[type="checkbox"], input[type="radio"]').forEach(el => el.checked = false);
        searchInput.value = '';
        document.getElementById('price-all').checked = true;
        form.querySelector('select[name="sort"]').value = 'latest';
        form.querySelector('select[name="per_page"]').value = '9';
        updateGrid();
    });

    document.addEventListener('click', (e) => {
        if (e.target.tagName === 'A' && e.target.classList.contains('ajax-link')) {
            e.preventDefault();
            fetchProducts(e.target.href);
            grid.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    });

    function getCookie(name) {
        const v = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
        return v ? v.pop() : '';
    }

    document.addEventListener('submit', function(e) {
        if (!e.target.classList.contains('js-add-to-cart')) return;
        e.preventDefault();
        var formEl = e.target;
        var btn = formEl.querySelector('button[type="submit"]');
        btn.disabled = true;
        fetch(formEl.action, {
            method: 'POST',
            body: new FormData(formEl),
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        })
        .then(function(r) { return r.json(); })
        .then(function(data) {
            btn.disabled = false;
            if (data.login_required) {
                window.location.href = '/accounts/login/';
                return;
            }
            document.querySelectorAll('.cart-count-badge').forEach(function(badge) {
                badge.textContent = data.cart_count;
                badge.style.display = data.cart_count ? '' : 'none';
            });
            btn.innerHTML = '<i class="fa fa-check"></i>';
            setTimeout(function() { btn.innerHTML = '<i class="fa fa-shopping-cart"></i>'; }, 1500);
        })
        .catch(function() { btn.disabled = false; });
    }, true);

    document.addEventListener('click', function (e) {
        var heart = e.target.closest('.js-toggle-favorite');
        if (!heart) return;
        e.preventDefault();
        fetch(heart.href, {
            method: 'GET',
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        })
            .then(function (r) { return r.json(); })
            .then(function (data) {
                if (data.login_required) {
                    window.location.href = '/accounts/login/';
                    return;
                }
                var icon = heart.querySelector('i');
                if (data.is_favorited) {
                    icon.classList.remove('far');
                    icon.classList.add('fas');
                } else {
                    icon.classList.remove('fas');
                    icon.classList.add('far');
                }
                document.querySelectorAll('.favorite-count-badge').forEach(function (badge) {
                    badge.textContent = data.user_favorite_count;
                });
            });
    }, true);

    window.addEventListener('popstate', () => fetchProducts(window.location.href));
});
