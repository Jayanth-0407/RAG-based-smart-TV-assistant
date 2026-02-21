const chatBox   = document.getElementById("chat-box");
const typingRow = document.getElementById("typing-row");
const chatPopup = document.getElementById("chatPopup");
const botPrompt = document.getElementById("botPrompt");

let chatOpened = false;

// ── Open / close popup ─────────────────────────────────────────────────────────
function toggleChat() {
  const isOpen = chatPopup.classList.toggle("open");
  if (isOpen) {
    botPrompt.style.display = "none";
    if (!chatOpened) {
      chatOpened = true;
      setTimeout(() => {
        appendMessage(
          "bot",
          `Hello! 👋 I'm **SamsungBot**, your Samsung Smart TV Manual Assistant.\n\nHow may i assist you?`,
        );
      }, 300);
    }
  }
}

// ── Markdown renderer ──────────────────────────────────────────────────────────
function renderMarkdown(text) {
  return text
    .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
    .replace(/\*(.*?)\*/g,   "<em>$1</em>")
    .replace(/\n/g, "<br/>");
}

// ── Append message bubble ──────────────────────────────────────────────────────
function appendMessage(from, text, sources = []) {
  const row    = document.createElement("div");
  row.className = `msg-row ${from}`;

  const avatar = document.createElement("div");
  avatar.className   = `msg-avatar ${from}`;
  avatar.textContent = from === "bot" ? "🤖" : "👤";

  const wrap = document.createElement("div");
  const bubble = document.createElement("div");
  bubble.className = `bubble ${from}`;
  bubble.innerHTML = renderMarkdown(text);
  wrap.appendChild(bubble);

  if (from === "bot" && sources.length > 0) {
    const chips = document.createElement("div");
    chips.className = "source-chips";
    sources.forEach(src => {
      const chip = document.createElement("span");
      chip.className   = "src-chip";
      chip.textContent = src;
      chips.appendChild(chip);
    });
    wrap.appendChild(chips);
  }

  if (from === "bot") {
    row.appendChild(avatar);
    row.appendChild(wrap);
  } else {
    wrap.style.display       = "flex";
    wrap.style.flexDirection = "column";
    wrap.style.alignItems    = "flex-end";
    row.appendChild(wrap);
    row.appendChild(avatar);
  }

  chatBox.appendChild(row);
  chatBox.scrollTop = chatBox.scrollHeight;
}

// ── Typing indicator ───────────────────────────────────────────────────────────
function showTyping(show) {
  typingRow.classList.toggle("visible", show);
  if (show) chatBox.scrollTop = chatBox.scrollHeight;
}

// ── Send to Flask RAG backend ──────────────────────────────────────────────────
async function sendMsg(text) {
  if (!text.trim()) return;

  appendMessage("user", text);
  document.getElementById("user-input").value = "";
  autoResize(document.getElementById("user-input"));
  showTyping(true);

  document.querySelectorAll(".topic-btn").forEach(btn => btn.classList.remove("active"));

  try {
    const res = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text })
    });
    const data = await res.json();
    showTyping(false);
    // Flask returns: { "reply": "...", "sources": ["doc.pdf"] }
    appendMessage("bot", data.reply, data.sources || []);
  } catch (e) {
    showTyping(false);
    appendMessage("bot", "⚠️ Could not reach the server. Please make sure Flask is running.");
  }
}

// ── Input helpers ──────────────────────────────────────────────────────────────
function sendFromInput() {
  const val = document.getElementById("user-input").value.trim();
  if (val) sendMsg(val);
}

function handleKey(e) {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendFromInput();
  }
}

function autoResize(el) {
  el.style.height = "auto";
  el.style.height = Math.min(el.scrollHeight, 80) + "px";
}