from fastapi import FastAPI

test_app = FastAPI()


@test_app.get("/test-only")
def only_in_tests():
    return {"test": True}


def test_only_in_tests():
    assert only_in_tests() == {"test": True}
