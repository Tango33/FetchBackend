from flask import Flask, jsonify, request
from bisect import insort
from collections import deque

app = Flask(__name__)

# In-memory databases to store user point transactions and balance.
# Ideally, for a production system, a persistent database system should be used.
transactions = deque()
balance = {}


class SpentPointsHelper:
    """
    Helper class for managing points deduction during spending.
    """

    def __init__(self):
        """
        Initialize an empty dictionary to track points subtracted from each payer.
        """
        self.subtracted_points = {}

    def subtract_points(self, payer, points_to_subtract):
        """
        Deduct a specified number of points from a payer's total.

        Args:
            payer (str): Name of the payer.
            points_to_subtract (int): Amount of points to be subtracted.
        """
        if payer in self.subtracted_points:
            self.subtracted_points[payer] -= points_to_subtract
        else:
            self.subtracted_points[payer] = -points_to_subtract

    def get_subtracted_points_for_payers(self):
        """
        Retrieve a list of payers and their formatted subtracted points.

        Returns:
            list: A list of dictionaries with payer names and their formatted subtracted points.
        """
        return [{"payer": payer, "points": "{:,.0f}".format(points)} for payer, points in
                self.subtracted_points.items()]


def spend_user_points(points):
    """
    Spend user's points based on specified rules.
    The rules are:
    1. Spend the oldest points first.
    2. No payer's points should go negative.

    Args:
        points (int): The total number of points the user wishes to spend.

    Returns:
        list: A list of dictionaries detailing the points deducted from each payer.
    """
    points_to_subtract = points
    spent_points_helper = SpentPointsHelper()

    # Continue processing until all points are spent or no transactions remain.
    while transactions and points_to_subtract > 0:
        timestamp, transaction = transactions[0]

        # Check if the entire transaction can be used up.
        if transaction["points"] <= points_to_subtract:
            points_to_subtract -= transaction["points"]
            spent_points_helper.subtract_points(transaction["payer"], transaction["points"])
            balance[transaction["payer"]] -= transaction["points"]  # Deduct from the global balance.
            transactions.popleft()  # Remove the transaction once processed.
        else:
            # If only a part of the transaction is used.
            spent_points_helper.subtract_points(transaction["payer"], points_to_subtract)
            balance[transaction["payer"]] -= points_to_subtract
            transaction["points"] -= points_to_subtract
            points_to_subtract = 0

    return spent_points_helper.get_subtracted_points_for_payers()


def subtract_points_from_payer_balances(spent_points_helper):
    """
    Adjust the global balance based on deducted points.

    Args:
        spent_points_helper (SpentPointsHelper): An instance containing deducted points data.
    """
    for payer, points in spent_points_helper.subtracted_points.items():
        balance[payer] += points  # Update the balance (since points are stored as negative values).


@app.route('/add', methods=['POST'])
def add_points():
    """
    Endpoint to add points for a user. Adds points to the in-memory transaction and balance.

    :return: HTTP Response
    """
    data = request.get_json()
    payer = data['payer']
    points = data['points']
    timestamp = data['timestamp']

    transaction_detail = {'payer': payer, 'points': points, 'timestamp': timestamp}

    # Insert the transaction in its correct position to keep the list sorted
    insort(transactions, (timestamp, transaction_detail))

    if payer in balance:
        balance[payer] += points
    else:
        balance[payer] = points

    return '', 200


@app.route('/spend', methods=['POST'])
def spend_points():
    """
    Endpoint to spend user's points. Utilizes the spend_user_points function.

    :return: JSON response with details of points spent from each payer.
    """
    points_to_spend = request.json["points"]
    if points_to_spend > sum(balance.values()):
        return "User doesn't have enough points", 400
    spent = spend_user_points(points_to_spend)
    return jsonify(spent), 200


@app.route('/balance', methods=['GET'])
def get_balance():
    """
    Endpoint to get the current balance of points per payer for the user.

    :return: JSON response with payer-wise balance.
    """
    return jsonify(balance), 200


if __name__ == '__main__':
    # Starts the Flask application on port 8000
    app.run(port=8000)
