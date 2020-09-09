# Noughts and Crosses
Simple interactive demo of a perfect noughts and crosses (tic tac toe) AI using minimax + alpha beta pruning.

This was used as part of a live demo for an outreach lecture in May 2020 to show prospective students the kind of things they might learn as part of an AI unit at the University of Bath.

Simply run `noughts_and_crosses.py` to get an interactive prompt to play against the AI. It will be slower if the AI goes first, since it has to compute every possible game (minus optimisations from alpha-beta pruning). None of these results are cached, though this would be trivial to add. The purpose of the demo was just the minimax algorithm.

It should be easy to see in the `play()` function how you could set up AI vs AI or human vs human too.