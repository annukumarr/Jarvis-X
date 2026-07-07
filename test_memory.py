from database.memory_db import save_memory, get_memory

save_memory(
    "profile",
    "dream_company",
    "Microsoft"
)

company = get_memory(
    "profile",
    "dream_company"
)

print(company)