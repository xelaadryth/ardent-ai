import llm_client


class DummyResponse:
    def __init__(self, text):
        self.text = text


class DummyModels:
    def generate_content(self, model, contents):
        assert model == "m"
        assert contents == "prompt"
        return DummyResponse("result")


class DummyClient:
    def __init__(self):
        self.models = DummyModels()


def test_generate_content_forwards_to_client(monkeypatch):
    monkeypatch.setattr(llm_client, "client", DummyClient())

    result = llm_client.generate_content(models=["m"], prompt="prompt")

    assert result == "result"
