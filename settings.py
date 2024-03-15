import pygame
import colors

cols = colors.Colors()

class Settings:
    def __init__(self) -> None:
        class Draw_Settings:
            def __init__(self) -> None:
                self.draw_eval_bar = True
                self.draw_stock = False
                self.cell_size = 80
                self.eval_bar_thkness = 40
                self.black_sq_color =  cols.DARK_BROWN
                self.white_sq_color = cols.LIGHT_BROWN
                self.highlight_color = cols.YELLOW

                self.eval_bar_white_col = cols.WHITE
                self.eval_bar_black_col = cols.BLACK

                self.stock_white_col = cols.LIGHT_PURPLE
                self.stock_black_col = cols.DARK_PURPLE
        
        class Engin_Sim_Settings:
            def __init__(self) -> None:
                self.n_games = 10

        self.draw_settings = Draw_Settings()
        self.engine_sim_settings = Engin_Sim_Settings()
    
    def get_draw_settings(self):
        return self.draw_settings
    
    def get_engine_sim_settings(self):
        return self.engine_sim_settings
