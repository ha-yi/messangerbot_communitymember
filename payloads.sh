curl -X POST -H "Content-Type: application/json" -d '{
  "get_started": {"payload": "START"}
}' "https://graph.facebook.com/v2.6/me/messenger_profile?access_token=EAAbysoLqFlMBADTYl25Wc8ZBFlyCxpT8iU2qzZBYH2GPb8XN9nUqrFgf2Y09l7fVYe0ZA3VFoAiA6QdVID2JVoKKcZAM7TI60VZAmFmKhHgNbqH1iiIwbisIPUzR8NRimnJ5CZBLSJdH0WldPrZCw8C8Yrn13wDVFIfZATn5Gt2gtgZDZD"

curl -X POST -H "Content-Type: application/json" -d '{
  "greeting": [
    {
      "locale":"default",
      "text":"Hello! Welcome to Lombok {DEV} Community" 
    }
  ]
}' "https://graph.facebook.com/v2.6/me/messenger_profile?access_token=EAAbysoLqFlMBADTYl25Wc8ZBFlyCxpT8iU2qzZBYH2GPb8XN9nUqrFgf2Y09l7fVYe0ZA3VFoAiA6QdVID2JVoKKcZAM7TI60VZAmFmKhHgNbqH1iiIwbisIPUzR8NRimnJ5CZBLSJdH0WldPrZCw8C8Yrn13wDVFIfZATn5Gt2gtgZDZD"
