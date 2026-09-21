🤖 AI-Powered Customer Support Chatbot
An AI-powered customer support chatbot for a food-delivery platform. The
system combines Gemini, LangGraph, LangChain/RAG, Chroma, FastAPI,
MySQL, and Streamlit to handle both knowledge-based questions and real
operational customer-support requests.

The chatbot can understand a user's request, identify the required
capability, execute the appropriate tool or database operation, verify
the result, and return a natural-language response.

🚀 Features
The chatbot currently supports six major capabilities:

1. 📚 RAG / Knowledge Support
Answers general customer-support and FAQ questions using a knowledge
base.

Example:

"What should I do if my food is missing?"

Flow:

User Question
     ↓
Request Understanding
     ↓
RAG
     ↓
Chroma Vector Search
     ↓
Relevant Knowledge
     ↓
Gemini
     ↓
Answer
2. 📦 Order Management
Supports:

Track order

Check order status

View order details

Cancel orders when cancellation is allowed

Ownership validation

Example:

"Where is my order?"

The system verifies the order against the authenticated user's ID before
returning information.

3. 💳 Payment & Refund
Supports:

Payment status

Refund status

Refund requests

Refund validation

Duplicate refund protection

Refund processing includes business-rule validation.

For example:

Order OUT_FOR_DELIVERY
        ↓
Refund rejected

Order DELIVERED
        ↓
Refund rejected

Order CANCELLED + Payment SUCCESS
        ↓
Refund allowed
Cancellation and refund are intentionally handled as separate
operations.

4. 🍽️ Restaurant Support
Supports:

Restaurant information

Restaurant lookup by name

Available dishes

Restaurant-related questions

Example:

"Tell me about Pizza Hub."

5. 🚴 Delivery Support
Supports:

Delivery status

Delivery partner information

Delivery ETA

Example:

"Who is delivering my order?"

6. 🎫 Human Support & Ticket Management
Supports:

Create/escalate a support ticket

View a specific ticket

List user's tickets

Update ticket status

Ticket ownership validation

Supported ticket statuses:

OPEN
IN_PROGRESS
RESOLVED
CLOSED
Example:

"Mark support ticket 7 as resolved."

🧠 System Architecture
                         ┌───────────────────┐
                         │    Streamlit UI   │
                         └─────────┬─────────┘
                                   │
                              HTTP /chat
                                   │
                                   ▼
                         ┌───────────────────┐
                         │   FastAPI API     │
                         └─────────┬─────────┘
                                   │
                                   ▼
                         ┌───────────────────┐
                         │    LangGraph      │
                         │  Support Agent    │
                         └─────────┬─────────┘
                                   │
                         Understand Request
                                   │
                    ┌──────────────┼──────────────┐
                    │              │              │
                    ▼              ▼              ▼
                  RAG          Order/Payment   Restaurant
                    │              │              │
                    │              ▼              │
                    │           Delivery          │
                    │              │              │
                    │              ▼              │
                    │        Human Support        │
                    │              │              │
                    └──────────────┼──────────────┘
                                   ▼
                              Verification
                                   │
                                   ▼
                           Response Generation
                                   │
                                   ▼
                              Streamlit UI
🔄 LangGraph Workflow
The main agent follows this workflow:

START
  ↓
Understand Request
  ↓
Select Capability
  ├── RAG
  ├── Order
  ├── Payment
  ├── Restaurant
  ├── Delivery
  └── Human Support
  ↓
Execute Tool / Operation
  ↓
Verify Result
  ↓
Generate Response
  ↓
END
This architecture keeps request understanding, business operations,
verification, and response generation separated.

🛠️ Technology Stack
Component Technology

Programming Language Python
API Framework FastAPI
Agent Framework LangGraph
LLM Google Gemini
RAG Framework LangChain
Vector Database Chroma
Embeddings Hugging Face
Database MySQL
Frontend Streamlit
API Communication REST / HTTP
Development Environment VS Code
Version Control Git

📁 Project Structure
AI Customer Support AI Agent/
│
├── backend/
│   │
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── seed_data.py
│   ├── seed_orders.py
│   │
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── state.py
│   │   ├── nodes.py
│   │   └── graph.py
│   │
│   ├── services/
│   │   ├── order_service.py
│   │   ├── payment_service.py
│   │   ├── refund_service.py
│   │   ├── restaurant_service.py
│   │   ├── delivery_service.py
│   │   └── support_service.py
│   │
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── order_tools.py
│   │   ├── payment_tools.py
│   │   ├── refund_tools.py
│   │   ├── restaurant_tools.py
│   │   ├── delivery_tools.py
│   │   └── support_tools.py
│   │
│   ├── rag/
│   │   ├── ...
│   │   ├── llm.py
│   │   └── rag_chain.py
│   │
│   └── test_*.py
│
├── frontend/
│   └── app.py
│
└── README.md
🔐 Security & Validation
The backend includes ownership checks for sensitive operations.

For example:

User 4 → Order 2
User 5 → Order 3
User 6 → Order 4
If User 4 requests Order 3:

User 4
  ↓
Request Order 3
  ↓
Database ownership check
  ↓
Order belongs to User 5
  ↓
Access denied / Order not found
Similar ownership validation is applied to:

Orders

Payments

Support tickets

The system therefore does not simply trust an order ID or ticket ID
supplied by the user.

🧾 Business Rules
Order Cancellation
Orders can be cancelled only when their current status permits
cancellation.

Cancellation is rejected for:

OUT_FOR_DELIVERY
DELIVERED
CANCELLED
Refund
A refund requires:

Order status = CANCELLED
Payment status = SUCCESS
A payment that is already:

