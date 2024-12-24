class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.prev = None


class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def add_head(self, value):
        """
        Adds specified value to the head of the linked list.
        If adds head to the empty linked list:
            1. Create new node with passed value. Next and prev will be None. Assign both head and tail to this new node
            2. Size++
        If adds head to non-empty linked list:
            1. Create new node with passed value.
            2. next = self.head, prev = None
            3. self.head.prev = new_node
            4. self.head = new_node
            5. Size++
        """
        new_node = Node(value)

        if self.size == 0:
            self.head, self.tail = new_node, new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node

        self.size += 1

    def add_tail(self, value):
        """
        Adds specified value to the tail of the linked list
        If adds tail to the empty linked list:
            1. Create new node with passed value. Next and prev will be none, assign both head an tail to this new node
            2. Size++
        If adds tail to non-empty linked list:
            1. Create new node with specified value
            2. next = null, prev=self.tail
            3. self.tail.next = new_node
            4. self.tail = new_node
            5. Size++
        """
        new_node = Node(value)
        if self.size == 0:
            self.head, self.tail = new_node, new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node

        self.size += 1

    def pop_head(self):
        """
        Removes and returns value from the head of the linked list
        If removes from empty linked list(size == 0):
            1. Return None
        If remove from linked list with one element:
            1. Retrieve value from head
            2. self.head = None
            3. self.tail = None
            4. self.size--
        If remove from linked list with >1 size:
            1. tmp = self.head
            2. new_head = self.head.next
            3. new_head.prev = None
            4. self.head = new_head
            5. self.size--
            6. return tmp.value
        """
        if self.size == 0:
            return None
        elif self.size == 1:
            tmp = self.head
            self.head, self.tail = None, None
            self.size -= 1
            return tmp.value
        else:
            tmp = self.head
            new_head = self.head.next
            new_head.prev = None
            self.head = new_head
            self.size -= 1
            return tmp.value

    def pop_tail(self):
        """
        Removes and returns value from the tail of the linked list
        If removes from empty linked list(size == 0):
            1. Return None
        If remove from linked list with one element:
            1. Retrieve value from tail
            2. self.tail = None
            3. self.head = None
            4. self.size --
        If remove from linked list with >1 size:
            1. tmp = self.tail
            2. new_tail = self.tail.prev
            3. new_tail.next = None
            4. self.tail = new_tail
            5. self.size --
            6. return tmp.value
        """
        if self.size == 0:
            return None
        elif self.size == 1:
            tmp = self.tail
            self.tail, self.head = None, None
            self.size -= 1
            return tmp.value
        else:
            tmp = self.tail
            new_tail = self.tail.prev
            new_tail.next = None
            self.tail = new_tail
            self.size -= 1
            return tmp.value


if __name__ == '__main__':
    a = DoublyLinkedList()
    assert (a.size == 0)
    a.add_head(15)
    assert (a.size == 1)
    assert (a.pop_tail() == 15)
    assert (a.size == 0)

    b = DoublyLinkedList()
    assert (a.size == 0)
    a.add_tail(20)
    assert (a.size == 1)
    assert (a.pop_head() == 20)
    assert (a.size == 0)

    c = DoublyLinkedList()
    c.add_head(1)
    c.add_head(2)
    c.add_head(3)
    c.add_head(4)

    assert (c.pop_head() == 4)
    assert (c.pop_head() == 3)
    assert (c.pop_head() == 2)
    assert (c.pop_head() == 1)

    c.add_head(1)
    c.add_head(2)
    c.add_head(3)
    c.add_head(4)

    assert (c.pop_tail() == 1)
    assert (c.pop_tail() == 2)
    assert (c.pop_tail() == 3)
    assert (c.pop_tail() == 4)