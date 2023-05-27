# BestsellerLLM
The project provides insight on scraping raw data from e-commerce website using [Scrapy](https://scrapy.org/), and we save it to MongoDB using [pymongo item-pipeline](https://docs.scrapy.org/en/latest/topics/item-pipeline.html) method. 
I wrote a series of blog which will help with understanding the project elements and how to implement:
- [[Tale 1] Scraping products using Scrapy + MongoDB.](https://medium.com/@ambesh.sinha/tale-1-scraping-products-using-scrapy-mongodb-8f2c24e120db)
- [[Tale 2] LLM sides with Indexers llama-index + transformers.](https://medium.com/@ambesh.sinha/tale-2-llm-sides-with-indexers-llama-index-transformers-5a3a3ea21ae0)


## Test Cases:


https://github.com/AmbiTyga/BestsellerLLM/assets/39136064/9f54205a-ec39-4132-8b69-30cf4673d24b



https://github.com/AmbiTyga/BestsellerLLM/assets/39136064/14bff984-2e71-4c86-8fe0-22b22a11d3c7




https://github.com/AmbiTyga/BestsellerLLM/assets/39136064/20a722bb-71b9-448f-8c68-e6c6ea3e62c6



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

## Scraping
First setup your MongoDB, follow the instructions:
- Download MongoDB Compass GUI from [here](https://www.mongodb.com/try/download/compass) and install it in your local system. 
- Open MongoDB compass and connect to your database server or create one if there's not any.
- On the left-hand-side panel, right next to ↻ symbol, there's a ➕symbol. Click it to create a new database. Rename it to amazon.
- Click on the database, and you'll see another ➕symbol, click it to create a new collection. Rename it to bestsellers.

Get back to project directory using your command line interface.
- Move to `./scraper` directory.
```
cd scraper
```
- Initialize the spider using following command:
```
scrapy crawl amzSpider
```

Your data will get dumped into MongoDB database at each extraction

## Loading LLM on UI
> Note: I expect you have 10GB of VRAM in your system, or you are using a dedicated server with GPU runtime.
Move to `./Indexer` directory using command line interface
```
cd Indexer
```
Run the gradio app:
```
python app.py
```
Go to [localhost:8888](https://localhost:8888/)
