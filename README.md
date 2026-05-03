# devscale_ai_1st_assignment
Repo ini untuk tugas pertama kelas AI Python Enabled Devscale (Class 03)

File yang digunakan adalah 03_interactive_chat.py.

Assignment ke 1:
- Membuat simple chat bot.
- Topic yang dibuat adalah cafe recommendation system
- Input yang diharapkan dari user adalah : menyebutkan jumlah orang, favorite/menu yang tidak disukai oleh seseorang, jumlah uang dan waktu yang tersedia sebagai constraint.
- Function yang dibuat menjadi 3 pipeline utama + 1 function tambahan untuk memformat output dalam bentuk invoice
  a. generate_raw_information --> untuk menampung inputan user dan memproses informasi
  b. summarize_info --> stelah mengolah informasi, menghasilkan rekomendasi user
  c. extract --> mengextract information menjadi structured (Order)
  d. tambahan function untuk memprint-out model invoice.

Case 1:
Inputan user : 
I am with my children. Chopper and Nami. Chopper love sausage and can eat spicy food. Nami cannot eat spicy, but really love chocolate drink. we have 1 hour to eat. I bring $50 with me.

Final Output:
```
-----------------------------------------
  JORE COFFEE - Food Order Recommendation
-----------------------------------------

Customers:
  - Elon (likes: sausage, spicy food, avoids: )
  - Mia (likes: chocolate drink, non-spicy food, avoids: spicy food)
  - You (likes: cafe latte, avoids: )

Order:
  1x Spicy Sausage             8  → Elon
  1x Milo Ice                  4  → Mia
  1x Chicken Nugget            5  → Mia
  1x Cafe Latte                5  → You
  1x French Fries              7  → To share
----------------------------------------
  Time available : 8 min
  Time needed    : 8 min
  Budget         : $50
  Total cost     : $26
-----------------------------------------
```

Case 2
Inputan User:
I and John need to grab a coffee for each of us as we walk into our office. we also need light snack to eat during our walk. We only bring $15 each. FYI, i am a little bit sleepier than John today, but John is hungrier than me.

Final Output
```
========================================
  JORE COFFEE - Recommended order
========================================

Customers:
  - You (likes: Cafe Latte, Extra Shot, Chicken Nugget, avoids: )
  - John (likes: Cafe Latte, French Fries, avoids: )

Order:
  1x Cafe Latte                5  → You
  1x Extra Shot                2  → You
  1x Chicken Nugget            5  → You
  1x Cafe Latte                5  → John
  1x French Fries              7  → John
----------------------------------------
  Time available : 7 min
  Time needed    : 7 min
  Budget         : $30
  Total cost     : $21
========================================
```
