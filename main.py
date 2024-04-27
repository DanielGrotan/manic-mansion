from manic_mansion import Game


def main() -> None:
    game = Game(800, 600)
    game.run(60)


if __name__ == "__main__":
    main()
