# Bước 1: Viết hàm so sánh 2 từ xem có ok không
import typer

from game import Game

# Hàm này kiểm tra xem list thứ hai có là tập con của list thứ nhất
app = typer.Typer()
game = Game()


@app.command()
def welcome():
    game.welcome()


@app.command()
def longest_word(game_mode: str, input_str: str,
                 missing_limit: int = typer.Option(0, "--missing-limit", "-m"),
                 output_limit: int = typer.Option(5, "--output-limit", "-o")):
    game.longest_word(game_mode, input_str, missing_limit, output_limit)


@app.command()
def word_master(game_mode: str,
                pattern: str,
                available: str,
                missing: str = typer.Option("", "--missing", "-m")):
    game.word_master(game_mode, pattern, available, missing)


# Tìm từ khóa cho trước dựa vào input
@app.command()
def mutant_word(input_str: str):
    game.mutant_word(input_str)


# Bước 2: Viết chương trình cho phép input các ký tự đang có, và trả về các từ dài nhất
if __name__ == '__main__':
    app()
