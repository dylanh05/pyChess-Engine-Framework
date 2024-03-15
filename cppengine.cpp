#include <iostream>
#include "chess.hpp"
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <vector>
#include <map>
#include <string>

namespace py = pybind11;

class Engine {
    public:
        Engine(){
            this->color = "";
        }

        Engine(std::string col){
            this->color = col;
        }

        std::string get_color(){
            return this->color;
        }

        void set_color(std::string col){
            this->color = col;
        }

        float evaluate(chess::Board board){
            if(board.isHalfMoveDraw()){
                std::pair<chess::GameResultReason, chess::GameResult> results = board.getHalfMoveDrawType();
                chess::GameResultReason reason = results.first;
                chess::GameResult result = results.second;
                if(reason == chess::GameResultReason::CHECKMATE){
                    if(this->color == "black")
                        return -10000;
                    else 
                        return 10000;
                }
                else if (result == chess::GameResult::DRAW)
                    return 0;
            }
            
            // Slows down eval significantly!!
            int score = 0;
            std::string pieces = board.getFen(false);
            for(int i = 0; i < pieces.size(); i++){
                if(pieces[i] == ' ')
                    break;
                else if (this->values.find(pieces[i]) != this->values.end()){
                    score = score + this->values[pieces[i]];
                }
            }
            return score;
        }

        std::pair<std::string, int> make_move(std::string position, std::vector<std::string> moves){
            chess::Board board = chess::Board(position);

            int best_score = -10000;
            chess::Move best_move = chess::uci::uciToMove(board, moves[0]);;
            if(this->color == "black")
                best_score = 10000;
            
            for(int i = 0; i < moves.size(); i++){
                chess::Move move = chess::uci::uciToMove(board, moves[i]);
                board.makeMove(move);
                int score = this->evaluate(board);
                if(this->color == "white"){
                    if(score > best_score){
                        best_score = score;
                        best_move = move;
                    }
                }
                else{
                    if(score < best_score){
                        best_score = score;
                        best_move = move;
                    }
                }
                board.unmakeMove(move);
            }

            std::string move = chess::uci::moveToUci(best_move);
            std::pair<std::string, int> data = std::make_pair(move, best_score);
            return data;
        }
        
    private:
        int depth;
        std::string color;
        bool is_eg;
        bool is_op;
        int eval_value;
        int num_exceptions;
        bool opening_prep;
        std::string opening_path;

        std::map<char, int> values {{'r', -5}, {'n', -3}, {'b', -3},
                {'q', -9}, {'k', 0}, {'p', -1},{'R', 5}, {'N', 3}, 
                {'B', 3}, {'Q', 9}, {'K', 0}, {'P', 1}, {'.', 0}};
        

};







PYBIND11_MODULE(cEngine, handle){
    handle.doc() = "Cpp Engine Python Wrapper";

    py::class_<Engine>(
        handle, "cEngine"
    ).def(py::init<std::string>())
    .def("get_color", &Engine::get_color)
    .def("set_color", &Engine::set_color)
    .def("evaluate", &Engine::evaluate)
    .def("make_move", &Engine::make_move)
    ;
}

