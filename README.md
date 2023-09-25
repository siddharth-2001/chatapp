# chatapp

## Endpoints

# User
- /api/online-users/ (GET)
  Get a list of all the online uses.
- /api/register/ (POST)
  ~ Post these value
  ~ name, phone, password (All of them are strings)
- /api/login/ (POST)
  ~ Post "username" and "password", username is the phone you registered with.
  ~ Output: json data with the user token. Put this token in the Headers like
  ~ Authorization: Token {token} for all subsequent requests
- /api/logout/ (POST)
  ~ Logs user out and sets them to offline status. Only need auth token in headers.

  # Chat
  - api/chat/start/ (POST)
    ~ Post "recipient" and make sure you have added your auth token in the headers.
    ~ Output: chat room name will be returned on successful request we can now use this to chat with the other user.
  - api/chat/lobby/{chat-room-name}/{token}/ (WEBSOCKET)
    ~ Opens a simple html page to start chat. Only the allowed users in the specific chat room can join. You need to create a chat with an online user to access this page.

  - api/chat/send/ (POST)
    Post "message" and "recipient", the recipient is the phone number of the recipient user.
# Recommendation
- Recommended friends: GET /api/suggested–friends/<user_id>
Get recommended friends for the given user id.

The recommendation algorithm runs in the complexity of O(Nlog N)

  

