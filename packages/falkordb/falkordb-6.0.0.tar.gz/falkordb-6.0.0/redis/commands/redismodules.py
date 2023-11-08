
class RedisModuleCommands:
    """This class contains the wrapper functions to bring supported redis
    modules into the command namespace.
    """

    def graph(self, index_name="idx"):
        """Access the graph namespace, providing support for
        redis graph data.
        """

        from .graph import Graph

        g = Graph(client=self, name=index_name)
        return g


class AsyncRedisModuleCommands(RedisModuleCommands):

    def graph(self, index_name="idx"):
        """Access the graph namespace, providing support for
        redis graph data.
        """

        from .graph import AsyncGraph

        g = AsyncGraph(client=self, name=index_name)
        return g
