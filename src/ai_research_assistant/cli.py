#!/usr/bin/env python3.13
"""
CLI principal para o MCP Server
"""

import sys
from pathlib import Path

from mcp_server.ai_research_assistant import main as assistant_main


def main():
    """Entry point principal"""
    assistant_main()


if __name__ == "__main__":
    main()
