# import csv
# import random
#
#
# class Industry:
#     def __init__(self, name, sector, emissions_by_year, production_output, emission_reduction_measures,
#                  future_expansion_plans, technological_infrastructure, carbon_intensity, compliance_history):
#         self.name = name
#         self.sector = sector
#         self.emissions_by_year = emissions_by_year
#         self.production_output = production_output
#         self.emission_reduction_measures = emission_reduction_measures
#         self.future_expansion_plans = future_expansion_plans
#         self.technological_infrastructure = technological_infrastructure
#         self.carbon_intensity = carbon_intensity
#         self.compliance_history = compliance_history
#
#     def calculate_current_emissions(self, year):
#         return self.emissions_by_year[year] + (self.production_output * self.carbon_intensity)
#
#     def alert_if_crossing_limit(self, emission_limit, year):
#         current_emissions = self.calculate_current_emissions(year)
#         if current_emissions > emission_limit:
#             return f"Alert: {self.name} has crossed emission limit in {year}. Current emissions: {current_emissions} tons."
#         else:
#             return f"{self.name} is within emission limits in {year}. Current emissions: {current_emissions} tons."
#
#
# # Simulated data generation for each industry
# def generate_emissions(years):
#     return {year: random.randint(5000, 20000) for year in years}
#
#
# years = range(2012, 2023)
#
# electronics_manufacturing = Industry(
#     name="Electronics Inc.",
#     sector="Electronics Manufacturing",
#     emissions_by_year=generate_emissions(years),
#     production_output=random.randint(1000, 5000),  # units
#     emission_reduction_measures=["Implementation of energy-efficient processes", "Waste recycling initiatives"],
#     future_expansion_plans="Expansion of manufacturing facilities",
#     technological_infrastructure="Advanced",
#     carbon_intensity=random.uniform(1.5, 2.5),  # tons per unit
#     compliance_history="Good"
# )
#
# power_generation = Industry(
#     name="PowerGen Corp.",
#     sector="Power Generation",
#     emissions_by_year=generate_emissions(years),
#     production_output=random.randint(5000, 10000),  # units
#     emission_reduction_measures=["Transition to cleaner energy sources", "Installation of emission control systems"],
#     future_expansion_plans="Investment in renewable energy projects",
#     technological_infrastructure="Moderate",
#     carbon_intensity=random.uniform(0.8, 1.2),  # tons per unit
#     compliance_history="Average"
# )
#
# transportation = Industry(
#     name="Transit Solutions Ltd.",
#     sector="Transportation",
#     emissions_by_year=generate_emissions(years),
#     production_output=random.randint(200, 500),  # vehicles
#     emission_reduction_measures=["Fleet modernization with fuel-efficient vehicles", "Promotion of public transit"],
#     future_expansion_plans="Expansion of vehicle fleet",
#     technological_infrastructure="Advanced",
#     carbon_intensity=random.uniform(5, 10),  # tons per vehicle
#     compliance_history="Good"
# )
#
# aerospace = Industry(
#     name="Skyward Aerospace",
#     sector="Aerospace",
#     emissions_by_year=generate_emissions(years),
#     production_output=random.randint(100, 500),  # aircraft
#     emission_reduction_measures=["Development of more fuel-efficient aircraft",
#                                  "Investment in sustainable aviation fuels"],
#     future_expansion_plans="Expansion of aircraft manufacturing capacity",
#     technological_infrastructure="Cutting-edge",
#     carbon_intensity=random.uniform(20, 30),  # tons per aircraft
#     compliance_history="Good"
# )
#
# automotive_manufacturing = Industry(
#     name="AutoWorks Ltd.",
#     sector="Automotive Manufacturing",
#     emissions_by_year=generate_emissions(years),
#     production_output=random.randint(1000, 5000),  # vehicles
#     emission_reduction_measures=["Adoption of electric vehicle technology", "Implementation of lean manufacturing"],
#     future_expansion_plans="Introduction of new vehicle models",
#     technological_infrastructure="Modern",
#     carbon_intensity=random.uniform(2, 5),  # tons per vehicle
#     compliance_history="Good"
# )
#
# # Create a list of industries
# industries = [electronics_manufacturing, power_generation, transportation, aerospace, automotive_manufacturing]
#
# # Write simulated data to CSV file
# with open('carbon_credits_data.csv', mode='w', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerow(['Year', 'Industry Name', 'Sector', 'Emissions', 'Production Output',
#                      'Emission Reduction Measures', 'Future Expansion Plans',
#                      'Technological Infrastructure', 'Carbon Intensity', 'Compliance History'])
#
#     for year in years:
#         for industry in industries:
#             writer.writerow([year, industry.name, industry.sector, industry.emissions_by_year[year],
#                              industry.production_output, industry.emission_reduction_measures,
#                              industry.future_expansion_plans, industry.technological_infrastructure,
#                              industry.carbon_intensity, industry.compliance_history])
#
#


import csv
import random

