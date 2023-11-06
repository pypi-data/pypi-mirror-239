# PyBingScrapper
Python wrapper for Bing Search results.

## Implementation

```
pip install PyBingScrapper
```

Below is a simple example for running the library

```python
from PyBingScrapper.search import BingSearch

bing = BingSearch("Narendra Modi")
#num - num of results to return
#max_lines - maximum number of lines/sentences to return in each result

bing_results = bing.get_results(num=4, max_lines=15)
# bing_results[i]['content'] - scrapped content
# nlines - num of iterations
# hfkey - hugging face secret key

print(bing.rag_output("Tell me about Mr. Narendra Modi?", bing_results, hfkey, n_iters=15)) #n_iters-optional

```
To only scrape results from the web use the below code snippet

```python
bing = BingSearch("Narendra Modi")
bing_results = bing.get_results(num=4, max_lines=15)

# the above code provides the top 4 results from bing search with 15 sentences from each result as content
```

To implement RAG algorithm over the query use the below. RAG - RAG is a framework/algorithm to improve LLM-generated responses by leveraging external information such as Wikipedia information etc for the queried prompt.

```python
print(bing.rag_output(bing_results, hfkey, n_iters=15))
```

