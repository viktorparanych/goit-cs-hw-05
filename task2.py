import requests
import string
import matplotlib.pyplot as plt
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor

def map_function(text):
    words = text.split()
    return [(word, 1) for word in words]

def shuffle_function(mapped_values):
    shuffled = defaultdict(list)
    for key, value in mapped_values:
        shuffled[key].append(value)
    return shuffled.items()

def reduce_function(shuffled_values):
    reduced = {}
    for key, values in shuffled_values:
        reduced[key] = sum(values)
    return reduced

def get_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Помилка при завантаженні тексту: {e}")
        return None

def remove_punctuation(text):
    return text.translate(str.maketrans("", "", string.punctuation))

def map_reduce(text):
    text = remove_punctuation(text).lower()
    
    # Для використання багатопотоковості розбиваємо текст на рядки (або частини)
    lines = text.splitlines()
    
    mapped_values = []
    
    #багатопотоковий мапінг
    with ThreadPoolExecutor() as executor:
        # map_function застосовується до кожного рядка тексту паралельно
        results = executor.map(map_function, lines)
        for result in results:
            mapped_values.extend(result)

    #shuffle
    shuffled_values = shuffle_function(mapped_values)

    #редукція
    reduced_values = reduce_function(shuffled_values)

    return reduced_values

def visualize_top_words(word_counts, top_n=10):
    # Сортування словника за спаданням частоти
    sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:top_n]
    
    if not sorted_words:
        print("Немає даних для візуалізації.")
        return

    words, counts = zip(*sorted_words)
    
    plt.figure(figsize=(10, 6))
    
    # [::-1] використовується, щоб найпопулярніше слово було зверху графіка
    plt.barh(words[::-1], counts[::-1], color='skyblue')
    plt.xlabel('Frequency')
    plt.ylabel('Words')
    plt.title('Top 10 Most Frequent Words')
    plt.tight_layout()
    plt.show()

def main():
    #URL приклад
    url = "https://gutenberg.net.au/ebooks01/0100021.txt" # Джордж Орвелл "1984"
    print(f"Завантаження тексту з {url}...")
    
    text = get_text(url)
    
    if text:
        print("Виконання аналізу MapReduce (це може зайняти кілька секунд)...")
        word_counts = map_reduce(text)
        
        print("Візуалізація результатів...")
        visualize_top_words(word_counts, top_n=10)

if __name__ == '__main__':
    main()
