# BestsellerLLM
The project provides insight on scraping raw data from e-commerce website using [Scrapy](https://scrapy.org/), and we save it to MongoDB using [pymongo item-pipeline](https://docs.scrapy.org/en/latest/topics/item-pipeline.html) method. 
I wrote a series of blog which will help with understanding the project elements and how to implement:
- [[Tale 1] Scraping products using Scrapy + MongoDB.](https://medium.com/@ambesh.sinha/tale-1-scraping-products-using-scrapy-mongodb-8f2c24e120db)
- [[Tale 2] LLM sides with Indexers llama-index + transformers.](https://medium.com/@ambesh.sinha/tale-2-llm-sides-with-indexers-llama-index-transformers-5a3a3ea21ae0)

## Setup:
Create a python environment, I will be using virtual env. Open your OS CLI and run this:
```
python -m venv bestsellerLLM
```
with this you have setup your virtual env, lets intialize it, run the following command from the same directory:
- For windows user:
  ```
  bestsellerLLM\\Scripts\\activate
  ```
- For OSX or Linux users:
  ```
  source bestseller/bin/activate
  ```
Clone this repo:
```
git clone https://github.com/AmbiTyga/BestsellerLLM.git
cd BestsellerLLM
```
Next install dependencies of the project to your virtual env using the `requirements.txt`, by running:
```
pip install -r requirements.txt
```
