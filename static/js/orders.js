$(document).ready(function () {
    var searchInput = $('#orderSearch');
    var statusFilter = $('#orderStatusFilter');
    var orderGrid = $('#orderGrid');
    var debounceTimer;
    var baseUrl = '{% url "dashboard:orders" %}';

    function fetchOrders() {
        var params = new URLSearchParams();
        var q = searchInput.val().trim();
        var status = statusFilter.val();
        if (q) params.set('q', q);
        if (status) params.set('status', status);
        var url = baseUrl + (params.toString() ? '?' + params.toString() : '');

        orderGrid.css('opacity', '0.5');
        fetch(url)
            .then(function (res) { return res.text(); })
            .then(function (html) {
                var doc = new DOMParser().parseFromString(html, 'text/html');
                var newGrid = doc.getElementById('orderGrid');
                if (newGrid) {
                    orderGrid.html(newGrid.innerHTML);
                    window.history.pushState(null, '', url);
                }
                orderGrid.css('opacity', '1');
            });
    }

    searchInput.on('input', function () {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(fetchOrders, 500);
    });

    statusFilter.on('change', fetchOrders);

    window.addEventListener('popstate', function () {
        var params = new URLSearchParams(window.location.search);
        searchInput.val(params.get('q') || '');
        statusFilter.val(params.get('status') || '');
        fetchOrders();
    });
});
