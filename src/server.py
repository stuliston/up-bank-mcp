from mcp.server.fastmcp import FastMCP
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize MCP server
mcp = FastMCP("Up Bank")

# Up Bank API configuration
UP_API_BASE = "https://api.up.com.au/api/v1"
UP_TOKEN = os.getenv("UP_TOKEN")

class UpBankAPI:
    def __init__(self, token):
        self.token = token
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }
    
    def get_accounts(self):
        response = requests.get(f"{UP_API_BASE}/accounts", headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def get_transactions(self, account_id, page_size=10):
        response = requests.get(
            f"{UP_API_BASE}/accounts/{account_id}/transactions",
            headers=self.headers,
            params={"page[size]": page_size}
        )
        response.raise_for_status()
        return response.json()

# Initialize API client
up_client = UpBankAPI(UP_TOKEN)

@mcp.tool()
def list_accounts() -> str:
    """List all Up Bank accounts and their balances."""
    try:
        accounts = up_client.get_accounts()
        result = []
        for account in accounts["data"]:
            balance = account["attributes"]["balance"]["value"]
            currency = account["attributes"]["balance"]["currencyCode"]
            name = account["attributes"]["displayName"]
            result.append(f"{name}: {balance} {currency}")
        return "\n".join(result)
    except Exception as e:
        return f"Error fetching accounts: {str(e)}"

@mcp.tool()
def recent_transactions(account_name: str) -> str:
    """Get recent transactions for a specific account."""
    try:
        # First get all accounts to find the matching one
        accounts = up_client.get_accounts()
        account_id = None
        
        for account in accounts["data"]:
            if account["attributes"]["displayName"].lower() == account_name.lower():
                account_id = account["id"]
                break
        
        if not account_id:
            return f"Account '{account_name}' not found"
        
        transactions = up_client.get_transactions(account_id)
        result = []
        for tx in transactions["data"]:
            amount = tx["attributes"]["amount"]["value"]
            description = tx["attributes"]["description"]
            status = tx["attributes"]["status"]
            result.append(f"{description}: {amount} ({status})")
        
        return "\n".join(result)
    except Exception as e:
        return f"Error fetching transactions: {str(e)}"

if __name__ == "__main__":
    if not UP_TOKEN:
        print("Error: UP_TOKEN environment variable not set")
        exit(1)
    mcp.run()