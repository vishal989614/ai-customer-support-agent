import os
import sys
import time
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests
import streamlit as st
from dotenv import load_dotenv
import mysql.connector

# Load environment variables
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

# Ensure backend directory is in python path for fallback/embedded execution
backend_path = BASE_DIR / "backend"
if str(backend_path) not in sys.path:
    sys.path.append(str(backend_path))

# ============================================================
# Streamlit Page Configuration
# ============================================================

st.set_page_config(
    page_title="QuickBite AI | Customer Support",
    page_icon="🍔",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# Configuration & Constants
# ============================================================

DB_CONFIG = {
    "host": os.getenv("MYSQL_HOST") or os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("MYSQL_PORT") or os.getenv("DB_PORT", "3306")),
    "user": os.getenv("MYSQL_USER") or os.getenv("DB_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD") or os.getenv("DB_PASSWORD", "root"),
    "database": os.getenv("MYSQL_DATABASE") or os.getenv("DB_NAME", "food_delivery"),
}

API_URL = os.getenv("CHATBOT_API_URL", "http://127.0.0.1:8000/chat")
HEALTH_URL = os.getenv("CHATBOT_HEALTH_URL", "http://127.0.0.1:8000/")
REQUEST_TIMEOUT = int(os.getenv("CHATBOT_TIMEOUT", "45"))

# ============================================================
# Embedded Agent Loader (Fallback if FastAPI server is offline)
# ============================================================

@st.cache_resource(show_spinner="Initializing AI Agent Engine...")
def get_embedded_agent():
    try:
        from agents.graph import build_support_graph
        agent = build_support_graph()
        return agent
    except Exception:
        return None

# ============================================================
# Modern Styling & Refined Aesthetics
# ============================================================

