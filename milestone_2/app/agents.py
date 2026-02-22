from dataclasses import dataclass, field
from typing import Dict, List, Optional

@dataclass
class Agent:
    agent_id: str
    skills: Dict[str, float]  # e.g., {"Technical": 0.9, "Billing": 0.1}
    capacity: int = 5
    current_load: int = 0

    def has_capacity(self) -> bool:
        return self.current_load < self.capacity

    def assign(self):
        self.current_load += 1

    def release(self):
        if self.current_load > 0:
            self.current_load -= 1


class AgentRegistry:
    def __init__(self):
        self.agents: List[Agent] = []

    def register_agent(self, agent: Agent):
        self.agents.append(agent)

    def assign_agent_for_category(self, category: str) -> Optional[Agent]:
        """
        Return the best available agent based on skill match and available capacity.
        """
        candidates = [a for a in self.agents if a.has_capacity()]
        if not candidates:
            return None
        # score by skill weight for category (default 0)
        scored = sorted(candidates, key=lambda a: a.skills.get(category, 0), reverse=True)
        best = scored[0]
        if best.skills.get(category, 0) == 0:
            # no agent has explicit skill for this category
            return None
        best.assign()
        return best


# Helper to create a small sample registry (used by worker)
def sample_register_agents(registry: AgentRegistry):
    registry.register_agent(Agent(agent_id="agent_1", skills={"Technical": 0.9, "Billing": 0.1}, capacity=3))
    registry.register_agent(Agent(agent_id="agent_2", skills={"Billing": 0.9, "Legal": 0.2}, capacity=2))
    registry.register_agent(Agent(agent_id="agent_3", skills={"Legal": 0.8, "Technical": 0.3}, capacity=2))

