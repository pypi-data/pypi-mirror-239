# The BingSearch class is used to perform web scraping on Bing search results.
import os
import requests
from bs4 import BeautifulSoup
from langchain.llms import HuggingFaceEndpoint, HuggingFaceHub, HuggingFacePipeline
from langchain import PromptTemplate, LLMChain
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document
from langchain.vectorstores import Chroma
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA

class BingSearch:

    def __init__(self, query):
        """
        The function initializes an object with a query parameter.
        
        :param query: The query parameter is a string that represents a query or question that the code
        is trying to address or answer
        """
        self.query = query
    
    def get_results(self, num, max_lines):
        """
        The function `get_results` retrieves search results from Bing based on a given query and returns
        the content of the web pages up to a specified maximum number of lines.
        
        :param num: The `num` parameter is the number of search results you want to retrieve. It
        determines how many search results will be returned in the `content_list`
        :param max_lines: The `max_lines` parameter specifies the maximum number of lines of content to
        retrieve from each URL
        :return: a list of content.
        """
        
        self.num = num
        self.max_lines = max_lines
        
        ua1 = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
        headers = {'User-Agent': ua1}
        
        try:
            bing_url = "https://www.bing.com/search?&q=" + self.query.lower().replace(" ","+")
            result = requests.get(url=bing_url, headers=headers)
            soup = BeautifulSoup(result.text, 'html.parser')
            a_tags = soup.find_all('a', {"class": "b_widePag sb_bp"})
            a_pages = [bing_url] + ["https://www.bing.com" + a['href'] for a in a_tags]
            pg_url_list = []
            content_list = []

            for pg in a_pages:
                res = requests.get(url=pg, headers=headers)
                soup = BeautifulSoup(res.text, 'html.parser')
                a_url_tags = soup.find_all('a', {"class": "tilk"})
                a_url_tags = [a['href'] for a in a_url_tags]
                for u in a_url_tags:
                    pg_url_list.append(u)
            i = 0
            for url_ in a_url_tags:
                if len(self.get_content(url_, self.max_lines)) == 3:
                    content_list.append(self.get_content(url_, self.max_lines))
                if i == self.num:
                    break
                i = i + 1
            return content_list
        
        except Exception as e:
            return str(e)
    
    def get_content(self, url, max_lines):
        """
        The function `get_content` takes a URL and a maximum number of lines as input, retrieves the
        content from the URL, and returns a dictionary containing the URL, title, and a truncated
        version of the content.
        
        :param url: The URL of the webpage you want to scrape the content from
        :param max_lines: The `max_lines` parameter is the maximum number of lines of content that you
        want to retrieve from the webpage
        :return: a dictionary object `u_dict` containing the following keys:
        - 'url': the input URL
        - 'title': the title of the webpage
        - 'content': a string containing the concatenated text of the first `max_lines` paragraphs on
        the webpage, separated by periods ('.')
        """
        
        self.url = url    
        self.max_lines = max_lines
        
        ua1 = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
        headers = {'User-Agent': ua1}
        
        try:
            u_dict = {}
            r = requests.get(self.url, headers=headers)
            soup = BeautifulSoup(r.text, 'html.parser')
            p_tags = soup.find_all('p', limit=self.max_lines)
            p_text = [x.text for x in p_tags]

            u_dict['url'] = self.url
            u_dict['title'] = soup.title.text
            u_dict['content'] = ('.').join(p_text)

            return u_dict
        
        except Exception as e:
            return str(e)
    
    def rag_init(self, query, bingresults):
        """
        The `rag_init` function takes a query and a list of Bing search results, calculates embeddings for
        the text results and the query using HuggingFaceEmbeddings, computes the cosine similarity between
        each text result and the query, and returns the text result with the highest cosine similarity.
        
        :param query: The query parameter is a string that represents the search query or question for which
        you want to find the most relevant result
        :param bingresults: The `bingresults` parameter is a list of dictionaries. Each dictionary
        represents a search result from Bing and contains information about the search result, such as the
        title, URL, and content of the search result
        :return: The function `rag_init` returns the text result from `bingresults` that has the highest
        cosine similarity with the embedded query.
        """
        
        self.query = query
        self.bingresults = bingresults

        texts = [Document(page_content=x['content']) for x in self.bingresults]
        docsearch = Chroma.from_documents(texts, HuggingFaceEmbeddings())
        most_matched = docsearch.similarity_search_with_relevance_scores(self.query)[0][0]
        retriever = docsearch.as_retriever(search_type="mmr", search_kwargs={'fetch_k': 20})

        return most_matched.page_content, retriever
    
    def rag_output(self, bingresults, hf_key, n_iters=15):
        """
        The `rag_output` function takes in a prompt query, number of iterations, Bing search results,
        and Hugging Face API key. It initializes the RAG model, generates a question based on the prompt
        query and Bing search results, and uses the RAG model to generate a response. It repeats this
        process for the specified number of iterations and returns the final question and response.
        
        :param promptquery: The promptquery parameter is a string that represents the initial query or
        prompt for the model. It is the input that the model will use to generate the desired output
        :param n_iters: The `n_iters` parameter specifies the number of iterations or loops to run the
        RAG model. Each iteration generates additional text based on the previous output, allowing the
        model to provide more detailed and comprehensive responses
        :param bingresults: The `bingresults` parameter is used to pass the search results obtained from
        the Bing search engine. It is likely used as input to the `rag_init` function, which initializes
        the RAG (Retrieval-Augmented Generation) model. The specific implementation of `rag_init` is not
        provided
        :param hf_key: The `hf_key` parameter is the Hugging Face API key. It is used to authenticate
        and access the Hugging Face models and resources
        :return: The function `rag_output` returns a string that consists of the original question
        followed by the generated text from the language model.
        """
        
        self.bingresults = bingresults
        self.n_iters = n_iters
        self.hf_key = hf_key
        
        os.environ['HUGGINGFACEHUB_API_TOKEN'] = self.hf_key
        
        rag_input, retriever_pipeline  = self.rag_init(self.query, self.bingresults)
        question = self.query + " Here is the requested information: " + rag_input
        
        try:
            repo_id = "tiiuae/falcon-7b"
            LLM = HuggingFaceHub(
                repo_id=repo_id, model_kwargs={"temperature": 0.6, "top-k": 100, "top-p":.85, "min_new_tokens": 1024, "max_len": 64}
            )
            qa = RetrievalQA.from_chain_type(llm=LLM, chain_type="stuff", retriever=retriever_pipeline, return_source_documents=True)

            for i in range(self.n_iters):
                result = qa({"query": question})
                question = str(question) + str(result['result'])
                
            return question, {"question": self.query + rag_input, "generated-text": question}
        
        except Exception as e:
            return str(e)
