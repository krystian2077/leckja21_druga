"""
Generuje 10 losowych polskich imion i nazwisk oraz 10 losowych zdań
"""

from faker import Faker

fake = Faker('pl_PL')

print("=" * 70)
print("FAKER - Generator losowych danych")
print("=" * 70)
print()

print("📝 10 losowych polskich imion i nazwisk:")
print("-" * 70)
for i in range(1, 11):
    name = fake.name()
    print(f"{i:2}. {name}")

print()
print("-" * 70)
print()

print("💬 10 losowych zdań:")
print("-" * 70)
for i in range(1, 11):
    sentence = fake.sentence()
    print(f"{i:2}. {sentence}")

print()
print("=" * 70)
print("✅ Skrypt zakończony pomyślnie!")
print("=" * 70)

