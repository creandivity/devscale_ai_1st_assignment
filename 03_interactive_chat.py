import os

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

load_dotenv()

OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

client = OpenAI(base_url=OPENROUTER_BASE_URL, api_key=OPENROUTER_API_KEY)

class Person(BaseModel):
    name: str
    favourite: str
    cannot_eat: str

class Menu(BaseModel):
    name: str
    qty: str
    price: str
    for_who: str    

class Order(BaseModel):
    title: str
    time_available: int
    money_available: int
    time_consumed: int
    money_spend: int
    persons: list[Person]
    menus: list[Menu]

INFORMATION_CONTEXT = """
    Jore Coffee is a Surabaya-based Cafe.
    Menus are:
    Cafe Latte      $5 (Prepare time 5min)
    Espresso        $2 (Prepare time 6min)
    Extra Shot      $2 (Prepare time 3min)
    Milo Ice        $4 (Prepare time 4min)
    Mineral Water   $1 (Prepare time 1min)

    Spaghetti       $10 (Prepare time 10min)
    Chicken Nugget  $5 (Prepare time 7min)
    Spicy Sausage   $8 (Prepare time 8min)
    French Fries    $7 (Prepare time 5min)

    Purchase exceeds $20 will get 10 percent discount.
"""

# fungsi ini untuk menampung inputan user dan mempelajari kebutuhan dari customer.
def generate_raw_information(info: str) -> str:
    SYSTEM_PROMPT = f"""
        You are a cashier for Jore Coffee.
        A customer will come and tell you their needs.
        You need to give recommendation based on customer's need (their available money, time, likes and dislikes etc.)

        Only only menu given from:
        {INFORMATION_CONTEXT}
    """
    completion = client.chat.completions.create(
        model="openai/gpt-5.4",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Customer says: {info}"},
        ],        
    )
    return completion.choices[0].message.content

# berdasarkan info dari function ke-1, hasil akan diolah dan menghasilkan suggestions
def summarize_info(raw_info: str) -> str:
    completion = client.chat.completions.create(
        model="openai/gpt-5.4",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an experienced cashier with expertise of giving recommendation based on customers needs. Break it down clearly, who will get what menu, total time needed, and how much does it cost. Don't forget that all menu listed in {INFORMATION_CONTEXT}"
                ),
            },
            {"role": "user", "content": raw_info},
        ],
    )
    return completion.choices[0].message.content

# suggestion dari function ke-2 akan diparse menjadi bentuk Order
def extract(summarized_content: str) -> Order:    
    completion = client.chat.completions.parse(
        model="openai/gpt-5.4",
        messages=[
            {
                "role": "system",
                "content": (
                    "Extract the order details into the required structured format. "
                    "time_available and money_available are integers (in minutes and dollars)."
                ),
            },
            {"role": "user", "content": summarized_content},
        ],
        response_format=Order,
    )
    return completion.choices[0].message.parsed

# fungsi terakhir untuk menampilkan Order dalam format seperti invoice.
def format_receipt(order: Order) -> str:
    lines = []
    lines.append("=" * 40)
    lines.append(f"  JORE COFFEE - {order.title}")
    lines.append("=" * 40)

    lines.append("\nCustomers:")
    for p in order.persons:
        lines.append(f"  - {p.name} (likes: {p.favourite}, avoids: {p.cannot_eat})")

    lines.append("\nOrder:")
    for m in order.menus:
        lines.append(f"  {m.qty}x {m.name:<20} {m.price:>6}  → {m.for_who}")

    lines.append("-" * 40)
    lines.append(f"  Time available : {order.time_available} min")
    lines.append(f"  Time needed    : {order.time_consumed} min")
    lines.append(f"  Budget         : ${order.money_available}")
    lines.append(f"  Total cost     : ${order.money_spend}")
    lines.append("=" * 40)

    return "\n".join(lines)

topic = input("Tell me about your visit (people, budget, time, preferences): ")

print("\nHere is the information given to our chatbot\n")
raw = generate_raw_information(topic)
print(raw)

print("\nHere are the recommendation made\n")
summary = summarize_info(raw)
print(summary)

print("\nExtract the recommendation\n")
order = extract(summary)
print(order)

print("\nPrint in invoice format\n")
receipt = format_receipt(order)
print(receipt)