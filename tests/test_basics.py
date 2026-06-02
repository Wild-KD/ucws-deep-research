"""Basic sanity tests for the Investment Research Logic Engine."""
from __future__ import annotations

import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestConfig:
    def test_config_from_env_defaults(self):
        from config import LLMConfig
        cfg = LLMConfig.from_env("anthropic")
        assert cfg.provider == "anthropic"
        assert cfg.model == "claude-sonnet-4-6"

    def test_config_openai(self):
        from config import LLMConfig
        cfg = LLMConfig.from_env("openai")
        assert cfg.provider == "openai"

    def test_config_miromind(self):
        from config import LLMConfig
        cfg = LLMConfig.from_env("miromind")
        assert cfg.provider == "miromind"
        assert "miromind" in cfg.base_url


class TestToolRegistry:
    def test_all_tools_registered(self):
        from tools.registry import TOOL_REGISTRY
        assert "web_search" in TOOL_REGISTRY
        assert "web_fetch" in TOOL_REGISTRY
        assert "pdf_reader" in TOOL_REGISTRY
        assert "html_writer" in TOOL_REGISTRY

    def test_tool_definitions_format(self):
        from tools.registry import get_tool_definitions
        defs = get_tool_definitions()
        assert len(defs) == 4
        for d in defs:
            assert "name" in d
            assert "description" in d
            assert "input_schema" in d

    def test_filter_by_name(self):
        from tools.registry import get_tool_definitions
        defs = get_tool_definitions(["web_search"])
        assert len(defs) == 1
        assert defs[0]["name"] == "web_search"


class TestSkillLoading:
    SKILLS_DIR = Path(__file__).parent.parent / "skills"

    def test_all_skill_dirs_exist(self):
        expected = ["search", "decompose", "verify", "distill-registry", "distill-explore", "merge", "visualize", "dashboard"]
        for name in expected:
            skill_dir = self.SKILLS_DIR / name
            assert skill_dir.exists(), f"Skill directory missing: {name}"

    def test_all_skills_have_md(self):
        for skill_dir in self.SKILLS_DIR.iterdir():
            if skill_dir.is_dir():
                md_files = list(skill_dir.glob("SKILL*.md"))
                assert len(md_files) > 0, f"No SKILL.md in {skill_dir.name}"

    def test_skill_frontmatter(self):
        from runtime.agent import BaseAgent
        skill_path = self.SKILLS_DIR / "search" / "SKILL.md"
        if not skill_path.exists():
            import pytest
            pytest.skip("Skill file not accessible (encoding issue)")
        prompt = BaseAgent._load_skill(skill_path)
        assert len(prompt) > 100
        assert "---" not in prompt[:10]  # frontmatter stripped


class TestLLMFactory:
    def test_create_anthropic(self):
        from config import LLMConfig
        from llm.factory import create_provider
        cfg = LLMConfig(provider="anthropic", api_key="test-key")
        provider = create_provider(cfg)
        assert provider is not None

    def test_create_openai(self):
        from config import LLMConfig
        from llm.factory import create_provider
        cfg = LLMConfig(provider="openai", api_key="test-key")
        provider = create_provider(cfg)
        assert provider is not None

    def test_unknown_provider_raises(self):
        from config import LLMConfig
        from llm.factory import create_provider
        cfg = LLMConfig(provider="unknown", api_key="test")
        try:
            create_provider(cfg)
            assert False, "Should have raised"
        except ValueError:
            pass


class TestDemoFiles:
    DEMO_DIR = Path(__file__).parent.parent / "demo" / "silver"

    def test_all_demo_htmls_exist(self):
        expected = [
            "markmap_guotai.html", "markmap_galaxy.html", "markmap_founder.html",
            "verify_guotai.html", "verify_galaxy.html", "verify_founder.html",
            "merged.html", "dashboard.html",
        ]
        for name in expected:
            assert (self.DEMO_DIR / name).exists(), f"Demo file missing: {name}"

    def test_demo_htmls_have_lang_support(self):
        for html_file in self.DEMO_DIR.glob("*.html"):
            content = html_file.read_text(encoding="utf-8")
            if html_file.name == "distill.html":
                continue
            assert "lang.js" in content, f"{html_file.name} missing lang.js"
