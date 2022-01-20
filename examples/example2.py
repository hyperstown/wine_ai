from random import choice
from experta import Fact, KnowledgeEngine, Rule, L, AS, Field, DefFacts, NOT, W, MATCH

class Greetings(KnowledgeEngine):
    @DefFacts()
    def _initial_action(self):
        yield Fact(user="okabe")
        yield Fact(action="abort", reason="Kurisu")

    @Rule(Fact(user='okabe'))
    def aborting(self):
        print("Aborting program. Reason:")


    @Rule(Fact(action='abort', reason=MATCH.reason))
    def greet(self, reason):
        print("Aborting program. Reason:", reason)

engine = Greetings()
engine.reset()  # Prepare the engine for the execution.
engine.run()  # Run it!