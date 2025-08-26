<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tictactoe</title>

    <style>
        .board {
          display: grid;
          grid-template-columns: repeat(3, 1fr);
          grid-template-rows: repeat(3, 1fr);
          gap: 5px;
          width: 300px;
          height: 300px;
          margin: 0 auto;
          border: 1px solid #ccc;
          padding: 5px;
        }
  
        .cell {
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 24px;
          font-weight: bold;
          background-color: #f2f2f2;
          cursor: pointer;
        }
  
        #currentPlayer  {
          text-align: center;
          font-size: 24px;
          margin-top: 20px;
        }
      </style>

</head>
<body>
    <div class="board">
        <div class="cell"></div>
        <div class="cell"></div>
        <div class="cell"></div>
        <div class="cell"></div>
        <div class="cell"></div>
        <div class="cell"></div>
        <div class="cell"></div>
        <div class="cell"></div>
        <div class="cell"></div>
      </div>
      <div id="currentPlayer">'X to play'</div>
</body>


<script>
    var winner = '';
    const colorlist = ["#bfbfbf","#999999","#404040"];
    const board = [0, 0, 0, 0, 0, 0, 0, 0, 0];
    const cells = document.querySelectorAll(".cell");
    let currentPlayer = "X";


    function updateCellView(board){
        for (let i = 0; i < cells.length; i++){
            if (board[i] > 0){
                cells[i].textContent = 'X';
                cells[i].style.color = colorlist[board[i]-1];
            }else if (board[i] < 0){
                cells[i].textContent = 'O';
                cells[i].style.color = colorlist[-board[i]-1];
            }else {
                cells[i].textContent = '';
            }
        } 
    }


    function updateLife(board,currentPlayer){
        for (let i = 0; i < cells.length; i++){
            if (board[i] > 0 && currentPlayer === "X"){
                board[i] = board[i]-1
            }else if (board[i] < 0 && currentPlayer === "O"){
                board[i] = board[i]+1
            }
        }
    }


    function switchPlayer(){
        if (currentPlayer === "X"){
            currentPlayer = "O";
        }else{
            currentPlayer = "X";
        }
        if (winner === ''){document.getElementById("currentPlayer").textContent = currentPlayer + ' to play';}
    }

    function checkWinner(board){
        const winningCombinations = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6],
      ];
      for (let i = 0; i < winningCombinations.length; i++){
        const [a, b, c] = winningCombinations[i];
        if ((board[a] >0 && board[b] >0 && board[c] >0) || (board[a] <0 && board[b] <0 && board[c] <0) ){
            cells[a].style.color = 'red';
            cells[b].style.color = 'red';
            cells[c].style.color = 'red';
            winner =  cells[a].textContent;
            document.getElementById("currentPlayer").textContent = winner  + ' Win!';
        }
      }
    }




    function step(index){
        if (board[index] != 0 || winner != ''){return '';}
        if (currentPlayer === "X"){board[index] = 3;}else{board[index] = -3;}
        updateCellView(board)
        checkWinner(board)
        updateLife(board,currentPlayer)
        switchPlayer()  
    }


    cells.forEach((cell, index) => {
      cell.addEventListener("click", () => step(index));
    });



</script>


</html>







