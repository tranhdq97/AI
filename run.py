from src.story_retriever.retriever import StoryRetriever


STORY_LINK = "https://truyenfull.vn/thien-dao-do-thu-quan-070820/"
story_retriever = StoryRetriever(STORY_LINK)
story_retriever.run()
