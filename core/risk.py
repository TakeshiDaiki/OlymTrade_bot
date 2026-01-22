class RiskManager:
    def __init__(self, loss_limit):
        """
        Initializes the risk management.
        :param loss_limit: Maximum number of losses allowed before stopping.
        """
        self.loss_limit = loss_limit
        self.current_losses = 0

    def register_result(self, result):
        """
        Updates the loss counter and checks if the bot should continue.
        :param result: String "WIN" or "LOSS"
        :return: Boolean (True if we can keep trading, False if limit reached)
        """
        if result == "LOSS":
            self.current_losses += 1

        # If current losses reach or exceed the limit, stop the bot
        if self.current_losses >= self.loss_limit:
            return False

        return True

    def reset_losses(self):
        """Resets the counter if you start a new session."""
        self.current_losses = 0