class Industry:
    def __init__(self, name, sector, emissions_by_year, production_output, emission_reduction_measures,
                 future_expansion_plans, technological_infrastructure, carbon_intensity, compliance_history,
                 emission_limit):
        self.name = name
        self.sector = sector
        self.emissions_by_year = emissions_by_year
        self.production_output = production_output
        self.emission_reduction_measures = emission_reduction_measures
        self.future_expansion_plans = future_expansion_plans
        self.technological_infrastructure = technological_infrastructure
        self.carbon_intensity = carbon_intensity
        self.compliance_history = compliance_history
        self.emission_limit = emission_limit

    def calculate_current_emissions(self, year):
        return self.emissions_by_year[year] + (self.production_output * self.carbon_intensity)

    def alert_if_crossing_limit(self, year):
        current_emissions = self.calculate_current_emissions(year)
        if current_emissions > self.emission_limit:
            return f"Alert: {self.name} has crossed emission limit in {year}. Current emissions: {current_emissions} tons."
        else:
            return f"{self.name} is within emission limits in {year}. Current emissions: {current_emissions} tons."

def generate_emissions(years):
    return {year: random.randint(5000, 20000) for year in years}

# Define emission limits for each industry
emission_limits = {
    "Electronics Inc.": 30000,
    "PowerGen Corp.": 50000,
    "Transit Solutions Ltd.": 15000,
    "Skyward Aerospace": 70000,
    "AutoWorks Ltd.": 40000
}

years = range(2012, 2023)

electronics_manufacturing = Industry(
    name="Electronics Inc.",
    sector="Electronics Manufacturing",
    emissions_by_year=generate_emissions(years),
    production_output=random.randint(1000, 5000),  # units
    emission_reduction_measures=["Implementation of energy-efficient processes", "Waste recycling initiatives"],
    future_expansion_plans="Expansion of manufacturing facilities",
    technological_infrastructure="Advanced",
    carbon_intensity=random.uniform(1.5, 2.5),  # tons per unit
    compliance_history="Good",
    emission_limit=emission_limits["Electronics Inc."]
)

power_generation = Industry(
    name="PowerGen Corp.",
    sector="Power Generation",
    emissions_by_year=generate_emissions(years),
    production_output=random.randint(5000, 10000),  # units
    emission_reduction_measures=["Transition to cleaner energy sources", "Installation of emission control systems"],
    future_expansion_plans="Investment in renewable energy projects",
    technological_infrastructure="Moderate",
    carbon_intensity=random.uniform(0.8, 1.2),  # tons per unit
    compliance_history="Average",
    emission_limit=emission_limits["PowerGen Corp."]
)

transportation = Industry(
    name="Transit Solutions Ltd.",
    sector="Transportation",
    emissions_by_year=generate_emissions(years),
    production_output=random.randint(200, 500),  # vehicles
    emission_reduction_measures=["Fleet modernization with fuel-efficient vehicles", "Promotion of public transit"],
    future_expansion_plans="Expansion of vehicle fleet",
    technological_infrastructure="Advanced",
    carbon_intensity=random.uniform(5, 10),  # tons per vehicle
    compliance_history="Good",
    emission_limit=emission_limits["Transit Solutions Ltd."]
)

aerospace = Industry(
    name="Skyward Aerospace",
    sector="Aerospace",
    emissions_by_year=generate_emissions(years),
    production_output=random.randint(100, 500),  # aircraft
    emission_reduction_measures=["Development of more fuel-efficient aircraft",
                                 "Investment in sustainable aviation fuels"],
    future_expansion_plans="Expansion of aircraft manufacturing capacity",
    technological_infrastructure="Cutting-edge",
    carbon_intensity=random.uniform(20, 30),  # tons per aircraft
    compliance_history="Good",
    emission_limit=emission_limits["Skyward Aerospace"]
)

automotive_manufacturing = Industry(
    name="AutoWorks Ltd.",
    sector="Automotive Manufacturing",
    emissions_by_year=generate_emissions(years),
    production_output=random.randint(1000, 5000),  # vehicles
    emission_reduction_measures=["Adoption of electric vehicle technology", "Implementation of lean manufacturing"],
    future_expansion_plans="Introduction of new vehicle models",
    technological_infrastructure="Modern",
    carbon_intensity=random.uniform(2, 5),  # tons per vehicle
    compliance_history="Good",
    emission_limit=emission_limits["AutoWorks Ltd."]
)

# Create a list of industries
industries = [electronics_manufacturing, power_generation, transportation, aerospace, automotive_manufacturing]

# Write simulated data to CSV file
with open('carbon_credits_data.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Year', 'Industry Name', 'Sector', 'Emissions', 'Production Output',
                     'Emission Reduction Measures', 'Future Expansion Plans',
                     'Technological Infrastructure', 'Carbon Intensity', 'Compliance History',
                     'Emission Limit'])

    for year in years:
        for industry in industries:
            writer.writerow([year, industry.name, industry.sector, industry.emissions_by_year[year],
                             industry.production_output, industry.emission_reduction_measures,
                             industry.future_expansion_plans, industry.technological_infrastructure,
                             industry.carbon_intensity, industry.compliance_history, industry.emission_limit])
