from fastapi import FastAPI

app = FastAPI()

from fastapi import FastAPI, HTTPException

app = FastAPI()

# In-memory database for users
users = {
    "faqeha": {"pin_number": "1234", "bank_balance": 10000},
    "Laiba": {"pin_number": "5678", "bank_balance": 5000},
    "Annie": {"pin_number": "1111", "bank_balance": 2000},
}

@app.get("/authenticate")
async def authenticate(name: str, pin_number: str):
    user = users.get(name)
    if not user or user["pin_number"] != pin_number:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"name": name, "bank_balance": user["bank_balance"]}

@app.post("/bank-transfer")
async def bank_transfer(sender_name: str, sender_pin: str, recipient_name: str, amount: float):
    # Authenticate sender
    sender = users.get(sender_name)
    if not sender or sender["pin_number"] != sender_pin:
        raise HTTPException(status_code=401, detail="Invalid sender credentials")

    # Check if recipient exists
    recipient = users.get(recipient_name)
    if not recipient:
        raise HTTPException(status_code=404, detail="Recipient not found")

    # Check for sufficient balance
    if sender["bank_balance"] < amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    # Perform transfer
    sender["bank_balance"] -= amount
    recipient["bank_balance"] += amount

    return {
        "message": "Transfer successful",
        "sender_new_balance": sender["bank_balance"],
        "recipient_authenticated_balance": {"name": recipient_name, "bank_balance": recipient["bank_balance"]}
    }