#include <iostream>
#include "chess.hpp"
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <vector>
#include <numeric>
#include <map>
#include <string>

namespace py = pybind11;

class Engine {
    public:
        Engine(){
            this->color = "";
        }

        Engine(std::string col){
            this->depth = 4;
            this->color = col;
            this->is_eg = false;
            this->is_op = true;
            this->eval_value = 0;
            this->opening_prep = true;
            this->opening_path = false;
        }

        class TreeNode{
            public:
                TreeNode(chess::Board position){
                    this->state = position;
                }
            private:
                chess::Board state;
                int eval;
                std::vector<TreeNode> children;
        };

        std::string get_color(){
            return this->color;
        }

        void eval_value_adjust(chess::Board& board, int eval_value) {
            std::string fen = board.getFen(false);

            int score = 0;
            for (int i = 0; i < fen.length(); ++i) {
                char piece = fen[i];
                if(piece == ' ')
                    break;

                if(this->values.find(piece) != this->values.end()){
                    score = score + this->values[piece];
                }
            }

            if(board.sideToMove() == chess::Color::WHITE) {
                if (std::abs(score) < 200) {
                    this->eval_value = (eval_value - 150) / 400.0;
                } else {
                    this->eval_value = (eval_value - 150) / 100.0;
                }
            } else {
                if (std::abs(score) < 200) {
                    this->eval_value = (eval_value + 150) / 400.0;
                } else {
                    this->eval_value = (eval_value + 150) / 100.0;
                }
            }
        }

        float evaluate(chess::Board &board){
            std::pair<chess::GameResultReason, chess::GameResult> results = board.isGameOver();
            chess::GameResultReason reason = results.first;
            chess::GameResult result = results.second;
            if(reason == chess::GameResultReason::CHECKMATE){
                if(board.sideToMove() == chess::Color::BLACK){
                    return 100000;
                }
                else{ 
                    return -100000;
                }
            }
            else if (result == chess::GameResult::DRAW)
                return 0;
            
            
            int score = 0;
            std::string pieces = board.getFen(false);

            int count = 0;
            for(int i = 0; i < pieces.size(); i++){
                char piece = pieces[i];
                if(piece == ' ')
                    break;

                // for piece sq tables
                else if(isdigit(piece)){
                    int add = piece - '0';
                    count = count + add - 1;
                    continue;
                }

                else if(piece == '/'){
                    continue;
                }

                // Add values
                if(this->values.find(piece) != this->values.end()){
                    score = score + this->values[piece];
                }

                // Add pc-sq scores
                if(isupper(piece)){
                    score = score + this->mg_table[(char)tolower(piece)][count];
                }
                else{
                    int flip_index = this->flip[count];
                    score = score - this->mg_table[piece][flip_index];
                }

                count++;
            }

            score = score + rand() % 11 - 5;
            return score;
        }


        std::pair<std::string, float> make_move(std::string position){
            chess::Board board = chess::Board(position);
            std::pair<std::string, float> move_and_eval;
            
            // Openings


            for(int i = 1; i < this->depth; i++){
                move_and_eval = this->make_move_helper(board, i);
            }
            
            // If a move would cause a draw in a winning position, find the next best move
            chess::Move move = chess::uci::uciToMove(board, move_and_eval.first);
            board.makeMove(move);

            std::cout << (board.isRepetition(1)) << std::endl;

            if (board.isGameOver().second == chess::GameResult::DRAW){
                board.unmakeMove(move);
                if (this->color == "white" && this->eval_value > 1) {
                    //this->eval_value_adjust(board, move_and_eval.second);
                    //move_and_eval.second = this->eval_value;
                    return this->next_best_move(move, board, this->depth);
                } 
                else if (color == "black" && eval_value < -1) {
                    //this->eval_value_adjust(board, move_and_eval.second);
                    //move_and_eval.second = this->eval_value;
                    return this->next_best_move(move, board, this->depth);
                } 
                else {
                    eval_value = 0;
                    return std::make_pair(move_and_eval.first, 0);
                }
            } 
            else {
                board.unmakeMove(move);
            }
            this->eval_value_adjust(board, move_and_eval.second);
            move_and_eval.second = this->eval_value;

            return move_and_eval;
            //int best_score = -10000;
            //chess::Move best_move = chess::uci::uciToMove(board, moves[0]);;
            //if(this->color == "black")
            //    best_score = 10000;
            
            //for(int i = 0; i < moves.size(); i++){
            //    chess::Move move = chess::uci::uciToMove(board, moves[i]);
            //    board.makeMove(move);
            //    int score = this->evaluate(board);
            //    if(this->color == "white"){
            //        if(score > best_score){
            //            best_score = score;
            //            best_move = move;
            //        }
            //    }
            //    else{
            //        if(score < best_score){
            //            best_score = score;
            //            best_move = move;
            //        }
            //   }
            //    board.unmakeMove(move);
            //}

            //std::string move = chess::uci::moveToUci(best_move);
            //std::pair<std::string, int> data = std::make_pair(move, best_score);
            //return data;
        }

