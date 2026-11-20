"""Plot Twist — the 3D campus game, inside Streamlit.

Run:  uv run streamlit run app_3d.py
This is the file to publish when the 3D version should be what everybody sees.
app.py (the plain version) is untouched and stays as the fallback.

How it works (the 3D page lives in an iframe, a Streamlit "component"):
1. The browser draws the 3D campus and the buttons (prototypes/campus-3d).
2. When the player does something, the page sends a small JSON command to Python
   through the component (the same commands the local server accepts).
3. campus_game.command() checks the command and calls game.py — all the rules and
   all the saving stay in logic.py / db.py. The browser can never set state itself.
4. The answer goes back to the page the same way, and the page redraws.
"""

import sys
import tempfile
import threading
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

PROJECT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT / "prototypes" / "campus-3d"))

import db  # noqa: E402
from campus_game import command  # noqa: E402
from page3d import build_page  # noqa: E402

# Same separate saves as the local 3D server, so the plain game's saves are not touched.
db.DB_PATH = PROJECT / "data" / "campus3d.db"

# Runs inside the iframe, before the game page: sends commands to Python and waits for the answer.
BRIDGE = """<script>
(function () {
  const pending = new Map();
  let counter = Date.now();
  const post = message => window.parent.postMessage(Object.assign({ isStreamlitMessage: true }, message), "*");
  window.addEventListener("message", event => {
    if (!event.data || event.data.type !== "streamlit:render") return;
    const reply = (event.data.args || {}).reply;
    if (reply && pending.has(reply.id)) {
      const waiting = pending.get(reply.id);
      pending.delete(reply.id);
      reply.error ? waiting.reject(new Error(reply.error)) : waiting.resolve(reply.result);
    }
    fitHeight();
  });
  function fitHeight() {
    let height = 800;
    try { height = Math.max(560, window.parent.innerHeight - 24); } catch (error) { /* keep default */ }
    post({ type: "streamlit:setFrameHeight", height });
  }
  window.campusBridge = {
    call(payload) {
      return new Promise((resolve, reject) => {
        const id = ++counter;
        pending.set(id, { resolve, reject });
        setTimeout(() => { if (pending.delete(id)) reject(new TypeError("timeout")); }, 20000);
        post({ type: "streamlit:setComponentValue", dataType: "json", value: { id, payload } });
      });
    },
  };
  post({ type: "streamlit:componentReady", apiVersion: 1 });
  fitHeight();
  window.addEventListener("resize", fitHeight);
})();
</script>"""


@st.cache_resource
def campus_component():
    """Write the 3D page once to a temporary folder and declare it as a component."""
    folder = Path(tempfile.mkdtemp(prefix="plot_twist_3d_"))
    page = build_page(playable=True, inline=True).replace("<head>", "<head>" + BRIDGE, 1)
    (folder / "index.html").write_text(page, encoding="utf-8")
    return components.declare_component("plot_twist_campus_3d", path=str(folder))


@st.cache_resource
def command_lock():
    return threading.Lock()


def answer(payload):
    """Run one command and return {"result": ...} or {"error": ...} (never a stack trace)."""
    try:
        with command_lock():
            return {"result": command(payload)}
    except (ValueError, UnicodeDecodeError) as error:
        return {"error": str(error)}
    except Exception:
        # Do not claim the action was saved, and do not expose local file paths.
        return {"error": "Could not complete the request. Reopen your game to check progress. / "
                         "Não foi possível concluir o pedido. Reabre o jogo para confirmar o progresso."}


st.set_page_config(page_title="Plot Twist — O quinto elemento", page_icon="🕵️", layout="wide")
# The game fills the window: hide Streamlit's header, footer and padding.
st.markdown(
    "<style>header, footer, #MainMenu {display: none !important;}"
    ".block-container {padding: 0 !important; max-width: 100% !important;}"
    "iframe {border: 0 !important; display: block;}</style>",
    unsafe_allow_html=True,
)

reply = st.session_state.get("campus_reply")
value = campus_component()(reply=reply, key="campus", default=None)

# A new command from the page: answer it once, then rerun so the page receives the answer.
if isinstance(value, dict) and value.get("id") != st.session_state.get("campus_last_id"):
    st.session_state["campus_last_id"] = value.get("id")
    reply = answer(value.get("payload"))
    reply["id"] = value.get("id")
    st.session_state["campus_reply"] = reply
    st.rerun()
