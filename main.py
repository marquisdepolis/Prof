import gptcalls
from utilities import load_and_prepare_data, get_financials_for_period
import os
import warnings
import openai
from dotenv import load_dotenv

load_dotenv()
warnings.filterwarnings("ignore")
openai.api_key = os.getenv('OPENAI_API_KEY')

# Database to store user game states
database = {}

class Game:
    def __init__(self, company, date, job_title, financial_data):
        self.company = company
        self.date = date
        self.job_title = job_title
        self.financial_data = financial_data
        self.current_state = None
        self.game_over = False

    def generate_game_state(self):
        income, balance, cashflow = get_financials_for_period(*self.financial_data, self.company, *self.date)
        game_prompt = f"Can you provide a simulated financial and operational overview for {self.company} in {self.date} from the following information and anything else you might know about the company at that time? The company financial statements are: \n{income}\n, {balance}\n, {cashflow}\n"
        print(f"The company financial statements are: \n{income}\n, {balance}\n, {cashflow}")
        game_state = gptcalls.call_gpt(game_prompt)
        return game_state

    def generate_decisions(self):
        decision_prompt = f"Given the state of {self.company} in {self.date}, what are three operational questions that a {self.job_title} could consider?"
        decisions = gptcalls.call_gpt(decision_prompt)
        return decisions

    def simulate_outcome(self, decision):
        outcome_prompt = f"If {self.company} had pursued {decision} in {self.date}, what would be the possible impact on the company's financials and operations?"
        outcome = gptcalls.call_gpt(outcome_prompt)
        return outcome

    def play(self):
        while not self.game_over:
            # Get financials for current period
            self.current_state = self.generate_game_state()
            print("The current state is: " + self.current_state)
            decisions = self.generate_decisions()
            user_decision = input(decisions + "\nInput your decision:")
            predicted_outcome = input("Input your prediction:")
            actual_outcome = self.simulate_outcome(user_decision)
            print(f"Your predicted outcome: {predicted_outcome}\nActual outcome: {actual_outcome}")
            
            save_game(self)

            continue_game = input("Do you want to continue the game? (yes/no)")
            if continue_game.lower() == 'no':
                self.game_over = True
            else:
                self.increment_date()

    def increment_date(self):
        year, quarter = self.date
        if quarter == 4:
            self.date = (year + 1, 1)
        else:
            self.date = (year, quarter + 1)

def save_game(game):
    game_id = f"{game.company}_{game.date}_{game.job_title}"
    database[game_id] = game

def load_game(company, date, job_title):
    game_id = f"{company}_{date}_{job_title}"
    if game_id in database:
        return database[game_id]
    else:
        print("Game not found.")
        return None

def main():
    financial_data = load_and_prepare_data()
    company = input("Enter company ticker: ")
    date = tuple(map(int, input("Enter date (in the format: 2017, 1 for Q1 2017): ").split(', ')))
    job_title = input("Enter your job title: ")

    game = Game(company, date, job_title, financial_data)
    game.play()

if __name__ == "__main__":
    main()