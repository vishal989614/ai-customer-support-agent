from .state import SupportState


def capability_router(
    state: SupportState
) -> str:

    capability = state["capability"]

    return capability