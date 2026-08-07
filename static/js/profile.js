$(document).ready(function () {
    // Phone number validation
    $('#phoneInput').on('input', function () {
        this.value = this.value.replace(/[^0-9+]/g, '');
        if (this.value.length > 0 && !this.value.startsWith('+')) {
            this.value = '+' + this.value.replace(/\+/g, '');
        }
    });

    // Password strength indicator
    $('#newPasswordInput').on('input', function () {
        var val = $(this).val();
        var score = 0;
        if (val.length >= 6) score++;
        if (val.length >= 10) score++;
        if (/[A-Z]/.test(val) && /[a-z]/.test(val)) score++;
        if (/[0-9]/.test(val) || /[^A-Za-z0-9]/.test(val)) score++;

        var cls = score <= 1 ? 'active-weak' : score <= 2 ? 'active-medium' : 'active-strong';
        for (var i = 1; i <= 4; i++) {
            var bar = $('#str' + i);
            bar.removeClass('active-weak active-medium active-strong');
            if (i <= score) bar.addClass(cls);
        }
    });

    // Profile form AJAX
    $('#profileForm').on('submit', function (e) {
        e.preventDefault();
        var btn = $('#profileSaveBtn');
        var origHTML = btn.html();
        btn.prop('disabled', true).html('<i class="fas fa-spinner fa-spin"></i> ' + (window.profileStrings ? window.profileStrings.saving : 'Saving...'));

        var data = {};
        $(this).serializeArray().forEach(function (field) {
            if (field.name !== 'csrfmiddlewaretoken') data[field.name] = field.value;
        });

        $.ajax({
            url: window.profileUpdateUrl,
            method: 'POST',
            headers: { 'X-CSRFToken': getCSRF(), 'Content-Type': 'application/json' },
            data: JSON.stringify(data),
            success: function (resp) {
                if (resp.ok) {
                    showToast(resp.message);
                    btn.closest('.pf-card').addClass('pf-success-flash');
                    setTimeout(function() { btn.closest('.pf-card').removeClass('pf-success-flash'); }, 600);
                }
            },
            error: function () { showToast(window.profileStrings ? window.profileStrings.error : 'Error saving profile.'); },
            complete: function () {
                btn.prop('disabled', false).html(origHTML);
            }
        });
    });

    // Password form AJAX
    $('#passwordForm').on('submit', function (e) {
        e.preventDefault();
        var btn = $('#passwordSaveBtn');
        var origHTML = btn.html();
        var errBox = $('#passwordError');
        errBox.hide();
        btn.prop('disabled', true).html('<i class="fas fa-spinner fa-spin"></i> ' + (window.profileStrings ? window.profileStrings.updating : 'Updating...'));

        var data = {};
        $(this).serializeArray().forEach(function (field) {
            if (field.name !== 'csrfmiddlewaretoken') data[field.name] = field.value;
        });

        $.ajax({
            url: window.changePasswordUrl,
            method: 'POST',
            headers: { 'X-CSRFToken': getCSRF(), 'Content-Type': 'application/json' },
            data: JSON.stringify(data),
            success: function (resp) {
                if (resp.ok) {
                    showToast(resp.message);
                    $('#passwordForm')[0].reset();
                    $('.pf-strength-bar').removeClass('active-weak active-medium active-strong');
                } else {
                    $('#passwordErrorMsg').text(resp.error);
                    errBox.show();
                }
            },
            error: function () {
                $('#passwordErrorMsg').text(window.profileStrings ? window.profileStrings.pwdError : 'Error changing password.');
                errBox.show();
            },
            complete: function () {
                btn.prop('disabled', false).html(origHTML);
            }
        });
    });
});
