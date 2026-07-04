from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

class ChatRequest(BaseModel):
    message: str

RESTAURANT_INFO ="""
Restaurant Name: Savora
Cuisine: Italian and Asian Fusion
Hours: Monday - Sunday, 12:00 PM - 11:00 PM
Address: 123 Gulberg Boulevard, Lahore, Pakistan
Phone: +92 300 1234567
Email: hello@savora.com

Most Popular Dishes:
- Wagyu Beef Risotto (Rs 2800) — our most ordered main course
- Truffle Mushroom Pasta (Rs 1850) — customer favourite, highly recommended
- Dark Chocolate Lava Cake (Rs 850) — best-selling dessert
- Truffle Arancini (Rs 950) — most popular starter

For a date night, recommend: Truffle Arancini to start, Wagyu Beef Risotto or 
Truffle Mushroom Pasta as main, Dark Chocolate Lava Cake for dessert.

Reservations:
- Customers can make a reservation directly on our website using the 
  Reservation form in the Reservations section of the page.
- They can also call us at +92 300 1234567
- Or email us at hello@savora.com

Menu - Starters:
- Bruschetta Trio (Rs 850): Toasted artisan bread, fresh tomatoes, basil, garlic, olive oil
- Crispy Spring Rolls (Rs 700): Vegetable-filled rolls, sweet chili dipping sauce
- Truffle Arancini (Rs 950): Crispy risotto balls with truffle and mozzarella
- Edamame with Sea Salt (Rs 600): Steamed soybeans, Himalayan pink salt
- Calamari Fritti (Rs 1000): Lightly fried squid rings, lemon aioli

Menu - Main Course:
- Truffle Mushroom Pasta (Rs 1850): Fettuccine, wild mushrooms, truffle cream sauce
- Teriyaki Glazed Salmon (Rs 2400): Grilled salmon, teriyaki glaze, steamed jasmine rice
- Wagyu Beef Risotto (Rs 2800): Creamy risotto, seared wagyu strips, parmesan
- Szechuan Chicken Stir-Fry (Rs 1700): Wok-tossed chicken, peppers, Szechuan sauce, noodles
- Margherita Flatbread Pizza (Rs 1400): San Marzano tomatoes, fresh mozzarella, basil

Menu - Desserts:
- Classic Tiramisu (Rs 750): Espresso-soaked layers, mascarpone cream
- Matcha Cheesecake (Rs 800): Japanese matcha, creamy cheesecake base
- Dark Chocolate Lava Cake (Rs 850): Warm chocolate cake, molten center, vanilla ice cream

Menu - Drinks:
- Italian Espresso (Rs 400)
- Matcha Latte (Rs 550)
- Fresh Mint Lemonade (Rs 450)
- Sparkling Berry Mocktail (Rs 600)

Dietary options:
- Vegan options: Edamame with Sea Salt, Crispy Spring Rolls, Fresh Mint Lemonade
- Vegetarian options: Bruschetta Trio, Truffle Arancini, Margherita Flatbread Pizza,
  Truffle Mushroom Pasta, all desserts, all drinks
"""

@app.post("/chat")
def chat(request: ChatRequest):
    system_prompt = f"""You are a helpful assistant for Savora restaurant.
Here is all the information about the restaurant: {RESTAURANT_INFO}

Rules:
- Answer ONLY using the information above
- For reservations, always mention the reservation form on the website first
- For popular dishes, refer to the Most Popular Dishes section
- Keep responses short, friendly, and specific
- If something is not in the info above, say you don't have that detail 
  and suggest calling +92 300 1234567"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": request.message}
        ]
    )

    reply = response.choices[0].message.content
    return {"reply": reply}