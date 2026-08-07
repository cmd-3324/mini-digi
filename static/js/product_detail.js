document.addEventListener('DOMContentLoaded', function () {
    // ── Quantity controls ──
    var qtyInput = document.getElementById('qtyInput');
    var qtyMinus = document.getElementById('qtyMinus');
    var qtyPlus = document.getElementById('qtyPlus');
    var maxStock = qtyInput ? (parseInt(qtyInput.max) || 99) : 99;

    if (qtyMinus && qtyPlus && qtyInput) {
        function updateQtyBtns() {
            var v = parseInt(qtyInput.value);
            qtyMinus.disabled = v <= 1;
            qtyPlus.disabled = v >= maxStock;
        }
        qtyMinus.addEventListener('click', function() {
            var v = parseInt(qtyInput.value);
            if (v > 1) { qtyInput.value = v - 1; updateQtyBtns(); }
        });
        qtyPlus.addEventListener('click', function() {
            var v = parseInt(qtyInput.value);
            if (v < maxStock) { qtyInput.value = v + 1; updateQtyBtns(); }
        });
        updateQtyBtns();
    }

    // ── Image zoom on hover ──
    var imgWrap = document.getElementById('pdImageWrap');
    var mainImg = document.getElementById('pdMainImg');
    if (imgWrap && mainImg) {
        imgWrap.addEventListener('mousemove', function(e) {
            var rect = imgWrap.getBoundingClientRect();
            var x = (e.clientX - rect.left) / rect.width * 100;
            var y = (e.clientY - rect.top) / rect.height * 100;
            mainImg.style.transformOrigin = x + '% ' + y + '%';
        });
        imgWrap.addEventListener('mouseleave', function() {
            mainImg.style.transformOrigin = 'center center';
        });
    }

    // ── Heart pop animation (CSS injected once) ──
    (function injectFavStyle() {
        var s = document.createElement('style');
        s.textContent = '@keyframes pdHeartPop{0%{transform:scale(1)}30%{transform:scale(1.35)}60%{transform:scale(0.9)}100%{transform:scale(1)}} .pd-btn-fav.pop i{animation:pdHeartPop .4s ease}';
        document.head.appendChild(s);
    })();

    // ── Add to Cart AJAX ──
    document.addEventListener('submit', function (e) {
        var formEl = e.target;
        if (!formEl.classList.contains('js-add-to-cart')) return;
        e.preventDefault();
        var btn = formEl.querySelector('.pd-btn-cart');
        var origHTML = btn.innerHTML;
        btn.disabled = true;
        btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> {% trans "Adding..." %}';

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
            btn.innerHTML = '<i class="fas fa-check"></i> {% trans "Added!" %}';
            btn.style.background = '#28a745';
            btn.style.color = '#fff';
            setTimeout(function() {
                btn.innerHTML = origHTML;
                btn.style.background = '';
                btn.style.color = '';
            }, 1800);
        })
        .catch(function() {
            btn.disabled = false;
            btn.innerHTML = origHTML;
        });
    }, true);

    // ── Toggle Favorite AJAX ──
    document.addEventListener('click', function (e) {
        var heart = e.target.closest('.js-toggle-favorite');
        if (!heart) return;
        e.preventDefault();
        e.stopPropagation();

        // Prevent double-click
        if (heart.dataset.loading === '1') return;
        heart.dataset.loading = '1';

        fetch(heart.href, {
            method: 'GET',
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        })
        .then(function(r) { return r.json(); })
        .then(function(data) {
            heart.dataset.loading = '0';
            if (data.login_required) {
                window.location.href = '/accounts/login/';
                return;
            }
            var icon = heart.querySelector('i');
            if (data.is_favorited) {
                icon.classList.remove('far');
                icon.classList.add('fas');
                heart.classList.add('active');
            } else {
                icon.classList.remove('fas');
                icon.classList.add('far');
                heart.classList.remove('active');
            }
            // Pop animation
            heart.classList.remove('pop');
            void heart.offsetWidth;
            heart.classList.add('pop');

            document.querySelectorAll('.favorite-count-badge').forEach(function(badge) {
                badge.textContent = data.user_favorite_count;
            });
        })
        .catch(function() { heart.dataset.loading = '0'; });
    }, true);

    // ── Tab switching + localStorage persistence ──
    var tabKey = window.pdTabKey || 'pd_active_tab';

    function activatePdTab(targetId) {
        if (!targetId) return;
        var target = document.querySelector(targetId);
        if (!target) return;
        document.querySelectorAll('.pd-tabs .nav-link').forEach(function (b) {
            b.classList.remove('active');
        });
        document.querySelectorAll('.pd-tabs .tab-pane').forEach(function (p) {
            p.classList.remove('show', 'active');
        });
        var link = document.querySelector('.pd-tabs .nav-link[data-bs-target="' + targetId + '"]');
        if (link) link.classList.add('active');
        target.classList.add('show', 'active');
    }

    document.querySelectorAll('.pd-tabs .nav-link[data-bs-toggle="tab"]').forEach(function (btn) {
        btn.addEventListener('click', function () {
            var targetId = this.getAttribute('data-bs-target');
            activatePdTab(targetId);
            try { localStorage.setItem(tabKey, targetId); } catch (e) {}
        });
    });

    // ── On load: restore saved tab if present (inline script already set the default) ──
    var savedTab = null;
    try { savedTab = localStorage.getItem(tabKey); } catch (e) {}
    if (savedTab && document.querySelector('.pd-tabs .nav-link[data-bs-target="' + savedTab + '"]')) {
        activatePdTab(savedTab);
    }

    var pdTabsEl = document.querySelector('.pd-tabs');
    if (pdTabsEl) pdTabsEl.style.visibility = 'visible';
});





    document.addEventListener('DOMContentLoaded', function () {
        // ✅ FIXED: Using the CORRECT ID from your HTML
        const img = document.getElementById('pdMainImg');
        const btnIn = document.getElementById('zoom-in');
        const btnOut = document.getElementById('zoom-out');

        if (!img || !btnIn || !btnOut) return;

        let currentScale = 1;
        const STEP = 0.25;
        const MAX = 3;
        const MIN = 1;

        // Apply essential styles directly since extra_css is empty
        Object.assign(img.style, {
            transition: 'transform 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94)',
            transformOrigin: 'center center',
            width: '100%',
            height: 'auto',
            display: 'block'
        });

        // Ensure parent has relative positioning for absolute buttons
        const wrap = document.getElementById('pdImageWrap');
        if (wrap && getComputedStyle(wrap).position === 'static') {
            wrap.style.position = 'relative';
            wrap.style.overflow = 'hidden';
        }

        // Style buttons inline
        [btnIn, btnOut].forEach(btn => {
            Object.assign(btn.style, {
                width: '36px', height: '36px', border: 'none',
                borderRadius: '50%', background: 'rgba(255,255,255,0.9)',
                color: '#333', fontSize: '18px', fontWeight: '600',
                cursor: 'pointer', display: 'flex', alignItems: 'center',
                justifyContent: 'center', boxShadow: '0 2px 5px rgba(0,0,0,0.1)',
                transition: 'all 0.2s ease'
            });
            btn.onmouseenter = () => { if (!btn.disabled) btn.style.transform = 'scale(1.1)'; };
            btn.onmouseleave = () => { btn.style.transform = 'scale(1)'; };
        });

        // Style controls container
        const controls = document.querySelector('.zoom-controls');
        if (controls) {
            Object.assign(controls.style, {
                position: 'absolute', top: '10px', right: '10px',
                display: 'flex', gap: '8px', zIndex: '10'
            });
        }

        function updateZoom() {
            img.style.transform = `scale(${currentScale})`;
            btnOut.disabled = currentScale <= MIN;
            btnIn.disabled = currentScale >= MAX;
            btnOut.style.opacity = btnOut.disabled ? '0.3' : '1';
            btnIn.style.opacity = btnIn.disabled ? '0.3' : '1';
        }

        updateZoom();

        btnIn.onclick = () => {
            if (currentScale < MAX) { currentScale += STEP; updateZoom(); }
        };

        btnOut.onclick = () => {
            if (currentScale > MIN) { currentScale -= STEP; updateZoom(); }
        };

        img.ondblclick = () => { currentScale = 1; updateZoom(); };
    });

        $(document).ready(function () {
    var container = $('#commentList');
        var slug = container.data('product-slug');
        var listUrl = container.data('list-url');
         // ── Variant Selector + Gallery Thumbs ──
            function updatePdChips(color, size) {
                var attrBlock = $('.pd-attributes');
                if (!attrBlock.length) return;

                function setAttr(labelKey, value, textId, labelId, chipsId) {
                    var text = $('#' + textId);
                    if (value) {
                        if (!text.length) {
                            attrBlock.append(
                                '<div class="pd-attr-label" id="' + labelId + '">' + labelKey + '</div>' +
                                '<div class="pd-attr-chips" id="' + chipsId + '">' +
                                '<span class="pd-chip active" id="' + textId + '"></span></div>'
                            );
                            text = $('#' + textId);
                        }
                        text.text(value);
                        $('#' + labelId).show();
                        $('#' + chipsId).show();
                    } else {
                        if (labelId) $('#' + labelId).hide();
                        if (chipsId) $('#' + chipsId).hide();
                    }
                }

                setAttr('Color', color ? color.charAt(0).toUpperCase() + color.slice(1) : '', 'pdColorText', 'pdColorLabel', 'pdColorChips');
                setAttr('Size', size ? size.toUpperCase() : '', 'pdSizeText', 'pdSizeLabel', 'pdSizeChips');
            }

            function selectVariant(variantId, opts) {
                opts = opts || {};
                var btn = $('.variant-selector[data-variant-id="' + variantId + '"]').first();
                var thumb = $('.pd-gallery-thumb[data-variant-id="' + variantId + '"]').first();
                var source = btn.length ? btn : thumb;

                var imageUrl = opts.image || source.data('image') || thumb.data('image');
                var price = opts.price !== undefined ? opts.price : source.data('price');
                var stock = opts.stock !== undefined ? opts.stock : source.data('stock');
                var color = opts.color !== undefined ? opts.color : source.data('color');
                var size = opts.size !== undefined ? opts.size : source.data('size');

                if (imageUrl) {
                    $('#pdMainImg').attr('src', imageUrl);
                }
                if (price !== undefined && price !== null && price !== '') {
                    $('.pd-price').text((typeof currencySymbol !== 'undefined' ? currencySymbol : '') + Number(price).toLocaleString());
                }
                if (stock !== undefined) {
                    var stockEl = $('.pd-stock');
                    if (stock > 0) {
                        stockEl.removeClass('pd-stock-out').addClass('pd-stock-in')
                            .html('<i class="fas fa-check-circle"></i> In Stock — ' + stock + ' units available');
                    } else {
                        stockEl.removeClass('pd-stock-in').addClass('pd-stock-out')
                            .html('<i class="fas fa-times-circle"></i> Out of Stock');
                    }
                }

                $('.variant-selector').removeClass('active');
                if (btn.length) btn.addClass('active');

                $('.pd-gallery-thumb').removeClass('active');
                if (thumb.length) thumb.addClass('active');

                $('#selectedVariantId').val(variantId);

                updatePdChips(color, size);
            }

            $('.variant-selector').on('click', function () {
                selectVariant($(this).data('variant-id'));
            });

            $('.pd-gallery-thumb').on('click', function () {
                var t = $(this);
                selectVariant(t.data('variant-id'), {
                    image: t.data('image'),
                    price: t.data('price'),
                    stock: t.data('stock'),
                    color: t.data('color'),
                    size: t.data('size')
                });
            });

            // Initialize with default variant
            $('.variant-selector.active').click();
        // Load Carousel
        $.get(listUrl, {carousel: 1 }).done(function (data) {
            $('#reviewCarouselWrapper').html(data.html);
        // Initialize Bootstrap carousel if available
        if (typeof bootstrap !== 'undefined') {
            var carouselEl = document.querySelector('#reviewCarousel');
        if (carouselEl) new bootstrap.Carousel(carouselEl, {interval: 5000 });
        }
    });

        // Load Full Thread (your existing comments.js will handle this)
        // But to be safe, we load it here as well.
        $.get(listUrl).done(function (data) {
            container.html(data.html);
    });

        // Filter & Sort events (already in comments.js, but we'll wire them)
        $('#rvFilterPills').on('click', '.rv-pill', function () {
        var rating = $(this).data('rating');
        var sort = $('#rvSortSelect').val();
        $.get(listUrl, {rating: rating, sort: sort }).done(function (data) {
            container.html(data.html);
        });
    });

        $('#rvSortSelect').on('change', function () {
        var sort = $(this).val();
        var rating = $('#rvFilterPills .rv-pill.active').data('rating') || 'all';
        $.get(listUrl, {rating: rating, sort: sort }).done(function (data) {
            container.html(data.html);
        });
       
    });
});