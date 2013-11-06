package main

import (
	"fmt"
    "net/http"
	"github.com/xboard/sudoku_solver/sudoku"
)
func init() {
	http.HandleFunc("/", MainPage)
	http.HandleFunc("/view", ViewHandler)
	http.HandleFunc("/solve", SolveHandler)
}
func MainPage(w http.ResponseWriter, r *http.Request) {
    fmt.Fprint(w, "Hello, world!")
}
func ViewHandler(w http.ResponseWriter, r *http.Request) {
    fmt.Fprint(w, "Hello, world!2")
}

//This is what you used to get Sudoku solutions
//Send a GET request with the query paramaters: puzzle [with the unsolved puzzle]
//Recieve: plain text with the solution in a grid
func SolveHandler(w http.ResponseWriter, r *http.Request) {
	switch r.Method{
	case "GET":
		//Extract query params
		params := r.URL.Query()
	    puzzle := params["puzzle"]
	
		//Solve this puzzle
		solution := sudoku.Solve(puzzle[0])
	
		//Print out
		sudoku.Display(w,solution)
		
	default:
		fmt.Fprint(w,"Unsupported Call")
	}
}
