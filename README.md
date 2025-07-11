# TicTacToe-RL
Side project implementing basic temporal difference learning RL algorithm to teach an agent to play tic-tac-toe. (From Sutton, 2014, 2015)

TicTacToe-RL/                    # Root of your Git repo
├── src/                         # Source code lives here
│   └── tictactoe_rl/            # Top-level package (no hyphen!)
│       ├── __init__.py          # Package initializer
│
│       ├── rl_init/             # RL agent initialization logic
│       │   ├── __init__.py
│       │   └── builder.py       # Functions for creating agents
│
│       ├── manual_training/     # Human-vs-AI interface
│       │   ├── __init__.py
│       │   └── game_loop.py     # Game logic for manual play
│
│       ├── auto_training/       # Self-play or automated training
│       │   ├── __init__.py
│       │   └── trainer.py       # Training loop, matchmaking
│
│       └── utils/               # Shared tools, game state, etc.
│           ├── __init__.py
│           └── board.py         # Board representation and logic
│
├── scripts/                     # CLI utilities or entry points
│   ├── run_manual.py            # Launch human-vs-agent match
│   ├── run_auto.py              # Launch self-play training
│   └── init_agent.py            # Agent setup or evaluation
│
├── tests/                       # Unit tests
│   ├── test_rl_init/
│   ├── test_manual_training/
│   └── test_auto_training/
│
├── pyproject.toml               # Modern build + dependency config
├── requirements.txt             # Optional: quick pip install
├── .gitignore                   # Files to exclude from git
├── README.md                    # Project overview & usage
└── LICENSE                      # Licensing info (e.g. MIT)
