# Up Bank MCP Server

An MCP (Model Context Protocol) server implementation for Up Bank's API, allowing AI agents to interact with Up Bank accounts.

## Features

- Account balance checking
- Transaction history viewing
- Secure API token handling
- MCP-compliant server implementation

## Requirements

- Python 3.10+
- Up Bank API token
- MCP SDK

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Unix/macOS
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file with your Up Bank API token:
   ```
   UP_TOKEN=your_token_here
   ```

## Development

Currently in initial development phase. Features being implemented:
- Basic account information retrieval
- Transaction history viewing
- MCP server implementation

## Security

- API tokens are stored in `.env` file (not committed to repository)
- Using environment variables for sensitive data
- Following Up Bank API security best practices

## License

MIT License