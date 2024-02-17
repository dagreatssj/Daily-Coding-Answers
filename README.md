# Daily Coding Answers

### Getting Started

This project uses ollama and GCP Gmail API.

When using ollama as an API use `OLLAMA_HOST=0.0.0.0:11435 ollama serve` and use the same env var for client.

1. Create model `ollama create coding-challenge-solver-model -f ./Modelfile`
2. Run model `ollama run coding-challenge-solver-model`

### Usage

For testing this is a question from daily coding challenge:
```text
You are given a circular lock with three wheels, each of which display the numbers 0 through 9 in order. Each of these
wheels rotate clockwise and counterclockwise.

In addition, the lock has a certain number of "dead ends", meaning that if you turn the wheels to one of these
combinations, the lock becomes stuck in that state and cannot be opened.

Let us consider a "move" to be a rotation of a single wheel by one digit, in either direction. Given a lock initially
set to 000, a target combination, and a list of dead ends, write a function that returns the minimum number of moves
required to reach the target state, or None if this is impossible.
```
