from dataclasses import dataclass
from typing import override
from app.actions.AbstractAction import AbstractAction
import csv

@dataclass
class AddToShoppingListAction(AbstractAction):
    items_list:list[str]
    
    @property
    @override
    def action_type(self) -> str:
        return "add_to_shoppinglist"

    @override
    def param_dict(self) -> dict[str, object]:
        param_dict:dict[str, object] = super().param_dict()
        param_dict["items_list"] = self.items_list
        return param_dict

    @override
    def run(self) -> None:
        #TODO Create call to BBDD actions api
        # Below is dummy action
        with open(r"resources/shopping_list.csv", mode="r+", newline="", encoding="utf-8") as shopping_list:
            existing_items = shopping_list.read().splitlines()
            writer = csv.writer(shopping_list)
            for item in self.items_list:
                if item not in existing_items:
                    writer.writerow([item])