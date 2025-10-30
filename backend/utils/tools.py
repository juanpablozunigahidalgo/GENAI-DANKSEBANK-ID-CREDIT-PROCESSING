from langchain.tools import Tool

# Simulated tool to fetch ID-verified user info
def fetch_user_info():
    return "User: John Doe, CPR: 123456-7890, verified for Denmark."

get_user_data_tool = Tool(
    name="GetVerifiedUser",
    func=fetch_user_info,
    description="Use this only AFTER the user has uploaded their ID to retrieve their verified data"
)
