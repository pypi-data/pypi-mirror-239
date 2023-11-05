from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin

from d2.block import Renderer
from d2.config import PluginConfig


class Plugin(BasePlugin[PluginConfig]):
    def on_config(self, config: MkDocsConfig) -> MkDocsConfig | None:
        markdown_extensions = config.setdefault("markdown_extensions", [])
        for ext in {"pymdownx.superfences", "attr_list", "d2_img"}:
            if ext not in markdown_extensions:
                markdown_extensions.append(ext)

        mdx_configs = config.setdefault("mdx_configs", {})

        superfences = mdx_configs.setdefault("pymdownx.superfences", {})
        custom_fences = superfences.setdefault("custom_fences", [])
        f = Renderer(self.config)
        custom_fences.append(
            {
                "name": "d2",
                "class": "d2",
                "validator": f.validator,
                "format": f.formatter,
            }
        )

        mdx_configs["d2_img"] = {
            "base_dir": config.docs_dir,
            "plugin_config": self.config,
        }

        return config