        std::vector<int> ind_by_eval(chess::Movelist &moves, std::vector<int> &evals, bool is_white){
            std::vector<int> indices(moves.size());
            std::iota(indices.begin(), indices.end(), 0);
            std::sort(indices.begin(), indices.end(),
                    [&](int A, int B) -> bool {
                            if(is_white){
                                return evals[A] > evals[B];
                            }
                            return evals[A] > evals[B];
                        }); 
            return indices;
        }


        std::pair<std::string, int> make_move_helper(chess::Board &board, int depth){
            bool is_white = false;
            if(board.sideToMove() == chess::Color::WHITE){
                is_white = true;
            }

            int best_move = -1000000000;
            if(!is_white){
                best_move = 1000000000;
            }
            std::string best_final = "";
            chess::Movelist moves;
            chess::movegen::legalmoves(moves, board);

            // Move ordering for speed
            std::vector<int> move_val_estimates(moves.size());
            for(int i = 0; i < move_val_estimates.size(); i++) {
                chess::Move move = moves[i];
                board.makeMove(move);
                move_val_estimates[i] = this->evaluate(board);
                board.unmakeMove(move);
            }

            std::vector<int> indices = ind_by_eval(moves, move_val_estimates, is_white);

            for (int i = 0; i < moves.size(); i++) {
                chess::Move move = moves[indices[i]];
                board.makeMove(move);
                int value = this->minimax_helper(depth-1, board, -100000000, 10000000, !is_white);
                board.unmakeMove(move);
                if((is_white && (value > best_move)) || (!is_white && (value < best_move))){
                    best_move = value;
                    best_final = chess::uci::moveToUci(move);
                }
            }
            return {best_final, best_move};
        }   
        

        int minimax_helper(int depth, chess::Board &board, int alpha, int beta, bool is_maximizing) {
            std::pair<chess::GameResultReason, chess::GameResult> results = board.isGameOver();
            
            if (depth <= 0 || results.first != chess::GameResultReason::NONE) {
                return evaluate(board);
            }

            chess::Movelist moves;
            chess::movegen::legalmoves(moves, board);

            if (is_maximizing) {
                int best_move = -10000000;
                for (const auto &move : moves) {
                    board.makeMove(move);
                    int value = minimax_helper(depth - 1, board, alpha, beta, false);
                    board.unmakeMove(move);
                    best_move = std::max(best_move, value);
                    alpha = std::max(alpha, best_move);
                    if (beta <= alpha) {
                        break;
                    }
                }
                return best_move;
            } 
            else {
                int best_move = 10000000;
                for (const auto &move : moves) {
                    board.makeMove(move);
                    int value = minimax_helper(depth - 1, board, alpha, beta, true);
                    board.unmakeMove(move);
                    best_move = std::min(best_move, value);
                    beta = std::min(beta, best_move);
                    if (beta <= alpha) {
                        break;
                    }
                }
                return best_move;
            }
        }

        std::pair<std::string, int> next_best_move(chess::Move draw_move, chess::Board &board, int depth){
            bool is_white = false;
            if(board.sideToMove() == chess::Color::WHITE){
                is_white = true;
            }

            int best_move = -1000000000;
            if(!is_white){
                best_move = 1000000000;
            }
            std::string best_final = "";
            chess::Movelist moves;
            chess::movegen::legalmoves(moves, board);

            // Move ordering for speed
            std::vector<int> move_val_estimates(moves.size());
            for(int i = 0; i < move_val_estimates.size(); i++) {
                chess::Move move = moves[i];                
                board.makeMove(move);
                move_val_estimates[i] = this->evaluate(board);
                board.unmakeMove(move);
            }

            std::vector<int> indices = ind_by_eval(moves, move_val_estimates, is_white);

            for (int i = 0; i < moves.size(); i++) {
                chess::Move move = moves[indices[i]];
                if(move == draw_move)
                    continue;
                board.makeMove(move);
                int value = this->minimax_helper(depth-1, board, -100000000, 10000000, !is_white);
                board.unmakeMove(move);
                if((is_white && (value > best_move)) || (!is_white && (value < best_move))){
                    best_move = value;
                    best_final = chess::uci::moveToUci(move);
                }
            }
            return {best_final, eval_value};
        }   
        
        
    private:
        int depth;
        std::string color;
        bool is_eg;
        bool is_op;
        float eval_value;
        int num_exceptions;
        bool opening_prep;
        std::string opening_path;
        bool sleep;

