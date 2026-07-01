/**
 * Vex — MultiShop Chat Widget
 * static/js/chatbot-widget.js
 */
(function () {

    /* ── CONFIG ──────────────────────────────────────────── */
    var DJANGO_ENDPOINT = '/api/chat/';
    var MAX_MESSAGES = 12;   // per chat session

    

    var SYSTEM_PROMPT =
        'IDENTITY\n' +
        'You are Vex. That is your name, full stop — never refer to yourself as "an AI assistant," "a language model," "Claude," "GPT," or any other name. If asked "who are you" or "what are you," answer simply: "I\'m Vex, MultiShop\'s shopping assistant."\n' +
        'You work for MultiShop, a Django-based e-commerce store. You are not a general-purpose chatbot — you exist specifically to help MultiShop customers.\n\n' +
        'PERSONALITY\n' +
        'Friendly, direct, a little upbeat — like a knowledgeable store employee, not a corporate script. Short sentences. No filler like "I would be happy to assist you with that."\n\n' +
        'SCOPE\n' +
        'Only respond to questions about MultiShop, its products, and its policies.\n' +
        'For anything unrelated, reply: "I can only help with MultiShop products and orders — for other topics you will want a general assistant."\n' +
        'Never invent products, prices, stock, policies, or links. If info is unavailable, say: "I couldn\'t find that in our store records."\n\n' +
        'STYLE\n' +
        '- Concise and professional.\n' +
        '- Bullet points for product lists.\n' +
        '- Include relevant URLs when helpful.\n' +
        '- Only expand detail if the customer asks.\n\n' +
        'HELP WITH\n' +
        'Navigation: product pages, categories, cart, checkout, account, order tracking, shipping, returns, contact, FAQ.\n' +
        'Products: recommend, compare, explain specs/pricing/availability, suggest alternatives.\n' +
        'Orders: status, shipping timelines, return/refund process, payment questions.';
    /* ── STORAGE HELPERS ─────────────────────────────────── */
    var STORAGE_KEY = 'vex_chats';

    function loadChats() {
        try { return JSON.parse(localStorage.getItem(STORAGE_KEY)) || []; }
        catch (e) { return []; }
    }
    function saveChats(chats) {
        try { localStorage.setItem(STORAGE_KEY, JSON.stringify(chats)); }
        catch (e) { }
    }

    /* ── STATE ───────────────────────────────────────────── */
    var chats = loadChats();   // [{id, title, messages, date}]
    var activeChat = null;          // current chat object (reference into chats[])
    var msgCount = 0;             // user messages sent this session
    var isOpen = false;
    var showHist = false;

    function getCsrf() {
        var m = document.cookie.match(/(?:^|;\s*)csrftoken=([^;]*)/);
        return m ? decodeURIComponent(m[1]) : '';
    }
    function uid() {
        return Date.now().toString(36) + Math.random().toString(36).slice(2, 6);
    }
    function ts() {
        return new Date().toLocaleDateString('en-GB', { day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit' });
    }

    /* ── CSS ─────────────────────────────────────────────── */
    document.head.insertAdjacentHTML('beforeend', '<style>' +
        /* Toggle */
        '#vx-tog{position:fixed;bottom:26px;right:26px;z-index:10000;width:58px;height:58px;border-radius:50%;' +
        'background:#007bff;border:none;cursor:pointer;box-shadow:0 4px 20px rgba(0,123,255,.5);' +
        'display:flex;align-items:center;justify-content:center;transition:background .2s,transform .18s;}' +
        '#vx-tog:hover{background:#0069d9;transform:scale(1.08);}' +
        '#vx-tog i{color:#fff;font-size:22px;}' +
        '#vx-tog .vx-ic{display:block;}#vx-tog .vx-ix{display:none;}' +
        '#vx-tog.open .vx-ic{display:none;}#vx-tog.open .vx-ix{display:block;}' +
        /* Badge */
        '#vx-badge{position:absolute;top:-3px;right:-3px;background:#dc3545;color:#fff;' +
        'font-size:10px;font-weight:700;min-width:18px;height:18px;border-radius:9px;' +
        'display:none;align-items:center;justify-content:center;border:2px solid #fff;padding:0 3px;}' +
        '#vx-badge.on{display:flex;}' +
        /* Window */
        '#vx-win{position:fixed;bottom:96px;right:26px;z-index:9999;width:360px;height:560px;' +
        'max-height:calc(100vh - 110px);background:#fff;border-radius:10px;' +
        'box-shadow:0 12px 48px rgba(0,0,0,.18);border:1px solid #dee2e6;' +
        'display:none;flex-direction:column;overflow:hidden;font-family:Roboto,sans-serif;' +
        'opacity:0;transform:translateY(14px) scale(.97);transition:opacity .2s,transform .2s;}' +
        '#vx-win.on{display:flex;opacity:1;transform:none;}' +
        /* Header */
        '#vx-head{background:#1a1a2e;padding:13px 14px;display:flex;align-items:center;' +
        'gap:10px;flex-shrink:0;}' +
        '.vx-av{width:36px;height:36px;border-radius:50%;background:linear-gradient(135deg,#007bff,#6610f2);' +
        'display:flex;align-items:center;justify-content:center;flex-shrink:0;font-weight:800;' +
        'color:#fff;font-size:14px;letter-spacing:-.5px;}' +
        '.vx-ht{flex:1;}' +
        '.vx-ht h6{margin:0;color:#fff;font-size:14px;font-weight:700;letter-spacing:.3px;}' +
        '.vx-ht small{color:rgba(255,255,255,.55);font-size:11px;}' +
        '.vx-dot{width:8px;height:8px;border-radius:50%;background:#28a745;' +
        'border:1.5px solid rgba(255,255,255,.4);animation:vx-p 2s infinite;margin-right:2px;}' +
        '@keyframes vx-p{0%,100%{opacity:1}50%{opacity:.35}}' +
        /* Header buttons */
        '.vx-hbtn{background:rgba(255,255,255,.12);border:none;border-radius:6px;' +
        'color:#fff;cursor:pointer;width:30px;height:30px;display:flex;align-items:center;' +
        'justify-content:center;font-size:13px;transition:background .15s;flex-shrink:0;}' +
        '.vx-hbtn:hover{background:rgba(255,255,255,.22);}' +
        /* Counter bar */
        '#vx-counter{background:#f8f9fa;border-bottom:1px solid #dee2e6;' +
        'padding:5px 14px;font-size:11px;color:#6c757d;display:flex;' +
        'align-items:center;justify-content:space-between;flex-shrink:0;}' +
        '#vx-counter .vx-bar{flex:1;height:3px;background:#dee2e6;border-radius:2px;margin:0 10px;}' +
        '#vx-counter .vx-fill{height:100%;border-radius:2px;background:#007bff;transition:width .3s;}' +
        '#vx-counter .vx-fill.warn{background:#fd7e14;}' +
        '#vx-counter .vx-fill.full{background:#dc3545;}' +
        /* Messages */
        '#vx-msgs{flex:1;overflow-y:auto;padding:14px 12px;display:flex;flex-direction:column;' +
        'gap:10px;background:#f8f9fa;}' +
        '#vx-msgs::-webkit-scrollbar{width:4px;}' +
        '#vx-msgs::-webkit-scrollbar-thumb{background:#ced4da;border-radius:4px;}' +
        '.vx-row{display:flex;gap:7px;align-items:flex-end;}' +
        '.vx-row.u{flex-direction:row-reverse;}' +
        '.vx-bub{max-width:80%;padding:9px 13px;font-size:13.5px;line-height:1.5;' +
        'word-break:break-word;border-radius:16px;}' +
        '.vx-row.b .vx-bub{background:#fff;color:#212529;border:1px solid #dee2e6;border-bottom-left-radius:3px;}' +
        '.vx-row.u .vx-bub{background:#007bff;color:#fff;border-bottom-right-radius:3px;}' +
        '.vx-bub a{color:#007bff;}.vx-row.u .vx-bub a{color:#cfe2ff;}' +
        '.vx-bub ul{margin:5px 0 0;padding-left:16px;}.vx-bub li{margin-bottom:2px;}' +
        '.vx-sm-av{width:26px;height:26px;border-radius:50%;' +
        'background:linear-gradient(135deg,#007bff,#6610f2);flex-shrink:0;' +
        'display:flex;align-items:center;justify-content:center;' +
        'font-weight:800;color:#fff;font-size:10px;}' +
        /* Typing */
        '.vx-dots{display:flex;gap:4px;padding:9px 13px;background:#fff;' +
        'border:1px solid #dee2e6;border-radius:16px;border-bottom-left-radius:3px;width:fit-content;}' +
        '.vx-dots span{width:7px;height:7px;border-radius:50%;background:#adb5bd;animation:vx-b .85s infinite;}' +
        '.vx-dots span:nth-child(2){animation-delay:.14s;}.vx-dots span:nth-child(3){animation-delay:.28s;}' +
        '@keyframes vx-b{0%,60%,100%{transform:translateY(0)}30%{transform:translateY(-6px)}}' +
        /* Limit wall */
        '#vx-limit{display:none;flex-direction:column;align-items:center;justify-content:center;' +
        'gap:10px;padding:20px;text-align:center;background:#f8f9fa;flex:1;}' +
        '#vx-limit.on{display:flex;}' +
        '#vx-limit i{font-size:32px;color:#fd7e14;}' +
        '#vx-limit p{margin:0;font-size:13px;color:#495057;line-height:1.5;}' +
        '#vx-limit button{background:#007bff;color:#fff;border:none;border-radius:6px;' +
        'padding:9px 20px;font-size:13px;cursor:pointer;font-weight:600;}' +
        '#vx-limit button:hover{background:#0069d9;}' +
        /* Footer */
        '#vx-foot{padding:10px 12px;border-top:1px solid #dee2e6;background:#fff;flex-shrink:0;}' +
        '#vx-form{display:flex;gap:7px;}' +
        '#vx-input{flex:1;border:1px solid #ced4da;border-radius:6px;padding:8px 11px;' +
        'font-size:13.5px;color:#495057;font-family:Roboto,sans-serif;outline:none;' +
        'resize:none;max-height:90px;line-height:1.45;background:#fff;transition:border-color .15s;}' +
        '#vx-input:focus{border-color:#007bff;box-shadow:0 0 0 2px rgba(0,123,255,.15);}' +
        '#vx-input::placeholder{color:#adb5bd;}' +
        '#vx-input:disabled{background:#f8f9fa;cursor:not-allowed;}' +
        '#vx-send{width:38px;height:38px;border-radius:6px;flex-shrink:0;background:#007bff;' +
        'border:none;cursor:pointer;display:flex;align-items:center;justify-content:center;' +
        'transition:background .15s;align-self:flex-end;}' +
        '#vx-send:hover{background:#0069d9;}#vx-send:disabled{opacity:.4;cursor:not-allowed;}' +
        '#vx-send i{color:#fff;font-size:14px;}' +
        /* History panel */
        '#vx-hist{position:absolute;top:0;left:0;right:0;bottom:0;background:#fff;' +
        'z-index:10;display:none;flex-direction:column;}' +
        '#vx-hist.on{display:flex;}' +
        '#vx-hist-head{background:#1a1a2e;padding:13px 14px;display:flex;align-items:center;' +
        'gap:10px;flex-shrink:0;}' +
        '#vx-hist-head h6{margin:0;color:#fff;font-size:14px;font-weight:600;flex:1;}' +
        '#vx-hist-list{flex:1;overflow-y:auto;padding:10px;}' +
        '#vx-hist-list::-webkit-scrollbar{width:4px;}' +
        '#vx-hist-list::-webkit-scrollbar-thumb{background:#ced4da;border-radius:4px;}' +
        '.vx-hi{padding:10px 12px;border:1px solid #dee2e6;border-radius:8px;' +
        'margin-bottom:8px;cursor:pointer;transition:border-color .15s,background .15s;}' +
        '.vx-hi:hover{border-color:#007bff;background:#f0f7ff;}' +
        '.vx-hi h6{margin:0 0 2px;font-size:13px;font-weight:600;color:#212529;' +
        'white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}' +
        '.vx-hi small{color:#6c757d;font-size:11px;}' +
        '.vx-hi .vx-hi-meta{display:flex;justify-content:space-between;align-items:center;}' +
        '.vx-hi .vx-hi-cnt{font-size:11px;color:#adb5bd;}' +
        '#vx-hist-empty{padding:30px;text-align:center;color:#adb5bd;font-size:13px;}' +
        /* Mobile */
        '@media(max-width:400px){#vx-win{width:calc(100vw - 16px);right:8px;}}' +
        '@media(prefers-reduced-motion:reduce){#vx-tog,#vx-win{transition:none;}' +
        '.vx-dots span,.vx-dot{animation:none;}}' +
        '</style>');

    /* ── MARKUP ──────────────────────────────────────────── */
    document.body.insertAdjacentHTML('beforeend',
        '<button id="vx-tog" aria-label="Chat with Vex">' +
        '<div id="vx-badge"></div>' +
        '<i class="fas fa-comment-dots vx-ic"></i>' +
        '<i class="fas fa-times vx-ix"></i>' +
        '</button>' +

        '<div id="vx-win" role="dialog" aria-label="Vex Assistant" aria-modal="true">' +

        /* Header */
        '<div id="vx-head">' +
        '<div class="vx-av">VX</div>' +
        '<div class="vx-ht"><h6>Vex</h6><small>MultiShop Assistant</small></div>' +
        '<div class="vx-dot"></div>' +
        '<button class="vx-hbtn" id="vx-hist-btn" title="Chat history"><i class="fas fa-history"></i></button>' +
        '<button class="vx-hbtn" id="vx-new-btn" title="New chat"><i class="fas fa-plus"></i></button>' +
        '</div>' +

        /* Message counter bar */
        '<div id="vx-counter">' +
        '<span id="vx-cnt-lbl">0 / ' + MAX_MESSAGES + '</span>' +
        '<div class="vx-bar"><div class="vx-fill" id="vx-fill" style="width:0%"></div></div>' +
        '<span>messages</span>' +
        '</div>' +

        /* Messages */
        '<div id="vx-msgs"></div>' +

        /* Limit wall (shown when MAX_MESSAGES hit) */
        '<div id="vx-limit">' +
        '<i class="fas fa-comment-slash"></i>' +
        '<p>You\'ve reached the <strong>' + MAX_MESSAGES + ' message limit</strong> for this chat.<br>Start a new chat to keep going. Your history is saved.</p>' +
        '<button id="vx-limit-new"><i class="fas fa-plus"></i> New Chat</button>' +
        '</div>' +

        /* Footer */
        '<div id="vx-foot">' +
        '<div id="vx-form">' +
        '<textarea id="vx-input" rows="1" placeholder="Ask Vex anything\u2026" aria-label="Message"></textarea>' +
        '<button id="vx-send" aria-label="Send"><i class="fas fa-paper-plane"></i></button>' +
        '</div>' +
        '</div>' +

        /* History panel (overlays everything) */
        '<div id="vx-hist">' +
        '<div id="vx-hist-head">' +
        '<div class="vx-av">VX</div>' +
        '<h6>Chat History</h6>' +
        '<button class="vx-hbtn" id="vx-hist-close" title="Back"><i class="fas fa-arrow-left"></i></button>' +
        '</div>' +
        '<div id="vx-hist-list"></div>' +
        '</div>' +

        '</div>'
    );

    /* ── REFS ────────────────────────────────────────────── */
    var tog = document.getElementById('vx-tog');
    var win = document.getElementById('vx-win');
    var feed = document.getElementById('vx-msgs');
    var input = document.getElementById('vx-input');
    var sendBtn = document.getElementById('vx-send');
    var badge = document.getElementById('vx-badge');
    var cntLbl = document.getElementById('vx-cnt-lbl');
    var fill = document.getElementById('vx-fill');
    var limitWall = document.getElementById('vx-limit');
    var foot = document.getElementById('vx-foot');
    var histPanel = document.getElementById('vx-hist');
    var histList = document.getElementById('vx-hist-list');

    /* ── OPEN / CLOSE ────────────────────────────────────── */
    function openWin() {
        isOpen = true;
        tog.classList.add('open');
        win.style.display = 'flex';
        requestAnimationFrame(function () { win.classList.add('on'); });
        badge.classList.remove('on');
        if (!activeChat) newChat();
        input.focus();
    }
    function closeWin() {
        isOpen = false;
        tog.classList.remove('open');
        win.classList.remove('on');
        setTimeout(function () { win.style.display = 'none'; }, 200);
    }
    tog.addEventListener('click', function () { isOpen ? closeWin() : openWin(); });
    document.addEventListener('click', function (e) {
        if (isOpen && !win.contains(e.target) && !tog.contains(e.target)) closeWin();
    });

    /* ── NEW CHAT ─────────────────────────────────────────── */
    function newChat() {
        // Save current chat if it has messages
        if (activeChat && activeChat.messages.length > 0) {
            var exists = chats.find(function (c) { return c.id === activeChat.id; });
            if (!exists) chats.unshift(activeChat);
            saveChats(chats);
        }

        activeChat = { id: uid(), title: 'Chat ' + ts(), messages: [], date: ts() };
        msgCount = 0;
        feed.innerHTML = '';
        limitWall.classList.remove('on');
        foot.style.display = '';
        feed.style.display = 'flex';
        updateCounter();
        greet();
    }

    document.getElementById('vx-new-btn').addEventListener('click', newChat);
    document.getElementById('vx-limit-new').addEventListener('click', newChat);

    /* ── GREETING ─────────────────────────────────────────── */
    function greet() {
        addBubble('bot', "Hey! \uD83D\uDC4B I\u2019m Vex, your MultiShop assistant. I can help you find products, track orders, or answer questions about shipping and returns. What can I help you with?");
    }

    /* ── COUNTER ──────────────────────────────────────────── */
    function updateCounter() {
        var pct = (msgCount / MAX_MESSAGES) * 100;
        cntLbl.textContent = msgCount + ' / ' + MAX_MESSAGES;
        fill.style.width = pct + '%';
        fill.className = 'vx-fill' + (pct >= 100 ? ' full' : pct >= 70 ? ' warn' : '');
    }

    function hitLimit() {
        feed.style.display = 'none';
        limitWall.classList.add('on');
        foot.style.display = 'none';
        // Save this chat
        var exists = chats.find(function (c) { return c.id === activeChat.id; });
        if (!exists) chats.unshift(activeChat);
        else chats[chats.indexOf(exists)] = activeChat;
        saveChats(chats);
    }

    /* ── BUBBLE ───────────────────────────────────────────── */
    function addBubble(role, text) {
        var row = document.createElement('div');
        row.className = 'vx-row ' + (role === 'bot' ? 'b' : 'u');
        if (role === 'bot') {
            row.innerHTML = '<div class="vx-sm-av">VX</div><div class="vx-bub">' + fmt(text) + '</div>';
        } else {
            row.innerHTML = '<div class="vx-bub">' + esc(text) + '</div>';
        }
        feed.appendChild(row);
        feed.scrollTop = feed.scrollHeight;
    }
    function showDots() {
        var row = document.createElement('div');
        row.className = 'vx-row b'; row.id = 'vx-dots';
        row.innerHTML = '<div class="vx-sm-av">VX</div><div class="vx-dots"><span></span><span></span><span></span></div>';
        feed.appendChild(row); feed.scrollTop = feed.scrollHeight;
    }
    function hideDots() { var el = document.getElementById('vx-dots'); if (el) el.remove(); }

    /* ── TEXT HELPERS ─────────────────────────────────────── */
    function esc(s) { return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
    function fmt(s) {
        return esc(s)
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/^[-\u2022]\s+(.+)$/gm, '<li>$1</li>')
            .replace(/((<li>[^]*?<\/li>\n?)+)/g, '<ul>$1</ul>')
            .replace(/\[([^\]]+)\]\((https?:\/\/[^\)]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>')
            .replace(/\n/g, '<br>');
    }

    /* ── AUTO-GROW ────────────────────────────────────────── */
    input.addEventListener('input', function () {
        input.style.height = 'auto';
        input.style.height = Math.min(input.scrollHeight, 90) + 'px';
    });

    /* ── SEND ─────────────────────────────────────────────── */
    function doSend() {
        var text = input.value.trim();
        if (!text || sendBtn.disabled || msgCount >= MAX_MESSAGES) return;

        input.value = ''; input.style.height = 'auto'; sendBtn.disabled = true;

        addBubble('user', text);
        activeChat.messages.push({ role: 'user', content: text });
        msgCount++;
        updateCounter();
        showDots();

        // Auto-title chat from first message
        if (msgCount === 1) {
            activeChat.title = text.length > 40 ? text.slice(0, 40) + '…' : text;
        }

        fetch(DJANGO_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrf(),
            },
            body: JSON.stringify({
                messages: activeChat.messages.slice(-20),
                system: SYSTEM_PROMPT,
            }),
        })
            .then(function (r) {
                if (!r.ok) throw new Error('HTTP ' + r.status);
                return r.json();
            })
            .then(function (d) {
                var reply = d.reply || d.content || 'Sorry, unexpected response.';
                activeChat.messages.push({ role: 'assistant', content: reply });

                // Persist after every exchange
                var idx = chats.findIndex(function (c) { return c.id === activeChat.id; });
                if (idx === -1) chats.unshift(activeChat);
                else chats[idx] = activeChat;
                saveChats(chats);

                hideDots();
                addBubble('bot', reply);

                if (!isOpen) { badge.textContent = '1'; badge.classList.add('on'); }
                if (msgCount >= MAX_MESSAGES) hitLimit();
            })
            .catch(function (err) {
                hideDots();
                addBubble('bot', "Sorry, I couldn\u2019t connect right now. Please try again.");
                console.error('[Vex]', err);
            })
            .finally(function () { sendBtn.disabled = false; input.focus(); });
    }

    sendBtn.addEventListener('click', doSend);
    input.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); doSend(); }
    });

    /* ── HISTORY PANEL ────────────────────────────────────── */
    function openHistory() {
        showHist = true;
        histList.innerHTML = '';
        var saved = chats.filter(function (c) { return c.messages.length > 0; });

        if (saved.length === 0) {
            histList.innerHTML = '<p id="vx-hist-empty">No previous chats yet.</p>';
        } else {
            saved.forEach(function (chat) {
                var item = document.createElement('div');
                item.className = 'vx-hi';
                item.innerHTML =
                    '<div class="vx-hi-meta">' +
                    '<h6>' + esc(chat.title || 'Chat') + '</h6>' +
                    '<span class="vx-hi-cnt">' + Math.floor(chat.messages.length / 2) + ' exchanges</span>' +
                    '</div>' +
                    '<small>' + (chat.date || '') + '</small>';
                item.addEventListener('click', function () { loadChat(chat); });
                histList.appendChild(item);
            });
        }
        histPanel.classList.add('on');
    }
    function closeHistory() {
        showHist = false;
        histPanel.classList.remove('on');
    }
    function loadChat(chat) {
        // Save current if needed
        if (activeChat && activeChat.messages.length > 0) {
            var idx = chats.findIndex(function (c) { return c.id === activeChat.id; });
            if (idx === -1) chats.unshift(activeChat);
            saveChats(chats);
        }
        activeChat = chat;
        msgCount = Math.floor(chat.messages.filter(function (m) { return m.role === 'user'; }).length);
        feed.innerHTML = '';
        limitWall.classList.remove('on');
        feed.style.display = 'flex';

        if (msgCount >= MAX_MESSAGES) {
            hitLimit();
        } else {
            foot.style.display = '';
        }

        // Render messages
        chat.messages.forEach(function (m) {
            addBubble(m.role === 'user' ? 'user' : 'bot', m.content);
        });

        updateCounter();
        closeHistory();
    }

    document.getElementById('vx-hist-btn').addEventListener('click', openHistory);
    document.getElementById('vx-hist-close').addEventListener('click', closeHistory);

})();