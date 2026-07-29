$(function () {
    var container = $('#commentList');
    if (!container.length) return;

    var productSlug = container.data('product-slug');
    var createUrl = container.data('create-url');
    var listUrl = container.data('list-url');
    var editUrlBase = container.data('edit-url-base');   // ends in ".../0/edit/"
    var deleteUrlBase = container.data('delete-url-base'); // ends in ".../0/delete/"
    var likeUrlBase = container.data('like-url-base');
    var dislikeUrlBase = container.data('dislike-url-base');

    function editUrl(id) { return editUrlBase.replace(/0(?=\/[^/]*\/?$)/, id); }
    function deleteUrl(id) { return deleteUrlBase.replace(/0(?=\/[^/]*\/?$)/, id); }
    function likeUrl(id) { return likeUrlBase.replace(/0(?=\/[^/]*\/?$)/, id); }
    function dislikeUrl(id) { return dislikeUrlBase.replace(/0(?=\/[^/]*\/?$)/, id); }

    function getCsrf() {
        var m = document.cookie.match(/(?:^|;\s*)csrftoken=([^;]*)/);
        return m ? decodeURIComponent(m[1]) : '';
    }

    function postJSON(url, data) {
        return $.ajax({
            url: url,
            method: 'POST',
            headers: { 'X-CSRFToken': getCsrf(), 'Content-Type': 'application/json' },
            data: JSON.stringify(data),
        });
    }

    // New top-level review
    $('#rvNewReviewForm').on('submit', function (e) {
        e.preventDefault();
        var body = $(this).find('textarea[name="body"]').val().trim();
        var rating = $('#rvRatingValue').val();
        if (!rating) { alert('Please select a rating.'); return; }
        if (!body) return;
        postJSON(createUrl, { body: body, rating: parseInt(rating, 10) }).done(function (resp) {
            if (resp.ok) {
                container.prepend(resp.html);
                $('#rvNewReviewForm')[0].reset();
                $('#rvRatingValue').val('');
                $('#rvRatingInput i').removeClass('fas').addClass('far');
            }
        });
    });

    // Star picker
    $('#rvRatingInput').on('click', 'i', function () {
        var val = $(this).data('value');
        $('#rvRatingValue').val(val);
        $('#rvRatingInput i').each(function () {
            $(this).toggleClass('fas', $(this).data('value') <= val)
                   .toggleClass('far', $(this).data('value') > val);
        });
    });

    // Reply toggle
    container.on('click', '.rv-reply-btn', function () {
        var id = $(this).data('id');
        var slot = $('#rv-reply-form-' + id);
        if (slot.children().length) { slot.empty(); return; }
        slot.html(
            '<textarea class="rv-reply-textarea"></textarea>' +
            '<button class="rv-reply-submit" data-id="' + id + '">Post Reply</button>'
        );
    });

    // Submit reply
    container.on('click', '.rv-reply-submit', function () {
        var parentId = $(this).data('id');
        var slot = $('#rv-reply-form-' + parentId);
        var body = slot.find('textarea').val().trim();
        if (!body) return;
        postJSON(createUrl, { body: body, parent_id: parentId }).done(function (resp) {
            if (resp.ok) {
                var item = container.find('.rv-item[data-id="' + parentId + '"]').first();
                var repliesBox = item.children('.rv-replies');
                if (!repliesBox.length) {
                    item.append('<div class="rv-replies"></div>');
                    repliesBox = item.children('.rv-replies');
                }
                repliesBox.append(resp.html);
                slot.empty();
            }
        });
    });

    // Edit
    container.on('click', '.rv-edit-btn', function () {
        var id = $(this).data('id');
        var item = container.find('.rv-item[data-id="' + id + '"]').first();
        var bodyEl = item.children('.rv-body').first();
        var original = bodyEl.text();
        bodyEl.html(
            '<textarea class="rv-edit-textarea">' + original + '</textarea>' +
            '<button class="rv-edit-save" data-id="' + id + '">Save</button>'
        );
    });

    container.on('click', '.rv-edit-save', function () {
        var id = $(this).data('id');
        var item = container.find('.rv-item[data-id="' + id + '"]').first();
        var newBody = item.find('.rv-edit-textarea').val().trim();
        if (!newBody) return;
        postJSON(editUrl(id), { body: newBody }).done(function (resp) {
            if (resp.ok) item.children('.rv-body').first().text(resp.body);
        });
    });

    // Delete
    container.on('click', '.rv-delete-btn', function () {
        if (!confirm('Delete this comment?')) return;
        var id = $(this).data('id');
        postJSON(deleteUrl(id), {}).done(function (resp) {
            if (resp.ok) container.find('.rv-item[data-id="' + id + '"]').first().remove();
        });
    });

    // Rating filter pills
    $('#rvFilterPills').on('click', '.rv-pill', function () {
        $('.rv-pill').removeClass('active');
        $(this).addClass('active');
        $.get(listUrl, { rating: $(this).data('rating') }).done(function (resp) {
            container.html(resp.html);
        });
    });

    // Like
    container.on('click', '.rv-like-btn', function () {
        var id = $(this).data('id');
        var item = container.find('.rv-item[data-id="' + id + '"]').first();
        postJSON(likeUrl(id), {}).done(function (resp) {
            if (!resp.ok) return;
            item.children('.rv-actions').find('.rv-like-btn').toggleClass('active', resp.liked)
                .find('.rv-like-count').text(resp.like_count);
            item.children('.rv-actions').find('.rv-dislike-btn').toggleClass('active', resp.disliked)
                .find('.rv-dislike-count').text(resp.dislike_count);
        });
    });

    // Dislike
    container.on('click', '.rv-dislike-btn', function () {
        var id = $(this).data('id');
        var item = container.find('.rv-item[data-id="' + id + '"]').first();
        postJSON(dislikeUrl(id), {}).done(function (resp) {
            if (!resp.ok) return;
            item.children('.rv-actions').find('.rv-dislike-btn').toggleClass('active', resp.disliked)
                .find('.rv-dislike-count').text(resp.dislike_count);
            item.children('.rv-actions').find('.rv-like-btn').toggleClass('active', resp.liked)
                .find('.rv-like-count').text(resp.like_count);
        });
    });
});