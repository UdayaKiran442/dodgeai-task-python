**About Repository**
This python service consists of core solution of converting data into knowledge graphs.

**Setup Instructions**
- Clone github repository using below command
```
git clone https://github.com/UdayaKiran442/dodgeai-task-python
```
- Open project folder in any code editor of your choice.
- Create virtual environment 
```
python3 -m venv .venv
source .venv/bin/activate
```
- requirements.txt consists of all dependencies to run the project. Install dependencies using command
```
pip3 install -r requirements.txt
```

**Running the project**
- Create .env file in the root project folder
- Create neo4j account, create instance and download credentials required for running the instance.
- Create Open AI account and generate an API Key for LLM Service.
- In .env file fill the values as mentioned in .env.example file.
- You can run the project using below command
```
fastapi dev
```
- Project will be ruuning in port 8000

**About Project**
- Project demonstrates user support system with help of Konwledge Graphs implemented using neo4j graph database and LLMs.
- All routes related to the project are present in app.py.
- Instance for graph database and LLM are defined in config.py
- controller.py is where core business logic of every route is present.

**Core Implementation Logic**
- We need to develop the project for users to ask queries related to company operations in form of natural language.
- We have data such as products, product descriptions, deliveries, payments, storage locations etc.
- If a user wants to get product description of product id 1, then the query prompt given by user will be converted into cypher query and the query will be executed.
- Example nodes and relationship: PRODUCT - [HAS_PRODUCT_DESCRIPTION] -> PRODUCT_DESCRIPTION
- LLM is used to convert user natural language query prompt into cypher prompt and to interpret the results.

**Script for converting raw data to graph db**
- ```script.py``` file consists of script for converting raw data into nodes and relation ships.
- Data is in form of objects, hence primary value will be identified and graph will be constructed over the primary value.
- Example consider {"product": "3001456", "language": "EN", "productDescription": "WB-CG CHARCOAL GANG"}, here product id is primary and graph can be constructed over product as
PRODUCT - [HAS_PRODUCT_DESCRIPTION] -> PRODUCT_DESCRIPTION.
- When user asks query on "what is product description of product '3001456' ". Then this will be converted into cypher query and result will be passed on to llm and description will be the response to the user.
