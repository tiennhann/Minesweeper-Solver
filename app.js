// Wait for the DOM to be ready before starting the game
document.addEventListener('DOMContentLoaded', () => {
    // Declare variables and store references to the game board and UI elements
    const grid = document.querySelector('.grid');
    const flagsLeft = document.querySelector('#flags-left');
    const result = document.querySelector('#result');
    const width = 5;   // Width of the game board
    let bombAmount = 5;    // Total number of bombs
    let squares = [];   // Array to store each square in the game board
    let isGameOver = false; // Boolean to check if the game is over
    let flags = 0;  // Counter for flags placed on the board

    // Function to create a game board
    function createBoard() {
        flagsLeft.innerHTML = bombAmount;   // Display initial number of bombs
        while (grid.hasChildNodes())
            grid.removeChild(grid.firstChild);

        // Create array for bombs and valid square 
        const bombsArray = Array(bombAmount).fill('bomb');
        const emptyArray = Array(width * width - bombAmount).fill('valid');
        
        // Shuffle the bombsArray and emptyArray together
        const gameArray = emptyArray.concat(bombsArray).sort(() => Math.random() - 0.5);

        // For loop to create each square as div element for the grid,
        // set attributes and also event listeners
        for (let i = 0; i < width * width; i++) {
            const square = document.createElement('div');
            square.id = i;  // Assign the ID to each square for the reference later
            square.classList.add(gameArray[i]); // Assign the class 'bomb' or 'valid' to each square
            grid.appendChild(square);
            squares.push(square);
            
            // Left click and right click event listeners
            square.addEventListener('click', () => click(square));
            square.addEventListener('contextmenu', (e) => {
                e.preventDefault();
                addFlag(square);
            });
        }

        // Calculate number of 'valid' squares indicating the count of adjacent bombs (boms around each square)
        for (let i = 0; i < squares.length; i++) {
            if (squares[i].classList.contains('valid')) {
                let total = 0;
                // Left edge usually at index 0,10,20...
                const isLeftEdge = i % width === 0;
                // Right edge usually at index 9,19,29...
                const isRightEdge = i % width === width - 1;

                // // You can use a loop or function here to avoid repeated code
                // if (i > 0 && !isLeftEdge && squares[i - 1].classList.contains('bomb')) total++;
                // if (i < 99 && !isRightEdge && squares[i + 1].classList.contains('bomb')) total++;
                // if (i > 10 && squares[i - width].classList.contains('bomb')) total++;
                // if (i > 9 && !isRightEdge && squares[i - width + 1].classList.contains('bomb')) total++;
                // if (i > 11 && !isLeftEdge && squares[i - width - 1].classList.contains('bomb')) total++;
                // if (i < 89 && squares[i + width].classList.contains('bomb')) total++;
                // if (i < 88 && !isRightEdge && squares[i + width + 1].classList.contains('bomb')) total++;
                // if (i < 90 && !isLeftEdge && squares[i + width - 1].classList.contains('bomb')) total++;
                
                // Define all directions of neighboring squares
                const directions = [
                    -1, +1, -width, +width, // Left, Right, Above, Below
                    -width -1, -width + 1,  // Top-left, Top-right
                    +width - 1, +width + 1,  // Bottom-left, Bottom-right
                ];

                // Check for each direction above
                directions.forEach((offset) => {
                    const index = i + offset;
                    // Check if the neighboring square is valid within the grid boundaries
                    if (
                        index >= 0 && index < width * width && // must be inside the grid
                        !(isLeftEdge && [-1, -width - 1, +width - 1].includes(offset)) && // must not be on the left
                        !(isRightEdge && [+1, -width + 1, +width + 1].includes(offset)) // must not be on the right
                    ) {
                        if(squares[index].classList.contains('bomb'))
                            total++;
                    }
                });
                squares[i].setAttribute('mydata', total);
                console.log('mydata', total);
            }
        }
    }

    createBoard();

    function addFlag(square) {
        if (isGameOver) return;
        if (!square.classList.contains('checked') && flags < bombAmount) {
            if (!square.classList.contains('flag')) {
                square.classList.add('flag');
                square.innerHTML = '🚩';
                flags++;
            } else {
                square.classList.remove('flag');
                square.innerHTML = '';
                flags--;
            }
            flagsLeft.innerHTML = bombAmount - flags;
        }
        checkWin();
    }

    function click(square) {
        if (isGameOver || square.classList.contains('checked') || square.classList.contains('flag')) return;

        if (square.classList.contains('bomb')) {
            gameOver();
        } else {
            let total = parseInt(square.getAttribute('mydata'));
            if (total !== 0) {
                square.innerHTML = total;
                square.classList.add('checked');
                square.classList.add(['one', 'two', 'three', 'four'][total - 1]);
            } else {
                checkSquare(square);
            }
            square.classList.add('checked');
            checkWin();
        }
    }

    function checkSquare(square) {
        const currentId = parseInt(square.id);
        const isLeftEdge = currentId % width === 0;
        const isRightEdge = currentId % width === width - 1;

        setTimeout(() => {
            if (currentId > 0 && !isLeftEdge) click(document.getElementById(currentId - 1));
            if (currentId > 9 && !isRightEdge) click(document.getElementById(currentId + 1 - width));
            if (currentId > 10) click(document.getElementById(currentId - width));
            if (currentId > 11 && !isLeftEdge) click(document.getElementById(currentId - 1 - width));
            if (currentId < 98 && !isRightEdge) click(document.getElementById(currentId + 1));
            if (currentId < 90 && !isLeftEdge) click(document.getElementById(currentId - 1 + width));
            if (currentId < 88 && !isRightEdge) click(document.getElementById(currentId + 1 + width));
            if (currentId < 89) click(document.getElementById(currentId + width));
        }, 10);
    }

    function checkWin() {
        let matches = 0;
        let safeSquaresOpened = true;

        squares.forEach(square => {
            if (square.classList.contains('flag') && square.classList.contains('bomb')) {
                matches++;
            }
            if (!square.classList.contains('bomb') && !square.classList.contains('checked')) {
                safeSquaresOpened = false;
            }
        });
        if (matches === bombAmount || safeSquaresOpened) {
            result.innerHTML = "You Win!";
            isGameOver = true;
            squares.forEach(square => {
                if (square.classList.contains('bomb') && !square.classList.contains('flag')) {
                    square.classList.add('flag');
                    square.innerHTML = '🚩';
                }
            })
        }
    }

    function gameOver() {
        result.innerHTML = "Game Over";
        isGameOver = true;
        squares.forEach(square => {
            if (square.classList.contains('bomb')) {
                square.innerHTML = '💣';
                square.classList.add('checked');
            }
        });
    }

    // Code for importing the backend from python
    document.getElementById('solve-button').addEventListener('click', () => {
        const board = squares.map(square => ({
            index: parseInt(square.id),
            status: square.classList.contains('checked') ? 'checked' : 'covered',
            isFlagged: square.classList.contains('flag'),
            number: square.getAttribute('mydata') === null?-1:0 
        }));

        fetch('http://localhost:5001/solve', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ board: board, width: width })
        })
        .then(response => response.json())
        .then(data => {
            data.forEach(action => {
                const targetSquare = squares[action.index];
                if (action.action === 'click') {
                    click(targetSquare);
                } else if (action.action === 'flag') {
                    addFlag(targetSquare);
                }
            });
        })
        .catch(error => console.error('Error:', error));
    });

    document.getElementById('astar-button').addEventListener('click', () => {
        const board = squares.map(square => ({
            index: parseInt(square.id),
            status: square.classList.contains('checked') ? 'checked' : 'covered',
            isFlagged: square.classList.contains('flag'),
            number: square.getAttribute('mydata') === null?-1:0 
        }));

        fetch('http://localhost:5001/astar', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ board: board, width: width })
        })
        .then(response => response.json())
        .then(data => {
            data.forEach(action => {
                const targetSquare = squares[action.index];
                if (action.action === 'click') {
                    click(targetSquare);
                } else if (action.action === 'flag') {
                    addFlag(targetSquare);
                }
            });
        })
        
        .catch(error => console.error('Error:', error));
    });
});