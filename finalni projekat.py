import tkinter as tk
import random
from random import randrange

# Osnovne postavke
width, height = 800, 600
root = tk.Tk()
root.title("Pucaj na cudovista!")

canvas = tk.Canvas(root, width=700, height=500, bg="black")
canvas.pack()

score = 0
health = 3
monsters = []
monster_speed = 300
vrijeme = 60  # trajanje igre u sekundama

# Prikaz rezultata, zdravlja i vremena
label = tk.Label(root, text=f"Rezultat: {score} | Zdravlje: {health} | Vrijeme: {vrijeme}", font=("Arial", 14))
label.pack()

# Funkcija za kreiranje čudovišta
def napravi_cudoviste():
    x = randrange(10, 681)
    y = randrange(10, 481)
    monster = canvas.create_oval(x, y, x+20, y+20, fill="red")
    monsters.append(monster)
    if health > 0 and vrijeme > 0:
        root.after(randrange(1000, 3001), napravi_cudoviste)

# Pomjeranje čudovišta
def pomjeri_cudoviste():
    global health
    for monster in monsters[:]:
        pomak_x = random.choice([5, 0, -5])
        pomak_y = random.choice([5, 0, -5])
        canvas.move(monster, pomak_x, pomak_y)
        x1, y1, x2, y2 = canvas.coords(monster)
        if x1 < 0 or y1 < 0 or x2 > 700 or y2 > 500:
            canvas.delete(monster)
            monsters.remove(monster)
            health -= 1
            update_label()
            if health == 0:
                game_over()
                return
    if health > 0 and vrijeme > 0:
        root.after(monster_speed, pomjeri_cudoviste)

# Pucanje
def pucati(event):
    global score
    pogodio = False

    # Dodaj metak
    metak = canvas.create_oval(event.x-3, event.y-3, event.x+3, event.y+3, fill="green")
    root.after(300, lambda: canvas.delete(metak))

    for monster in monsters[:]:
        x1, y1, x2, y2 = canvas.coords(monster)
        if x1 <= event.x <= x2 and y1 <= event.y <= y2:
            canvas.delete(monster)
            monsters.remove(monster)
            score += 1
            update_label()
            pogodio = True
            if score % 5 == 0 and monster_speed > 100:
                ubrzaj_igru()
            break

    if pogodio:
        prikazi_poruku("Bravo!")

# Ažuriranje prikaza
def update_label():
    label.config(text=f"Rezultat: {score} | Zdravlje: {health} | Vrijeme: {vrijeme}")

# Poruka kad pogodiš
def prikazi_poruku(text):
    poruka = canvas.create_text(350, 30, text=text, fill="yellow", font=("Arial", 20))
    root.after(700, lambda: canvas.delete(poruka))

# Kraj igre
def game_over():
    canvas.create_text(350, 250, text="KRAJ IGRE", fill="white", font=("Arial", 30))

# Ubrzaj igru
def ubrzaj_igru():
    global monster_speed
    monster_speed -= 20

# Odbrojavanje vrijemena
def odbrojavanje():
    global vrijeme
    if vrijeme > 0 and health > 0:
        vrijeme -= 1
        update_label()
        root.after(1000, odbrojavanje)
    elif vrijeme == 0:
        game_over()

# Restart igre
def restartuj_igru():
    global score, health, monsters, monster_speed, vrijeme
    canvas.delete("all")
    score = 0
    health = 3
    vrijeme = 60
    monsters = []
    monster_speed = 300
    update_label()
    napravi_cudoviste()
    pomjeri_cudoviste()
    odbrojavanje()

# Dugme za restart
dugme = tk.Button(root, text="Restartuj igru", command=restartuj_igru)
dugme.pack(pady=10)

canvas.bind("<Button-1>", pucati)

# Pokretanje igre
napravi_cudoviste()
pomjeri_cudoviste()
odbrojavanje()  

