from openai import OpenAI

client = OpenAI(
    api_key="AIzaSyAkEbWnW2b-lDKsR90BMKZsNdAEKNGbIJk",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

tools = [
  {
    "type": "function",
    "function": {
      "name": "get_weather",
      "description": "Get the weather in a given location",
      "parameters": {
        "type": "object",
        "properties": {
          "location": {
            "type": "string",
            "description": "The city and state, e.g. Chicago, IL",
          },
          "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
        },
        "required": ["location"],
      },
    }
  }
]



def main():
    messages = [{"role": "user", "content": "What's Weather in Rajasthan Jaipur"}]
    response = client.chat.completions.create(
      model="gemini-2.0-flash",
      messages=messages,
      tools=tools,
      tool_choice="auto"
    )
    if response.choices[0].finish_reason == "tool_calls":
    # Simulating : sends it TaskManager.
    
    # Response from taskmanager
      print(response.choices)
    
    else:
      print(response.choices[0].message.content)
    
import asyncio    
from task_system.task_manager import TaskConsumer, TaskProducer
    
async def main():
    # Initialize the system
    producer = TaskProducer()
    consumer = TaskConsumer(producer)
    
    # Start the consumer in the background
    consumer_task = asyncio.create_task(consumer.start())
    
    # Now your application can assign tasks as needed over time
    # For example, you might have an API endpoint that calls producer.assign_task()
    
    # For demonstration purposes, let's assign a task every few seconds
    for i in range(5):
        # Simulate getting task data from somewhere (API request, etc.)
        task_data = {
            "function_name": "send_email",
            "arguments": {
                "recipient": f"user{i}@example.com",
                "subject": f"Test {i}",
                "body": f"Hello world {i}"
            }
        }
        
        # Assign the task
        task_id = await producer.assign_task(task_data)
        print(f"Assigned task with ID: {task_id}")
        
        # Wait a bit before next task
        await asyncio.sleep(2)
    ### IMPORTANT ------------------------------------------------------
    # In a real application, you might keep the consumer running indefinitely
    # and only stop it when shutting down the application
    await consumer.stop()
    await consumer_task
    
    print("All done!")

if __name__ == "__main__":
    asyncio.run(main())