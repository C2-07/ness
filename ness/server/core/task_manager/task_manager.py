""" To-Do Replace Function_regsitry with actually regsitry from plugins.
"""
from .models import Task, Priority
from typing import Dict
import asyncio

class TaskProducer:
    def __init__(self):
        self.task_queue = asyncio.Queue()
        self.task_results = {}

    async def assign_task(self, task_data: Dict):
        task = Task(
            function_name=task_data['function_name'],
            arguments=task_data.get('arguments'),
            priority=task_data.get('priority', Priority.MEDIUM)
        )
        await self.task_queue.put(task)
        print(f"✅ Task {task.function_name} added to queue with priority {task.priority}")
        return task.id

    async def get_task(self):
        task: Task = await self.task_queue.get()
        print(f"📦 Got task: {task.function_name} ({task.id})")
        return task

    async def get_task_result(self, task_id):
        return self.task_results.get(task_id)
    
    
class TaskConsumer:
    def __init__(self, producer: TaskProducer):
        self.producer = producer
        self.running = False
        
    async def start(self):
        """Start the consumer and keep it running indefinitely."""
        self.running = True
        await self.process_tasks()
        
    async def stop(self):
        """Stop the consumer gracefully."""
        self.running = False
        # Optionally, you can add a dummy task to unblock the consumer
        # if it's waiting at the queue.get() call
        await self.producer.task_queue.put(None)  # Add sentinel value
    
    async def process_tasks(self):
        """Process tasks until explicitly stopped."""
        while self.running:
            task = None  # Initialize task as None
            try:
                # Wait for a task
                task = await self.producer.get_task()
                
                # Execute the task
                result = await self._execute_task(task)
                
                # Store the result
                self.producer.task_results[task.id] = result
                print(f"✓ Task {task.function_name} ({task.id}) completed")
                
                # Mark task as done - ONLY for successful processing
                self.producer.task_queue.task_done()
                
            except asyncio.CancelledError:
                # Handle cancellation - don't call task_done() here
                print("Task processing was cancelled")
                break
            except Exception as e:
                if task:  # Only attempt to record an error if we actually got a task
                    self.producer.task_results[task.id] = {"error": str(e)}
                    print(f"✗ Task {task.function_name} ({task.id}) failed: {e}")
                    # Mark task as done even if it failed
                    self.producer.task_queue.task_done()
    
    async def _execute_task(self, task: Task):
        # Handle sentinel value used for shutdown
        if task is None:
            return None
        
        # Rest of your implementation...
        # This method would contain logic to execute different function types
        # For example, you might have a registry of functions
        function_registry = {
            "send_email": self._send_email,
            "process_data": self._process_data,
            # Add more functions as needed
        }
        
        if task.function_name in function_registry:
            func = function_registry[task.function_name]
            return await func(**task.arguments)
        else:
            raise ValueError(f"Unknown function: {task.function_name}")
    
    # Example task functions
    async def _send_email(self, recipient, subject, body):
        # Mock implementation
        await asyncio.sleep(1)  # Simulate network delay
        return {"status": "sent", "recipient": recipient}
    
    async def _process_data(self, data):
        # Mock implementation
        await asyncio.sleep(0.5)  # Simulate processing time
        return {"processed_items": len(data)}