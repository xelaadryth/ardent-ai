from internal.llm import generate_content


class DummyResponse:
    def __init__(self, text):
        self.text = text


class DummyModels:
    def generate_content(self, model, contents, config=None):
        assert model == "m"
        assert contents == "prompt"
        assert config is not None
        return DummyResponse("result")


class DummyClient:
    def __init__(self):
        self.models = DummyModels()


def test_generate_content_forwards_to_client(monkeypatch):
    monkeypatch.setattr("internal.llm.client", DummyClient())

    result = generate_content(prompt="prompt", models=["m"], max_retries=1)

    assert result == "result"
