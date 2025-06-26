├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── README.md                # Comprehensive documentation
├── env_example.txt          # Environment setup guide
├── ai_providers/           # AI service integrations
│   ├── gemini_provider.py     # Google Gemini (Primary)
│   ├── openai_provider.py     # OpenAI (Backup)
│   ├── claude_provider.py     # Claude (Alternative)
│   ├── ai_manager.py          # Provider management
│   └── base_provider.py       # Base provider interface
├── utils/                   # Helper functions
│   ├── job_analyzer.py        # Job description analysis
│   ├── resume_generator.py    # Resume customization
│   └── cover_letter_generator.py # Cover letter customization
└── data/                    # User profile management
    └── profile_manager.py     # Profile data handling
