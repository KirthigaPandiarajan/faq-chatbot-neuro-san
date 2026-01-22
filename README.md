# faq-chatbot-neuro-san
FAQ Chatbot that answers customer questions using a static FAQ dataset
faq-chatbot-neuro-san/
├── backend/
│   ├── app/
│   │   ├── main.py            # FastAPI entry point
│   │   ├── agent_logic.py     # Neuro-SAN network initialization
│   │   └── tools.py           # Python CodedTool to read FAQ data
│   ├── data/
│   │   └── faq.json           # Your static FAQ dataset
│   ├── config/
│   │   └── network.hocon      # Neuro-SAN Agent definitions
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── App.js             # Chat UI logic
│   │   └── ChatWindow.js      # UI Components
│   ├── package.json
│   └── Dockerfile
├── .github/workflows/main.yml # CI/CD Pipeline
├── docker-compose.yml
└── README.md