        std::map<char, int> values {{'r', -500}, {'n', -320}, {'b', -330},
                {'q', -900}, {'k', -9000}, {'p', -100},{'R', 500}, {'N', 320}, 
                {'B', 330}, {'Q', 900}, {'K', 9000}, {'P', 100}, {'.', 0}};
        
        std::vector<int> mg_pawn_table = {
            0,   0,   0,   0,   0,   0,   0,   0,
            5,  10,  15,  20,  20,  15,  10,   5,
            4,   8,  12,  16,  16,  12,   8,   4,
            3,   6,   9,  12,  12,   9,   6,   3,
            2,   4,   6,   8,   8,   6,   4,   2,
            1,   2,   3, -10, -10,   3,   2,   1,
            0,   0,   0, -40, -40,   0,   0,   0,
            0,   0,   0,   0,   0,   0,   0,   0
        };

        std::vector<int> eg_pawn_table = {
            0,   0,   0,   0,   0,   0,   0,   0,
            30,  40,  45,  50,  50,  45,  40,   30,
            20,   18,  16,  16,  16,  16,   18,   20,
            3,   6,   9,  12,  12,   9,   6,   3,
            2,   4,   6,   8,   8,   6,   4,   2,
            1,   2,   3, -10, -10,   3,   2,   1,
            0,   0,   0, -40, -40,   0,   0,   0,
            0,   0,   0,   0,   0,   0,   0,   0};

        std::vector<int> mg_knight_table = {
            -167, -89, -34, -49,  61, -97, -15, -107,
            -73, -41,  5,  3,  2,  4,   1,  -17,
            -47,  31,  2,  4,  7, 6,  3,   3,
            -9,  1,  2,  5,  3,  3,  1,   2,
            -13,   2,  1,  3,  2,  1,  2,   -8,
            -23,  -9,  1,  1,  1,  1,  25,  -16,
            -29, -53, -12,  -3,  -1,  18, -14,  -19,
            -105, -21, -58, -33, -17, -28, -19,  -23};

        std::vector<int> eg_knight_table = {
            -58, -38, -13, -28, -31, -27, -63, -99,
            -25,  -8, -25,  -2,  -9, -25, -24, -52,
            -24, -20,  10,   3,  -1,  -9, -19, -41,
            -17,   -4,  2,  2,  2,  1,   8, -18,
            -18,  -6,  1,  1,  1,  1,   1, -18,
            -23,  -3,  -1,  15,  10,  -3, -20, -22,
            -42, -20, -10,  -5,  -2, -20, -23, -44,
            -29, -51, -23, -15, -22, -18, -50, -64};

        std::vector<int> mg_bishop_table = {
            -29,   4, -82, -37, -25, -42,   7,  -8,
            -26,  16, -18, -13,  30,  59,  18, -47,
            -16,  37,  43,  40,  35,  50,  37,  -2,
            -4,   5,  19,  50,  37,  37,   7,  -2,
            -6,  13,  13,  26,  34,  12,  10,   4,
            0,  15,  15,  15,  14,  27,  18,  10,
            4,  15,  16,   0,   7,  21,  33,   1,
            -33,  -3, -14, -21, -13, -12, -39, -21};

        std::vector<int> eg_bishop_table = {
            -14, -21, -11,  -8, -7,  -9, -17, -24,
            -8,  -4,   7, -12, -3, -13,  -4, -14,
            2,  -8,   0,  -1, -2,   6,   0,   4,
            -3,   9,  12,   9, 14,  10,   3,   2,
            -6,   3,  13,  19,  7,  10,  -3,  -9,
            -12,  -3,   8,  10, 13,   3,  -7, -15,
            -14, -18,  -7,  -1,  4,  -9, -15, -27,
            -23,  -9, -23,  -5, -9, -16,  -5, -17};

        std::vector<int> mg_rook_table = {
            32,  42,  32,  51, 63,  9,  31,  43,
            27,  32,  58,  62, 80, 67,  26,  44,
            -5,  19,  26,  36, 17, 45,  61,  16,
            -24, -11,   7,  26, 24, 35,  -8, -20,
            -36, -26, -12,  -1,  9, -7,   6, -23,
            -45, -25, -16, -17,  3,  0,  -5, -33,
            -44, -16, -20,  -9, -1, 11,  -6, -71,
            -19, -13,   1,  17, 16,  7, -37, -26};

