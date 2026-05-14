import agent
import run_pipeline


def test_run_pipeline_main_is_agent_main():
    assert run_pipeline.main is agent.main
