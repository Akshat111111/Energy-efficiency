class EnergyEfficiencyScorecard:
    @staticmethod
    def get_score_and_plan(home_size_sqft: float, consumption_kwh: float, insulation_level: str, appliance_efficiency: str) -> dict:
        home_size_sqft = float(home_size_sqft)
        consumption_kwh = float(consumption_kwh)
        insulation_level = str(insulation_level).lower().strip()
        appliance_efficiency = str(appliance_efficiency).lower().strip()

        if home_size_sqft <= 0:
            raise ValueError("Home size must be greater than 0.")
        if consumption_kwh < 0:
            raise ValueError("Consumption cannot be negative.")

        # 1. Consumption Density Component (Max 40 points)
        # Regional average is ~1.0 kWh/sqft/month
        consumption_density = consumption_kwh / home_size_sqft
        
        # density <= 0.4 -> 40 points (extremely efficient)
        # density >= 2.0 -> 0 points (highly inefficient)
        if consumption_density <= 0.4:
            density_score = 40.0
        elif consumption_density >= 2.0:
            density_score = 0.0
        else:
            # Linear scale between 0.4 and 2.0
            density_score = 40.0 * (1.0 - (consumption_density - 0.4) / 1.6)

        # 2. Insulation Level Component (Max 30 points)
        insulation_scores = {
            "poor": 6.0,
            "fair": 12.0,
            "average": 18.0,
            "good": 24.0,
            "excellent": 30.0
        }
        if insulation_level not in insulation_scores:
            raise ValueError("Insulation level must be one of: poor, fair, average, good, excellent.")
        insulation_score = insulation_scores[insulation_level]

        # 3. Appliance Efficiency Component (Max 30 points)
        appliance_scores = {
            "low": 10.0,
            "medium": 20.0,
            "high": 30.0
        }
        if appliance_efficiency not in appliance_scores:
            raise ValueError("Appliance efficiency must be one of: low, medium, high.")
        appliance_score = appliance_scores[appliance_efficiency]

        # Total Score calculation
        total_score = round(density_score + insulation_score + appliance_score)
        total_score = max(0, min(100, total_score))

        # Determine Rating letter
        if total_score >= 90:
            rating = "A (Highly Efficient)"
        elif total_score >= 80:
            rating = "B (Efficient)"
        elif total_score >= 70:
            rating = "C (Average)"
        elif total_score >= 50:
            rating = "D (Below Average)"
        else:
            rating = "F (Inefficient)"

        # 4. Benchmark against similar homes
        # Comparison with typical target of 1.0 kWh/sqft/month
        target_density = 1.0
        percent_diff = ((consumption_density - target_density) / target_density) * 100.0
        
        if percent_diff > 0:
            comparison_phrase = f"Your home consumes {consumption_density:.2f} kWh/sqft, which is {percent_diff:.1f}% higher than the typical average home of similar size."
        else:
            comparison_phrase = f"Your home consumes {consumption_density:.2f} kWh/sqft, which is {abs(percent_diff):.1f}% lower (more efficient) than the typical average home of similar size."

        # 5. Personalized Improvement Plan
        improvement_plan = []

        if insulation_level in ["poor", "fair"]:
            improvement_plan.append("Upgrade Insulation: Adding insulation to your attic and exterior walls can reduce heating/cooling waste by up to 15%.")
            improvement_plan.append("Seal Air Leaks: Apply weatherstripping and caulk around windows, doors, and plumbing penetrations to block drafts.")
        
        if appliance_efficiency == "low":
            improvement_plan.append("Replace Old Appliances: Upgrade older, energy-hungry appliances (especially your HVAC system, water heater, or refrigerator) to Energy Star certified models.")
        elif appliance_efficiency == "medium":
            improvement_plan.append("Optimize Appliances: Clean refrigerator coils, replace HVAC air filters monthly, and use eco modes on your dishwasher/washing machine.")

        if consumption_density > 1.2:
            improvement_plan.append("Install Smart Thermostat: Optimize heating and cooling schedules to automatically conserve energy when sleeping or away.")
            improvement_plan.append("Transition to LEDs: Replace any remaining legacy incandescent or halogen light bulbs with high-efficiency LEDs.")

        if total_score < 50:
            improvement_plan.append("Professional Audit: Schedule an official home energy audit to run a blower-door test and identify major thermal losses.")
        elif total_score >= 85:
            improvement_plan.append("Solar & Storage: Your home is prime for solar integration. Consider installing rooftop panels and a home battery backup system to move toward net-zero.")

        # Default fallback tip
        if not improvement_plan:
            improvement_plan.append("Keep it up: Monitor your seasonal energy usage to maintain your high efficiency score.")

        return {
            "score": total_score,
            "rating": rating,
            "benchmark": {
                "density_kwh_per_sqft": round(consumption_density, 3),
                "national_average_density": target_density,
                "comparison": comparison_phrase
            },
            "improvement_plan": improvement_plan
        }


if __name__ == "__main__":
    import json
    
    # Run a sample calculation
    print("--- Energy Efficiency Scorecard Simulator ---")
    sample_result = EnergyEfficiencyScorecard.get_score_and_plan(
        home_size_sqft=2000,
        consumption_kwh=1600,
        insulation_level="fair",
        appliance_efficiency="medium"
    )
    print(json.dumps(sample_result, indent=2))