REFUNDED
is not refunded again.

Support Tickets
Allowed statuses:

OPEN
IN_PROGRESS
RESOLVED
CLOSED
Invalid statuses are rejected by the backend.

🧪 Testing
The backend was tested at multiple levels.

Capability Testing
All six capabilities were tested end-to-end:

✅ RAG
✅ Order
✅ Payment / Refund
✅ Restaurant
✅ Delivery
✅ Human Support
Security Testing
Cross-user access was tested for:

✅ Orders
✅ Payments
✅ Support Tickets
Edge-Case Testing
The following scenarios were tested:

✅ Cancel OUT_FOR_DELIVERY order
✅ Cancel DELIVERED order
✅ Cancel already-cancelled order
✅ Refund OUT_FOR_DELIVERY order
✅ Refund DELIVERED order
✅ Already-refunded payment
✅ Invalid ticket status
✅ Nonexistent ticket
Final Health Check
Final backend health testing covered one successful operation from each
capability:

RAG             ✅
Order           ✅
Payment         ✅
Restaurant      ✅
Delivery        ✅
Human Support  ✅

Result: 6/6 PASS
⚙️ Setup
1. Clone the project
git clone <your-repository-url>
cd "AI Customer Support AI Agent"
2. Create and activate a virtual environment
python -m venv venv
macOS/Linux:

source venv/bin/activate
Windows:

venv\Scripts\activate
3. Install dependencies
pip install -r requirements.txt
If requirements.txt has not yet been generated:

pip freeze > requirements.txt
🗄️ Database Configuration
Create a MySQL database for the application.

The project uses MySQL for operational data such as:

Users
Orders
Order Items
Payments
Restaurants
Dishes
Support Tickets
Conversations
Messages
Configure the database connection through the project's
configuration/environment variables.

Do not commit passwords, API keys, or other secrets to Git.

🔑 Environment Variables
Create a .env file for local development.

Example:

GEMINI_API_KEY=your_gemini_api_key

DB_HOST=localhost
DB_PORT=3306
DB_USER=your_mysql_user
DB_PASSWORD=your_mysql_password
DB_NAME=food_delivery
If your RAG/embedding setup requires additional credentials, configure
them through environment variables as appropriate.

Add .env to .gitignore:

.env
venv/
__pycache__/
*.pyc
▶️ Running the Backend
From the project root:

cd backend
Activate the virtual environment if necessary:

source ../venv/bin/activate
Start FastAPI:

uvicorn main:app --reload
The API will be available at:

http://127.0.0.1:8000
FastAPI documentation:

http://127.0.0.1:8000/docs
🖥️ Running the Streamlit Frontend
Open another terminal.

From the project root:

source venv/bin/activate
Then:

streamlit run frontend/app.py
The Streamlit application will normally be available at:

http://localhost:8501
The frontend communicates with:

POST /chat
on the FastAPI backend.

💬 Example Requests
Order
Where is my order?
Payment
What is the payment status of order 2?
Restaurant
Tell me about Pizza Hub.
Delivery
When will my delivery arrive?
Support
I need human help with my order.
Ticket
What is the status of support ticket 7?
Ticket Update
Mark support ticket 7 as resolved.
🔌 API Example
Request
POST /chat
Content-Type: application/json
{
  "question": "Where is my order?",
  "user_id": 4
}
Response
{
  "question": "Where is my order?",
  "user_id": 4,
  "capability": "order",
  "intent": "track_order",
  "order_id": 2,
  "restaurant_name": "Spice Garden",
  "payment_id": null,
  "ticket_id": null,
  "new_status": null,
  "answer": "Your order is currently out for delivery.",
  "verification": "Order information successfully verified."
}
🎯 Design Principles
The project follows several important principles:

Separation of Responsibilities
LLM
 ↓
Understand the request

Tools
 ↓
Perform operations

Services
 ↓
Contain business/database logic

Verification
 ↓
Validate operation results

Response Generation
 ↓
Communicate result to user
User Ownership
Sensitive resources are always checked against the requesting user's ID.

Verification Before Response
The agent does not blindly trust tool execution. Results are verified
before the final response is produced.

Business Rules in Backend
Critical operations such as cancellation, refunds, and ticket status
changes are validated in backend services rather than relying only on
the LLM.

🚧 Future Improvements
Possible future improvements include:

Authentication and JWT-based sessions

Persistent conversation history

Streaming AI responses

Faster response generation

Better LLM fallback/retry handling

Structured order/payment/ticket UI cards

Real-time delivery tracking

Admin/support-agent dashboard

Human-agent handoff

Observability and logging

Automated unit and integration tests

Docker deployment

Cloud deployment

Production database and secrets management

📌 Project Status
Backend Architecture        ✅ Complete
RAG                          ✅ Complete
Order Capability             ✅ Complete
Payment Capability           ✅ Complete
Refund Capability            ✅ Complete
Restaurant Capability        ✅ Complete
Delivery Capability          ✅ Complete
Human Support                ✅ Complete
Ticket Lifecycle             ✅ Complete
Security Testing             ✅ Complete
Edge-Case Testing            ✅ Complete
Comprehensive Testing        ✅ Complete
Streamlit Frontend           ✅ Complete
The current application provides a working end-to-end AI
customer-support system with six operational capabilities and a
Streamlit interface for interacting with the backend.


⭐ Project Summary
This project demonstrates how an AI customer-support system can combine
LLMs, RAG, LangGraph, tool calling, FastAPI, MySQL, and vector
search to handle both conversational questions and real backend
operations.

Instead of being only a chatbot, the system is designed as an AI agent
capable of understanding requests, selecting capabilities, executing
tools, validating results, and responding to users.
