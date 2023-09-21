# Rami Chatbot

## Problem Statement

The Rami Chatbot project aims to create an intelligent chatbot capable of handling food orders from customers. The chatbot assists users in placing food orders, tracking orders, and providing information about the store's operating hours. It is designed to enhance the user experience and streamline the ordering process.

## Project Inspiration

Inspired by the Codebasics YouTube channel.

[Watch the video](https://www.youtube.com/watch?v=2e5pQqBvGco)


## Improvements

### Database Normalization

Implemented first normal form (1NF) and second normal form (2NF) to optimize data organization and efficiency.

### 1. First Normal Form (1NF)

Split the table into "orders" and "orderitems."

**Table "orders":**
- order_id (primary key, auto increment)
- total_price

### 2. Second Normal Form (2NF)

Introduced the "orderitems" table.

**Table "orderitems":**
- order_id (foreign key to "orders" table)
- food_id
- quantity
- price
- food_name

Achieved a normalized database structure for efficient data management.

## Code Enhancements

Implemented logging and exception handling for improved reliability.

### Logging

Comprehensive logging system for method execution and error tracking.

### Exception Handling

Structured exception handling ensures graceful error recovery.

## How to Run

1. **Clone the Repository:**
   Clone the repository to your local machine:

   ```shell
   git clone https://github.com/your-username/rami-chatbot.git
   ```

2. **Setup the conda environment and install the requirements.txt file:**
   ```shell
   pip install -r requirements.txt
   ```

3. **Since this project is based on FastAPI we need to run Uvicorn:**
   ```shell
   python -m uvicorn main:app --reload
   ```

4. **Open another terminal and execute the following command:**
   ```shell
   ngrok http 8000
   ```

5. **Paste the 'https' link in fulfillment tab of DialogFlow**