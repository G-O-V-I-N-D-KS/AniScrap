import requests

def search_anime(keyword, page=1, per_page=10):
    url = "https://graphql.anilist.co"

    query = '''
    query ($search: String, $page: Int, $perPage: Int) {
      Page(page: $page, perPage: $perPage) {
        pageInfo {
          total
          currentPage
          lastPage
          hasNextPage
        }
        media(search: $search, type: ANIME) {
          id
          title {
            romaji
            english
            native
          }
          episodes
          averageScore
          startDate {
            year
          }
          season
          seasonYear
          format
          status
          genres
          duration
          description
          coverImage {
            large
          }
          trailer {
            site
            id
          }
          studios(isMain: true) {
            nodes {
              name
            }
          }
        }
      }
    }
    '''

    variables = {
        'search': keyword,
        'page': page,
        'perPage': per_page
    }

    response = requests.post(url, json={'query': query, 'variables': variables})
    if response.status_code != 200:
        print("Error:", response.status_code)
        return None, None

    data = response.json().get('data', {}).get('Page')
    return data.get('media'), data.get('pageInfo')

def get_anime_details_by_id(anime_id):
    url = "https://graphql.anilist.co"

    query = '''
    query ($id: Int) {
      Media(id: $id, type: ANIME) {
        title {
          romaji
          english
          native
        }
        episodes
        averageScore
        startDate {
          year
        }
        season
        seasonYear
        format
        status
        genres
        duration
        description
        coverImage {
          large
        }
        trailer {
          site
          id
        }
        studios(isMain: true) {
          nodes {
            name
          }
        }
        relations {
          edges {
            relationType
            node {
              title {
                romaji
                english
              }
            }
          }
        }
      }
    }
    '''

    response = requests.post(url, json={'query': query, 'variables': {'id': anime_id}})
    if response.status_code != 200:
        print("Error fetching details:", response.status_code)
        return

    data = response.json().get('data', {}).get('Media')
    if not data:
        print("Details not found.")
        return

    # Display main anime info
    print("\n🎬 Selected Anime Details")
    print(f"Cover Image   : {data['coverImage']['large']}")
    print(f"English Title : {data['title'].get('english', 'N/A')}")
    print(f"Romaji Title  : {data['title'].get('romaji', 'N/A')}")
    print(f"Native Title  : {data['title'].get('native', 'N/A')}")
    print(f"Episodes      : {data.get('episodes', 'Unknown')}")
    print(f"Rating        : {data.get('averageScore', 'N/A')}/100")
    print(f"Year          : {data.get('startDate', {}).get('year', 'Unknown')}")
    print(f"Season        : {data.get('season', 'Unknown')} ({data.get('seasonYear', 'Unknown')})")
    print(f"Status        : {data.get('status', 'Unknown')}")
    print(f"Format        : {data.get('format', 'Unknown')}")
    print(f"Duration      : {data.get('duration', 'Unknown')} minutes per episode")
    print(f"Genres        : {', '.join(data.get('genres', []))}")
    print(f"\n📝 Description:\n{data.get('description', 'No description available')}")
    print(f"\n🏢 Studios: {', '.join(studio['name'] for studio in data.get('studios', {}).get('nodes', []))}")

    # Related anime
    print("\n🔗 Related Anime:")
    relations = data.get('relations', {}).get('edges', [])
    if not relations:
        print("  No related anime found.")
    else:
        for rel in relations:
            rel_type = rel.get('relationType', 'Unknown')
            title = rel.get('node', {}).get('title', {}).get('english', 'Unknown')
            print(f"  [{rel_type}] {title}")

# Run the tool
keyword = input("🔍 Enter keyword to search in anime titles: ")
page = 1
per_page = 10

while True:
    anime_list, page_info = search_anime(keyword, page, per_page)
    if not anime_list:
        print("No results.")
        break

    print(f"\n📄 Page {page_info['currentPage']} of {page_info['lastPage']}")
    for idx, anime in enumerate(anime_list, 1):
        title = anime['title'].get('english') or anime['title'].get('romaji') or anime['title'].get('native')
        print(f"{idx}. {title} ({anime.get('startDate', {}).get('year', '?')})")

    print("\nOptions:")
    print("  [1–{}] View details of anime".format(len(anime_list)))
    if page_info['hasNextPage']:
        print("  N - Next page")
    if page > 1:
        print("  P - Previous page")
    print("  Q - Quit")

    choice = input("👉 Enter your choice: ").strip().lower()

    if choice == 'q':
        break
    elif choice == 'n' and page_info['hasNextPage']:
        page += 1
    elif choice == 'p' and page > 1:
        page -= 1
    elif choice.isdigit() and 1 <= int(choice) <= len(anime_list):
        anime_id = anime_list[int(choice) - 1]['id']
        get_anime_details_by_id(anime_id)
        input("\n🔁 Press Enter to go back to results...")
    else:
        print("❗ Invalid input. Try again.")