st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        /* Top Header Banner */
        .qb-header {
            background: linear-gradient(135deg, #1A1A24 0%, #262638 100%);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            padding: 1.1rem 1.6rem;
            color: white;
            box-shadow: 0 8px 24px -4px rgba(0, 0, 0, 0.25);
            margin-bottom: 1.2rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .qb-header-title {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .qb-header-title h2 {
            margin: 0;
            font-size: 1.45rem;
            font-weight: 800;
            letter-spacing: -0.02em;
            background: linear-gradient(135deg, #FF6B4A 0%, #FF881B 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .qb-header-subtitle {
            margin: 0;
            font-size: 0.85rem;
            color: #9CA3AF;
        }

        .qb-status-pill {
            background: rgba(16, 185, 129, 0.12);
            color: #34D399;
            border: 1px solid rgba(16, 185, 129, 0.3);
            padding: 0.35rem 0.8rem;
            border-radius: 999px;
            font-size: 0.78rem;
            font-weight: 600;
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }

        .qb-status-dot {
            width: 7px;
            height: 7px;
            background-color: #34D399;
            border-radius: 50%;
            box-shadow: 0 0 8px #34D399;
        }

        /* Sidebar Profile Card */
        .qb-profile-box {
            background: rgba(128, 128, 128, 0.06);
            border: 1px solid rgba(128, 128, 128, 0.15);
            border-radius: 12px;
            padding: 0.85rem 1rem;
            margin-top: 0.5rem;
        }

        /* Live Context Cards */
        .qb-card {
            background: rgba(128, 128, 128, 0.05);
            border: 1px solid rgba(128, 128, 128, 0.18);
            border-radius: 14px;
            padding: 1.1rem 1.25rem;
            margin-bottom: 1rem;
            transition: border-color 0.2s ease, transform 0.2s ease;
        }

        .qb-card:hover {
            border-color: #FF5E36;
        }

        .qb-card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0.75rem;
        }

        .qb-card-title {
            font-size: 0.92rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            color: #9CA3AF;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        /* Badges */
        .badge {
            display: inline-block;
            padding: 0.22rem 0.6rem;
            border-radius: 999px;
            font-size: 0.72rem;
            font-weight: 700;
            letter-spacing: 0.02em;
        }
        .badge-green { background: #D1FAE5; color: #065F46; }
        .badge-amber { background: #FEF3C7; color: #92400E; }
        .badge-red { background: #FEE2E2; color: #991B1B; }
        .badge-blue { background: #DBEAFE; color: #1E40AF; }
        .badge-purple { background: #EDE9FE; color: #5B21B6; }

        /* Progress Stepper */
        .stepper-mini {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin: 0.85rem 0 0.4rem 0;
            position: relative;
        }

        .stepper-step {
            display: flex;
            flex-direction: column;
            align-items: center;
            font-size: 0.68rem;
            font-weight: 600;
            color: #888;
        }

        .stepper-dot {
            width: 18px;
            height: 18px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.6rem;
            margin-bottom: 4px;
        }

        .step-done {
            background: #10B981;
            color: white;
        }

        .step-curr {
            background: #FF5E36;
            color: white;
            box-shadow: 0 0 8px rgba(255, 94, 54, 0.6);
        }

        .step-wait {
            background: rgba(128, 128, 128, 0.2);
            color: #777;
        }

        .stepper-bar {
            flex-grow: 1;
            height: 2px;
            background: rgba(128, 128, 128, 0.2);
            margin: 0 4px;
            margin-bottom: 14px;
        }

        .stepper-bar.active {
            background: #10B981;
        }

        /* Telemetry Inspector */
        .telemetry-pill {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            font-size: 0.72rem;
            color: #9CA3AF;
            background: rgba(128, 128, 128, 0.08);
            border-radius: 6px;
            padding: 3px 8px;
            margin-top: 6px;
        }

        /* Suggestion Action Pills */
        .chip-btn {
            background: rgba(128, 128, 128, 0.08);
            border: 1px solid rgba(128, 128, 128, 0.2);
            border-radius: 999px;
            padding: 0.4rem 0.85rem;
            font-size: 0.8rem;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.15s ease;
        }
        .chip-btn:hover {
            border-color: #FF5E36;
            background: rgba(255, 94, 54, 0.1);
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# Database Engine & Optimized Data Handlers
# ============================================================

@st.cache_resource
def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

def run_query(query: str, params: tuple = (), fetch: bool = True):
    conn = get_db_connection()
    if not conn.is_connected():
        conn.reconnect(attempts=3, delay=1)
    
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(query, params)
        if fetch:
            return cursor.fetchall()
        conn.commit()
        return []
    finally:
        cursor.close()

def run_query_one(query: str, params: tuple = ()):
    rows = run_query(query, params, fetch=True)
    return rows[0] if rows else None

@st.cache_data(ttl=20)
def get_all_users():
    return run_query("SELECT id, name, email, phone FROM users ORDER BY id ASC")

@st.cache_data(ttl=5)
def get_user_active_order(user_id: int):
    """Retrieves the customer's active order or latest order for context panel."""
    # First priority: In-transit / active order
    active = run_query_one(
        """
        SELECT 
            o.id AS order_id,
            o.status AS order_status,
            o.total_amount,
            o.delivery_address,
            o.created_at,
            r.name AS restaurant_name,
            r.cuisine,
            d.status AS delivery_status,
            d.delivery_partner_name,
            d.delivery_partner_phone,
            d.estimated_delivery_time,
            p.status AS payment_status,
            p.payment_method
        FROM orders o
        JOIN restaurants r ON r.id = o.restaurant_id
        LEFT JOIN deliveries d ON d.order_id = o.id
        LEFT JOIN payments p ON p.order_id = o.id
        WHERE o.user_id = %s AND o.status NOT IN ('DELIVERED', 'CANCELLED')
        ORDER BY o.created_at DESC
        LIMIT 1
        """,
        (user_id,)
    )
    if active:
        active["is_active"] = True
        return active

    # Fallback to most recent order
    latest = run_query_one(
        """
        SELECT 
            o.id AS order_id,
            o.status AS order_status,
            o.total_amount,
            o.delivery_address,
            o.created_at,
            r.name AS restaurant_name,
            r.cuisine,
            d.status AS delivery_status,
            d.delivery_partner_name,
            d.delivery_partner_phone,
            d.estimated_delivery_time,
            p.status AS payment_status,
            p.payment_method
        FROM orders o
        JOIN restaurants r ON r.id = o.restaurant_id
        LEFT JOIN deliveries d ON d.order_id = o.id
        LEFT JOIN payments p ON p.order_id = o.id
        WHERE o.user_id = %s
        ORDER BY o.created_at DESC
        LIMIT 1
        """,
        (user_id,)
    )
    if latest:
        latest["is_active"] = False
        return latest
    return None

@st.cache_data(ttl=5)
def get_user_recent_ticket(user_id: int):
    """Retrieves the customer's latest open or active support ticket."""
    return run_query_one(
        """
        SELECT id, order_id, issue_type, priority, status, description, created_at
        FROM support_tickets
        WHERE user_id = %s
        ORDER BY (status = 'OPEN' OR status = 'IN_PROGRESS') DESC, created_at DESC
        LIMIT 1
        """,
        (user_id,)
    )

# ============================================================
# AI Support Agent Invocation
# ============================================================

def check_backend_api_health() -> bool:
    try:
        resp = requests.get(HEALTH_URL, timeout=1.2)
        return resp.status_code == 200
    except Exception:
        return False

def invoke_support_agent(
    question: str, 
    user_id: int,
    context: Optional[List[str]] = None,
    order_id: Optional[int] = None,
    ticket_id: Optional[int] = None
) -> Dict[str, Any]:
    start_time = time.time()

    payload: Dict[str, Any] = {"question": question, "user_id": user_id}
    if context:
        payload["context"] = context
    if order_id:
        payload["order_id"] = order_id
    if ticket_id:
        payload["ticket_id"] = ticket_id

    # 1. Attempt FastAPI REST call
    try:
        response = requests.post(
            API_URL,
            json=payload,
            timeout=REQUEST_TIMEOUT,
        )
        if response.status_code == 200:
            data = response.json()
            elapsed = time.time() - start_time
            data["latency_sec"] = round(elapsed, 2)
            data["engine"] = "FastAPI Backend"
            return data
    except Exception:
        pass

    # 2. Embedded Engine Fallback
    agent = get_embedded_agent()
    if agent is not None:
        try:
            result = agent.invoke(payload)
            elapsed = time.time() - start_time
            return {
                "question": question,
                "user_id": user_id,
                "capability": result.get("capability"),
                "intent": result.get("intent"),
                "order_id": result.get("order_id"),
                "restaurant_name": result.get("restaurant_name"),
                "payment_id": result.get("payment_id"),
                "ticket_id": result.get("ticket_id"),
                "new_status": result.get("new_status"),
                "answer": result.get("answer") or "I processed your request, but no response was generated.",
                "verification": result.get("verification_result"),
                "latency_sec": round(elapsed, 2),
                "engine": "Embedded LangGraph Agent",
            }
        except Exception as exc:
            return {
                "answer": f"Agent execution error: {str(exc)}",
                "capability": "error",
                "intent": "exception",
                "verification": "FAILED",
                "latency_sec": round(time.time() - start_time, 2),
                "engine": "Embedded Agent (Error)",
            }

    return {
        "answer": "The AI Support Service is currently unreachable. Please ensure the backend server or environment is configured.",
        "capability": "offline",
        "intent": "none",
        "verification": "FAILED",
        "latency_sec": round(time.time() - start_time, 2),
        "engine": "Offline",
    }

# ============================================================
# Formatters & UI Helpers
# ============================================================

def fmt_inr(amount: Any) -> str:
    if amount is None:
        return "₹0.00"
    return f"₹{float(amount):,.2f}"

def render_status_badge(status: str) -> str:
    s = (status or "").upper()
    if s in ("DELIVERED", "RESOLVED", "SUCCESS", "COMPLETED"):
        return f'<span class="badge badge-green">✓ {s.replace("_", " ")}</span>'
    elif s in ("OUT_FOR_DELIVERY", "ON_THE_WAY", "ARRIVED", "IN_PROGRESS", "PREPARING", "READY"):
        return f'<span class="badge badge-amber">● {s.replace("_", " ")}</span>'
    elif s in ("CANCELLED", "FAILED", "CRITICAL"):
        return f'<span class="badge badge-red">✕ {s.replace("_", " ")}</span>'
    elif s in ("PLACED", "CONFIRMED", "ASSIGNED", "OPEN"):
        return f'<span class="badge badge-blue">● {s.replace("_", " ")}</span>'
    elif s in ("REFUNDED", "ESCALATED"):
        return f'<span class="badge badge-purple">★ {s.replace("_", " ")}</span>'
    return f'<span class="badge badge-blue">{s.replace("_", " ")}</span>'

def render_mini_stepper(current_status: str):
    stages = [
        ("PLACED", "Placed"),
        ("CONFIRMED", "Confirmed"),
        ("PREPARING", "Cooking"),
        ("OUT_FOR_DELIVERY", "On The Way"),
        ("DELIVERED", "Delivered")
    ]
    if current_status == "CANCELLED":
        st.markdown('<span style="color:#EF4444; font-size:0.8rem; font-weight:600;">🚫 Order Cancelled</span>', unsafe_allow_html=True)
        return

    stage_order = {s[0]: i for i, s in enumerate(stages)}
    curr_idx = stage_order.get(current_status, 1)

    steps_html = '<div class="stepper-mini">'
    for i, (code, label) in enumerate(stages):
        if i < curr_idx:
            cls = "step-done"
            dot = "✓"
        elif i == curr_idx:
            cls = "step-curr"
            dot = "●"
        else:
            cls = "step-wait"
            dot = str(i + 1)
        
        steps_html += f'<div class="stepper-step"><div class="stepper-dot {cls}">{dot}</div><div>{label}</div></div>'
        if i < len(stages) - 1:
            line_active = "active" if i < curr_idx else ""
            steps_html += f'<div class="stepper-bar {line_active}"></div>'
    steps_html += '</div>'
    st.markdown(steps_html, unsafe_allow_html=True)

# ============================================================
# Session State Initialization
# ============================================================

if "user_id" not in st.session_state:
    st.session_state.user_id = 1

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_prefill" not in st.session_state:
    st.session_state.chat_prefill = ""

# ============================================================
# Sidebar: Clean Customer Switcher & Diagnostics
# ============================================================

all_users = get_all_users()
current_user = next((u for u in all_users if u["id"] == st.session_state.user_id), all_users[0])

with st.sidebar:
    st.markdown("### 🍔 QuickBite Support")
    st.caption("AI Customer Support Assistant")

    # Customer Persona Switcher
    user_options = {u["id"]: f"👤 {u['name']} (#{u['id']})" for u in all_users}
    selected_uid = st.selectbox(
        "Active Customer Profile",
        options=list(user_options.keys()),
        format_func=lambda uid: user_options[uid],
        index=list(user_options.keys()).index(st.session_state.user_id) if st.session_state.user_id in user_options else 0,
        help="Switch user to evaluate multi-user order tracking, payment refunds, and data isolation."
    )

    if selected_uid != st.session_state.user_id:
        st.session_state.user_id = selected_uid
        st.session_state.messages = []
        st.session_state.chat_prefill = ""
        st.rerun()

    # Compact User Card
    st.markdown(
        f"""
        <div class="qb-profile-box">
            <div style="font-weight: 700; font-size: 0.95rem;">{current_user['name']}</div>
            <div style="font-size: 0.78rem; color: #888;">✉️ {current_user['email']}</div>
            <div style="font-size: 0.78rem; color: #888;">📞 +91 {current_user['phone']}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")
    
    # System Status
    api_online = check_backend_api_health()
    if api_online:
        st.markdown('<span style="color:#10B981; font-size:0.8rem; font-weight:600;">🟢 Backend API Online (Port 8000)</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span style="color:#F59E0B; font-size:0.8rem; font-weight:600;">🟡 Embedded Agent (Local Direct)</span>', unsafe_allow_html=True)

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    if st.button("🧹 Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.session_state.chat_prefill = ""
        st.rerun()

# ============================================================
# Main Page Header
# ============================================================

st.markdown(
    f"""
    <div class="qb-header">
        <div class="qb-header-title">
            <span style="font-size: 1.8rem;">🍔</span>
            <div>
                <h2>QuickBite AI Customer Support</h2>
                <p class="qb-header-subtitle">Real-time order assistance, delivery tracking, payment refunds, and issue resolution.</p>
            </div>
        </div>
        <div>
            <span class="qb-status-pill">
                <span class="qb-status-dot"></span>
                AI Agent Active
            </span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Fetch customer context for side panel
active_order = get_user_active_order(st.session_state.user_id)
recent_ticket = get_user_recent_ticket(st.session_state.user_id)

# ============================================================
# 2-Column Responsive Layout: Chat (Left) + Context (Right)
# ============================================================

chat_col, context_col = st.columns([2.3, 1], gap="medium")

# ------------------------------------------------------------
# RIGHT COLUMN: Live Order & Support Context Panel
# ------------------------------------------------------------

with context_col:
    # 1. Current / Active Order Card
    st.markdown(
        """
        <div class="qb-card-title">📦 Current Order Status</div>
        """,
        unsafe_allow_html=True
    )

    if active_order:
        oid = active_order["order_id"]
        ostatus = active_order["order_status"]
        rest_name = active_order["restaurant_name"]
        amount = fmt_inr(active_order["total_amount"])
        
        with st.container():
            st.markdown(
                f"""
                <div class="qb-card">
                    <div class="qb-card-header">
                        <span style="font-weight:700; font-size:1.05rem;">Order #{oid}</span>
                        <span>{render_status_badge(ostatus)}</span>
                    </div>
                    <div style="font-size:0.85rem; margin-bottom: 4px;">
                        <b>Restaurant:</b> {rest_name} <span style="color:#888;">({active_order['cuisine']})</span>
                    </div>
                    <div style="font-size:0.85rem; margin-bottom: 6px;">
                        <b>Total Bill:</b> <span style="font-weight:700; color:#FF5E36;">{amount}</span>
                    </div>
                    <div style="font-size:0.8rem; color:#888; margin-bottom: 8px;">
                        📍 {active_order['delivery_address']}
                    </div>
                """,
                unsafe_allow_html=True
            )
            
            # Mini Stepper
            render_mini_stepper(ostatus)

            # Delivery courier if on the way
            if active_order.get("delivery_partner_name") and ostatus in ("OUT_FOR_DELIVERY", "PREPARING"):
                st.markdown(
                    f"""
                    <div style="font-size:0.78rem; background:rgba(128,128,128,0.08); padding:6px 10px; border-radius:6px; margin-top:8px;">
                        🚴 <b>Courier:</b> {active_order['delivery_partner_name']} (+91 {active_order['delivery_partner_phone'] or '—'})
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown(
            """
            <div class="qb-card" style="text-align: center; color: #888; font-size: 0.85rem; padding: 1.5rem;">
                No active orders for this account.
            </div>
            """,
            unsafe_allow_html=True
        )

    # 2. Active Support Ticket Card (if exists)
    st.markdown(
        """
        <div class="qb-card-title" style="margin-top: 1.2rem;">🎫 Support Ticket</div>
        """,
        unsafe_allow_html=True
    )

    if recent_ticket:
        tid = recent_ticket["id"]
        tstatus = recent_ticket["status"]
        tpriority = recent_ticket["priority"]
        tissue = recent_ticket["issue_type"]
        tdesc = recent_ticket["description"]

        st.markdown(
            f"""
            <div class="qb-card">
                <div class="qb-card-header">
                    <span style="font-weight:700; font-size:0.95rem;">Ticket #{tid}</span>
                    <span>{render_status_badge(tstatus)}</span>
                </div>
                <div style="font-size:0.82rem; margin-bottom: 4px;">
                    <b>Issue:</b> {tissue or 'General Support'} &nbsp;|&nbsp; <b>Priority:</b> `{tpriority}`
                </div>
                <div style="font-size:0.78rem; color:#888; font-style:italic; margin-top:6px; line-height:1.3;">
                    "{tdesc[:90] + '...' if len(tdesc) > 90 else tdesc}"
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            """
            <div class="qb-card" style="text-align: center; color: #888; font-size: 0.85rem; padding: 1.2rem;">
                No open support tickets.
            </div>
            """,
            unsafe_allow_html=True
        )

    # 3. Quick Assistance Actions
    st.markdown(
        """
        <div class="qb-card-title" style="margin-top: 1.2rem;">⚡ Quick Actions</div>
        """,
        unsafe_allow_html=True
    )

    qa1, qa2 = st.columns(2)
    with qa1:
        if st.button("🚴 Track Order", use_container_width=True):
            st.session_state.chat_prefill = "Where is my order?"
            st.rerun()
    with qa2:
        if st.button("💳 Payment Info", use_container_width=True):
            st.session_state.chat_prefill = "What's the payment status?"
            st.rerun()

    qa3, qa4 = st.columns(2)
    with qa3:
        if st.button("⚠️ Missing Food", use_container_width=True):
            st.session_state.chat_prefill = "My food is missing."
            st.rerun()
    with qa4:
        if st.button("👤 Human Help", use_container_width=True):
            st.session_state.chat_prefill = "I want human help."
            st.rerun()


# ------------------------------------------------------------
# LEFT COLUMN: Core AI Chatbot Experience
# ------------------------------------------------------------

with chat_col:
    # Initial Welcome message
    if not st.session_state.messages:
        fname = current_user['name'].split()[0]
        st.session_state.messages.append({
            "role": "assistant",
            "content": f"Hello {fname}! 👋 How can I help you today? I can track your orders, check payment status, investigate missing food items, or connect you to human support.",
            "metadata": None
        })

    # Render Conversation History
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            
            meta = msg.get("metadata")
            if meta:
                cap = (meta.get("capability") or "agent").upper()
                latency = meta.get("latency_sec", 0)
                verif = meta.get("verification") or "PASSED"
                
                # Subtle reasoning pill
                st.markdown(
                    f"""
                    <div class="telemetry-pill">
                        ⚡ <b>{cap}</b> &nbsp;•&nbsp; {latency}s &nbsp;•&nbsp; Verification: <b>{verif}</b>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    # Interactive Prompt Chips
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    st.caption("Suggested Questions:")
    chip_c1, chip_c2, chip_c3, chip_c4 = st.columns(4)
    
    with chip_c1:
        if st.button("🚴 Where is my order?", key="chip_order", use_container_width=True):
            st.session_state.chat_prefill = "Where is my order?"
            st.rerun()
    with chip_c2:
        if st.button("🍽️ What restaurant is it from?", key="chip_rest", use_container_width=True):
            st.session_state.chat_prefill = "What restaurant is it from?"
            st.rerun()
    with chip_c3:
        if st.button("💳 Payment status?", key="chip_pay", use_container_width=True):
            st.session_state.chat_prefill = "What's the payment status?"
            st.rerun()
    with chip_c4:
        if st.button("🎫 Status of my ticket?", key="chip_ticket", use_container_width=True):
            st.session_state.chat_prefill = "What is the status of my support ticket?"
            st.rerun()

    # Chat Input Handling
    user_input = st.chat_input("Type your question or issue here...")
    
    active_prompt = None
    if st.session_state.chat_prefill:
        active_prompt = st.session_state.chat_prefill
        st.session_state.chat_prefill = ""
    elif user_input:
        active_prompt = user_input

    if active_prompt:
        # Append User Message
        st.session_state.messages.append({"role": "user", "content": active_prompt})
        with st.chat_message("user"):
            st.markdown(active_prompt)

        # AI Assistant Response
        with st.chat_message("assistant"):
            with st.spinner("QuickBite AI is reviewing database & policies..."):
                # Extract conversational context and recent entities from history
                conv_context = []
                recent_order_id = active_order["order_id"] if active_order else None
                recent_ticket_id = recent_ticket["id"] if recent_ticket else None
                
                for m in st.session_state.messages[:-1][-6:]:
                    r = m.get("role", "user").capitalize()
                    c = m.get("content", "")
                    conv_context.append(f"{r}: {c}")
                    m_meta = m.get("metadata")
                    if m_meta:
                        if m_meta.get("order_id"):
                            recent_order_id = m_meta.get("order_id")
                        if m_meta.get("ticket_id"):
                            recent_ticket_id = m_meta.get("ticket_id")

                agent_res = invoke_support_agent(
                    active_prompt, 
                    st.session_state.user_id,
                    context=conv_context,
                    order_id=recent_order_id,
                    ticket_id=recent_ticket_id
                )
                answer_text = agent_res.get("answer", "I received a blank answer from the agent.")
                st.markdown(answer_text)

                cap = (agent_res.get("capability") or "agent").upper()
                latency = agent_res.get("latency_sec", 0)
                verif = agent_res.get("verification") or "PASSED"
                st.markdown(
                    f"""
                    <div class="telemetry-pill">
                        ⚡ <b>{cap}</b> &nbsp;•&nbsp; {latency}s &nbsp;•&nbsp; Verification: <b>{verif}</b>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer_text,
                    "metadata": agent_res
                })
                # Refresh so context panel updates immediately if ticket/order changed
                st.cache_data.clear()
                st.rerun()
