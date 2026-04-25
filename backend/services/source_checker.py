# import os
# import requests
# from dotenv import load_dotenv

# load_dotenv()

# NEWS_API_KEY = os.getenv('NEWS_API_KEY')
# NEWS_API_URL = "https://newsapi.org/v2/everything"

# def check_sources(text: str, limit: int = 5) -> dict:
#     """
#     Check if news sources cover similar topics
    
#     Args:
#         text: Text to search for
#         limit: Number of articles to fetch
        
#     Returns:
#         Dictionary with sources and credibility
#     """
#     try:
#         if not NEWS_API_KEY:
#             print("⚠️ News API key not found, using mock")
#             return mock_source_check(text)
        
#         keywords = ' '.join(text.split()[:5])
        
#         params = {
#             'q': keywords,
#             'apiKey': NEWS_API_KEY,
#             'sortBy': 'relevancy',
#             'pageSize': limit,
#             'language': 'en'
#         }
        
#         response = requests.get(NEWS_API_URL, params=params, timeout=10)
        
#         if response.status_code == 200:
#             data = response.json()
#             articles = data.get('articles', [])
            
#             sources = []
#             credible_sources = 0
            
#             for article in articles:
#                 source_data = {
#                     'source': article.get('source', {}).get('name', 'Unknown'),
#                     'title': article.get('title', ''),
#                     'url': article.get('url', ''),
#                     'publishedAt': article.get('publishedAt', '')
#                 }
#                 sources.append(source_data)
#                 credible_sources += 1
            
#             credibility_score = min(30, credible_sources * 6)
            
#             return {
#                 "sources_found": len(sources),
#                 "sources": sources,
#                 "credibility_score": credibility_score,
#                 "has_coverage": len(sources) > 0
#             }
#         else:
#             return {
#                 "sources_found": 0,
#                 "sources": [],
#                 "credibility_score": 0,
#                 "has_coverage": False
#             }
            
#     except Exception as e:
#         print(f"❌ Source check error: {str(e)}")
#         return mock_source_check(text)

# def mock_source_check(text: str) -> dict:
#     """Mock source check"""
#     return {
#         "sources_found": 0,
#         "sources": [],
#         "credibility_score": 0,
#         "has_coverage": False
#     }