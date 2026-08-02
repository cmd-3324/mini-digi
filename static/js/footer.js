    (function () {
        var form = document.getElementById('newsletterForm');
        var toast = document.getElementById('newsletterToast');
        var toastMsg = document.getElementById('toastMsg');
        var toastBar = document.getElementById('toastBar');
        var toastClose = document.getElementById('toastClose');
        var errorDiv = document.getElementById('newsletterError');
        var dismissTimer, barTimer;

        function showToast(msg) {
            toastMsg.textContent = msg;
            toast.classList.add('show');
            toastBar.style.transition = 'none';
            toastBar.style.width = '100%';
            void toast.offsetHeight;
            toastBar.style.transition = 'width 4.8s linear';
            toastBar.style.width = '0%';
            if (dismissTimer) clearTimeout(dismissTimer);
            dismissTimer = setTimeout(function () {
                toast.classList.remove('show');
            }, 5000);
        }

        function hideToast() {
            toast.classList.remove('show');
            if (dismissTimer) clearTimeout(dismissTimer);
        }

        toastClose.addEventListener('click', hideToast);

        form.addEventListener('submit', function (e) {
            e.preventDefault();
            errorDiv.style.display = 'none';
            var email = form.querySelector('input[name="email"]').value.trim();
            if (!email) return;

            var xhr = new XMLHttpRequest();
            xhr.open('POST', form.action, true);
            xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
            xhr.setRequestHeader('X-CSRFToken', form.querySelector('input[name="csrfmiddlewaretoken"]').value);
            xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
            xhr.onload = function () {
                var data = JSON.parse(xhr.responseText);
                if (data.ok) {
                    showToast(data.message);
                    form.querySelector('input[name="email"]').value = '';
                } else {
                    errorDiv.textContent = data.error;
                    errorDiv.style.display = 'block';
                }
            };
            xhr.onerror = function () {
                errorDiv.textContent = '{% trans "Network error. Please try again." %}';
                errorDiv.style.display = 'block';
            };
            xhr.send('email=' + encodeURIComponent(email));
        });
    })();