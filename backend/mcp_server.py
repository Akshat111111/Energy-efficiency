from mcp.server.fastmcp import FastMCP
from energy_efficiency_scorecard import EnergyEfficiencyScorecard

# Initialize the FastMCP server
mcp = FastMCP("Energy Efficiency Scorecard MCP")

@mcp.tool()
def calculate_efficiency_score(
    home_size_sqft: float,
    consumption_kwh: float,
    insulation_level: str,
    appliance_efficiency: str
) -> dict:
    """
    Calculate the energy efficiency score (0-100) of a residential home
    along with benchmark rankings and a personalized improvement plan.
    
    Parameters:
    - home_size_sqft: Total interior floor area of the home in square feet.
    - consumption_kwh: Total monthly electricity/energy consumption in kWh.
    - insulation_level: Quality of home insulation. Allowed values: 'poor', 'fair', 'average', 'good', 'excellent'.
    - appliance_efficiency: Average efficiency of large appliances. Allowed values: 'low', 'medium', 'high'.
    
    Returns a dictionary with 'score', 'rating', 'benchmark', and 'improvement_plan'.
    """
    return EnergyEfficiencyScorecard.get_score_and_plan(
        home_size_sqft=home_size_sqft,
        consumption_kwh=consumption_kwh,
        insulation_level=insulation_level,
        appliance_efficiency=appliance_efficiency
    )

if __name__ == "__main__":
    # Runs the MCP server using standard I/O (which is how Claude Desktop communicates with it)
    mcp.run()

