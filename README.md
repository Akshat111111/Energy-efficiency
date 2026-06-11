# Energy Efficiency Scorecard & MCP Server Integration

This repository contains a Python-based energy efficiency scorecard service that has been adapted to run as a Model Context Protocol (MCP) server. This allows AI assistants like Claude to interact with the scorecard's scoring and analysis features natively as tools.

This example follows the [Expose MCP (Python) quick-start guide](https://academy.graftcode.com/quick-start/expose-mcp/python) on the GraftCode Academy.




<img width="1306" height="842" alt="energy scorecard" src="https://github.com/user-attachments/assets/d5fa6f92-b690-453f-b2ba-76aa74582944" />
<img width="1912" height="1137" alt="energy scorecard 4" src="https://github.com/user-attachments/assets/3b8f737f-88cf-4337-a9c4-fdae6e4242a0" />
<img width="1917" height="1137" alt="energy scorecard 3" src="https://github.com/user-attachments/assets/218a1fdc-d8af-4bc2-b19c-80922ba000f0" />
<img width="1902" height="1132" alt="energy scorecard 2" src="https://github.com/user-attachments/assets/90973a0c-adb0-4645-b728-6de7a537123e" />



## What we did

### 1. Created the Energy
Efficiency Scorecard
- Created `energy_efficiency_scorecard.py` containing the `EnergyEfficiencyScorecard` class.
- Implemented a 0–100 scoring algorithm evaluating:
  - **Consumption Density** (kWh/month per sqft vs. a typical regional density of 1.0)
  - **Insulation Quality** (poor, fair, average, good, excellent)
  - **Appliance Efficiency** (low, medium, high)
- Generated benchmarking metrics showing how the home ranks against similar-sized homes.
- Compiled a personalized, actionable improvement plan suggesting specific upgrades (insulation, sealing, smart thermostats, LEDs, appliances, solar panels).

### 2. Created the MCP Server
- Installed the official Anthropic `mcp` SDK package (`pip install mcp`).
- Created `mcp_server.py`, which uses `FastMCP` to expose the scorecard methods as an accessible tool (`calculate_efficiency_score`).

---

## How to use

### Setup (one-time)

Create and activate a Python virtual environment, then install dependencies:

**macOS / Linux:**
```bash
cd py-ai-backend

# Create the virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install the MCP SDK (needed for the MCP server)
pip install mcp
```

**Windows (PowerShell):**
```powershell
cd py-ai-backend
python -m venv venv
venv\Scripts\Activate.ps1
pip install mcp
```

To leave the virtual environment later, run `deactivate`.

**Running the scorecard directly:**
```bash
# Make sure the venv is activated first
python energy_efficiency_scorecard.py
```

**Using with Claude:**
Once configured, you can open Claude and ask questions like:
- *"Calculate my energy scorecard: 1800 sq ft home, 900 kWh monthly, poor insulation, and high appliance efficiency."*
- *"Based on my efficiency rating, what is my improvement plan?"*

Claude will automatically call the local MCP tool to fetch the score, rating letter, benchmark, and tips.

---

### Alternative Workflow: Containerized with GraftCode Gateway
Instead of running a local `mcp_server.py` file, you can achieve the exact same integration using Docker and a remote MCP gateway.

1. **Start the environment:** Run your `Dockerfile` alongside the GraftCode gateway, which exposes the service on `http://localhost:81/mcp`.
2. **Update Claude Config:** In `claude_desktop_config.json`, configure the server to connect remotely via `npx` and `mcp-remote`:

```json
    "energy-service": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "http://localhost:81/mcp"
      ]
    }
```
This containerized approach allows Claude to access the scorecard tools over the network (via the GraftCode gateway) without needing to write or maintain separate local Python MCP server scripts!