        std::vector<int> eg_rook_table = {
            13, 10, 18, 15, 12,  12,   8,   5,
            11, 13, 13, 11, -3,   3,   8,   3,
            7,  7,  7,  5,  4,  -3,  -5,  -3,
            4,  3, 13,  1,  2,   1,  -1,   2,
            3,  5,  8,  4, -5,  -6,  -8, -11,
            -4,  0, -5, -1, -7, -12,  -8, -16,
            -6, -6,  0,  2, -9,  -9, -11,  -3,
            -9,  2,  3, -1, -5, -13,   4, -20};

        std::vector<int> mg_queen_table = {
            -28,   0,  29,  12,  59,  44,  43,  45,
            -24, -39,  -5,   1, -16,  57,  28,  54,
            -13, -17,   7,   8,  29,  56,  47,  57,
            -27, -27, -16, -16,  -1,  17,  -2,   1,
            -9, -26,  -9, -10,  -2,  -4,   3,  -3,
            -14,   2, -11,  -2,  -5,   2,  14,   5,
            -35,  -8,  11,   2,   8,  15,  -3,   1,
            -1, -18,  -9,  10, -15, -25, -31, -50};

        std::vector<int> eg_queen_table = {
            -9,  22,  22,  27,  27,  19,  10,  20,
            -17,  20,  32,  41,  58,  25,  30,   0,
            -20,   6,   9,  49,  47,  35,  19,   9,
            3,  22,  24,  45,  57,  40,  57,  36,
            -18,  28,  19,  47,  31,  34,  39,  23,
            -16, -27,  15,   6,   9,  17,  10,   5,
            -22, -23, -30, -16, -16, -23, -36, -32,
            -33, -28, -22, -43,  -5, -32, -20, -41};

        std::vector<int> mg_king_table = {
            -65,  23,  16, -15, -56, -34,   2,  13,
            29,  -1, -20,  -7,  -8,  -4, -38, -29,
            -9,  24,   2, -16, -20,   6,  22, -22,
            -17, -20, -12, -27, -30, -25, -14, -36,
            -49,  -1, -27, -39, -46, -44, -33, -51,
            -14, -14, -22, -46, -44, -30, -15, -27,
            1,   7,  -54, -64, -43, -40,   9,   8,
            -15,  36,  -54, -28,  -28, -28,  24,  14};

        std::vector<int> eg_king_table = {
            -74, -35, -18, -18, -11,  15,   4, -17,
            -12,  17,  14,  17,  17,  38,  23,  11,
            10,  17,  23,  15,  20,  45,  44,  13,
            -8,  22,  24,  27,  26,  33,  26,   3,
            -18,  -4,  21,  24,  27,  23,   9, -11,
            -19,  -3,  11,  21,  23,  16,   7,  -9,
            -27, -11,   4,  13,  14,   4,  -5, -17,
            -53, -34, -21, -11, -28, -14, -24, -43};


        std::map<char, std::vector<int>> mg_table = {
            {'p', mg_pawn_table}, 
            {'n', mg_knight_table},
            {'b', mg_bishop_table},
            {'r', mg_rook_table},
            {'q', mg_queen_table},
            {'k', mg_king_table}
        };

        std::map<char, std::vector<int>> eg_table = {
            {'p', eg_pawn_table}, 
            {'n', eg_knight_table},
            {'b', eg_bishop_table},
            {'r', eg_rook_table},
            {'q', eg_queen_table},
            {'k', eg_king_table}
        };


        std::vector<int> flip = {
                56, 57, 58, 59, 60, 61, 62, 63,
                48, 49, 50, 51, 52, 53, 54, 55,
                40, 41, 42, 43, 44, 45, 46, 47,
                32, 33, 34, 35, 36, 37, 38, 39,
                24, 25, 26, 27, 28, 29, 30, 31,
                16, 17, 18, 19, 20, 21, 22, 23,
                8, 9, 10, 11, 12, 13, 14, 15,
                0, 1, 2, 3, 4, 5, 6, 7
        };

};







PYBIND11_MODULE(cEngine, handle){
    handle.doc() = "Cpp Engine Python Wrapper";

    py::class_<Engine>(
        handle, "cEngine"
    ).def(py::init<std::string>())
    .def("get_color", &Engine::get_color)
    .def("evaluate", &Engine::evaluate)
    .def("make_move", &Engine::make_move)
    ;
}

