import random
from collections import deque


class User:
    def __init__(self, name):
        self.name = name


class SocialGraph:
    def __init__(self):
        self.lastID = 0
        self.users = {}
        self.friendships = {}

    def addFriendship(self, userID, friendID):
        """
        Creates a bi-directional friendship
        """
        if userID == friendID:
            print("WARNING: You cannot be friends with yourself")
        elif friendID in self.friendships[userID] or (
                userID in self.friendships[friendID]):
            print("WARNING: Friendship already exists")
        else:
            self.friendships[userID].add(friendID)
            self.friendships[friendID].add(userID)

    def addUser(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.lastID += 1  # increment the ID to assign the new user
        self.users[self.lastID] = User(name)
        self.friendships[self.lastID] = set()

    def populateGraph(self, numUsers, avgFriendships):
        """
        Takes a number of users and an average number of friendships
        as arguments

        Creates that number of users and a randomly distributed friendships
        between those users.

        The number of users must be greater than the average number of
            friendships.
        """

        # Reset graph
        self.lastID = 0
        self.users = {}
        self.friendships = {}

        # Add users
        for user in range(numUsers):
            self.addUser(f'User {user}')

        # Create friendships
        friend_combinations = []

        for i in range(1, numUsers):
            for j in range(i + 1, numUsers):
                friend_combinations.append([i, j])

        random.shuffle(friend_combinations)

        for combo in friend_combinations[:(numUsers * avgFriendships // 2)]:
            self.addFriendship(combo[0], combo[1])

    def getAllSocialPaths(self, userID):
        """
        Takes a user's userID as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.
        """
        visited = {userID: {userID}}
        queue = deque([[userID]])

        while len(queue):
            path = queue.popleft()
            user = path[-1]

            for friend in self.friendships[user]:
                if friend not in visited:
                    new_path = path + [friend]
                    visited[friend] = new_path

                    queue.append(new_path)

        return visited


if __name__ == '__main__':
    import time
    start = time.time()

    sg = SocialGraph()
    sg.populateGraph(100, 4)
    print(sg.friendships)

    end = time.time()
    print(f'{end - start}s')

    start = time.time()

    connections = sg.getAllSocialPaths(1)
    print(connections)

    end = time.time()
    print(f'{end - start}s')
