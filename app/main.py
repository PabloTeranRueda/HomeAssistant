from app.Orchestrator import Orchestrator


def main() -> None:
    orchestrator = Orchestrator()
    orchestrator.set_listener_on()


if __name__ == "__main__":
    main()