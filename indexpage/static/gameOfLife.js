/*
 A JavaScript implementation of Conway's Game of life:
 http://en.wikipedia.org/wiki/Conway%27s_Game_of_Life
 */

"use strict";
/* jshint browser: true, devel: true, globalstrict: true */


/*
 Global variables.
 */

// Globals relevant to rendering
var g_canvas = document.getElementById("myCanvas");
var g_ctx = g_canvas.getContext("2d");

// Game logic globals
var g_cellMatrix;
var g_neighbourOffsets = [
    {col: -1, row: -1},
    {col: 0, row: -1},
    {col: 1, row: -1},
    {col: -1, row: 0},
    {col: 1, row: 0},
    {col: -1, row: 1},
    {col: 0, row: 1},
    {col: 1, row: 1}
];
var g_colCount;
var g_rowCount;
var g_generations = 0;

/*
 CELLS
 Logic relating to individual cells
 */

function Cell(descr) {
    this.isAlive = descr.isAlive;

    this.row = descr.row;
    this.col = descr.col;
    this.size = descr.size;
}

// Calculates whether the cell should live on to the next generation.
Cell.prototype.willSurvive = function () {
    var numAliveNeighbours = 0;

    // Checking how many living neighbours the cell has
    for (var k = 0; k < g_neighbourOffsets.length; k++) {
        var rowOff = g_neighbourOffsets[k].row;
        var colOff = g_neighbourOffsets[k].col;

        var row = this.row + rowOff;
        var col = this.col + colOff;

        // Wrap-around logic
        if (row > (g_rowCount - 1)) {
            row -= (g_rowCount - 1);
        } else if (row < 0) {
            row += (g_rowCount - 1);
        }
        if (col > (g_colCount - 1)) {
            col -= (g_colCount - 1);
        } else if (col < 0) {
            col += (g_colCount - 1);
        }

        var neighbouringCell = g_cellMatrix[row][col];

        if (neighbouringCell.isAlive) {
            numAliveNeighbours++;
        }
    }

    // Making a decision on whether the cell will live based on the
    // neighbour count. Constants standard for the GoL.
    if (this.isAlive) {
        return numAliveNeighbours === 2 || numAliveNeighbours === 3;
    } else {
        return numAliveNeighbours === 3;
    }
};

Cell.prototype.changeColor = function () {
    if (this.isAlive) {
        this.color = "black";
    } else {
        this.color = "white";
    }
};

Cell.prototype.render = function (ctx) {
    var size = this.size;

    this.changeColor();
    var oldFillStyle = ctx.fillStyle;
    ctx.fillStyle = this.color;
    ctx.fillRect(this.col * size, this.row * size, size, size);
    ctx.fillStyle = oldFillStyle;
};


/*
 Methods relating to the simulation as a whole
 */

// Big fat method to initialize the cells
function initializeSimulation(cellSize, livingCells) {
    g_cellMatrix = [];

    // If no array of living cell coordinates is given, we generate some
    var generateRandomly = livingCells === undefined;

    // The size of the base matrix calculated from the drawing canvas size
    g_colCount = Math.floor(g_canvas.width / cellSize);
    g_rowCount = Math.floor(g_canvas.height / cellSize);

    for (var i = 0; i < g_rowCount; i++) {
        g_cellMatrix[i] = [];
        for (var j = 0; j < g_colCount; j++) {
            var cellIsAlive;
            if (generateRandomly) {
                var chance = 0.5; // Arbitrarily decided.
                cellIsAlive = Math.random() > chance;
            } else {
                cellIsAlive = false;
            }
            g_cellMatrix[i][j] = new Cell({
                row: i,
                col: j,
                isAlive: cellIsAlive,
                size: cellSize
            });
        }
    }

    if (!generateRandomly) {
        for (var k = 0; k < livingCells.length; k++) {
            var livingCell = livingCells[k];
            g_cellMatrix[livingCell[0]][livingCell[1]].isAlive = true;
        }
    }
}

function updateSimulation() {

    var lifeMatrix = [];
    for (var i = 0; i < g_cellMatrix.length; i++) {
        lifeMatrix[i] = [];
        for (var j = 0; j < g_cellMatrix[i].length; j++) {
            var currentCell = g_cellMatrix[i][j];
            lifeMatrix[i][j] = currentCell.willSurvive();
        }
    }

    for (var k = 0; k < g_cellMatrix.length; k++) {
        for (var l = 0; l < g_cellMatrix[k].length; l++) {
            g_cellMatrix[k][l].isAlive = lifeMatrix[k][l];
        }
    }
    g_generations++;
}

function renderSimulation() {
    for (var i = 0; i < g_cellMatrix.length; i++) {
        for (var j = 0; j < g_cellMatrix[i].length; j++) {
            var currentCell = g_cellMatrix[i][j];
            currentCell.render(g_ctx);
        }
    }
}

/*
 Main loop. Iterates at a fixed interval.
 */

function main() {
    updateSimulation();
    renderSimulation(g_ctx);
}
window.setInterval(main, 100);

// Kick it off!
var g_cell_size = 5;
initializeSimulation(g_cell_size, undefined);