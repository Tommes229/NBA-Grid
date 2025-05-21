let selectedGridItem = 0;
let teams = [];
let grid = [];


document.addEventListener('DOMContentLoaded', function() {

    initGame();
    
    // Set up the search and submit functionality
    document.getElementById('searchButton').addEventListener('click', submitPlayer);
    document.getElementById('playerSearch').addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            submitPlayer();
        }
    });
    
    // Set up radio button selection
    const radioButtons = document.querySelectorAll('input[type="radio"]');
    radioButtons.forEach((radio) => {
        radio.addEventListener('change', function() {
            selectedGridItem = parseInt(this.value);
        });
    });
    
   // Set up reset button
    document.getElementById('resetButton').addEventListener('click', function() {
        selectedGridItem = 0;
        const gridItems = document.querySelectorAll('.grid_item');
        gridItems.forEach((item) => {
            const img = item.querySelector('img');
            if (img) img.style.display = 'block';

            const radio = item.querySelector('input[type="radio"]');
            if (radio) {
                radio.checked = false;
                radio.disabled = false;
            }

            const playerInfo = item.querySelector('.player-info');
            if (playerInfo) {
                playerInfo.remove();
            }
        });

        // Clear the search field and message
        document.getElementById('playerSearch').value = '';
        const messageArea = document.getElementById('message');
        if (messageArea) {
            messageArea.textContent = '';
            messageArea.classList.remove('show');
        }

        // Re-initialize grid headers, etc.
        initGame();
    });


});

// Initialize the game board
function initGame() {
    // Generate the grid
    eel.generateGrid()(function(result) {
        teams = result.teams;
        grid = result.grid;
        
        // Set the team names in the grid header cells
        for (let i = 1; i <= 3; i++) {
            document.getElementById(`team-row-${i}`).textContent = grid[i][0];
            document.getElementById(`team-col-${i}`).textContent = grid[0][i];
        }
    });
}

// Submit player 
function submitPlayer() {
    const playerName = document.getElementById('playerSearch').value;
    
    if (!playerName || playerName.trim() === '') {
        showMessage('Please enter a player name');
        return;
    }
    
    if (selectedGridItem === 0) {
        showMessage('Please select a grid item first');
        return;
    }
    
    // Convert the selected grid item to row/column coordinates
    const row = Math.ceil(selectedGridItem / 3);
    const col = ((selectedGridItem - 1) % 3) + 1;
    
    // Call Python to check if the player played for both teams
    eel.checkPlayer(playerName, row, col)(function(result) {
        if (result.success) {
            // Mark the grid item as completed
            const gridItem = document.querySelector(`.grid_item${selectedGridItem}`);
            const img = gridItem.querySelector('img');
            const playerInfo = document.createElement('div');
            playerInfo.className = 'player-info';
            playerInfo.textContent = result.playerName;
            
            // Replace the image with the player name
            img.style.display = 'none';
            gridItem.querySelector('input[type="radio"]').disabled = true;
            gridItem.appendChild(playerInfo);
            
            showMessage(`Correct! ${result.playerName} played for both teams.`, true);
        } else if (result.playerFound) {
            showMessage(`Incorrect. ${result.playerName} has not played for both teams.`);
        } else {
            showMessage('Player not found. Please check the spelling.');
        }
        
        // Clear the search field
        document.getElementById('playerSearch').value = '';
    });
}

// Display a message to the user
function showMessage(msg, isCorrect = false) {
    const messageArea = document.getElementById('message');
    messageArea.textContent = msg;

    if (isCorrect) {
        messageArea.classList.add('show', 'correct');
    } else {
        messageArea.classList.add('show');
        messageArea.classList.remove('correct');
    }
    
    
    // Auto-hide after 3 seconds
    setTimeout(() => {
        messageArea.classList.remove('show');
    }, 3000);
}
