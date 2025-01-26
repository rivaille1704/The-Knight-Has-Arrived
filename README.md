This is a simple game for 2 players.
Rules:
<pre>
  Each player will take turns controlling 3 knights on the board.
  Each knight can only move to the right. It cannot go out of the board, cross another row, or go backwards (to the left). 
  The number of spaces it can move at one time is unlimited (up to the edge of the board). Once a knight reaches the edge of the board, it cannot move any further.
  The winner is the one who, on his turn, makes three knights come to the side of the board.
  At the start of the game, the 3 knights cannot have 2 knights on the same column and cannot have a knight already on the right side of the board.
</pre>
For example, the initial formation would look like this:

![image](https://github.com/user-attachments/assets/3f455670-7691-47e6-84c8-859e49a9d876)

If you are the first player, you want to speed up the progress and play the first move by bringing the blue knight to the edge of the board:

![image](https://github.com/user-attachments/assets/2660339d-87a4-4f8d-99d8-08eeeb253b58)

The opponent has seen how to win, they play like this:

![image](https://github.com/user-attachments/assets/4c299f60-bbbe-461c-9325-010bc7607e6e)

On your turn, if you move one of the green or red knights to a certain position, your opponent will move the other knight so that these two knights are in the same column. 

![image](https://github.com/user-attachments/assets/6e26ddf6-16eb-44d6-9d99-e2b04207fcd9)

![image](https://github.com/user-attachments/assets/dc0c0153-d9e8-4eba-92bd-b6d3d9c85657)

Therefore, gradually the game will lead to the opponent winning.

![image](https://github.com/user-attachments/assets/fc532b18-b3f8-4973-b9fa-ec0e1eae1f08)

As you can see in the example above, the first mover made a mistake. However, if he had made the right move, the first mover could have still won. So you have to think more to win!


This project has had some interesting things:

<pre>
  Knights: I used knights modeled after the Fire Emblem (ファイアーエムブレム) series.
  Animation: I created an animation that performs the knights' movements at 30FPS
</pre>

In the future I think the project will be able to develop as follows:

<pre>
  Create more interfaces to make the game more vivid.
  Create a game menu and put instructions on how to play the game into the game.
  Create a bot that can play against players (This mode will be called "vs CPU")
  Create an AI that can learn this gameplay and become a "good player".
</pre>

According to game theory, there will always be a way for the first mover to always win, or the second mover to always win. Please think about it and find outヾ(≧▽≦*)o
