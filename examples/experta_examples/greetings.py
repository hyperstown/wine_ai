from experta import Fact, KnowledgeEngine, Rule, DefFacts, MATCH

class Greetings(KnowledgeEngine):
    @DefFacts()
    def _initial_action(self):
        yield Fact(user="okabe")
        yield Fact(user="kurisu", occupation="scientist")

    @Rule(Fact(user='okabe'))
    def user_is_okabe(self):
        print("User is okabe")


    @Rule(Fact(action='kurisu', occupation=MATCH.occupation))
    def user_is_kurisu(self, occupation):
        print("User is kurisu. Her job title is", occupation)

engine = Greetings()
engine.reset()  # Prepare the engine for the execution.
engine.run()  # Run it!