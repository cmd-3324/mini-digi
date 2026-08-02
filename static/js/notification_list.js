(function () {
var container = document.getElementById('notifListContainer');
var typeFilter = document.getElementById('notifTypeFilter');
var readFilter = document.getElementById('notifReadFilter');
var btnMarkAll = document.getElementById('btnMarkAllRead');
var btnDeleteAll = document.getElementById('btnDeleteAll');
var unreadBadge = document.querySelector('.notif-unread-badge');
var baseUrl = '{% url "dashboard:notifications" %}';

function getParams() {
    var params = new URLSearchParams();
    var t = typeFilter.value;
    var r = readFilter.value;
    if (t) params.set('type', t);
    if (r) params.set('read', r);
    return params;
}

function fetchList() {
    var params = getParams();
    var url = baseUrl + (params.toString() ? '?' + params.toString() : '');
    container.style.opacity = '0.4';
    fetch(url)
        .then(function (res) { return res.text(); })
        .then(function (html) {
            var doc = new DOMParser().parseFromString(html, 'text/html');
            var newList = doc.getElementById('notifListContainer');
            if (newList) {
                container.innerHTML = newList.innerHTML;
                window.history.pushState(null, '', url);
                rebind();
            }
            container.style.opacity = '1';
        });
}

function updateBadge(count) {
    if (unreadBadge) {
        if (count > 0) {
            unreadBadge.textContent = count;
            unreadBadge.style.display = '';
        } else {
            unreadBadge.style.display = 'none';
        }
    } else if (count > 0) {
        var h4 = document.querySelector('.font-weight-semi-bold');
        if (h4) {
            var span = document.createElement('span');
            span.className = 'badge badge-pill badge-primary ml-2 notif-unread-badge';
            span.textContent = count;
            h4.appendChild(span);
            unreadBadge = span;
        }
    }
}

function postAjax(url, callback) {
    fetch(url, {
        method: 'POST',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': getCSRF()
        }
    })
    .then(function (r) { return r.json(); })
    .then(function (data) {
        if (data.ok) {
            if (data.unread_count !== undefined) updateBadge(data.unread_count);
            if (callback) callback(data);
        }
    });
}

function rebind() {
    container.querySelectorAll('.js-notif-read').forEach(function (el) {
        el.addEventListener('click', function (e) {
            e.preventDefault();
            var id = el.getAttribute('data-id');
            var item = el.closest('.notif-item');
            postAjax('{% url "dashboard:notification_mark_read" 0 %}'.replace('0', id), function () {
                if (item) item.classList.remove('notif-unread');
                var dot = item ? item.querySelector('.notif-dot') : null;
                if (dot) dot.remove();
                var readBtn = item ? item.querySelector('.js-notif-read') : null;
                if (readBtn && readBtn.textContent.trim().indexOf('Mark') !== -1) readBtn.remove();
            });
        });
    });

    container.querySelectorAll('.js-notif-delete').forEach(function (el) {
        el.addEventListener('click', function (e) {
            e.preventDefault();
            var id = el.getAttribute('data-id');
            var item = el.closest('.notif-item');
            postAjax('{% url "dashboard:notification_delete" 0 %}'.replace('0', id), function () {
                if (item) {
                    item.style.transition = 'opacity .25s ease, transform .25s ease';
                    item.style.opacity = '0';
                    item.style.transform = 'translateX(30px)';
                    setTimeout(function () {
                        item.remove();
                        if (!container.querySelector('.notif-item')) fetchList();
                    }, 260);
                }
            });
        });
    });

    container.querySelectorAll('.notif-page-link').forEach(function (el) {
        el.addEventListener('click', function (e) {
            e.preventDefault();
            var page = el.getAttribute('data-page');
            if (!page) return;
            var params = getParams();
            params.set('page', page);
            var url = baseUrl + '?' + params.toString();
            container.style.opacity = '0.4';
            fetch(url)
                .then(function (res) { return res.text(); })
                .then(function (html) {
                    var doc = new DOMParser().parseFromString(html, 'text/html');
                    var newList = doc.getElementById('notifListContainer');
                    if (newList) {
                        container.innerHTML = newList.innerHTML;
                        window.history.pushState(null, '', url);
                        rebind();
                    }
                    container.style.opacity = '1';
                });
        });
    });
}

typeFilter.addEventListener('change', fetchList);
readFilter.addEventListener('change', fetchList);

if (btnMarkAll) {
    btnMarkAll.addEventListener('click', function () {
        postAjax('{% url "dashboard:notification_mark_all_read" %}', function () {
            container.querySelectorAll('.notif-unread').forEach(function (el) {
                el.classList.remove('notif-unread');
                var dot = el.querySelector('.notif-dot');
                if (dot) dot.remove();
            });
        });
    });
}

if (btnDeleteAll) {
    btnDeleteAll.addEventListener('click', function () {
        if (!confirm('{% trans "Clear all notifications?" %}')) return;
        postAjax('{% url "dashboard:notification_delete_all" %}', function () {
            fetchList();
        });
    });
}

window.addEventListener('popstate', function () {
    var params = new URLSearchParams(window.location.search);
    typeFilter.value = params.get('type') || '';
    readFilter.value = params.get('read') || '';
    fetchList();
});

rebind();
})();
