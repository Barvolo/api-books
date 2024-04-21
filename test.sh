#!/bin/bash

# Define the commands
commands=(
    'curl -X POST -H "Content-Type: application/json" -d '\''{"title": "Book Title 1", "ISBN": "9780805371757", "genre": "Fiction"}'\'' http://localhost:8000/books'
    'curl -X POST -H "Content-Type: application/json" -d '\''{"title": "Book Title 2", "ISBN": "9780805371762", "genre": "Fiction"}'\'' http://localhost:8000/books'
    'curl -X POST -H "Content-Type: application/json" -d '\''{"title": "Book Title 3", "ISBN": "9780805371801", "genre": "Fiction"}'\'' http://localhost:8000/books'
    'curl -X POST -H "Content-Type: application/json" -d '\''{"title": "Book Title 4", "ISBN": "9780805371710", "genre": "Fiction"}'\'' http://localhost:8000/books'
    'curl -X POST -H "Content-Type: application/json" -d '\''{"title": "Book Title 5", "ISBN": "9781408855652", "genre": "Fiction"}'\'' http://localhost:8000/books'
)

# Execute the commands
for command in "${commands[@]}"; do
    echo "Executing command: $command"
    eval $command
done



curl -X POST -H "Content-Type: application/json" -d '{"value": 4}' http://localhost:8000/ratings/1/values
curl -X POST -H "Content-Type: application/json" -d '{"value": 4}' http://localhost:8000/ratings/1/values
curl -X POST -H "Content-Type: application/json" -d '{"value": 4}' http://localhost:8000/ratings/1/values
curl -X POST -H "Content-Type: application/json" -d '{"value": 4}' http://localhost:8000/ratings/2/values
curl -X POST -H "Content-Type: application/json" -d '{"value": 4}' http://localhost:8000/ratings/2/values
curl -X POST -H "Content-Type: application/json" -d '{"value": 4}' http://localhost:8000/ratings/2/values
curl -X POST -H "Content-Type: application/json" -d '{"value": 4}' http://localhost:8000/ratings/3/values
curl -X POST -H "Content-Type: application/json" -d '{"value": 4}' http://localhost:8000/ratings/3/values
curl -X POST -H "Content-Type: application/json" -d '{"value": 4}' http://localhost:8000/ratings/3/values
curl -X POST -H "Content-Type: application/json" -d '{"value": 4}' http://localhost:8000/ratings/4/values
curl -X POST -H "Content-Type: application/json" -d '{"value": 4}' http://localhost:8000/ratings/4/values
curl -X POST -H "Content-Type: application/json" -d '{"value": 4}' http://localhost:8000/ratings/4/values
curl -X POST -H "Content-Type: application/json" -d '{"value": 4}' http://localhost:8000/ratings/5/values
curl -X POST -H "Content-Type: application/json" -d '{"value": 4}' http://localhost:8000/ratings/5/values
curl -X POST -H "Content-Type: application/json" -d '{"value": 4}' http://localhost:8000/ratings/5/values

