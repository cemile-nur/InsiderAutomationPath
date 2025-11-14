from typing import List, Dict, Optional


class Person:
    def __init__(self,
                 first_name: str = "NoFirstName",
                 last_name: str = "NoLastName",
                 age: int = 0,
                 country: str = "NoCountry",
                 city: str = "NoCity",
                 skills: Optional[List[str]] = None):
       
        self._first_name: str = first_name
        self._last_name: str = last_name
        self._age: int = age
        self._country: str = country
        self._city: str = city
        self._skills: List[str] = list(skills) if skills is not None else []

    @property
    def first_name(self) -> str:
        return self._first_name

    @first_name.setter
    def first_name(self, value: str) -> None:
        if not isinstance(value, str):
            raise ValueError("First name must be a string.")
        self._first_name = value.strip()

    @property
    def last_name(self) -> str:
        return self._last_name

    @last_name.setter
    def last_name(self, value: str) -> None:
        if not isinstance(value, str):
            raise ValueError("Last name must be a string.")
        self._last_name = value.strip()

    @property
    def age(self) -> int:
        return self._age

    @age.setter
    def age(self, value: int) -> None:
        if not isinstance(value, int) or value < 0:
            raise ValueError("Age must be a non-negative integer.")
        self._age = value

    @property
    def country(self) -> str:
        return self._country

    @country.setter
    def country(self, value: str) -> None:
        if not isinstance(value, str):
            raise ValueError("Country must be a string.")
        self._country = value.strip()

    @property
    def city(self) -> str:
        return self._city

    @city.setter
    def city(self, value: str) -> None:
        if not isinstance(value, str):
            raise ValueError("City must be a string.")
        self._city = value.strip()

    @property
    def skills(self) -> List[str]:
        
        return list(self._skills)

    def add_skill(self, skill: str) -> None:
        
        if not isinstance(skill, str):
            raise ValueError("Skill must be a string.")
        skill = skill.strip()
        if not skill:
            raise ValueError("Skill cannot be empty.")
        self._skills.append(skill)

    def get_person_info(self) -> Dict[str, object]:
     
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "age": self.age,
            "country": self.country,
            "city": self.city,
            "skills": self.skills
        }

    def __str__(self) -> str:
        skills_str = ", ".join(self._skills) if self._skills else "None"
        return (f"Name: {self.first_name} {self.last_name}\n"
                f"Age: {self.age}\n"
                f"Location: {self.country}, {self.city}\n"
                f"Skills: {skills_str}")


def main():
    person = Person(first_name="John", last_name="Doe", age=30, country="USA", city="New York")

    person.add_skill("Riding a bike")
    person.add_skill("Python programming")

    info = person.get_person_info()
    print("--- Person Information ---")
    for key, value in info.items():
        if key == "skills":
            print(f"{key.capitalize()}: {', '.join(value) if value else 'None'}")
        else:
            print(f"{key.capitalize()}: {value}")

    print("\n(Summary)")
    print(person)


if __name__ == "__main__":
    main()
