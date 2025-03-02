import json
import threading
import time
from channels.generic.websocket import WebsocketConsumer
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from .models import ChatMessage

User = get_user_model()

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.keep_alive = True  

        # Extract token from query parameters
        query_params = self.scope['query_string'].decode('utf-8')
        print(f"Query Params: {query_params}")
        token = None
        for param in query_params.split('&'):
            if param.startswith('token='):
                token = param.split('=')[1]
                break

        if not token:
            print("No token found!")
            self.close()
            return

        try:
            # Validate the token and get user
            access_token = AccessToken(token)
            user_id = access_token['user_id']
            self.user = User.objects.get(id=user_id)
            print(f"Authenticated user: {self.user.username}")
        except (KeyError, ObjectDoesNotExist, Exception):
            print(f"Authentication failed:")
            self.close()
            return

        self.receiver_username = self.scope['url_route']['kwargs']['receiver_username']

        try:
            self.receiver = User.objects.get(username=self.receiver_username)
            print(f"Receiver found: {self.receiver.username}")  # Debugging
        except User.DoesNotExist:
            print("Receiver not found, closing connection.")
            self.close()
            return

        self.accept()  # Accept connection
        print("WebSocket connection accepted.")  # Debugging
        # Start keep-alive loop inside the same thread (NO blocking, NO crashes)
        self.start_keep_alive()

    def start_keep_alive(self):
        """Sends a ping every 30 seconds to keep the connection open."""
        def keep_alive_loop():
            while self.keep_alive:  # Runs until disconnect
                try:
                    time.sleep(30)  # Wait 30 seconds
                    self.send(json.dumps({
                        'type': 'keep_alive',
                        'message': 'ping',
                    }))
                    print("Sent keep-alive ping")
                except Exception as e:
                    print(f"Keep-alive error: {e}")
                    break  # Stop the loop if an error occurs

        #Runs the keep-alive function in the background (doesn't block message processing).            
        threading.Thread(target=keep_alive_loop, daemon=True).start()

    def disconnect(self, close_code):
        self.keep_alive = False

    def receive(self, text_data):

        try:
            text_data_json = json.loads(text_data)
        except json.JSONDecodeError as e:
            return  # Exit function if JSON is invalid

        message = text_data_json.get('message', text_data_json.get('content', '')).strip()


        if not message:
            print("Received an empty message. Ignoring.")
            return  

        print(f"Attempting to save message: '{message}'")
        print(f"Sender: {self.user} (ID: {self.user.id if self.user else 'None'})")
        print(f"Receiver: {self.receiver} (ID: {self.receiver.id if self.receiver else 'None'})")

        try:
            chat_message = ChatMessage.objects.create(
                sender=self.user, 
                receiver=self.receiver, 
                content=message
            )
            print(f"Message saved successfully: {chat_message}")
        except Exception as e:
            print(f"Error saving message: {e}")

        # Send message back to the same client
        self.send(json.dumps({
            'message': message,
            'sender': self.user.username,
        }))



