from statemachine import State, StateMachine

def BurgerFSM(StateMachine):
    raw = State('Raw', initial=True)
    cooking = State('Cooking')
    cooked = State('Cooked')
    burnt = State('Burnt')

    start_cooking = raw.to(cooking)
    finish_cooking = cooking.to(cooked)
    burnt_cooking = cooked.to(burnt)

    def place_on_stove(self):
        if self.cooking_fsm.is_raw:
            self.cooking_fsm.start_cooking()

    def update_cooking(self):
        if self.cooking_fsm.is_cooking:
            # Simulate cooking process, update cooking time, etc.
            # Check if the patty is now cooked or burnt
            if self.is_done_cooking():
                self.cooking_fsm.finish_cooking()

    def is_done_cooking(self):
        # Replace this with your own logic to determine if the patty is cooked or burnt
        return True