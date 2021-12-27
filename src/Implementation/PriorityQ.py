# # A simple implementation of Priority Queue
# # using Queue.
#
#  # https://www.geeksforgeeks.org/priority-queue-in-python/
#
# class PriorityQueue(object):
#     def __init__(self):
#         self.queue = []
#
#     def __str__(self):
#         return ' '.join([str(i) for i in self.queue])
#
#     # for checking if the queue is empty
#     def isEmpty(self):
#         return len(self.queue) == 0
#
#     # for inserting an element in the queue
#     def insert(self, data):
#         self.queue.append(data)
#
#     # for popping an element based on Priority
#     def delete(self):
#         try:
#             min = len(self.queue) - 1
#             for i in range(len(self.queue)):
#                 if self.queue[i].w < self.queue[min].w:
#                     min = i
#             item = self.queue[min]
#             del self.queue[min]
#             return item
#         except IndexError:
#             print()
#             exit()
# class for Priority queue

# https://stackoverflow.com/questions/9969236/how-to-implement-priority-queues-in-python
class PriorityQueue:

    def __init__(self):
        self.queue = list()
        # if you want you can set a maximum size for the queue

    def insert(self, node):
        # if queue is empty
        if self.size() == 0:
            # add the new node
            self.queue.append(node)
        else:
            # traverse the queue to find the right place for new node
            for x in range(0, self.size()):
                # if the priority of new node is greater
                if node.w >= self.queue[x].w:
                    # if we have traversed the complete queue
                    if x == (self.size() - 1):
                        # add new node at the end
                        self.queue.insert(x + 1, node)
                    else:
                        continue
                else:
                    self.queue.insert(x, node)
                    return True

    def delete(self):
        # remove the first node from the queue
        return self.queue.pop(0)

    def show(self):
        for x in self.queue:
            print(str(x.info) + " - " + str(x.priority))

    def size(self):
        return len(self.queue)
