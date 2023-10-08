from abc import ABC, abstractmethod


class Chain(ABC):
    def __init__(self):
        self.module = "Chain"

    @abstractmethod
    def run(self,
             prompt_templates,
             input,
             kernel):
        pass
