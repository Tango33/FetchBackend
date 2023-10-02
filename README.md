# Points System API

Manage users' points based on different payers. Users can accumulate points from various payers, spend them, and check their balance. The points from earlier transactions are spent first, and a payer's points do not go negative.

## Features

- Add points to a user's account from a specific payer with a timestamp.
- Spend points from the oldest transactions first.
- Get the balance of points per payer.

## Requirements

- Python 3.6 or newer
- Flask

## Setup and Installation

### Python Installation

If you don't have Python installed, download it from the [official website](https://www.python.org/downloads/) and install.

### Install Flask

```bash
pip install flask
```

### Download the Application

Clone this repository or download the `points_api.py` file.

## Running the Application

Navigate to the directory where `points_api.py` is saved and execute:

```bash
python3 points_api.py
```

The API will start, and you can access it at [http://localhost:8000](http://localhost:8000).

## API Endpoints

### Add Points

- **URL**: `/add`
- **Method**: `POST`
- **Data Params**:
  ```json
  {
    "payer": "PAYER_NAME",
    "points": POINTS,
    "timestamp": "YYYY-MM-DDTHH:MM:SSZ"
  }
  ```
- **Success Response**:
  - **Code**: 200

### Spend Points

- **URL**: `/spend`
- **Method**: `POST`
- **Data Params**:
  ```json
  {
    "points": POINTS_TO_SPEND
  }
  ```
- **Success Response**:
  - **Code**: 200
  - **Content**:
    ```json
    [
      {"payer": "PAYER_NAME", "points": -SPENT_POINTS},
      ...
    ]
    ```

### Get Balance

- **URL**: `/balance`
- **Method**: `GET`
- **Success Response**:
  - **Code**: 200
  - **Content**:
    ```json
    {
      "PAYER_NAME": BALANCE_POINTS,
      ...
    }
    ```

## Testing

To ensure the system's reliability and correctness, a testing suite is provided. Navigate to the directory containing `test_points_api.py` and execute:

```bash
python3 test_points_api.py
```

You should see an output indicating the number of tests run and their results.
