import queue

class MaxPriorityQueue(queue.PriorityQueue):
    def __init__(self):
        super().__init__()

    def put(self, item, priority):
        super().put((-priority, item))

    def get(self):
        _, item = super().get()
        return item
    
    def pop(self):
        priority, item = super().get()
        return item, -priority

# Example usage:
max_pq = MaxPriorityQueue()

max_pq.put('task1', 5)
max_pq.put('task2', 10)
max_pq.put('task3', 3)

print(max_pq.get())  # Output: task2
print(max_pq.get())  # Output: task1
print(max_pq.get())  # Output: task3

max_pq.pop()
