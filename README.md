# 📺 AniList Anime Search CLI Tool

A simple command-line interface (CLI) tool to search and explore anime details using the [AniList GraphQL API](https://anilist.gitbook.io/dev-api/). This Python script allows users to search anime by keyword, navigate through paginated results, and view detailed information including cover image, rating, studio, related anime, and more.

---

## 🚀 Features

- 🔍 Search anime by keyword
- 📄 View paginated search results
- 📘 Fetch and display detailed information about selected anime
- 🎞 See related anime entries
- 🏢 View studios, genres, description, trailer link, and more

---

## 🛠️ Requirements

- Python 3.x
- `requests` library

You can install the required library using:


pip install requests


## Sample Output

🔍 Enter keyword to search in anime titles: naruto

📄 Page 1 of 2
1. Naruto (2002)
2. Naruto: Shippuden (2007)
...

Options:
  [1–10] View details of anime
  N - Next page
  Q - Quit
👉 Enter your choice: 2

🎬 Selected Anime Details
English Title : Naruto: Shippuden
Episodes      : 500
Rating        : 85/100
...



```bash