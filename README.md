# Python Language Learning Bot

## Overview

This repository contains the code for a Python-based language learning bot designed to help users practice vocabulary and translation skills. The bot generates language exercises tailored to the user’s proficiency level (A1 to C2) and their available study time. Exercises include translation tasks (both directions) and multiple-choice questions, making it easy for users to improve their language skills through interactive text-based exercises.

### Features:
- **Customizable Exercises:** Tailors language exercises based on the user's input language, level, and study time.
- **Bilingual Translation Tasks:** Presents words for translation from English to the desired language and vice versa.
- **Multiple-Choice Questions:** Offers questions with 3 possible answers to challenge the user’s vocabulary.
- **Text-Based Interactions:** All exercises are designed for clear text-based interactions.

## Usage

To use the bot, clone the repository and follow these steps:

1. **Installation:**
   Make sure you have Python installed. If not, download and install it from [here](https://www.python.org/downloads/).

   Install the required dependencies by running:
   ```bash
   pip install -r requirements.txt
   ```

2. **Running the Bot:**
   Run the main script to start generating exercises based on user inputs:
   ```bash
   python bot.py
   ```

3. **User Inputs:**
   When running the bot, users will need to input:
   - Desired language
   - Proficiency level (A1 to C2)
   - Study time (in minutes)

   Example input flow:
   ```
   Enter your desired language: Spanish
   Enter your proficiency level (A1 to C2): A2
   How much time do you have for studying (in minutes)? 20
   ```

4. **Exercise Generation:**
   The bot will then generate a set of 10 exercises tailored to the user's level and time, divided between translation tasks and multiple-choice questions.

### Example Output:

```
1. Translate the following word into Spanish: "dog".
2. ¿Cómo se dice "casa" en inglés?
3. Translate the following word into Spanish: "chair".
4. ¿Cómo se dice "perro" en inglés?
5. Choose the correct translation for "book": 
   a) casa 
   b) coche 
   c) libro
6. Translate the following word into Spanish: "window".
7. ¿Cómo se dice "puerta" en inglés?
8. Translate the following word into Spanish: "sun".
9. ¿Cómo se dice "luna" en inglés?
10. Choose the correct translation for "cat":
    a) perro 
    b) gato 
    c) caballo
```

## File Structure

- `bot.py`: Main script for the bot.
- `README.md`: This readme file with usage instructions.
- `requirements.txt`: Python dependencies required to run the bot.

## Contributing

Contributions are welcome! If you'd like to add features or fix bugs, feel free to submit a pull request. Please make sure to write clear commit messages and update the documentation as necessary.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.