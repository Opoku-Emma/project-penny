from src import generate_seed as g_seed

seed_obj = g_seed.SeedGenerator()

seed_obj = seed_obj.get_next_seed()
print(seed_obj)
