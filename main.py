import base64
import os

import requests
from dotenv import load_dotenv


load_dotenv()

API_URL = "https://api.rodiumai.io/v1"
API_KEY = os.getenv("RODIUMAI_API_KEY")


def get_headers():
    return {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }


def display_error(response):
    print("\nErreur HTTP :", response.status_code)

    try:
        error = response.json().get("error", {})
        print("Code erreur :", error.get("code"))
        print("Message :", error.get("message"))
    except ValueError:
        print("Réponse :", response.text)


def chat():
    question = input("\nVotre question : ")

    data = {
        "model": "openai/gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": question,
            }
        ],
    }

    response = requests.post(
        f"{API_URL}/chat/completions",
        headers=get_headers(),
        json=data,
    )

    if response.status_code != 200:
        display_error(response)
        return "error"

    result = response.json()

    answer = result["choices"][0]["message"]["content"]
    cost = result.get("cost_rodi")

    print("\nRéponse du modèle :")
    print(answer)

    if cost is not None:
        print(f"\nCoût : {cost} RODI")
    else:
        print("\nCoût : non fourni dans la réponse API")

    while True:
        choix = input("\n[r] Refaire le chat  [s] Suivant : ").lower()

        if choix == "r":
            return "repeat"

        if choix == "s":
            return "next"

        print("Choix invalide. Tapez r ou s.")


def image():
    description = input("\nDescription de l'image : ")

    data = {
        "model": "openai/gpt-image-1.5",
        "prompt": description,
        "n": 1,
        "size": "1024x1024",
    }

    response = requests.post(
        f"{API_URL}/images/generations",
        headers=get_headers(),
        json=data,
        timeout=120,
    )

    if response.status_code != 200:
        display_error(response)
        return "error"

    result = response.json()

    image_base64 = result["data"][0]["b64_json"]
    image_bytes = base64.b64decode(image_base64)

    with open("image.png", "wb") as file:
        file.write(image_bytes)

    print("\nImage générée avec succès : image.png")

    while True:
        choix = input(
            "\n[b] Retour  [r] Refaire  [s] Suivant : "
        ).lower()

        if choix == "b":
            return "back"

        if choix == "r":
            return "repeat"

        if choix == "s":
            return "next"

        print("Choix invalide. Tapez b, r ou s.")


def video():
    description = input("\nDescription de la vidéo : ")

    data = {
        "model": "openai/sora-2",
        "prompt": description,
        "duration_seconds": 4,
        "size": "1280x720",
    }

    print("\nGénération de la vidéo en cours...")
    print("Cela peut prendre quelques instants...")

    try:
        response = requests.post(
            f"{API_URL}/videos/generations",
            headers=get_headers(),
            json=data,
            timeout=150,
        )
    except requests.exceptions.RequestException as error:
        print("\nErreur de connexion :", error)
        return "error"

    if response.status_code != 200:
        display_error(response)
        return "error"

    result = response.json()

    try:
        video_base64 = result["data"][0]["b64_json"]
        video_bytes = base64.b64decode(video_base64)

        with open("video.mp4", "wb") as file:
            file.write(video_bytes)

        print("\nVidéo générée avec succès : video.mp4")

    except (KeyError, IndexError, TypeError):
        print("\nLa réponse ne contient pas directement la vidéo en base64.")
        print("Réponse reçue :")
        print(result)
        return "error"

    return "next"


def main():
    if not API_KEY:
        print("Erreur : RODIUMAI_API_KEY est absente.")
        print("Vérifiez votre fichier .env.")
        return

    # Étape 1 : Chat
    while True:
        action = chat()

        if action == "repeat":
            continue

        if action == "next":
            break

        if action == "error":
            return

    # Étape 2 : Image
    while True:
        action = image()

        if action == "repeat":
            continue

        if action == "back":
            print("\nRetour au Chat...")
            return

        if action == "next":
            break

        if action == "error":
            return

    # Étape 3 : Vidéo
    while True:
        action = video()

        if action == "error":
            return

        if action == "next":
            break

    print("\nLes trois étapes sont terminées.")


if __name__ == "__main__":
    main()