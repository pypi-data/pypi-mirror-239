from yapygen import generate
from yapygen.meta import get_info


def main() -> None:
    info = get_info()
    generate.main(info)


if __name__ == "__main__":
    main()
