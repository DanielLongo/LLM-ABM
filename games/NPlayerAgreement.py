from typing import List, Dict, Callable
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    HumanMessage,
    SystemMessage,
)

import sys
sys.path.append("..")
from BetterAgents import DialogueAgent, DialogueSimulator

num_players = 3
max_iters = 8
word_limit = 50
player_names = ["Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Heidi", "Ivan", "Judy", "Kevin", "Larry", "Mallory", "Nancy", "Olivia", "Peggy", "Quentin", "Rupert", "Sybil", "Trent", "Ursula", "Victor", "Walter", "Xavier", "Yvonne", "Zelda"]
dilemia = "Should we allow in more immgrants from Mexico?"

game_description = f"""Here is the topic for a negotation between {num_players} people. The dilemma is: {dilemia}."""

player_descriptor_system_message = SystemMessage(
    content="You can add detail to the description of an individual in a negotiation."
)

player_specifier_prompts = []

for i in range(num_players):
    player_specifier_prompts.append([
        player_descriptor_system_message,
        HumanMessage(content=
            f"""{game_description}
            Please reply with a creative description of the player, {player_names[i]}, in {word_limit} words or less.
            Speak directly to {player_names[i]}.
            Do not add anything else."""
            )
    ])

player_descriptions = [ChatOpenAI(temperature=1.0)(player_specifier_prompts[i]).content for i in range(num_players)]

for i in range(num_players):
    print(f'{player_names[i]} Description:')
    print(player_descriptions[i])

player_system_messages = []
for i in range(num_players):
    player_system_messages.append(SystemMessage(content=(
    f"""{game_description}
    Never forget you are {player_names[i]}. 
    Your character description is as follows: {player_descriptions[i]}.
    Speak in the first person from the perspective of {player_names[i]}.
    For describing your own body movements, wrap your description in '*'.
    If the whole have reached a decision, type 'we have reached a decision' followed by the resolution.
    Do not change roles!
    """)))

agents = [DialogueAgent(name=player_names[i], system_message=player_system_messages[i], model=ChatOpenAI(temperature=.2)) for i in range(num_players)]

def select_next_speaker(step: int, agents: List[DialogueAgent]) -> int:
    return step % len(agents)


simulator = DialogueSimulator(agents=agents, selection_function=select_next_speaker)

simulator.reset()
simulator.inject(agents[0], "Let us begin discussing the dilemma: {dilemia}.")
for i in range(max_iters):
    name, message = simulator.step()
    print(f'{name}: {message}')
    print('\n')
    if "we have reached a decision" in message.lower():
        break